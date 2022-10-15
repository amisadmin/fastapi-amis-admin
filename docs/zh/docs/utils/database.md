## AsyncDatabase

- `sqlalchemy`异步客户端

### 字段

#### engine

- `sqlalchemy`异步引擎.
-

参考: [Asynchronous I/O (asyncio) — SQLAlchemy 1.4 Documentation](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html?highlight=async#sqlalchemy.ext.asyncio.AsyncEngine)

- 示例:

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine("sqlite+aiosqlite:///amisadmin.db", future=True)
# engine = create_async_engine("mysql+aiomysql://amisadmin:amisadmin@127.0.0.1:3306/amisadmin?charset=utf8mb4", future=True)
# engine = create_async_engine("postgresql+asyncpg://user:pass@host/dbname", future=True)
```

#### session_maker

```python
self.session_maker: sessionmaker = sessionmaker(self.async_engine, class_=AsyncSession, autoflush=False)
```

### 方法:

#### session_generator

```python
async def session_generator(self) -> AsyncGenerator[AsyncSession, Any]:
    async with self.session_maker() as session:
        yield session
```

## Database

- `sqlalchemy`同步客户端

### 字段

#### engine

- `sqlalchemy`同步引擎.
-

参考: [Establishing Connectivity - the Engine — SQLAlchemy 1.4 Documentation](https://docs.sqlalchemy.org/en/14/tutorial/engine.html)

- 示例:

```python
from sqlalchemy import create_engine

engine = create_engine("sqlite+pysqlite:///amisadmin.db", echo=True, future=True)
# engine = create_async_engine("mysql+pymysql://amisadmin:amisadmin@127.0.0.1:3306/amisadmin?charset=utf8mb4", future=True)
# engine = create_async_engine("postgresql+psycopg2://user:pass@host/dbname", future=True)


```

#### session_maker

```python
self.session_maker: sessionmaker = sessionmaker(self.async_engine, autoflush=False)
```

### 方法:

#### session_generator

```python
def session_generator(self) -> Generator[Session, Any, None]:
    with self.session_maker() as session:
        yield session
```

### 参考项目: 

[sqlalchemy-database](https://github.com/amisadmin/sqlalchemy_database)