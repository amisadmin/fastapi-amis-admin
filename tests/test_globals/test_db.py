import pytest
from sqlalchemy_database import AsyncDatabase, Database

from fastapi_amis_admin import globals as g
from tests.conftest import sync_db


def test_sites(site):
    # 清空sites,db,确保测试环境
    g.remove_global()
    # 没有设置db,返回False
    assert g.exists_db() is False
    assert g.exists_db(is_async=True) is False
    with pytest.raises(ValueError):
        assert g.sync_db
    with pytest.raises(ValueError):
        assert g.async_db
    # 设置site,site.db为异步数据库
    g.set_site(site)
    # 判断db是否存在
    assert g.exists_db() is False
    assert g.exists_db(is_async=True) is False
    # 获取db
    with pytest.raises(ValueError):
        assert g.sync_db
    assert g.async_db == site.db  # 读取site.db
    assert isinstance(g.async_db, AsyncDatabase)
    # 设置同步db
    g.set_db(sync_db)
    # 判断db是否存在
    assert g.exists_db() is True
    assert g.exists_db(is_async=True) is False
    # 获取db
    assert g.sync_db == sync_db
    assert isinstance(g.sync_db, Database)
    # 重复设置db
    assert g.set_db(sync_db) is False
