from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, relationship

from tests.models.schemas import (
    ArticleContentSchema,
    ArticleSchema,
    ArticleTagLinkSchema,
    CategorySchema,
    TagSchema,
    UserSchemaBase,
)

Base = declarative_base()


class PkModelMixin(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, nullable=False)


class CreateTimeModelMixin(Base):
    __abstract__ = True
    create_time = Column(DateTime, default=datetime.utcnow)


class User(PkModelMixin, CreateTimeModelMixin):
    __tablename__ = "user"
    __pydantic_model__ = UserSchemaBase

    username = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(100), default="")
    address = Column(JSON)
    attach = Column(JSON)
    articles = relationship("Article", back_populates="user")


class Category(PkModelMixin, CreateTimeModelMixin):
    __tablename__ = "category"
    __pydantic_model__ = CategorySchema

    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(100), default="")
    articles = relationship("Article", back_populates="category")


class ArticleTagLink(Base):
    __tablename__ = "article_tag_link"
    __pydantic_model__ = ArticleTagLinkSchema

    tag_id = Column(Integer, ForeignKey("tag.id"), primary_key=True, default=None)
    article_id = Column(Integer, ForeignKey("article.id"), primary_key=True, default=None)


class Tag(PkModelMixin, CreateTimeModelMixin):
    __tablename__ = "tag"
    __pydantic_model__ = TagSchema

    name = Column(String(255), unique=True, index=True, nullable=False)
    articles = relationship(
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

    content = Column(String(100))
    article = relationship("Article", back_populates="content")


class Article(PkModelMixin, CreateTimeModelMixin):
    __tablename__ = "article"
    __pydantic_model__ = ArticleSchema

    title = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(100))
    status = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="articles")
    content_id = Column(Integer, ForeignKey("article_content.id"))
    content = relationship("ArticleContent", back_populates="article")
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="articles")
    tags = relationship(
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
