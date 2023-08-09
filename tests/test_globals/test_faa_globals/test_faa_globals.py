import os
import sys
from importlib import import_module

from tests.test_globals.test_faa_globals import globals as g2


def test_faa_globals():
    # must set FAA_GLOBALS environment variable before importing globals
    os.environ.setdefault("FAA_GLOBALS", "tests.test_globals.test_faa_globals.globals")

    # Clear previous import
    sys.modules.pop("fastapi_amis_admin.globals", None)
    sys.modules.pop("fastapi_amis_admin.globals.core", None)

    # Re-import
    g = import_module("fastapi_amis_admin.globals")
    # from fastapi_amis_admin import globals as g

    g.remove_global()
    assert g.__faa_globals__ is not None
    # Default read site in faa_globals
    assert g.exists_global("site")
    assert g.site is g2.site
    # Default read sync_db/async_db in faa_globals
    # If not set, try to read site.db
    assert g.sync_db is g2.sync_db
    assert g.async_db is g2._async_db
    assert g.exists_db(is_async=True) is False  # site.db
