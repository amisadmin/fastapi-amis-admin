import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from pydantic import BaseModel
from sqlalchemy import event

from fastapi_amis_admin.crud import SqlalchemyCrud
from fastapi_amis_admin.crud.parser import TableModelParser
from tests.conftest import async_db as db
from tests.test_crud.test_SqlalchemyCrud_routes_async import (
    test_route_create,
    test_route_delete,
    test_route_update,
)


class EventsCounter(BaseModel):
    before: int = 0
    after: int = 0


@pytest.fixture()
def event_counter():
    return EventsCounter()


@pytest.fixture(autouse=True)
def app_routes(app: FastAPI, models):
    user_schema = TableModelParser.get_table_model_schema(models.User)
    user_crud = SqlalchemyCrud(models.User, db.engine).register_crud(schema_read=user_schema)
    app.include_router(user_crud.router)


async def test_create_event(async_client: AsyncClient, event_counter, models):
    @event.listens_for(models.User, "before_insert")
    def receive_before_insert(mapper, connection, target):
        "listen for the 'before_insert' event"
        assert isinstance(target, models.User)
        event_counter.before += 1

    @event.listens_for(models.User, "after_insert")
    def receive_after_insert(mapper, connection, target):
        "listen for the 'after_insert' event"
        assert isinstance(target, models.User)
        event_counter.after += 1

    assert event_counter.before == 0
    assert event_counter.after == 0
    await test_route_create(async_client, models)
    assert event_counter.before > 0
    assert event_counter.after == event_counter.before


async def test_update_event(async_client: AsyncClient, fake_users, event_counter, models):
    @event.listens_for(models.User, "before_update")
    def receive_before_update(mapper, connection, target):
        "listen for the 'before_update' event"
        assert isinstance(target, models.User)
        event_counter.before += 1

    @event.listens_for(models.User, "after_update")
    def receive_after_update(mapper, connection, target):
        "listen for the 'after_update' event"
        assert isinstance(target, models.User)
        event_counter.after += 1

    @event.listens_for(models.User.username, "set")
    def receive_set(target, value, old, initiator):
        "listen for the 'set' event"
        assert isinstance(target, models.User)

    # update one
    assert event_counter.before == 0
    assert event_counter.after == 0
    await test_route_update(async_client, fake_users, models)
    assert event_counter.before > 0
    assert event_counter.after == event_counter.before


async def test_delete_event(async_client: AsyncClient, fake_users, event_counter, models):
    @event.listens_for(models.User, "before_delete")
    def receive_before_delete(mapper, connection, target):
        "listen for the 'before_delete' event"
        assert isinstance(target, models.User)
        event_counter.before += 1

    @event.listens_for(models.User, "after_delete")
    def receive_after_delete(mapper, connection, target):
        "listen for the 'after_delete' event"
        assert isinstance(target, models.User)
        event_counter.after += 1

    # delete one
    assert event_counter.before == 0
    assert event_counter.after == 0
    await test_route_delete(async_client, fake_users, models)
    assert event_counter.before > 0
    assert event_counter.after == event_counter.before
