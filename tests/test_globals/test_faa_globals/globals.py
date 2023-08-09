# sqlite
from sqlalchemy_database import AsyncDatabase, Database

from fastapi_amis_admin.admin import AdminSite, Settings

sync_db = Database.create(
    "sqlite:///amisadmin.db?check_same_thread=False",
    session_options={
        "expire_on_commit": False,
    },
)
_async_db = AsyncDatabase.create(
    "sqlite+aiosqlite:///amisadmin.db?check_same_thread=False",
    session_options={
        "expire_on_commit": False,
    },
)
site = AdminSite(settings=Settings(site_path=""), engine=_async_db.engine)
