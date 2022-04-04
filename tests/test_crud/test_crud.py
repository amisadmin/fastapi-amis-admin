from fastapi.testclient import TestClient
from tests.test_crud.main import app

client = TestClient(app)


def test_register_crud():
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


def test_crud_one():
    # create one
    res = client.post('/category/item', json={"name": 'category_name', "description": "description"})
    category = res.json().get('data')
    assert category['id'] > 0, res.json()
    assert category['name'] == 'category_name', res.json()
    # update one
    res = client.put(f'/category/item/{category["id"]}', json={"name": "category_name1"})
    count = res.json()['data']
    assert count == 1
    # read one
    res = client.get(f'/category/item/{category["id"]}')
    category_new = res.json()['data']
    assert category_new['id'] == category["id"]
    assert category_new['name'] == "category_name1"
    # delete one
    res = client.delete(f'/category/item/{category["id"]}')
    count = res.json()['data']
    assert count == 1, res.text


def test_crud_bulk():
    # create one
    category_name = 'category_name'
    count = 3
    # create bulk
    categorys = [{'id': i + 1, "name": f'{category_name}_{i}', "description": "description","create_time":f"2022-01-0{i+1} 00:00:00"} for i in range(count)]
    res = client.post('/category/item', json=categorys)
    assert res.json()['data'] == count, res.json()
    # update bulk
    item_ids = ','.join([str(category['id']) for category in categorys])
    res = client.put(f'/category/item/{item_ids}', json={"description": "description2"})
    assert res.json()['data'] == count, res.json()
    # read bulk
    res = client.get(f'/category/item/{item_ids}')
    categorys_new = res.json()['data']
    assert len(categorys_new) == count, res.json()
    assert categorys_new[0]['description'] == "description2"
    # list
    res = client.post('/category/list')
    categorys_new = res.json()['data']['items']
    assert len(categorys_new) == count, res.json()

    res = client.post('/category/list',json={"id":1})
    categorys_new = res.json()['data']['items']
    assert  categorys_new[0]['id'] == 1, res.json()

    res = client.post('/category/list',json={"name":"category_name_1"})
    categorys_new = res.json()['data']['items']
    assert  categorys_new[0]['name'] == "category_name_1", res.json()

    res = client.post('/category/list', json={"id": "[>]1"})
    assert len(res.json()['data']['items']) == 2, res.json()

    res = client.post('/category/list', json={"id": "[*]1,3"})
    assert len(res.json()['data']['items']) == 2, res.json()

    res = client.post('/category/list', json={"id": "[-]2,3"})
    assert len(res.json()['data']['items']) == 2, res.json()

    res = client.post('/category/list', json={"name": "[~]category_name%"})
    assert len(res.json()['data']['items']) == 3, res.json()

    res = client.post('/category/list', json={"create_time": "[-]2022-01-02 00:00:00,2022-01-04 00:00:00"})
    assert len(res.json()['data']['items']) == 2, res.json()

    res = client.post('/category/list', json={"create_time": "[-]2022-01-04 00:00:00,2022-01-05 00:00:00"})
    assert len(res.json()['data']['items']) == 0, res.json()

    # delete one
    res = client.delete(f'/category/item/{item_ids}')
    assert res.json()['data'] == count, res.json()
