from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Awaitable, Callable, List, Union

from sqlalchemy.sql import Select
from starlette.requests import Request

from fastapi_amis_admin.admin import ModelAdmin


class FieldPermEnum(int, Enum):
    LIST = 1 << 0
    FILTER = 1 << 1
    CREATE = 1 << 2
    READ = 1 << 3
    UPDATE = 1 << 4
    ALL = LIST | FILTER | CREATE | READ | UPDATE
    VIEW = LIST | FILTER | READ
    EDIT = CREATE | UPDATE


SelectPermCallable = Callable[[ModelAdmin, Request, Select], Union[Select, Awaitable[Select]]]


@dataclass
class SelectPerm:
    name: str
    label: str
    reverse: bool = False
    call: SelectPermCallable = None

    def __post_init__(self):
        if self.call is None and hasattr(self, "_call"):
            self.call = self._call
        assert self.call is not None, "call must be set"


@dataclass
class RecentTimeSelectPerm(SelectPerm):
    """最近时间选择数据集"""

    td: Union[int, timedelta] = 60 * 60 * 24 * 7
    time_column: str = "create_time"

    def __post_init__(self):
        super().__post_init__()
        # 如果td为int,则表示秒数
        self.td = timedelta(seconds=self.td) if isinstance(self.td, int) else self.td

    async def _call(self, admin: ModelAdmin, request: Request, sel: Select) -> Select:
        column = getattr(admin.model, self.time_column)
        return sel.where(column > datetime.now() - self.td)


@dataclass
class UserSelectPerm(SelectPerm):
    """所属用户选择数据集,只能选择匹配当前用户的数据"""

    user_column: str = "user_id"
    user_attr: str = "id"

    async def _call(self, admin: ModelAdmin, request: Request, sel: Select) -> Select:
        user = await admin.site.auth.get_current_user(request)
        if not user:  # 未登录
            return sel.where(False)
        column = getattr(admin.model, self.user_column)
        return sel.where(column == getattr(user, self.user_attr))


@dataclass
class SimpleSelectPerm(SelectPerm):
    """简单列选择数据集"""

    values: Union[List[str], List[int]] = None
    column: str = "status"

    async def _call(self, admin: ModelAdmin, request: Request, sel: Select) -> Select:
        if not self.values:
            return sel
        column = getattr(admin.model, self.column)
        if len(self.values) == 1:
            return sel.where(column == self.values[0])
        return sel.where(column.in_(self.values))


@dataclass
class FilterSelectPerm(SelectPerm):
    """filter(where)子句选择数据集"""

    filters: list = None

    async def _call(self, admin: ModelAdmin, request: Request, sel: Select) -> Select:
        if not self.filters:
            return sel
        return sel.filter(*self.filters)
