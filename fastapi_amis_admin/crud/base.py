from typing import Any, Callable, List, Optional, Type, Union

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request

from .schema import BaseApiOut, CrudEnum, ItemListSchema, Paginator
from .utils import schema_create_by_schema


class RouterMixin:
    router: APIRouter = None
    router_prefix: Optional[str] = None
    router_permission_depend: Callable = None

    def __init__(self):
        self.router = self.get_router()

    def get_router(self) -> APIRouter:
        if self.router is None:
            if self.router_prefix is None:
                self.router_prefix = f"/{self.__class__.__name__.lower()}"
            self.router = APIRouter(prefix=self.router_prefix, tags=[self.router_prefix[1:]])
        if self.router_permission_depend is not None:
            self.router.dependencies.insert(0, Depends(self.router_permission_depend))
        return self.router

    def error_no_router_permission(self, request: Request):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No router permissions")


class BaseCrud(RouterMixin):
    schema_model: Type[BaseModel] = None
    schema_list: Type[BaseModel] = None
    schema_filter: Type[BaseModel] = None
    schema_create: Type[BaseModel] = None
    schema_read: Type[BaseModel] = None
    schema_update: Type[BaseModel] = None
    pk_name: str = "id"
    list_per_page_max: int = None

    def __init__(self, schema_model: Type[BaseModel], router: APIRouter = None):
        self.paginator = Paginator()
        self.schema_model = schema_model or self.schema_model
        assert self.schema_model, "schema_model is None"
        self.router = router
        RouterMixin.__init__(self)

    @property
    def router_prefix(self):
        return f"/{self.schema_model.__name__.lower()}"

    @property
    def schema_name_prefix(self):
        return self.__class__.__name__

    def register_crud(
        self,
        schema_list: Type[BaseModel] = None,
        schema_filter: Type[BaseModel] = None,
        schema_create: Type[BaseModel] = None,
        schema_read: Type[BaseModel] = None,
        schema_update: Type[BaseModel] = None,
        list_per_page_max: int = None,
        depends_list: List[Depends] = None,
        depends_read: List[Depends] = None,
        depends_create: List[Depends] = None,
        depends_update: List[Depends] = None,
        depends_delete: List[Depends] = None,
    ) -> "BaseCrud":
        self.schema_list = schema_list or self._create_schema_list()
        self.schema_filter = schema_filter or self._create_schema_filter()
        self.schema_create = schema_create or self._create_schema_create()
        self.schema_read = schema_read or self._create_schema_read()
        self.schema_update = schema_update or self._create_schema_update()
        self.list_per_page_max = list_per_page_max or self.list_per_page_max
        self.paginator = Paginator(perPage_max=self.list_per_page_max)
        self.router.add_api_route(
            "/list",
            self.route_list,
            methods=["POST"],
            response_model=BaseApiOut[ItemListSchema[self.schema_list]],
            dependencies=depends_list,
            name=CrudEnum.list,
        )
        self.router.add_api_route(
            "/item/{item_id}",
            self.route_read,
            methods=["GET"],
            response_model=BaseApiOut[Union[self.schema_read, List[self.schema_read]]],
            dependencies=depends_read,
            name=CrudEnum.read,
        )
        self.router.add_api_route(
            "/item",
            self.route_create,
            methods=["POST"],
            response_model=BaseApiOut[Union[int, self.schema_model]],
            dependencies=depends_create,
            name=CrudEnum.create,
        )
        self.router.add_api_route(
            "/item/{item_id}",
            self.route_update,
            methods=["PUT"],
            response_model=BaseApiOut[int],
            dependencies=depends_update,
            name=CrudEnum.update,
        )
        self.router.add_api_route(
            "/item/{item_id}",
            self.route_delete,
            methods=["DELETE"],
            response_model=BaseApiOut[int],
            dependencies=depends_delete,
            name=CrudEnum.delete,
        )
        return self

    def _create_schema_list(self):
        return self.schema_list or self.schema_model

    def _create_schema_filter(self):
        return self.schema_filter or schema_create_by_schema(self.schema_list, f"{self.schema_name_prefix}Filter", set_none=True)

    def _create_schema_read(self):
        return self.schema_read or self.schema_model

    def _create_schema_update(self):
        return self.schema_update or schema_create_by_schema(
            self.schema_model,
            f"{self.schema_name_prefix}Update",
            exclude={self.pk_name},
            set_none=True,
        )

    def _create_schema_create(self):
        return self.schema_create or schema_create_by_schema(self.schema_model, f"{self.schema_name_prefix}Create")

    @property
    def route_list(self) -> Callable[..., Any]:
        raise NotImplementedError

    @property
    def route_read(self) -> Callable[..., Any]:
        raise NotImplementedError

    @property
    def route_create(self) -> Callable[..., Any]:
        raise NotImplementedError

    @property
    def route_update(self) -> Callable[..., Any]:
        raise NotImplementedError

    @property
    def route_delete(self) -> Callable[..., Any]:
        raise NotImplementedError

    async def has_list_permission(
        self,
        request: Request,
        paginator: Optional[Paginator],
        filters: Optional[BaseModel],
        **kwargs,
    ) -> bool:
        return True

    async def has_create_permission(self, request: Request, obj: Optional[BaseModel], **kwargs) -> bool:
        return True

    async def has_read_permission(self, request: Request, item_id: Optional[List[str]], **kwargs) -> bool:
        return True

    async def has_update_permission(
        self,
        request: Request,
        item_id: Optional[List[str]],
        obj: Optional[BaseModel],
        **kwargs,
    ) -> bool:
        return True

    async def has_delete_permission(self, request: Request, item_id: Optional[List[str]], **kwargs) -> bool:
        return True

    def error_data_handle(self, request: Request):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "error data handle")

    def error_execute_sql(self, request: Request, error: Exception):
        if isinstance(error, IntegrityError):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Key already exists",
            ) from error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error Execute SQL：{error}",
        ) from error
