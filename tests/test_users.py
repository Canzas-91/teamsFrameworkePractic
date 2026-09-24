import pytest

from models import User
from users import add_user, find_user_by_id, find_users


def test_add_and_find_user_object() -> None:
    users: list[User] = []
    add_user(users, "Мария", "MARIA@example.com", "Python", 2)
    user = users[0]
    assert user.id == 1
    assert user.email == "maria@example.com"
    assert find_user_by_id(users, 1) is user
    assert find_users(users, "maria") == [user]
    assert "Мария" in str(user)


def test_user_from_data() -> None:
    user = User.from_data(
        {
            "id": 7,
            "name": "Иван",
            "email": "ivan@example.com",
            "stack": "Python",
            "experience": 1,
        }
    )
    assert user.id == 7
    assert user.stack == "python"
    assert user.experience == 1


def test_duplicate_email_is_forbidden() -> None:
    users: list[User] = []
    add_user(users, "Мария", "maria@example.com")
    with pytest.raises(ValueError):
        add_user(users, "Маша", "MARIA@example.com")
