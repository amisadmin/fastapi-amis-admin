# Model Management

Model management is the most commonly used management class in background management, and its functions are also the most abundant. fastapi-amis-admin has implemented various basic operations commonly used for data models, and you can still make on this basis. More personalized extensions.

## Example-1

```python
# First create a SQLModel model, please refer to: https://sqlmodel.tiangolo.com/
class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(title='CategoryName')
    description: str = Field(default='', title='Description')


# Register ModelAdmin
@site.register_admin
class CategoryAdmin(admin.ModelAdmin):
    page_schema = 'Category Management'
    # Configuration management model
    model = Category
```

Let's take a look at this simple example-1. It completes the following steps:

1. Define a `Category` model.
1. Define a model management class that inherits `admin.ModelAdmin`.
1. Configure the model and register to the management site.

!!! note annotate "About the SQLModel model"

    In fact, this part of the code does not belong to the `amis-admin` code, because it can be reused anywhere ORM mapping is required, in the project you should define a separate `models.py` file to write this part of the code.
    
    SQLModel is a very good Python ORM library, written by the same author of FastAPI, which perfectly combines SQLAlchemy and Pydantic. Please read its official documentation: https://sqlmodel.tiangolo.com/

## Example-2

```python
# Create a SQLModel model, please refer to: https://sqlmodel.tiangolo.com/
class Article(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    title: str = Field(title='ArticleTitle', max_length=200)
    description: Optional[str] = Field(default='', title='ArticleDescription', max_length=400)
    status: bool = Field(None, title='status')
    content: str = Field(title='ArticleContent')
    # Associate Category model, model definition reference [Example-1]
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", title='CategoryId')
    # category: Optional[Category] = Relationship(back_populates="articles")


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
```

Example 2 is more complicated than Example 1. But if you are familiar with `Django-Admin` you will find they are very similar, yes. `fastapi_amis_admin` is inspired by `Django-Admin`, so many functions are designed with is similar, and `fastapi_amis_admin`
The functions are more abundant and the configuration is more flexible.

### Configure display fields

By default, the management list will display all fields of the current model. But if you only need to display some fields, or you also need to display other fields of related models, you can customize the fields to be displayed by configuring `list_display`.

- For example in example 2:

- `Article.content` and `Article.category_id` are not included in the display field.
- `Category.name` is a field of another model and can also be included in the display field, but here you need to customize the selector `left join` `Category` model through the `get_select` method.

### Configure fuzzy search fields

`search_fields` configures the query method for string fields as `like` filtering. If `search_fields` is not configured, the default is `equal` query method.

### Custom selector

The `get_select` custom selector can achieve different initial data query conditions for different requests, similar to the `get_queryset` method in `django-admin`.

## function list

Currently, the model management class `ModelAdmin` in `fastapi-amis-admin` has supported functions including but not limited to the following list.

| Function | Related Fields or Methods | Remarks |
|:---------------:|:------------------------------ --------:| :------------------------------------------------------: |
| Custom bulk query fields | `fields`, `exclude` | |
| Custom batch query display fields | `list_display`, `get_list_display` | Support display types are picture, audio, video, list, `Json` |
| Custom batch query filter form | `list_filter` | Support text exact/fuzzy matching, time range filtering, multiple selection filtering |
| Custom batch query sorting field | `ordering` | |
| Custom model primary key | `pk_name` | |
| Custom bulk query selector | `get_select` | Support `Jion` other database table models |
| Custom Model Database | `engine` | |
| Custom batch query read-only fields | `readonly_fields` | |
| Customize batch query data volume per page | `list_per_page` | |
| Custom bulk query fuzzy search fields | `search_fields` | |
| Customize fields for new models | `create_fields` | |
| Customize fields that support editing | `update_fields` | |
| Customize fields that support bulk editing | `bulk_update_fields` | |
| Customize the new model data form | `get_create_form` | |
| Custom update model data form | `get_update_form` | |
| Customize the new model data execution action | `get_create_action` | |
| Custom update model data execution action | `get_update_action` | |
| Custom delete model data execution action | `get_delete_action` | |
| Custom batch query data return protocol | `schema_list` | |
| Customize batch query data filtering submission protocol | `schema_filter` | |
| Custom Create Data Submission Protocol | `schema_create` | |
| Custom read data return protocol | `schema_read` | |
| Custom update data submission protocol | `schema_update` | |
| Custom batch query permission | `has_list_permission` | |
| Custom single query permission | `has_read_permission` | |
| Custom create data permission | `has_create_permission` | |
| Custom update data permission | `has_update_permission` | |
| Custom delete data permission | `has_delete_permission` | |
| | | |

## More usage

The usage of `ModelAdmin` is very flexible, only the most basic usage is shown here, you can read the [API documentation](/amis_admin/ModelAdmin/)
Or refer to the [demo program](https://github.com/amisadmin/fastapi_amis_admin_demo/) for more detailed usage. Examples of specific application scenarios will be added in the future.
If you have better application examples or tutorial documents, you can submit them through github, thank you very much for your support! `fastapi_amis_admin` will do better!

- [FastAPI-Amis-Admin-Demo](https://github.com/amisadmin/fastapi_amis_admin_demo)

- [FastAPI-User-Auth-Demo](https://github.com/amisadmin/fastapi_user_auth_demo)

- [ModelAdmin - FastAPI-Amis-Admin](/amis_admin/ModelAdmin/)

- [SQLModelCrud - FastAPI-Amis-Admin](/fastapi_amis_admin/crud/SQLModelCrud/)

- [Table 表格 (gitee.io)](https://baidu.gitee.io/amis/zh-CN/components/table)

!!! note annotate "About fastapi_amis_admin and django-admin"

    [django-admin](https://docs.djangoproject.com/zh-hans/4.0/ref/contrib/admin/) is a very mature and powerful web management background tool, users who use django should often use it, But he is not suitable for non-django projects, which is one of the main reasons why fastapi_amis_admin was born.
    
    Fastapi_amis_admin has more extensions and functions than django-admin, but fastapi_amis_admin is still in the growth stage, many functions are immature, and need long-term continuous improvement and upgrading. I look forward to your participation in [fastapi_amis_admin](https://github .com/amisadmin/fastapi_amis_admin), contribute code to the project, or [provide suggestions](https://github.com/amisadmin/fastapi_amis_admin/issues).
