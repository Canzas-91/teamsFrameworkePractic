import pytest

from teams import (
    add_role,
    create_team,
    find_teams,
    selection_for_the_team,
    sort_teams,
)


def test_create_team() -> None:
    teams: list[dict] = []
    team = create_team(teams, "Dream Team", "Артём")
    assert team["id"] == 1
    assert teams == [team]


def test_add_and_find_role() -> None:
    teams: list[dict] = []
    create_team(teams, "Dream Team", "Артём")
    role = add_role(teams, 1, "Backend", "Python", 2)
    assert role["stack"] == "python"
    assert selection_for_the_team(role, "PYTHON", 3)


def test_find_and_sort_teams() -> None:
    teams: list[dict] = []
    create_team(teams, "Web Studio", "Анна", "Сайт")
    create_team(teams, "Analytics", "Иван", "Анализ данных")
    assert find_teams(teams, "данных")[0]["name"] == "Analytics"
    assert [team["name"] for team in sort_teams(teams)] == [
        "Analytics",
        "Web Studio",
    ]


def test_duplicate_team_is_forbidden() -> None:
    teams: list[dict] = []
    create_team(teams, "Dream Team", "Артём")
    with pytest.raises(ValueError):
        create_team(teams, "dream team", "Иван")
