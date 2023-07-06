# User Authentication

`FastAPI-Amis-Admin` provides simple and powerful user `RBAC` authentication and authorization for the system in the form of application plug-ins.

Project address: [FastAPI-User-Auth](https://github.com/amisadmin/fastapi_user_auth), more tutorial documents and usage examples are being added continuously,

Welcome to join the Q group [229036692](https://jq.qq.com/?_wv=1027&k=U4Dv6x8W) to study and discuss together.

## Install

```bash
pip install fastapi-user-auth
```

## Simple example

```python linenums="1" hl_lines="3 9 10 11 14"
from fastapi import FastAPI
from fastapi_amis_admin.admin import Settings
from fastapi_user_auth.site import AuthAdminSite

# Create FastAPI application
app = FastAPI()

# Create AdminSite instance
site = AuthAdminSite(
    settings=Settings(database_url_async='sqlite+aiosqlite:///amisadmin.db')
)
auth = site.auth
# Mount the background management system
site.mount_app(app)

# Create initialized database table
@app.on_event("startup")
async def startup():
    await site.db.async_run_sync(SQLModel.metadata.create_all,is_session=False)
    # Create a default test user, please change the password in time!!!
    await auth.create_role_user('admin')
    await auth.create_role_user('vip')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
```

!!! note "About `AuthAdminSite`"

	- AuthAdminSite is a default authorization management site class encapsulated by FastAPI-User-Auth, which requires users to be logged in.
	- Admin objects registered through AuthAdminSite have the same default permissions (ie: users must also be logged in).
	- You can upgrade or downgrade the default permission requirements by overriding the `has_page_permission` method.

## Example-1

Requirements: There is an existing user management application. On the basis of requiring user login, it is also required that the currently logged in user is an administrator, and other non-administrator users are prohibited from operating.

```python hl_lines="4"
class UserAuthApp(AdminApp):
    async def has_page_permission(self, request: Request) -> bool:
        return  await request.auth.requires(roles='admin', response=False)(request)
```

## Example-2

Requirements: Under the user management application in the above example, the user login/registration form management object is included, and this part of the route does not require the user to be logged in.

```python  hl_lines="3"
class UserLoginFormAdmin(FormAdmin):
    async def has_page_permission(self, request: Request) -> bool:
        return True
```

## Example-3

Requirements: There is a `ModelAdmin` article model management, the permission requirements are as follows:

- All articles are made public and can be viewed without user login.
- The user is not logged in, cannot filter articles by title, and can only view up to 10 pieces of data per page.
- The user is logged in and the registration time is more than 3 days before publishing articles.
- The user is logged in and can only modify his own articles, and cannot be modified in batches.
- Administrators can modify all articles, and can modify them in batches.
- You must be an administrator to delete articles.

```python linenums="1" hl_lines="32 33 41 42 49 60 65"
class ArticleAdmin(admin.ModelAdmin):
    page_schema = PageSchema(label='article management', icon='fa fa-file')
    model = Article
    # Configure list display fields
    list_display = [Article.id, Article.title, Article.img, Article.status,
                    Category.name, User.username,
                    TableColumn(type='tpl', label='custom template column',
                                tpl='<a href="${source}" target="_blank">ID:${id},Title:${title}</a>'),
                    Article.create_time, Article.description,
                    ]
    # Configure fuzzy search fields
    search_fields = [Article.title, Category.name, User.username]
    # Configure the associated model
    link_model_fields = [Article.tags]

    # custom query selector
    async def get_select(self, request: Request) -> Select:
        sel = await super().get_select(request)
        return sel.join(Category, isouter=True).join(User, isouter=True)

    # ASD
    async def has_page_permission(self, request: Request) -> bool:
        return True

    async def has_list_permission(
            self, request: Request, paginator: Paginator,
            filter: BaseModel = None, **kwargs
    ) -> bool:
        # The user is not logged in, cannot filter articles by title, and can only view up to 10 pieces of data per page.
        return bool(
            await self.site.auth.requires(response=False)(request)
            or (paginator.perPage <= 10 and filter.title == '')
        )

    async def has_create_permission(
            self, request: Request, data: BaseModel, **kwargs
    ) -> bool:
        # The user is logged in and the registration time is greater than 3 days before they can publish articles; or the admin role
        return bool(
            await self.site.auth.requires(response=False)(request)
            and request.user.create_time < datetime.now() - timedelta(days=3)
        ) or await self.site.auth.requires(roles='admin', response=False)(request)

    async def has_delete_permission(
            self, request: Request, item_id: List[str], **kwargs
    ) -> bool:
        # You must be an administrator to delete articles.
        return await self.site.auth.requires(roles='admin', response=False)(request)

    async def has_update_permission(
            self, request: Request, item_id: List[str], 
        	data: BaseModel, **kwargs
    ) -> bool:
        if await self.site.auth.requires(response=False)(request):
            if item_id is None:
                return True
            async with self.site.db.session_maker() as session:
                # Administrators can modify all articles, and can modify them in batches.
                if await request.user.has_role(['admin'], session):
                    return True
                # Non-administrators can only modify their own articles, and cannot modify them in batches.
                result = await session.execute(
                    select(Article.id).where(
                        Article.id == item_id[0], Article.user_id == request.user.id
                    ).limit(1)
                )
            if result.first():
                return True
        return False

    async def on_create_pre(
            self, request: Request, obj: BaseModel, **kwargs
    ) -> Dict[str, Any]:
        data = await super().on_create_pre(request, obj, **kwargs)
        # When creating a new article, set the current user as the publisher
        data['user_id'] = request.user.id
        return data
```

## Interface preview

- Open `http://127.0.0.1:8000/admin/auth/form/login` in your browser:

![Login](https://s2.loli.net/2022/03/20/SZy6sjaVlBT8gin.png)

- Open `http://127.0.0.1:8000/admin/` in your browser:

![ModelAdmin](https://s2.loli.net/2022/03/20/ItgFYGUONm1jCz5.png)

- Open `http://127.0.0.1:8000/admin/docs` in your browser:

![Docs](https://s2.loli.net/2022/03/20/1GcCiPdmXayxrbH.png)
