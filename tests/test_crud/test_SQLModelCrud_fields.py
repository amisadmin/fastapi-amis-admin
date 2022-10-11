from fastapi import FastAPI
from httpx import AsyncClient
from sqlmodel.sql.expression import Select
from starlette.requests import Request

from fastapi_amis_admin.crud import SQLModelCrud
from fastapi_amis_admin.crud.parser import LabelField
from fastapi_amis_admin.models import Field
from tests.conftest import async_db as db
from tests.models import Article, User


async def test_pk_name(app: FastAPI, async_client: AsyncClient, fake_users):
    class UserCrud(SQLModelCrud):
        router_prefix = "/user"
        pk_name = "username"

    ins = UserCrud(User, db.engine).register_crud()

    app.include_router(ins.router)
    assert ins.pk.key == "username"
    # read one
    res = await async_client.get("/user/item/User_1")
    user = res.json()["data"]
    assert user["id"] == 1
    assert user["username"] == "User_1"
    # read bulk
    res = await async_client.get("/user/item/User_1,User_2,User_4")
    users = res.json()["data"]
    assert len(users) == 3
    assert users[0]["username"] == "User_1"
    assert users[2]["username"] == "User_4"


async def test_readonly_fields(app: FastAPI, async_client: AsyncClient, fake_users):
    class UserCrud(SQLModelCrud):
        router_prefix = "/user"
        readonly_fields = [User.username]

    ins = UserCrud(User, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    openapi = app.openapi()
    schemas = openapi["components"]["schemas"]
    assert "password" in schemas["UserCrudUpdate"]["properties"]
    assert "username" not in schemas["UserCrudUpdate"]["properties"]

    # test api
    res = await async_client.put("/user/item/1", json={"username": "new_name"})
    assert res.json() == {"detail": "error data handle"}
    res = await async_client.put("/user/item/1", json={"password": "new_password"})
    assert res.json()["data"] == 1


async def test_update_fields(app: FastAPI, async_client: AsyncClient, fake_users):
    class UserCrud(SQLModelCrud):
        router_prefix = "/user"
        update_fields = [User.username]

    ins = UserCrud(User, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    openapi = app.openapi()
    schemas = openapi["components"]["schemas"]
    assert "password" not in schemas["UserCrudUpdate"]["properties"]
    assert "username" in schemas["UserCrudUpdate"]["properties"]

    # test api
    res = await async_client.put("/user/item/1", json={"username": "new_name"})
    assert res.json()["data"] == 1

    res = await async_client.put("/user/item/1", json={"password": "new_password"})
    assert res.json() == {"detail": "error data handle"}


async def test_list_filter(app: FastAPI, async_client: AsyncClient, fake_users):
    class UserCrud(SQLModelCrud):
        router_prefix = "/user"
        list_filter = [User.id, User.username]

    ins = UserCrud(User, db.engine).register_crud()

    app.include_router(ins.router)

    assert "username" in ins.schema_filter.__fields__
    assert "password" not in ins.schema_filter.__fields__

    # test schemas
    openapi = app.openapi()
    schemas = openapi["components"]["schemas"]
    assert "username" in schemas["UserCrudFilter"]["properties"]
    assert "password" not in schemas["UserCrudFilter"]["properties"]

    # test api
    res = await async_client.post("/user/list", json={"id": 2})
    items = res.json()["data"]["items"]
    assert items[0]["id"] == 2

    res = await async_client.post("/user/list", json={"username": "User_2"})
    items = res.json()["data"]["items"]
    assert items[0]["username"] == "User_2"

    res = await async_client.post("/user/list", json={"password": "new_password"})
    items = res.json()["data"]["items"]
    assert items


async def test_create_fields(app: FastAPI, async_client: AsyncClient):
    class UserCrud(SQLModelCrud):
        router_prefix = "/user"
        create_fields = [User.username]

    ins = UserCrud(User, db.engine).register_crud()

    app.include_router(ins.router)

    assert "username" in ins.schema_create.__fields__
    assert "password" not in ins.schema_create.__fields__

    # test schemas
    openapi = app.openapi()
    schemas = openapi["components"]["schemas"]
    assert "username" in schemas["UserCrudCreate"]["properties"]
    assert "password" not in schemas["UserCrudCreate"]["properties"]
    # test api
    body = {"username": "User", "password": "password"}
    res = await async_client.post("/user/item", json=body)
    data = res.json().get("data")
    assert data["id"] > 0
    assert data["username"] == "User"
    assert data["password"] == ""


async def test_list_filter_relationship(app: FastAPI, async_client: AsyncClient, fake_articles):
    class ArticleCrud(SQLModelCrud):
        router_prefix = "/article"
        list_filter = [
            "id",
            Article.title,
            User.username,
            User.password.label("pwd"),
            LabelField(
                label=User.password.label("pwd2"),
                field=Field(None, title="pwd_title"),
            ),
        ]

        async def get_select(self, request: Request) -> Select:
            sel = await super().get_select(request)
            return sel.outerjoin(User, User.id == Article.user_id)

    ins = ArticleCrud(Article, db.engine).register_crud()

    app.include_router(ins.router)
    # test schemas
    assert "title" in ins.schema_filter.__fields__
    assert "user_username" in ins.schema_filter.__fields__
    assert "pwd" in ins.schema_filter.__fields__
    assert "pwd2" in ins.schema_filter.__fields__
    assert ins.schema_filter.__fields__["pwd2"].field_info.title == "pwd_title"
    assert "description" not in ins.schema_filter.__fields__
    # test openapi
    openapi = app.openapi()
    schemas = openapi["components"]["schemas"]

    assert "title" in schemas["ArticleCrudFilter"]["properties"]
    assert "user__username" in schemas["ArticleCrudFilter"]["properties"]
    assert "pwd" in schemas["ArticleCrudFilter"]["properties"]
    assert "description" not in schemas["ArticleCrudFilter"]["properties"]

    # test api
    res = await async_client.post("/article/list", json={"id": 2})
    items = res.json()["data"]["items"]
    assert items[0]["id"] == 2
    assert "user__username" not in items[0]
    assert "pwd" not in items[0]

    res = await async_client.post("/article/list", json={"user__username": "User_2"})
    items = res.json()["data"]["items"]
    assert items[0]["id"] == 2

    res = await async_client.post("/article/list", json={"pwd": "password_2"})
    items = res.json()["data"]["items"]
    assert items[0]["id"] == 2

    res = await async_client.post("/article/list", json={"pwd2": "password_2"})
    items = res.json()["data"]["items"]
    assert items[0]["id"] == 2


async def test_fields(app: FastAPI, async_client: AsyncClient, fake_articles):
    class ArticleCrud(SQLModelCrud):
        router_prefix = "/article"
        fields = [
            Article.title,
            User.username,
            User.password.label("pwd"),
            "not_exist",
            LabelField(
                label=User.password.label("pwd2"),
                field=Field(None, title="pwd_title"),
            ),
        ]

        async def get_select(self, request: Request) -> Select:
            sel = await super().get_select(request)
            return sel.outerjoin(User, User.id == Article.user_id)

    ins = ArticleCrud(Article, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    assert "id" in ins.schema_list.__fields__
    assert "title" in ins.schema_list.__fields__
    assert "user_username" in ins.schema_list.__fields__
    assert "pwd" in ins.schema_list.__fields__
    assert "pwd2" in ins.schema_list.__fields__
    assert "description" not in ins.schema_list.__fields__
    # test schema_filter
    assert "title" in ins.schema_filter.__fields__
    assert "user_username" in ins.schema_filter.__fields__
    assert "pwd" in ins.schema_filter.__fields__
    assert "pwd2" in ins.schema_filter.__fields__
    assert ins.schema_filter.__fields__["pwd2"].field_info.title == "pwd_title"
    assert "description" not in ins.schema_filter.__fields__
    # test openapi
    openapi = app.openapi()
    schemas = openapi["components"]["schemas"]

    assert "title" in schemas["ArticleCrudFilter"]["properties"]
    assert "user__username" in schemas["ArticleCrudFilter"]["properties"]
    assert "pwd" in schemas["ArticleCrudFilter"]["properties"]
    assert "pwd2" in schemas["ArticleCrudFilter"]["properties"]
    assert "description" not in schemas["ArticleCrudFilter"]["properties"]

    # test api
    res = await async_client.post("/article/list", json={"id": 2})
    items = res.json()["data"]["items"]
    assert items[0]["id"] == 2
    assert items[0]["user__username"] == "User_2"
    assert items[0]["pwd"] == "password_2"
