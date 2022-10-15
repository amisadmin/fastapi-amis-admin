## AdminApp

- 管理应用

### 继承基类

- #### [PageAdmin](../PageAdmin)

### 字段

#### engine

- 当前应用`sqlalchemy`数据库引擎,支持同步引擎和异步引擎.

-
参考: [Asynchronous I/O (asyncio) — SQLAlchemy 1.4 Documentation](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html?highlight=async#sqlalchemy.ext.asyncio.AsyncEngine)
- 示例:

```python
from sqlalchemy.ext.asyncio import create_async_engine
engine = create_async_engine("sqlite+aiosqlite:///amisadmin.db", future=True)
# engine = create_async_engine("mysql+aiomysql://amisadmin:amisadmin@127.0.0.1:3306/amisadmin?charset=utf8mb4", future=True)
# engine = create_async_engine("postgresql+asyncpg://user:pass@host/dbname", future=True)
```

#### db

- 当前应用`sqlalchemy`客户端,支持同步或异步, 即 `AsyncDatabase`或`Database` 对象.
- 参考: [AsyncDatabase](../../utils/database)

#### site

- 当前应用所属站点.

### 方法

#### get_admin_or_create

返回或创建管理类对象实例.

```python
def get_admin_or_create(self, admin_cls: Type[_BaseAdminT], register: bool = True) -> Optional[_BaseAdminT]
```

#### create_admin_instance_all

创建当前应用全部管理类对象实例

```python
def create_admin_instance_all(self) -> None
```

#### get_model_admin

获取当前应用数据库表对应的模型管理对象实例.

- 必须设置: `ModelAdmin.bind_model=True`

```python
@lru_cache
def get_model_admin(self, table_name: str) -> Optional[ModelAdmin]
```

#### register_admin

注册一个或多个BaseAdmin管理类到当前应用对象, 并且返回第一个类对象.

```python
def register_admin(self, *admin_cls: Type[_BaseAdminT]) -> Type[_BaseAdminT]
```

#### unregister_admin

取消注册当前应用对象中一个或多个BaseAdmin管理类.

```python
def unregister_admin(self, *admin_cls: Type[BaseAdmin])
```

#### get_page

返回当前应用页面.

1. 如果`tabs_mode`未设置,则返回amis App 对象.
2. 如果设置了`tabs_mode`,则返回的一个主体为`Tabs`的amis Page页面.

- 参考: [App 多页应用](https://baidu.gitee.io/amis/zh-CN/components/app)
- 参考: [Tabs 选项卡](https://aisuda.bce.baidu.com/amis/zh-CN/components/tabs)

```python
async def get_page(self, request: Request) -> Union[Page, App]
```

