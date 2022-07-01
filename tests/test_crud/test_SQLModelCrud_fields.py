from fastapi import FastAPI
from httpx import AsyncClient

from fastapi_amis_admin.crud import SQLModelCrud
from tests.db import async_db as db
from tests.models import User


async def test_pk_name(app: FastAPI, async_client: AsyncClient, fake_users):
    class UserCrud(SQLModelCrud):
        router_prefix = '/user'
        pk_name = "username"

    ins = UserCrud(User, db.engine).register_crud()

    app.include_router(ins.router)
    assert ins.pk.key == "username"
    # read one
    res = await async_client.get('/user/item/User_1')
    user = res.json()['data']
    assert user['id'] == 1
    assert user["username"] == "User_1"
    # read bulk
    res = await async_client.get('/user/item/User_1,User_2,User_4')
    users = res.json()['data']
    assert len(users) == 3
    assert users[0]["username"] == "User_1"
    assert users[2]["username"] == "User_4"


async def test_readonly_fields(app: FastAPI, async_client: AsyncClient, fake_users):
    class UserCrud(SQLModelCrud):
        router_prefix = '/user'
        readonly_fields = [User.username]

    ins = UserCrud(User, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    openapi = app.openapi()
    schemas = openapi['components']['schemas']
    assert 'password' in schemas['UserCrudUpdate']['properties']
    assert "username" not in schemas['UserCrudUpdate']['properties']

    # test api
    res = await async_client.put('/user/item/1', json={"username": "new_name"})
    assert res.json() == {'detail': 'error data handle'}
    res = await async_client.put('/user/item/1', json={"password": "new_password"})
    assert res.json()['data'] == 1


async def test_update_fields(app: FastAPI, async_client: AsyncClient, fake_users):
    class UserCrud(SQLModelCrud):
        router_prefix = '/user'
        update_fields = [User.username]

    ins = UserCrud(User, db.engine).register_crud()

    app.include_router(ins.router)

    # test schemas
    openapi = app.openapi()
    schemas = openapi['components']['schemas']
    assert 'password' not in schemas['UserCrudUpdate']['properties']
    assert "username" in schemas['UserCrudUpdate']['properties']

    # test api
    res = await async_client.put('/user/item/1', json={"username": "new_name"})
    assert res.json()['data'] == 1

    res = await async_client.put('/user/item/1', json={"password": "new_password"})
    assert res.json() == {'detail': 'error data handle'}


async def test_list_filter(app: FastAPI, async_client: AsyncClient, fake_users):
    class UserCrud(SQLModelCrud):
        router_prefix = '/user'
        list_filter = [User.id, User.username]

    ins = UserCrud(User, db.engine).register_crud()

    app.include_router(ins.router)

    assert "username" in ins.schema_filter.__fields__
    assert 'password' not in ins.schema_filter.__fields__

    # test schemas
    openapi = app.openapi()
    schemas = openapi['components']['schemas']
    assert "username" in schemas['UserCrudFilter']['properties']
    assert 'password' not in schemas['UserCrudFilter']['properties']

    # test api
    res = await async_client.post('/user/list', json={"id": 1})
    items = res.json()['data']['items']
    assert items[0]['id'] == 1

    res = await async_client.post('/user/list', json={"username": "User_1"})
    items = res.json()['data']['items']
    assert items[0]["username"] == "User_1"

    res = await async_client.post('/user/list', json={"password": "new_password"})
    items = res.json()['data']['items']
    assert items


async def test_create_fields(app: FastAPI, async_client: AsyncClient):
    class UserCrud(SQLModelCrud):
        router_prefix = '/user'
        create_fields = [User.username]

    ins = UserCrud(User, db.engine).register_crud()

    app.include_router(ins.router)

    assert "username" in ins.schema_create.__fields__
    assert 'password' not in ins.schema_create.__fields__

    # test schemas
    openapi = app.openapi()
    schemas = openapi['components']['schemas']
    assert "username" in schemas['UserCrudCreate']['properties']
    assert 'password' not in schemas['UserCrudCreate']['properties']
    # test api
    body = {"username": 'User', "password": "password"}
    res = await async_client.post('/user/item', json=body)
    data = res.json().get('data')
    assert data['id'] > 0
    assert data["username"] == 'User'
    assert data['password'] == ''
