from datetime import datetime
from typing import List, Optional

from sqlalchemy import JSON, Column, String, Text
from sqlmodel import Field, Relationship, SQLModel

Base = SQLModel


class PkModelMixin(SQLModel):
    id: int = Field(default=None, primary_key=True, nullable=False)


class CreateTimeModelMixin(SQLModel):
    create_time: datetime = Field(default_factory=datetime.utcnow, title="Create Time")


class User(PkModelMixin, CreateTimeModelMixin, table=True):
    username: str = Field(
        title="Username",
        sa_column=Column(String(100), unique=True, index=True, nullable=False),
    )
    password: str = Field(default="", title="Password")
    address: List[str] = Field(None, title="Address", sa_column=Column(JSON))
    attach: dict = Field(None, title="Attach", sa_column=Column(JSON))

    articles: List["Article"] = Relationship(back_populates="user")


class Category(PkModelMixin, CreateTimeModelMixin, table=True):
    name: str = Field(
        title="CategoryName",
        sa_column=Column(String(100), unique=True, index=True, nullable=False),
    )
    description: str = Field(default="", title="CategoryDescription")

    articles: List["Article"] = Relationship(back_populates="category")


class ArticleTagLink(SQLModel, table=True):
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
    article_id: Optional[int] = Field(default=None, foreign_key="article.id", primary_key=True)


class Tag(PkModelMixin, CreateTimeModelMixin, table=True):
    name: str = Field(
        ...,
        title="TagName",
        sa_column=Column(String(255), unique=True, index=True, nullable=False),
    )

    articles: List["Article"] = Relationship(back_populates="tags", link_model=ArticleTagLink)


class ArticleContent(PkModelMixin, table=True):
    content: str = Field(title="ArticleContent", sa_column=Column(Text, default=""))
    article: Optional["Article"] = Relationship(back_populates="content")


class Article(PkModelMixin, CreateTimeModelMixin, table=True):
    title: str = Field(title="ArticleTitle", max_length=200)
    description: str = Field(default="", title="ArticleDescription", sa_column=Column(Text))
    status: int = Field(None, title="status")

    category_id: Optional[int] = Field(default=None, foreign_key="category.id", title="CategoryId")
    category: Optional[Category] = Relationship(back_populates="articles")

    content_id: Optional[int] = Field(default=None, foreign_key="articlecontent.id", title="ArticleContentId")
    content: Optional[ArticleContent] = Relationship(back_populates="article")

    user_id: Optional[int] = Field(default=None, foreign_key="user.id", title="Author")
    user: Optional[User] = Relationship(back_populates="articles")

    tags: List[Tag] = Relationship(back_populates="articles", link_model=ArticleTagLink)

    @property
    def content_text(self):
        return self.content.content if self.content else ""
