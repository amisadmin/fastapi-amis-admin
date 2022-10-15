## AsyncDatabase

- `sqlalchemy` asynchronous client

### fields

#### engine

- `sqlalchemy` asynchronous engine.
-

Reference: [Asynchronous I/O (asyncio) — SQLAlchemy 1.4 Documentation](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html?highlight=async#sqlalchemy.ext.asyncio.AsyncEngine)

- Example:

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

### method:

#### session_generator

```python
async def session_generator(self) -> AsyncGenerator[AsyncSession, Any]:
    async with self.session_maker() as session:
        yield session
```

## Database

- `sqlalchemy` sync client

### fields

#### engine

- `sqlalchemy` synchronization engine.

Reference: [Establishing Connectivity - the Engine — SQLAlchemy 1.4 Documentation](https://docs.sqlalchemy.org/en/14/tutorial/engine.html)

- Example:

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

### method:

#### session_generator

```python
def session_generator(self) -> Generator[Session, Any, None]:
    with self.session_maker() as session:
        yield session
```

### Reference project:

[sqlalchemy-database](https://github.com/amisadmin/sqlalchemy_database)