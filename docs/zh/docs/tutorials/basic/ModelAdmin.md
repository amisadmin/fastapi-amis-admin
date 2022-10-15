# 模型管理

模型管理在后台管理中是最为常用的一个管理类,其使用功能也是最为丰富的. fastapi-amis-admin目前已经实现针对数据模型常用的各种基本操作,
并且你仍然可以在此基础上做出更多个性化的拓展.

## 示例-1

```python
# 先创建一个SQLModel模型,详细请参考: https://sqlmodel.tiangolo.com/
class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(title='CategoryName')
    description: str = Field(default='', title='Description')


# 注册ModelAdmin
@site.register_admin
class CategoryAdmin(admin.ModelAdmin):
    page_schema = '分类管理'
    # 配置管理模型
    model = Category
```

先看一下这个简单的示例-1吧.它完成了以下几个步骤:

1. 定义了一个`Category`模型.
1. 定义一个模型管理类, 继承`admin.ModelAdmin`.
1. 配置模型,并注册到管理站点.

!!! note annotate "关于SQLModel模型"

    事实上这部分代码并不属于`amis-admin`的代码,因为它可以用重用在任何需要ORM映射的地方, 在项目中你应该单独定义一个`models.py`文件编写这部分代码.
    
    SQLModel是一个非常优秀的Python ORM库,由FastAPI同一位作者编写,完美的结合了SQLAlchemy和Pydantic.请阅读它的官方文档: https://sqlmodel.tiangolo.com/

## 示例-2

```python
# 创建一个SQLModel模型,详细请参考: https://sqlmodel.tiangolo.com/
class Article(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    title: str = Field(title='ArticleTitle', max_length=200)
    description: Optional[str] = Field(default='', title='ArticleDescription', max_length=400)
    status: bool = Field(None, title='status')
    content: str = Field(title='ArticleContent')
    # 关联Category模型,模型定义参考[示例-1]
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", title='CategoryId')
    # category: Optional[Category] = Relationship(back_populates="articles")


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
```

示例2相比于示例1显得更为复杂. 但是如果你熟悉`Django-Admin`你会发现他们非常的相似,是的. `fastapi_amis_admin`启发自`Django-Admin`
,所以很多功能的设计都与之类似, 并且`fastapi_amis_admin`
的功能更加丰富,配置更加灵活.

### 配置展示字段

默认情况下,管理列表会展示当前模型的全部字段.但是如果你只需要展示部分字段,或者你还需要展示相关模型的其他字段,你可以通过配置`list_display`
来自定义需要展示的字段.

- 例如在示例2中:

- `Article.content`与`Article.category_id`并不包括在展示字段当中.
- `Category.name`是另一个模型的字段,也可以包括在展示字段中, 但是这里需要通过`get_select`方法自定义选择器`left join` `Category`模型.

### 配置模糊搜索字段

`search_fields`配置针对字符串字段查询方式为`like`过滤.如果不配置`search_fields`,则默认为`equal`查询方式.

### 自定义选择器

`get_select`自定义选择器可以实现针对不同请求的获取不同的初始化数据查询条件,类似于`django-admin`当中的`get_queryset`方法.

## 功能列表

目前`fastapi-amis-admin`中的模型管理类`ModelAdmin`已支持功能包括但不限于以下列表.

|       功能        |                相关字段或方法                 |                    备注                     |
|:---------------:|:--------------------------------------:| :-----------------------------------------: |
|    自定义批量查询字段    |          `fields`, `exclude`           |                                             |
|   自定义批量查询展示字段   |   `list_display`, `get_list_display`   |  支持展示类型为图片,音频,视频,列表,`Json`   |
|   自定义批量查询过滤表单   |             `list_filter`              | 支持文本精准/模糊匹配,时间范围过滤,多选过滤 |
|   自定义批量查询排序字段   |               `ordering`               |                                             |
|     自定义模型主键     |               `pk_name`                |                                             |
|   自定义批量查询选择器    |              `get_select`              |         支持`Jion`其他数据库表模型          |
|    自定义模型数据库     |                `engine`                |                                             |
|   自定义批量查询只读字段   |           `readonly_fields`            |                                             |
|  自定义批量查询每页的数据量  |            `list_per_page`             |                                             |
| 自定义批量查询模糊搜索的字段  |            `search_fields`             |                                             |
|   自定义新增模型的字段    |            `create_fields`             |                                             |
|   自定义支持编辑的字段    |            `update_fields`             |                                             |
|  自定义支持批量编辑的字段   |          `bulk_update_fields`          |                                             |
|   自定义新增模型数据表单   |           `get_create_form`            |                                             |
|   自定义更新模型数据表单   |           `get_update_form`            |                                             |
|  自定义新增模型数据执行动作  |          `get_create_action`           |                                             |
|  自定义更新模型数据执行动作  |          `get_update_action`           |                                             |
|  自定义删除模型数据执行动作  |          `get_delete_action`           |                                             |
|  自定义批量查询数据返回协议  |             `schema_list`              |                                             |
| 自定义批量查询数据过滤提交协议 |            `schema_filter`             |                                             |
|   自定义创建数据提交协议   |            `schema_create`             |                                             |
|   自定义读取数据返回协议   |             `schema_read`              |                                             |
|   自定义更新数据提交协议   |            `schema_update`             |                                             |
|    自定义批量查询权限    |         `has_list_permission`          |                                             |
|    自定义单项查询权限    |         `has_read_permission`          |                                             |
|    自定义创建数据权限    |        `has_create_permission`         |                                             |
|    自定义更新数据权限    |        `has_update_permission`         |                                             |
|    自定义删除数据权限    |        `has_delete_permission`         |                                             |
|                 |                                        |                                             |

## 更多用法

`ModelAdmin`的用法非常灵活,这里仅仅展示了最为基本的用法,你可以阅读[API文档](/amis_admin/ModelAdmin/)
或参考[demo程序](https://github.com/amisadmin/fastapi_amis_admin_demo/)了解更为详细的用法.后续将会陆续补充具体的应用场景示例.
如果你有较好的应用示例或教程文档,可以通过github提交,非常感谢你的支持!`fastapi_amis_admin`将会做的更好!

- [FastAPI-Amis-Admin-Demo](https://github.com/amisadmin/fastapi_amis_admin_demo)

- [FastAPI-User-Auth-Demo](https://github.com/amisadmin/fastapi_user_auth_demo)

- [ModelAdmin - FastAPI-Amis-Admin](/amis_admin/ModelAdmin/)

- [SQLModelCrud - FastAPI-Amis-Admin](/fastapi_amis_admin/crud/SQLModelCrud/)

- [Table 表格 (gitee.io)](https://baidu.gitee.io/amis/zh-CN/components/table)

!!! note annotate "关于fastapi_amis_admin与django-admin"

    [django-admin](https://docs.djangoproject.com/zh-hans/4.0/ref/contrib/admin/)是一个非常成熟强大的web管理后台工具,使用django的用户应该经常使用到它,但他是并不适用于非django项目,这也是fastapi_amis_admin诞生的主要原因之一.
    
    fastapi_amis_admin相比django-admin拥有更多的拓展与功能,但是fastapi_amis_admin目前仍然处于成长阶段,很多功能并不成熟,需要漫长的不断完善与升级.非常期待你参与到[fastapi_amis_admin](https://github.com/amisadmin/fastapi_amis_admin)的项目开发之中,为项目贡献代码,或为项目[提供建议](https://github.com/amisadmin/fastapi_amis_admin/issues).

