import warnings

from ._sqlalchemy import SqlalchemyCrud, SqlalchemySelector

warnings.warn(
    "fastapi_amis_admin.crud._sqlmodel is deprecated, use fastapi_amis_admin.crud._sqlalchemy instead.",
    DeprecationWarning,
    stacklevel=2,
)
SQLModelSelector = SqlalchemySelector
"""Deprecated, use SqlalchemySelector instead."""
SQLModelCrud = SqlalchemyCrud
"""Deprecated, use SqlalchemyCrud instead."""
