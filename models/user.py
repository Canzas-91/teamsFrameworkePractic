"""User entity."""


class User:
    """A registered user who can create or join teams."""

    def __init__(
        self,
        user_id: int,
        name: str,
        email: str,
        stack: str = "",
        experience: int = 0,
    ) -> None:
        if user_id < 1:
            raise ValueError("ID пользователя должен быть положительным.")
        if not name.strip():
            raise ValueError("Имя пользователя не может быть пустым.")
        if not self.validate_email(email):
            raise ValueError("Укажите корректный адрес электронной почты.")
        if experience < 0:
            raise ValueError("Опыт не может быть отрицательным.")

        self.id = user_id
        self.name = name.strip()
        self.email = email.strip().lower()
        self.stack = stack.strip().lower()
        self.experience = experience

    @staticmethod
    def validate_email(email: str) -> bool:
        """Check the basic structure of an email address."""
        local_part, separator, domain = email.strip().partition("@")
        return bool(local_part and separator and "." in domain)

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Create a user from JSON-compatible data."""
        return cls(
            user_id=int(data["id"]),
            name=str(data["name"]),
            email=str(data["email"]),
            stack=str(data.get("stack", "")),
            experience=int(data.get("experience", 0)),
        )

    def to_data(self) -> dict:
        """Return a JSON-compatible representation of the user."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "stack": self.stack,
            "experience": self.experience,
        }

    def __str__(self) -> str:
        profile = self.stack or "стек не указан"
        return (
            f"#{self.id} {self.name} <{self.email}> | "
            f"{profile}, опыт: {self.experience} г."
        )
