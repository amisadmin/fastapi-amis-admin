## BaseAdminSite

- Admin site base class

### Inherit base class

- #### [AdminApp](. /AdminApp)

### Fields

#### settings

- Current admin site configuration settings `Settings` object.

- Reference: [Settings](... /Settings) /Settings)

#### fastapi

- The FastAPI object that is currently mounted on the management site.
- Reference: https://fastapi.tiangolo.com/

### Methods

#### `__init__`

Initialize the management site.

- `settings`: Basic configuration of the management site
- `fastapi`: manages the site FastAPI application
- `engine`: manages the site's default database engine.

```python
def __init__(self, settings: Settings, fastapi: FastAPI = None, engine: AsyncEngine = None)
```

#### mount_app

Mount the current management site to a FastAPI instance.

```python
def mount_app(self, fastapi: FastAPI, name: str = None) -> None
```

## AdminSite

- Admin Site
- AdminSite registers several administrative classes by default with respect to the base site: HomeAdmin, DocsAdmin, ReDocsAdmin, FileAdmin

### Inheritance of the base class

- #### [BaseAdminSite](#baseadminsite)

