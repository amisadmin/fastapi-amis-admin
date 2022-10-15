# Inheritance override

The inheritance and rewriting of classes in fastapi-amis-admin is very extensive. Skilled application of inheritance and rewriting will make your code more concise and easier to extend.

- The usual admin pages inherit from the default admin classes, such as: `IframeAdmin`, `PageAdmin`, `ModelAdmin`, `FormAdmin`, `AdminApp`, etc.
- The management page inherited from the default management class can also be inherited twice or multiple times.

## Example-1 (custom home page)

```python linenums="1" hl_lines="4 9"
from fastapi_amis_admin import admin

# Cancel the default home page
site.unregister_admin(admin.HomeAdmin)


# Register custom homepage
@site.register_admin
class MyHomeAdmin(admin.HomeAdmin):

    async def get_page(self, request: Request) -> Page:
        # Get the default page
        page = await super().get_page(request)
        # custom modification
        page.body.title = 'MyHome'
        ...
        return page
```

## Example-2 (custom template management base class)

```python linenums="1" hl_lines="6 7 11 20"
import datetime

from fastapi_amis_admin import admin, amis


class MyJinja2Admin(admin.TemplateAdmin):
    templates: Jinja2Templates = Jinja2Templates(directory='apps/demo/templates')


@site.register_admin
class SimpleTemplateAdmin(MyJinja2Admin):
    page_schema = amis.PageSchema(label='Jinja2', icon='fa fa-link')
    template_name = 'simple.html'

    async def get_page(self, request: Request) -> Dict[str, Any]:
        return {'current_time': datetime.datetime.now()}


@site.register_admin
class ElementTemplateAdmin(MyJinja2Admin):
    page_schema = amis.PageSchema(label='ElementUI', icon='fa fa-link')
    template_name = 'element.html'

```

## Example-3 (reuse model management class)

```python linenums="1" hl_lines="32"
from fastapi_amis_admin import admin
from fastapi_amis_admin.models.fields import Field


# Create a SQLModel model, please refer to: https://sqlmodel.tiangolo.com/
class Article(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    title: str = Field(title='ArticleTitle', max_length=200)
    description: Optional[str] = Field(default='', title='ArticleDescription', max_length=400)
    status: bool = Field(None, title='status')
    content: str = Field(title='ArticleContent')
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", title='CategoryId')
    is_active: bool = False


@site.register_admin
class ArticleAdmin(admin.ModelAdmin):
    page_schema = 'article management'
    model = Article
    # Set the fields to display
    list_display = [Article.id, Article.title, Article.description, Article.status, Category.name]
    # Set up fuzzy search field
    search_fields = [Article.title, Category.name]

    # custom base selector
    async def get_select(self, request: Request) -> Select:
        stmt = await super().get_select(request)
        return stmt.outerjoin(Category, Article.category_id == Category.id)


@site.register_admin
class ActiveArticle(ArticleAdmin):
    """Inheritance and reuse of `ArticleAdmin`; this example is relatively simple, the actual application may be more complex."""

    # custom route prefix
    router_prefix = '/article.active'

    # Override the base selector
    async def get_select(self, request: Request) -> Select:
        stmt = await super().get_select(request)
        return stmt.where(Article.is_active == True)
```

## Example-4 (custom management application)

参考: [fastapi_user_auth.UserAuthApp](https://github.com/amisadmin/fastapi_user_auth/blob/9a7c30f5f562543c376fd0235091666547fb175d/fastapi_user_auth/app.py#L14)

## Example-5 (custom admin site)

Reference: [Basic Tutorial->Site Configuration->Custom Management Site](/tutorials/basic/Settings/#_4)

参考: [fastapi_user_auth.AuthAdminSite](https://github.com/amisadmin/fastapi_user_auth/blob/9a7c30f5f562543c376fd0235091666547fb175d/fastapi_user_auth/site.py#L16)
