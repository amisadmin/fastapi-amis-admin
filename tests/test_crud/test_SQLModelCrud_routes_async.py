import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import select, func

from fastapi_amis_admin.crud import SQLModelCrud
from tests.db import async_db as db
from tests.models import Category, Tag

pytestmark = pytest.mark.asyncio


@pytest.fixture(autouse=True)
def app_routes(app: FastAPI):
    category_crud = SQLModelCrud(Category, db.engine).register_crud()

    app.include_router(category_crud.router)

    tag_crud = SQLModelCrud(Tag, db.engine).register_crud()

    app.include_router(tag_crud.router)


async def test_register_crud(async_client: AsyncClient):
    response = await async_client.get('/openapi.json')
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


async def test_route_create(async_client: AsyncClient):
    # create one
    body = {"name": 'Category', "description": "description"}
    res = await async_client.post('/category/item', json=body)
    data = res.json().get('data')
    assert data['id'] > 0
    assert data['name'] == 'Category'
    result = await db.get(Category, data['id'])
    assert result.id == data['id'], result
    await db.delete(result)
    # create bulk
    count = 3
    categorys = [
        {'id': i,
         "name": f'Category_{i}',
         "description": "description",
         "create_time": f"2022-01-0{i + 1} 00:00:00"
         } for i in range(1, count + 1)
    ]
    res = await async_client.post('/category/item', json=categorys)
    assert res.json()['data'] == count
    stmt = select(func.count(Category.id))
    result = await db.scalar(stmt)
    assert result == count


async def test_route_read(async_client: AsyncClient, fake_categorys):
    # read one
    res = await async_client.get('/category/item/1')
    category = res.json()['data']
    assert category['id'] == 1
    assert category['name'] == "Category_1"
    # read bulk
    res = await async_client.get('/category/item/1,2,4')
    categorys = res.json()['data']
    assert len(categorys) == 3
    assert categorys[0]['name'] == "Category_1"
    assert categorys[2]['name'] == "Category_4"


async def test_route_update(async_client: AsyncClient, fake_categorys):
    # update one
    res = await async_client.put('/category/item/1', json={"name": "new_name"})
    count = res.json()['data']
    assert count == 1
    category = await db.get(Category, 1)
    assert category.name == 'new_name'
    # update bulk
    res = await async_client.put('/category/item/1,2,4', json={"description": "new_description"})
    count = res.json()['data']
    assert count == 3
    for category in await db.scalars_all(select(Category).where(Category.id.in_([1, 2, 4]))):
        assert category.description == "new_description"


async def test_route_delete(async_client: AsyncClient, fake_categorys):
    # delete one
    res = await async_client.delete('/category/item/1')
    count = res.json()['data']
    assert count == 1
    category = await db.get(Category, 1)
    assert category is None
    # delete bulk
    res = await async_client.delete('/category/item/2,4')
    count = res.json()['data']
    assert count == 2
    assert await db.get(Category, 2) is None
    assert await db.get(Category, 4) is None


async def test_route_list(async_client: AsyncClient, fake_categorys):
    # list
    res = await async_client.post('/category/list')
    items = res.json()['data']['items']
    assert len(items) == 5

    res = await async_client.post('/category/list', json={"id": 1})
    items = res.json()['data']['items']
    assert items[0]['id'] == 1

    res = await async_client.post('/category/list', json={"name": "Category_1"})
    items = res.json()['data']['items']
    assert items[0]['name'] == "Category_1"

    res = await async_client.post('/category/list', json={"id": "[>]1"})
    assert len(res.json()['data']['items']) == 4

    res = await async_client.post('/category/list', json={"id": "[*]1,3"})
    assert len(res.json()['data']['items']) == 2

    res = await async_client.post('/category/list', json={"id": "[-]2,3"})
    assert len(res.json()['data']['items']) == 2

    res = await async_client.post('/category/list', json={"name": "[~]Category_%"})
    assert len(res.json()['data']['items']) == 5

    res = await async_client.post('/category/list', json={"create_time": "[-]2022-01-02 00:00:00,2022-01-04 01:00:00"})
    assert len(res.json()['data']['items']) == 3
