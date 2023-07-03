import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import func, select

from fastapi_amis_admin.crud import SqlalchemyCrud
from fastapi_amis_admin.crud.parser import TableModelParser
from tests.conftest import async_db as db


@pytest.fixture(autouse=True)
def app_routes(app: FastAPI, models):
    user_schema = TableModelParser.get_table_model_schema(models.User)
    user_crud = SqlalchemyCrud(models.User, db.engine).register_crud(schema_read=user_schema)

    app.include_router(user_crud.router)

    tag_crud = SqlalchemyCrud(models.Tag, db.engine).register_crud()

    app.include_router(tag_crud.router)


async def test_register_crud(async_client: AsyncClient):
    response = await async_client.get("/openapi.json")
    # test paths
    paths = response.json()["paths"]
    assert "/User/list" in paths
    assert "/User/item" in paths
    assert "/User/item/{item_id}" in paths
    assert "/Tag/list" in paths
    assert "/Tag/item" in paths
    assert "/Tag/item/{item_id}" in paths

    # test schemas
    schemas = response.json()["components"]["schemas"]
    # assert "UserSchema" in schemas
    assert "UserFilter" in schemas
    assert "UserList" in schemas
    assert "UserUpdate" in schemas
    assert "ItemListSchema_UserList_" in schemas
    assert "TagFilter" in schemas
    assert "TagList" in schemas
    assert "TagUpdate" in schemas


async def test_route_create(async_client: AsyncClient, models):
    # create one
    body = {"username": "User", "password": "password"}
    res = await async_client.post("/User/item", json=body)
    data = res.json().get("data")
    assert data["id"] > 0
    assert data["username"] == "User"
    user = await db.session.get(models.User, data["id"])
    assert user.id == data["id"], user
    await db.session.delete(user)
    # await db.session.flush()  # If flush is used here, the sqlite database is locked, causing subsequent tests to fail
    await db.session.commit()  # Commit transaction, delete data

    # create bulk
    count = 3
    users = [
        {
            "id": i,
            "username": f"User_{i}",
            "password": "password",
            "create_time": f"2022-01-0{i + 1} 00:00:00",
            "address": ["address_1", "address_2"],
            "attach": {"attach_1": "attach_1", "attach_2": "attach_2"},
        }
        for i in range(1, count + 1)
    ]
    res = await async_client.post("/User/item", json=users)
    assert res.json()["data"] == count
    stmt = select(func.count(models.User.id))
    result = await db.scalar(stmt)
    assert result == count


async def test_route_read(async_client: AsyncClient, fake_users):
    # read one
    res = await async_client.get("/User/item/1")
    user = res.json()["data"]
    assert user["id"] == 1
    assert user["username"] == "User_1"
    assert user["address"] == ["address_1", "address_2"]
    assert user["attach"] == {"attach_1": "attach_1", "attach_2": "attach_2"}
    # read bulk
    res = await async_client.get("/User/item/1,2,4")
    users = res.json()["data"]
    assert len(users) == 3
    assert users[0]["username"] == "User_1"
    assert users[2]["username"] == "User_4"
    assert users[0]["address"] == ["address_1", "address_2"]
    assert users[2]["address"] == ["address_1", "address_2"]


async def test_route_update(async_client: AsyncClient, fake_users, models):
    # update one
    res = await async_client.put(
        "/User/item/1",
        json={
            "username": "new_name",
            "address": ["address_3"],
            "attach": {"attach_3": "attach_3"},
        },
    )
    count = res.json()["data"]
    assert count == 1
    user = await db.session.get(models.User, 1)
    assert user.username == "new_name"
    assert user.address == ["address_3"]
    assert user.attach == {"attach_3": "attach_3"}
    # update bulk
    res = await async_client.put(
        "/User/item/1,2,4",
        json={
            "password": "new_password",
            "address": ["address_3"],
            "attach": {"attach_3": "attach_3"},
        },
    )
    count = res.json()["data"]
    assert count == 3
    db.session.expire_all()
    for user in await db.session.scalars(select(models.User).where(models.User.id.in_([1, 2, 4]))):
        assert user.password == "new_password"
        assert user.address == ["address_3"]
        assert user.attach == {"attach_3": "attach_3"}


async def test_route_delete(async_client: AsyncClient, fake_users, models):
    # delete one
    res = await async_client.delete("/User/item/1")
    count = res.json()["data"]
    assert count == 1
    user = await db.get(models.User, 1)
    assert user is None
    # delete bulk
    res = await async_client.delete("/User/item/2,4")
    count = res.json()["data"]
    assert count == 2
    assert await db.get(models.User, 2) is None
    assert await db.get(models.User, 4) is None


async def test_route_list(async_client: AsyncClient, fake_users):
    # list
    res = await async_client.post("/User/list")
    items = res.json()["data"]["items"]
    assert len(items) == 5

    res = await async_client.post("/User/list", json={"id": 1})
    items = res.json()["data"]["items"]
    assert items[0]["id"] == 1
    assert items[0]["username"] == "User_1"
    assert items[0]["address"] == ["address_1", "address_2"]
    assert items[0]["attach"] == {"attach_1": "attach_1", "attach_2": "attach_2"}

    res = await async_client.post("/User/list", json={"username": "User_1"})
    items = res.json()["data"]["items"]
    assert items[0]["username"] == "User_1"

    res = await async_client.post("/User/list", json={"id": "[>]1"})
    assert len(res.json()["data"]["items"]) == 4

    res = await async_client.post("/User/list", json={"id": "[*]1,3"})
    assert len(res.json()["data"]["items"]) == 2

    res = await async_client.post("/User/list", json={"id": "[-]2,3"})
    assert len(res.json()["data"]["items"]) == 2

    res = await async_client.post("/User/list", json={"username": "[~]User_%"})
    assert len(res.json()["data"]["items"]) == 5

    res = await async_client.post("/User/list", json={"create_time": "[-]2022-01-02 00:00:00,2022-01-04 01:00:00"})
    assert len(res.json()["data"]["items"]) == 3
