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
        # page.body.title = 'MyHome' # page.body已改为list类型，该行废弃
        # 修改后台首页的内页标题
        page.title = 'MyHome'
        # 后台首页主体尾部追加内容
        page.body.append('welcome FastApi-AMIS')
        ...
        return page
```

## 示例-2.1(自定义模板管理基类)

根目录`templates`文件夹中新建`element.html`，html内容如下：
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>
    <p>The current time is: {{ current_time }}</p>
</body>
</html>
```

main.py增加如下代码：
```python linenums="1" hl_lines="6 7 11 20"
import datetime

from fastapi_amis_admin import admin, amis


class MyJinja2Admin(admin.TemplateAdmin):
    templates: Jinja2Templates = Jinja2Templates(directory='templates')


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

    async def get_page(self, request: Request) -> Dict[str, Any]:
        page = await super().get_page(request)
        # 有别于示例1中 admin.HomeAdmin 对page的修改，这里的page来自 admin.TemplateAdmin，是一个dict
        page['title'] = 'Element Title'  # 该行不会生效
        return {'current_time': datetime.datetime.now(), 'title': 'Element Content'}

```
## 示例-2.2(将多个page以tab形式展示)
我们基于示例2.1进行修改,
1、首先将`SimpleTemplateAdmin`、`ElementTemplateAdmin`的页面注册装饰函数(`@site.register_admin`)注释或删除。
2、我们创建一个Page管理页，然后将上述2个页面注册到`TemplatePageApp`下。
```python
from fastapi_amis_admin import admin, amis
from fastapi_amis_admin.admin import AdminApp
from fastapi_amis_admin.amis import TabsModeEnum


@site.register_admin
class TemplatePageApp(admin.AdminApp):
    page_schema = PageSchema(label="TemplatePage", icon="fa fa-link", tabsMode=TabsModeEnum.chrome)

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.register_admin(
            SimpleTemplateAdmin,
            ElementTemplateAdmin,
        )
```
此时，左侧菜单栏将会显示TemplatePageApp的类目，同时TemplatePageApp页面下则显示`SimpleTemplateAdmin`、`ElementTemplateAdmin`相关tab。


## 示例-3(重用模型管理类)
我们在*模型管理*-示例2的基础上进行改造，将`Article`类新增一行属性`is_active: bool = False  # add`,如下：
```python linenums="1" hl_lines="32"
class Article(Base):
    __tablename__ = 'article'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String(400), default='')
    status: Mapped[bool] = mapped_column(Boolean, default=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    category_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('category.id'))
    is_active: bool = False  # add

```
然后我们继承原油`ArticleAdmin`重新实现一个新的page类别：
```python
@site.register_admin
class ActiveArticle(ArticleAdmin):
    """继承重用`ArticleAdmin`;此示例较为简单,实际应用可能比较复杂."""
    page_schema = PageSchema(label='文章管理(已激活)', icon='fa fa-file')
    # 自定义路由前缀
    router_prefix = '/article.active'

    # 重写基础选择器
    async def get_select(self, request: Request) -> Select:
        stmt = await super().get_select(request)
        return stmt.where(Article.is_active == True)
```
此时，page中将分别有`文章管理`以及`文章管理(已激活)`，后者将只显示`is_active`为True的文章。
## ~~~示例-3(重用模型管理类)~~~

```python linenums="1" hl_lines="32"
from fastapi_amis_admin import admin
from fastapi_amis_admin.models import Field


# 创建一个SQLModel模型,详细请参考: https://sqlmodel.tiangolo.com/
class Article(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
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

