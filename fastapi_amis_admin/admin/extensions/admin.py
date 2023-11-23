import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Set, Union

from sqlalchemy.engine import Result
from sqlalchemy.sql import Select
from starlette.requests import Request

from fastapi_amis_admin.admin.admin import AdminAction, AdminApp, FormAdmin, ModelAdmin
from fastapi_amis_admin.admin.extensions.schemas import FieldPermEnum, SelectPerm
from fastapi_amis_admin.admin.extensions.utils import get_schema_fields_name_label
from fastapi_amis_admin.amis import FormItem, SchemaNode, TableColumn, TableCRUD
from fastapi_amis_admin.crud.base import ItemListSchema, SchemaCreateT, SchemaFilterT, SchemaModelT, SchemaReadT, SchemaUpdateT
from fastapi_amis_admin.crud.parser import TableModelT
from fastapi_amis_admin.crud.schema import CrudEnum
from fastapi_amis_admin.utils.functools import cached_property
from fastapi_amis_admin.utils.pydantic import ModelField
from fastapi_amis_admin.utils.translation import i18n as _


class ReadOnlyModelAdmin(ModelAdmin):
    """只读模型管理Mixin
    移除了创建,更新,删除等操作
    """

    @cached_property
    def registered_admin_actions(self) -> Dict[str, "AdminAction"]:
        actions = super().registered_admin_actions
        return {
            key: action
            for key, action in actions.items()
            if key not in {"create", "update", "delete", "bulk_delete", "bulk_update", "bulk_create"}
        }

    async def has_create_permission(self, request: Request, data: SchemaUpdateT, **kwargs) -> bool:
        return False

    async def has_update_permission(
        self,
        request: Request,
        item_id: List[str],
        data: SchemaUpdateT,
        **kwargs,
    ) -> bool:
        return False

    async def has_delete_permission(self, request: Request, item_id: List[str], **kwargs) -> bool:
        return False


class AutoTimeModelAdmin(ModelAdmin):
    """禁止修改模型管理时间字段.没有Id,创建时间,更新时间,删除时间等字段的创建和更新"""

    create_exclude = {
        "id",
        "create_time",
        "update_time",
        "delete_time",
    }
    update_exclude = {
        "id",
        "create_time",
        "update_time",
        "delete_time",
    }


class SoftDeleteModelAdmin(AutoTimeModelAdmin):
    """软删除模型管理Mixin.
    - 需要在模型中定义delete_time字段.如果delete_time字段为None,则表示未删除.
    """

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        assert hasattr(self.model, "delete_time"), "SoftDeleteModelAdmin需要在模型中定义delete_time字段"

    async def get_select(self, request: Request):
        sel = await super().get_select(request)
        return sel.where(self.model.delete_time == None)  # noqa E711

    def delete_item(self, obj: SchemaModelT) -> None:
        obj.delete_time = datetime.now()


class FootableModelAdmin(ModelAdmin):
    """为模型管理Amis表格添加底部展示(Footable)属性"""

    async def get_list_table(self, request: Request) -> TableCRUD:
        table = await super().get_list_table(request)
        table.footable = True
        return table


class ToggledModelAdmin(ModelAdmin):
    """为模型管理Amis表格列字段添加toggled属性"""

    toggled_columns: List[str] = []

    async def get_list_columns(self, request: Request) -> List[TableColumn]:
        columns = await super().get_list_columns(request)
        for column in columns:
            if column and column.name in self.toggled_columns:
                column.toggled = False
        return columns


class BaseAuthFieldModelAdmin(ModelAdmin):
    """字段级别权限控制模型管理.
    - xxx_permission_fields:
        1.动作权限字段,可以通过覆盖这些属性来控制哪些字段需要进行权限验证.
        2.未设置的字段,则不进行权限验证.
        3.一旦类被实例化,则会缓存这些属性,禁止再次修改.
    #todo 优化
    """

    perm_fields: Dict[Union[FieldPermEnum, int], Sequence[str]] = None
    """指定的字段,进行权限验证."""
    perm_fields_exclude: Dict[Union[FieldPermEnum, int], Sequence[str]] = None
    """exclude指定的字段,不进行权限验证."""

    def __init__(self, app: "AdminApp"):
        super().__init__(app)

    def get_permission_fields(self, action: str) -> Dict[str, str]:
        """获取权限字段"""
        info = {
            "list": (self.schema_list, _("List display")+'-', FieldPermEnum.LIST),
            "filter": (self.schema_filter, _("List filter")+'-', FieldPermEnum.FILTER),
            "create": (self.schema_create, _("Create")+'-', FieldPermEnum.CREATE),
            "read": (self.schema_read, _("Read")+'-', FieldPermEnum.READ),
            "update": (self.schema_update, _("Update")+'-', FieldPermEnum.UPDATE),
        }
        if action not in info:
            return {}
        schema, prefix, perm = info[action]
        perm_fields_exclude = self.perm_fields_exclude or {}
        perm_fields = self.perm_fields or {}
        exclude = set()
        for k, fields in perm_fields_exclude.items():
            if (k & perm) == perm:
                exclude.update(set(fields))
        include = set()
        for k, fields in perm_fields.items():
            if (k & perm) == perm:
                include.update(set(fields))
        return get_schema_fields_name_label(schema, prefix=prefix, exclude_required=True, exclude=exclude, include=include)

    @cached_property
    def create_permission_fields(self) -> Dict[str, str]:
        """创建权限字段"""
        return self.get_permission_fields("create")

    @cached_property
    def read_permission_fields(self) -> Dict[str, str]:
        """读取权限字段"""
        return self.get_permission_fields("read")

    @cached_property
    def update_permission_fields(self) -> Dict[str, str]:
        """更新权限字段"""
        return self.get_permission_fields("update")

    @cached_property
    def list_permission_fields(self) -> Dict[str, str]:
        """列表权限字段"""
        return self.get_permission_fields("list")

    @cached_property
    def filter_permission_fields(self) -> Dict[str, str]:
        """过滤筛选权限字段"""
        return self.get_permission_fields("filter")

    async def has_field_permission(self, request: Request, field: str, action: str = "") -> bool:
        """判断用户是否有字段权限"""
        return True

    async def get_deny_fields(self, request: Request, action: str = None) -> Set[str]:
        """获取没有权限的字段"""
        cache_key = f"{self.unique_id}_exclude_fields"
        request_cache = request.scope.get(cache_key, {})
        if action in request_cache:
            return request_cache[action]
        check_fields = {}
        if action == "list":
            check_fields = self.list_permission_fields.keys()
        elif action == "filter":
            check_fields = self.filter_permission_fields.keys()
        elif action == "create":
            check_fields = self.create_permission_fields.keys()
        elif action == "update":
            check_fields = self.update_permission_fields.keys()
        elif action == "read":
            check_fields = self.read_permission_fields.keys()
        else:
            pass
        fields = {field for field in check_fields if not await self.has_field_permission(request, field, action)}
        request_cache[action] = fields
        if cache_key not in request.scope:
            request.scope[cache_key] = request_cache
        return fields

    async def on_list_after(self, request: Request, result: Result, data: ItemListSchema, **kwargs) -> ItemListSchema:
        """Parse the database data query result dictionary into schema_list."""
        exclude = await self.get_deny_fields(request, "list")  # 过滤没有权限的字段
        data = await super().on_list_after(request, result, data, **kwargs)
        data.items = [item.dict(exclude=exclude) for item in data.items]  # 过滤没有权限的字段
        return data

    async def on_filter_pre(self, request: Request, obj: Optional[SchemaFilterT], **kwargs) -> Dict[str, Any]:
        data = await super().on_filter_pre(request, obj, **kwargs)
        if not data:
            return data
        exclude = await self.get_deny_fields(request, "filter")  # 过滤没有权限的字段
        return {k: v for k, v in data.items() if k not in exclude}

    async def create_items(self, request: Request, items: List[SchemaCreateT]) -> List[TableModelT]:
        """Create multiple data"""
        exclude = await self.get_deny_fields(request, "create")
        items = [item.copy(exclude=exclude) for item in items]  # 过滤没有权限的字段
        items = await super().create_items(request, items)
        return items

    async def read_items(self, request: Request, item_id: List[str]) -> List[SchemaReadT]:
        """Read multiple data"""
        items = await super().read_items(request, item_id)
        exclude = await self.get_deny_fields(request, "read")  # 过滤没有权限的字段
        return [item.copy(exclude=exclude) for item in items]

    async def on_update_pre(
        self,
        request: Request,
        obj: SchemaUpdateT,
        item_id: Union[List[str], List[int]],
        **kwargs,
    ) -> Dict[str, Any]:
        exclude = await self.get_deny_fields(request, "update")  # 过滤没有权限的字段
        obj = obj.copy(exclude=exclude)  # 过滤没有权限的字段
        data = await super().on_update_pre(request, obj, item_id, **kwargs)
        return data

    async def get_form_item(
        self, request: Request, modelfield: ModelField, action: CrudEnum
    ) -> Union[FormItem, SchemaNode, None]:
        """过滤前端创建,更新,筛选表单字段"""
        # action为list时,表示列表展示字段.否则为筛选表单字段
        act = "filter" if action == "list" else action
        exclude = await self.get_deny_fields(request, act)  # 获取没有权限的字段
        name = modelfield.alias or modelfield.name
        if name in exclude:
            return None
        form_item = await super().get_form_item(request, modelfield, action)
        return form_item

    async def get_list_column(self, request: Request, modelfield: ModelField) -> Optional[TableColumn]:
        """过滤前端展示字段"""
        exclude = await self.get_deny_fields(request, "list")  # 获取没有权限的字段
        name = modelfield.alias or modelfield.name
        if name in exclude:
            return None
        column = await super().get_list_column(request, modelfield)
        return column


class BaseAuthSelectModelAdmin(ModelAdmin):
    """选择数据集权限控制的模型管理"""

    select_permissions: List[SelectPerm] = []
    """需要进行权限控制的数据集列表"""

    async def has_select_permission(self, request: Request, name: str) -> bool:
        """判断用户是否有数据集权限"""
        return True

    async def get_select(self, request: Request) -> Select:
        sel = await super().get_select(request)
        return await self.filter_select(request, sel)

    async def filter_select(self, request: Request, sel: Select) -> Select:
        """在sel中添加权限过滤条件"""
        for permission in self.select_permissions:
            if not isinstance(permission, SelectPerm):
                continue
            effect = await self.has_select_permission(request, permission.name)
            # 如果权限为反向权限,则判断用户是否没有权限
            if permission.reverse ^ effect:
                sel = permission.call(self, request, sel)
                if asyncio.iscoroutine(sel):
                    sel = await sel
        return sel


class BaseAuthFieldFormAdmin(FormAdmin):
    """#todo 字段级别权限控制表单管理"""

    pass
