import os

import pytest

django = pytest.importorskip("django")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teamfinder.settings")
django.setup()

from django.test import Client  # noqa: E402


@pytest.fixture
def client() -> Client:
    return Client()


@pytest.mark.parametrize(
    ("url", "expected_text"),
    [
        ("/", "TeamFinder"),
        ("/teams/", "Dream Team"),
        ("/teams/1/", "Backend-разработчик"),
        ("/applications/", "Заявка №1"),
        ("/applications/1/", "принята"),
    ],
)
def test_web_pages(client: Client, url: str, expected_text: str) -> None:
    response = client.get(url)
    assert response.status_code == 200
    assert expected_text in response.content.decode()


@pytest.mark.parametrize("url", ["/teams/999/", "/applications/999/"])
def test_missing_objects_return_404(client: Client, url: str) -> None:
    response = client.get(url)
    assert response.status_code == 404
