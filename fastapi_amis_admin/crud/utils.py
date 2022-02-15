from enum import Enum
from typing import Optional, Type, List, Set, Union, Iterable
from fastapi.params import Path
from pydantic import BaseModel, BaseConfig
from pydantic.fields import ModelField
from pydantic.utils import smart_deepcopy
from .schema import Paginator


def validator_skip_blank(cls, v, config: BaseConfig, field: ModelField, *args, **kwargs):
    if isinstance(v, str):
        v = v or None
        if issubclass(field.type_, Enum) and issubclass(field.type_, int) and v:
            v = int(v)
    return v


def schema_create_by_schema(schema_cls: Type[BaseModel], schema_name: str, include: Set[str] = None,
                            exclude: Set[str] = None,
                            set_none: bool = False) -> Type[BaseModel]:
    schema_fields = smart_deepcopy(schema_cls.__dict__['__fields__'])
    exclude = exclude or {}
    include = include or {}
    fields = {name: schema_fields[name] for name in include
              if name in schema_fields
              } or {
                 name: schema_fields[name] for name in schema_fields
                 if name not in exclude
             }
    return schema_create_by_modelfield(schema_name, fields.values(), set_none=set_none)


def schema_create_by_modelfield(schema_name: str, modelfields: Iterable[ModelField],
                                set_none: bool = False, **kwargs) -> Type[BaseModel]:
    dct = {'__fields__': {}, '__annotations__': {}}
    for modelfield in modelfields:
        if set_none:
            modelfield.required = False
            modelfield.allow_none = True
            if not modelfield.pre_validators:
                modelfield.pre_validators = [validator_skip_blank]
            else:
                modelfield.pre_validators.insert(0, validator_skip_blank)
        dct['__fields__'][modelfield.name] = modelfield
        dct['__annotations__'][modelfield.name] = modelfield.type_
    dct.update(kwargs)
    return type(schema_name, (BaseModel,), dct)  # type: ignore


def paginator_factory(perPage_max: Optional[int] = None) -> Type[Paginator]:
    class PaginatorCls(Paginator):
        perPageMax = perPage_max

    return PaginatorCls


def parser_str_set_list(set_str: Union[int, str]) -> List[str]:
    if isinstance(set_str, int):
        return [str(set_str)]
    elif not isinstance(set_str, str):
        return []
    return list(set(set_str.split(',')))


def parser_item_id(item_id: str = Path(..., min_length=1, title='pk', example='1,2,3',
                                       description='Primary key or list of primary keys')) -> List[str]:
    return parser_str_set_list(set_str=item_id)
