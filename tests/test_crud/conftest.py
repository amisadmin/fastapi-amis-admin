import datetime
from typing import AsyncGenerator, Any, List

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import insert
from sqlmodel import SQLModel

from tests.db import async_db as db
from tests.models import Category

pytestmark = pytest.mark.asyncio


@pytest.fixture
def app() -> FastAPI:
    return FastAPI()


@pytest.fixture
async def prepare_database() -> AsyncGenerator[None, None]:
    async with db.engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with db.engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await db.engine.dispose()


@pytest.fixture
async def async_client(app: FastAPI, prepare_database: Any) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://testserver") as c:
        yield c


@pytest.fixture
async def fake_categorys() -> List[Category]:
    data = [
        {'id': i,
         "name": f'Category_{i}',
         "description": f"description_{i}",
         "create_time": datetime.datetime.strptime(f"2022-01-0{i} 00:00:00", "%Y-%m-%d %H:%M:%S")
         } for i in range(1, 6)
    ]
    await db.execute(insert(Category).values(data), commit=True)
    return [Category.parse_obj(item) for item in data]
