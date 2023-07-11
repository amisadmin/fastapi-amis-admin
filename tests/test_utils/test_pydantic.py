from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union

from fastapi._compat import (
    field_annotation_is_complex,
    field_annotation_is_scalar,
    field_annotation_is_scalar_sequence,
    field_annotation_is_sequence,
)
from pydantic import BaseModel
from typing_extensions import Annotated, Literal, get_origin

from fastapi_amis_admin.models import IntegerChoices
from fastapi_amis_admin.utils.pydantic import annotation_outer_type, scalar_sequence_inner_type, validator_skip_blank


class TestValidatorSkipBlank:
    def test_with_empty_string_and_str_type(self):
        result = validator_skip_blank("", str)
        assert result == ""

    def test_with_empty_string_and_int_type(self):
        result = validator_skip_blank("", int)
        assert result is None

    def test_with_non_empty_string_and_str_type(self):
        result = validator_skip_blank("test", str)
        assert result == "test"

    def test_with_non_empty_string_and_int_type(self):
        result = validator_skip_blank("123", int)
        assert result == 123

    def test_with_integer_and_str_type(self):
        result = validator_skip_blank(123, str)
        assert result == "123"

    def test_with_integer_and_int_type(self):
        result = validator_skip_blank(123, int)
        assert result == 123

    def test_with_enum_and_str_type(self):
        class MyEnum(Enum):
            VALUE = "value"

        result = validator_skip_blank("", MyEnum)
        assert result is None

    def test_with_enum_and_str_type_with_blank_member(self):
        class MyEnum(Enum):
            VALUE = "value"
            BLANK = ""

        result = validator_skip_blank("", MyEnum)
        assert result == ""


class MyModel(BaseModel):
    id: int
    name: str


class TestAnnotationOuterType:
    def test_scalar_type_int(self):
        assert annotation_outer_type(int) == int

    def test_scalar_type_str(self):
        assert annotation_outer_type(str) == str

    def test_scalar_type_list(self):
        assert annotation_outer_type(List[int]) == list

    def test_scalar_type_union(self):
        assert annotation_outer_type(Union[int, str]) == int

    def test_scalar_type_optional(self):
        assert annotation_outer_type(Optional[int]) == int

    def test_scalar_type_ellipsis(self):
        assert annotation_outer_type(Ellipsis) == Any

    def test_scalar_type_literal(self):
        assert annotation_outer_type(Literal[None, "a", "b"]) == str

    def test_scalar_type_enum(self):
        class MyEnum(Enum):
            VALUE = "value"

        assert annotation_outer_type(MyEnum) == MyEnum

        assert annotation_outer_type(Optional[MyEnum]) == MyEnum

    def test_scalar_type_choices(self):
        class UserStatus(IntegerChoices):
            NORMAL = 1, "正常"
            DISABLED = 2, "禁用"

        assert annotation_outer_type(UserStatus) == UserStatus

    def test_scalar_type_dict(self):
        assert annotation_outer_type(Dict[str, int]) == dict

    def test_scalar_type_datetime(self):
        from datetime import datetime

        assert annotation_outer_type(datetime) == datetime

    def test_scalar_type_base_model(self):
        assert annotation_outer_type(MyModel) == MyModel
        assert annotation_outer_type(Optional[MyModel]) == MyModel

    def test_scalar_type_annotated(self):
        assert annotation_outer_type(Annotated[int, "123"]) == int
        assert annotation_outer_type(Annotated[Optional[int], "123"]) == int
        assert annotation_outer_type(Annotated[List[int], "123"]) == list


def test_scalar_sequence_inner_type():
    assert scalar_sequence_inner_type(List[int]) == int
    assert scalar_sequence_inner_type(List[MyModel]) == MyModel
    assert scalar_sequence_inner_type(List[Optional[MyModel]]) == MyModel
    assert scalar_sequence_inner_type(list) == Any
    assert scalar_sequence_inner_type(List[Union[str, int]]) == str
    assert scalar_sequence_inner_type(Annotated[List[Union[str, int]], "123"]) == str


def test_annotation_utils():
    assert field_annotation_is_scalar(str) is True
    assert field_annotation_is_scalar(int) is True
    assert field_annotation_is_scalar(datetime) is True
    assert field_annotation_is_scalar(Optional[str]) is True
    assert field_annotation_is_scalar(Optional[datetime]) is True
    assert field_annotation_is_scalar(Union[datetime, date]) is True
    assert field_annotation_is_scalar_sequence(List[str]) is True
    assert field_annotation_is_scalar_sequence(Set[str]) is True
    assert field_annotation_is_scalar_sequence(list) is True
    assert field_annotation_is_scalar_sequence(tuple) is True
    assert field_annotation_is_scalar_sequence(Optional[Set[str]]) is True
    assert field_annotation_is_scalar(MyModel) is False
    assert field_annotation_is_complex(list) is True
    assert field_annotation_is_complex(MyModel) is True
    assert field_annotation_is_complex(dict) is True
    assert field_annotation_is_complex(Dict[str, Any]) is True
    assert get_origin(Literal[42, 43]) is Literal
    assert get_origin(int) is None
    assert get_origin(Optional[int]) is Union
    assert get_origin(Union[int, str]) is Union
    assert field_annotation_is_sequence(List[str]) is True
    assert field_annotation_is_sequence(List[MyModel]) is True
