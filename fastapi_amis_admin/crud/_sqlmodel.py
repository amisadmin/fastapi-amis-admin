import datetime
import re
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Pattern, Tuple, Type, Union

from fastapi import APIRouter, Body, Depends, Query
from pydantic import BaseModel, Extra, Json
from sqlalchemy import Column, Table, delete, func, insert, update
from sqlalchemy.future import select
from sqlalchemy.orm import InstrumentedAttribute, Session
from sqlalchemy.sql import Select
from sqlalchemy.sql.elements import BinaryExpression, Label, UnaryExpression
from sqlmodel import SQLModel
from starlette.requests import Request

from fastapi_amis_admin.utils.functools import cached_property

from .base import BaseCrud
from .parser import (
    SqlField,
    SQLModelField,
    SQLModelFieldParser,
    SQLModelListField,
    get_python_type_parse,
)
from .schema import BaseApiOut, ItemListSchema
from .utils import (
    SqlalchemyDatabase,
    get_engine_db,
    parser_item_id,
    parser_str_set_list,
    schema_create_by_modelfield,
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


class SQLModelSelector:
    model: Type[SQLModel] = None  # SQLModel模型
    fields: List[SQLModelListField] = []  # 需要查询的字段
    list_filter: List[SQLModelListField] = []  # 查询可过滤的字段
    exclude: List[SQLModelField] = []  # 不需要查询的字段
    ordering: List[Union[SQLModelListField, UnaryExpression]] = []  # 默认排序字段
    link_models: Dict[str, Tuple[Type[Table], Column, Column]] = {}  # 关联模型
    pk_name: str = "id"  # 主键名称

    def __init__(self, model: Type[SQLModel] = None, fields: List[SQLModelListField] = None) -> None:
        self.model = model or self.model
        assert self.model, "model is None"
        self.pk_name: str = self.pk_name or self.model.__table__.primary_key.columns.keys()[0]
        self.pk: InstrumentedAttribute = self.model.__dict__[self.pk_name]
        self.parser = SQLModelFieldParser(self.model)
        self.fields = fields or self.fields or [self.model]
        exclude = self.parser.filter_insfield(self.exclude)
        self.fields = [
            sqlfield
            for sqlfield in self.parser.filter_insfield(self.fields + [self.pk], save_class=(Label,))
            if sqlfield not in exclude
        ]
        assert self.fields, "fields is None"
        self.list_filter = self.list_filter or self.fields

    @cached_property
    def _select_entities(self) -> Dict[str, SqlField]:
        return {self.parser.get_alias(insfield): insfield for insfield in self.fields}

    @cached_property
    def _filter_entities(self) -> Dict[str, SqlField]:
        return {
            self.parser.get_alias(sqlfield): sqlfield
            for sqlfield in self.parser.filter_insfield(self.list_filter, save_class=(Label,))
        }

    async def get_select(self, request: Request) -> Select:
        return select(*self._select_entities.values())

    def _calc_ordering(self, orderBy, orderDir):
        sqlfield = self._select_entities.get(orderBy) or self._filter_entities.get(orderBy)
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
                stmt: Select = Depends(self.get_select),
                link_clause=Depends(self.get_link_clause),
            ) -> Select:
                if link_clause is not None:
                    stmt = stmt.where(link_clause)
                return stmt

        else:
            select_maker = self.get_select
        return select_maker

    async def get_link_clause(
        self,
        request: Request,
        link_model: str = None,
        link_item_id: Union[int, str] = Query(
            None,
            title="pk",
            example="1,2,3",
            description="Link Model Primary key or list of primary keys",
        ),
    ) -> Optional[Any]:
        if link_model and link_item_id:
            result = self.link_models.get(link_model)
            if not result:
                return None
            table, pk_col, link_col = result
            if table is not None:
                op = "in_"
                if isinstance(link_item_id, str) and link_item_id.startswith("!"):
                    op = "not_in"
                    link_item_id = link_item_id[1:]
                    if not link_item_id:
                        return None
                link_item_id = list(
                    map(
                        get_python_type_parse(link_col),
                        parser_str_set_list(link_item_id),
                    )
                )
                if op == "in_":
                    return self.pk.in_(select(pk_col).where(link_col.in_(link_item_id)))
                elif op == "not_in":
                    return self.pk.not_in(select(pk_col).where(link_col.in_(link_item_id)))
        return None

    @staticmethod
    def _parser_query_value(
        value: Any, operator: str = "__eq__", python_type_parse: Callable = str
    ) -> Tuple[Optional[str], Union[tuple, None]]:
        if isinstance(value, str):
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


class SQLModelCrud(BaseCrud, SQLModelSelector):
    engine: SqlalchemyDatabase = None
    create_fields: List[SQLModelField] = []  # 新增数据字段
    readonly_fields: List[SQLModelListField] = []  # 只读字段
    update_fields: List[SQLModelListField] = []  # 可编辑字段

    def __init__(
        self,
        model: Type[SQLModel],
        engine: SqlalchemyDatabase,
        fields: List[SQLModelListField] = None,
        router: APIRouter = None,
    ) -> None:
        self.engine = engine or self.engine
        assert self.engine, "engine is None"
        self.db = get_engine_db(self.engine)
        SQLModelSelector.__init__(self, model, fields)
        BaseCrud.__init__(self, self.model, router)

    def _create_schema_list(self):
        if self.schema_list:
            return self.schema_list
        modelfields = list(
            filter(
                None,
                [self.parser.get_modelfield(sqlfield, deepcopy=True) for sqlfield in self._select_entities.values()],
            )
        )
        return schema_create_by_modelfield(
            schema_name=f"{self.schema_name_prefix}List",
            modelfields=modelfields,
            set_none=True,
            extra=Extra.allow,
        )

    def _create_schema_filter(self):
        if self.schema_filter:
            return self.schema_filter
        self.list_filter = self.list_filter or self._select_entities.values()
        modelfields = list(
            filter(
                None,
                [
                    self.parser.get_modelfield(sqlfield, deepcopy=True)
                    for sqlfield in self.parser.filter_insfield(self.list_filter, save_class=(Label,))
                ],
            )
        )
        # todo perfect
        for modelfield in modelfields:
            if not issubclass(modelfield.type_, (Enum, bool)) and issubclass(
                modelfield.type_,
                (int, float, datetime.datetime, datetime.date, datetime.time, Json),
            ):
                modelfield.type_ = str
                modelfield.outer_type_ = str
                modelfield.validators = []
        return schema_create_by_modelfield(
            schema_name=f"{self.schema_name_prefix}Filter",
            modelfields=modelfields,
            set_none=True,
        )

    def _create_schema_update(self):
        if self.schema_update:
            return self.schema_update
        if not self.readonly_fields and not self.update_fields:
            return super(SQLModelCrud, self)._create_schema_update()
        self.update_fields = self.parser.filter_insfield(self.update_fields) or self.schema_model.__fields__.values()
        modelfields = {self.parser.get_modelfield(ins, deepcopy=True) for ins in self.update_fields}
        readonly_fields = {
            self.parser.get_modelfield(ins, deepcopy=True).name for ins in self.parser.filter_insfield(self.readonly_fields)
        } | {self.pk_name}
        modelfields = {field for field in modelfields if field.name not in readonly_fields}
        return schema_create_by_modelfield(f"{self.schema_name_prefix}Update", modelfields, set_none=True)

    def _create_schema_create(self):
        if self.schema_create:
            return self.schema_create
        if not self.create_fields:
            return super(SQLModelCrud, self)._create_schema_create()
        modelfields = list(
            filter(
                None,
                [self.parser.get_modelfield(field, deepcopy=True) for field in self.create_fields],
            )
        )
        return schema_create_by_modelfield(f"{self.schema_name_prefix}Create", modelfields)

    def _read_items(self, session: Session, item_id: List[str]):
        stmt = select(self.model).where(self.pk.in_(list(map(get_python_type_parse(self.pk), item_id))))
        items = session.scalars(stmt).all()
        parse = self.schema_read.from_orm if self.schema_read.Config.orm_mode else self.schema_read.parse_obj
        return [parse(obj) for obj in items]

    @property
    def schema_name_prefix(self):
        if self.__class__ is SQLModelCrud:
            return self.model.__name__
        return super().schema_name_prefix

    async def on_create_pre(self, request: Request, obj: BaseModel, **kwargs) -> Dict[str, Any]:
        data_dict = obj.dict(by_alias=True)  # exclude=set(self.pk)
        if self.pk_name in data_dict and not data_dict.get(self.pk_name):
            del data_dict[self.pk_name]
        return data_dict

    async def on_update_pre(
        self,
        request: Request,
        obj: BaseModel,
        item_id: Union[List[str], List[int]],
        **kwargs,
    ) -> Dict[str, Any]:
        data = obj.dict(exclude_unset=True, by_alias=True)
        data = {key: val for key, val in data.items() if val is not None or self.model.__fields__[key].allow_none}
        return data

    async def on_filter_pre(self, request: Request, obj: BaseModel, **kwargs) -> Dict[str, Any]:
        return obj and {k: v for k, v in obj.dict(exclude_unset=True, by_alias=True).items() if v is not None}

    @property
    def route_list(self) -> Callable:
        async def route(
            request: Request,
            paginator: self.paginator = Depends(),  # type: ignore
            filters: self.schema_filter = Body(None),  # type: ignore
            stmt: Select = Depends(self._select_maker),
        ):
            if not await self.has_list_permission(request, paginator, filters):
                return self.error_no_router_permission(request)
            data = ItemListSchema(items=[])
            page, perPage = paginator.page, paginator.perPage
            filters_data = await self.on_filter_pre(request, filters)
            if filters_data:
                stmt = stmt.filter(*self.calc_filter_clause(filters_data))
            if paginator.show_total:
                data.total = await self.db.async_execute(
                    select(func.count("*")).select_from(stmt.subquery()),
                    on_close_pre=lambda r: r.scalar(),
                )
            orderBy = self._calc_ordering(paginator.orderBy, paginator.orderDir)
            if orderBy:
                stmt = stmt.order_by(*orderBy)
            stmt = stmt.limit(perPage).offset((page - 1) * perPage)
            data.items = await self.db.async_execute(stmt, on_close_pre=lambda r: r.all())
            data.items = self.parser.conv_row_to_dict(data.items)
            data.items = [self.schema_list.parse_obj(item) for item in data.items] if data.items else []
            data.query = request.query_params
            data.filters = filters_data
            return BaseApiOut(data=data)

        return route

    @property
    def route_create(self) -> Callable:
        async def route(
            request: Request,
            data: Union[self.schema_create, List[self.schema_create]] = Body(...),  # type: ignore
        ) -> BaseApiOut[Union[int, self.schema_model]]:  # type: ignore
            if not await self.has_create_permission(request, data):
                return self.error_no_router_permission(request)
            is_bulk = True
            if not isinstance(data, list):
                is_bulk = False
                data = [data]
            values = [await self.on_create_pre(request, value) for value in data]
            if not values:
                return self.error_data_handle(request)
            stmt = insert(self.model).values(values)
            if not is_bulk and self.db.engine.dialect.name == "postgresql":
                stmt = stmt.returning(self.pk)
            try:
                result = await self.db.async_execute(stmt)
            except Exception as error:
                return self.error_execute_sql(request=request, error=error)
            if is_bulk:
                return BaseApiOut(data=getattr(result, "rowcount", None))
            data = values[0]
            if self.db.engine.dialect.name == "postgresql":
                data[self.pk_name] = result.scalar()
            else:
                data[self.pk_name] = getattr(result, "lastrowid", None)
            data = self.schema_model.parse_obj(data)
            return BaseApiOut(data=data)

        return route

    @property
    def route_read(self) -> Callable:
        async def route(
            request: Request,
            item_id: List[str] = Depends(parser_item_id),
        ):
            if not await self.has_read_permission(request, item_id):
                return self.error_no_router_permission(request)
            items = await self.db.async_run_sync(self._read_items, item_id)
            if len(items) == 1:
                items = items[0]
            return BaseApiOut(data=items)

        return route

    @property
    def route_update(self) -> Callable:
        async def route(
            request: Request,
            item_id: List[str] = Depends(parser_item_id),
            data: self.schema_update = Body(...),  # type: ignore
        ):
            if not await self.has_update_permission(request, item_id, data):
                return self.error_no_router_permission(request)
            item_id = list(map(get_python_type_parse(self.pk), item_id))
            stmt = update(self.model).where(self.pk.in_(item_id))
            values = await self.on_update_pre(request, data, item_id=item_id)
            if not values:
                return self.error_data_handle(request)
            stmt = stmt.values(values)
            result = await self.db.async_execute(stmt)
            return BaseApiOut(data=getattr(result, "rowcount", None))

        return route

    @property
    def route_delete(self) -> Callable:
        async def route(
            request: Request,
            item_id: List[str] = Depends(parser_item_id),
        ):
            if not await self.has_delete_permission(request, item_id):
                return self.error_no_router_permission(request)
            stmt = delete(self.model).where(self.pk.in_(list(map(get_python_type_parse(self.pk), item_id))))
            result = await self.db.async_execute(stmt)
            return BaseApiOut(data=getattr(result, "rowcount", None))

        return route
