from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class PkSchemaMixin(BaseModel):
    id: int = Field(default=None, primary_key=True, nullable=False)

    class Config:
        orm_mode = True


class CreateTimeSchemaMixin(BaseModel):
    create_time: datetime = Field(default_factory=datetime.utcnow, title="Create Time")


class UserSchemaBase(PkSchemaMixin, CreateTimeSchemaMixin):
    username: str = Field(title="Username")
    password: str = Field(default="", title="Password")
    address: List[str] = Field(
        None,
        title="Address",
    )
    attach: dict = Field(None, title="Attach")


class UserSchema(UserSchemaBase):
    articles: List["ArticleSchema"] = []


class CategorySchema(PkSchemaMixin, CreateTimeSchemaMixin):
    name: str = Field(title="CategoryName")
    description: str = Field(default="", title="CategoryDescription")

    # articles: List["ArticleSchema"] = []


class ArticleTagLinkSchema(BaseModel):
    tag_id: int = None
    article_id: int = None


class TagSchema(PkSchemaMixin, CreateTimeSchemaMixin):
    name: str = Field(title="TagName", max_length=255)

    # articles: List["ArticleSchema"] = []


class ArticleContentSchema(PkSchemaMixin):
    content: str = Field(title="ArticleContent")
    # article: Optional["ArticleSchema"] = None


class ArticleSchema(PkSchemaMixin, CreateTimeSchemaMixin):
    title: str = Field(title="ArticleTitle", max_length=200)
    description: str = Field(default="", title="ArticleDescription")
    status: int = Field(default=0, title="ArticleStatus")

    category_id: int = Field(default=None, title="ArticleCategoryID")
    category: CategorySchema = None

    content_id: int = Field(default=None, title="ArticleContentID")
    content: ArticleContentSchema = None

    user_id: int = Field(default=None, title="ArticleUserID")
    user: UserSchemaBase = None  # Avoid circular references

    tags: List[TagSchema] = []

    content_text: str = None


UserSchema.update_forward_refs()
ArticleTagLinkSchema.update_forward_refs()
