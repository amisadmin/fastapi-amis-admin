import datetime
from functools import lru_cache
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Type, Union

from pydantic import BaseConfig
from pydantic.datetime_parse import parse_date, parse_datetime
from pydantic.fields import FieldInfo, ModelField
from pydantic.utils import smart_deepcopy
from sqlalchemy import Column
from sqlalchemy.engine import Row
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql import Select
from sqlalchemy.sql.elements import Label
from sqlmodel import SQLModel

SQLModelField = Union[str, InstrumentedAttribute]
SqlField = Union[InstrumentedAttribute, Label]
SQLModelListField = Union[Type[SQLModel], SQLModelField, SqlField]


class SQLModelFieldParser:
    _name_format = "{model_name}_{field_name}"
    _alias_format = "{table_name}__{field_key}"

    def __init__(self, default_model: Type[SQLModel]):
        self.default_model = default_model

    def get_modelfield(self, field: Union[ModelField, SQLModelField, Label], deepcopy: bool = False) -> Optional[ModelField]:
        """pydantic ModelField"""
        modelfield = None
        if isinstance(field, InstrumentedAttribute):
            modelfield = field.class_.__fields__[field.key]
            if deepcopy:
                modelfield = smart_deepcopy(modelfield)
                if field.class_ is not self.default_model:
                    modelfield.name = self.get_name(field)
                    modelfield.alias = self.get_alias(field)
            return modelfield
        elif isinstance(field, str):
            if field in self.default_model.__fields__:
                modelfield = self.default_model.__fields__[field]
        elif isinstance(field, ModelField):
            modelfield = field
        elif isinstance(field, Label):
            return get_label_model_field(field)
        else:  # other
            return None
        if deepcopy:
            modelfield = smart_deepcopy(modelfield)
        return modelfield

    def get_column(self, field: SQLModelField) -> Optional[Column]:
        """sqlalchemy Column"""
        if isinstance(field, InstrumentedAttribute):
            return field.class_.__table__.columns.get(field.key)
        elif isinstance(field, str):
            return self.default_model.__table__.columns.get(field)
        return None

    def get_alias(self, field: Union[Column, SQLModelField, Label]) -> str:
        if isinstance(field, Column):
            return (
                field.name
                if field.table.name == self.default_model.__tablename__
                else self._alias_format.format(table_name=field.table.name, field_key=field.name)
            )
        elif isinstance(field, InstrumentedAttribute):
            return (
                field.key
                if field.class_.__tablename__ == self.default_model.__tablename__
                else self._alias_format.format(
                    table_name=field.class_.__tablename__,
                    field_key=field.expression.key,
                )
            )
        elif isinstance(field, Label):
            return field.key
        elif isinstance(field, str) and field in self.default_model.__fields__:
            return field
        return ""

    def get_name(self, field: InstrumentedAttribute) -> str:
        return (
            field.key
            if field.class_.__tablename__ == self.default_model.__tablename__
            else self._name_format.format(model_name=field.class_.__tablename__, field_name=field.key)
        )

    def get_row_keys(self, row: Row) -> List[str]:
        """sqlalchemy row keys"""
        return [self.get_alias(row._keymap[field][2][1]) for field in row._fields]

    def get_select_keys(self, stmt: Select) -> List[str]:
        """sqlalchemy select keys"""
        return [self.get_alias(column) for column in stmt.exported_columns]

    def conv_row_to_dict(self, rows: Union[Row, List[Row]]) -> Union[None, Dict[str, Any], List[Dict[str, Any]]]:
        """sqlalchemy row to dict"""
        if not rows:
            return None
        elif isinstance(rows, list):
            keys = self.get_row_keys(rows[0])
            data = [dict(zip(keys, row)) for row in rows]
        else:
            keys = self.get_row_keys(rows)
            data = dict(zip(keys, rows))
        return data

    def get_sqlmodel_insfield(self, model: Type[SQLModel]) -> List[InstrumentedAttribute]:
        # 不包括 relationship 字段
        return [model.__dict__[field_name] for field_name in model.__fields__]

    def get_insfield(self, field: SQLModelField) -> Optional[InstrumentedAttribute]:
        if isinstance(field, InstrumentedAttribute):
            return field
        elif isinstance(field, str) and field in self.default_model.__fields__:
            return self.default_model.__dict__[field]

        return None

    def filter_insfield(
        self,
        fields: Iterable[Union[SQLModelListField, Any]],
        save_class: Tuple[Union[type, Tuple[Any, ...]], ...] = None,
    ) -> List[Union[InstrumentedAttribute, Any]]:
        result = []
        for field in fields:
            insfield = self.get_insfield(field)
            if insfield is not None:
                result.append(insfield)
            elif isinstance(field, type) and issubclass(field, SQLModel):
                result.extend(self.get_sqlmodel_insfield(field))
            elif save_class and isinstance(field, save_class):
                result.append(field)
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


def get_label_model_field(label: Label) -> ModelField:
    modelfield = getattr(label, "__ModelField__", None)
    if modelfield is None:
        try:
            python_type = label.expression.type.python_type
        except NotImplementedError:
            python_type = str
        modelfield = ModelField(name=label.key, type_=python_type, class_validators={}, model_config=BaseConfig)
        label.__ModelField__ = modelfield
    return modelfield


def LabelField(label: Label, field: FieldInfo) -> Label:
    modelfield = get_label_model_field(label)
    field.alias = label.key
    modelfield.field_info = field
    label.__ModelField__ = modelfield
    return label
