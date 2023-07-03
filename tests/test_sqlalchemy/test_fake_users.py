from tests.test_sqlalchemy.models import User


async def test_fake_users(prepare_database, fake_users, async_session):
    print("get_users", fake_users)
    for i in range(1, 6):
        user = await async_session.get(User, i)
        assert user.username == f"User_{i}"
        assert user.username == fake_users[i - 1].username
