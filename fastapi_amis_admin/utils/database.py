import functools
from typing import Generator, Any, AsyncGenerator, Callable, Optional, Mapping, Union, Sequence, TypeVar, Type, List

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.future import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import Executable

try:
    from asyncio import to_thread  # python 3.9+
except ImportError:
    import asyncio
    import contextvars
    from typing_extensions import ParamSpec

    _P = ParamSpec("_P")
    _R = TypeVar("_R")


    async def to_thread(func: Callable[_P, _R], *args: _P.args, **kwargs: _P.kwargs) -> _R:
        loop = asyncio.get_running_loop()
        ctx = contextvars.copy_context()
        func_call = functools.partial(ctx.run, func, *args, **kwargs)
        return await loop.run_in_executor(None, func_call)

_T = TypeVar("_T")
_ExecuteParams = Union[Mapping[Any, Any], Sequence[Mapping[Any, Any]]]
_ExecuteOptions = Mapping[Any, Any]


class AsyncDatabase:

    def __init__(self, engine: AsyncEngine, **session_options):
        self.engine: AsyncEngine = engine
        session_options.setdefault('class_', AsyncSession)
        self.session_maker: Callable[..., AsyncSession] = sessionmaker(self.engine, **session_options)

    @classmethod
    def create(cls, url, *, session_options: Optional[Mapping[str, Any]] = None, **kwargs):
        kwargs.setdefault('future', True)
        engine = create_async_engine(url, **kwargs)
        session_options = session_options or {}
        return cls(engine, **session_options)

    async def session_generator(self) -> AsyncGenerator[AsyncSession, Any]:
        async with self.session_maker() as session:
            yield session

    async def execute(
            self,
            statement: Executable,
            params: Optional[_ExecuteParams] = None,
            /,
            *,
            execution_options: Optional[_ExecuteOptions] = None,
            bind_arguments: Optional[Mapping[str, Any]] = None,
            commit: bool = False,
            on_close_pre: Callable[[Result], _T] = None,
            **kw: Any,
    ) -> Union[Result, _T]:
        async with self.session_maker() as session:
            result = await session.execute(statement, params, execution_options, bind_arguments, **kw)
            if commit:
                await session.commit()
            if on_close_pre:
                result = on_close_pre(result)
        return result

    async_execute = execute

    async def scalar(
            self,
            statement: Executable,
            params: Optional[_ExecuteParams] = None,
            /,
            *,
            execution_options: Optional[_ExecuteOptions] = None,
            bind_arguments: Optional[Mapping[str, Any]] = None,
            **kw: Any,
    ) -> Any:
        async with self.session_maker() as session:
            return await session.scalar(
                statement,
                params,
                execution_options=execution_options,
                bind_arguments=bind_arguments,
                **kw,
            )

    async def scalars_all(
            self,
            statement: Executable,
            params: Optional[_ExecuteParams] = None,
            /,
            *,
            execution_options: Optional[_ExecuteOptions] = None,
            **kw: Any,
    ) -> List[Any]:
        async with self.session_maker() as session:
            result = await session.scalars(
                statement,
                params,
                execution_options=execution_options,
                **kw,
            )
            return result.all()

    async def get(
            self,
            entity: Type[_T],
            ident: Any,
            /,
            *,
            options: Optional[Sequence[Any]] = None,
            populate_existing: bool = False,
            with_for_update: Optional[Any] = None,
            identity_token: Optional[Any] = None,
            execution_options: Optional[_ExecuteOptions] = None,
    ) -> Optional[_T]:
        async with self.session_maker() as session:
            return await session.get(
                entity,
                ident,
                options=options,
                populate_existing=populate_existing,
                with_for_update=with_for_update,
                identity_token=identity_token,
            )

    async def delete(self, instance: Any) -> None:
        async with self.session_maker() as session:
            async with session.begin():
                await session.delete(instance)


class Database:

    def __init__(self, engine: Engine, **session_options):
        self.engine: Engine = engine
        self.session_maker: Callable[..., Session] = sessionmaker(self.engine, **session_options)

    @classmethod
    def create(cls, url, *, session_options: Optional[Mapping[str, Any]] = None, **kwargs):
        kwargs.setdefault('future', True)
        engine = create_engine(url, **kwargs)
        session_options = session_options or {}
        return cls(engine, **session_options)

    def session_generator(self) -> Generator[Session, Any, None]:
        with self.session_maker() as session:
            yield session

    def execute(
            self,
            statement: Executable,
            params: Optional[_ExecuteParams] = None,
            /,
            *,
            execution_options: Optional[_ExecuteOptions] = None,
            bind_arguments: Optional[Mapping[str, Any]] = None,
            commit: bool = False,
            on_close_pre: Callable[[Result], _T] = None,
            **kw: Any,
    ) -> Union[Result, _T]:
        with self.session_maker() as session:
            result = session.execute(statement, params, execution_options, bind_arguments, **kw)
            if commit:
                session.commit()
            if on_close_pre:
                result = on_close_pre(result)
        return result

    @functools.cached_property
    def async_execute(self):
        return functools.partial(to_thread, self.execute)

    def scalar(
            self,
            statement: Executable,
            params: Optional[_ExecuteParams] = None,
            /,
            *,
            execution_options: Optional[_ExecuteOptions] = None,
            bind_arguments: Optional[Mapping[str, Any]] = None,
            **kw: Any,
    ) -> Any:
        with self.session_maker() as session:
            return session.scalar(
                statement,
                params,
                execution_options=execution_options,
                bind_arguments=bind_arguments,
                **kw,
            )

    def scalars_all(
            self,
            statement: Executable,
            params: Optional[_ExecuteParams] = None,
            /,
            *,
            execution_options: Optional[_ExecuteOptions] = None,
            bind_arguments: Optional[Mapping[str, Any]] = None,
            **kw: Any,
    ) -> List[Any]:
        with self.session_maker() as session:
            return session.scalars(
                statement,
                params,
                execution_options=execution_options,
                bind_arguments=bind_arguments,
                **kw,
            ).all()

    def get(
            self,
            entity: Type[_T],
            ident: Any,
            /,
            *,
            options: Optional[Sequence[Any]] = None,
            populate_existing: bool = False,
            with_for_update: Optional[Any] = None,
            identity_token: Optional[Any] = None,
            execution_options: Optional[_ExecuteOptions] = None,
    ) -> Optional[_T]:
        with self.session_maker() as session:
            return session.get(
                entity,
                ident,
                options=options,
                populate_existing=populate_existing,
                with_for_update=with_for_update,
                identity_token=identity_token,
            )

    def delete(self, instance: Any) -> None:
        with self.session_maker() as session:
            with session.begin():
                session.delete(instance)
