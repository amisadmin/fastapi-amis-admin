from sqlalchemy_database import AsyncDatabase, Database

from fastapi_amis_admin.admin import AdminSite

from ._db import (
    ASYNC_DB_NAME,
    SYNC_DB_NAME,
    exists_db,
    get_async_db,
    get_db,
    get_sync_db,
    set_db,
)
from ._sites import (
    SITE_NAME,
    exists_site,
    get_site,
    set_site,
)
from .core import (
    DEFAULT_ALIAS,
    __faa_globals__,
    exists_global,
    get_global,
    remove_global,
    set_global,
)

sync_db: Database
async_db: AsyncDatabase
site: AdminSite


def __getattr__(name: str):
    if __faa_globals__ is not None and hasattr(__faa_globals__, name):
        return getattr(__faa_globals__, name)
    elif name == SYNC_DB_NAME:
        return get_sync_db()
    elif name == ASYNC_DB_NAME:
        return get_async_db()
    elif name == SITE_NAME:
        return get_site()
    elif exists_global(name, alias=DEFAULT_ALIAS):
        return get_global(name, alias=DEFAULT_ALIAS)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
