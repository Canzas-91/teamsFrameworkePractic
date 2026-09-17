import pytest

from applications import (
    ApplicationError,
    cancel_application,
    is_role_available,
    review_application,
    submit_application,
)
from teams import add_role, create_team


def make_team() -> list[dict]:
    teams: list[dict] = []
    create_team(teams, "Dream Team", "Артём")
    add_role(teams, 1, "Backend", "Python", 2)
    return teams


def test_submit_application() -> None:
    teams = make_team()
    applications: list[dict] = []
    application = submit_application(
        teams, applications, 1, "Мария", "Backend", "Python", 3
    )
    assert application["status"] == "pending"
    assert len(applications) == 1


def test_unsuitable_candidate_is_rejected() -> None:
    teams = make_team()
    applications: list[dict] = []
    with pytest.raises(ApplicationError):
        submit_application(teams, applications, 1, "Мария", "Backend", "Java", 3)


def test_cancel_application() -> None:
    teams = make_team()
    applications: list[dict] = []
    submit_application(
        teams, applications, 1, "Мария", "Backend", "Python", 3
    )
    assert cancel_application(applications, 1)["status"] == "cancelled"


def test_accept_application_fills_vacancy() -> None:
    teams = make_team()
    applications: list[dict] = []
    submit_application(
        teams, applications, 1, "Мария", "Backend", "Python", 3
    )
    review_application(teams, applications, 1, "accepted")
    assert teams[0]["members"] == [{"name": "Мария", "role": "Backend"}]
    assert not is_role_available(teams[0], "Backend")
