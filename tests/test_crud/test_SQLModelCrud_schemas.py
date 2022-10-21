from typing import List, Optional

from fastapi import FastAPI
from httpx import AsyncClient
from pydantic import BaseModel
from sqlmodel import SQLModel

from fastapi_amis_admin.crud import SQLModelCrud
from tests.conftest import async_db as db
from tests.models import Article, ArticleContent, Category, Tag, User


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


# todo perfect;test more comparison operators
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


async def test_schema_read_relationship(app: FastAPI, async_client: AsyncClient, fake_articles, fake_article_tags):
    class ArticleRead(SQLModel):  # must be SQLModel, not BaseModel
        id: int
        title: str
        description: str
        category: Optional[Category] = None  # Relationship
        content: Optional[ArticleContent] = None  # Relationship
        user: Optional[User] = None  # Relationship
        tags: List[Tag] = []  # Relationship

    class ArticleCrud(SQLModelCrud):
        router_prefix = "/article"
        schema_read = ArticleRead

    ins = ArticleCrud(Article, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    openapi = app.openapi()
    schemas = openapi["components"]["schemas"]
    assert "category" in schemas["ArticleRead"]["properties"]
    assert schemas["ArticleRead"]["properties"]["category"]["$ref"] == "#/components/schemas/Category"
    assert "content" in schemas["ArticleRead"]["properties"]
    assert "user" in schemas["ArticleRead"]["properties"]
    assert "tags" in schemas["ArticleRead"]["properties"]

    # test api
    res = await async_client.get("/article/item/1")
    items = res.json()["data"]
    assert items["id"] == 1
    assert "category" in items
    assert "content" in items
    assert "user" in items
    assert items["category"]["id"] == 1
    assert items["content"]["id"] == 1
    assert items["user"]["id"] == 1
    assert items["tags"][0]["id"] == 1


async def test_schema_update_relationship(app: FastAPI, async_client: AsyncClient, fake_articles, async_session):
    class ArticleUpdate(SQLModel):  # must be SQLModel, not BaseModel
        title: str = None
        description: str = None
        content: Optional[ArticleContent] = None  # Relationship

    class ArticleCrud(SQLModelCrud):
        router_prefix = "/article"
        update_exclude = {"content": {"id"}}
        schema_update = ArticleUpdate

    ins = ArticleCrud(Article, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    openapi = app.openapi()
    schemas = openapi["components"]["schemas"]

    assert "content" in schemas["ArticleUpdate"]["properties"]
    assert schemas["ArticleUpdate"]["properties"]["content"]["$ref"] == "#/components/schemas/ArticleContent"

    # test api
    res = await async_client.put("/article/item/1", json={"title": "new_title"})
    assert res.json()["data"] == 1
    article = await async_session.get(Article, 1, with_for_update=True)
    assert article.title == "new_title"

    res = await async_client.put(
        "/article/item/1", json={"content": {"id": 2, "content": "new_content"}}  # will be ignored by `update_exclude`
    )
    assert res.json()["data"] == 1
    content = await async_session.get(ArticleContent, 1, with_for_update=True)
    assert content.content == "new_content"
