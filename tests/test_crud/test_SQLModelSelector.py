from fastapi_amis_admin.crud import SQLModelSelector
from tests.models import Article, User


async def test_fields():
    class ArticleSelector(SQLModelSelector):
        router_prefix = "/user"
        fields = [
            "id",
            Article.title,
            User.username,
            User.password.label("pwd"),
            "not_exist",
        ]

    selector = ArticleSelector(Article)
    assert "id" in selector._select_entities
    assert "title" in selector._select_entities
    assert "user__username" in selector._select_entities
    assert "pwd" in selector._select_entities
    assert "not_exist" not in selector._select_entities
    assert selector._filter_entities == selector._select_entities


async def test_list_filter():
    class ArticleSelector(SQLModelSelector):
        router_prefix = "/user"
        list_filter = [
            "id",
            Article.title,
            User.username,
            User.password.label("pwd"),
            "not_exist",
        ]

    selector = ArticleSelector(Article)
    assert "id" in selector._filter_entities
    assert "title" in selector._filter_entities
    assert "user__username" in selector._filter_entities
    assert "pwd" in selector._filter_entities
    assert "not_exist" not in selector._filter_entities
    assert selector._filter_entities != selector._select_entities
