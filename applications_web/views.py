"""Web pages for applications loaded from the PR3 JSON storage."""

from html import escape
from pathlib import Path

from django.http import HttpRequest, HttpResponse

from applications import find_application_by_id
from homepage.views import page
from storage import load_applications, load_teams, load_users

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
USERS_FILE = DATA_DIR / "users.json"
TEAMS_FILE = DATA_DIR / "teams.json"
APPLICATIONS_FILE = DATA_DIR / "applications.json"

STATUS_LABELS = {
    "pending": "ожидает решения",
    "accepted": "принята",
    "rejected": "отклонена",
    "cancelled": "отменена",
}
STATUS_BADGES = {
    "pending": "bg-warning text-dark",
    "accepted": "bg-success",
    "rejected": "bg-danger",
    "cancelled": "bg-secondary",
}


def _load_applications():
    """Load all linked objects needed for application pages."""
    users = load_users(USERS_FILE)
    teams = load_teams(TEAMS_FILE, users)
    return load_applications(APPLICATIONS_FILE, teams, users)


def _status(application) -> tuple[str, str]:
    """Return a localized status label and Bootstrap badge class."""
    return (
        STATUS_LABELS.get(application.status, application.status),
        STATUS_BADGES.get(application.status, "bg-secondary"),
    )


def applications(request: HttpRequest) -> HttpResponse:
    """Show all submitted team applications."""
    items = ""
    for application in _load_applications():
        status, badge = _status(application)
        items += f"""
        <li class="list-group-item d-flex justify-content-between
                   align-items-center">
            <a href="/applications/{application.id}/">
                Заявка №{application.id}: {escape(application.applicant.name)}
                &rarr; {escape(application.team.name)},
                роль {escape(application.role.name)}
            </a>
            <span class="badge {badge}">{status}</span>
        </li>
        """
    if not items:
        items = '<li class="list-group-item">Заявок пока нет.</li>'
    content = f"""
    <h1>Заявки</h1>
    <p class="text-body-secondary">
        Заявки пользователей из data/applications.json.
    </p>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("TeamFinder - заявки", content))


def application_detail(
    request: HttpRequest, application_id: int
) -> HttpResponse:
    """Show one application or return an HTML response with status 404."""
    application = find_application_by_id(
        _load_applications(), application_id
    )
    if application is None:
        content = """
        <h1 class="text-danger">Заявка не найдена</h1>
        <p>Заявки с таким идентификатором нет.</p>
        <a href="/applications/" class="btn btn-outline-secondary">
            &larr; к списку заявок
        </a>
        """
        return HttpResponse(page("Заявка не найдена", content), status=404)

    status, badge = _status(application)
    suitable = application.role.is_suitable_for(application.applicant)
    match_text = "соответствует" if suitable else "не соответствует"
    match_badge = "bg-success" if suitable else "bg-danger"
    content = f"""
    <div class="card shadow-sm">
        <div class="card-body">
            <h1 class="card-title">Заявка №{application.id}</h1>
            <p><strong>Команда:</strong>
                <a href="/teams/{application.team.id}/">
                    {escape(application.team.name)}
                </a>
            </p>
            <p><strong>Кандидат:</strong>
                {escape(application.applicant.name)}
            </p>
            <p><strong>Email:</strong>
                {escape(application.applicant.email)}
            </p>
            <p><strong>Роль:</strong> {escape(application.role.name)}</p>
            <p><strong>Стек кандидата:</strong>
                {escape(application.applicant.stack or "не указан")}
            </p>
            <p><strong>Опыт:</strong>
                {application.applicant.experience} г.
            </p>
            <p><strong>Соответствие требованиям:</strong>
                <span class="badge {match_badge}">{match_text}</span>
            </p>
            <p><strong>Статус:</strong>
                <span class="badge {badge}">{status}</span>
            </p>
            <a href="/applications/" class="btn btn-outline-secondary">
                &larr; к списку заявок
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Заявка №{application.id}", content))
