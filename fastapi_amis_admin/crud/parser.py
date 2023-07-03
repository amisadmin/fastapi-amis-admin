import datetime
from functools import lru_cache
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Type, TypeVar, Union

from fastapi.utils import create_cloned_field
from pydantic import BaseConfig, BaseModel
from pydantic.datetime_parse import parse_date, parse_datetime
from pydantic.fields import FieldInfo, ModelField
from sqlalchemy import Column, Table
from sqlalchemy.engine import Row
from sqlalchemy.orm import InstrumentedAttribute, RelationshipProperty
from sqlalchemy.sql import Select
from sqlalchemy.sql.elements import Label

SqlaInsAttr = Union[str, InstrumentedAttribute]
SqlaField = Union[SqlaInsAttr, Label]
SqlaPropertyField = Union[SqlaInsAttr, "PropertyField"]
ModelFieldType = Union[ModelField, "ModelFieldProxy"]
InspecTableType = TypeVar("InspecTableType")  # SQLModel,DeclarativeMeta,InspectTable


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


def get_inspect_table_fields(inspec_table: Type[InspecTableType]) -> Dict[str, ModelField]:
    """Get pydantic ModelField from sqlalchemy InspecTable."""
    if hasattr(inspec_table, "__fields__"):
        return inspec_table.__fields__
    elif hasattr(inspec_table, "__schema__") and isinstance(inspec_table.__schema__, BaseModel):
        return inspec_table.__schema__.__fields__
    return {}


class InspecTableParser:
    _name_format = "{model_name}_{field_name}"
    _alias_format = "{table_name}__{field_key}"

    def __init__(self, inspec_table: Type[InspecTableType]):
        assert hasattr(inspec_table, "__table__"), "inspec_table must be has __table__ attribute."
        self.inspec_table = inspec_table
        self.__table__: Table = self.inspec_table.__table__
        self.__fields__ = get_inspect_table_fields(inspec_table)

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
            modelfield = get_inspect_table_fields(field.class_).get(field.key, None)
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
        return [self.get_alias(row._keymap[field][2][1]) for field in row._fields]

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
            field = self.inspec_table.__dict__.get(field, None)
        if isinstance(field, InstrumentedAttribute):
            return field
        return None

    def filter_insfield(
        self,
        fields: Iterable[Union[SqlaField, Any]],
        save_class: Tuple[Union[type, Tuple[Any, ...]], ...] = None,
        exclude_prop: Tuple[Union[type, Tuple[Any, ...]], ...] = (RelationshipProperty,),
    ) -> List[Union[InstrumentedAttribute, Any]]:
        result = []
        for field in fields:
            insfield = self.get_insfield(field)
            if insfield is not None:
                if isinstance(insfield.prop, exclude_prop):
                    continue
            elif save_class and isinstance(field, save_class):
                insfield = field
            if insfield is not None:
                result.append(insfield)
        return sorted(set(result), key=result.index)  # 去重复并保持原顺序


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


def get_modelfield_by_alias(model: Type[BaseModel], alias: str) -> Optional[ModelField]:
    """Get the field of the model according to the alias"""
    for field in model.__fields__.values():
        if field.alias == alias:
            return field
    return None
