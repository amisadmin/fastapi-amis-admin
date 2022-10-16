## Project Introduction

`fastapi-sqlmodel-crud` is a project based on `FastAPI`+`SQLModel`, which is used to quickly build Create, Read, Update, Delete common API interfaces.

## Install

```bash
pip install fastapi-sqlmodel-crud 
```

## Simple example

**main.py**:

```python
from typing import Optional
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel, Field
from fastapi_amis_admin.crud import SQLModelCrud


# 1. Create SQLModel model
class Article(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    title: str = Field(title='ArticleTitle', max_length=200)
    description: Optional[str] = Field(default='', title='ArticleDescription', max_length=400)
    status: bool = Field(None, title='status')
    content: str = Field(title='ArticleContent')


# 2. Create AsyncEngine
database_url = 'sqlite+aiosqlite:///amisadmin.db'
engine: AsyncEngine = create_async_engine(database_url, future=True)

# 3. Register crud route
article_crud = SQLModelCrud(model=Article, engine=engine).register_crud()

app = FastAPI(debug=True)

# 4. Include the router
app.include_router(article_crud.router)


# 5. Create model database table (first run)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

```

## Development documentation

- https://docs.gh.amis.work/crud/SQLModelCrud/

## Dependent projects

- [FastAPI](https://fastapi.tiangolo.com)

- [SQLModel](https://sqlmodel.tiangolo.com/)

## Licence

The project follows the Apache2.0 license agreement.