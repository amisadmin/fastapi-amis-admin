from enum import Enum
from typing import Any, Dict, Iterable, List, Set, Type, Union

from fastapi.params import Path
from fastapi.utils import create_cloned_field
from pydantic import BaseConfig, BaseModel, Extra
from pydantic.fields import ModelField
from pydantic.main import ModelMetaclass
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy_database import AsyncDatabase, Database

from .schema import BaseApiSchema

SqlalchemyDatabase = Union[Engine, AsyncEngine, Database, AsyncDatabase]


def validator_skip_blank(cls, v, config: BaseConfig, field: ModelField, *args, **kwargs):
    if isinstance(v, str):
        v = v or None
        if issubclass(field.type_, Enum) and issubclass(field.type_, int) and v:
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
    namespaces: Dict[str, Any] = None,
    extra: Extra = Extra.ignore,
    **kwargs,
) -> Type[BaseModel]:
    namespaces = namespaces or {}
    namespaces["Config"] = type("Config", (BaseApiSchema.Config,), {"extra": extra, **kwargs})
    namespaces.update({"__fields__": {}, "__annotations__": {}})
    for modelfield in modelfields:
        if set_none:
            modelfield.required = False
            modelfield.allow_none = True
            if not modelfield.pre_validators:
                modelfield.pre_validators = [validator_skip_blank]
            else:
                modelfield.pre_validators.insert(0, validator_skip_blank)
        namespaces["__fields__"][modelfield.name] = modelfield
        namespaces["__annotations__"][modelfield.name] = modelfield.type_
    return ModelMetaclass(schema_name, (BaseApiSchema,), namespaces)


def parser_str_set_list(set_str: Union[int, str]) -> List[str]:
    if isinstance(set_str, int):
        return [str(set_str)]
    elif not isinstance(set_str, str):
        return []
    return list(set(set_str.split(",")))


def parser_item_id(
    item_id: str = Path(
        ...,
        min_length=1,
        title="pk",
        example="1,2,3",
        description="Primary key or list of primary keys",
    )
) -> List[str]:
    return parser_str_set_list(set_str=item_id)


def get_engine_db(engine: SqlalchemyDatabase) -> Union[Database, AsyncDatabase]:
    if isinstance(engine, (Database, AsyncDatabase)):
        return engine
    if isinstance(engine, Engine):
        return Database(engine)
    if isinstance(engine, AsyncEngine):
        return AsyncDatabase(engine)
    raise TypeError(f"Unknown engine type: {type(engine)}")
