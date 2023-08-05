from typing import Union

from lazy_object_proxy import Proxy
from sqlalchemy_database import AsyncDatabase, Database
from typing_extensions import overload

from fastapi_amis_admin.globals._sites import exists_site, get_site
from fastapi_amis_admin.globals.core import exists_global, get_global, set_global

SYNC_DB_NAME = "sync_db"
ASYNC_DB_NAME = "async_db"


def get_sync_db(*, alias: str = "default") -> Database:
    """Get sync database"""
    if exists_global(SYNC_DB_NAME, alias=alias):
        return get_global(SYNC_DB_NAME, alias=alias)
    if exists_site(alias=alias):
        db = get_site(alias=alias).db
        if isinstance(db, Database):
            return db
    raise ValueError(f"sync_db[{alias}] not found, please call `set_db` first")


def get_async_db(*, alias: str = "default") -> AsyncDatabase:
    """Get async database"""
    if exists_global(ASYNC_DB_NAME, alias=alias):
        return get_global(ASYNC_DB_NAME, alias=alias)
    if exists_site(alias=alias):
        db = get_site(alias=alias).db
        if isinstance(db, AsyncDatabase):
            return db
    raise ValueError(f"async_db[{alias}] not found, please call `set_db` first")


@overload
def get_db(*, alias: str = "default") -> Database:
    ...


@overload
def get_db(*, alias: str = "default", is_async: bool = True) -> AsyncDatabase:
    ...


def get_db(*, alias: str = "default", is_async: bool = False) -> Union[Database, AsyncDatabase]:
    """Get database"""
    if is_async:
        return get_async_db(alias=alias)
    return get_sync_db(alias=alias)


def set_db(db: Union[Database, AsyncDatabase], *, alias: str = "default") -> None:
    """Set database"""
    if isinstance(db, AsyncDatabase):
        set_global(ASYNC_DB_NAME, db, alias=alias)
    elif isinstance(db, Database):
        set_global(SYNC_DB_NAME, db, alias=alias)
    else:
        raise ValueError(f"db[{alias}] must be Database or AsyncDatabase")


def exists_db(*, alias: str = "default", is_async: bool = False) -> bool:
    """Judge whether the database exists"""
    if is_async:
        return exists_global(ASYNC_DB_NAME, alias=alias)
    else:
        return exists_global(SYNC_DB_NAME, alias=alias)


# Default sync database. Need to call `set_db` to set when the project starts
sync_db: Database = Proxy(get_sync_db)
# Default async database. Need to call `set_db` to set when the project starts
async_db: AsyncDatabase = Proxy(get_async_db)
