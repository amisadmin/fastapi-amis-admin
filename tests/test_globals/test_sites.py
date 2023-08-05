import pytest

from fastapi_amis_admin.globals import sites


def test_sites(site):
    # 清空sites,确保测试环境
    sites.__sites__.clear()
    # 没有设置站点,返回False
    assert sites.exists_site() is False
    # 没有设置站点,抛出异常
    with pytest.raises(ValueError):
        assert sites.get_site()
    with pytest.raises(ValueError):
        assert sites.site
    # 设置站点
    sites.set_site(site)
    # 判断站点是否存在
    assert sites.exists_site() is True
    # 获取站点
    assert sites.get_site() == site
    assert sites.site == site
    assert isinstance(sites.site, sites.AdminSite)
    # 重复设置站点
    with pytest.raises(ValueError):
        sites.set_site(site)
