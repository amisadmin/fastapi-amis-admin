from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request

from fastapi_amis_admin.admin import admin
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_amis_admin.amis.components import Form
from fastapi_amis_admin.crud.schema import BaseApiOut
from fastapi_amis_admin.models.fields import Field

# 创建FastAPI应用
app = FastAPI()

# 创建AdminSite实例
site = AdminSite(settings=Settings(database_url_async="sqlite+aiosqlite:///amisadmin.db", language="zh_CN"))


# 注册FormAdmin
@site.register_admin
class UserLoginFormAdmin(admin.FormAdmin):
    page_schema = "用户登录表单"
    # 配置表单信息, 可省略
    form = Form(title="这是一个测试登录表单", submitText="登录")

    # 创建表单数据模型
    class schema(BaseModel):
        username: str = Field(..., title="用户名", min_length=3, max_length=30)
        password: str = Field(..., title="密码")

    # 处理表单提交数据
    async def handle(self, request: Request, data: BaseModel, **kwargs) -> BaseApiOut[Any]:
        if data.username == "amisadmin" and data.password == "amisadmin":
            return BaseApiOut(msg="登录成功!", data={"token": "xxxxxx"})
        return BaseApiOut(status=-1, msg="用户名或密码错误!")


# 挂载后台管理系统
site.mount_app(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
