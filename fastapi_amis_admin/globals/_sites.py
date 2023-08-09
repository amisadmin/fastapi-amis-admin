from fastapi_amis_admin.admin import AdminSite
from fastapi_amis_admin.globals.core import DEFAULT_ALIAS, exists_global, get_global, set_global

SITE_NAME = "site"


def get_site(*, alias: str = DEFAULT_ALIAS) -> AdminSite:
    """Get site"""
    return get_global(SITE_NAME, alias=alias)


def set_site(
    site: AdminSite,
    *,
    alias: str = DEFAULT_ALIAS,
    overwrite: bool = False,
) -> bool:
    """Set site"""
    return set_global(SITE_NAME, site, alias=alias, overwrite=overwrite)


def exists_site(*, alias: str = DEFAULT_ALIAS) -> bool:
    """Judge whether the site exists"""
    return exists_global(SITE_NAME, alias=alias)
