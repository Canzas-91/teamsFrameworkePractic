import pytest

from models import Role, Team, User
from teams import (
    add_role,
    create_team,
    find_teams,
    selection_for_the_team,
    sort_teams,
)


def make_user(user_id: int = 1, name: str = "Артём") -> User:
    return User(user_id, name, f"user{user_id}@example.com", "python", 3)


def test_create_team_creates_object() -> None:
    teams: list[Team] = []
    creator = make_user()
    team = create_team(teams, "Dream Team", creator)
    assert isinstance(team, Team)
    assert team.id == 1
    assert team.creator is creator
    assert teams == [team]


def test_add_and_find_role_objects() -> None:
    teams: list[Team] = []
    create_team(teams, "Dream Team", make_user())
    role = add_role(teams, 1, "Backend", "Python", 2)
    assert isinstance(role, Role)
    assert role.stack == "python"
    assert selection_for_the_team(role, make_user())


def test_find_and_sort_teams() -> None:
    teams: list[Team] = []
    create_team(teams, "Web Studio", make_user(), "Сайт")
    create_team(
        teams, "Analytics", make_user(2, "Иван"), "Анализ данных"
    )
    assert find_teams(teams, "данных")[0].name == "Analytics"
    assert [team.name for team in sort_teams(teams)] == [
        "Analytics",
        "Web Studio",
    ]


def test_duplicate_team_is_forbidden() -> None:
    teams: list[Team] = []
    create_team(teams, "Dream Team", make_user())
    with pytest.raises(ValueError):
        create_team(teams, "dream team", make_user(2, "Иван"))
