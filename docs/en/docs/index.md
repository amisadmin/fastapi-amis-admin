[简体中文](https://github.com/amisadmin/fastapi_amis_admin/blob/master/README.zh.md)
| [English](https://github.com/amisadmin/fastapi_amis_admin)

# Introduction

<h2 align="center">
  FastAPI-Amis-Admin
</h2>
<p align="center">
    <em>fastapi-amis-admin is a high-performance, efficient and easily extensible FastAPI admin framework.</em><br/>
    <em>Inspired by Django-admin, and has as many powerful functions as Django-admin.</em>
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
</p>
<p align="center">
  <a href="https://github.com/amisadmin/fastapi_amis_admin" target="_blank">source code</a>
  ·
  <a href="http://demo.amis.work/admin" target="_blank">online demo</a>
  ·
  <a href="http://docs.gh.amis.work" target="_blank">documentation</a>
  ·
  <a href="http://docs.amis.work" target="_blank">can't open the document?</a>
</p>


------

`fastapi-amis-admin` is a high-performance and efficient framework based on `fastapi` & `amis` with `Python 3.7+`, and
based on standard Python type hints. The original intention of the development is to improve the application ecology and
to quickly generate a visual dashboard for the web application . According to the `Apache2.0` protocol, it is free and
open source . But in order to better operate and maintain this project in the long run, I very much hope to get
everyone's sponsorship and support.

## Features

- **High performance**: Based on [FastAPI](https://fastapi.tiangolo.com/). Enjoy all the benefits.
- **High efficiency**: Perfect code type hints. Higher code reusability.
- **Support asynchronous and synchronous hybrid writing**: `ORM`  is based on`SQLModel` & `Sqlalchemy`. Freely customize
  database type. Support synchronous and asynchronous mode. Strong scalability.
- **Front-end separation**: The front-end is rendered by `Amis`, the back-end interface is automatically generated
  by `fastapi-amis-admin`. The interface is reusable.
- **Strong scalability**: The background page supports `Amis` pages and ordinary `html` pages. Easily customize the
  interface freely.
- **Automatic api documentation**: Automatically generate Interface documentation by `FastAPI`. Easily debug and share
  interfaces.

## Dependencies

- [FastAPI](https://fastapi.tiangolo.com/): Finish the web part.
- [SQLModel](https://sqlmodel.tiangolo.com/): Finish `ORM` model mapping. Perfectly
  combine  [SQLAlchemy](https://www.sqlalchemy.org/) with [Pydantic](https://pydantic-docs.helpmanual.io/), and have all
  their features .
- [Amis](https://baidu.gitee.io/amis): Finish admin page presentation.

## Composition

`fastapi-amis-admin` consists of three core modules, of which, `amis`, `crud` can be used as separate
modules, `admin` is developed by the former.

- `amis`: Based on the `pydantic` data model building library of `baidu amis`. To generate/parse data rapidly.
- `crud`: Based on `FastAPI` &`Sqlalchemy`. To quickly build Create, Read, Update, Delete common API
  interface .
- `admin`: Inspired by `Django-Admin`. Combine `amis` with `crud`. To quickly build Web Admin
  dashboard .

## Installation

```bash
pip install fastapi_amis_admin
```

### Note

- `sqlmodel` currently does not support `sqlalchemy 2.0+`. If you use `sqlalchemy 2.0+` to create a model, you cannot
  use `sqlmodel` at the same time.
- After version `fastapi-amis-admin>=0.6.0`, `sqlmodel` is no longer a required dependency library. If you use `sqlmodel`
  to create a model, you can install it with the following command.

```bash
pip install fastapi_amis_admin[sqlmodel]
```

## Simple Example

```python
from fastapi import FastAPI
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite

# create FastAPI application
app = FastAPI()

# create AdminSite instance
site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///amisadmin.db'))

# mount AdminSite instance
site.mount_app(app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
```

## ModelAdmin Example

### Create Model

- Support `SQLModel` model, `SQLAlchemy` model, `SQLAlchemy 2.0` model
- Method 1: Create model through `SQLModel`.

```python
from sqlmodel import SQLModel
from fastapi_amis_admin.models.fields import Field


class Base(SQLModel):
    pass


# Create an SQLModel, see document for details: https://sqlmodel.tiangolo.com/
class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(title='CategoryName', max_length=100, unique=True, index=True, nullable=False)
    description: str = Field(default='', title='Description', max_length=255)

```

- Method 2: Create model through `SQLAlchemy`.

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Create an SQLAlchemy model, see document for details: https://docs.sqlalchemy.org/en/14/orm/tutorial.html
class Category(Base):
    __tablename__ = 'category'
    # Specify the Schema class corresponding to the model. It is recommended to specify it. If omitted, it can be automatically generated.
    __pydantic_model__ = CategorySchema

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(255), default='')
```

- Method 3: Create model through `SQLAlchemy 2.0`.

```python
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


# Create an SQLAlchemy 2.0 model, see document for details: https://docs.sqlalchemy.org/en/20/orm/quickstart.html
class Category(Base):
    __tablename__ = "category"
    # Specify the Schema class corresponding to the model. It is recommended to specify it. If omitted, it can be automatically generated.
    __pydantic_model__ = CategorySchema

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), default="")
```

- If you create a model through `sqlalchemy`, it is recommended to create a corresponding pydantic model at the same
  time, and set `orm_mode=True`.

```python
from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    id: int = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(title="CategoryName")
    description: str = Field(default="", title="CategoryDescription")

    class Config:
        orm_mode = True
```

### Register ModelAdmin

```python
from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_amis_admin.admin import admin

# create FastAPI application
app = FastAPI()

# create AdminSite instance
site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///amisadmin.db'))


# register ModelAdmin
@site.register_admin
class CategoryAdmin(admin.ModelAdmin):
    page_schema = 'Category'
    # set model
    model = Category


# mount AdminSite instance
site.mount_app(app)


# create initial database table
@app.on_event("startup")
async def startup():
    await site.db.async_run_sync(Base.metadata.create_all, is_session=False)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
```

## FormAdmin Example

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

# create FastAPI application
app = FastAPI()

# create AdminSite instance
site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///amisadmin.db'))


# register FormAdmin
@site.register_admin
class UserLoginFormAdmin(admin.FormAdmin):
    page_schema = 'UserLoginForm'
    # set form information, optional
    form = Form(title='This is a test login form', submitText='login')

    # create form schema
    class schema(BaseModel):
        username: str = Field(..., title='username', min_length=3, max_length=30)
        password: str = Field(..., title='password')

    # handle form submission data
    async def handle(self, request: Request, data: BaseModel, **kwargs) -> BaseApiOut[Any]:
        if data.username == 'amisadmin' and data.password == 'amisadmin':
            return BaseApiOut(msg='Login successfully!', data={'token': 'xxxxxx'})
        return BaseApiOut(status=-1, msg='Incorrect username or password!')


# mount AdminSite instance
site.mount_app(app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
```

## Working with Command

```bash
# Install command line extension
pip install fastapi_amis_admin[cli]

# View help
faa --help

# Initialize a `FastAPI-Amis-Admin` project
faa new project_name --init

# Initialize a `FastAPI-Amis-Admin` application
faa new app_name

# Fast running project
faa run
```

## Preview

- Open `http://127.0.0.1:8000/admin/` in your browser:

![ModelAdmin](https://s2.loli.net/2022/03/20/ItgFYGUONm1jCz5.png)

- Open `http://127.0.0.1:8000/admin/docs` in your browser:

![Docs](https://s2.loli.net/2022/03/20/1GcCiPdmXayxrbH.png)

## Project

- [`Amis-Admin-Theme-Editor`](https://github.com/swelcker/amis-admin-theme-editor):Theme-Editor for the fastapi-amis-admin.
  Allows to add custom css styles and to apply theme --vars change on the fly.
- [`FastAPI-User-Auth`](https://github.com/amisadmin/fastapi_user_auth): A simple and powerful `FastAPI` user `RBAC`
  authentication and authorization library.
- [`FastAPI-Scheduler`](https://github.com/amisadmin/fastapi_scheduler): A simple scheduled task management `FastAPI` extension
  based on `APScheduler`.
- [`FastAPI-Config`](https://github.com/amisadmin/fastapi-config): A visual dynamic configuration management extension package based on `FastAPI-Amis-Admin`.
- [`FastAPI-Amis-Admin-Demo`](https://github.com/amisadmin/fastapi_amis_admin_demo): An example `FastAPI-Amis-Admin` application.
- [`FastAPI-User-Auth-Demo`](https://github.com/amisadmin/fastapi_user_auth_demo): An example `FastAPI-User-Auth` application.

## License

- According to the `Apache2.0` protocol, `fastapi-amis-admin` is free and open source. It can be used for commercial for
  free, but please clearly display copyright information about `FastAPI-Amis-Admin` on the display interface.