"""Functions for submitting, cancelling and reviewing applications."""

from teams import find_team_by_id, selection_for_the_team


class ApplicationError(ValueError):
    """Error caused by an invalid operation with an application."""


def _next_id(applications: list[dict]) -> int:
    """Return the next application identifier."""
    return max(
        (application.get("id", 0) for application in applications),
        default=0,
    ) + 1


def _find_role(team: dict, role_name: str) -> dict:
    """Return a role by name or raise ApplicationError."""
    for role in team["roles"]:
        if role["name"].lower() == role_name.strip().lower():
            return role
    raise ApplicationError("Указанная роль не найдена в команде.")


def _find_application(applications: list[dict], application_id: int) -> dict:
    """Return an application by identifier or raise ApplicationError."""
    for application in applications:
        if application["id"] == application_id:
            return application
    raise ApplicationError(f"Заявка с ID {application_id} не найдена.")


def is_role_available(team: dict, role_name: str) -> bool:
    """Check whether a team has a free place for the selected role."""
    role = _find_role(team, role_name)
    occupied_places = sum(
        member["role"].lower() == role["name"].lower()
        for member in team.get("members", [])
    )
    return occupied_places < role["vacancies"]


def submit_application(
    teams: list[dict],
    applications: list[dict],
    team_id: int,
    applicant: str,
    role_name: str,
    stack: str,
    experience: int,
) -> dict:
    """Validate candidate data and add a pending application."""
    if not applicant.strip():
        raise ApplicationError("Имя кандидата не может быть пустым.")
    if experience < 0:
        raise ApplicationError("Опыт не может быть отрицательным.")

    team = find_team_by_id(teams, team_id)
    role = _find_role(team, role_name)
    if not is_role_available(team, role_name):
        raise ApplicationError("На выбранную роль нет свободных мест.")
    if not selection_for_the_team(role, stack, experience):
        raise ApplicationError(
            "Стек или опыт не соответствуют требованиям роли."
        )

    duplicate = any(
        application["team_id"] == team_id
        and application["applicant"].lower() == applicant.strip().lower()
        and application["role"].lower() == role["name"].lower()
        and application["status"] in {"pending", "accepted"}
        for application in applications
    )
    if duplicate:
        raise ApplicationError("Активная заявка кандидата уже существует.")

    application = {
        "id": _next_id(applications),
        "team_id": team_id,
        "applicant": applicant.strip(),
        "role": role["name"],
        "stack": stack.strip().lower(),
        "experience": experience,
        "status": "pending",
    }
    applications.append(application)
    return application


def cancel_application(
    applications: list[dict], application_id: int
) -> dict:
    """Cancel a pending application."""
    application = _find_application(applications, application_id)
    if application["status"] != "pending":
        raise ApplicationError("Отменить можно только ожидающую заявку.")
    application["status"] = "cancelled"
    return application


def review_application(
    teams: list[dict],
    applications: list[dict],
    application_id: int,
    decision: str,
) -> dict:
    """Accept or reject a pending application."""
    if decision not in {"accepted", "rejected"}:
        raise ApplicationError("Решение должно быть accepted или rejected.")

    application = _find_application(applications, application_id)
    if application["status"] != "pending":
        raise ApplicationError("Заявка уже рассмотрена или отменена.")

    team = find_team_by_id(teams, application["team_id"])
    if decision == "accepted":
        if not is_role_available(team, application["role"]):
            raise ApplicationError("Свободное место на роль уже занято.")
        team.setdefault("members", []).append(
            {
                "name": application["applicant"],
                "role": application["role"],
            }
        )

    application["status"] = decision
    return application
