from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi_amis_admin.amis_admin.settings import Settings
from fastapi_amis_admin.amis_admin.site import AdminSite
from fastapi_amis_admin.amis_admin import admin
from fastapi_amis_admin.models.fields import Field

# 创建FastAPI应用
app = FastAPI()

# 创建AdminSite实例
site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///admisadmin.db'))


# 先创建一个SQLModel模型,详细请参考: https://sqlmodel.tiangolo.com/
class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(title='CategoryName')
    description: str = Field(default='', title='Description')


# 注册ModelAdmin
@site.register_admin
class CategoryAdmin(admin.ModelAdmin):
    page_schema = '分类管理'
    # 配置管理模型
    model = Category


# 挂载后台管理系统
site.mount_app(app)


# 创建初始化数据库表
@app.on_event("startup")
async def startup():
    await site.create_db_and_tables()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, debug=True)
