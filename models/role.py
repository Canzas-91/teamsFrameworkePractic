"""Role entity."""


class Role:
    """A role required by a project team."""

    def __init__(
        self,
        name: str,
        stack: str,
        min_experience: int,
        vacancies: int = 1,
    ) -> None:
        if not name.strip() or not stack.strip():
            raise ValueError("Название роли и стек обязательны.")
        if min_experience < 0 or vacancies < 1:
            raise ValueError(
                "Опыт не может быть отрицательным, мест должно быть > 0."
            )

        self.name = name.strip()
        self.stack = stack.strip().lower()
        self.min_experience = min_experience
        self.vacancies = vacancies

    @classmethod
    def from_data(cls, data: dict) -> "Role":
        """Create a role from JSON-compatible data."""
        return cls(
            name=str(data["name"]),
            stack=str(data["stack"]),
            min_experience=int(data["min_experience"]),
            vacancies=int(data.get("vacancies", 1)),
        )

    def is_suitable_for(self, user: "User") -> bool:
        """Return whether a user's profile meets the role requirements."""
        return (
            self.stack == user.stack.lower()
            and user.experience >= self.min_experience
        )

    def to_data(self) -> dict:
        """Return a JSON-compatible representation of the role."""
        return {
            "name": self.name,
            "stack": self.stack,
            "min_experience": self.min_experience,
            "vacancies": self.vacancies,
        }

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.stack}, опыт от "
            f"{self.min_experience} г., мест: {self.vacancies})"
        )


from .user import User  # noqa: E402
