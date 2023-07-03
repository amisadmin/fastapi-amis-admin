from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# Base.metadata.create_all(engine)


class User(Base):
    __tablename__ = "tmp_user"
    id = Column(Integer, primary_key=True, nullable=False)
    create_time = Column(DateTime, default=datetime.utcnow)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(100))
    address = Column(JSON)
    attach = Column(JSON)
    # articles = relationship("Article", back_populates="user")


class Category(Base):
    __tablename__ = "tmp_category"
    id = Column(Integer, primary_key=True, nullable=False)
    create_time = Column(DateTime, default=datetime.utcnow)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(100))
    # articles = relationship("Article", back_populates="category")
