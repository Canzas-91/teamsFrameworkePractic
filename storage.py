"""JSON persistence and conversion between dictionaries and domain objects."""

import json
from pathlib import Path
from typing import TypeVar

from models import Application, Role, Team, TeamMember, User

JSONData = TypeVar("JSONData", list, dict)


def load_json(filename: Path, default: JSONData) -> JSONData:
    """Load raw JSON data, returning a copy of the default on failure."""
    try:
        with filename.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return default.copy()
    except json.JSONDecodeError as error:
        print(f"Некорректный JSON в файле {filename}: {error}")
        return default.copy()

    if not isinstance(data, type(default)):
        print(f"Неверный формат данных в файле {filename}.")
        return default.copy()
    return data


def save_json(filename: Path, data: list[dict] | dict) -> None:
    """Save JSON-compatible data to a file."""
    filename.parent.mkdir(parents=True, exist_ok=True)
    with filename.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_users(filename: Path) -> list[User]:
    """Load users and create User objects."""
    return [User.from_data(item) for item in load_json(filename, [])]


def save_users(filename: Path, users: list[User]) -> None:
    """Convert users to dictionaries and save them."""
    save_json(filename, [user.to_data() for user in users])


def _legacy_email(name: str, users: list[User]) -> str:
    """Build a unique local email while importing old PR2 data."""
    base = "".join(character for character in name.lower() if character.isalnum())
    base = base or "user"
    number = 1
    email = f"{base}@local.invalid"
    existing = {user.email for user in users}
    while email in existing:
        number += 1
        email = f"{base}{number}@local.invalid"
    return email


def _find_or_create_legacy_user(
    users: list[User],
    name: str,
    stack: str = "",
    experience: int = 0,
) -> User:
    """Find a user by name or migrate a name-only user from PR2."""
    for user in users:
        if user.name.lower() == name.strip().lower():
            if not user.stack and stack:
                user.stack = stack.strip().lower()
                user.experience = experience
            return user
    user = User(
        max((item.id for item in users), default=0) + 1,
        name,
        _legacy_email(name, users),
        stack,
        experience,
    )
    users.append(user)
    return user


def _user_by_id(users: list[User], user_id: int) -> User:
    for user in users:
        if user.id == user_id:
            return user
    raise ValueError(f"В JSON указан неизвестный user_id={user_id}.")


def load_teams(filename: Path, users: list[User]) -> list[Team]:
    """Load teams, roles and memberships while restoring object links."""
    teams: list[Team] = []
    for data in load_json(filename, []):
        if "creator_id" in data:
            creator = _user_by_id(users, int(data["creator_id"]))
        else:
            creator = _find_or_create_legacy_user(users, str(data["creator"]))

        roles = [Role.from_data(item) for item in data.get("roles", [])]
        team = Team(
            int(data["id"]),
            str(data["name"]),
            creator,
            str(data.get("description", "")),
            roles,
        )
        for item in data.get("members", []):
            role = team.find_role(str(item["role"]))
            if "user_id" in item:
                user = _user_by_id(users, int(item["user_id"]))
            else:
                user = _find_or_create_legacy_user(
                    users, str(item.get("name", "Пользователь"))
                )
            team.members.append(TeamMember(user, role))
        teams.append(team)
    return teams


def save_teams(filename: Path, teams: list[Team]) -> None:
    """Convert teams and nested objects to dictionaries and save them."""
    data = [
        {
            "id": team.id,
            "name": team.name,
            "creator_id": team.creator.id,
            "description": team.description,
            "roles": [role.to_data() for role in team.roles],
            "members": [
                {"user_id": member.user.id, "role": member.role.name}
                for member in team.members
            ],
        }
        for team in teams
    ]
    save_json(filename, data)


def _team_by_id(teams: list[Team], team_id: int) -> Team:
    for team in teams:
        if team.id == team_id:
            return team
    raise ValueError(f"В JSON указан неизвестный team_id={team_id}.")


def load_applications(
    filename: Path, teams: list[Team], users: list[User]
) -> list[Application]:
    """Load applications and restore links to Team, User and Role objects."""
    applications: list[Application] = []
    for data in load_json(filename, []):
        team = _team_by_id(teams, int(data["team_id"]))
        role = team.find_role(str(data["role"]))
        if "user_id" in data:
            applicant = _user_by_id(users, int(data["user_id"]))
        else:
            applicant = _find_or_create_legacy_user(
                users,
                str(data["applicant"]),
                str(data.get("stack", "")),
                int(data.get("experience", 0)),
            )
        applications.append(
            Application(
                int(data["id"]),
                team,
                applicant,
                role,
                str(data.get("status", "pending")),
            )
        )
    return applications


def save_applications(
    filename: Path, applications: list[Application]
) -> None:
    """Convert applications to IDs and save them."""
    data = [
        {
            "id": application.id,
            "team_id": application.team.id,
            "user_id": application.applicant.id,
            "role": application.role.name,
            "status": application.status,
        }
        for application in applications
    ]
    save_json(filename, data)
