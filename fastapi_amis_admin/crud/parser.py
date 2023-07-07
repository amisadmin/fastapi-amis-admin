import datetime
from functools import lru_cache
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Type, TypeVar, Union

import sqlalchemy
from fastapi.utils import create_cloned_field
from pydantic import BaseConfig, BaseModel
from pydantic.datetime_parse import parse_date, parse_datetime
from pydantic.fields import Field, FieldInfo, ModelField
from sqlalchemy import Column, String, Table
from sqlalchemy.engine import Row
from sqlalchemy.orm import ColumnProperty, DeclarativeMeta, InstrumentedAttribute, RelationshipProperty
from sqlalchemy.sql import Select
from sqlalchemy.sql.elements import Label

from fastapi_amis_admin.crud.base import SchemaModelT
from fastapi_amis_admin.crud.utils import schema_create_by_modelfield

SqlaInsAttr = Union[str, InstrumentedAttribute]
SqlaField = Union[SqlaInsAttr, Label]
SqlaPropertyField = Union[SqlaInsAttr, "PropertyField"]
ModelFieldType = Union[ModelField, "ModelFieldProxy"]
SchemaT = TypeVar("SchemaT", bound=BaseModel)
TableModel = DeclarativeMeta

if sqlalchemy.__version__.startswith("2."):
    from sqlalchemy.orm import DeclarativeBase

    TableModel = Union[DeclarativeMeta, DeclarativeBase]
try:  # sqlmodel orm
    from sqlmodel import SQLModel

    TableModel = Union[TableModel, SQLModel]
except ImportError:
    pass
TableModelT = TypeVar("TableModelT", bound=TableModel)


class ModelFieldProxy:
    """Proxy for pydantic ModelField to modify some attributes without affecting the original ModelField.
    Reduce the deep copy of the original ModelField to improve performance.
    """

    def __init__(self, modelfield: ModelField, update: Dict[str, Any] = None):
        self.__dict__["_modelfield"] = modelfield
        self.__dict__["_update"] = update or {}

    def __getattr__(self, item):
        if item == "new_model_field":
            return self.__dict__[item]
        return self.__dict__["_update"].get(item, getattr(self.__dict__["_modelfield"], item))

    def __setattr__(self, key, value):
        self.__dict__["_update"][key] = value

    def cloned_field(self):
        modelfield = create_cloned_field(self.__dict__["_modelfield"])
        for k, v in self.__dict__["_update"].items():
            setattr(modelfield, k, v)
        return modelfield


class TableModelParser:
    _name_format = "{model_name}_{field_name}"
    _alias_format = "{table_name}__{field_key}"

    def __init__(self, table_model: Type[TableModelT]):
        assert hasattr(table_model, "__table__"), "table_model must be has __table__ attribute."
        self.table_model = table_model
        self.__table__: Table = self.table_model.__table__  # type: ignore
        self.__fields__ = self.get_table_model_fields(table_model)

    @staticmethod
    def get_table_model_insfields(table_model: Type[TableModelT]) -> Dict[str, InstrumentedAttribute]:
        """Get sqlalchemy InstrumentedAttribute from InspecTable."""
        return {name: field for name, field in table_model.__dict__.items() if isinstance(field, InstrumentedAttribute)}

    @staticmethod
    def get_table_model_fields(table_model: Type[TableModelT]) -> Dict[str, ModelField]:
        """Get pydantic ModelField from sqlalchemy InspecTable."""
        if hasattr(table_model, "__fields__"):
            return table_model.__fields__
        elif hasattr(table_model, "__schema__") and issubclass(table_model.__schema__, BaseModel):
            return table_model.__schema__.__fields__
        return {}

    @staticmethod
    def get_table_model_schema(table_model: Type[TableModelT]) -> Optional[Type[BaseModel]]:
        """Get pydantic schema from sqlalchemy InspecTable."""

        if issubclass(table_model, BaseModel):
            return table_model
        elif hasattr(table_model, "__schema__") and issubclass(table_model.__schema__, BaseModel):
            return table_model.__schema__
        elif hasattr(table_model, "__fields__"):
            table_model.__schema__ = schema_create_by_modelfield(
                table_model.__name__, table_model.__fields__.values(), orm_mode=True
            )
            return table_model.__schema__
        insfields = TableModelParser.get_table_model_insfields(table_model)
        if not insfields:
            return None
        modelfields = [insfield_to_modelfield(insfield) for insfield in insfields.values()]
        modelfields = list(filter(None, modelfields))
        table_model.__schema__ = schema_create_by_modelfield(table_model.__name__, modelfields, orm_mode=True)
        return table_model.__schema__

    def get_modelfield(self, field: Union[ModelField, SqlaInsAttr, Label], clone: bool = False) -> Optional[ModelFieldType]:
        """Get pydantic ModelField from sqlmodel field.
        Args:
            field:  ModelField, SQLModelField or Label
            clone:  Whether to return a cloned of the original ModelField.

        Returns:  pydantic ModelField or ModelFieldProxy.
        """
        modelfield = None
        update = {}
        if isinstance(field, InstrumentedAttribute):
            modelfield = self.get_table_model_fields(field.class_).get(field.key, None)
            if not modelfield:  # Maybe it's a declared_attr or column_property.
                return None
            if field.class_.__table__ is not self.__fields__:
                update = {
                    "name": self.get_name(field),
                    "alias": self.get_alias(field),
                }
        elif isinstance(field, str) and field in self.__fields__:
            modelfield = self.__fields__[field]
        elif isinstance(field, ModelField):
            modelfield = field
        elif isinstance(field, Label):
            modelfield = _get_label_modelfield(field)
        if not modelfield:
            return None
        field_proxy = ModelFieldProxy(modelfield, update=update)
        return field_proxy.cloned_field() if clone else field_proxy

    def get_column(self, field: SqlaInsAttr) -> Optional[Column]:
        """sqlalchemy Column"""
        if isinstance(field, InstrumentedAttribute):
            return field.class_.__table__.columns.get(field.key)
        elif isinstance(field, str):
            return self.__table__.columns.get(field)
        return None

    def get_alias(self, field: Union[Column, SqlaInsAttr, Label]) -> str:
        if isinstance(field, Column):
            return (
                field.name
                if field.table.name == self.__table__.name
                else self._alias_format.format(table_name=field.table.name, field_key=field.name)
            )
        elif isinstance(field, InstrumentedAttribute):
            return (
                field.key
                if field.class_.__tablename__ == self.__table__.name
                else self._alias_format.format(
                    table_name=field.class_.__tablename__,
                    field_key=field.expression.key,
                )
            )
        elif isinstance(field, Label):
            return field.key
        elif isinstance(field, str) and field in self.__fields__:
            return field
        return ""

    def get_name(self, field: InstrumentedAttribute) -> str:
        return (
            field.key
            if field.class_.__tablename__ == self.__table__.name
            else self._name_format.format(model_name=field.class_.__tablename__, field_name=field.key)
        )

    def get_row_keys(self, row: Row) -> List[str]:
        """sqlalchemy row keys"""
        keymap = row._parent._keymap
        return [self.get_alias(keymap[field_name][2][1]) for field_name in row._fields]

    def get_select_keys(self, stmt: Select) -> List[str]:
        """sqlalchemy select keys"""
        return [self.get_alias(column) for column in stmt.exported_columns]

    def conv_row_to_dict(self, rows: List[Row]) -> List[Dict[str, Any]]:
        """sqlalchemy row to dict"""
        if not rows:
            return []
        keys = self.get_row_keys(rows[0])
        return [dict(zip(keys, row)) for row in rows]

    def get_insfield(self, field: SqlaInsAttr) -> Optional[InstrumentedAttribute]:
        if isinstance(field, str):
            field = self.table_model.__dict__.get(field, None)
        if isinstance(field, InstrumentedAttribute):
            return field
        return None

    def filter_insfield(
        self,
        fields: Iterable[Union[SqlaField, Any]],
        save_class: Tuple[Union[type, Tuple[Any, ...]], ...] = None,
        exclude_property: Tuple[Union[type, Tuple[Any, ...]], ...] = (RelationshipProperty,),
    ) -> List[Union[InstrumentedAttribute, Any]]:
        result = []
        for field in fields:
            insfield = self.get_insfield(field)
            if insfield is not None:
                if isinstance(insfield.property, exclude_property):
                    continue
            elif save_class and isinstance(field, save_class):
                insfield = field
            if insfield is not None:
                result.append(insfield)
        return sorted(set(result), key=result.index)  # 去重复并保持原顺序

    def filter_modelfield(
        self,
        fields: Iterable[Union[SqlaField, Any]],
        save_class: Tuple[Union[type, Tuple[Any, ...]], ...] = (ModelField,),
        exclude: Iterable[str] = None,
    ) -> List[ModelField]:
        exclude = exclude or []
        # Filter out any non-model fields from the read fields
        fields = self.filter_insfield(fields, save_class=save_class)
        modelfields = [self.get_modelfield(ins, clone=True) for ins in fields]
        # Filter out any None values or out excluded fields
        modelfields = [field for field in modelfields if field and field.name not in exclude]
        return modelfields


SQLModelFieldParser = TableModelParser
"""Deprecated, use TableModelParser instead."""


@lru_cache()
def get_python_type_parse(field: Union[InstrumentedAttribute, Column, Label]) -> Callable:
    try:
        python_type = field.expression.type.python_type
        if issubclass(python_type, datetime.date):
            if issubclass(python_type, datetime.datetime):
                return parse_datetime
            return parse_date
        return python_type
    except NotImplementedError:
        return str


def _get_label_modelfield(label: Label) -> ModelField:
    modelfield = getattr(label, "__ModelField__", None)
    if modelfield is None:
        try:
            python_type = label.expression.type.python_type
        except NotImplementedError:
            python_type = str
        modelfield = ModelField(
            name=label.key,
            type_=python_type,
            class_validators={},
            model_config=BaseConfig,
        )
        label.__ModelField__ = modelfield
    return modelfield


def LabelField(label: Label, field: FieldInfo) -> Label:
    """Use for adding FieldInfo to sqlalchemy Label type"""
    modelfield = _get_label_modelfield(label)
    field.alias = label.key
    modelfield.field_info = field
    label.__ModelField__ = modelfield
    return label


class PropertyField(ModelField):
    """Use this to quickly initialize a ModelField, mainly used in schema_read and schema_update"""

    def __init__(
        self,
        *,
        name: str,
        type_: Type[Any],
        required: bool = False,
        field_info: Optional[FieldInfo] = None,
        **kwargs: Any,
    ) -> None:
        kwargs.setdefault("class_validators", {})
        kwargs.setdefault("model_config", BaseConfig)
        super().__init__(name=name, type_=type_, required=required, field_info=field_info, **kwargs)


def get_insfield_by_key(table_model: Type[TableModelT], key: str) -> Optional[InstrumentedAttribute]:
    """Get the field of the model according to the alias"""
    for insfield in table_model.__dict__.values():
        if isinstance(insfield, InstrumentedAttribute) and insfield.key == key:
            return insfield
    return None


def get_modelfield_by_alias(table_model: Type[TableModelT], alias: str) -> Optional[ModelField]:
    """Get the field of the model according to the alias"""
    fields = TableModelParser.get_table_model_fields(table_model).values()
    for field in fields:
        if field.alias == alias:
            return field
    return None


def parse_obj_to_schema(obj: SchemaModelT, schema: Type[SchemaT]) -> SchemaT:
    """parse obj to schema"""
    parse = schema.from_orm if getattr(schema.Config, "orm_mode", False) else schema.parse_obj
    return parse(obj)


def insfield_to_modelfield(insfield: InstrumentedAttribute) -> Optional[ModelField]:
    """InstrumentedAttribute to ModelField"""
    if not isinstance(insfield.property, ColumnProperty):
        return None
    expression = insfield.expression
    field_info_kwargs = {}
    required = not expression.nullable
    default = ...
    if expression.nullable:
        default = None
    if expression.default:
        if expression.default.is_scalar:
            default = expression.default.arg
            required = False
        elif expression.default.is_callable:
            field_info_kwargs["default_factory"] = expression.default.arg
            required = False
    if isinstance(expression.type, String):
        field_info_kwargs["max_length"] = expression.type.length
    if "default_factory" not in field_info_kwargs:
        field_info_kwargs["default"] = default
    return ModelField(
        name=insfield.key,
        type_=expression.type.python_type,
        required=required,
        class_validators={},
        model_config=BaseConfig,
        field_info=Field(
            title=expression.comment,
            **field_info_kwargs,
        ),
    )
