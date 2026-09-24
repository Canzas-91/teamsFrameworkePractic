"""Functions for creating, searching and analysing project teams."""

from models import Application, Role, Team, User


def _next_id(items: list[Team]) -> int:
    """Return an identifier greater than all identifiers in a collection."""
    return max((item.id for item in items), default=0) + 1


def create_team(
    teams: list[Team],
    team_name: str,
    creator: User,
    description: str = "",
) -> Team:
    """Create a team object and add it to the collection."""
    if not team_name.strip():
        raise ValueError("Название команды обязательно.")
    normalized_name = team_name.strip().lower()
    if any(team.name.lower() == normalized_name for team in teams):
        raise ValueError("Команда с таким названием уже существует.")

    team = Team(_next_id(teams), team_name, creator, description)
    teams.append(team)
    return team


def find_team_by_id(teams: list[Team], team_id: int) -> Team:
    """Return a team by its identifier or raise KeyError."""
    for team in teams:
        if team.id == team_id:
            return team
    raise KeyError(f"Команда с ID {team_id} не найдена.")


def add_role(
    teams: list[Team],
    team_id: int,
    role_name: str,
    stack: str,
    min_experience: int,
    vacancies: int = 1,
) -> Role:
    """Create a role object and add it to an existing team."""
    team = find_team_by_id(teams, team_id)
    role = Role(role_name, stack, min_experience, vacancies)
    team.add_role(role)
    return role


def find_teams(teams: list[Team], query: str) -> list[Team]:
    """Find teams by a substring in the name or description."""
    normalized_query = query.strip().lower()
    return [
        team
        for team in teams
        if normalized_query in team.name.lower()
        or normalized_query in team.description.lower()
    ]


def sort_teams(teams: list[Team]) -> list[Team]:
    """Return teams sorted by name without changing the source list."""
    return sorted(teams, key=lambda team: team.name.lower())


def selection_for_the_team(role: Role, user: User) -> bool:
    """Check whether a user meets a role's requirements."""
    return role.is_suitable_for(user)


def get_available_roles(team: Team) -> list[Role]:
    """Return role objects that still have free places in the team."""
    return [role for role in team.roles if team.is_role_available(role)]


def team_info(team: Team) -> str:
    """Return a formatted summary of a team."""
    return str(team)


def team_statistics(
    teams: list[Team], applications: list[Application]
) -> dict[str, int | dict[str, int]]:
    """Calculate general statistics for teams and applications."""
    statuses = {"pending": 0, "accepted": 0, "rejected": 0, "cancelled": 0}
    for application in applications:
        statuses[application.status] = statuses.get(application.status, 0) + 1

    return {
        "teams": len(teams),
        "roles": sum(len(team.roles) for team in teams),
        "members": sum(len(team.members) for team in teams),
        "applications": len(applications),
        "applications_by_status": statuses,
    }
