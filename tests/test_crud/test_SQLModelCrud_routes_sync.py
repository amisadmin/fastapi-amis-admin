import datetime
from typing import Any, Generator, List

import pytest
from fastapi import FastAPI
from sqlalchemy import select, func, insert
from sqlmodel import SQLModel
from starlette.testclient import TestClient

from fastapi_amis_admin.crud import SQLModelCrud
from tests.db import sync_db as db
from tests.models import Category, Tag


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
def fake_categorys() -> List[Category]:
    data = [
        {'id': i,
         "name": f'Category_{i}',
         "description": f"description_{i}",
         "create_time": datetime.datetime.strptime(f"2022-01-0{i} 00:00:00", "%Y-%m-%d %H:%M:%S")
         } for i in range(1, 6)
    ]
    db.execute(insert(Category).values(data), commit=True)
    return [Category.parse_obj(item) for item in data]


@pytest.fixture(autouse=True)
def app_routes(app: FastAPI):
    category_crud = SQLModelCrud(Category, db.engine).register_crud()

    app.include_router(category_crud.router)

    tag_crud = SQLModelCrud(Tag, db.engine).register_crud()

    app.include_router(tag_crud.router)


def test_register_crud(client: TestClient):
    response = client.get('/openapi.json')
    # test paths
    paths = response.json()['paths']
    assert '/category/list' in paths
    assert '/category/item' in paths
    assert '/category/item/{item_id}' in paths
    assert '/tag/list' in paths
    assert '/tag/item' in paths
    assert '/tag/item/{item_id}' in paths

    # test schemas
    schemas = response.json()['components']['schemas']
    assert 'Category' in schemas
    assert 'CategoryFilter' in schemas
    assert 'CategoryList' in schemas
    assert 'CategoryUpdate' in schemas
    assert 'ItemListSchema_CategoryList_' in schemas
    assert 'TagFilter' in schemas
    assert 'TagList' in schemas
    assert 'TagUpdate' in schemas


def test_route_create(client: TestClient):
    # create one
    body = {"name": 'create', "description": "description"}
    res = client.post('/category/item', json=body)
    data = res.json().get('data')
    assert data['id'] > 0
    assert data['name'] == 'create'
    result = db.get(Category, data['id'])
    assert result.id == data['id'], result
    db.delete(result)

    # create bulk
    count = 3
    categorys = [
        {'id': i,
         "name": f'create_{i}',
         "description": "description",
         "create_time": f"2022-01-0{i + 1} 00:00:00"
         } for i in range(1, count + 1)
    ]
    res = client.post('/category/item', json=categorys)
    assert res.json()['data'] == count
    stmt = select(func.count(Category.id))
    result = db.scalar(stmt)
    assert result == count


def test_route_read(client: TestClient, fake_categorys):
    # read one
    res = client.get('/category/item/1')
    category = res.json()['data']
    assert category['id'] == 1
    assert category['name'] == "Category_1"
    # read bulk
    res = client.get('/category/item/1,2,4')
    categorys = res.json()['data']
    assert len(categorys) == 3
    assert categorys[0]['name'] == "Category_1"
    assert categorys[2]['name'] == "Category_4"


def test_route_update(client: TestClient, fake_categorys):
    # update one
    res = client.put('/category/item/1', json={"name": "new_name"})
    count = res.json()['data']
    assert count == 1
    category = db.get(Category, 1)
    assert category.name == 'new_name'
    # update bulk
    res = client.put('/category/item/1,2,4', json={"description": "new_description"})
    count = res.json()['data']
    assert count == 3

    for category in db.scalars_all(select(Category).where(Category.id.in_([1, 2, 4]))):
        assert category.description == "new_description"


def test_route_delete(client: TestClient, fake_categorys):
    # delete one
    res = client.delete('/category/item/1')
    count = res.json()['data']
    assert count == 1
    category = db.get(Category, 1)
    assert category is None
    # delete bulk
    res = client.delete('/category/item/2,4')
    count = res.json()['data']
    assert count == 2
    assert db.get(Category, 2) is None
    assert db.get(Category, 4) is None


def test_route_list(client: TestClient, fake_categorys):
    # list
    res = client.post('/category/list')
    items = res.json()['data']['items']
    assert len(items) == 5

    res = client.post('/category/list', json={"id": 1})
    items = res.json()['data']['items']
    assert items[0]['id'] == 1

    res = client.post('/category/list', json={"name": "Category_1"})
    items = res.json()['data']['items']
    assert items[0]['name'] == "Category_1"

    res = client.post('/category/list', json={"id": "[>]1"})
    assert len(res.json()['data']['items']) == 4

    res = client.post('/category/list', json={"id": "[*]1,3"})
    assert len(res.json()['data']['items']) == 2

    res = client.post('/category/list', json={"id": "[-]2,3"})
    assert len(res.json()['data']['items']) == 2

    res = client.post('/category/list', json={"name": "[~]Category_%"})
    assert len(res.json()['data']['items']) == 5

    res = client.post('/category/list', json={"create_time": "[-]2022-01-02 00:00:00,2022-01-04 01:00:00"})
    assert len(res.json()['data']['items']) == 3
