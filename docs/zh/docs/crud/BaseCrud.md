## BaseCrud

- FastAPICrud路由注册器基类

### 继承基类

- #### [RouterMixin](../RouterMixin/#routermixin)

### 派生子类

- #### [SQLModelCrud](../SQLModelCrud/#sqlmodelcrud)

- 其他ORM后端暂时未支持, SQLModel已经足够强大...

### 字段

#### schema_model

- 当前模型协议

#### schema_list

- 批量查询数据返回协议, 默认: `self.schema_model`

#### schema_filter

- 批量查询数据过滤提交协议, 默认: `self.schema_model`

#### schema_create

- 创建数据提交协议, 默认: `self.schema_model`

#### schema_read

- 读取数据返回协议, 默认: `self.schema_model`

#### schema_update

- 更新数据提交协议, 默认: `self.schema_model`

#### pk_name

- 当前模型主键字符串, 默认: `id`.
- 说明: **数据库表有且只能有一个自增加主键**.(待拓展)

#### list_per_page_max

- 批量读取每页数据数量上限. 默认: None, 无限制.

#### route_list

- 批量读取路由函数. 支持同步/异步函数.

```python
@property
def route_list(self) -> Callable
```

#### route_read

- 单项/批量读取路由函数.支持同步/异步函数.

```python
@property
def route_read(self) -> Callable
```

#### route_create

- 单项/批量创建路由函数.支持同步/异步函数.

```python
@property
def route_create(self) -> Callable
```

#### route_update

- 单项/批量更新路由函数.支持同步/异步函数.

```python
@property
def route_update(self) -> Callable
```

#### route_delete

- 单项/批量删除路由函数.支持同步/异步函数.

```python
@property
def route_delete(self) -> Callable
```

### 方法:

#### has_list_permission

- 检查是否具有批量查询权限.

```python
async def has_list_permission(
    self,
    request: Request,
    paginator: Optional[Paginator],
    filter: Optional[SchemaFilterT],
    **kwargs
) -> bool
```

#### has_read_permission

- 检查是否具有单项查询权限.

```python
async def has_read_permission(
    self,
    request: Request,
    item_id: Optional[List[str]],
    **kwargs
) -> bool
```

#### has_create_permission

- 检查是否具有创建数据权限.

```python
async def has_create_permission(
    self, 
    request: Request, 
    obj: Optional[SchemaCreateT], 
    **kwargs
) -> bool
```

#### has_update_permission

- 检查是否具有更新数据权限.

```python
async def has_update_permission(
    self, 
    request: Request, 
    item_id: Optional[List[str]], 
    obj: Optional[SchemaUpdateT], 
    **kwargs
) -> bool
```

#### has_delete_permission

- 检查是否具有删除数据权限.

```python
async def has_delete_permission(
    self, 
    request: Request, 
    item_id: Optional[List[str]], 
    **kwargs
) -> bool:
    return True
```

#### register_crud

- 注册Crud路由.

```python
def register_crud(
    self,
    schema_list: Type[SchemaListT] = None,
    schema_filter: Type[SchemaFilterT] = None,
    schema_create: Type[SchemaCreateT] = None,
    schema_read: Type[SchemaReadT] = None,
    schema_update: Type[SchemaUpdateT] = None,
    list_max_per_page: int = None,
    depends_list: List[Depends] = None,
    depends_read: List[Depends] = None,
    depends_create: List[Depends] = None,
    depends_update: List[Depends] = None,
    depends_delete: List[Depends] = None
) -> "BaseCrud"
```



