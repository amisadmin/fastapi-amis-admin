from typing import List

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlmodel.sql.expression import Select
from starlette.requests import Request
from starlette.routing import NoMatchFound

from fastapi_amis_admin.crud import SQLModelCrud
from fastapi_amis_admin.crud.parser import LabelField, PropertyField
from fastapi_amis_admin.models import Field
from tests.conftest import async_db as db
from tests.models import Article, ArticleContent, Category, Tag, User


async def test_pk_name(app: FastAPI, async_client: AsyncClient, fake_users):
    class UserCrud(SQLModelCrud):
        router_prefix = "/user"
        pk_name = "username"
        read_fields = [User]

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


async def test_read_fields(app: FastAPI, async_client: AsyncClient, fake_articles):
    class ArticleCrud(SQLModelCrud):
        router_prefix = "/article"
        read_fields = [
            Article.title,
            Article.description,
            # Article.category,  # Relationship
            # Article.user  # Relationship
        ]

    ins = ArticleCrud(Article, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    assert "id" not in ins.schema_read.__fields__
    assert "title" in ins.schema_read.__fields__
    assert "description" in ins.schema_read.__fields__
    # test api
    res = await async_client.get("/article/item/1")
    items = res.json()["data"]
    assert "id" not in items
    assert items["title"] == "Article_1"
    assert items["description"] == "Description_1"


async def test_read_fields_relationship(app: FastAPI, async_client: AsyncClient, fake_articles, fake_article_tags):
    class ArticleCrud(SQLModelCrud):
        router_prefix = "/article"
        read_fields = [
            Article.title,
            Article.description,
            PropertyField(name="category", type_=Category),  # Relationship attribute
            # Article.category,  # Relationship todo support
            PropertyField(name="content_text", type_=str),  # property attribute
            PropertyField(name="tags", type_=List[Tag]),  # property attribute
        ]

    ins = ArticleCrud(Article, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    assert "id" not in ins.schema_read.__fields__
    assert "title" in ins.schema_read.__fields__
    assert "description" in ins.schema_read.__fields__
    assert "category" in ins.schema_read.__fields__
    assert "tags" in ins.schema_read.__fields__
    # test api
    res = await async_client.get("/article/item/1")
    items = res.json()["data"]
    assert "id" not in items
    assert "category" in items
    assert items["category"]["name"] == "Category_1"
    assert "content_text" in items
    assert items["tags"][0]["name"] == "Tag_1"


async def test_update_fields_relationship(app: FastAPI, async_client: AsyncClient, fake_articles, async_session):
    class ArticleCrud(SQLModelCrud):
        router_prefix = "/article"
        update_exclude = {"content": {"id"}}
        update_fields = [
            Article.description,
            PropertyField(name="content", type_=ArticleContent),  # Relationship attribute
        ]

    ins = ArticleCrud(Article, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    assert "id" not in ins.schema_update.__fields__
    assert "title" not in ins.schema_update.__fields__
    assert "description" in ins.schema_update.__fields__
    assert "content" in ins.schema_update.__fields__

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
    article = await async_session.get(Article, 1)
    assert article.title != "new_title"
    assert article.description == "new_description"

    content = await async_session.get(ArticleContent, 1)
    assert content.content == "new_content"


async def test_read_fields_and_schema_read_is_none(app: FastAPI, async_client: FastAPI):
    class ArticleCrud(SQLModelCrud):
        router_prefix = "/article"

    ins = ArticleCrud(Article, db.engine).register_crud()

    app.include_router(ins.router)
    assert ins.schema_read is None

    with pytest.raises(NoMatchFound):
        ins.router.url_path_for(name="read")

    # test schemas
    openapi = app.openapi()
    paths = openapi["paths"]
    assert "/article/list" in paths
    assert "/article/item/{item_id}" in paths
    assert "put" in paths["/article/item/{item_id}"]
    assert "get" not in paths["/article/item/{item_id}"]
