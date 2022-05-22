## RouterMixin

- FastAPI路由注册器

### 字段

#### router

- 路由注册器

#### router_prefix

- 路由注册器前缀

#### router_permission_depend

- 路由注册器权限控制依赖

### 方法:

#### get_router

- 返回当前路由注册器.

```python
def get_router(self) -> APIRouter
```

#### error_no_router_permission

- 没有路由权限错误.

```python
def error_no_router_permission(self, request: Request)
```
