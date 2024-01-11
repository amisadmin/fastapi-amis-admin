from typing import Type

from sqlalchemy import types

from ._enums import Choices


class BaseChoicesType(types.TypeDecorator):
    def __init__(self, choices: Type[Choices] = None, impl=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = choices

    def process_bind_param(self, value, dialect):
        if value is not None and isinstance(value, Choices):
            return value.value
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            if issubclass(self.choices, int):
                value = int(value)
            return self.choices(value)
        return value


class TextChoicesType(BaseChoicesType):
    impl = types.CHAR(40)
    cache_ok = True


class IntegerChoicesType(BaseChoicesType):
    impl = types.Integer
    cache_ok = True


def ChoiceType(choices: Type[Choices], *args, **kwargs):
    return (IntegerChoicesType if issubclass(choices, int) else TextChoicesType)(choices, *args, **kwargs)
