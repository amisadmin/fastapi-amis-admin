import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import func, select

from fastapi_amis_admin.crud import SQLModelCrud
from tests.conftest import async_db as db
from tests.models import Tag, User


@pytest.fixture(autouse=True)
def app_routes(app: FastAPI):
    user_crud = SQLModelCrud(User, db.engine).register_crud()

    app.include_router(user_crud.router)

    tag_crud = SQLModelCrud(Tag, db.engine).register_crud()

    app.include_router(tag_crud.router)


async def test_register_crud(async_client: AsyncClient):
    response = await async_client.get("/openapi.json")
    # test paths
    paths = response.json()["paths"]
    assert "/user/list" in paths
    assert "/user/item" in paths
    assert "/user/item/{item_id}" in paths
    assert "/tag/list" in paths
    assert "/tag/item" in paths
    assert "/tag/item/{item_id}" in paths

    # test schemas
    schemas = response.json()["components"]["schemas"]
    assert "User" in schemas
    assert "UserFilter" in schemas
    assert "UserList" in schemas
    assert "UserUpdate" in schemas
    assert "ItemListSchema_UserList_" in schemas
    assert "TagFilter" in schemas
    assert "TagList" in schemas
    assert "TagUpdate" in schemas


async def test_route_create(async_client: AsyncClient):
    # create one
    body = {"username": "User", "password": "password"}
    res = await async_client.post("/user/item", json=body)
    data = res.json().get("data")
    assert data["id"] > 0
    assert data["username"] == "User"
    result = await db.get(User, data["id"])
    assert result.id == data["id"], result
    await db.delete(result)
    # create bulk
    count = 3
    users = [
        {
            "id": i,
            "username": f"User_{i}",
            "password": "password",
            "create_time": f"2022-01-0{i + 1} 00:00:00",
        }
        for i in range(1, count + 1)
    ]
    res = await async_client.post("/user/item", json=users)
    assert res.json()["data"] == count
    stmt = select(func.count(User.id))
    result = await db.scalar(stmt)
    assert result == count


async def test_route_read(async_client: AsyncClient, fake_users):
    # read one
    res = await async_client.get("/user/item/1")
    user = res.json()["data"]
    assert user["id"] == 1
    assert user["username"] == "User_1"
    # read bulk
    res = await async_client.get("/user/item/1,2,4")
    users = res.json()["data"]
    assert len(users) == 3
    assert users[0]["username"] == "User_1"
    assert users[2]["username"] == "User_4"


async def test_route_update(async_client: AsyncClient, fake_users):
    # update one
    res = await async_client.put("/user/item/1", json={"username": "new_name"})
    count = res.json()["data"]
    assert count == 1
    user = await db.get(User, 1)
    assert user.username == "new_name"
    # update bulk
    res = await async_client.put("/user/item/1,2,4", json={"password": "new_password"})
    count = res.json()["data"]
    assert count == 3
    for user in await db.scalars_all(select(User).where(User.id.in_([1, 2, 4]))):
        assert user.password == "new_password"


async def test_route_delete(async_client: AsyncClient, fake_users):
    # delete one
    res = await async_client.delete("/user/item/1")
    count = res.json()["data"]
    assert count == 1
    user = await db.get(User, 1)
    assert user is None
    # delete bulk
    res = await async_client.delete("/user/item/2,4")
    count = res.json()["data"]
    assert count == 2
    assert await db.get(User, 2) is None
    assert await db.get(User, 4) is None


async def test_route_list(async_client: AsyncClient, fake_users):
    # list
    res = await async_client.post("/user/list")
    items = res.json()["data"]["items"]
    assert len(items) == 5

    res = await async_client.post("/user/list", json={"id": 1})
    items = res.json()["data"]["items"]
    assert items[0]["id"] == 1

    res = await async_client.post("/user/list", json={"username": "User_1"})
    items = res.json()["data"]["items"]
    assert items[0]["username"] == "User_1"

    res = await async_client.post("/user/list", json={"id": "[>]1"})
    assert len(res.json()["data"]["items"]) == 4

    res = await async_client.post("/user/list", json={"id": "[*]1,3"})
    assert len(res.json()["data"]["items"]) == 2

    res = await async_client.post("/user/list", json={"id": "[-]2,3"})
    assert len(res.json()["data"]["items"]) == 2

    res = await async_client.post("/user/list", json={"username": "[~]User_%"})
    assert len(res.json()["data"]["items"]) == 5

    res = await async_client.post("/user/list", json={"create_time": "[-]2022-01-02 00:00:00,2022-01-04 01:00:00"})
    assert len(res.json()["data"]["items"]) == 3
