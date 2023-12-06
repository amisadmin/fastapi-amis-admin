from typing import Type

from sqlalchemy import types
from sqlalchemy.engine import Dialect

from .enums import Choices


class ChoiceType(types.TypeDecorator):
    impl = types.CHAR
    cache_ok = True

    def __init__(self, choices: Type[Choices], impl=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = choices

    @property
    def python_type(self):
        return self.impl.python_type

    def load_dialect_impl(self, dialect: Dialect):
        return dialect.type_descriptor(types.CHAR(20))

    def process_bind_param(self, value, dialect):
        if value and isinstance(value, Choices):
            return value.value
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            if issubclass(self.choices, int):
                value = int(value)
            return self.choices(value)
        return value
