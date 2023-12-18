from typing import AbstractSet, Any, Callable, Dict, List, Literal, Mapping, Optional, Sequence, Type, Union

from sqlalchemy import Column
from sqlmodel._compat import Undefined, UndefinedType, post_init_field_info
from sqlmodel.main import FieldInfo, NoArgAnyCallable

from fastapi_amis_admin.amis import FormItem, TableColumn
from fastapi_amis_admin.utils.pydantic import PYDANTIC_V2

if PYDANTIC_V2:
    from pydantic.fields import AliasChoices, AliasPath

    ValidationAliasT = Union[str, AliasPath, AliasChoices, None]
else:
    ValidationAliasT = Optional[str]


def Field(
    default: Any = Undefined,
    *,
    default_factory: Optional[NoArgAnyCallable] = None,
    alias: Optional[str] = None,
    alias_priority: Optional[int] = Undefined,
    validation_alias: ValidationAliasT = Undefined,
    serialization_alias: Optional[str] = Undefined,
    title: Optional[str] = None,
    description: Optional[str] = None,
    examples: Optional[List[Any]] = Undefined,
    exclude: Union[AbstractSet[Union[int, str]], Mapping[Union[int, str], Any], Any] = None,
    include: Union[AbstractSet[Union[int, str]], Mapping[Union[int, str], Any], Any] = None,
    const: Optional[bool] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    multiple_of: Optional[float] = None,
    max_digits: Optional[int] = None,
    decimal_places: Optional[int] = None,
    min_items: Optional[int] = None,
    max_items: Optional[int] = None,
    unique_items: Optional[bool] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    allow_mutation: bool = True,
    regex: Optional[str] = None,
    discriminator: Optional[str] = None,
    repr: bool = True,
    init_var: Optional[bool] = Undefined,
    kw_only: Optional[bool] = Undefined,
    pattern: Optional[str] = Undefined,
    strict: Optional[bool] = Undefined,
    allow_inf_nan: Optional[bool] = Undefined,
    union_mode: Literal["smart", "left_to_right"] = Undefined,
    frozen: Optional[bool] = Undefined,
    validate_default: Optional[bool] = Undefined,
    primary_key: Union[bool, UndefinedType] = Undefined,
    foreign_key: Any = Undefined,
    unique: Union[bool, UndefinedType] = Undefined,
    nullable: Union[bool, UndefinedType] = Undefined,
    index: Union[bool, UndefinedType] = Undefined,
    sa_type: Union[Type[Any], UndefinedType] = Undefined,
    sa_column: Union[Column, UndefinedType] = Undefined,  # type: ignore
    sa_column_args: Union[Sequence[Any], UndefinedType] = Undefined,
    sa_column_kwargs: Union[Mapping[str, Any], UndefinedType] = Undefined,
    schema_extra: Optional[Dict[str, Any]] = None,
    amis_form_item: Union[FormItem, dict, str, Callable] = None,
    amis_filter_item: Union[FormItem, dict, str, Callable] = None,
    amis_table_column: Union[TableColumn, dict, str, Callable] = None,
) -> FieldInfo:
    current_schema_extra = schema_extra or {}
    if amis_form_item:
        current_schema_extra["amis_form_item"] = amis_form_item
    if amis_filter_item:
        current_schema_extra["amis_filter_item"] = amis_filter_item
    if amis_table_column:
        current_schema_extra["amis_table_column"] = amis_table_column
    if PYDANTIC_V2:
        current_schema_extra = {
            "json_schema_extra": current_schema_extra,
            "alias_priority": alias_priority,
            "validation_alias": validation_alias,
            "serialization_alias": serialization_alias,
            "examples": examples,
            "init_var": init_var,
            "kw_only": kw_only,
            "pattern": pattern,
            "strict": strict,
            "allow_inf_nan": allow_inf_nan,
            "union_mode": union_mode,
            "frozen": frozen,
            "validate_default": validate_default,
        }
    field_info = FieldInfo(
        default,
        default_factory=default_factory,
        alias=alias,
        title=title,
        description=description,
        exclude=exclude,
        include=include,
        const=const,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        max_digits=max_digits,
        decimal_places=decimal_places,
        min_items=min_items,
        max_items=max_items,
        unique_items=unique_items,
        min_length=min_length,
        max_length=max_length,
        allow_mutation=allow_mutation,
        regex=regex,
        discriminator=discriminator,
        repr=repr,
        primary_key=primary_key,
        foreign_key=foreign_key,
        unique=unique,
        nullable=nullable,
        index=index,
        sa_type=sa_type,
        sa_column=sa_column,
        sa_column_args=sa_column_args,
        sa_column_kwargs=sa_column_kwargs,
        **current_schema_extra,
    )
    post_init_field_info(field_info)
    return field_info
