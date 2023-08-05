import pytest

from fastapi_amis_admin.globals import db, sites
from tests.conftest import sync_db


def test_sites(site):
    # 清空sites,db,确保测试环境
    sites.__sites__.clear()
    db.__dbs__.clear()
    # 没有设置db,返回False
    assert db.exists_db() is False
    assert db.exists_db(is_async=True) is False
    with pytest.raises(ValueError):
        assert db.sync_db
    with pytest.raises(ValueError):
        assert db.async_db
    # 设置site,site.db为异步数据库
    sites.set_site(site)
    # 判断db是否存在
    assert db.exists_db() is False
    assert db.exists_db(is_async=True) is False
    # 获取db
    with pytest.raises(ValueError):
        assert db.sync_db
    assert db.async_db == site.db  # 读取site.db
    assert isinstance(db.async_db, db.AsyncDatabase)
    # 设置同步db
    db.set_db(sync_db)
    # 判断db是否存在
    assert db.exists_db() is True
    assert db.exists_db(is_async=True) is False
    # 获取db
    assert db.sync_db == sync_db
    assert isinstance(db.sync_db, db.Database)
    # 重复设置db
    with pytest.raises(ValueError):
        db.set_db(sync_db)
