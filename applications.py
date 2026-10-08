"""Functions for submitting, cancelling and reviewing applications."""

from models import Application, Team, User
from teams import find_team_by_id


class ApplicationError(ValueError):
    """Error caused by an invalid operation with an application."""


def _next_id(applications: list[Application]) -> int:
    """Return the next application identifier."""
    return max((application.id for application in applications), default=0) + 1


def _find_application(
    applications: list[Application], application_id: int
) -> Application:
    """Return an application by identifier or raise ApplicationError."""
    application = find_application_by_id(applications, application_id)
    if application is not None:
        return application
    raise ApplicationError(f"Заявка с ID {application_id} не найдена.")


def find_application_by_id(
    applications: list[Application], application_id: int
) -> Application | None:
    """Return an application by identifier or None if it does not exist."""
    for application in applications:
        if application.id == application_id:
            return application
    return None


def is_role_available(team: Team, role_name: str) -> bool:
    """Check whether a team has a free place for the selected role."""
    try:
        role = team.find_role(role_name)
    except ValueError as error:
        raise ApplicationError(str(error)) from error
    return team.is_role_available(role)


def submit_application(
    teams: list[Team],
    applications: list[Application],
    team_id: int,
    applicant: User,
    role_name: str,
) -> Application:
    """Validate a user profile and add a pending application object."""
    team = find_team_by_id(teams, team_id)
    try:
        role = team.find_role(role_name)
    except ValueError as error:
        raise ApplicationError(str(error)) from error

    if not team.is_role_available(role):
        raise ApplicationError("На выбранную роль нет свободных мест.")
    if not role.is_suitable_for(applicant):
        raise ApplicationError(
            "Стек или опыт не соответствуют требованиям роли."
        )

    duplicate = any(
        application.team.id == team_id
        and application.applicant.id == applicant.id
        and application.role.name.lower() == role.name.lower()
        and application.status in {"pending", "accepted"}
        for application in applications
    )
    if duplicate:
        raise ApplicationError("Активная заявка пользователя уже существует.")

    application = Application(
        _next_id(applications), team, applicant, role
    )
    applications.append(application)
    return application


def cancel_application(
    applications: list[Application], application_id: int
) -> Application:
    """Cancel a pending application through the object's method."""
    application = _find_application(applications, application_id)
    try:
        application.cancel()
    except ValueError as error:
        raise ApplicationError(str(error)) from error
    return application


def review_application(
    teams: list[Team],
    applications: list[Application],
    application_id: int,
    decision: str,
) -> Application:
    """Accept or reject a pending application through the object's method."""
    del teams  # the application already references its Team object
    application = _find_application(applications, application_id)
    try:
        application.review(decision)
    except ValueError as error:
        raise ApplicationError(str(error)) from error
    return application
