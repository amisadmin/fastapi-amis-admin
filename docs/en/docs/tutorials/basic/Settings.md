# Site configuration

`AdminSite` in the creation of the instance, receive `settings`, `fastapi`, `engine` three basic parameters. Through these three basic parameters, you can already meet most of the custom configuration needs. If you need more personalized configuration, you can inherit the `AdminSite` class for more rich configuration.

## Basic configuration

`settings` receives a `Settings` object, which can be configured whether the current site is open for debugging, mount path, database connection, CDN address, Amis version number and so on.

- Reference: [Settings](/amis_admin/Settings/)

## FastAPI application

The `AdminSite` object maintains a `fastapi` application object inside, which you can configure through the `fastapi` parameter:

- whether to enable debugging
- api document path
- Start/stop application events
- Registering dependencies
- Other FastAPI configurations, refer to: [FastAPI](https://fastapi.tiangolo.com/zh/tutorial/metadata/?h=docs_url#urls)

## Database configuration

The `AdminSite` object also maintains an internal `sqlalchemy` asynchronous client, and you can provide a custom asynchronous database engine via the `engine` parameter.

## Example-1

```python
from fastapi import FastAPI
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite

site = AdminSite(
    # Basic configuration
    settings=Settings(debug=True, database_url_async='sqlite+aiosqlite:///amisadmin.db'),
    # fastapi related configuration
    fastapi=FastAPI(debug=True, docs_url='/admin_docs', redoc_url='/admin_redoc')
)
```

## Customizing the admin site

Admin site rewriting can achieve very free and rich site configuration, such as changing the backend interface template, adding/removing default administrative classes or administrative applications, changing static resource links, etc..

### Example-2

```python
from fastapi import FastAPI, Request
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite, ReDocsAdmin, DocsAdmin
from sqlalchemy.ext.asyncio import AsyncEngine
from fastapi_amis_admin.amis.components import App


# Custom backend administration site
class NewAdminSite(AdminSite):
    # custom application template, copy the original template file to modify the original path: fastapi_amis_admin/amis/templates/app.html
    template_name = '/templates/new_app.html'

    def __init__(self, settings: Settings, fastapi: FastAPI = None, engine: AsyncEngine = None):
        super(). __init__(settings, fastapi, engine)
        # Unregister the default admin class
        self.unregister_admin(DocsAdmin, ReDocsAdmin)

    async def get_page(self, request: Request) -> App:
        app = await super().get_page(request)
        # Custom site name, logo information, reference: https://baidu.gitee.io/amis/zh-CN/components/app
        app.brandName = 'MyAdminSite'
        app.logo = 'https://baidu.gitee.io/amis/static/logo_408c434.png'
        return app


# Create a backend management system instance with a custom admin site class
site = NewAdminSite(settings=Settings(debug=True, database_url_async='sqlite+aiosqlite:///amisadmin.db'))
```

- By modifying the `template_name` field, you can customize the backend interface template. For example: modify the static resource link to speed up web access, modify the backend display style.

!!! note annotate "About customizing the admin site"

    Admin site inheritance rewrite is an advanced feature, it is recommended to rewrite only if you know enough about fastapi_amis_admin.
    
    You are free to modify the backend administration interface, but please respect the development achievements of fastapi_amis_admin team and show the copyright information about FastAPI-Amis-Admin clearly in the display interface.

