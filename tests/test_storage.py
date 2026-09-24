from pathlib import Path

from applications import review_application, submit_application
from models import Application, Team, User
from storage import (
    load_applications,
    load_teams,
    load_users,
    save_applications,
    save_teams,
    save_users,
)
from teams import add_role, create_team


def test_json_round_trip_restores_object_links(tmp_path: Path) -> None:
    users = [
        User(1, "Артём", "artem@example.com"),
        User(2, "Мария", "maria@example.com", "python", 3),
    ]
    teams: list[Team] = []
    create_team(teams, "Dream Team", users[0])
    add_role(teams, 1, "Backend", "python", 2)
    applications: list[Application] = []
    submit_application(teams, applications, 1, users[1], "Backend")
    review_application(teams, applications, 1, "accepted")

    users_file = tmp_path / "users.json"
    teams_file = tmp_path / "teams.json"
    applications_file = tmp_path / "applications.json"
    save_users(users_file, users)
    save_teams(teams_file, teams)
    save_applications(applications_file, applications)

    loaded_users = load_users(users_file)
    loaded_teams = load_teams(teams_file, loaded_users)
    loaded_applications = load_applications(
        applications_file, loaded_teams, loaded_users
    )

    application = loaded_applications[0]
    assert application.team is loaded_teams[0]
    assert application.applicant is loaded_users[1]
    assert application.role is loaded_teams[0].roles[0]
    assert loaded_teams[0].members[0].user is loaded_users[1]
