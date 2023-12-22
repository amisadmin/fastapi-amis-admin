from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from sqlmodel import SQLModel

from fastapi_amis_admin.admin import admin
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_amis_admin.models.fields import Field


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 创建初始化数据库表
    await site.db.async_run_sync(SQLModel.metadata.create_all, is_session=False)
    yield


# 创建FastAPI应用
app = FastAPI(lifespan=lifespan)

# 创建AdminSite实例
site = AdminSite(settings=Settings(database_url_async="sqlite+aiosqlite:///amisadmin.db?check_same_thread=False"))


# 先创建一个SQLModel模型,详细请参考: https://sqlmodel.tiangolo.com/
class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    name: str = Field("", title="CategoryName")
    description: str = Field(default="", title="Description")


# 注册ModelAdmin
@site.register_admin
class CategoryAdmin(admin.ModelAdmin):
    page_schema = "Category"
    # 配置管理模型
    model = Category
    display_item_action_as_column = True


# 挂载后台管理系统
site.mount_app(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
