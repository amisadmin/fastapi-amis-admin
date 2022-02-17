## 项目介绍

`fastapi-sqlmodel-crud`是一个基于`FastAPI`+`SQLModel`, 用于快速构建Create,Read,Update,Delete通用API接口的项目.



## 安装

```bash
pip install fastapi-sqlmodel-crud 
```

## 简单示例

**main.py**:

```python
from typing import Optional, Generator, Any
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Field
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi_amis_admin.crud import SQLModelCrud


#  1.创建SQLModel模型
class Article(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    title: str = Field(title='ArticleTitle', max_length=200)
    description: Optional[str] = Field(default='', title='ArticleDescription', max_length=400)
    status: bool = Field(None, title='status')
    content: str = Field(title='ArticleContent')


# 2.创建 AsyncSession
database_url = 'sqlite+aiosqlite:///admisadmin.db'
engine: AsyncEngine = create_async_engine(database_url, future=True, pool_recycle=1200)
session_maker: sessionmaker = sessionmaker(engine, class_=AsyncSession,
                                           expire_on_commit=False, autocommit=False, autoflush=False)


async def session_factory() -> Generator[AsyncSession, Any, None]:
    async with session_maker() as session:
        yield session


# 3. 注册crud路由
article_crud = SQLModelCrud(model=Article, session_factory=session_factory).register_crud()

app = FastAPI(debug=True)

# 4. 包含路由器
app.include_router(article_crud.router)


# 5. 创建模型数据库表(首次运行)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

```


## 开发文档

- https://docs.gh.amis.work/crud/SQLModelCrud/



## 依赖项目

- [Fastapi](https://fastapi.tiangolo.com)

- [SQLModel](https://sqlmodel.tiangolo.com/)


## 许可协议

该项目遵循 Apache2.0 许可协议。
