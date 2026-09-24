"""Team and team membership entities."""

from .role import Role
from .user import User


class TeamMember:
    """A user accepted into a team for a particular role."""

    def __init__(self, user: User, role: Role) -> None:
        self.user = user
        self.role = role

    def __str__(self) -> str:
        return f"{self.user.name} — {self.role.name}"


class Team:
    """A project team created by a user."""

    def __init__(
        self,
        team_id: int,
        name: str,
        creator: User,
        description: str = "",
        roles: list[Role] | None = None,
        members: list[TeamMember] | None = None,
    ) -> None:
        if team_id < 1:
            raise ValueError("ID команды должен быть положительным.")
        if not name.strip():
            raise ValueError("Название команды обязательно.")

        self.id = team_id
        self.name = name.strip()
        self.creator = creator
        self.description = description.strip()
        self.roles = list(roles or [])
        self.members = list(members or [])

    def find_role(self, role_name: str) -> Role:
        """Return a role by name or raise ValueError."""
        normalized_name = role_name.strip().lower()
        for role in self.roles:
            if role.name.lower() == normalized_name:
                return role
        raise ValueError("Указанная роль не найдена в команде.")

    def add_role(self, role: Role) -> None:
        """Add a role if a role with the same name does not exist."""
        if any(item.name.lower() == role.name.lower() for item in self.roles):
            raise ValueError("Такая роль уже добавлена в команду.")
        self.roles.append(role)

    def is_role_available(self, role: Role) -> bool:
        """Return whether the role has a free place."""
        occupied = sum(
            member.role.name.lower() == role.name.lower()
            for member in self.members
        )
        return occupied < role.vacancies

    def add_member(self, user: User, role: Role) -> None:
        """Add a user to the team for an available role."""
        if not self.is_role_available(role):
            raise ValueError("Свободное место на роль уже занято.")
        self.members.append(TeamMember(user, role))

    def __str__(self) -> str:
        available = [
            role.name for role in self.roles if self.is_role_available(role)
        ]
        roles = ", ".join(available) or "нет свободных ролей"
        return (
            f"#{self.id} {self.name} | создатель: {self.creator.name} | "
            f"доступные роли: {roles}"
        )
