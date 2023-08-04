from enum import Enum
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from fastapi_amis_admin.utils.pydantic import AllowExtraModelMixin, GenericModel

_T = TypeVar("_T")


class BaseApiSchema(AllowExtraModelMixin):
    pass


class BaseApiOut(BaseApiSchema, GenericModel, Generic[_T]):
    status: int = 0
    msg: str = "success"
    data: Optional[_T] = None
    code: Optional[int] = None


class ItemListSchema(BaseApiSchema, GenericModel, Generic[_T]):
    """Data list query return format."""

    items: List[_T] = []  # Data list
    total: Optional[int] = None  # Data total
    query: Optional[Dict[str, Any]] = None
    filter: Optional[Dict[str, Any]] = None


class CrudEnum(str, Enum):
    list = "list"
    filter = "filter"
    create = "create"
    read = "read"
    update = "update"
    delete = "delete"


class Paginator:
    """Used for data paging when querying a data list."""

    def __init__(self, perPageMax: int = None, perPageDefault: int = 10):
        self.perPageMax = perPageMax
        self.perPageDefault = perPageDefault

    def __call__(
        self,
        page: Union[int, str] = 1,
        perPage: Union[int, str] = None,
        show_total: int = 1,
        orderBy: str = None,
        orderDir: str = "asc",
    ):
        self.page = page if page and page > 0 else self.perPageDefault
        self.perPage = perPage if perPage and perPage > 0 else self.perPageDefault
        if self.perPageMax:
            self.perPage = min(self.perPage, self.perPageMax)
        self.show_total = show_total
        self.orderBy = orderBy
        self.orderDir = orderDir
        return self
