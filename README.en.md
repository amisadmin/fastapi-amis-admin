[简体中文](https://github.com/amisadmin/fastapi_amis_admin) | [English](https://github.com/amisadmin/fastapi_amis_admin/blob/master/README.en.md)

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

`fastapi-amis-admini` is a high-performance and efficient framework based on `fastapi` & `amis` with `Python 3.7+`, and
based on standard Python type hints. The original intention of the development is to improve the application ecology and
to quickly generate a visual dashboard for the web application . According to the `Apache2.0` protocol, it is free and
open source . But in order to better operate and maintain this project in the long run, I very much hope to get
everyone's sponsorship and support.

## Features

- **High performance**: Based on [FastAPI](https://fastapi.tiangolo.com/zh/). Enjoy all the benefits.
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

- [Fastapi](https://fastapi.tiangolo.com/): Finish the web part.
- [SQLModel](https://sqlmodel.tiangolo.com/): Finish `ORM` model mapping. Perfectly
  combine  [SQLAlchemy](https://www.sqlalchemy.org/) with [Pydantic](https://pydantic-docs.helpmanual.io/), and have all
  their features .
- [Amis](https://baidu.gitee.io/amis): Finish admin page presentation.

## Composition

`fastapi-amis-admin` consists of three core modules, of which, `amis`, `fastapi-sqlmodel-crud` can be used as separate
modules, `amis_admin` is developed by the former.

- `amis`: Based on the `pydantic` data model building library of `baidu amis`. To generate/parse data rapidly.
- `fastapi-sqlmodel-crud`: Based on `FastAPI` &`SQLModel`. To quickly build Create, Read, Update, Delete common API
  interface .
- `amis_admin`: Inspired by `Django-Admin`. Combine `amis` with `fastapi-sqlmodel-crud`. To quickly build Web Admin
  dashboard .

## Installation

```bash
pip install fastapi_amis_admin
```

## Simple Example

```python
from fastapi import FastAPI
from fastapi_amis_admin.amis_admin.settings import Settings
from fastapi_amis_admin.amis_admin.site import AdminSite

# create FastAPI application
app = FastAPI()

# create AdminSite instance
site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///admisadmin.db'))

# mount AdminSite instance
site.mount_app(app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, debug=True)
```

## ModelAdmin Example

```python
from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi_amis_admin.amis_admin.settings import Settings
from fastapi_amis_admin.amis_admin.site import AdminSite
from fastapi_amis_admin.amis_admin import admin
from fastapi_amis_admin.models.fields import Field

# create FastAPI application
app = FastAPI()

# create AdminSite instance
site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///admisadmin.db'))


# Create an SQLModel, see document for details: https://sqlmodel.tiangolo.com/
class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(title='CategoryName')
    description: str = Field(default='', title='Description')


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
    await site.create_db_and_tables()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, debug=True)
```

## FormAdmin Example

```python
from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from fastapi_amis_admin.amis.components import Form
from fastapi_amis_admin.amis_admin import admin
from fastapi_amis_admin.amis_admin.settings import Settings
from fastapi_amis_admin.amis_admin.site import AdminSite
from fastapi_amis_admin.crud.schema import BaseApiOut
from fastapi_amis_admin.models.fields import Field

# create FastAPI application
app = FastAPI()

# create AdminSite instance
site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///admisadmin.db'))


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

    uvicorn.run(app, debug=True)
```

## Preview

- Open `http://127.0.0.1:8000/admin/` in your browser:

![ModelAdmin](https://raw.githubusercontent.com/amisadmin/fastapi_amis_admin_demo/master/upload/img/ModelAdmin.png)

- Open `http://127.0.0.1:8000/admin/docs` in your browser:

![Docs](https://raw.githubusercontent.com/amisadmin/fastapi_amis_admin_demo/master/upload/img/Docs.png)

## Future

- [ ] Fix bug and improve details.
- [ ] Improve the user tutorial documentation.
- [ ] Expand and improve core functions continuously .
- [ ] Add user authentication and authorization system.

## License

- According to the `Apache2.0` protocol, `fastapi-amis-admin` is free and open source. It can be used for commercial for
  free, but please clearly display copyright information about `FastAPI-Amis-Admin` on the display interface.

