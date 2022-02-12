## AdminApp

- 管理应用

### 继承基类

- #### [PageAdmin](../PageAdmin)



### 字段

#### engine

- 当前应用`sqlalchemy`数据库异步引擎.

- 参考: [Asynchronous I/O (asyncio) — SQLAlchemy 1.4 Documentation](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html?highlight=async#sqlalchemy.ext.asyncio.AsyncEngine)
- 示例:

```python
from sqlalchemy.ext.asyncio import create_async_engine
engine = create_async_engine("sqlite+aiosqlite:///admisadmin.db", future=True)
# engine = create_async_engine("mysql+aiomysql://amisadmin:amisadmin@127.0.0.1:3306/amisadmin?charset=utf8mb4", future=True)
# engine = create_async_engine("postgresql+asyncpg://user:pass@host/dbname", future=True)
```

#### db

- 当前应用`sqlalchemy`异步客户端, 即 `SqlalchemyAsyncClient` 对象. 
- 参考: [SqlalchemyAsyncClient](../../utils/db)

#### route_index

- 当前应用主页路由.

#### site

- 当前应用所属站点.



### 方法

#### create_admin_instance

创建并返回管理类对象实例.

```python
def create_admin_instance(self, admin_cls: Type[_BaseAdminT]) -> _BaseAdminT
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

返回当前应用页面amis App 对象.

- 参考: [App 多页应用](https://baidu.gitee.io/amis/zh-CN/components/app)

```python
async def get_page(self, request: Request) -> App
```

#### get_page_schema_children

返回当前应用导航页面属性列表.

- 参考: [App 多页应用#属性说明](https://baidu.gitee.io/amis/zh-CN/components/app#属性说明)

```python
async def get_page_schema_children(self, request: Request) -> List[PageSchema]
```
