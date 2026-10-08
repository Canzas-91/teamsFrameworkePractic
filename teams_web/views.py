"""Web pages for teams loaded from the PR3 JSON storage."""

from html import escape
from pathlib import Path

from django.http import HttpRequest, HttpResponse

from homepage.views import page
from storage import load_teams, load_users
from teams import find_team_by_id, get_available_roles

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
USERS_FILE = DATA_DIR / "users.json"
TEAMS_FILE = DATA_DIR / "teams.json"


def _load_teams():
    """Load users and teams while restoring their object links."""
    users = load_users(USERS_FILE)
    return load_teams(TEAMS_FILE, users)


def teams(request: HttpRequest) -> HttpResponse:
    """Show all project teams."""
    items = ""
    for team in _load_teams():
        available = get_available_roles(team)
        roles = len(available)
        roles_text = f"Свободных ролей: {roles}"
        items += f"""
        <a href="/teams/{team.id}/"
           class="list-group-item list-group-item-action">
            <div class="d-flex justify-content-between align-items-center">
                <strong>{escape(team.name)}</strong>
                <span class="badge bg-primary rounded-pill">{roles_text}</span>
            </div>
            <div class="text-body-secondary">
                {escape(team.description or "Описание не указано")}
            </div>
        </a>
        """
    if not items:
        items = '<p class="alert alert-info">Команды пока не созданы.</p>'
    content = f"""
    <h1>Команды</h1>
    <p class="text-body-secondary">
        Проектные команды и доступные роли из data/teams.json.
    </p>
    <div class="list-group">{items}</div>
    """
    return HttpResponse(page("TeamFinder - команды", content))


def team_detail(request: HttpRequest, team_id: int) -> HttpResponse:
    """Show one team or return an HTML response with status 404."""
    try:
        team = find_team_by_id(_load_teams(), team_id)
    except KeyError:
        content = """
        <h1 class="text-danger">Команда не найдена</h1>
        <p>Команды с таким идентификатором нет.</p>
        <a href="/teams/" class="btn btn-outline-secondary">
            &larr; к списку команд
        </a>
        """
        return HttpResponse(page("Команда не найдена", content), status=404)

    role_items = ""
    for role in team.roles:
        available = team.is_role_available(role)
        badge = "bg-success" if available else "bg-secondary"
        status = "есть места" if available else "мест нет"
        role_items += f"""
        <li class="list-group-item">
            <div class="d-flex justify-content-between">
                <strong>{escape(role.name)}</strong>
                <span class="badge {badge}">{status}</span>
            </div>
            Стек: {escape(role.stack)}; опыт от {role.min_experience} г.;
            мест: {role.vacancies}
        </li>
        """
    if not role_items:
        role_items = '<li class="list-group-item">Роли пока не добавлены.</li>'

    member_items = "".join(
        f'<li class="list-group-item">{escape(str(member))}</li>'
        for member in team.members
    )
    if not member_items:
        member_items = (
            '<li class="list-group-item">В команде пока нет участников.</li>'
        )

    content = f"""
    <div class="card shadow-sm">
        <div class="card-body">
            <h1 class="card-title">{escape(team.name)}</h1>
            <p class="card-text">{escape(team.description or "Без описания")}</p>
            <p><strong>ID:</strong> {team.id}</p>
            <p><strong>Создатель:</strong> {escape(team.creator.name)}</p>
            <h2 class="h4 mt-4">Роли</h2>
            <ul class="list-group mb-4">{role_items}</ul>
            <h2 class="h4">Участники</h2>
            <ul class="list-group mb-4">{member_items}</ul>
            <a href="/teams/" class="btn btn-outline-secondary">
                &larr; к списку команд
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(team.name, content))
