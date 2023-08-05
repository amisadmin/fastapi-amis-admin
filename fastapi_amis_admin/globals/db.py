from collections import namedtuple
from typing import Dict, Union

from lazy_object_proxy import Proxy
from sqlalchemy_database import AsyncDatabase, Database
from typing_extensions import overload

from fastapi_amis_admin.globals.sites import exists_site, get_site

DBs = namedtuple("DBs", ["sync", "async_"])

__dbs__: Dict[str, DBs] = {}


@overload
def get_db(alias: str = "default") -> Database:
    ...


@overload
def get_db(alias: str = "default", is_async: bool = True) -> AsyncDatabase:
    ...


def get_async_db(alias: str = "default") -> AsyncDatabase:
    """获取异步数据库"""
    return get_db(alias, is_async=True)


def get_db(alias: str = "default", is_async: bool = False) -> Union[Database, AsyncDatabase]:
    """获取数据库"""
    if alias in __dbs__:
        dbs = __dbs__[alias]
        if is_async and dbs.async_:
            return dbs.async_
        elif not is_async and dbs.sync:
            return dbs.sync
    if exists_site(alias):
        db = get_site(alias).db
        if is_async and isinstance(db, AsyncDatabase):
            return db
        elif not is_async and isinstance(db, Database):
            return db
    raise ValueError(f"db[{alias}] not found, please call `set_db` first")


def set_db(db: Union[Database, AsyncDatabase], alias: str = "default") -> None:
    """设置数据库"""
    if alias not in __dbs__:
        __dbs__[alias] = DBs(sync=None, async_=None)
    if isinstance(db, AsyncDatabase):
        if __dbs__[alias].async_ is not None:
            raise ValueError(f"async db[{alias}] already exists")
        __dbs__[alias] = __dbs__[alias]._replace(async_=db)
    elif isinstance(db, Database):
        if __dbs__[alias].sync is not None:
            raise ValueError(f"sync db[{alias}] already exists")
        __dbs__[alias] = __dbs__[alias]._replace(sync=db)
    else:
        raise ValueError(f"db[{alias}] must be Database or AsyncDatabase")


def exists_db(alias: str = "default", is_async: bool = False) -> bool:
    """判断数据库是否存在"""
    if alias in __dbs__:
        dbs = __dbs__[alias]
        if is_async and dbs.async_:
            return True
        elif not is_async and dbs.sync:
            return True
    return False


# 默认同步数据库.需要在项目启动时调用`set_db`设置
sync_db: Database = Proxy(get_db)
# 默认异步数据库.需要在项目启动时调用`set_db`设置
async_db: AsyncDatabase = Proxy(get_async_db)
