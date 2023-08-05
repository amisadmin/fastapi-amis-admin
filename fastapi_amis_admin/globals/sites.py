from typing import Dict

from lazy_object_proxy import Proxy

from fastapi_amis_admin.admin import AdminSite

__sites__: Dict[str, AdminSite] = {}


def get_site(alias: str = "default") -> AdminSite:
    """获取站点"""
    if alias not in __sites__:
        raise ValueError(f"site[{alias}] not found, please call `set_site` first")
    return __sites__[alias]


def set_site(site: AdminSite, alias: str = "default") -> None:
    """设置站点"""
    if alias in __sites__:
        raise ValueError(f"site[{alias}] already exists")
    __sites__[alias] = site


def exists_site(alias: str = "default") -> bool:
    """判断站点是否存在"""
    return alias in __sites__


# 默认站点.需要在项目启动时调用`set_site`设置
site: AdminSite = Proxy(get_site)
