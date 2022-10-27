## BaseModelAction

- Model management action base class

### fields

#### admin

- The model management object to which the current action belongs.

#### action

- The current action amis Action object.
- Reference: [Action Action Button](https://baidu.gitee.io/amis/zh-CN/components/action?page=1#popbox)

### method

#### register_router

- Register action routes.

#### fetch_item_scalars

- Get option data.

```python
async def fetch_item_scalars(self,item_id: List[str]) -> List[BaseModel]:
    stmt = select(self.admin.model).where(self.admin.pk.in_(item_id))
    return await self.admin.db.async_execute(stmt)
```

## ModelAction

- Model management actions

### Inherit from base class

- #### [BaseFormAdmin](../FormAdmin/#baseformadmin)

- #### [BaseModelAction](#basemodelaction)

### fields

#### schema

- Form data model, can be set to: `None`.

### method

#### get_action

- Get the current action amis Action object.

```python
async def get_action(self, request: Request, **kwargs) -> Action
```

#### handle

Process model action data.

- `request`: The current request object.
- `item_id`: A list of primary keys for model data selected by the user.
- `data`: Form data object if the action form data model `schema` is configured. `None` otherwise
- `session`: The asynchronous session of the database connection to which the current management model belongs.

```python
async def handle(
    self, 
    request: Request, 
    item_id: List[str], 
    data: Optional[BaseModel],
    **quargs
) -> BaseApiOut[Any]
```
