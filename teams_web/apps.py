"""Configuration for the teams web application."""

from django.apps import AppConfig


class TeamsWebConfig(AppConfig):
    """Configure the teams web application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "teams_web"
