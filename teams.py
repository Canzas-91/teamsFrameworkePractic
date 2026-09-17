"""Functions for teams, roles, searching, sorting and statistics."""


def _next_id(items: list[dict]) -> int:
    """Return an identifier greater than all identifiers in a collection."""
    return max((item.get("id", 0) for item in items), default=0) + 1


def create_team(
    teams: list[dict],
    team_name: str,
    creator: str,
    description: str = "",
) -> dict:
    """Create a team and add it to the teams collection."""
    if not team_name.strip() or not creator.strip():
        raise ValueError("Название команды и имя создателя обязательны.")
    normalized_name = team_name.strip().lower()
    if any(team["name"].lower() == normalized_name for team in teams):
        raise ValueError("Команда с таким названием уже существует.")

    team = {
        "id": _next_id(teams),
        "name": team_name.strip(),
        "creator": creator.strip(),
        "description": description.strip(),
        "roles": [],
        "members": [],
    }
    teams.append(team)
    return team


def find_team_by_id(teams: list[dict], team_id: int) -> dict:
    """Return a team by its identifier or raise KeyError."""
    for team in teams:
        if team["id"] == team_id:
            return team
    raise KeyError(f"Команда с ID {team_id} не найдена.")


def add_role(
    teams: list[dict],
    team_id: int,
    role_name: str,
    stack: str,
    min_experience: int,
    vacancies: int = 1,
) -> dict:
    """Add a required role to an existing team."""
    if min_experience < 0 or vacancies < 1:
        raise ValueError(
            "Опыт не может быть отрицательным, мест должно быть > 0."
        )
    if not role_name.strip() or not stack.strip():
        raise ValueError("Название роли и стек обязательны.")

    team = find_team_by_id(teams, team_id)
    if any(
        role["name"].lower() == role_name.strip().lower()
        for role in team["roles"]
    ):
        raise ValueError("Такая роль уже добавлена в команду.")

    role = {
        "name": role_name.strip(),
        "stack": stack.strip().lower(),
        "min_experience": min_experience,
        "vacancies": vacancies,
    }
    team["roles"].append(role)
    return role


def find_teams(teams: list[dict], query: str) -> list[dict]:
    """Find teams by a substring in the name or description."""
    normalized_query = query.strip().lower()
    return [
        team
        for team in teams
        if normalized_query in team["name"].lower()
        or normalized_query in team.get("description", "").lower()
    ]


def sort_teams(teams: list[dict]) -> list[dict]:
    """Return teams sorted by name without changing the source list."""
    return sorted(teams, key=lambda team: team["name"].lower())


def selection_for_the_team(
    role: dict, applicant_stack: str, experience: int
) -> bool:
    """Check whether a candidate meets a role's basic requirements."""
    return (
        role["stack"].lower() == applicant_stack.strip().lower()
        and experience >= role["min_experience"]
    )


def get_available_roles(team: dict) -> list[str]:
    """Return role names that still have free places in the team."""
    occupied = {}
    for member in team.get("members", []):
        member_role = member["role"].lower()
        occupied[member_role] = occupied.get(member_role, 0) + 1

    return [
        role["name"]
        for role in team["roles"]
        if occupied.get(role["name"].lower(), 0) < role["vacancies"]
    ]


def team_info(team: dict) -> str:
    """Return a formatted summary of a team."""
    roles = ", ".join(get_available_roles(team)) or "нет свободных ролей"
    return (
        f"#{team['id']} {team['name']} | создатель: {team['creator']} | "
        f"доступные роли: {roles}"
    )


def team_statistics(teams: list[dict], applications: list[dict]) -> dict:
    """Calculate general statistics for teams and applications."""
    statuses = {"pending": 0, "accepted": 0, "rejected": 0, "cancelled": 0}
    for application in applications:
        status = application.get("status", "pending")
        statuses[status] = statuses.get(status, 0) + 1

    return {
        "teams": len(teams),
        "roles": sum(len(team["roles"]) for team in teams),
        "members": sum(len(team.get("members", [])) for team in teams),
        "applications": len(applications),
        "applications_by_status": statuses,
    }
