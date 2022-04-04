import datetime
import re
from functools import lru_cache
from typing import Type, Callable, Generator, Any, List, Union, Dict, Iterable, Optional, Tuple, TypeVar, NewType
from fastapi import Request, Depends, FastAPI, Query, HTTPException, Body
from pydantic import BaseModel
from pydantic.fields import ModelField
from sqlalchemy import delete, Column, Table, insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import InstrumentedAttribute, RelationshipProperty
from sqlmodel import SQLModel, select
from sqlmodel.engine.result import ScalarResult
from sqlmodel.main import SQLModelMetaclass
from starlette import status
from starlette.responses import HTMLResponse, JSONResponse, Response, RedirectResponse
from starlette.templating import Jinja2Templates
import fastapi_amis_admin
from fastapi_amis_admin.amis.components import Page, TableCRUD, Action, ActionType, Dialog, Form, FormItem, Picker, \
    Remark, Service, Iframe, PageSchema, TableColumn, ColumnOperation, App, Tpl
from fastapi_amis_admin.amis.constants import LevelEnum, DisplayModeEnum, SizeEnum
from fastapi_amis_admin.amis.types import BaseAmisApiOut, BaseAmisModel, AmisAPI, SchemaNode
from fastapi_amis_admin.amis_admin.parser import AmisParser
from fastapi_amis_admin.crud.base import RouterMixin
from fastapi_amis_admin.crud._sqlmodel import SQLModelCrud, SQLModelSelector
from fastapi_amis_admin.crud.parser import SQLModelFieldParser, SQLModelField, SQLModelListField
from fastapi_amis_admin.crud.schema import CrudEnum, BaseApiOut, Paginator
from fastapi_amis_admin.crud.utils import parser_item_id, schema_create_by_schema, parser_str_set_list
from fastapi_amis_admin.utils.db import SqlalchemyAsyncClient
from fastapi_amis_admin.amis_admin.settings import Settings
from fastapi_amis_admin.utils.functools import cached_property

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

_BaseAdminT = TypeVar('_BaseAdminT', bound="BaseAdmin")
_BaseModel = NewType('_BaseModel', BaseModel)


class LinkModelForm:
    link_model: Table
    display_admin_cls: Type["ModelAdmin"]
    session_factory: Callable[..., Generator[AsyncSession, Any, None]] = None

    def __init__(self,
                 pk_admin: "BaseModelAdmin",
                 display_admin_cls: Type["ModelAdmin"],
                 link_model: Union[SQLModel, Table],
                 link_col: Column,
                 item_col: Column,
                 session_factory: Callable[..., Generator[AsyncSession, Any, None]] = None):
        self.link_model = link_model
        self.pk_admin = pk_admin
        self.display_admin_cls = display_admin_cls or self.display_admin_cls
        assert self.display_admin_cls in self.pk_admin.app._admins_dict, f'{self.display_admin_cls} display_admin_cls is not register'
        self.display_admin: ModelAdmin = self.pk_admin.app.create_admin_instance(self.display_admin_cls)
        assert isinstance(self.display_admin, ModelAdmin)
        self.session_factory = session_factory or self.pk_admin.session_factory
        self.link_col = link_col
        self.item_col = item_col
        assert self.item_col is not None, 'item_col is None'
        assert self.link_col is not None, 'link_col is None'
        self.path = f'/{self.display_admin_cls.model.__name__.lower()}'

    @classmethod
    def bind_model_admin(cls,
                         pk_admin: "BaseModelAdmin",
                         insfield: InstrumentedAttribute
                         ) -> Optional["LinkModelForm"]:
        if not isinstance(insfield.prop, RelationshipProperty):
            return None
        table = insfield.prop.secondary
        if table is None:
            return None
        admin = None
        link_key = None
        item_key = None
        for key in table.foreign_keys:
            if key.column.table != pk_admin.model.__table__:  # 获取关联第三方表
                admin = pk_admin.app.get_model_admin(key.column.table.name)
                link_key = key  # auth_group.id
            else:
                item_key = key  # auth_user.id
        if admin and link_key and item_key:
            if not admin.link_models:
                admin.link_models = {pk_admin.model.__tablename__: (table, link_key.parent, item_key.parent)}
            else:
                admin.link_models.update(
                    {pk_admin.model.__tablename__: (table, link_key.parent, item_key.parent)})
            return LinkModelForm(
                pk_admin=pk_admin,
                display_admin_cls=admin.__class__,
                link_model=table,
                link_col=link_key.parent,
                item_col=item_key.parent
            )
        return None

    @property
    def route_delete(self):
        async def route(
                request: Request,
                item_id: List[str] = Depends(parser_item_id),
                link_id: str = Query(..., min_length=1, title='link_id', example='1,2,3',
                                     description='link model Primary key or list of link model primary keys'),
                db: AsyncSession = Depends(self.session_factory)
        ):
            if not await self.pk_admin.has_update_permission(request, item_id, None):
                return self.pk_admin.error_no_router_permission(request)
            stmt = delete(self.link_model).where(
                self.link_col.in_(list(map(self.pk_admin.parser.get_python_type_parse(self.link_col), parser_str_set_list(link_id))))
            ).where(
                self.item_col.in_(list(map(self.pk_admin.parser.get_python_type_parse(self.item_col), item_id)))
            )
            result = await db.execute(stmt)
            if result.rowcount:  # type: ignore
                await db.commit()
            return BaseApiOut(data=result.rowcount)  # type: ignore

        return route

    @property
    def route_create(self):
        async def route(
                request: Request,
                item_id: List[str] = Depends(parser_item_id),
                link_id: str = Query(..., min_length=1, title='link_id', example='1,2,3',
                                     description='link model Primary key or list of link model primary keys'),
                db: AsyncSession = Depends(self.session_factory)
        ):
            if not await self.pk_admin.has_update_permission(request, item_id, None):
                return self.pk_admin.error_no_router_permission(request)
            values = []
            for item in map(self.pk_admin.parser.get_python_type_parse(self.item_col), item_id):
                values.extend(
                    {self.link_col.key: link, self.item_col.key: item}
                    for link in
                    map(self.pk_admin.parser.get_python_type_parse(self.link_col), parser_str_set_list(link_id))
                )
            stmt = insert(self.link_model).values(values)
            try:
                result = await db.execute(stmt)
                if result.rowcount:  # type: ignore
                    await db.commit()
            except Exception as error:
                return self.pk_admin.error_execute_sql(request=request, error=error)
            return BaseApiOut(data=result.rowcount)  # type: ignore

        return route

    async def get_form_item(self, request: Request):
        url = self.pk_admin.app.router_path + self.display_admin.router.url_path_for('page')
        picker = Picker(
            name=self.display_admin_cls.model.__tablename__,
            label=self.display_admin_cls.page_schema.label,
            labelField='name',
            valueField='id', multiple=True,
            required=False, modalMode='dialog', size='full',
            pickerSchema={'&': '${body}'},
            source={
                'method': 'post',
                'data': '${body.api.data}',
                'url': '${body.api.url}&link_model=' + self.pk_admin.model.__tablename__ + '&link_item_id=${api.qsOptions.id}'
            }
        )
        adaptor = None
        if await self.pk_admin.has_update_permission(request, None, None):
            button_create = ActionType.Ajax(
                actionType='ajax', label='添加关联', level=LevelEnum.danger,
                confirmText='确定要添加关联?',
                api=f"post:{self.pk_admin.app.router_path}{self.pk_admin.router.prefix}{self.path}"
                    + '/${REPLACE(query.link_item_id, "!", "")}?link_id=${IF(ids, ids, id)}'
            )  # query.link_item_id
            adaptor = 'if(!payload.hasOwnProperty("_payload")){payload._payload=JSON.stringify(payload);}payload=JSON.parse(payload._payload);button_create=' + button_create.amis_json() \
                      + ';payload.data.body.bulkActions.push(button_create);payload.data.body.itemActions.push(button_create);return payload;'.replace(
                'action_id', 'create' + self.path.replace('/', '_'))
            button_create_dialog = ActionType.Dialog(
                icon='fa fa-plus pull-left',
                label='添加关联',
                level=LevelEnum.danger,
                dialog=Dialog(
                    title='添加关联',
                    size='full',
                    body=Service(
                        schemaApi=AmisAPI(
                            method='get',
                            url=url,
                            cache=20000,
                            responseData={
                                '&': '${body}',
                                'api.url': '${body.api.url}&link_model='
                                           + self.pk_admin.model.__tablename__
                                           + '&link_item_id=!${api.qsOptions.id}',
                            },
                            qsOptions={'id': f'${self.pk_admin.pk_name}'},
                            adaptor=adaptor,
                        )
                    ),
                ),
            )

            button_delete = ActionType.Ajax(
                actionType='ajax', label='移除关联', level=LevelEnum.danger,
                confirmText='确定要移除关联?',
                api=f"delete:{self.pk_admin.app.router_path}{self.pk_admin.router.prefix}{self.path}"
                    + '/${query.link_item_id}?link_id=${IF(ids, ids, id)}'
            )
            adaptor = 'if(!payload.hasOwnProperty("_payload")){payload._payload=JSON.stringify(payload);}payload=JSON.parse(payload._payload);button_delete=' \
                      + button_delete.amis_json() + ';payload.data.body.headerToolbar.push(' + button_create_dialog.amis_json() \
                      + ');payload.data.body.bulkActions.push(button_delete);payload.data.body.itemActions.push(button_delete);return payload;'.replace(
                'action_id', 'delete' + self.path.replace('/', '_'))
        return Service(schemaApi=AmisAPI(
            method='get', url=url, cache=20000,
            responseData=dict(controls=[picker]),
            qsOptions={'id': f'${self.pk_admin.pk_name}'},
            adaptor=adaptor
        ))

    def register_router(self):
        self.pk_admin.router.add_api_route(
            self.path + '/{item_id}',
            self.route_delete,
            methods=["DELETE"],
            response_model=BaseApiOut[int],
            name=f'{self.link_model.name}_Delete',
        )

        self.pk_admin.router.add_api_route(
            self.path + '/{item_id}',
            self.route_create,
            methods=["POST"],
            response_model=BaseApiOut[int],
            name=f'{self.link_model.name}_Create',
        )

        return self


class BaseModelAdmin(SQLModelCrud):
    list_display: List[Union[SQLModelListField, TableColumn]] = []  # 需要显示的字段
    list_filter: List[Union[SQLModelListField, FormItem]] = []  # 需要查询的字段
    list_per_page: int = 10  # 每页数据量
    link_model_fields: List[InstrumentedAttribute] = []  # 内联字段
    link_model_forms: List[LinkModelForm] = []
    bulk_edit_fields: List[Union[SQLModelListField, FormItem]] = []  # 批量编辑字段
    search_fields: List[SQLModelField] = []  # 模糊搜索字段

    def __init__(self, app: "AdminApp"):
        assert self.model, 'model is None'
        assert app, 'app is None'
        self.app = app
        self.session_factory = self.session_factory or self.app.db.session_factory
        self.parser = SQLModelFieldParser(default_model=self.model)
        list_display_insfield = self.parser.filter_insfield(self.list_display)
        self.list_filter = self.list_filter or list_display_insfield
        self.fields = self.fields or [self.model]
        self.fields.extend(list_display_insfield)
        super().__init__(self.model, self.session_factory)

    @cached_property
    def router_path(self) -> str:
        return self.app.router_path + self.router.prefix

    def get_link_model_forms(self) -> List[LinkModelForm]:
        self.link_model_forms = list(
            filter(None, [LinkModelForm.bind_model_admin(self, insfield) for insfield in self.link_model_fields]))
        return self.link_model_forms

    async def get_list_display(self, request: Request) -> List[Union[SQLModelListField, TableColumn]]:
        return self.list_display or list(self.schema_list.__fields__.values())

    async def get_list_filter(self, request: Request) -> List[Union[SQLModelListField, FormItem]]:
        return self.list_filter or list(self.schema_filter.__fields__.values())

    async def get_list_column(self, request: Request, modelfield: ModelField) -> TableColumn:
        return AmisParser(modelfield).as_table_column()

    async def get_list_columns(self, request: Request) -> List[TableColumn]:
        columns = []
        for field in await self.get_list_display(request):
            if isinstance(field, BaseAmisModel):
                columns.append(field)
            elif isinstance(field, SQLModelMetaclass):
                ins_list = self.parser.get_sqlmodel_insfield(field)  # type:ignore
                modelfield_list = [self.parser.get_modelfield(ins, deepcopy=True) for ins in ins_list]
                columns.extend([await self.get_list_column(request, modelfield) for modelfield in modelfield_list])
            else:
                columns.append(await self.get_list_column(request, self.parser.get_modelfield(field, deepcopy=True)))
        for link_form in self.link_model_forms:
            form = await link_form.get_form_item(request)
            if form:
                columns.append(ColumnOperation(
                    width=160, label=link_form.display_admin_cls.page_schema.label, breakpoint='*',
                    buttons=[form]
                ))
        return columns

    async def get_list_filter_api(self, request: Request) -> AmisAPI:
        data = {'&': '$$'}
        for field in self.search_fields:
            alias = self.parser.get_alias(field)
            if alias:
                data[alias] = f'[~]${alias}'
        for field in await self.get_list_filter(request):
            modelfield = self.parser.get_modelfield(field, deepcopy=True)
            if modelfield and issubclass(modelfield.type_, (datetime.datetime, datetime.date, datetime.time)):
                data[modelfield.alias] = f'[-]${modelfield.alias}'
        return AmisAPI(
            method='POST',
            url=f'{self.router_path}/list?'
                + 'page=${page}&perPage=${perPage}&orderBy=${orderBy}&orderDir=${orderDir}',
            data=data,
        )

    async def get_list_table(self, request: Request) -> TableCRUD:
        headerToolbar = ["filter-toggler", "reload", "bulkActions", {"type": "columns-toggler", "align": "right"},
                         {"type": "drag-toggler", "align": "right"}, {"type": "pagination", "align": "right"},
                         {"type": "tpl", "tpl": "当前有 ${total} 条数据.", "className": "v-middle", "align": "right"}]
        headerToolbar.extend(await self.get_actions_on_header_toolbar(request))
        table = TableCRUD(
            api=await self.get_list_filter_api(request),
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
            footerToolbar=["statistics", "switch-per-page", "pagination", "load-more", "export-csv"],
            columns=await self.get_list_columns(request),
            primaryField=self.pk_name,
        )
        if self.link_model_forms:
            table.footable = True
        return table

    async def get_form_item_on_foreign_key(self, request: Request,
                                           modelfield: ModelField) -> Union[Service, SchemaNode]:
        column = self.parser.get_column(modelfield.alias)
        if column is None:
            return None
        foreign_keys = list(column.foreign_keys) or None
        if foreign_keys is None:
            return None
        admin = self.app.get_model_admin(foreign_keys[0].column.table.name)
        if not admin:
            return None
        url = self.app.router_path + admin.router.url_path_for('page')
        label = modelfield.field_info.title or modelfield.name
        remark = Remark(content=modelfield.field_info.description) if modelfield.field_info.description else None
        picker = Picker(name=modelfield.alias, label=label, labelField='name', valueField='id',
                        required=modelfield.required, modalMode='dialog',
                        size='full', labelRemark=remark, pickerSchema='${body}', source='${body.api}')
        return Service(
            schemaApi=AmisAPI(method='get', url=url, cache=20000, responseData=dict(controls=[picker])))

    async def get_form_item(self, request: Request, modelfield: ModelField,
                            action: CrudEnum) -> Union[FormItem, SchemaNode]:
        is_filter = action == CrudEnum.list
        return await self.get_form_item_on_foreign_key(request, modelfield) or AmisParser(modelfield).as_form_item(
            is_filter=is_filter)

    async def get_list_filter_form(self, request: Request) -> Form:
        body = await self._conv_modelfields_to_formitems(request, await self.get_list_filter(request),
                                                         CrudEnum.list)
        return Form(
            type='',
            title='数据筛选',
            name=CrudEnum.list,
            body=body,
            mode=DisplayModeEnum.inline,
            actions=[
                Action(
                    actionType='clear-and-submit',
                    label='清空',
                    level=LevelEnum.default,
                ),
                Action(
                    actionType='reset-and-submit',
                    label='重置',
                    level=LevelEnum.default,
                ),
                Action(actionType='submit', label='搜索', level=LevelEnum.primary),
            ],
            trimValues=True,
        )

    async def get_create_form(self, request: Request, bulk: bool = False) -> Form:
        api = f'post:{self.router_path}/item'
        fields = [field for field in self.schema_create.__fields__.values() if field.name != self.pk_name]
        return Form(
            api=api,
            name=CrudEnum.create,
            body=await self._conv_modelfields_to_formitems(
                request, fields, CrudEnum.create
            ),
            submitText=None,
        )

    async def get_update_form(self, request: Request, bulk: bool = False) -> Form:
        if not bulk:
            api = f'put:{self.router_path}/item/${self.pk_name}'
            fields = self.schema_update.__fields__.values()
        else:
            api = f'put:{self.router_path}/item/' + '${ids|raw}'
            fields = self.bulk_edit_fields
        return Form(
            api=api,
            name=CrudEnum.update,
            body=await self._conv_modelfields_to_formitems(
                request, fields, CrudEnum.update
            ),
            submitText=None,
            trimValues=True,
        )

    async def get_create_action(self, request: Request, bulk: bool = False) -> Optional[Action]:
        return ActionType.Dialog(
            icon='fa fa-plus pull-left',
            label='新增',
            level=LevelEnum.primary,
            dialog=Dialog(
                title='新增',
                size=SizeEnum.lg,
                body=await self.get_create_form(request, bulk=bulk),
            ),
        ) if await self.has_create_permission(request, None) else None

    async def get_update_action(self, request: Request, bulk: bool = False) -> Optional[Action]:
        if not await self.has_update_permission(request, None, None):
            return None
        # 开启批量编辑
        if not bulk:
            return ActionType.Dialog(
                icon='fa fa-pencil',
                tooltip='编辑',
                dialog=Dialog(
                    title='编辑',
                    size=SizeEnum.lg,
                    body=await self.get_update_form(request, bulk=bulk),
                ),
            )

        elif self.bulk_edit_fields:
            return ActionType.Dialog(
                label='批量修改',
                dialog=Dialog(
                    title='批量修改',
                    size=SizeEnum.lg,
                    body=await self.get_update_form(request, bulk=True),
                ),
            )

        else:
            return None

    async def get_delete_action(self, request: Request, bulk: bool = False) -> Optional[Action]:
        if not await self.has_delete_permission(request, None):
            return None
        return ActionType.Ajax(
            label='批量删除',
            confirmText='确定要批量删除?',
            api=f"delete:{self.router_path}/item/" + '${ids|raw}',
        ) if bulk else ActionType.Ajax(
            icon='fa fa-times text-danger',
            tooltip='删除',
            confirmText='您确认要删除?',
            api=f"delete:{self.router_path}/item/${self.pk_name}",
        )

    async def get_actions_on_header_toolbar(self, request: Request) -> List[Action]:
        actions = [await self.get_create_action(request, bulk=False)]
        return list(filter(None, actions))

    async def get_actions_on_item(self, request: Request) -> List[Action]:
        actions = [await self.get_update_action(request, bulk=False),
                   await self.get_delete_action(request, bulk=False)
                   ]
        return list(filter(None, actions))

    async def get_actions_on_bulk(self, request: Request) -> List[Action]:
        bulkActions = [await self.get_update_action(request, bulk=True),
                       await self.get_delete_action(request, bulk=True)]

        return list(filter(None, bulkActions))

    async def _conv_modelfields_to_formitems(self, request: Request,
                                             fields: Iterable[Union[SQLModelListField, ModelField, FormItem]],
                                             action: CrudEnum = None) -> List[FormItem]:
        items = []
        for field in fields:
            if isinstance(field, FormItem):
                items.append(field)
            else:
                field = self.parser.get_modelfield(field, deepcopy=True)
                if field:
                    item = await self.get_form_item(request, field, action)
                    if item:
                        items.append(item)
        return items


class BaseAdmin:
    def __init__(self, app: "AdminApp"):
        self.app = app
        assert self.app, 'app is None'

    @cached_property
    def site(self) -> "BaseAdminSite":
        return self.app if isinstance(self.app, BaseAdminSite) else self.app.site


class PageSchemaAdmin(BaseAdmin):
    group_schema: Union[PageSchema, str] = PageSchema()
    page_schema: Union[PageSchema, str] = PageSchema()

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.page_schema = self.get_page_schema()
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
                self.group_schema.label = self.group_schema.label or 'default'
            else:
                raise TypeError()
        return self.group_schema


class LinkAdmin(PageSchemaAdmin):
    link: str = ''

    def get_page_schema(self) -> Optional[PageSchema]:
        super().get_page_schema()
        if self.page_schema:
            self.page_schema.link = self.page_schema.link or self.link
        return self.page_schema


class IframeAdmin(PageSchemaAdmin):
    iframe: Iframe = None
    src: str = ''

    def get_page_schema(self) -> Optional[PageSchema]:
        super().get_page_schema()
        if self.page_schema:
            iframe = self.iframe or Iframe(src=self.src)
            self.page_schema.url = re.sub(r"^https?://", "", iframe.src)
            self.page_schema.schema_ = Page(body=iframe)
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
    """Amis页面管理"""
    page: Page = None
    page_path: Optional[str] = None
    page_parser_mode: Literal["json", "html"] = 'json'
    page_route_kwargs: Dict[str, Any] = {}
    template_name: str = ''
    router_prefix = '/page'

    def __init__(self, app: "AdminApp"):
        RouterAdmin.__init__(self, app)
        if self.page_path is None:
            self.page_path = f'/{self.__class__.__module__}/{self.__class__.__name__.lower()}/amis.json'
        PageSchemaAdmin.__init__(self, app)

    async def page_permission_depend(self, request: Request) -> bool:
        return await self.has_page_permission(request) or self.error_no_page_permission(request)

    def error_no_page_permission(self, request: Request):
        page_parser_mode = request.query_params.get('_parser') or self.page_parser_mode
        raise HTTPException(status_code=status.HTTP_307_TEMPORARY_REDIRECT, detail='No page permissions',
                            headers={
                                'location': f'{self.app.site.router_path}/auth/form/login?_parser={page_parser_mode}&redirect={request.url}'})

    async def get_page(self, request: Request) -> Page:
        return self.page or Page()

    def get_page_schema(self) -> Optional[PageSchema]:
        super().get_page_schema()
        if self.page_schema:
            self.page_schema.url = f'{self.router_path}{self.page_path}'  # ?_parser=html
            self.page_schema.schemaApi = f'{self.router_path}{self.page_path}'
            if self.page_parser_mode == 'html':
                self.page_schema.schema_ = Page(body=Iframe(src=self.page_schema.schemaApi))
        return self.page_schema

    def page_parser(self, request: Request, page: Page) -> Response:
        mode = request.query_params.get('_parser') or self.page_parser_mode
        result = None
        if mode == 'json':
            result = BaseAmisApiOut(data=page.amis_dict())
            result = JSONResponse(result.dict())
        elif mode == 'html':
            result = page.amis_html(self.template_name)
            result = HTMLResponse(result)
        return result

    def register_router(self):
        kwargs = {**self.page_route_kwargs}
        if self.page_parser_mode == 'json':
            kwargs.update(dict(response_model=BaseAmisApiOut))
        else:
            kwargs.update(dict(response_class=HTMLResponse))
        self.router.add_api_route(
            self.page_path,
            self.route_page,
            methods=["GET"],
            name='page', **kwargs,
            dependencies=[Depends(self.page_permission_depend)],
            include_in_schema=False,
        )
        return self

    @property
    def route_page(self) -> Callable:
        async def route(request: Request, page: Page = Depends(self.get_page)):
            return self.page_parser(request, page)

        return route


class TemplateAdmin(PageAdmin):
    """Jinja2渲染模板管理"""
    page: Dict[str, Any] = {}
    page_parser_mode = 'html'
    templates: Jinja2Templates = None

    def __init__(self, app: "AdminApp"):
        assert self.templates, 'templates:Jinja2Templates is None'
        assert self.template_name, 'template_name is None'
        self.page_path = self.page_path or f'/{self.template_name}'
        super().__init__(app)

    def page_parser(self, request: Request, page: Dict[str, Any]) -> Response:
        page['request'] = request
        return self.templates.TemplateResponse(self.template_name, page)

    async def get_page(self, request: Request) -> Dict[str, Any]:
        return {}


class BaseFormAdmin(PageAdmin):
    schema: Type[BaseModel]
    schema_init_out: Type[Any] = Any
    schema_submit_out: Type[Any] = Any
    form: Form = None
    form_init: bool = None
    form_path: str = ''
    route_init: Callable = None
    route_submit: Callable = None
    router_prefix: str = '/form'

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        assert self.route_submit, 'route_submit is None'
        self.form_path = self.form_path or self.page_path.replace('/amis.json', '') + '/api'

    async def get_page(self, request: Request) -> Page:
        page = await super(BaseFormAdmin, self).get_page(request)
        page.body = await self.get_form(request)
        return page

    async def get_form_item(self, request: Request, modelfield: ModelField) -> Union[FormItem, SchemaNode]:
        return AmisParser(modelfield).as_form_item()

    async def get_form(self, request: Request) -> Form:
        form = self.form or Form()
        form.api = AmisAPI(method='POST', url=f"{self.router_path}{self.form_path}")
        form.initApi = AmisAPI(method='GET', url=f"{self.router_path}{self.form_path}") if self.form_init else None
        form.title = ''
        form.body = []
        if self.schema:
            for modelfield in self.schema.__fields__.values():
                formitem = await self.get_form_item(request, modelfield)
                if formitem:
                    form.body.append(formitem)
        return form

    def register_router(self):
        super().register_router()
        self.router.add_api_route(self.form_path, self.route_submit, methods=["POST"],
                                  response_model=BaseApiOut[self.schema_submit_out],
                                  dependencies=[Depends(self.page_permission_depend)])
        if self.form_init:
            self.schema_init_out = self.schema_init_out or schema_create_by_schema(self.schema,
                                                                                   self.__class__.__name__ + 'InitOut',
                                                                                   set_none=True)
            self.router.add_api_route(self.form_path, self.route_init, methods=["GET"],
                                      response_model=BaseApiOut[self.schema_init_out],
                                      dependencies=[Depends(self.page_permission_depend)])
        return self


class FormAdmin(BaseFormAdmin):
    """表单管理"""

    @property
    def route_submit(self):
        async def route(request: Request, data: self.schema):  # type:ignore
            return await self.handle(request, data)

        return route

    async def handle(self, request: Request, data: BaseModel, **kwargs) -> BaseApiOut[Any]:
        return BaseApiOut(data=data)

    async def get_init_data(self, request: Request, **kwargs) -> BaseApiOut[Any]:
        return BaseApiOut(data=None)

    @property
    def route_init(self):
        async def route(request: Request):
            return await self.get_init_data(request)

        return route


class ModelFormAdmin(FormAdmin, SQLModelSelector):
    """todo Read and update a model resource """

    def __init__(self, app: "AdminApp"):
        FormAdmin.__init__(self, app)
        SQLModelSelector.__init__(self)


class ModelAdmin(BaseModelAdmin, PageAdmin):
    """模型管理"""
    page_path: str = '/amis.json'
    bind_model: bool = True

    def __init__(self, app: "AdminApp"):
        BaseModelAdmin.__init__(self, app)
        PageAdmin.__init__(self, app)

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

    async def has_list_permission(self, request: Request,
                                  paginator: Paginator,
                                  filter: BaseModel = None,  # type self.schema_filter
                                  **kwargs) -> bool:
        return await self.has_page_permission(request)

    async def has_create_permission(self, request: Request,
                                    data: BaseModel,  # type self.schema_create
                                    **kwargs) -> bool:
        return await self.has_page_permission(request)

    async def has_read_permission(self, request: Request, item_id: List[str], **kwargs) -> bool:
        return await self.has_page_permission(request)

    async def has_update_permission(self, request: Request, item_id: List[str],
                                    data: BaseModel,  # type self.schema_update
                                    **kwargs) -> bool:
        return await self.has_page_permission(request)

    async def has_delete_permission(self, request: Request, item_id: List[str], **kwargs) -> bool:
        return await self.has_page_permission(request)


class BaseModelAction:
    admin: "ModelAdmin" = None
    action: Action = None

    def __init__(self, admin: "ModelAdmin"):
        self.admin = admin
        assert self.admin, 'admin is None'

    async def fetch_item_scalars(self, session: AsyncSession, item_id: List[str]) -> ScalarResult:
        result = await session.execute(select(self.admin.model).where(self.admin.pk.in_(item_id)))
        return result.scalars()

    def register_router(self):
        raise NotImplementedError


class ModelAction(BaseFormAdmin, BaseModelAction):
    schema: Type[BaseModel] = None
    action: ActionType.Dialog = None

    def __init__(self, admin: "ModelAdmin"):
        BaseModelAction.__init__(self, admin)
        self.router = self.admin.router
        BaseFormAdmin.__init__(self, self.admin.app)

    async def get_action(self, request: Request, **kwargs) -> Action:
        action = self.action or ActionType.Dialog(label='自定义表单动作', dialog=Dialog())
        action.dialog.title = action.label
        action.dialog.body = Service(schemaApi=AmisAPI(method='get',
                                                       url=self.router_path + self.page_path + '?item_id=${IF(ids, ids, id)}',
                                                       responseData={'&': '${body}',
                                                                     'api.url': '${body.api.url}?item_id=${api.query.item_id}',
                                                                     'submitText': ''}))
        return action

    async def handle(self, request: Request, item_id: List[str], data: Optional[BaseModel],
                     session: AsyncSession, **kwargs) -> BaseApiOut[Any]:
        return BaseApiOut(data=data)

    @property
    def route_submit(self):
        default = ... if self.schema else None

        async def route(request: Request, data: self.schema = Body(default=default),  # type:ignore
                        item_id: str = Query(None, title='item_id', example='1,2,3',
                                             description='Primary key or list of primary keys'),
                        session: AsyncSession = Depends(self.admin.session_factory),
                        ):
            return await self.handle(request, parser_str_set_list(set_str=item_id), data, session)

        return route


class AdminApp(PageAdmin):
    group_schema: Union[PageSchema, str] = None
    engine: AsyncEngine = None
    page_path = '/amis.json'
    page_parser_mode = 'json'

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.engine = self.engine or self.app.site.engine
        assert self.engine, 'engine is None'
        self.db = SqlalchemyAsyncClient(self.engine)
        self._pages_dict: Dict[str, Tuple[PageSchema, List[Union[PageSchema, BaseAdmin]]]] = {}
        self._admins_dict: Dict[Type[BaseAdmin], Optional[BaseAdmin]] = {}

    def get_page_schema(self) -> Optional[PageSchema]:
        super().get_page_schema()
        if self.page_schema:
            self.page_schema.url = None
            self.page_schema.schemaApi = None
        return self.page_schema

    def create_admin_instance(self, admin_cls: Type[_BaseAdminT]) -> _BaseAdminT:
        admin = self._admins_dict.get(admin_cls)
        if admin is not None or not issubclass(admin_cls, BaseAdmin):
            return admin
        admin = admin_cls(self)  # type: ignore
        self._admins_dict[admin_cls] = admin
        if isinstance(admin, PageSchemaAdmin):
            group_label = admin.group_schema and admin.group_schema.label
            if admin.page_schema:
                if not self._pages_dict.get(group_label):
                    self._pages_dict[group_label] = (admin.group_schema, [])
                self._pages_dict[group_label][1].append(admin)
        return admin

    def create_admin_instance_all(self) -> None:
        [self.create_admin_instance(admin_cls) for admin_cls in self._admins_dict.keys()]

    def _register_admin_router_all_pre(self):
        [admin.get_link_model_forms() for admin in self._admins_dict.values() if isinstance(admin, ModelAdmin)]

    def _register_admin_router_all(self):
        for admin in self._admins_dict.values():
            if isinstance(admin, RouterAdmin):  # 注册路由
                admin.register_router()
                self.router.include_router(admin.router)

    def route_index(self):
        return RedirectResponse(url=self.router_path + self.page_path + '?_parser=html')

    def register_router(self):
        super(AdminApp, self).register_router()
        self.router.add_api_route('/', self.route_index, name='index', include_in_schema=False)
        self.create_admin_instance_all()
        self._register_admin_router_all_pre()
        self._register_admin_router_all()
        return self

    @lru_cache()
    def get_model_admin(self, table_name: str) -> Optional[ModelAdmin]:
        for admin_cls, admin in self._admins_dict.items():
            if issubclass(admin_cls,
                          ModelAdmin) and admin_cls.bind_model and admin_cls.model.__tablename__ == table_name:
                return admin
            elif isinstance(admin, AdminApp):
                return admin.get_model_admin(table_name)
        return None

    def register_admin(self, *admin_cls: Type[_BaseAdminT]) -> Type[_BaseAdminT]:
        [self._admins_dict.update({cls: None}) for cls in admin_cls if cls]
        return admin_cls[0]

    def unregister_admin(self, *admin_cls: Type[BaseAdmin]):
        [self._admins_dict.pop(cls) for cls in admin_cls if cls]

    async def get_page(self, request: Request) -> App:
        app = App(api=self.router_path + self.page_path)
        app.brandName = 'AmisAdmin'
        app.header = Tpl(className='w-full',
                         tpl='<div class="flex justify-between"><div></div>'
                             f'<div><a href="{fastapi_amis_admin.__url__}" target="_blank" '
                             'title="版权信息,不可删除!"><i class="fa fa-github fa-2x"></i></a></div></div>')
        app.footer = '<div class="p-2 text-center bg-light">Copyright © 2021 - 2022  ' \
                     f'<a href="{fastapi_amis_admin.__url__}" target="_blank" ' \
                     'class="link-secondary">fastapi-amis-admin</a>. All rights reserved. ' \
                     f'<a target="_blank" href="{fastapi_amis_admin.__url__}" ' \
                     f'class="link-secondary" rel="noopener">v{fastapi_amis_admin.__version__}</a></div> '
        # app.asideBefore = '<div class="p-2 text-center">菜单前面区域</div>'
        # app.asideAfter = f'<div class="p-2 text-center"><a href="{fastapi_amis_admin.__url__}"  target="_blank">fastapi-amis-admin</a></div>'
        _parser = request.query_params.get('_parser') or self.page_parser_mode
        if _parser == 'json':
            children = await self.get_page_schema_children(request)
            app.pages = [{'children': children}] if children else []
        return app

    async def get_page_schema_children(self, request: Request) -> List[PageSchema]:
        children = []
        for group_label, (group_schema, admins_list) in self._pages_dict.items():
            lst = []
            for admin in admins_list:
                if admin and isinstance(admin, PageSchemaAdmin):
                    if await admin.has_page_permission(request):
                        if isinstance(admin, AdminApp):
                            sub_children = await admin.get_page_schema_children(request)
                            if sub_children:
                                page_schema = admin.page_schema.copy(deep=True)
                                page_schema.children = sub_children
                                lst.append(page_schema)
                        else:
                            lst.append(admin.page_schema)
                else:
                    lst.append(admin)
            if lst:
                if group_label:
                    lst.sort(key=lambda p: p.sort or 0, reverse=True)
                    group_schema = group_schema.copy(deep=True)
                    group_schema.children = lst
                    children.append(group_schema)
                else:  # ModelAdmin
                    children.extend(lst)
        if children:
            children.sort(key=lambda p: p.sort or 0, reverse=True)
        return children


class BaseAdminSite(AdminApp):

    def __init__(self, settings: Settings, fastapi: FastAPI = None, engine: AsyncEngine = None):
        self.auth = None
        self.settings = settings
        self.fastapi = fastapi or FastAPI(debug=settings.debug, reload=settings.debug)
        self.router = self.fastapi.router
        self.engine = engine or create_async_engine(settings.database_url_async, echo=settings.debug, future=True)
        super().__init__(self)

    @cached_property
    def router_path(self) -> str:
        return self.settings.site_url + self.settings.root_path + self.router.prefix

    def mount_app(self, fastapi: FastAPI, name: str = None) -> None:
        self.register_router()
        fastapi.mount(self.settings.root_path, self.fastapi, name=name)

    async def create_db_and_tables(self) -> None:
        async with self.db.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
