from typing import List, Type

from fastapi import APIRouter

from ._sqlalchemy import SqlalchemyCrud, SqlalchemySelector
from .base import SchemaModelT
from .parser import SqlaField
from .utils import SqlalchemyDatabase

SQLModelSelector = SqlalchemySelector


class SQLModelCrud(SqlalchemyCrud):
    def __init__(
        self,
        model: Type[SchemaModelT],
        engine: SqlalchemyDatabase,
        fields: List[SqlaField] = None,
        router: APIRouter = None,
    ) -> None:
        SqlalchemyCrud.__init__(self, model, engine, model, fields, router)

    @property
    def schema_name_prefix(self):
        if self.__class__ is SQLModelCrud:
            return self.model.__name__
        return super().schema_name_prefix
