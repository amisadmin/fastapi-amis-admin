from datetime import datetime
from typing import List

from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from tests.models.schemas import (
    ArticleContentSchema,
    ArticleSchema,
    ArticleTagLinkSchema,
    CategorySchema,
    TagSchema,
    UserSchemaBase,
)


class Base(DeclarativeBase):
    pass


class PkModelMixin(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)


class CreateTimeModelMixin(Base):
    __abstract__ = True
    create_time: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class User(PkModelMixin, CreateTimeModelMixin):
    __tablename__ = "user"
    __pydantic_model__ = UserSchemaBase

    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), default="")
    address: Mapped[list] = mapped_column(JSON, default=[])
    attach: Mapped[dict] = mapped_column(JSON, default={})
    articles: Mapped[List["Article"]] = relationship("Article", back_populates="user")


class Category(PkModelMixin, CreateTimeModelMixin):
    __tablename__ = "category"
    __pydantic_model__ = CategorySchema

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(100), default="")
    articles: Mapped[List["Article"]] = relationship("Article", back_populates="category")


class ArticleTagLink(Base):
    __tablename__ = "article_tag_link"
    __pydantic_model__ = ArticleTagLinkSchema

    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey("tag.id"), primary_key=True, default=None)
    article_id: Mapped[int] = mapped_column(Integer, ForeignKey("article.id"), primary_key=True, default=None)


class Tag(PkModelMixin, CreateTimeModelMixin):
    __tablename__ = "tag"
    __pydantic_model__ = TagSchema

    name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    articles: Mapped[List["Article"]] = relationship(
        "Article",
        back_populates="tags",
        secondary="article_tag_link",
        primaryjoin="ArticleTagLink.article_id == Tag.id",
        secondaryjoin="Article.id == ArticleTagLink.tag_id",
        viewonly=True,
    )


class ArticleContent(PkModelMixin):
    __tablename__ = "article_content"
    __pydantic_model__ = ArticleContentSchema

    content: Mapped[str] = mapped_column(String(100))
    article: Mapped["Article"] = relationship("Article", back_populates="content")


class Article(PkModelMixin, CreateTimeModelMixin):
    __tablename__ = "article"
    __pydantic_model__ = ArticleSchema

    title: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(100))
    status: Mapped[int] = mapped_column(Integer, default=0)

    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("category.id"))
    category: Mapped[Category] = relationship("Category", back_populates="articles")

    content_id: Mapped[int] = mapped_column(Integer, ForeignKey("article_content.id"))
    content: Mapped[ArticleContent] = relationship("ArticleContent", back_populates="article")

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    user: Mapped[User] = relationship("User", back_populates="articles")

    tags: Mapped[List[Tag]] = relationship(
        "Tag",
        back_populates="articles",
        secondary="article_tag_link",
        primaryjoin="ArticleTagLink.article_id == Article.id",
        secondaryjoin="Tag.id == ArticleTagLink.tag_id",
        viewonly=True,
    )

    @hybrid_property
    def content_text(self):
        return self.content.content if self.content else None
