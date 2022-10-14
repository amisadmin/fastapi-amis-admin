## AdminApp

- AdminApp

### Inheritance base class

- #### [PageAdmin](. /PageAdmin)



### Fields

#### engine

- The current application `sqlalchemy` database engine, supports both synchronous and asynchronous engines.

- Reference: [Asynchronous I/O (asyncio) - SQLAlchemy 1.4 Documentation](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio. html?highlight=async#sqlalchemy.ext.asyncio.AsyncEngine)
- Example:

```python
from sqlalchemy.ext.asyncio import create_async_engine
engine = create_async_engine("sqlite+aiosqlite:///amisadmin.db", future=True)
# engine = create_async_engine("mysql+aiomysql://amisadmin:amisadmin@127.0.0.1:3306/amisadmin?charset=utf8mb4", future=True)
# engine = create_async_engine("postgresql+asyncpg://user:pass@host/dbname", future=True)
```

#### db

- The current application is the `sqlalchemy` client, which supports either synchronous or asynchronous, i.e. `AsyncDatabase` or `Database` objects. 
- Reference: [AsyncDatabase](... /... /utils/database)

#### site

- The site of the current application.



### Methods

#### get_admin_or_create

Returns or creates an instance of the admin class object.

```python
def get_admin_or_create(self, admin_cls: Type[_BaseAdminT], register: bool = True) -> Optional[_BaseAdminT]
```

#### create_admin_instance_all

Create all instances of the current application's administrative class objects

```python
def create_admin_instance_all(self) -> None
```

#### get_model_admin

Gets the instance of the model admin object corresponding to the current application database table.

- Must be set: ``ModelAdmin.bind_model=True`''

```python
@lru_cache
def get_model_admin(self, table_name: str) -> Optional[ModelAdmin]
```

#### register_admin

Register one or more BaseAdmin administrative classes to the current application object, and return the first class object.

```python
def register_admin(self, *admin_cls: Type[_BaseAdminT]) -> Type[_BaseAdminT]
```

#### unregister_admin

Unregister one or more BaseAdmin administrative classes in the current application object.

``` python
def unregister_admin(self, *admin_cls: Type[BaseAdmin])
```

#### get_page

Returns the current application page.

1. if `tabs_mode` is not set, return amis App object. 2. if `tabs_mode` is set, return amis App object.
2. if `tabs_mode` is set, the amis Page page with the body `Tabs` will be returned.

- Reference: [App multi-page application](https://baidu.gitee.io/amis/zh-CN/components/app)
- Reference: [Tabs tab](https://aisuda.bce.baidu.com/amis/zh-CN/components/tabs)

```python
async def get_page(self, request: Request) -> Union[Page, App]
```

