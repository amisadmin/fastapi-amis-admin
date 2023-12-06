from importlib.util import find_spec

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.mark.skipif(not find_spec("sqlmodel"), reason="sqlmodel not installed")
async def test_models(prepare_database, async_session: AsyncSession):
    import tests.models.sqlm as models

    user_1 = models.User(username="User_1", password="password_1")
    user_2 = models.User(username="User_2", password="password_2")
    assert user_1.address == []
    assert user_1.attach == {}
    assert user_2.address == []
    assert user_2.attach == {}
    assert user_1.address is not user_2.address
    assert user_1.attach is not user_2.attach
    user_1.attach["a"] = "a"
    user_2.attach["b"] = "b"
    async_session.add(user_1)
    async_session.add(user_2)
    await async_session.commit()
    await async_session.refresh(user_1)
    await async_session.refresh(user_2)
    user_1_ = await async_session.get(models.User, user_1.id)
    user_2_ = await async_session.get(models.User, user_2.id)
    assert user_1_.username == "User_1"
    assert user_1_.attach == {"a": "a"}
    assert user_2_.username == "User_2"
    assert user_2_.attach == {"b": "b"}


@pytest.mark.skipif(not find_spec("sqlmodel"), reason="sqlmodel not installed")
async def test_models_choices_field(prepare_database, async_session: AsyncSession):
    import tests.models.sqlm as models

    article_1 = models.Article(title="Article_1", description="Description_1")
    article_2 = models.Article(title="Article_2", description="Description_2", status=1)
    article_3 = models.Article(title="Article_3", description="Description_3", status=models.ArticleStatusChoices.DELETED)
    assert article_1.status == models.ArticleStatusChoices.PENDING
    assert article_2.status == models.ArticleStatusChoices.PUBLISHED
    assert article_3.status == models.ArticleStatusChoices.DELETED
    async_session.add_all([article_1, article_2, article_3])
    await async_session.commit()
    await async_session.refresh(article_1)
    await async_session.refresh(article_2)
    await async_session.refresh(article_3)
    article_1_ = await async_session.get(models.Article, article_1.id)
    article_2_ = await async_session.get(models.Article, article_2.id)
    article_3_ = await async_session.get(models.Article, article_3.id)
    assert article_1_.status is models.ArticleStatusChoices.PENDING
    assert article_2_.status is models.ArticleStatusChoices.PUBLISHED
    assert article_3_.status is models.ArticleStatusChoices.DELETED
