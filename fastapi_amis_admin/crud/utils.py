import warnings
from enum import Enum
from typing import Iterable, List, Set, Type, Union

from fastapi import Depends, Path, Query
from fastapi.utils import create_cloned_field
from pydantic import BaseConfig, BaseModel, Extra
from pydantic.fields import ModelField
from pydantic.main import create_model
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy_database import AsyncDatabase, Database
from typing_extensions import Annotated

from .schema import BaseApiSchema

SqlalchemyDatabase = Union[Engine, AsyncEngine, Database, AsyncDatabase]


def validator_skip_blank(cls, v, config: BaseConfig, field: ModelField, *args, **kwargs):
    if isinstance(v, str):
        if not v:
            if not issubclass(field.type_, str):
                return None
            if issubclass(field.type_, Enum) and "" not in field.type_.__members__:
                return None
            return ""
        if issubclass(field.type_, int):
            v = int(v)
    return v


def schema_create_by_schema(
    schema_cls: Type[BaseModel],
    schema_name: str,
    *,
    include: Set[str] = None,
    exclude: Set[str] = None,
    set_none: bool = False,
    **kwargs,
) -> Type[BaseModel]:
    keys = set(schema_cls.__fields__.keys())
    if include:
        keys &= include
    if exclude:
        keys -= exclude
    fields = {name: create_cloned_field(field) for name, field in schema_cls.__fields__.items() if name in keys}
    return schema_create_by_modelfield(schema_name, fields.values(), set_none=set_none, **kwargs)


def schema_create_by_modelfield(
    schema_name: str,
    modelfields: Iterable[ModelField],
    *,
    set_none: bool = False,
    extra: Extra = Extra.ignore,
    **kwargs,
) -> Type[BaseModel]:
    __config__ = type("Config", (BaseApiSchema.Config,), {"extra": extra, **kwargs})
    model = create_model(schema_name, __config__=__config__)  # type: ignore
    for f in modelfields:
        if set_none:
            f.required = False
            f.allow_none = True
            if not f.pre_validators:
                f.pre_validators = [validator_skip_blank]
            else:
                f.pre_validators.insert(0, validator_skip_blank)
        model.__fields__[f.name] = f
        model.__annotations__[f.name] = f.type_
    return model


IdStrQuery = Annotated[
    str,
    Query(
        title="ids",
        example="1,2,3",
        description="Primary key or list of primary keys",
    ),
]


def parser_str_set_list(item_id: Union[int, str]) -> List[str]:
    if isinstance(item_id, int):
        return [str(item_id)]
    elif not isinstance(item_id, str):
        return []
    return list(set(item_id.split(",")))


ItemIdListDepend = Annotated[List[str], Depends(parser_str_set_list)]


def parser_item_id(
    item_id: str = Path(
        ...,
        min_length=1,
        title="pk",
        example="1,2,3",
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
