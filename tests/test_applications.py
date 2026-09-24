import pytest

from applications import (
    ApplicationError,
    cancel_application,
    is_role_available,
    review_application,
    submit_application,
)
from models import Application, Team, User
from teams import add_role, create_team


def make_team() -> tuple[list[Team], User]:
    creator = User(1, "Артём", "artem@example.com")
    applicant = User(2, "Мария", "maria@example.com", "python", 3)
    teams: list[Team] = []
    create_team(teams, "Dream Team", creator)
    add_role(teams, 1, "Backend", "Python", 2)
    return teams, applicant


def test_submit_application_creates_linked_object() -> None:
    teams, applicant = make_team()
    applications: list[Application] = []
    application = submit_application(
        teams, applications, 1, applicant, "Backend"
    )
    assert application.status == "pending"
    assert application.team is teams[0]
    assert application.applicant is applicant
    assert application.role is teams[0].roles[0]


def test_unsuitable_candidate_is_rejected() -> None:
    teams, _ = make_team()
    applicant = User(3, "Анна", "anna@example.com", "java", 3)
    with pytest.raises(ApplicationError):
        submit_application(teams, [], 1, applicant, "Backend")


def test_cancel_application() -> None:
    teams, applicant = make_team()
    applications: list[Application] = []
    submit_application(teams, applications, 1, applicant, "Backend")
    assert cancel_application(applications, 1).status == "cancelled"


def test_accept_application_adds_linked_member() -> None:
    teams, applicant = make_team()
    applications: list[Application] = []
    submit_application(teams, applications, 1, applicant, "Backend")
    review_application(teams, applications, 1, "accepted")
    member = teams[0].members[0]
    assert member.user is applicant
    assert member.role is teams[0].roles[0]
    assert not is_role_available(teams[0], "Backend")
