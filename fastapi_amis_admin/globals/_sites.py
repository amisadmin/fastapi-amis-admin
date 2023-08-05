from lazy_object_proxy import Proxy

from fastapi_amis_admin.admin import AdminSite
from fastapi_amis_admin.globals.core import exists_global, get_global, set_global

SITE_NAME = "site"


def get_site(*, alias: str = "default") -> AdminSite:
    """Get site"""
    return get_global(SITE_NAME, alias=alias)


def set_site(site: AdminSite, *, alias: str = "default") -> None:
    """Set site"""
    return set_global(SITE_NAME, site, alias=alias)


def exists_site(*, alias: str = "default") -> bool:
    """Judge whether the site exists"""
    return exists_global(SITE_NAME, alias=alias)


# Default site. Need to call `set_site` to set when the project starts
site: AdminSite = Proxy(get_site)
