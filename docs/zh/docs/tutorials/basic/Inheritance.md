# 继承重写

在fastapi-amis-admin中类的继承和重写非常广泛,熟练的应用继承重写将让你的代码更简洁,更易于拓展.

- 通常的管理页面继承自默认管理类,例如:`IframeAdmin`,`PageAdmin`,`ModelAdmin`,`FormAdmin`,`AdminApp`等.
- 继承自默认管理类的管理页面,也可以被二次或多次继承.

## 示例-1(自定义首页)

```python linenums="1" hl_lines="4 9"
from fastapi_amis_admin import admin

# 取消默认首页
site.unregister_admin(admin.HomeAdmin)


# 注册自定义首页
@site.register_admin
class MyHomeAdmin(admin.HomeAdmin):

    async def get_page(self, request: Request) -> Page:
        # 获取默认页面
        page = await super().get_page(request)
        # 自定义修改
        page.body.title = 'MyHome'
        ...
        return page
```

## 示例-2(自定义模板管理基类)

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

## 示例-3(重用模型管理类)

```python linenums="1" hl_lines="32"
from fastapi_amis_admin import admin
from fastapi_amis_admin.models.fields import Field


# 创建一个SQLModel模型,详细请参考: https://sqlmodel.tiangolo.com/
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
    page_schema = '文章管理'
    model = Article
    # 设置需要展示的字段
    list_display = [Article.id, Article.title, Article.description, Article.status, Category.name]
    # 设置模糊搜索字段
    search_fields = [Article.title, Category.name]

    # 自定义基础选择器
    async def get_select(self, request: Request) -> Select:
        stmt = await super().get_select(request)
        return stmt.outerjoin(Category, Article.category_id == Category.id)


@site.register_admin
class ActiveArticle(ArticleAdmin):
    """继承重用`ArticleAdmin`;此示例较为简单,实际应用可能比较复杂."""

    # 自定义路由前缀
    router_prefix = '/article.active'

    # 重写基础选择器
    async def get_select(self, request: Request) -> Select:
        stmt = await super().get_select(request)
        return stmt.where(Article.is_active == True)
```

## 示例-4(自定义管理应用)

参考: [fastapi_user_auth.UserAuthApp](https://github.com/amisadmin/fastapi_user_auth/blob/9a7c30f5f562543c376fd0235091666547fb175d/fastapi_user_auth/app.py#L14)

## 示例-5(自定义管理站点)

参考: [基础教程->站点配置->自定义管理站点](/tutorials/basic/Settings/#_4)

参考: [fastapi_user_auth.AuthAdminSite](https://github.com/amisadmin/fastapi_user_auth/blob/9a7c30f5f562543c376fd0235091666547fb175d/fastapi_user_auth/site.py#L16)

