import re
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    Pattern,
    Tuple,
    Type,
    Union,
)

from fastapi import APIRouter, Body, Depends
from fastapi._compat import field_annotation_is_scalar
from fastapi.types import IncEx
from sqlalchemy import Column, Table, func
from sqlalchemy.engine import Result
from sqlalchemy.future import select
from sqlalchemy.orm import InstrumentedAttribute, Session, object_session
from sqlalchemy.sql import Select
from sqlalchemy.sql.elements import BinaryExpression, Label, UnaryExpression
from starlette.requests import Request
from typing_extensions import Annotated, Literal

from fastapi_amis_admin.utils.pydantic import (
    PYDANTIC_V2,
    ModelField,
    ValueItems,
    annotation_outer_type,
    create_model_by_fields,
    field_allow_none,
    model_fields,
)

try:
    from functools import cached_property
except ImportError:
    from sqlalchemy.util.langhelpers import memoized_property as cached_property

from .base import (
    BaseCrud,
    SchemaCreateT,
    SchemaFilterT,
    SchemaListT,
    SchemaModelT,
    SchemaReadT,
    SchemaUpdateT,
)
from .parser import (
    SqlaField,
    SqlaInsAttr,
    SqlaPropertyField,
    TableModelParser,
    TableModelT,
    get_modelfield_by_alias,
    get_python_type_parse,
    parse_obj_to_schema,
)
from .schema import BaseApiOut, ItemListSchema
from .utils import (
    IdStrQuery,
    ItemIdListDepend,
    SqlalchemyDatabase,
    get_engine_db,
    parser_str_set_list,
)

sql_operator_pattern: Pattern = re.compile(r"^\[(=|<=|<|>|>=|!|!=|<>|\*|!\*|~|!~|-)]")
sql_operator_map: Dict[str, str] = {
    "=": "__eq__",
    "<=": "__le__",
    "<": "__lt__",
    ">": "__gt__",
    ">=": "__ge__",
    "!": "__ne__",
    "!=": "__ne__",
    "<>": "__ne__",
    "*": "in_",
    "!*": "not_in",
    "~": "like",
    "!~": "not_like",
    "-": "between",
}


class SqlalchemySelector(Generic[TableModelT]):
    model: Type[TableModelT] = None  # SQLModel,DeclarativeMeta,InspectTable
    fields: List[SqlaField] = []  # Need to query the field from the database
    list_filter: List[SqlaField] = []  # Query filterable fields
    exclude: List[SqlaInsAttr] = []  # Model fields that do not need to be queried. It is not recommended to use.
    ordering: List[Union[SqlaField, UnaryExpression]] = []  # Default sort field
    link_models: Dict[str, Tuple[Type[Table], Column, Column]] = None  # Link table information
    """Relate information of the target model with the current model.
    - The Data structure is: {Target table name: (link model table,
        Column in the link model table associated with the current model,
        Column in the link model table associated with the target model)}
    - E.g. the current model is Role, you can add the target model User through `User.roles` here.
        And then you can query the Role through the primary key field of the target model User.
    - Saved information: {auth_user: (auth_user_roles, auth_user_roles.role_id, auth_user_roles.user_id)}
    - You can add the query parameters to the route url to access the role list of the user:
        `?link_model=auth_user&link_item_id={user_id}`.
    """
    pk_name: str = "id"  # Primary key name

    def __init__(self, model: Type[TableModelT] = None, fields: List[SqlaField] = None) -> None:
        self.model = model or self.model
        assert self.model, "model is None"
        assert hasattr(self.model, "__table__"), "model must be has __table__ attribute."
        self.pk_name: str = self.pk_name or self.model.__table__.primary_key.columns.keys()[0]
        self.pk: InstrumentedAttribute = self.model.__dict__[self.pk_name]
        self.parser = TableModelParser(self.model)
        fields = fields or self.fields or self.model_insfields
        exclude = self.parser.filter_insfield(self.exclude)
        self.fields = [
            sqlfield
            for sqlfield in self.parser.filter_insfield(fields + [self.pk], save_class=(Label,))
            if sqlfield not in exclude
        ]
        assert self.fields, "fields is None"
        self.list_filter = self.list_filter and self.list_filter.copy() or self.fields
        self.link_models = self.link_models or {}
        """Make sure the value of link_models is an object attribute, not a class attribute."""

    @cached_property
    def model_insfields(self) -> List[SqlaInsAttr]:
        return self.parser.filter_insfield(self.model.__dict__.values())

    @cached_property
    def _select_entities(self) -> Dict[str, Union[InstrumentedAttribute, Label]]:
        return {self.parser.get_alias(insfield): insfield for insfield in self.fields}

    @cached_property
    def _filter_entities(self) -> Dict[str, Union[InstrumentedAttribute, Label]]:
        return {
            self.parser.get_alias(sqlfield): sqlfield
            for sqlfield in self.parser.filter_insfield(self.list_filter, save_class=(Label,))
        }

    async def get_select(self, request: Request) -> Select:
        return select(*self._select_entities.values())

    def _calc_ordering(self, orderBy, orderDir):
        sqlfield = self._select_entities.get(orderBy, self._filter_entities.get(orderBy))
        order = None
        if sqlfield is not None:
            order = sqlfield.desc() if orderDir == "desc" else sqlfield.asc()
            return [order]
        elif self.ordering is not None:
            order = self.parser.filter_insfield(
                self.ordering,
                save_class=(
                    UnaryExpression,
                    Label,
                ),
            )
        return order

    @property
    def _select_maker(self):
        if self.link_models:

            def select_maker(
                sel: Annotated[Select, Depends(self.get_select)],  # type: ignore
                link_clause: Annotated[Optional[Any], Depends(self.get_link_clause)] = None,  # type: ignore
            ) -> Select:
                if link_clause is not None:
                    sel = sel.where(link_clause)
                return sel

        else:
            select_maker = self.get_select
        return select_maker

    async def get_link_clause(
        self,
        request: Request,
        link_model: str = None,
        link_item_id: IdStrQuery = None,
        op: Literal["in_", "not_in", None] = None,
    ) -> Optional[Any]:
        if link_model and link_item_id:
            result = self.link_models.get(link_model)
            if not result:
                return None
            table, pk_col, link_col = result
            if table is not None:
                link_item_id = list(
                    map(
                        get_python_type_parse(link_col),
                        parser_str_set_list(link_item_id),
                    )
                )
                if op == "not_in":
                    return self.pk.not_in(select(pk_col).where(link_col.in_(link_item_id)))
                else:
                    return self.pk.in_(select(pk_col).where(link_col.in_(link_item_id)))
        return None

    @staticmethod
    def _parser_query_value(
        value: Any, operator: str = "__eq__", python_type_parse: Callable = str
    ) -> Tuple[Optional[str], Union[tuple, None]]:
        if isinstance(value, str):
            if not value:
                return None, None
            match = sql_operator_pattern.match(value)
            if match:
                op_key = match.group(1)
                operator = sql_operator_map.get(op_key)
                value = value.replace(f"[{op_key}]", "")
                if not value:
                    return None, None
                if operator in ["like", "not_like"] and value.find("%") == -1:
                    return operator, (f"%{value}%",)
                elif operator in ["in_", "not_in"]:
                    return operator, (list(map(python_type_parse, set(value.split(",")))),)
                elif operator == "between":
                    value = value.split(",")[:2]
                    if len(value) < 2:
                        return None, None
                    return operator, tuple(map(python_type_parse, value))
        return operator, (python_type_parse(value),)

    def calc_filter_clause(self, data: Dict[str, Any]) -> List[BinaryExpression]:
        lst = []
        for k, v in data.items():
            sqlfield = self._filter_entities.get(k)
            if sqlfield is not None:
                operator, val = self._parser_query_value(v, python_type_parse=get_python_type_parse(sqlfield))
                if operator:
                    lst.append(getattr(sqlfield, operator)(*val))
        return lst


class SqlalchemyCrud(
    BaseCrud[SchemaModelT, SchemaListT, SchemaFilterT, SchemaCreateT, SchemaReadT, SchemaUpdateT], SqlalchemySelector[TableModelT]
):
    engine: SqlalchemyDatabase = None  # sqlalchemy engine
    create_fields: List[SqlaInsAttr] = []  # Create item data field
    create_exclude: Optional[IncEx] = None
    """create exclude fields, such as: {'id', 'key', 'name'} or {'id': True, 'category': {'id', 'name'}}."""
    update_fields: List[SqlaPropertyField] = []
    """model update fields;support model property and relationship field."""
    update_exclude: Optional[IncEx] = None
    """update exclude fields, such as: {'id', 'key', 'name'} or {'id': True, 'category': {'id', 'name'}}."""
    read_fields: List[SqlaPropertyField] = []
    """Model read fields; used in route_read, note the difference between readonly_fields and read_fields.
    default is None, means not use read route."""

    def __init__(
        self,
        model: Type[TableModelT],
        engine: SqlalchemyDatabase,
        fields: List[SqlaField] = None,
        router: APIRouter = None,
    ) -> None:
        self.engine = engine or self.engine
        assert self.engine, "engine is None"
        self.db = get_engine_db(self.engine)
        SqlalchemySelector.__init__(self, model, fields)
        schema_model: Type[SchemaModelT] = self.schema_model or TableModelParser.get_table_model_schema(model)
        BaseCrud.__init__(self, schema_model, router)
        # if self.readonly_fields:
        #     logging.warning(
        #         "readonly fields, deprecated, not recommended, will be removed in version 0.4.0."
        #         "Please replace them with update_fields and update_exclude."
        #     )

    @property
    def router_prefix(self):
        return f"/{self.model.__name__}"

    def _create_schema_list(self) -> Type[SchemaListT]:
        # Get the model fields from the select entities
        modelfields = self.parser.filter_modelfield(
            self._select_entities.values(),
            save_class=(
                Label,
                ModelField,
            ),
        )
        # Create the schema using the model fields
        return create_model_by_fields(
            name=f"{self.schema_name_prefix}List",
            fields=modelfields,
            set_none=True,
            extra="allow",
        )

    def _create_schema_filter(self) -> Type[SchemaFilterT]:
        # Get the filter fields from the list filter or select entities
        list_filter = self.list_filter or self._select_entities.values()
        # Filter out the model fields from the filter fields
        modelfields = self.parser.filter_modelfield(list_filter, save_class=(Label,))
        # Modify the modelfields if necessary
        for modelfield in modelfields:
            type_ = annotation_outer_type(modelfield.type_)
            if field_annotation_is_scalar(modelfield.type_) and issubclass(type_, (Enum, bool, str)):
                continue
            if PYDANTIC_V2:
                modelfield.field_info.annotation = str
            else:
                modelfield.type_ = str
                modelfield.outer_type_ = str
                modelfield.validators = []
        # Create the schema using the model fields
        return create_model_by_fields(
            name=f"{self.schema_name_prefix}Filter",
            fields=modelfields,
            set_none=True,
        )

    def _create_schema_read(self) -> Optional[Type[SchemaReadT]]:
        if not self.read_fields:
            return None
        # Filter out any non-model fields from the read fields
        modelfields = self.parser.filter_modelfield(self.read_fields)
        # Create the schema using the model fields
        return create_model_by_fields(
            name=f"{self.schema_name_prefix}Read",
            fields=modelfields,
            orm_mode=True,
        )

    def _create_schema_update(self) -> Type[SchemaUpdateT]:
        # Set the update fields to the model insfields if not provided
        self.update_fields = self.update_fields or self.model_insfields
        # Exclude certain fields if specified
        exclude = {k for k, v in ValueItems.merge(self.update_exclude, {}).items() if not isinstance(v, (dict, list, set))} or {
            self.pk_name
        }
        # Filter out any non-model fields from the update fields
        modelfields = self.parser.filter_modelfield(self.update_fields, exclude=exclude)
        # Create the schema using the model fields
        return create_model_by_fields(
            name=f"{self.schema_name_prefix}Update",
            fields=modelfields,
            set_none=True,
        )

    def _create_schema_create(self) -> Type[SchemaCreateT]:
        # Set the create fields to the model insfields if not provided
        self.create_fields = self.create_fields or self.model_insfields
        # Exclude certain fields if specified
        exclude = {k for k, v in ValueItems.merge(self.create_exclude, {}).items() if not isinstance(v, (dict, list, set))} or {
            self.pk_name
        }
        # Filter out any non-model fields from the create fields
        modelfields = self.parser.filter_modelfield(self.create_fields, exclude=exclude)
        # Create the schema using the model fields
        return create_model_by_fields(
            name=f"{self.schema_name_prefix}Create",
            fields=modelfields,
        )

    def create_item(self, item: Dict[str, Any]) -> TableModelT:
        """Create a database orm object through a dictionary."""
        return self.model(**item)

    def read_item(self, obj: TableModelT) -> SchemaReadT:
        """read database data and parse to schema_read"""
        return parse_obj_to_schema(obj, self.schema_read)

    def update_item(self, obj: TableModelT, values: Dict[str, Any]) -> None:
        """update schema_update data to database,support relational attributes"""
        for k, v in values.items():
            field = get_modelfield_by_alias(self.model, k)
            if not field and not hasattr(obj, k):
                continue
            name = field.name if field else k
            if isinstance(v, dict):
                # Relational attributes, nested;such as: setattr(article.content, "body", "new body")
                sub = getattr(obj, name)
                if not isinstance(sub, dict):  # Ensure that the attribute is an object.
                    self.update_item(sub, v)
                    continue
            setattr(obj, name, v)

    def delete_item(self, obj: TableModelT) -> None:
        """delete database data"""
        object_session(obj).delete(obj)

    def list_item(self, values: Dict[str, Any]) -> SchemaListT:
        """Parse the database data query result dictionary into schema_list."""
        return self.schema_list.parse_obj(values)

    def _fetch_item_scalars(self, session: Session, item_id: Iterable[str]) -> List[TableModelT]:
        sel = select(self.model).where(self.pk.in_(list(map(get_python_type_parse(self.pk), item_id))))
        return session.scalars(sel).all()

    async def fetch_items(self, *item_id: str) -> List[TableModelT]:
        """Fetch the database data by id."""
        return await self.db.async_run_sync(self._fetch_item_scalars, item_id)

    def _create_items(self, session: Session, items: List[Dict[str, Any]]) -> List[TableModelT]:
        if not items:
            return []
        objs = [self.create_item(item) for item in items]
        session.add_all(objs)
        session.flush()
        return objs

    async def create_items(self, request: Request, items: List[SchemaCreateT]) -> List[TableModelT]:
        """Create multiple database data."""
        items = [await self.on_create_pre(request, obj) for obj in items]
        return await self.db.async_run_sync(self._create_items, items)

    def _read_items(self, session: Session, item_id: List[str]) -> List[SchemaReadT]:
        items = self._fetch_item_scalars(session, item_id)
        return [self.read_item(obj) for obj in items]

    async def read_items(self, request: Request, item_id: List[str]) -> List[SchemaReadT]:
        """Fetch the database data by id."""
        return await self.db.async_run_sync(self._read_items, item_id)

    def _update_items(self, session: Session, item_id: List[str], values: Dict[str, Any]) -> List[TableModelT]:
        items = self._fetch_item_scalars(session, item_id)
        for item in items:
            self.update_item(item, values)
        return items

    async def update_items(self, request: Request, item_id: List[str], values: Dict[str, Any]) -> List[TableModelT]:
        """Update the database data by id."""
        return await self.db.async_run_sync(self._update_items, item_id, values)

    def _delete_items(self, session: Session, item_id: List[str]) -> List[TableModelT]:
        items = self._fetch_item_scalars(session, item_id)
        for item in items:
            self.delete_item(item)
        return items

    async def delete_items(self, request: Request, item_id: List[str]) -> List[TableModelT]:
        """Delete the database data by id."""
        return await self.db.async_run_sync(self._delete_items, item_id)

    @property
    def schema_name_prefix(self):
        if self.__class__ is SqlalchemyCrud:
            return self.model.__name__
        return super().schema_name_prefix

    async def on_create_pre(self, request: Request, obj: SchemaCreateT, **kwargs) -> Dict[str, Any]:
        data = obj.dict(by_alias=True)  # exclude=set(self.pk)
        if self.pk_name in data and not data.get(self.pk_name):
            del data[self.pk_name]
        return data

    async def on_update_pre(
        self,
        request: Request,
        obj: SchemaUpdateT,
        item_id: Union[List[str], List[int]],
        **kwargs,
    ) -> Dict[str, Any]:
        data = obj.dict(exclude=self.update_exclude, exclude_unset=True, by_alias=True)
        data = {key: val for key, val in data.items() if val is not None or field_allow_none(model_fields(self.model)[key])}
        return data

    async def on_filter_pre(self, request: Request, obj: Optional[SchemaFilterT], **kwargs) -> Dict[str, Any]:
        return obj and {k: v for k, v in obj.dict(exclude_unset=True, by_alias=True).items() if v is not None}

    async def on_list_after(self, request: Request, result: Result, data: ItemListSchema, **kwargs) -> ItemListSchema:
        """Parse the database data query result dictionary into schema_list."""
        data.items = self.parser.conv_row_to_dict(result.all())
        data.items = [self.list_item(item) for item in data.items]
        return data

    @property
    def AnnotatedSelect(self):
        """Annotated Select, used to automatically perform fastapi dependency injection"""
        return Annotated[Select, Depends(self._select_maker)]

    @property
    def AnnotatedItemIdList(self):
        """Annotated Item ID List, used to filter the id of the data that the user has permission to operate on.
        And automatically perform fastapi dependency injection
        """
        return Annotated[List[str], Depends(self.filtered_item_id)]

    @property
    def filtered_item_id(self) -> Callable:
        """Filter the id of the data that the user has permission to operate on."""

        async def depend(
            item_id: ItemIdListDepend,
            sel: self.AnnotatedSelect,  # type: ignore
        ):
            item_id = list(map(get_python_type_parse(self.pk), item_id))
            filtered_id = await self.db.async_scalars(sel.where(self.pk.in_(item_id)).with_only_columns(self.pk))
            return filtered_id.all()

        return depend

    @property
    def route_list(self) -> Callable:
        async def route(
            request: Request,
            sel: self.AnnotatedSelect,  # type: ignore
            paginator: Annotated[self.paginator, Depends()],  # type: ignore
            filters: Annotated[self.schema_filter, Body()] = None,  # type: ignore
        ):
            if not await self.has_list_permission(request, paginator, filters):
                return self.error_no_router_permission(request)
            data = ItemListSchema(items=[])
            data.query = request.query_params
            if await self.has_filter_permission(request, filters):
                data.filters = await self.on_filter_pre(request, filters)
                if data.filters:
                    sel = sel.filter(*self.calc_filter_clause(data.filters))
            if paginator.show_total:
                data.total = await self.db.async_scalar(
                    select(func.count("*")).select_from(sel.with_only_columns(self.pk).subquery())
                )
            orderBy = self._calc_ordering(paginator.orderBy, paginator.orderDir)
            if orderBy:
                sel = sel.order_by(*orderBy)
            sel = sel.limit(paginator.perPage).offset((paginator.page - 1) * paginator.perPage)
            result = await self.db.async_execute(sel)
            return BaseApiOut(data=await self.on_list_after(request, result, data))

        return route

    @property
    def route_create(self) -> Callable:
        async def route(
            request: Request,
            data: Annotated[Union[List[self.schema_create], self.schema_create], Body()],  # type: ignore
        ) -> BaseApiOut[Union[int, self.schema_model]]:  # type: ignore
            if not await self.has_create_permission(request, data):
                return self.error_no_router_permission(request)
            if not isinstance(data, list):
                data = [data]
            try:
                items = await self.create_items(request, data)
            except Exception as error:
                await self.db.async_rollback()
                return self.error_execute_sql(request=request, error=error)
            result = len(items)
            if result == 1:  # if only one item, return the first item
                result = await self.db.async_run_sync(lambda _: parse_obj_to_schema(items[0], self.schema_model, refresh=True))
            return BaseApiOut(data=result)

        return route

    @property
    def route_read(self) -> Callable:
        async def route(
            request: Request,
            item_id: self.AnnotatedItemIdList,  # type: ignore
        ):
            if not await self.has_read_permission(request, item_id):
                return self.error_no_router_permission(request)
            items = await self.read_items(request, item_id)
            return BaseApiOut(data=items if len(items) > 1 else items[0])

        return route

    @property
    def route_update(self) -> Callable:
        async def route(
            request: Request,
            item_id: self.AnnotatedItemIdList,  # type: ignore
            data: Annotated[self.schema_update, Body()],  # type: ignore
        ):
            if not await self.has_update_permission(request, item_id, data):
                return self.error_no_router_permission(request)
            values = await self.on_update_pre(request, data, item_id=item_id)
            if not values:
                return self.error_data_handle(request)
            items = await self.update_items(request, item_id, values)
            return BaseApiOut(data=len(items))

        return route

    @property
    def route_delete(self) -> Callable:
        async def route(
            request: Request,
            item_id: self.AnnotatedItemIdList,  # type: ignore
        ):
            if not await self.has_delete_permission(request, item_id):
                return self.error_no_router_permission(request)
            items = await self.delete_items(request, item_id)
            return BaseApiOut(data=len(items))

        return route
