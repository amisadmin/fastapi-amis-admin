from typing import Any, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

engine: AsyncEngine = create_async_engine('sqlite+aiosqlite:///:memory:', future=True)
session_maker: sessionmaker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autocommit=False,
                                           autoflush=False)


async def session_factory() -> AsyncGenerator[AsyncSession, Any]:
    async with session_maker() as session:
        yield session
