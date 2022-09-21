import datetime
from typing import Any, Generator, List

import pytest
from fastapi import FastAPI
from sqlalchemy import func, insert, select
from sqlmodel import SQLModel
from starlette.testclient import TestClient

from fastapi_amis_admin.crud import SQLModelCrud
from tests.conftest import sync_db as db
from tests.models import Tag, User


@pytest.fixture
def prepare_database() -> Generator[None, None, None]:
    SQLModel.metadata.create_all(db.engine)
    yield
    SQLModel.metadata.drop_all(db.engine)


@pytest.fixture
def client(app: FastAPI, prepare_database: Any) -> Generator[TestClient, None, None]:
    with TestClient(app=app, base_url="http://testserver") as c:
        yield c


@pytest.fixture
def fake_users() -> List[User]:
    data = [
        {
            "id": i,
            "username": f"User_{i}",
            "password": f"password_{i}",
            "create_time": datetime.datetime.strptime(f"2022-01-0{i} 00:00:00", "%Y-%m-%d %H:%M:%S"),
        }
        for i in range(1, 6)
    ]
    db.execute(insert(User).values(data), commit=True)
    return [User.parse_obj(item) for item in data]


@pytest.fixture(autouse=True)
def app_routes(app: FastAPI):
    user_crud = SQLModelCrud(User, db.engine).register_crud()

    app.include_router(user_crud.router)

    tag_crud = SQLModelCrud(Tag, db.engine).register_crud()

    app.include_router(tag_crud.router)


def test_register_crud(client: TestClient):
    response = client.get("/openapi.json")
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


def test_route_create(client: TestClient):
    # create one
    body = {"username": "create", "password": "password"}
    res = client.post("/user/item", json=body)
    data = res.json().get("data")
    assert data["id"] > 0
    assert data["username"] == "create"
    result = db.get(User, data["id"])
    assert result.id == data["id"], result
    db.delete(result)

    # create bulk
    count = 3
    users = [
        {
            "id": i,
            "username": f"create_{i}",
            "password": "password",
            "create_time": f"2022-01-0{i + 1} 00:00:00",
        }
        for i in range(1, count + 1)
    ]
    res = client.post("/user/item", json=users)
    assert res.json()["data"] == count
    stmt = select(func.count(User.id))
    result = db.scalar(stmt)
    assert result == count


def test_route_read(client: TestClient, fake_users):
    # read one
    res = client.get("/user/item/1")
    user = res.json()["data"]
    assert user["id"] == 1
    assert user["username"] == "User_1"
    # read bulk
    res = client.get("/user/item/1,2,4")
    users = res.json()["data"]
    assert len(users) == 3
    assert users[0]["username"] == "User_1"
    assert users[2]["username"] == "User_4"


def test_route_update(client: TestClient, fake_users):
    # update one
    res = client.put("/user/item/1", json={"username": "new_name"})
    count = res.json()["data"]
    assert count == 1
    user = db.get(User, 1)
    assert user.username == "new_name"
    # update bulk
    res = client.put("/user/item/1,2,4", json={"password": "new_password"})
    count = res.json()["data"]
    assert count == 3

    for user in db.scalars_all(select(User).where(User.id.in_([1, 2, 4]))):
        assert user.password == "new_password"


def test_route_delete(client: TestClient, fake_users):
    # delete one
    res = client.delete("/user/item/1")
    count = res.json()["data"]
    assert count == 1
    user = db.get(User, 1)
    assert user is None
    # delete bulk
    res = client.delete("/user/item/2,4")
    count = res.json()["data"]
    assert count == 2
    assert db.get(User, 2) is None
    assert db.get(User, 4) is None


def test_route_list(client: TestClient, fake_users):
    # list
    res = client.post("/user/list")
    items = res.json()["data"]["items"]
    assert len(items) == 5

    res = client.post("/user/list", json={"id": 1})
    items = res.json()["data"]["items"]
    assert items[0]["id"] == 1

    res = client.post("/user/list", json={"username": "User_1"})
    items = res.json()["data"]["items"]
    assert items[0]["username"] == "User_1"

    res = client.post("/user/list", json={"id": "[>]1"})
    assert len(res.json()["data"]["items"]) == 4

    res = client.post("/user/list", json={"id": "[*]1,3"})
    assert len(res.json()["data"]["items"]) == 2

    res = client.post("/user/list", json={"id": "[-]2,3"})
    assert len(res.json()["data"]["items"]) == 2

    res = client.post("/user/list", json={"username": "[~]User_%"})
    assert len(res.json()["data"]["items"]) == 5

    res = client.post("/user/list", json={"create_time": "[-]2022-01-02 00:00:00,2022-01-04 01:00:00"})
    assert len(res.json()["data"]["items"]) == 3
