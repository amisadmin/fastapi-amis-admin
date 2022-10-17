from datetime import datetime
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel, Extra
from pydantic.generics import GenericModel

try:
    import ujson as json
except ImportError:
    import json

_T = TypeVar("_T")


class BaseApiSchema(BaseModel):
    class Config:
        extra = Extra.allow
        json_loads = json.loads
        json_dumps = json.dumps
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
        }


class BaseApiOut(GenericModel, Generic[_T], BaseApiSchema):
    status: int = 0
    msg: str = "success"
    data: Optional[_T] = None
    code: int = None


class ItemListSchema(GenericModel, Generic[_T], BaseApiSchema):
    """Data list query return format."""

    items: List[_T] = []  # Data list
    total: int = None  # Data total
    query: Dict[str, Any] = None
    filter: Dict[str, Any] = None


class CrudEnum(str, Enum):
    list = "list"
    create = "create"
    read = "read"
    update = "update"
    delete = "delete"


class Paginator:
    """Used for data paging when querying a data list."""

    def __init__(self, perPage_max: Optional[int] = None):
        self.perPageMax = perPage_max

    def __call__(
        self,
        page: Union[int, str] = 1,
        perPage: Union[int, str] = 10,
        show_total: int = 1,
        orderBy: str = None,
        orderDir: str = "asc",
    ):
        self.page = page if page and page > 0 else 1
        self.perPage = perPage if perPage and perPage > 0 else 10
        if self.perPageMax:
            self.perPage = min(self.perPage, self.perPageMax)
        self.show_total = show_total
        self.orderBy = orderBy
        self.orderDir = orderDir
        return self
