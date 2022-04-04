from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, Text
from sqlmodel import SQLModel, Field, Relationship


class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(title='CategoryName', sa_column=Column(String(100), unique=True, index=True, nullable=False))
    description: str = Field(default='', title='CategoryDescription')
    articles: List["Article"] = Relationship(back_populates="category")
    create_time: datetime = Field(default_factory=datetime.utcnow, title='创建时间')

class ArticleTagLink(SQLModel, table=True):
    tag_id: Optional[int] = Field(
        default=None, foreign_key="tag.id", primary_key=True
    )
    article_id: Optional[int] = Field(
        default=None, foreign_key="article.id", primary_key=True
    )


class Tag(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(..., title='TagName', sa_column=Column(String(255), unique=True, index=True, nullable=False))
    articles: List["Article"] = Relationship(back_populates="tags", link_model=ArticleTagLink)


class ArticleContent(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    content: str = Field(title='ArticleContent', sa_column=Column(Text, default=''))
    article: Optional["Article"] = Relationship(back_populates="content")


class Article(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    title: str = Field(title='ArticleTitle',max_length=200)
    description: str = Field(default='', title='ArticleDescription', sa_column=Column(Text))
    status: int = Field(None, title='status')
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", title='CategoryId')
    category: Optional[Category] = Relationship(back_populates="articles")
    content_id: Optional[int] = Field(default=None, foreign_key="articlecontent.id", title='ArticleContentId')
    content: Optional[ArticleContent] = Relationship(back_populates="article")
    tags: List[Tag] = Relationship(back_populates="articles", link_model=ArticleTagLink)
    create_time: datetime = Field(default_factory=datetime.utcnow, title='创建时间')