from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy_database import AsyncDatabase, Database
from starlette.testclient import TestClient

from fastapi_amis_admin.admin import AdminSite, Settings

# sqlite
sync_db = Database.create("sqlite:///amisadmin.db?check_same_thread=False")
async_db = AsyncDatabase.create("sqlite+aiosqlite:///amisadmin.db?check_same_thread=False")


# mysql
# sync_db = Database.create('mysql+pymysql://root:123456@127.0.0.1:3306/amisadmin?charset=utf8mb4')
# async_db = AsyncDatabase.create('mysql+aiomysql://root:123456@127.0.0.1:3306/amisadmin?charset=utf8mb4')

# postgresql
# sync_db = Database.create('postgresql://postgres:root@127.0.0.1:5432/amisadmin')
# async_db = AsyncDatabase.create('postgresql+asyncpg://postgres:root@127.0.0.1:5432/amisadmin')

# oracle
# sync_db = Database.create('oracle+cx_oracle://scott:tiger@tnsname')

# SQL Server
# sync_db = Database.create('mssql+pyodbc://scott:tiger@mydsn')


@pytest.fixture
def site() -> AdminSite:
    return AdminSite(settings=Settings(site_path=""), engine=async_db.engine)


@pytest.fixture
def client(site: AdminSite) -> TestClient:
    with TestClient(app=site.fastapi, base_url="http://testserver") as c:
        yield c


@pytest.fixture
async def async_client(site: AdminSite) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=site.fastapi, base_url="http://testserver") as c:
        yield c


@pytest.fixture
def session():
    with sync_db.session_maker() as session:
        yield session


@pytest.fixture
async def async_session():
    async with async_db.session_maker() as session:
        yield session


@pytest.fixture(autouse=True)
def _setup_sync_db() -> Database:
    yield sync_db
    # Free connection pool resources
    sync_db.close()  # type: ignore


@pytest.fixture(autouse=True)
async def _setup_async_db() -> AsyncDatabase:
    yield async_db
    await async_db.async_close()  # Free connection pool resources
