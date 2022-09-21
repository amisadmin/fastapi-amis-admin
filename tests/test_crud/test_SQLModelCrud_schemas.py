from fastapi import FastAPI
from httpx import AsyncClient
from pydantic import BaseModel

from fastapi_amis_admin.crud import SQLModelCrud
from tests.conftest import async_db as db
from tests.models import User


class UserFilter(BaseModel):
    id: int = None
    name: str = None


async def test_schema_update(app: FastAPI, async_client: AsyncClient, fake_users):
    class UserUpdate(BaseModel):
        password: str = None

    class UserCrud(SQLModelCrud):
        router_prefix = "/user"
        schema_update = UserUpdate

    ins = UserCrud(User, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    openapi = app.openapi()
    schemas = openapi["components"]["schemas"]
    assert "password" in schemas["UserUpdate"]["properties"]
    assert "username" not in schemas["UserUpdate"]["properties"]

    # test api
    res = await async_client.put("/user/item/1", json={"username": "new_name"})
    assert res.json() == {"detail": "error data handle"}
    res = await async_client.put("/user/item/1", json={"password": "new_password"})
    assert res.json()["data"] == 1


async def test_schema_create(app: FastAPI, async_client: AsyncClient):
    class UserCreate(BaseModel):
        username: str

    class UserCrud(SQLModelCrud):
        router_prefix = "/user"
        schema_create = UserCreate

    ins = UserCrud(User, db.engine).register_crud()

    app.include_router(ins.router)

    assert "username" in ins.schema_create.__fields__
    assert "password" not in ins.schema_create.__fields__

    # test schemas
    openapi = app.openapi()
    schemas = openapi["components"]["schemas"]
    assert "username" in schemas["UserCreate"]["properties"]
    assert "password" not in schemas["UserCreate"]["properties"]
    # test api
    body = {"username": "User", "password": "password"}
    res = await async_client.post("/user/item", json=body)
    data = res.json().get("data")
    assert data["id"] > 0
    assert data["username"] == "User"
    assert data["password"] == ""


async def test_schema_list(app: FastAPI, async_client: AsyncClient, fake_users):
    class UserList(BaseModel):
        id: int
        username: str

    class UserCrud(SQLModelCrud):
        router_prefix = "/user"
        schema_list = UserList

    ins = UserCrud(User, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    openapi = app.openapi()
    schemas = openapi["components"]["schemas"]
    assert "password" not in schemas["UserList"]["properties"]
    assert "username" in schemas["UserList"]["properties"]

    # test api
    res = await async_client.post("/user/list", json={"id": 1})
    items = res.json()["data"]["items"]
    assert items[0]["id"] == 1
    assert "username" in items[0]
    assert "password" not in items[0]


async def test_schema_read(app: FastAPI, async_client: AsyncClient, fake_users):
    class UserRead(BaseModel):
        id: int
        username: str

    class UserCrud(SQLModelCrud):
        router_prefix = "/user"
        schema_read = UserRead

    ins = UserCrud(User, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    openapi = app.openapi()
    schemas = openapi["components"]["schemas"]
    assert "password" not in schemas["UserRead"]["properties"]
    assert "username" in schemas["UserRead"]["properties"]

    # test api
    res = await async_client.get("/user/item/1")
    items = res.json()["data"]
    assert items["id"] == 1
    assert "username" in items
    assert "password" not in items


# todo perfect
async def test_schema_filter(app: FastAPI, async_client: AsyncClient, fake_users):
    class UserFilter(BaseModel):
        id: int = None
        username: str = None

    class UserCrud(SQLModelCrud):
        router_prefix = "/user"
        schema_filter = UserFilter

    ins = UserCrud(User, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    openapi = app.openapi()
    schemas = openapi["components"]["schemas"]
    assert "password" not in schemas["UserFilter"]["properties"]
    assert "username" in schemas["UserFilter"]["properties"]

    # test api
    res = await async_client.post("/user/list", json={"id": 1})
    items = res.json()["data"]["items"]
    assert items[0]["id"] == 1

    res = await async_client.post("/user/list", json={"username": "User_1"})
    items = res.json()["data"]["items"]
    assert items[0]["username"] == "User_1"

    res = await async_client.post("/user/list", json={"password": "new_password"})
    items = res.json()["data"]["items"]
    assert items
