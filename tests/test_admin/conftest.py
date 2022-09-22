from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from starlette.testclient import TestClient

from fastapi_amis_admin.admin import AdminSite, Settings
from tests.conftest import async_db


@pytest.fixture
def site() -> AdminSite:
    return AdminSite(settings=Settings(root_path=""), engine=async_db.engine)


@pytest.fixture
def client(site: AdminSite) -> TestClient:
    with TestClient(app=site.fastapi, base_url="http://testserver") as c:
        yield c


@pytest.fixture
async def async_client(site: AdminSite) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=site.fastapi, base_url="http://testserver") as c:
        yield c
