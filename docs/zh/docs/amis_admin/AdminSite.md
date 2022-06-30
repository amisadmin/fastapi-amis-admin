## BaseAdminSite

- 管理站点基类

### 继承基类

- #### [AdminApp](../AdminApp)

### 字段

#### settings

- 当前管理站点配置设置`Settings`对象.

- 参考: [Settings](../Settings)

#### fastapi

- 当前管理站点所挂载的FastAPI对象.
- 参考: https://fastapi.tiangolo.com/

### 方法

#### `__init__`

管理站点初始化.

- `settings`: 管理站点基本配置
- `fastapi`: 管理站点FastAPI应用
- `engine`: 管理站点默认数据库引擎.

```python
def __init__(self, settings: Settings, fastapi: FastAPI = None, engine: AsyncEngine = None)
```

#### mount_app

将当前管理站点挂载到FastAPI实例.

```python
def mount_app(self, fastapi: FastAPI, name: str = None) -> None
```

## AdminSite

- 管理站点
- 管理站点相对于基础站点默认注册了几个管理类: HomeAdmin, DocsAdmin, ReDocsAdmin, FileAdmin

### 继承基类

- #### [BaseAdminSite](#baseadminsite)

