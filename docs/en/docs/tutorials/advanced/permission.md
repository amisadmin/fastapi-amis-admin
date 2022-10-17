# Permission Control

FastAPI-Amis-Admin' provides very rich permission control methods, you can use different granularity of
site/application/page/route permission control for different scenarios.

## Execution flowchart

```mermaid
graph LR
    request(request)-->AdminSite[has_page_permission]
    subgraph  [AdminSite]
    	AdminSite--False-->AdminSite.error_no_page_permission(error_no_page_permission)
    end
    subgraph  [AdminApp]
		AdminSite--True-->AdminApp[has_page_permission]
		AdminApp--False-->AdminApp.error_no_page_permission(error_no_page_permission)
	end
	subgraph  [ModelAdmin]
		AdminApp--True-->ModelAdmin[has_page_permission]
        ModelAdmin--False-->ModelAdmin.error_no_page_permission(error_no_page_permission)

        ModelAdmin--True-->ModelAdmin.list[has_list_permission]
        ModelAdmin.list--False-->Response3(error_no_router_permission)

        ModelAdmin--True-->ModelAdmin.create[has_create_permission]
        ModelAdmin.create--False-->Response3

        ModelAdmin--True-->ModelAdmin.read[has_read_permission]
        ModelAdmin.read--False-->Response3

        ModelAdmin--True-->ModelAdmin.update[has_update_permission]
        ModelAdmin.update--False-->Response3

        ModelAdmin--True-->ModelAdmin.delete[has_delete_permission]
        ModelAdmin.delete--False-->Response3
	end
	subgraph  [PageAdmin]
		AdminApp--True-->PageAdmin[has_page_permission]
		PageAdmin--False-->PageAdmin.error_no_page_permission(error_no_page_permission)
	end
```

## Authentication method

### Inheritance override permission validation method

#### has_page_permission

- Check if you have permission to access the current page, default return: `True`
- Subordinate objects: `PageSchemaAdmin` and its subclasses, 
  for example: `PageAdmin` , `FormAdmin` , `ModelAdmin` , `AdminApp` , `AdminSite`.
- The permissions of the current administrative object depend on the permissions owned by the administrative application or
  administrative site to which it is bound.

```python
async def has_page_permission(self, request: Request) -> bool:
    return self.app is self or await self.app.has_page_permission(request)
```

!!! note "If `has_page_permission` validates to `False`"

	- The backend menu will not display the current admin page and all default routes under the current admin object will be disabled.
	- If the current object is `AdminApp`, all the administrative objects registered under the administrative application `has_page_permission` will return `False` by default.
	- If the current object is `ModelAdmin`, then `has_list_permission`, `has_read_permission`, `has_create_permission`, `has_update_permission`, `has_delete_ permission` all return `False` by default.

#### has_list_permission

- Check if you have bulk query permission. The default is:`True`.

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

- Checks if a single query permission is available. Default return:``True`''

```python
async def has_read_permission(
    self, 
    request: Request, 
    item_id: Optional[List[str]],
    **kwargs
) -> bool
```

#### has_create_permission

- Checks if the data creation permission is available. Default return:``True`''

```python
async def has_create_permission(
    self, 
    request: Request, 
    obj: Optional[SchemaCreateT], 
    **kwargs
) -> bool
```

#### has_update_permission

- Checks if the user has permission to update data. Default return:``True`''

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

- Checks if the data deletion permission is available. Default return:``True`''

```python
async def has_delete_permission(
    self, 
    request: Request, 
    item_id: Optional[List[str]], 
    **kwargs
) -> bool:
    return True
```

!!! note "If `has_crud_permission` validates to `False`"

	- the CRUD form page will no longer display the corresponding action buttons and the corresponding API routes will be disabled.

### Custom permission validation dependencies

#### router_permission_depend

- The route registrar permission validation dependency. Default: `None`.

#### page_permission_depend

- Current page routing permission validation dependency. Default: `has_page_permission`

### Registering global permission validation dependencies

By registering a global permission validation dependency, all routes under the `AdminSite` object will be required to pass the
specified permission validation.

```python
from fastapi import Depends, FastAPI, Header, HTTPException


async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


site = AdminSite(
    settings=Settings(debug=True, database_url_async='sqlite+aiosqlite:///amisadmin.db'),
    fastapi=FastAPI(dependencies=[Depends(verify_token)])
)

```

