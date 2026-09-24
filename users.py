"""Functions for creating and searching users."""

from models import User


def _next_id(users: list[User]) -> int:
    """Return the next user identifier."""
    return max((user.id for user in users), default=0) + 1


def add_user(
    users: list[User],
    name: str,
    email: str,
    stack: str = "",
    experience: int = 0,
) -> None:
    """Create a user and add it to the collection."""
    normalized_email = email.strip().lower()
    if any(user.email == normalized_email for user in users):
        raise ValueError("Пользователь с таким email уже существует.")
    users.append(User(_next_id(users), name, email, stack, experience))


def find_user_by_id(users: list[User], user_id: int) -> User:
    """Return a user by identifier or raise KeyError."""
    for user in users:
        if user.id == user_id:
            return user
    raise KeyError(f"Пользователь с ID {user_id} не найден.")


def find_users(users: list[User], query: str) -> list[User]:
    """Find users by a substring in the name or email."""
    normalized_query = query.strip().lower()
    return [
        user
        for user in users
        if normalized_query in user.name.lower()
        or normalized_query in user.email
    ]


def show_users(users: list[User]) -> None:
    """Print user objects."""
    if not users:
        print("Пользователей пока нет.")
        return
    for user in users:
        print(user)
