from typing import List, Optional

from fastapi import FastAPI
from httpx import AsyncClient
from pydantic import BaseModel

from fastapi_amis_admin.crud import SqlalchemyCrud
from fastapi_amis_admin.crud.parser import TableModelParser
from fastapi_amis_admin.utils.pydantic import ORMModelMixin, model_fields
from tests.conftest import async_db as db


async def test_schema_update(app: FastAPI, async_client: AsyncClient, fake_users, models):
    class UserUpdate(BaseModel):
        password: str = None

    class UserCrud(SqlalchemyCrud):
        router_prefix = "/user"
        schema_update = UserUpdate

    ins = UserCrud(models.User, db.engine).register_crud()

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


async def test_schema_create(app: FastAPI, async_client: AsyncClient, models):
    class UserCreate(BaseModel):
        username: str

    class UserCrud(SqlalchemyCrud):
        router_prefix = "/user"
        schema_create = UserCreate

    ins = UserCrud(models.User, db.engine).register_crud()

    app.include_router(ins.router)

    assert "username" in model_fields(ins.schema_create)
    assert "password" not in model_fields(ins.schema_create)

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


async def test_schema_list(app: FastAPI, async_client: AsyncClient, fake_users, models):
    class UserList(BaseModel):
        id: int
        username: str

    class UserCrud(SqlalchemyCrud):
        router_prefix = "/user"
        schema_list = UserList

    ins = UserCrud(models.User, db.engine).register_crud()

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


async def test_schema_read(app: FastAPI, async_client: AsyncClient, fake_users, models):
    class UserRead(ORMModelMixin):
        id: int
        username: str

    class UserCrud(SqlalchemyCrud):
        router_prefix = "/user"
        schema_read = UserRead

    ins = UserCrud(models.User, db.engine).register_crud()

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
async def test_schema_filter(app: FastAPI, async_client: AsyncClient, fake_users, models):
    class UserFilter(BaseModel):
        id: int = None
        username: str = None

    class UserCrud(SqlalchemyCrud):
        router_prefix = "/user"
        schema_filter = UserFilter

    ins = UserCrud(models.User, db.engine).register_crud()

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


async def test_schema_read_relationship(app: FastAPI, async_client: AsyncClient, fake_articles, fake_article_tags, models):
    category_schema = TableModelParser.get_table_model_schema(models.Category)
    content_schema = TableModelParser.get_table_model_schema(models.ArticleContent)
    user_schema = TableModelParser.get_table_model_schema(models.User)
    tag_schema = TableModelParser.get_table_model_schema(models.Tag)

    class ArticleRead(ORMModelMixin):
        id: int
        title: str
        description: str
        category: Optional[category_schema] = None  # Relationship
        content: Optional[content_schema] = None  # Relationship
        user: Optional[user_schema] = None  # Relationship
        tags: List[tag_schema] = []  # Relationship

    class ArticleCrud(SqlalchemyCrud):
        router_prefix = "/article"
        schema_read = ArticleRead

    ins = ArticleCrud(models.Article, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    openapi = app.openapi()
    schemas = openapi["components"]["schemas"]
    assert "category" in schemas["ArticleRead"]["properties"]
    # assert schemas["ArticleRead"]["properties"]["category"]["$ref"] == "#/components/schemas/" + category_schema.__name__
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


async def test_schema_update_relationship(app: FastAPI, async_client: AsyncClient, fake_articles, async_session, models):
    content_schema = TableModelParser.get_table_model_schema(models.ArticleContent)

    class ArticleUpdate(BaseModel):
        title: str = None
        description: str = None
        content: Optional[content_schema] = None  # Relationship

    class ArticleCrud(SqlalchemyCrud):
        router_prefix = "/article"
        update_exclude = {"content": {"id"}}
        schema_update = ArticleUpdate

    ins = ArticleCrud(models.Article, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    openapi = app.openapi()
    schemas = openapi["components"]["schemas"]

    assert "content" in schemas["ArticleUpdate"]["properties"]
    # assert schemas["ArticleUpdate"]["properties"]["content"]["$ref"] == "#/components/schemas/" + content_schema.__name__

    # test api
    res = await async_client.put("/article/item/1", json={"title": "new_title"})
    assert res.json()["data"] == 1
    article = await async_session.get(models.Article, 1, with_for_update=True)
    await async_session.refresh(article)
    assert article.title == "new_title"

    res = await async_client.put(
        "/article/item/1",
        json={"content": {"id": 2, "content": "new_content"}},  # will be ignored by `update_exclude`
    )
    assert res.json()["data"] == 1
    content = await async_session.get(models.ArticleContent, 1, with_for_update=True)
    await async_session.refresh(content)
    assert content.content == "new_content"
