from fastapi import FastAPI

from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite

# 创建FastAPI应用
app = FastAPI()

# 创建AdminSite实例
site = AdminSite(settings=Settings(database_url_async="sqlite+aiosqlite:///amisadmin.db"))

# 挂载后台管理系统
site.mount_app(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
