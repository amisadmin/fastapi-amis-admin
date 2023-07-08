[简体中文](https://github.com/amisadmin/fastapi_amis_admin/blob/master/README.zh.md)
| [English](https://github.com/amisadmin/fastapi_amis_admin)

# 项目介绍

<h2 align="center">
  FastAPI-Amis-Admin
</h2>
<p align="center">
    <em>fastapi-amis-admin是一个拥有高性能,高效率,易拓展的fastapi管理后台框架.</em><br/>
    <em>启发自Django-Admin,并且拥有不逊色于Django-Admin的强大功能.</em>
</p>
<p align="center">
    <a href="https://github.com/amisadmin/fastapi_amis_admin/actions/workflows/pytest.yml" target="_blank">
        <img src="https://github.com/amisadmin/fastapi_amis_admin/actions/workflows/pytest.yml/badge.svg" alt="Pytest">
    </a>
    <a href="https://pypi.org/project/fastapi_amis_admin" target="_blank">
        <img src="https://badgen.net/pypi/v/fastapi-amis-admin?color=blue" alt="Package version">
    </a>
    <a href="https://pepy.tech/project/fastapi-amis-admin" target="_blank">
        <img src="https://pepy.tech/badge/fastapi-amis-admin" alt="Downloads">
    </a>
    <a href="https://gitter.im/amisadmin/fastapi-amis-admin">
        <img src="https://badges.gitter.im/amisadmin/fastapi-amis-admin.svg" alt="Chat on Gitter"/>
    </a>
    <a href="https://jq.qq.com/?_wv=1027&k=U4Dv6x8W" target="_blank">
        <img src="https://badgen.net/badge/qq%E7%BE%A4/229036692/orange" alt="229036692">
    </a>
</p>
<p align="center">
  <a href="https://github.com/amisadmin/fastapi_amis_admin" target="_blank">源码</a>
  ·
  <a href="http://demo.amis.work/admin" target="_blank">在线演示</a>
  ·
  <a href="http://docs.amis.work" target="_blank">文档</a>
  ·
  <a href="http://docs.gh.amis.work" target="_blank">文档打不开？</a>
</p>



------

`fastapi-amis-admin`是一个基于`fastapi`+`amis`开发的高性能并且高效率 `web-admin` 框架，使用 Python 3.7+ 并基于标准的 Python 类型提示.
`fastapi-amis-admin`开发的初衷是为了完善`fastapi`应用生态, 为`fastapi` web应用程序快速生成一个可视化管理后台.

## 关键特性

- **性能极高**：基于[FastAPI](https://fastapi.tiangolo.com/zh/), 可享受`FastAPI`的全部优势.

- **效率更快**：完善的编码类型提示, 代码可重用性更高.

- **支持异步和同步混合编写**: `ORM`基于`SQLModel`+`Sqlalchemy`, 可自由定制数据库类型, 支持同步及异步模式, 可拓展性强.

- **前后端分离**: 前端由`Amis`渲染, 后端接口由`fastapi-amis-admin`自动生成, 接口可重复利用.

- **可拓展性强**: 后台页面支持`Amis`页面及普通`html`页面,开发者可以很方便的自由定制界面.

- **自动生成API文档**: 由`FastAPI`自动生成接口文档,方便开发者调试,以及接口分享.

## 核心依赖

- [FastAPI](https://fastapi.tiangolo.com) 负责 web 部分
- [SQLModel](https://sqlmodel.tiangolo.com/) 负责ORM模型映射(
  完美结合[SQLAlchemy](https://www.sqlalchemy.org/)+[Pydantic](https://pydantic-docs.helpmanual.io/), 拥有`SQLAlchemy`
  和`Pydantic`的所有功能)
- [Amis](https://baidu.gitee.io/amis) 负责Admin后台页面展示

## 项目组成

`fastapi-amis-admin`由三部分核心模块组成,其中`amis`, `crud` 可作为独立模块单独使用,`admin`基于前者共同构建.

- `amis`: 基于`baidu amis`的`pydantic`数据模型构建库,用于快速生成/解析`amis` `json` 数据.
- `crud`: 基于`FastAPI`+`Sqlalchemy`, 用于快速构建Create,Read,Update,Delete通用API接口.
- `admin`: 启发自`Django-Admin`, 结合`amis`+`crud`, 用于快速构建`Web Admin`管理后台.

## 安装

```bash
pip install fastapi_amis_admin
```

### 注意

- `sqlmodel`目前暂不支持`sqlalchemy 2.0+`, 如果你使用`sqlalchemy 2.0+`创建模型, 则不可同时使用`sqlmodel`.
- `fastapi-amis-admin>=0.6.0`版本以后,`sqlmodel`不再是必须依赖库,如果你使用`sqlmodel`创建模型, 可以通过以下命令安装.

```bash
pip install fastapi_amis_admin[sqlmodel]
``` 

## 简单示例

```python
from fastapi import FastAPI
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite

# 创建FastAPI应用
app = FastAPI()

# 创建AdminSite实例
site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///amisadmin.db'))

# 挂载后台管理系统
site.mount_app(app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
```

## 模型管理示例

### 创建模型

- 支持`SQLModel`模型的、`SQLAlchemy`模型、`SQLAlchemy 2.0`模型
- 方式一: 通过`SQLModel`创建模型.

```python
from sqlmodel import SQLModel
from fastapi_amis_admin.models.fields import Field


class Base(SQLModel):
    pass


# 创建SQLModel模型,详细请参考: https://sqlmodel.tiangolo.com/
class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(title='CategoryName', max_length=100, unique=True, index=True, nullable=False)
    description: str = Field(default='', title='Description', max_length=255)

```

- 方式二: 通过`SQLAlchemy`创建模型.

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# 创建SQLAlchemy模型,详细请参考: https://docs.sqlalchemy.org/en/14/orm/tutorial.html
class Category(Base):
    __tablename__ = 'category'
    __pydantic_model__ = CategorySchema  # 指定模型对应的Schema类.省略可自动生成,但是建议指定.

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(255), default='')
```

- 方式三: 通过`SQLAlchemy 2.0`创建模型.

```python
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


# 创建SQLAlchemy 2.0模型,详细请参考: https://docs.sqlalchemy.org/en/20/orm/quickstart.html
class Category(Base):
    __tablename__ = "category"
    __pydantic_model__ = CategorySchema  # 指定模型对应的Schema类.省略可自动生成,但是建议指定.

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), default="")
```

- 如果你通过`sqlalchemy`创建模型,建议同时创建一个对应的pydantic模型,并且设置`orm_mode=True`.

```python
from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    id: int = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(title="CategoryName")
    description: str = Field(default="", title="CategoryDescription")

    class Config:
        orm_mode = True
```

### 注册模型管理

```python
from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_amis_admin.admin import admin

# 创建FastAPI应用
app = FastAPI()

# 创建AdminSite实例
site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///amisadmin.db'))


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
    await site.db.async_run_sync(Base.metadata.create_all, is_session=False)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
```

## 表单管理示例

```python
from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from fastapi_amis_admin.amis.components import Form
from fastapi_amis_admin.admin import admin
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_amis_admin.crud.schema import BaseApiOut
from fastapi_amis_admin.models.fields import Field

# 创建FastAPI应用
app = FastAPI()

# 创建AdminSite实例
site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///amisadmin.db'))


# 注册FormAdmin
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


# 挂载后台管理系统
site.mount_app(app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
```

## 使用命令行

```bash
# 安装命令行拓展
pip install fastapi_amis_admin[cli]

# 查看帮助
faa --help

# 初始化一个`FastAPI-Amis-Admin`项目
faa new project_name --init

# 初始化一个`FastAPI-Amis-Admin`应用
faa new app_name

# 快速运行项目
faa run
```

## 界面预览

- Open `http://127.0.0.1:8000/admin/` in your browser:

![ModelAdmin](https://s2.loli.net/2022/03/20/ItgFYGUONm1jCz5.png)

- Open `http://127.0.0.1:8000/admin/docs` in your browser:

![Docs](https://s2.loli.net/2022/03/20/1GcCiPdmXayxrbH.png)

## 相关项目

- [`Amis-Admin-Theme-Editor`](https://github.com/swelcker/amis-admin-theme-editor):`FastAPI-Amis-Admin`的主题编辑器。
  允许添加自定义css样式和应用主题,变量改变及时生效.
- [`FastAPI-User-Auth`](https://github.com/amisadmin/fastapi_user_auth): 一个简单而强大的`FastAPI`用户`RBAC`认证与授权库.
- [`FastAPI-Scheduler`](https://github.com/amisadmin/fastapi_scheduler): 一个基于`APScheduler`的简单定时任务管理`FastAPI`拓展库.
- [`FastAPI-Config`](https://github.com/amisadmin/fastapi-config): 一个基于`FastAPI-Amis-Admin`的可视化动态配置管理拓展包.
- [`FastAPI-Amis-Admin-Demo`](https://github.com/amisadmin/fastapi_amis_admin_demo):  一个`FastAPI-Amis-Admin` 应用程序示例.
- [`FastAPI-User-Auth-Demo`](https://github.com/amisadmin/fastapi_user_auth_demo): 一个`FastAPI-User-Auth` 应用程序示例.

## 许可协议

- `fastapi-amis-admin`基于`Apache2.0`开源免费使用，可以免费用于商业用途，但请在展示界面中明确显示关于FastAPI-Amis-Admin的版权信息.

## 鸣谢

感谢以下开发者对 FastAPI-Amis-Admin 作出的贡献：

<a href="https://github.com/amisadmin/fastapi_amis_admin/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=amisadmin/fastapi_amis_admin" />
</a>