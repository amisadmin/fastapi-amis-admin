from typing import Any

from sqlalchemy import Column
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import ColumnProperty, declared_attr
from sqlalchemy.util import classproperty, memoized_property
from sqlmodel import main as sqlmodel_main
from sqlmodel._compat import IS_PYDANTIC_V2, SQLModelConfig, Undefined, get_type_from_field
from sqlmodel.main import SQLModel as _SQLModel
from sqlmodel.main import get_column_from_field as _get_column_from_field

from .enums import Choices
from .sqltypes import ChoiceType

try:
    from functools import cached_property
except ImportError:
    cached_property = memoized_property

SaColumnTypes = (
    Column,
    ColumnProperty,
    hybrid_property,
    declared_attr,
)
__sqlmodel_ignored_types__ = (classproperty, cached_property, memoized_property, hybrid_method, *SaColumnTypes)


def get_column_from_field(field: Any) -> Column:  # type: ignore
    """support for choices enums"""
    if IS_PYDANTIC_V2:
        field_info = field
    else:
        field_info = field.field_info
    sa_column = getattr(field_info, "sa_column", Undefined)
    if isinstance(sa_column, SaColumnTypes):
        return sa_column
    if isinstance(field_info.default, SaColumnTypes):
        return field_info.default
    type_ = get_type_from_field(field)
    # Support for choices enums
    if issubclass(type_, Choices):
        field_info.sa_type = ChoiceType(type_)
    return _get_column_from_field(field)


class SQLModel(_SQLModel):
    # support cached_property,hybrid_method,hybrid_property
    if IS_PYDANTIC_V2:
        model_config = SQLModelConfig(
            from_attributes=True,
            ignored_types=__sqlmodel_ignored_types__,
        )
    else:

        class Config:
            orm_mode = True
            keep_untouched = __sqlmodel_ignored_types__


# patch sqlmodel
sqlmodel_main.get_column_from_field = get_column_from_field
sqlmodel_main.SQLModel = SQLModel
