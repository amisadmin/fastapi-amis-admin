# 权限控制

当前你可以通过以下两种方法实现权限控制: 

## 继承重写自定义权限验证方法

### router_permission_depend

- 路由注册器权限控制依赖.默认: `None`

### page_permission_depend

- 当前页面路由权限检测依赖.默认: `has_page_permission`

### has_page_permission

检查是否拥有访问当前页面权限,默认返回:`True`

```python
async def has_page_permission(self, request: Request)->bool:
    return True
```

### has_list_permission

- 检查是否具有批量查询权限.默认返回:`True`

```python
async def has_list_permission(self, request: Request, paginator: Optional[Paginator], filter: Optional[BaseModel],**kwargs) -> bool
```

### has_read_permission

- 检查是否具有单项查询权限.默认返回:`True`

```python
async def has_read_permission(self, request: Request, item_id: Optional[List[str]], **kwargs) -> bool
```

### has_create_permission

- 检查是否具有创建数据权限.默认返回:`True`

```python
async def has_create_permission(self, request: Request, obj: Optional[BaseModel], **kwargs) -> bool
```

### has_update_permission

- 检查是否具有更新数据权限.默认返回:`True`

```python
async def has_update_permission(self, request: Request, item_id: Optional[List[str]], obj: Optional[BaseModel],**kwargs) -> bool
```

### has_delete_permission

- 检查是否具有删除数据权限.默认返回:`True`

```python
async def has_delete_permission(self, request: Request, item_id: Optional[List[str]], **kwargs) -> bool:
        return True
```



## 注册全局权限验证依赖

通过注册全局权限验证依赖, `AdminSite`对象下全部的路由都将需要通过指定的权限验证.

```python
from fastapi import Depends, FastAPI, Header, HTTPException


async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


site = AdminSite(settings=Settings(debug=True, database_url_async='sqlite+aiosqlite:///admisadmin.db'),
                 fastapi=FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)]))

```



## 用户认证与授权系统

正在开发当中, 目前大概完成70%左右, 发布时间暂时不确定,可能在3月份吧, 优先体验内测版本,可以加入Q群: [229036692](https://jq.qq.com/?_wv=1027&k=U4Dv6x8W)