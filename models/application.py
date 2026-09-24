"""Application entity connecting a user, team and role."""

from .role import Role
from .team import Team
from .user import User


class Application:
    """A user's application for a team role."""

    STATUSES = {"pending", "accepted", "rejected", "cancelled"}

    def __init__(
        self,
        application_id: int,
        team: Team,
        applicant: User,
        role: Role,
        status: str = "pending",
    ) -> None:
        if application_id < 1:
            raise ValueError("ID заявки должен быть положительным.")
        if status not in self.STATUSES:
            raise ValueError("Неизвестный статус заявки.")

        self.id = application_id
        self.team = team
        self.applicant = applicant
        self.role = role
        self.status = status

    def cancel(self) -> None:
        """Cancel a pending application."""
        if self.status != "pending":
            raise ValueError("Отменить можно только ожидающую заявку.")
        self.status = "cancelled"

    def review(self, decision: str) -> None:
        """Accept or reject a pending application."""
        if decision not in {"accepted", "rejected"}:
            raise ValueError("Решение должно быть accepted или rejected.")
        if self.status != "pending":
            raise ValueError("Заявка уже рассмотрена или отменена.")
        if decision == "accepted":
            self.team.add_member(self.applicant, self.role)
        self.status = decision

    def __str__(self) -> str:
        return (
            f"#{self.id}: {self.applicant.name} -> "
            f"{self.team.name}, роль {self.role.name}, статус: {self.status}"
        )
