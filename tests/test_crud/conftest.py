import pytest

from tests.test_crud.main import app


@pytest.fixture(scope='session', autouse=True)
def startup():
    import asyncio
    # asyncio.run(app.router.startup())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.router.startup())
