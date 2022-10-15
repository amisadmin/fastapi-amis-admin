# alembic database migration

## create migration folder

- The first time the project runs, the migrations folder is generated

```bash
alembic init -t async migrations
```

## Modify the configuration file

- env ​​file path: `backend/migrations/env.py`

```python
# import SQLModel

from sqlmodel import SQLModel  

# import model data

from app.models import *  

# set metadata

target_metadata = SQLModel.metadata

```

- ini file path: `backend/alembic.ini`

```this
# Modify the asynchronous database connection of the project
sqlalchemy.url = sqlite+aiosqlite:///amisadmin.db
```

## Generate migration files

- Execute the command to generate the sqlModel initialization migration file

```bash
alembic revision --autogenerate
```

## update database

```bash
- Execute command to update database: alembic_version
alembic upgrade head
```

## Migration

- The following commands are executed once every time the model is modified.

```bash
- Execute command to generate sqlModel update migration file
alembic revision --autogenerate

- Execute command to update database: alembic_version
alembic upgrade head
```

## Reference documentation:

- [FastAPI with Async SQLAlchemy, SQLModel, and Alembic | TestDriven.io](https://testdriven.io/blog/fastapi-sqlmodel/)

- [Alembic 1.7.5 documentation](https://alembic.sqlalchemy.org/en/latest/)