import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from fastapi_amis_admin.crud import SQLModelCrud
from tests.db import async_db as db
from tests.models import Category

pytestmark = pytest.mark.asyncio


async def test_pk_name(app: FastAPI, async_client: AsyncClient, fake_categorys):
    class CategoryCrud(SQLModelCrud):
        router_prefix = '/category'
        pk_name = 'name'

    ins = CategoryCrud(Category, db.engine).register_crud()

    app.include_router(ins.router)
    assert ins.pk.key == 'name'
    # read one
    res = await async_client.get('/category/item/Category_1')
    category = res.json()['data']
    assert category['id'] == 1
    assert category['name'] == "Category_1"
    # read bulk
    res = await async_client.get('/category/item/Category_1,Category_2,Category_4')
    categorys = res.json()['data']
    assert len(categorys) == 3
    assert categorys[0]['name'] == "Category_1"
    assert categorys[2]['name'] == "Category_4"


async def test_readonly_fields(app: FastAPI, async_client: AsyncClient, fake_categorys):
    class CategoryCrud(SQLModelCrud):
        router_prefix = '/category'
        readonly_fields = [Category.name]

    ins = CategoryCrud(Category, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    openapi = app.openapi()
    schemas = openapi['components']['schemas']
    assert 'description' in schemas['CategoryCrudUpdate']['properties']
    assert 'name' not in schemas['CategoryCrudUpdate']['properties']

    # test api
    res = await async_client.put('/category/item/1', json={"name": "new_name"})
    assert res.json() == {'detail': 'error data handle'}
    res = await async_client.put('/category/item/1', json={"description": "new_description"})
    assert res.json()['data'] == 1


async def test_update_fields(app: FastAPI, async_client: AsyncClient, fake_categorys):
    class CategoryCrud(SQLModelCrud):
        router_prefix = '/category'
        update_fields = [Category.name]

    ins = CategoryCrud(Category, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    openapi = app.openapi()
    schemas = openapi['components']['schemas']
    assert 'description' not in schemas['CategoryCrudUpdate']['properties']
    assert 'name' in schemas['CategoryCrudUpdate']['properties']

    # test api
    res = await async_client.put('/category/item/1', json={"name": "new_name"})
    assert res.json()['data'] == 1

    res = await async_client.put('/category/item/1', json={"description": "new_description"})
    assert res.json() == {'detail': 'error data handle'}


async def test_list_filter(app: FastAPI, async_client: AsyncClient, fake_categorys):
    class CategoryCrud(SQLModelCrud):
        router_prefix = '/category'
        list_filter = [Category.id, Category.name]

    ins = CategoryCrud(Category, db.engine).register_crud()

    app.include_router(ins.router)

    assert 'name' in ins.schema_filter.__fields__
    assert 'description' not in ins.schema_filter.__fields__

    # test schemas
    openapi = app.openapi()
    schemas = openapi['components']['schemas']
    assert 'name' in schemas['CategoryCrudFilter']['properties']
    assert 'description' not in schemas['CategoryCrudFilter']['properties']

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


async def test_create_fields(app: FastAPI, async_client: AsyncClient):
    class CategoryCrud(SQLModelCrud):
        router_prefix = '/category'
        create_fields = [Category.name]

    ins = CategoryCrud(Category, db.engine).register_crud()

    app.include_router(ins.router)

    assert 'name' in ins.schema_create.__fields__
    assert 'description' not in ins.schema_create.__fields__

    # test schemas
    openapi = app.openapi()
    schemas = openapi['components']['schemas']
    assert 'name' in schemas['CategoryCrudCreate']['properties']
    assert 'description' not in schemas['CategoryCrudCreate']['properties']
    # test api
    body = {"name": 'Category', "description": "description"}
    res = await async_client.post('/category/item', json=body)
    data = res.json().get('data')
    assert data['id'] > 0
    assert data['name'] == 'Category'
    assert data['description'] == ''
