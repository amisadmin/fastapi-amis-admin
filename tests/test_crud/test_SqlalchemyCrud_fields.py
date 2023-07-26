from typing import List

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from pydantic import Field
from sqlalchemy.sql import Select
from starlette.requests import Request
from starlette.routing import NoMatchFound

from fastapi_amis_admin.crud import SqlalchemyCrud
from fastapi_amis_admin.crud.parser import LabelField, PropertyField
from fastapi_amis_admin.utils.pydantic import model_fields
from tests.conftest import async_db as db
from tests.models.schemas import ArticleContentSchema, CategorySchema, TagSchema


async def test_pk_name(app: FastAPI, async_client: AsyncClient, fake_users, models):
    class UserCrud(SqlalchemyCrud):
        router_prefix = "/user"
        pk_name = "username"
        read_fields = [models.User.id, models.User.username, models.User.password]

    ins = UserCrud(models.User, db.engine).register_crud()

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


async def test_update_exclude(app: FastAPI, async_client: AsyncClient, fake_users, models):
    class UserCrud(SqlalchemyCrud):
        router_prefix = "/user"
        update_exclude = {"username"}

    ins = UserCrud(models.User, db.engine).register_crud()

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


async def test_update_fields(app: FastAPI, async_client: AsyncClient, fake_users, models):
    class UserCrud(SqlalchemyCrud):
        router_prefix = "/user"
        update_fields = [models.User.username]

    ins = UserCrud(models.User, db.engine).register_crud()

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


async def test_list_filter(app: FastAPI, async_client: AsyncClient, fake_users, models):
    class UserCrud(SqlalchemyCrud):
        router_prefix = "/user"
        list_filter = [models.User.id, models.User.username]

    ins = UserCrud(models.User, db.engine).register_crud()

    app.include_router(ins.router)

    assert "username" in model_fields(ins.schema_filter)
    assert "password" not in model_fields(ins.schema_filter)

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


async def test_create_fields(app: FastAPI, async_client: AsyncClient, models):
    class UserCrud(SqlalchemyCrud):
        router_prefix = "/user"
        create_fields = [models.User.username]

    ins = UserCrud(models.User, db.engine).register_crud()

    app.include_router(ins.router)

    assert "username" in model_fields(ins.schema_create)
    assert "password" not in model_fields(ins.schema_create)

    # test schemas
    openapi = app.openapi()
    schemas = openapi["components"]["schemas"]
    assert "username" in schemas["UserCrudCreate"]["properties"]
    assert "password" not in schemas["UserCrudCreate"]["properties"]
    # test api
    body = {"username": "User", "password": "password", "address": [], "attach": {}}
    res = await async_client.post("/user/item", json=body)
    data = res.json().get("data")
    assert data["id"] > 0
    assert data["username"] == "User"
    assert data["password"] == ""


async def test_list_filter_relationship(app: FastAPI, async_client: AsyncClient, fake_articles, models):
    class ArticleCrud(SqlalchemyCrud):
        router_prefix = "/article"
        list_filter = [
            "id",
            models.Article.title,
            models.User.username,
            models.User.password.label("pwd"),
            LabelField(
                label=models.User.password.label("pwd2"),
                field=Field(None, title="pwd_title"),
            ),
        ]

        async def get_select(self, request: Request) -> Select:
            sel = await super().get_select(request)
            return sel.outerjoin(models.User, models.User.id == models.Article.user_id)

    ins = ArticleCrud(models.Article, db.engine).register_crud()

    app.include_router(ins.router)
    # test schemas
    assert "title" in model_fields(ins.schema_filter)
    assert "user_username" in model_fields(ins.schema_filter)
    assert "pwd" in model_fields(ins.schema_filter)
    assert "pwd2" in model_fields(ins.schema_filter)
    assert model_fields(ins.schema_filter)["pwd2"].field_info.title == "pwd_title"
    assert "description" not in model_fields(ins.schema_filter)
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


async def test_fields(app: FastAPI, async_client: AsyncClient, fake_articles, models):
    class ArticleCrud(SqlalchemyCrud):
        router_prefix = "/article"
        fields = [
            models.Article.title,
            models.User.username,
            models.User.password.label("pwd"),
            "not_exist",
            LabelField(
                label=models.User.password.label("pwd2"),
                field=Field(None, title="pwd_title"),
            ),
        ]

        async def get_select(self, request: Request) -> Select:
            sel = await super().get_select(request)
            return sel.outerjoin(models.User, models.User.id == models.Article.user_id)

    ins = ArticleCrud(models.Article, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    assert "id" in model_fields(ins.schema_list)
    assert "title" in model_fields(ins.schema_list)
    assert "user_username" in model_fields(ins.schema_list)
    assert "pwd" in model_fields(ins.schema_list)
    assert "pwd2" in model_fields(ins.schema_list)
    assert "description" not in model_fields(ins.schema_list)
    # test schema_filter
    assert "title" in model_fields(ins.schema_filter)
    assert "user_username" in model_fields(ins.schema_filter)
    assert "pwd" in model_fields(ins.schema_filter)
    assert "pwd2" in model_fields(ins.schema_filter)
    assert model_fields(ins.schema_filter)["pwd2"].field_info.title == "pwd_title"
    assert "description" not in model_fields(ins.schema_filter)
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


async def test_read_fields(app: FastAPI, async_client: AsyncClient, fake_articles, models):
    class ArticleCrud(SqlalchemyCrud):
        router_prefix = "/article"
        read_fields = [
            models.Article.title,
            models.Article.description,
            # Article.category,  # Relationship
            # Article.user  # Relationship
        ]

    ins = ArticleCrud(models.Article, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    assert "id" not in model_fields(ins.schema_read)
    assert "title" in model_fields(ins.schema_read)
    assert "description" in model_fields(ins.schema_read)
    # test api
    res = await async_client.get("/article/item/1")
    items = res.json()["data"]
    assert "id" not in items
    assert items["title"] == "Article_1"
    assert items["description"] == "Description_1"


async def test_read_fields_relationship(app: FastAPI, async_client: AsyncClient, fake_articles, fake_article_tags, models):
    class ArticleCrud(SqlalchemyCrud):
        router_prefix = "/article"
        read_fields = [
            models.Article.title,
            models.Article.description,
            PropertyField(name="category", type_=CategorySchema),  # Relationship attribute
            # Article.category,  # Relationship todo support
            PropertyField(name="content_text", type_=str),  # property attribute
            PropertyField(name="tags", type_=List[TagSchema]),  # property attribute
        ]

    ins = ArticleCrud(models.Article, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    assert "id" not in model_fields(ins.schema_read)
    assert "title" in model_fields(ins.schema_read)
    assert "description" in model_fields(ins.schema_read)
    assert "category" in model_fields(ins.schema_read)
    assert "tags" in model_fields(ins.schema_read)
    # test api
    res = await async_client.get("/article/item/1")
    items = res.json()["data"]
    assert "id" not in items
    assert "category" in items
    assert items["category"]["name"] == "Category_1"
    assert "content_text" in items
    assert items["tags"][0]["name"] == "Tag_1"


async def test_update_fields_relationship(app: FastAPI, async_client: AsyncClient, fake_articles, async_session, models):
    class ArticleCrud(SqlalchemyCrud):
        router_prefix = "/article"
        update_exclude = {"content": {"id"}}
        update_fields = [
            models.Article.description,
            PropertyField(name="content", type_=ArticleContentSchema),  # Relationship attribute
        ]
        read_fields = [
            models.Article.title,
            models.Article.description,
            PropertyField(name="content", type_=ArticleContentSchema),  # Relationship attribute
        ]

    ins = ArticleCrud(models.Article, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    assert "id" not in model_fields(ins.schema_update)
    assert "title" not in model_fields(ins.schema_update)
    assert "description" in model_fields(ins.schema_update)
    assert "content" in model_fields(ins.schema_update)

    # test api
    res = await async_client.put(
        "/article/item/1",
        json={
            "title": "new_title",
            "description": "new_description",
            "content": {
                "id": 22,  # will be ignored by `update_exclude`
                "content": "new_content",
            },
        },
    )
    assert res.json()["data"] == 1

    article = await async_session.get(models.Article, 1)
    await async_session.refresh(article)

    assert article.title != "new_title"
    assert article.description == "new_description"

    content = await async_session.get(models.ArticleContent, 1)
    await async_session.refresh(content)
    assert content.content == "new_content"


async def test_read_fields_and_schema_read_is_none(app: FastAPI, models):
    class ArticleCrud(SqlalchemyCrud):
        router_prefix = "/article"

    ins = ArticleCrud(models.Article, db.engine).register_crud()

    app.include_router(ins.router)
    assert ins.schema_read is None

    with pytest.raises(NoMatchFound):
        ins.router.url_path_for("read")

    # test schemas
    openapi = app.openapi()
    paths = openapi["paths"]
    assert "/article/list" in paths
    assert "/article/item/{item_id}" in paths
    assert "put" in paths["/article/item/{item_id}"]
    assert "get" not in paths["/article/item/{item_id}"]
