# Quick start

## Install

```bash
pip install fastapi_amis_admin
```

## Simple example

1. Create the file **`adminsite.py`**:

```python
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_amis_admin.admin import admin
from fastapi_amis_admin.amis.components import PageSchema

# Create AdminSite instance
site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///amisadmin.db'))


# Registration management class
@site.register_admin
class GitHubIframeAdmin(admin.IframeAdmin):
    # Set page menu information
    page_schema = PageSchema(label='AmisIframeAdmin', icon='fa fa-github')
    # Set the jump link
    src = 'https://github.com/amisadmin/fastapi_amis_admin'
```

2. Create the file **`main.py`**:

```python
from fastapi import FastAPI
from adminsite import site

app = FastAPI()

# Mount the background management system
site.mount_app(app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
```

## Run the program

```bash
uvicorn main:app
```

## Interface preview

- Open a browser to access: `http://127.0.0.1:8000/admin/`

## Smple program

- [`FastAPI-Amis-Admin-Demo`](https://github.com/amisadmin/fastapi_amis_admin_demo): A sample `FastAPI-Amis-Admin` application.
- [`FastAPI-User-Auth-Demo`](https://github.com/amisadmin/fastapi_user_auth_demo): A sample `FastAPI-User-Auth` application.

## Related Items

- [`FastAPI-User-Auth`](https://github.com/amisadmin/fastapi_user_auth): A simple and powerful `FastAPI` user `RBAC` authentication and authorization library.
- [`FastAPI-Scheduler`](https://github.com/amisadmin/fastapi_scheduler): A simple scheduled task management project based on `FastAPI`+`APScheduler`.

## More features

- API reference documentation: [API Reference](../../amis_admin/BaseAdmin)