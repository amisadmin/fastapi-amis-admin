import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from pydantic import BaseModel

from fastapi_amis_admin.crud import SQLModelCrud
from tests.db import async_db as db
from tests.models import Category

pytestmark = pytest.mark.asyncio


class CategoryFilter(BaseModel):
    id: int = None
    name: str = None

async def test_schema_update(app: FastAPI, async_client: AsyncClient, fake_categorys):
    class CategoryUpdate(BaseModel):
        description: str = None

    class CategoryCrud(SQLModelCrud):
        router_prefix = '/category'
        schema_update = CategoryUpdate

    ins = CategoryCrud(Category, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    openapi = app.openapi()
    schemas = openapi['components']['schemas']
    assert 'description' in schemas['CategoryUpdate']['properties']
    assert 'name' not in schemas['CategoryUpdate']['properties']

    # test api
    res = await async_client.put('/category/item/1', json={"name": "new_name"})
    assert res.json() == {'detail': 'error data handle'}
    res = await async_client.put('/category/item/1', json={"description": "new_description"})
    assert res.json()['data'] == 1


async def test_schema_create(app: FastAPI, async_client: AsyncClient):
    class CategoryCreate(BaseModel):
        name: str

    class CategoryCrud(SQLModelCrud):
        router_prefix = '/category'
        schema_create = CategoryCreate

    ins = CategoryCrud(Category, db.engine).register_crud()

    app.include_router(ins.router)

    assert 'name' in ins.schema_create.__fields__
    assert 'description' not in ins.schema_create.__fields__

    # test schemas
    openapi = app.openapi()
    schemas = openapi['components']['schemas']
    assert 'name' in schemas['CategoryCreate']['properties']
    assert 'description' not in schemas['CategoryCreate']['properties']
    # test api
    body = {"name": 'Category', "description": "description"}
    res = await async_client.post('/category/item', json=body)
    data = res.json().get('data')
    assert data['id'] > 0
    assert data['name'] == 'Category'
    assert data['description'] == ''


async def test_schema_list(app: FastAPI, async_client: AsyncClient, fake_categorys):
    class CategoryList(BaseModel):
        id: int
        name: str

    class CategoryCrud(SQLModelCrud):
        router_prefix = '/category'
        schema_list = CategoryList

    ins = CategoryCrud(Category, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    openapi = app.openapi()
    schemas = openapi['components']['schemas']
    assert 'description' not in schemas['CategoryList']['properties']
    assert 'name' in schemas['CategoryList']['properties']

    # test api
    res = await async_client.post('/category/list', json={"id": 1})
    items = res.json()['data']['items']
    assert items[0]['id'] == 1
    assert 'name' in items[0]
    assert 'description' not in items[0]


async def test_schema_read(app: FastAPI, async_client: AsyncClient, fake_categorys):
    class CategoryRead(BaseModel):
        id: int
        name: str

    class CategoryCrud(SQLModelCrud):
        router_prefix = '/category'
        schema_read = CategoryRead

    ins = CategoryCrud(Category, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    openapi = app.openapi()
    schemas = openapi['components']['schemas']
    assert 'description' not in schemas['CategoryRead']['properties']
    assert 'name' in schemas['CategoryRead']['properties']

    # test api
    res = await async_client.get('/category/item/1')
    items = res.json()['data']
    assert items['id'] == 1
    assert 'name' in items
    assert 'description' not in items


# todo perfect
async def test_schema_filter(app: FastAPI, async_client: AsyncClient, fake_categorys):
    class CategoryFilter(BaseModel):
        id: int = None
        name: str = None

    class CategoryCrud(SQLModelCrud):
        router_prefix = '/category'
        schema_filter = CategoryFilter

    ins = CategoryCrud(Category, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    openapi = app.openapi()
    schemas = openapi['components']['schemas']
    assert 'description' not in schemas['CategoryFilter']['properties']
    assert 'name' in schemas['CategoryFilter']['properties']

    # test api
    res = await async_client.post('/category/list', json={"id": 1})
    items = res.json()['data']['items']
    assert items[0]['id'] == 1

    res = await async_client.post('/category/list', json={"name": "Category_1"})
    items = res.json()['data']['items']
    assert items[0]['name'] == "Category_1"

    res = await async_client.post('/category/list', json={"description": "new_description"})
    items = res.json()['data']['items']
    assert items
