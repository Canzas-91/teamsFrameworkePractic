"""Views and the shared HTML frame for the web interface."""

from django.http import HttpRequest, HttpResponse


def page(title: str, content: str) -> str:
    """Return a complete Bootstrap HTML document."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/"
        "dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand-md bg-dark mb-4" data-bs-theme="dark">
        <div class="container">
            <a class="navbar-brand" href="/">TeamFinder</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Главная</a>
                <a class="nav-link" href="/teams/">Команды</a>
                <a class="nav-link" href="/applications/">Заявки</a>
            </div>
        </div>
    </nav>
    <main class="container pb-5">{content}</main>
</body>
</html>"""


def index(request: HttpRequest) -> HttpResponse:
    """Show the project description and links to its sections."""
    content = """
    <div class="p-5 bg-white rounded-3 shadow-sm">
        <h1 class="display-4">TeamFinder</h1>
        <p class="lead">Система подбора участников в проектную команду.</p>
        <p>
            Просматривайте команды, открытые роли и заявки участников.
            Данные загружаются из JSON-файлов проекта ПР3.
        </p>
        <a href="/teams/" class="btn btn-primary me-2">Команды</a>
        <a href="/applications/" class="btn btn-secondary">Заявки</a>
    </div>
    """
    return HttpResponse(page("TeamFinder", content))
