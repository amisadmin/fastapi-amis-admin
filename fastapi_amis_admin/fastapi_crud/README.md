## fastapi_crud介绍

fastapi_crud是一个基于FastAPI+SQLModel, 用于快速构建Create,Read,Update,Delete通用API接口的项目.



## 安装

```bash
pip install fastapi_amis_admin
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

app = FastAPI(debug=True)

from fastapi_amis_admin.fastapi_crud import SQLModelCrud


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


async def session_factory(self) -> Generator[AsyncSession, Any, None]:
    async with self.session_maker() as session:
        yield session


# 3. 注册crud路由
article_crud = SQLModelCrud(model=Article, session_factory=session_factory).register_crud()

# 4. 包含路由器
app.include_router(article_crud.router)
```



## 开发文档

- https://github.com/amisadmin/fastapi_amis_admin




## 依赖项目

- [pydantic](https://pydantic-docs.helpmanual.io/) 

- [amis](https://baidu.gitee.io/amis) 

  

## 许可协议

该项目遵循 Apache2.0 许可协议。
