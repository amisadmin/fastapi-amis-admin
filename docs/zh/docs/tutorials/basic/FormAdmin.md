# 表单管理

`FormAdmin`实现在菜单列表显示一个菜单.点击菜单后将展现一个`amis`表单页面.

## 示例

```python
from fastapi_amis_admin.admin import admin
from fastapi_amis_admin.crud import BaseApiOut
from fastapi_amis_admin.models.fields import Field
from pydantic import BaseModel
from starlette.requests import Request


@site.register_admin
class UserLoginFormAdmin(admin.FormAdmin):
    page_schema = 'UserLoginForm'
    # 配置表单信息, 可省略
    form = Form(title='这是一个测试登录表单', submitText='登录')

    # 创建表单数据模型
    class schema(BaseModel):
        username: str = Field(..., title='用户名', min_length=3, max_length=30)
        password: str = Field(..., title='密码')

    # 处理表单提交数据
    async def handle(self, request: Request, data: BaseModel, **kwargs) -> BaseApiOut[Any]:
        if data.username == 'amisadmin' and data.password == 'amisadmin':
            return BaseApiOut(msg='登录成功!', data={'token': 'xxxxxx'})
        return BaseApiOut(status=-1, msg='用户名或密码错误!')
```

这里展示的仅仅是一个最简单基础的功能.

## 表单对象

类字段`form`可以配置表单的基本信息,例如:
标题,表单样式,提交按钮,提交API,信息提示等等.请参考: [Form 表单](https://baidu.gitee.io/amis/zh-CN/components/form/index)

## 表单数据模型

类字段`schema`定义表单数据模型,它继承自 `pydantic BaseModel`, 支持各种类型字段, 通过`amis`自动在前端解析成对应的组件.通过`schema`
可以完成的功能有:

- 定义字段基本属性. 例如: 名称,标签,数据类型,基本限制
- 自定义字段处理或验证器. 参考: [Validators - pydantic](https://pydantic-docs.helpmanual.io/usage/validators/)

- 自定义`amis`组件.可通过`amis_form_item`自定义`amis`组件

## 处理函数

类方法`handle`接收用户提交的表单数据,在这里你可以进行各种复杂的表单数据逻辑处理.

## 更多用法

实际上`FormAdmin`拥有更多复杂的使用,这里无法展开详细说明,请参考以下相关资料.

### 相关文档

- [FormAdmin](/amis_admin/FormAdmin/)

