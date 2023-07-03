from datetime import datetime
from typing import List

from sqlalchemy import JSON, Column, String
from sqlmodel import Field, SQLModel


class PkModelMixin(SQLModel):
    id: int = Field(default=None, primary_key=True, nullable=False)


class CreateTimeModelMixin(SQLModel):
    create_time: datetime = Field(default_factory=datetime.utcnow, title="Create Time")


class User(PkModelMixin, CreateTimeModelMixin, table=True):
    __tablename__ = "tmp_user"
    username: str = Field(
        title="Username",
        sa_column=Column(String(100), unique=True, index=True, nullable=False),
    )
    password: str = Field(default="", title="Password")
    address: List[str] = Field(None, title="Address", sa_column=Column(JSON))
    attach: dict = Field(None, title="Attach", sa_column=Column(JSON))
