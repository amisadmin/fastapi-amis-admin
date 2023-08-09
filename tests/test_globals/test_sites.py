import pytest

from fastapi_amis_admin import globals as g
from fastapi_amis_admin.admin import AdminSite


def test_sites(site):
    # 清空sites,确保测试环境
    g.remove_global()
    # 没有设置站点,返回False
    assert g.exists_site() is False
    # 没有设置站点,抛出异常
    with pytest.raises(ValueError):
        assert g.get_site()
    with pytest.raises(ValueError):
        assert g.site
    # 设置站点
    g.set_site(site)
    # 判断站点是否存在
    assert g.exists_site() is True
    # 获取站点
    assert g.get_site() == site
    assert g.site == site
    assert isinstance(g.site, AdminSite)
    # 重复设置站点
    assert g.set_site(site) is False
