# 权限控制

`FastAPI-Amis-Admin`提供了非常丰富的权限控制方法, 你可以针对不同的场景,采用站点/应用/页面/路由不同粒度的权限控制.

## 执行流程图

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

## 验证方式

### 继承重写权限验证方法

#### has_page_permission

- 检查是否拥有访问当前页面权限,默认返回:`True`
- 所属对象: `PageSchemaAdmin`及其子类,例如: `PageAdmin` , `FormAdmin` , `ModelAdmin`, `AdminApp`,`AdminSite`.
- 当前管理对象的权限,依赖于自身所绑定的管理应用或管理站点所拥有的权限.

```python
async def has_page_permission(self, request: Request) -> bool:
    return self.app is self or await self.app.has_page_permission(request)
```

!!! note "如果`has_page_permission`验证结果为`False`"

	- 后台菜单将不显示当前管理对象页面,并且当前管理对象下的默认路由都将禁止访问.
	- 如果当前对象为`AdminApp`,则管理应用下注册的全部管理对象`has_page_permission`都默认返回`False`.
	- 如果当前对象为`ModelAdmin`,则`has_list_permission`,`has_read_permission`,`has_create_permission`,`has_update_permission`,`has_delete_permission`都默认返回`False`.

#### has_list_permission

- 检查是否具有批量查询权限.默认返回:`True`

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

- 检查是否具有单项查询权限.默认返回:`True`

```python
async def has_read_permission(
    self, 
    request: Request, 
    item_id: Optional[List[str]],
    **kwargs
) -> bool
```

#### has_create_permission

- 检查是否具有创建数据权限.默认返回:`True`

```python
async def has_create_permission(
    self, 
    request: Request, 
    obj: Optional[SchemaCreateT], 
    **kwargs
) -> bool
```

#### has_update_permission

- 检查是否具有更新数据权限.默认返回:`True`

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

- 检查是否具有删除数据权限.默认返回:`True`

```python
async def has_delete_permission(
    self, 
    request: Request, 
    item_id: Optional[List[str]], 
    **kwargs
) -> bool:
    return True
```

!!! note "如果`has_crud_permission`验证结果为`False`"

	- CRUD表格页面将会不再显示对应的操作按钮,并且对应的API路由都将禁止访问.

### 自定义权限验证依赖

#### router_permission_depend

- 路由注册器权限验证依赖.默认: `None`

#### page_permission_depend

- 当前页面路由权限验证依赖.默认: `has_page_permission`

### 注册全局权限验证依赖

通过注册全局权限验证依赖, `AdminSite`对象下全部的路由都将需要通过指定的权限验证.

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

