## BaseCrud

- FastAPICrud route registrar base class

### Inherit from base class

- #### [RouterMixin](../RouterMixin/#routermixin)

### Derived subclass

- #### [SQLModelCrud](../SQLModelCrud/#sqlmodelcrud)

- Other ORM backends are not supported yet, SQLModel is powerful enough...

### fields

#### schema_model

- Current model agreement

#### schema_list

- Batch query data return protocol, default: `self.schema_model`

#### schema_filter

- Batch query data filter submission protocol, default: `self.schema_model`

#### schema_create

- Create data submission protocol, default: `self.schema_model`

#### schema_read

- read data return protocol, default: `self.schema_model`

#### schema_update

- Update data submission protocol, default: `self.schema_model`

#### pk_name

- current model primary key string, default: `id`.
- Description: **Database table has and can only have one self-incrementing primary key**. (To be expanded)

#### list_per_page_max

- The maximum number of data per page to be read in batches. Default: None, no limit.

#### route_list

- Bulk read routing functions. Supports sync/async functions.

```python
@property
def route_list(self) -> Callable
```

#### route_read

- Single item/batch read routing function. Support synchronous/asynchronous functions.

```python
@property
def route_read(self) -> Callable
```

#### route_create

- Single/batch create routing functions. Support synchronous/asynchronous functions.

```python
@property
def route_create(self) -> Callable
```

#### route_update

- Single/batch update routing functions. Support synchronous/asynchronous functions.

```python
@property
def route_update(self) -> Callable
```

#### route_delete

- Single item/batch delete routing function. Support synchronous/asynchronous function.

```python
@property
def route_delete(self) -> Callable
```

### method:

#### has_list_permission

- Check if you have batch query permission.

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

- Check if you have single query permission.

```python
async def has_read_permission(
    self, 
    request: Request, 
    item_id: Optional[List[str]],
    **kwargs
) -> bool
```

#### has_create_permission

- Check if you have permission to create data.

```python
async def has_create_permission(
    self, 
    request: Request, 
    obj: Optional[SchemaCreateT], 
    **kwargs
) -> bool
```

#### has_update_permission

- Check if you have permission to update data.

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

- Check if you have permission to delete data.

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

- Register Crud routing.

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


