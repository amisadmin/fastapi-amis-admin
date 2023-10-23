import warnings
from typing import List, Union

from fastapi import Depends, Path, Query
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy_database import AsyncDatabase, Database
from typing_extensions import Annotated

SqlalchemyDatabase = Union[Engine, AsyncEngine, Database, AsyncDatabase]


IdStrQuery = Annotated[
    str,
    Query(
        title="ids",
        examples=["1", "1,2,3"],
        description="Primary key or list of primary keys",
    ),
]


def parser_str_set_list(item_id: Union[int, str]) -> List[str]:
    if isinstance(item_id, int):
        return [str(item_id)]
    elif not isinstance(item_id, str) or not item_id:
        return []
    return list(set(item_id.split(",")))


ItemIdListDepend = Annotated[List[str], Depends(parser_str_set_list)]


def parser_item_id(
    item_id: str = Path(
        ...,
        min_length=1,
        title="pk",
        examples=["1", "1,2,3"],
        description="Primary key or list of primary keys",
    )
) -> List[str]:
    """Deprecated, use ItemIdListDepend and parser_str_set_list instead"""
    warnings.warn(
        "Deprecated, use ItemIdListDepend and parser_str_set_list instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return parser_str_set_list(item_id)


def get_engine_db(engine: SqlalchemyDatabase) -> Union[Database, AsyncDatabase]:
    if isinstance(engine, (Database, AsyncDatabase)):
        return engine
    if isinstance(engine, Engine):
        return Database(engine)
    if isinstance(engine, AsyncEngine):
        return AsyncDatabase(engine)
    raise TypeError(f"Unknown engine type: {type(engine)}")
