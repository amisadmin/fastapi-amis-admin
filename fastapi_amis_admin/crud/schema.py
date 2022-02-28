from enum import Enum
from typing import Dict, TypeVar, Optional, Generic, List, Any, Union
import ujson
from pydantic import BaseModel, Extra
from pydantic.generics import GenericModel

_T = TypeVar('_T')


class BaseApiSchema(BaseModel):
    class Config:
        extra = Extra.allow
        json_loads = ujson.loads
        json_dumps = ujson.dumps


class BaseApiOut(GenericModel, Generic[_T], BaseApiSchema):
    status: int = 0
    msg: str = 'success'
    data: Optional[_T] = None
    code: int = None


class ItemListSchema(GenericModel, Generic[_T], BaseApiSchema):
    """数据查询返回格式"""
    items: List[_T]  # 数据列表
    total: int = None  # 数据总量
    query: Dict[str, Any] = None
    filter: Dict[str, Any] = None


class CrudEnum(str, Enum):
    list = 'list'  # 批量查询数据
    create = 'create'  # 新增数据
    read = 'read'  # 查询数据
    update = 'update'  # 更新数据
    delete = 'delete'  # 删除数据


class Paginator():
    perPageMax: int = None

    def __init__(self, page: Union[int, str] = 1, perPage: Union[int, str] = 10, show_total: int = 1,
                 orderBy: str = None,
                 orderDir: str = 'asc'):
        self.page = page if page and page > 0 else 1
        self.perPage = perPage if perPage and perPage > 0 else 10
        if self.perPageMax:
            self.perPage = self.perPage if self.perPage <= self.perPageMax else self.perPageMax
        self.show_total = show_total
        self.orderBy = orderBy
        self.orderDir = orderDir
