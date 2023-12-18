from .fields import Field

try:
    from sqlmodelx import SQLModel
except ImportError:
    from sqlmodel import SQLModel

try:
    from sqlmodelx.enums import Choices, IntegerChoices, TextChoices
    from sqlmodelx.sqltypes import ChoiceType
except ImportError:
    from ._enums import Choices, IntegerChoices, TextChoices
    from ._sqltypes import ChoiceType
