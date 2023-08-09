from typing import Union

from sqlalchemy_database import AsyncDatabase, Database
from typing_extensions import overload

from fastapi_amis_admin.globals._sites import exists_site, get_site
from fastapi_amis_admin.globals.core import DEFAULT_ALIAS, exists_global, get_global, set_global

SYNC_DB_NAME = "sync_db"
ASYNC_DB_NAME = "async_db"


def get_sync_db(*, alias: str = DEFAULT_ALIAS) -> Database:
    """Get sync database"""
    if exists_global(SYNC_DB_NAME, alias=alias):
        return get_global(SYNC_DB_NAME, alias=alias)
    if exists_site(alias=alias):
        db = get_site(alias=alias).db
        if isinstance(db, Database):
            return db
    raise ValueError(f"sync_db[{alias}] not found, please call `set_db` first")


def get_async_db(*, alias: str = DEFAULT_ALIAS) -> AsyncDatabase:
    """Get async database"""
    if exists_global(ASYNC_DB_NAME, alias=alias):
        return get_global(ASYNC_DB_NAME, alias=alias)
    if exists_site(alias=alias):
        db = get_site(alias=alias).db
        if isinstance(db, AsyncDatabase):
            return db
    raise ValueError(f"async_db[{alias}] not found, please call `set_db` first")


@overload
def get_db(*, alias: str = DEFAULT_ALIAS) -> Database:
    ...


@overload
def get_db(*, alias: str = DEFAULT_ALIAS, is_async: bool = True) -> AsyncDatabase:
    ...


def get_db(*, alias: str = DEFAULT_ALIAS, is_async: bool = False) -> Union[Database, AsyncDatabase]:
    """Get database"""
    if is_async:
        return get_async_db(alias=alias)
    return get_sync_db(alias=alias)


def set_db(
    db: Union[Database, AsyncDatabase],
    *,
    alias: str = DEFAULT_ALIAS,
    overwrite: bool = False,
) -> bool:
    """Set database"""
    if isinstance(db, AsyncDatabase):
        return set_global(ASYNC_DB_NAME, db, alias=alias, overwrite=overwrite)
    elif isinstance(db, Database):
        return set_global(SYNC_DB_NAME, db, alias=alias, overwrite=overwrite)
    else:
        raise ValueError(f"db[{alias}] must be Database or AsyncDatabase")


def exists_db(*, alias: str = DEFAULT_ALIAS, is_async: bool = False) -> bool:
    """Judge whether the database exists"""
    if is_async:
        return exists_global(ASYNC_DB_NAME, alias=alias)
    else:
        return exists_global(SYNC_DB_NAME, alias=alias)
