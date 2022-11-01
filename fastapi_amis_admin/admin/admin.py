import datetime
import re
from functools import lru_cache
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    NewType,
    Optional,
    Type,
    TypeVar,
    Union,
)

from fastapi import Body, Depends, FastAPI, HTTPException, Query, Request
from pydantic import BaseModel
from pydantic.fields import ModelField
from pydantic.utils import deep_update
from sqlalchemy import Column, Table, delete, insert
from sqlalchemy.orm import InstrumentedAttribute, RelationshipProperty
from sqlalchemy.sql.elements import Label
from sqlalchemy.util import md5_hex
from sqlalchemy_database import AsyncDatabase, Database
from sqlmodel import SQLModel
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.templating import Jinja2Templates
from typing_extensions import Literal

import fastapi_amis_admin
from fastapi_amis_admin.admin.handlers import register_exception_handlers
from fastapi_amis_admin.admin.parser import AmisParser
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.amis.components import (
    Action,
    ActionType,
    App,
    ColumnOperation,
    Dialog,
    Form,
    FormItem,
    Iframe,
    InputExcel,
    InputTable,
    Page,
    PageSchema,
    Picker,
    Remark,
    Service,
    TableColumn,
    TableCRUD,
    Tpl,
)
from fastapi_amis_admin.amis.constants import (
    DisplayModeEnum,
    LevelEnum,
    SizeEnum,
    TabsModeEnum,
)
from fastapi_amis_admin.amis.types import (
    AmisAPI,
    BaseAmisApiOut,
    BaseAmisModel,
    SchemaNode,
)
from fastapi_amis_admin.crud import RouterMixin, SQLModelCrud
from fastapi_amis_admin.crud.base import (
    SchemaCreateT,
    SchemaFilterT,
    SchemaModelT,
    SchemaUpdateT,
)
from fastapi_amis_admin.crud.parser import (
    SQLModelFieldParser,
    SQLModelListField,
    get_python_type_parse,
)
from fastapi_amis_admin.crud.schema import BaseApiOut, CrudEnum, Paginator
from fastapi_amis_admin.crud.utils import (
    SqlalchemyDatabase,
    get_engine_db,
    parser_item_id,
    parser_str_set_list,
    schema_create_by_schema,
)
from fastapi_amis_admin.utils.functools import cached_property
from fastapi_amis_admin.utils.translation import i18n as _

_BaseAdminT = TypeVar("_BaseAdminT", bound="BaseAdmin")
_PageSchemaAdminT = TypeVar("_PageSchemaAdminT", bound="PageSchemaAdmin")
_BaseModel = NewType("_BaseModel", BaseModel)


class LinkModelForm:
    link_model: Table

    def __init__(
        self,
        pk_admin: "BaseModelAdmin",
        display_admin: "ModelAdmin",
        link_model: Union[SQLModel, Table],
        link_col: Column,
        item_col: Column,
    ):
        self.link_model = link_model
        self.pk_admin = pk_admin
        self.display_admin = display_admin
        assert self.display_admin, "display_admin is None"
        self.link_col = link_col
        self.item_col = item_col
        assert self.item_col is not None, "item_col is None"
        assert self.link_col is not None, "link_col is None"
        self.path = f"/{self.display_admin.model.__name__}"

    @classmethod
    def bind_model_admin(cls, pk_admin: "BaseModelAdmin", insfield: InstrumentedAttribute) -> Optional["LinkModelForm"]:
        if not isinstance(insfield.prop, RelationshipProperty):
            return None
        table = insfield.prop.secondary
        if table is None:
            return None
        admin = None
        link_key = None
        item_key = None
        for key in table.foreign_keys:
            if key.column.table != pk_admin.model.__table__:  # Get the associated third-party table
                admin = pk_admin.app.site.get_model_admin(key.column.table.name)
                link_key = key
            else:
                item_key = key
        if admin and link_key and item_key:
            admin.link_models[pk_admin.model.__tablename__] = (table, link_key.parent, item_key.parent)
            return LinkModelForm(
                pk_admin=pk_admin,
                display_admin=admin,
                link_model=table,
                link_col=link_key.parent,
                item_col=item_key.parent,
            )
        return None

    @property
    def route_delete(self):
        async def route(
            request: Request,
            item_id: List[str] = Depends(parser_item_id),
            link_id: str = Query(
                ...,
                min_length=1,
                title="link_id",
                example="1,2,3",
                description="link model Primary key or list of link model primary keys",
            ),
        ):
            if not await self.pk_admin.has_update_permission(request, item_id, None):
                return self.pk_admin.error_no_router_permission(request)
            stmt = (
                delete(self.link_model)
                .where(
                    self.link_col.in_(
                        list(
                            map(
                                get_python_type_parse(self.link_col),
                                parser_str_set_list(link_id),
                            )
                        )
                    )
                )
                .where(self.item_col.in_(list(map(get_python_type_parse(self.item_col), item_id))))
            )
            result = await self.pk_admin.db.async_execute(stmt)
            return BaseApiOut(data=result.rowcount)  # type: ignore

        return route

    @property
    def route_create(self):
        async def route(
            request: Request,
            item_id: List[str] = Depends(parser_item_id),
            link_id: str = Query(
                ...,
                min_length=1,
                title="link_id",
                example="1,2,3",
                description="link model Primary key or list of link model primary keys",
            ),
        ):
            if not await self.pk_admin.has_update_permission(request, item_id, None):
                return self.pk_admin.error_no_router_permission(request)
            values = []
            for item in map(get_python_type_parse(self.item_col), item_id):
                values.extend(
                    {self.link_col.key: link, self.item_col.key: item}
                    for link in map(
                        get_python_type_parse(self.link_col),
                        parser_str_set_list(link_id),
                    )
                )
            stmt = insert(self.link_model).values(values)
            try:
                result = await self.pk_admin.db.async_execute(stmt)
            except Exception as error:
                return self.pk_admin.error_execute_sql(request=request, error=error)
            return BaseApiOut(data=result.rowcount)  # type: ignore

        return route

    async def get_form_item(self, request: Request):
        url = self.display_admin.router_path + self.display_admin.page_path
        picker = Picker(
            name=self.display_admin.model.__tablename__,
            label=self.display_admin.page_schema.label,
            labelField="name",
            valueField="id",
            multiple=True,
            required=False,
            modalMode="dialog",
            size="full",
            pickerSchema={"&": "${body}"},
            source={
                "method": "post",
                "data": "${body.api.data}",
                "url": "${body.api.url}&link_model=" + self.pk_admin.model.__tablename__ + "&link_item_id=${api.qsOptions.id}",
            },
        )
        adaptor = None
        if await self.pk_admin.has_update_permission(request, None, None):
            button_create = ActionType.Ajax(
                actionType="ajax",
                label=_("Add Association"),
                level=LevelEnum.danger,
                confirmText=_("Are you sure you want to add the association?"),
                api=f"post:{self.pk_admin.app.router_path}{self.pk_admin.router.prefix}{self.path}"
                + '/${REPLACE(query.link_item_id, "!", "")}?link_id=${IF(ids, ids, id)}',
            )  # query.link_item_id
            adaptor = (
                'if(!payload.hasOwnProperty("_payload")){payload._payload=JSON.stringify(payload);}'
                "payload=JSON.parse(payload._payload);button_create=" + button_create.amis_json() + ";"
                "payload.data.body.bulkActions.push(button_create);"
                "payload.data.body.itemActions.push(button_create);"
                "return payload;".replace("action_id", "create" + self.path.replace("/", "_"))
            )
            button_create_dialog = ActionType.Dialog(
                icon="fa fa-plus pull-left",
                label=_("Add Association"),
                level=LevelEnum.danger,
                dialog=Dialog(
                    title=_("Add Association"),
                    size="full",
                    body=Service(
                        schemaApi=AmisAPI(
                            method="post",
                            url=url,
                            data={},
                            cache=300000,
                            responseData={
                                "&": "${body}",
                                "api.url": "${body.api.url}&link_model="
                                + self.pk_admin.model.__tablename__
                                + "&link_item_id=!${api.qsOptions.id}",
                            },
                            qsOptions={"id": f"${self.pk_admin.pk_name}"},
                            adaptor=adaptor,
                        )
                    ),
                ),
            )

            button_delete = ActionType.Ajax(
                actionType="ajax",
                label=_("Remove Association"),
                level=LevelEnum.danger,
                confirmText=_("Are you sure you want to remove the association?"),
                api=f"delete:{self.pk_admin.app.router_path}{self.pk_admin.router.prefix}{self.path}"
                + "/${query.link_item_id}?link_id=${IF(ids, ids, id)}",
            )
            adaptor = (
                'if(!payload.hasOwnProperty("_payload")){payload._payload=JSON.stringify(payload);}'
                "payload=JSON.parse(payload._payload);button_delete="
                + button_delete.amis_json()
                + ";payload.data.body.headerToolbar.push("
                + button_create_dialog.amis_json()
                + ");payload.data.body.bulkActions.push(button_delete);payload.data.body.itemActions.push(button_delete);"
                "return payload;".replace("action_id", "delete" + self.path.replace("/", "_"))
            )
        return Service(
            schemaApi=AmisAPI(
                method="post",
                url=url,
                data={},
                cache=300000,
                responseData=dict(controls=[picker]),
                qsOptions={"id": f"${self.pk_admin.pk_name}"},
                adaptor=adaptor,
            )
        )

    def register_router(self):
        self.pk_admin.router.add_api_route(
            self.path + "/{item_id}",
            self.route_delete,
            methods=["DELETE"],
            response_model=BaseApiOut[int],
            name=f"{self.link_model.name}_Delete",
        )

        self.pk_admin.router.add_api_route(
            self.path + "/{item_id}",
            self.route_create,
            methods=["POST"],
            response_model=BaseApiOut[int],
            name=f"{self.link_model.name}_Create",
        )

        return self


class BaseModelAdmin(SQLModelCrud):
    list_display: List[Union[SQLModelListField, TableColumn]] = []  # Fields to be displayed
    list_filter: List[Union[SQLModelListField, FormItem]] = []  # Query filterable fields
    list_per_page: int = 10  # Amount of data per page
    link_model_fields: List[InstrumentedAttribute] = []  # inline field
    link_model_forms: List[LinkModelForm] = []
    bulk_update_fields: List[Union[SQLModelListField, FormItem]] = []  # Bulk edit fields
    enable_bulk_create: bool = False  # whether to enable batch creation
    search_fields: List[SQLModelListField] = []  # fuzzy search fields
    page_schema: Union[PageSchema, str] = PageSchema()

    def __init__(self, app: "AdminApp"):
        assert self.model, "model is None"
        assert app, "app is None"
        self.app = app
        self.engine = self.engine or self.app.engine
        self.amis_parser = self.app.site.amis_parser
        self.parser = SQLModelFieldParser(default_model=self.model)
        list_display_insfield = self.parser.filter_insfield(self.list_display, save_class=(Label,))
        self.list_filter = self.list_filter or list_display_insfield or [self.model]
        self.list_filter.extend(self.search_fields)
        super().__init__(self.model, self.engine)
        self.fields.extend(list_display_insfield)

    @cached_property
    def router_path(self) -> str:
        return self.app.router_path + self.router.prefix

    def get_link_model_forms(self) -> List[LinkModelForm]:
        self.link_model_forms = list(
            filter(
                None,
                [LinkModelForm.bind_model_admin(self, insfield) for insfield in self.link_model_fields],
            )
        )
        return self.link_model_forms

    async def get_list_display(self, request: Request) -> List[Union[SQLModelListField, TableColumn]]:
        return self.list_display or list(self.schema_list.__fields__.values())

    async def get_list_filter(self, request: Request) -> List[Union[SQLModelListField, FormItem]]:
        return self.list_filter or list(self.schema_filter.__fields__.values())

    async def get_list_column(self, request: Request, modelfield: ModelField) -> TableColumn:
        column = self.amis_parser.as_table_column(modelfield)
        if await self.has_update_permission(request, None, None) and modelfield.name in self.schema_update.__fields__:
            item = await self.get_form_item(request, modelfield, action=CrudEnum.update)
            if isinstance(item, BaseModel):
                item = item.dict(exclude_none=True, by_alias=True, exclude={"name", "label"})
            if isinstance(item, dict):
                column.quickEdit = item
                column.quickEdit.update({"saveImmediately": True})
                if item.get("type") == "switch":
                    column.quickEdit.update({"mode": "inline"})
        return column

    async def get_list_columns(self, request: Request) -> List[TableColumn]:
        columns = []
        for field in await self.get_list_display(request):
            if isinstance(field, BaseAmisModel):
                columns.append(field)
            elif isinstance(field, type) and issubclass(field, SQLModel):
                ins_list = self.parser.get_sqlmodel_insfield(field)
                modelfields = [self.parser.get_modelfield(ins) for ins in ins_list]
                columns.extend([await self.get_list_column(request, modelfield) for modelfield in modelfields])
            else:
                modelfield = self.parser.get_modelfield(field)
                if modelfield:
                    columns.append(await self.get_list_column(request, modelfield))
        for link_form in self.link_model_forms:
            form = await link_form.get_form_item(request)
            if form:
                columns.append(
                    ColumnOperation(
                        width=160,
                        label=link_form.display_admin.page_schema.label,
                        breakpoint="*",
                        buttons=[form],
                    )
                )
        return columns

    async def get_list_table_api(self, request: Request) -> AmisAPI:
        data = {"&": "$$"}
        for field in self.search_fields:
            alias = self.parser.get_alias(field)
            if alias:
                data[alias] = f"[~]${alias}"
        for field in await self.get_list_filter(request):
            modelfield = self.parser.get_modelfield(field)
            if modelfield and issubclass(modelfield.type_, (datetime.datetime, datetime.date, datetime.time)):
                data[modelfield.alias] = f"[-]${modelfield.alias}"
        return AmisAPI(
            method="POST",
            url=f"{self.router_path}/list?" + "page=${page}&perPage=${perPage}&orderBy=${orderBy}&orderDir=${orderDir}",
            data=data,
        )

    async def get_list_table(self, request: Request) -> TableCRUD:
        headerToolbar = [
            "filter-toggler",
            "reload",
            "bulkActions",
            {"type": "columns-toggler", "align": "right", "draggable": True},
            {"type": "drag-toggler", "align": "right"},
            {"type": "pagination", "align": "right"},
            {
                "type": "tpl",
                "tpl": _("SHOWING ${items|count} OF ${total} RESULT(S)"),
                "className": "v-middle",
                "align": "right",
            },
        ]
        headerToolbar.extend(await self.get_actions_on_header_toolbar(request))
        table = TableCRUD(
            api=await self.get_list_table_api(request),
            autoFillHeight=True,
            headerToolbar=headerToolbar,
            filterTogglable=True,
            filterDefaultVisible=False,
            filter=await self.get_list_filter_form(request),
            syncLocation=False,
            keepItemSelectionOnPageChange=True,
            perPage=self.list_per_page,
            itemActions=await self.get_actions_on_item(request),
            bulkActions=await self.get_actions_on_bulk(request),
            footerToolbar=[
                "statistics",
                "switch-per-page",
                "pagination",
                "load-more",
                "export-csv",
                "export-excel",
            ],
            columns=await self.get_list_columns(request),
            primaryField=self.pk_name,
            quickSaveItemApi=f"put:{self.router_path}/item/" + "${id}",
        )
        if self.link_model_forms:
            table.footable = True
        return table

    async def get_form_item_on_foreign_key(
        self, request: Request, modelfield: ModelField, is_filter: bool = False
    ) -> Union[Service, SchemaNode, None]:
        column = self.parser.get_column(modelfield.alias)
        if column is None:
            return None
        foreign_keys = list(column.foreign_keys) or None
        if foreign_keys is None:
            return None
        admin = self.app.site.get_model_admin(foreign_keys[0].column.table.name)
        if not admin:
            return None
        url = admin.router_path + admin.page_path
        label = modelfield.field_info.title or modelfield.name
        remark = Remark(content=modelfield.field_info.description) if modelfield.field_info.description else None
        picker = Picker(
            name=modelfield.alias,
            label=label,
            labelField="name",
            valueField="id",
            required=(modelfield.required and not is_filter),
            modalMode="dialog",
            inline=is_filter,
            size="full",
            labelRemark=remark,
            pickerSchema="${body}",
            source="${body.api}",
        )
        return Service(
            name=modelfield.alias,
            schemaApi=AmisAPI(
                method="post",
                url=url,
                data={},
                cache=300000,
                responseData=dict(controls=[picker]),
            ),
        )

    async def get_form_item(
        self, request: Request, modelfield: ModelField, action: CrudEnum
    ) -> Union[FormItem, SchemaNode, None]:
        is_filter = action == CrudEnum.list
        set_default = action == CrudEnum.create
        return await self.get_form_item_on_foreign_key(request, modelfield, is_filter=is_filter) or self.amis_parser.as_form_item(
            modelfield, is_filter=is_filter, set_default=set_default
        )

    async def get_list_filter_form(self, request: Request) -> Form:
        body = await self._conv_modelfields_to_formitems(request, await self.get_list_filter(request), CrudEnum.list)
        return Form(
            type="",
            title=_("Filter"),
            name=CrudEnum.list,
            body=body,
            mode=DisplayModeEnum.inline,
            actions=[
                Action(
                    actionType="clear-and-submit",
                    label=_("Clear"),
                    level=LevelEnum.default,
                ),
                Action(
                    actionType="reset-and-submit",
                    label=_("Reset"),
                    level=LevelEnum.default,
                ),
                Action(actionType="submit", label=_("Search"), level=LevelEnum.primary),
            ],
            trimValues=True,
        )

    async def get_create_form(self, request: Request, bulk: bool = False) -> Form:
        fields = [field for field in self.schema_create.__fields__.values() if field.name != self.pk_name]
        if not bulk:
            return Form(
                api=f"post:{self.router_path}/item",
                name=CrudEnum.create,
                body=await self._conv_modelfields_to_formitems(request, fields, CrudEnum.create),
            )
        columns, keys = [], {}
        for field in fields:
            column = await self.get_list_column(request, self.parser.get_modelfield(field))
            keys[column.name] = "${" + column.label + "}"
            column.name = column.label
            columns.append(column)
        return Form(
            api=AmisAPI(
                method="post",
                url=f"{self.router_path}/item",
                data={"&": {"$excel": keys}},
            ),
            mode=DisplayModeEnum.normal,
            body=[
                InputExcel(name="excel"),
                InputTable(
                    name="excel",
                    showIndex=True,
                    columns=columns,
                    addable=True,
                    copyable=True,
                    editable=True,
                    removable=True,
                ),
            ],
        )

    async def get_update_form(self, request: Request, bulk: bool = False) -> Form:
        extra = {}
        if not bulk:
            api = f"put:{self.router_path}/item/${self.pk_name}"
            fields = self.schema_update.__fields__.values()
            if self.schema_read:
                extra["initApi"] = f"get:{self.router_path}/item/${self.pk_name}"
        else:
            api = f"put:{self.router_path}/item/" + "${ids|raw}"
            fields = self.bulk_update_fields
        return Form(
            api=api,
            name=CrudEnum.update,
            body=await self._conv_modelfields_to_formitems(request, fields, CrudEnum.update),
            submitText=None,
            trimValues=True,
            **extra,
        )

    async def get_read_form(self, request: Request) -> Form:
        return Form(
            initApi=f"get:{self.router_path}/item/${self.pk_name}",
            name=CrudEnum.read,
            body=await self._conv_modelfields_to_formitems(request, self.schema_read.__fields__.values(), CrudEnum.read),
            submitText=None,
        )

    async def get_read_action(self, request: Request) -> Optional[Action]:
        if not self.schema_read:
            return None
        return ActionType.Dialog(
            icon="fa fa-eye",
            tooltip=_("View"),
            level=LevelEnum.primary,
            dialog=Dialog(
                title=_("View") + " - " + _(self.page_schema.label),
                size=SizeEnum.lg,
                body=await self.get_read_form(request),
            ),
        )

    async def get_create_action(self, request: Request, bulk: bool = False) -> Optional[Action]:
        if not await self.has_create_permission(request, None):
            return None
        if not bulk:
            return ActionType.Dialog(
                icon="fa fa-plus pull-left",
                label=_("Create"),
                level=LevelEnum.primary,
                dialog=Dialog(
                    title=_("Create") + " - " + _(self.page_schema.label),
                    size=SizeEnum.lg,
                    body=await self.get_create_form(request, bulk=bulk),
                ),
            )
        return ActionType.Dialog(
            icon="fa fa-plus pull-left",
            label=_("Bulk Create"),
            level=LevelEnum.primary,
            dialog=Dialog(
                title=_("Bulk Create") + " - " + _(self.page_schema.label),
                size=SizeEnum.full,
                body=await self.get_create_form(request, bulk=bulk),
            ),
        )

    async def get_update_action(self, request: Request, bulk: bool = False) -> Optional[Action]:
        if not await self.has_update_permission(request, None, None):
            return None
        # Turn on batch editing
        if not bulk:
            return ActionType.Dialog(
                icon="fa fa-pencil",
                tooltip=_("Update"),
                dialog=Dialog(
                    title=_("Update") + " - " + _(self.page_schema.label),
                    size=SizeEnum.lg,
                    body=await self.get_update_form(request, bulk=bulk),
                ),
            )

        elif self.bulk_update_fields:
            return ActionType.Dialog(
                label=_("Bulk Update"),
                dialog=Dialog(
                    title=_("Bulk Update") + " - " + _(self.page_schema.label),
                    size=SizeEnum.lg,
                    body=await self.get_update_form(request, bulk=True),
                ),
            )

        else:
            return None

    async def get_delete_action(self, request: Request, bulk: bool = False) -> Optional[Action]:
        if not await self.has_delete_permission(request, None):
            return None
        return (
            ActionType.Ajax(
                label=_("Bulk Delete"),
                confirmText=_("Are you sure you want to delete the selected rows?"),
                api=f"delete:{self.router_path}/item/" + "${ids|raw}",
            )
            if bulk
            else ActionType.Ajax(
                icon="fa fa-times text-danger",
                tooltip=_("Delete"),
                confirmText=_("Are you sure you want to delete row ${%s}?") % self.pk_name,
                api=f"delete:{self.router_path}/item/${self.pk_name}",
            )
        )

    async def get_actions_on_header_toolbar(self, request: Request) -> List[Action]:
        actions = [
            await self.get_create_action(request, bulk=False),
        ]
        if self.enable_bulk_create:
            actions.append(await self.get_create_action(request, bulk=True))
        return list(filter(None, actions))

    async def get_actions_on_item(self, request: Request) -> List[Action]:
        actions = [
            await self.get_read_action(request),
            await self.get_update_action(request, bulk=False),
            await self.get_delete_action(request, bulk=False),
        ]
        return list(filter(None, actions))

    async def get_actions_on_bulk(self, request: Request) -> List[Action]:
        bulkActions = [
            await self.get_update_action(request, bulk=True),
            await self.get_delete_action(request, bulk=True),
        ]
        return list(filter(None, bulkActions))

    async def _conv_modelfields_to_formitems(
        self,
        request: Request,
        fields: Iterable[Union[SQLModelListField, ModelField, FormItem]],
        action: CrudEnum = None,
    ) -> List[FormItem]:
        items = []
        for field in fields:
            if isinstance(field, FormItem):
                items.append(field)
            else:
                field = self.parser.get_modelfield(field)
                if field:
                    item = await self.get_form_item(request, field, action)
                    if item:
                        items.append(item)
        items.sort(key=lambda i: isinstance(i, Service))
        return items


class BaseAdmin:
    def __init__(self, app: "AdminApp"):
        self.app = app
        assert self.app, "app is None"

    @cached_property
    def site(self) -> "BaseAdminSite":
        return self if self.app is self else self.app.site

    @cached_property
    def unique_id(self) -> str:
        unique_str = f"{self.__class__.__module__}:{self.__class__.__qualname__}"
        if self.app is not self:
            unique_str += f"{self.app.unique_id}"
        return md5_hex(unique_str)[:16]


class PageSchemaAdmin(BaseAdmin):
    group_schema: Union[PageSchema, str] = None
    page_schema: Union[PageSchema, str] = PageSchema()

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.page_schema = self.get_page_schema()
        if self.page_schema and self.page_schema.url:
            self.page_schema.url = self.page_schema.url.replace(self.site.settings.site_url, "")
        self.group_schema = self.get_group_schema()

    async def has_page_permission(self, request: Request) -> bool:
        return self.app is self or await self.app.has_page_permission(request)

    def get_page_schema(self) -> Optional[PageSchema]:
        if self.page_schema:
            if isinstance(self.page_schema, str):
                self.page_schema = PageSchema(label=self.page_schema)
            elif isinstance(self.page_schema, PageSchema):
                self.page_schema = self.page_schema.copy(deep=True)
                self.page_schema.label = self.page_schema.label or self.__class__.__name__
            else:
                raise TypeError()
        return self.page_schema

    def get_group_schema(self) -> Optional[PageSchema]:
        if self.group_schema:
            if isinstance(self.group_schema, str):
                self.group_schema = PageSchema(label=self.group_schema)
            elif isinstance(self.group_schema, PageSchema):
                self.group_schema = self.group_schema.copy(deep=True)
                self.group_schema.label = self.group_schema.label or "default"
            else:
                raise TypeError()
        return self.group_schema


class LinkAdmin(PageSchemaAdmin):
    link: str = ""

    def get_page_schema(self) -> Optional[PageSchema]:
        if super().get_page_schema():
            assert self.link, "link is None"
            self.page_schema.link = self.page_schema.link or self.link
        return self.page_schema


class IframeAdmin(PageSchemaAdmin):
    iframe: Iframe = None
    src: str = ""

    def get_page_schema(self) -> Optional[PageSchema]:
        if super().get_page_schema():
            assert self.src, "src is None"
            iframe = self.iframe or Iframe(src=self.src)
            if self.site.settings.site_url and iframe.src.startswith(self.site.settings.site_url):
                self.page_schema.url = iframe.src
            else:
                self.page_schema.url = re.sub(r"^https?:", "", iframe.src)
            self.page_schema.schema_ = iframe
        return self.page_schema


class RouterAdmin(BaseAdmin, RouterMixin):
    def __init__(self, app: "AdminApp"):
        BaseAdmin.__init__(self, app)
        RouterMixin.__init__(self)

    def register_router(self):
        raise NotImplementedError()

    @cached_property
    def router_path(self) -> str:
        if self.router is self.app.router:
            return self.app.router_path
        return self.app.router_path + self.router.prefix


class PageAdmin(PageSchemaAdmin, RouterAdmin):
    """Amis page management"""

    page: Page = None
    page_path: Optional[str] = None
    page_parser_mode: Literal["json", "html"] = "json"
    page_route_kwargs: Dict[str, Any] = {}
    template_name: str = ""
    router_prefix = "/page"

    def __init__(self, app: "AdminApp"):
        RouterAdmin.__init__(self, app)
        if self.page_path is None:
            self.page_path = f"/{self.__class__.__module__}/{self.__class__.__name__}"
        PageSchemaAdmin.__init__(self, app)

    async def page_permission_depend(self, request: Request) -> bool:
        return await self.has_page_permission(request) or self.error_no_page_permission(request)

    def error_no_page_permission(self, request: Request):
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            detail="No page permissions",
            headers={
                "location": f"{self.app.site.router_path}/auth/form/login?redirect={request.url}",
            },
        )

    async def get_page(self, request: Request) -> Page:
        return self.page or Page()

    def get_page_schema(self) -> Optional[PageSchema]:
        if super().get_page_schema():
            self.page_schema.url = f"{self.router_path}{self.page_path}"
            self.page_schema.schemaApi = AmisAPI(
                method="post",
                url=f"{self.router_path}{self.page_path}",
                data={},
                cache=300000,
            )
            if self.page_parser_mode == "html":
                self.page_schema.schema_ = Iframe(src=self.page_schema.url)
        return self.page_schema

    async def page_parser(self, request: Request, page: Page) -> Response:
        if request.method == "GET":
            result = page.amis_html(
                template_path=self.template_name,
                locale=_.get_language(),
                cdn=self.site.settings.amis_cdn,
                pkg=self.site.settings.amis_pkg,
                theme=self.site.settings.amis_theme,
                site_title=self.site.settings.site_title,
                site_icon=self.site.settings.site_icon,
            )
            result = HTMLResponse(result)
        else:
            data = page.amis_dict()
            if await request.body():
                data = deep_update(data, (await request.json()).get("_update", {}))
            result = BaseAmisApiOut(data=data)
            result = JSONResponse(result.dict())
        return result

    def register_router(self):
        self.router.add_api_route(
            self.page_path,
            self.route_page,
            methods=["GET"],
            dependencies=[Depends(self.page_permission_depend)],
            include_in_schema=False,
            response_class=HTMLResponse,
            **self.page_route_kwargs,
        )
        self.router.add_api_route(
            self.page_path,
            self.route_page,
            methods=["POST"],
            dependencies=[Depends(self.page_permission_depend)],
            response_model=BaseAmisApiOut,
            include_in_schema=(self.page_parser_mode == "json"),
            **self.page_route_kwargs,
        )
        return self

    @property
    def route_page(self) -> Callable:
        async def route(request: Request, page: Page = Depends(self.get_page)):
            return await self.page_parser(request, page)

        return route


class TemplateAdmin(PageAdmin):
    """Jinja2 render template management"""

    page: Dict[str, Any] = {}
    page_parser_mode = "html"
    templates: Jinja2Templates = None

    def __init__(self, app: "AdminApp"):
        assert self.templates, "templates:Jinja2Templates is None"
        assert self.template_name, "template_name is None"
        self.page_path = self.page_path or f"/{self.template_name}"
        super().__init__(app)

    async def page_parser(self, request: Request, page: Dict[str, Any]) -> Response:
        page["request"] = request
        return self.templates.TemplateResponse(self.template_name, page)

    async def get_page(self, request: Request) -> Dict[str, Any]:
        return {}


class BaseFormAdmin(PageAdmin, Generic[SchemaUpdateT]):
    schema: Type[SchemaUpdateT] = None
    schema_init_out: Type[Any] = Any
    schema_submit_out: Type[Any] = Any
    form: Form = None
    form_init: bool = None
    form_path: str = ""
    route_init: Callable = None
    route_submit: Callable = None
    router_prefix: str = "/form"

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        assert self.route_submit, "route_submit is None"
        self.form_path = self.form_path or f"{self.page_path}/api"

    async def get_page(self, request: Request) -> Page:
        page = await super(BaseFormAdmin, self).get_page(request)
        page.body = await self.get_form(request)
        return page

    async def get_form_item(self, request: Request, modelfield: ModelField) -> Union[FormItem, SchemaNode]:
        return self.site.amis_parser.as_form_item(modelfield, set_default=True)

    async def get_form(self, request: Request) -> Form:
        form = self.form or Form()
        form.api = AmisAPI(method="POST", url=f"{self.router_path}{self.form_path}")
        form.initApi = AmisAPI(method="GET", url=f"{self.router_path}{self.form_path}") if self.form_init else None
        form.title = ""
        form.body = []
        if self.schema:
            for modelfield in self.schema.__fields__.values():
                formitem = await self.get_form_item(request, modelfield)
                if formitem:
                    form.body.append(formitem)
        return form

    def register_router(self):
        super().register_router()
        self.router.add_api_route(
            self.form_path,
            self.route_submit,
            methods=["POST"],
            response_model=BaseApiOut[self.schema_submit_out],
            dependencies=[Depends(self.page_permission_depend)],
        )
        if self.form_init:
            self.schema_init_out = self.schema_init_out or schema_create_by_schema(
                self.schema, f"{self.__class__.__name__}InitOut", set_none=True
            )
            self.router.add_api_route(
                self.form_path,
                self.route_init,
                methods=["GET"],
                response_model=BaseApiOut[self.schema_init_out],
                dependencies=[Depends(self.page_permission_depend)],
            )
        return self


class FormAdmin(BaseFormAdmin):
    """Form management"""

    @property
    def route_submit(self):
        assert self.schema, "schema is None"

        async def route(request: Request, data: self.schema):  # type:ignore
            return await self.handle(request, data)  # type:ignore

        return route

    async def handle(self, request: Request, data: SchemaUpdateT, **kwargs) -> BaseApiOut[Any]:
        raise NotImplementedError

    async def get_init_data(self, request: Request, **kwargs) -> BaseApiOut[Any]:
        raise NotImplementedError

    @property
    def route_init(self):
        async def route(request: Request):
            return await self.get_init_data(request)

        return route


class ModelAdmin(BaseModelAdmin, PageAdmin):
    """Model management"""

    page_path: str = ""
    bind_model: bool = True

    def __init__(self, app: "AdminApp"):
        BaseModelAdmin.__init__(self, app)
        PageAdmin.__init__(self, app)

    @property
    def router_prefix(self):
        if issubclass(self.__class__.__base__, ModelAdmin):
            return f"/{self.__class__.__name__}"
        return f"/{self.model.__name__}"

    def register_router(self):
        for form in self.link_model_forms:
            form.register_router()
        self.register_crud()
        super(ModelAdmin, self).register_router()
        return self

    async def get_page(self, request: Request) -> Page:
        page = await super(ModelAdmin, self).get_page(request)
        page.body = await self.get_list_table(request)
        return page

    async def has_list_permission(
        self,
        request: Request,
        paginator: Paginator,
        filters: SchemaFilterT = None,
        **kwargs,
    ) -> bool:
        return await self.has_page_permission(request)

    async def has_create_permission(self, request: Request, data: SchemaCreateT, **kwargs) -> bool:  # type self.schema_create
        return await self.has_page_permission(request)

    async def has_read_permission(self, request: Request, item_id: List[str], **kwargs) -> bool:
        return await self.has_page_permission(request)

    async def has_update_permission(
        self,
        request: Request,
        item_id: List[str],
        data: SchemaUpdateT,
        **kwargs,
    ) -> bool:
        return await self.has_page_permission(request)

    async def has_delete_permission(self, request: Request, item_id: List[str], **kwargs) -> bool:
        return await self.has_page_permission(request)


class BaseFormAction:
    admin: "FormAdmin" = None
    action: Action = None

    def __init__(self, admin: "FormAdmin"):
        self.admin = admin
        assert self.admin, "admin is None"

    def register_router(self):
        raise NotImplementedError


class BaseModelAction:
    admin: "ModelAdmin" = None
    action: Action = None

    def __init__(self, admin: "ModelAdmin"):
        self.admin = admin
        assert self.admin, "admin is None"

    async def fetch_item_scalars(self, item_id: List[str]) -> List[SchemaModelT]:
        # noinspection PyProtectedMember
        return await self.admin.db.async_run_sync(self.admin._fetch_item_scalars, item_id)

    def register_router(self):
        raise NotImplementedError


class FormAction(FormAdmin, BaseFormAction):
    schema: Type[BaseModel] = None
    action: ActionType.Dialog = None

    def __init__(self, admin: "FormAdmin"):
        BaseFormAction.__init__(self, admin)
        self.router = self.admin.router
        FormAdmin.__init__(self, self.admin.app)

    async def get_action(self, request: Request, **kwargs) -> Action:
        action = self.action or ActionType.Dialog(label=_("Custom form actions"), dialog=Dialog())
        action.dialog.title = action.dialog.title or action.label  # only override if not set
        action.dialog.size = action.dialog.size or SizeEnum.xl
        action.dialog.body = action.dialog.body or ""  # keep it empty for non model related custom form
        return action

    async def handle(self, request: Request, data: BaseModel, **kwargs) -> BaseApiOut[Any]:
        return BaseApiOut(data=data)


class ModelAction(BaseFormAdmin, BaseModelAction):
    action: ActionType.Dialog = None

    def __init__(self, admin: "ModelAdmin"):
        BaseModelAction.__init__(self, admin)
        self.router = self.admin.router
        BaseFormAdmin.__init__(self, self.admin.app)

    async def get_action(self, request: Request, **kwargs) -> Action:
        action = self.action or ActionType.Dialog(label=_("Custom form actions"), dialog=Dialog())
        action.dialog.title = action.dialog.title or action.label  # only override if not set
        action.dialog.body = Service(
            schemaApi=AmisAPI(
                method="post",
                url=self.router_path + self.page_path + "?item_id=${IF(ids, ids, id)}",
                responseData={
                    "&": "${body}",
                    "api.url": "${body.api.url}?item_id=${api.query.item_id}",
                    "submitText": "",
                },
            )
        )
        return action

    async def handle(self, request: Request, item_id: List[str], data: Optional[SchemaUpdateT], **kwargs) -> BaseApiOut[Any]:
        return BaseApiOut(data=data)

    @property
    def route_submit(self):
        default = ... if self.schema else None

        async def route(
            request: Request,
            data: self.schema = Body(default=default),  # type:ignore
            item_id: str = Query(
                None,
                title="item_id",
                example="1,2,3",
                description="Primary key or list of primary keys",
            ),
        ):
            return await self.handle(request, parser_str_set_list(set_str=item_id), data)

        return route


class AdminGroup(PageSchemaAdmin):
    def __init__(self, app: "AdminApp") -> None:
        super().__init__(app)
        self._children: List[_PageSchemaAdminT] = []

    @cached_property
    def unique_id(self) -> str:
        unique_str = super().unique_id
        if self._children:
            unique_str += self._children[0].unique_id
        return md5_hex(unique_str)[:16]

    def append_child(self, child: _PageSchemaAdminT, group_schema: PageSchema = None) -> None:
        if not child.page_schema:
            return
        group_label = group_schema and group_schema.label
        if not group_label:
            self._children.append(child)
        else:
            for item in self._children:
                if isinstance(item, AdminGroup) and item.page_schema and item.page_schema.label == group_label:
                    item.append_child(child, group_schema=None)
                    return
            group = AdminGroup(self.app)
            group.page_schema = group_schema.copy()
            group.append_child(child, group_schema=None)
            self._children.append(group)

    async def get_page_schema_children(self, request: Request) -> List[PageSchema]:
        page_schema_list = []
        for child in self._children:
            if not child.page_schema or not await child.has_page_permission(request):
                continue
            if (isinstance(child, AdminGroup) and not isinstance(child, AdminApp)) or (
                isinstance(child, AdminApp) and child.tabs_mode is None
            ):
                sub_children = await child.get_page_schema_children(request)
                if sub_children:
                    page_schema = child.page_schema.copy(deep=True)
                    page_schema.children = sub_children
                    page_schema_list.append(page_schema)
            else:
                page_schema_list.append(child.page_schema)
        if page_schema_list:
            page_schema_list.sort(key=lambda p: p.sort or 0, reverse=True)
        return page_schema_list

    def get_page_schema_child(self, unique_id: str) -> Optional[_PageSchemaAdminT]:
        for child in self._children:
            if child.unique_id == unique_id:
                return child
            if isinstance(child, AdminGroup):
                child = child.get_page_schema_child(unique_id)
                if child:
                    return child
        return None

    def __iter__(self) -> Iterator[_PageSchemaAdminT]:
        return self._children.__iter__()


class AdminApp(PageAdmin, AdminGroup):
    """Manage applications"""

    engine: SqlalchemyDatabase = None
    page_path = "/"
    tabs_mode: TabsModeEnum = None

    def __init__(self, app: "AdminApp"):
        PageAdmin.__init__(self, app)
        AdminGroup.__init__(self, app)
        self.engine = self.engine or self.app.engine
        self.db = get_engine_db(self.engine)
        self._registered: Dict[Type[_BaseAdminT], Optional[_BaseAdminT]] = {}
        self.__register_lock = False

    @property
    def router_prefix(self):
        return f"/{self.__class__.__name__}"

    def get_admin_or_create(self, admin_cls: Type[_BaseAdminT], register: bool = True) -> Optional[_BaseAdminT]:
        if admin_cls not in self._registered and (not register or self.__register_lock):
            return None
        admin = self._registered.get(admin_cls)
        if admin:
            return admin
        admin = admin_cls(self)
        self._registered[admin_cls] = admin
        if isinstance(admin, PageSchemaAdmin):
            self.append_child(admin, group_schema=admin.group_schema)
        return admin

    def _create_admin_instance_all(self) -> None:
        [self.get_admin_or_create(admin_cls) for admin_cls in self._registered.keys()]

    def _register_admin_router_all_pre(self):
        [admin.get_link_model_forms() for admin in self._registered.values() if isinstance(admin, ModelAdmin)]

    def _register_admin_router_all(self):
        for admin in self._registered.values():
            if isinstance(admin, RouterAdmin):  # register route
                admin.register_router()
                self.router.include_router(admin.router)

    def register_router(self):
        if not self.__register_lock:
            super(AdminApp, self).register_router()
            self._create_admin_instance_all()
            self._register_admin_router_all_pre()
            self._register_admin_router_all()
            self.__register_lock = True
        return self

    @lru_cache()  # noqa: B019
    def get_model_admin(self, table_name: str) -> Optional[ModelAdmin]:
        for admin_cls, admin in self._registered.items():
            admin = admin or self.get_admin_or_create(admin_cls)
            if issubclass(admin_cls, ModelAdmin) and admin.bind_model and admin.model.__tablename__ == table_name:
                return admin
            elif isinstance(admin, AdminApp) and self.engine is admin.engine:
                admin = admin.get_model_admin(table_name)
                if admin:
                    return admin
        return None

    def register_admin(self, *admin_cls: Type[_BaseAdminT]) -> Type[_BaseAdminT]:
        [self._registered.update({cls: None}) for cls in admin_cls if cls]
        return admin_cls[0]

    def unregister_admin(self, *admin_cls: Type[BaseAdmin]):
        [self._registered.pop(cls) for cls in admin_cls if cls]

    def get_page_schema(self) -> Optional[PageSchema]:
        if super().get_page_schema() and self.tabs_mode is None:
            self.page_schema.schemaApi = None
        return self.page_schema

    async def get_page(self, request: Request) -> Union[Page, App]:
        if self.tabs_mode is None:
            return await self._get_page_as_app(request)
        return await self._get_page_as_tabs(request)

    async def _get_page_as_app(self, request: Request) -> App:
        app = App()
        app.brandName = self.site.settings.site_title
        app.logo = self.site.settings.site_icon
        app.header = Tpl(
            className="w-full",
            tpl='<div class="flex justify-between"><div></div>'
            f'<div><a href="{fastapi_amis_admin.__url__}" target="_blank" '
            'title="Copyright"><i class="fa fa-github fa-2x"></i></a></div></div>',
        )
        app.footer = (
            '<div class="p-2 text-center bg-light">Copyright © 2021 - 2022  '
            f'<a href="{fastapi_amis_admin.__url__}" target="_blank" '
            'class="link-secondary">fastapi-amis-admin</a>. All rights reserved. '
            f'<a target="_blank" href="{fastapi_amis_admin.__url__}" '
            f'class="link-secondary" rel="noopener">v{fastapi_amis_admin.__version__}</a></div> '
        )
        # app.asideBefore = '<div class="p-2 text-center">菜单前面区域</div>'
        # app.asideAfter = f'<div class="p-2 text-center">' \
        #                  f'<a href="{fastapi_amis_admin.__url__}"  target="_blank">fastapi-amis-admin</a></div>'
        children = await self.get_page_schema_children(request)
        app.pages = [{"children": children}] if children else []
        return app

    async def _get_page_as_tabs(self, request: Request) -> Page:
        page = await super(AdminApp, self).get_page(request)
        children = await self.get_page_schema_children(request)
        page.body = PageSchema(children=children).as_tabs_item(tabs_extra=dict(tabsMode=self.tabs_mode, mountOnEnter=True)).tab
        return page


class BaseAdminSite(AdminApp):
    def __init__(
        self,
        settings: Settings,
        fastapi: FastAPI = None,
        engine: SqlalchemyDatabase = None,
    ):
        try:
            from fastapi_user_auth.auth import Auth

            self.auth: Auth = None  # type: ignore
        except ImportError:
            pass
        self.settings = settings
        self.amis_parser = AmisParser(
            image_receiver=self.settings.amis_image_receiver,
            file_receiver=self.settings.amis_file_receiver,
        )
        self.fastapi = fastapi or FastAPI(debug=settings.debug, reload=settings.debug)
        register_exception_handlers(self.fastapi, self.settings.logger)
        self.router = self.fastapi.router
        if engine:
            self.engine = engine
        elif settings.database_url_async:
            self.engine = AsyncDatabase.create(settings.database_url_async, echo=settings.debug)
        elif settings.database_url:
            self.engine = Database.create(settings.database_url, echo=settings.debug)
        super().__init__(self)

    @cached_property
    def router_path(self) -> str:
        return self.settings.site_url + self.settings.root_path + self.router.prefix

    def mount_app(self, fastapi: FastAPI, name: str = "admin") -> None:
        """mount app to fastapi, the path is: site.settings.root_path.
        once mount, the site will create all registered admin instance and register router.
        """
        self.register_router()
        fastapi.mount(self.settings.root_path, self.fastapi, name=name)
        fastapi.add_middleware(BaseHTTPMiddleware, dispatch=self.db.asgi_dispatch)
        """Add SQLAlchemy Session middleware to the main application, and the session object will be bound to each request.
        Note:
        1. The session will be automatically closed when the request ends, so you don't need to close it manually.
        2. In the sub-application, you can also use this middleware, but you need to pay attention that the session object
        in the sub-application will be closed in the main application.
        3. If the sub-application needs to use its own session object, you need to add this middleware to the sub-application.
        4. Middleware or routes after this middleware can get the session object through `db.session`.
        """
