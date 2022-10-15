## RouterMixin

- FastAPI Route Registrar

### fields

#### router

- Route Registrar

#### router_prefix

- route registrar prefix

#### router_permission_depend

- Route registrar permission control dependency

### method:

#### get_router

- Returns the current route registrar.

```python
def get_router(self) -> APIRouter
```

#### error_no_router_permission

- No routing permission error.

```python
def error_no_router_permission(self, request: Request)
```