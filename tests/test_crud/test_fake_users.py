from typing import List

from tests.models.sqla import User


async def test_fake_users(prepare_database, async_session, fake_users: List[User], models):
    for i in range(1, 6):
        user = await async_session.get(models.User, i)
        assert user.username == f"User_{i}"
        assert user.username == fake_users[i - 1].username
