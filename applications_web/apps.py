"""Configuration for the applications web application."""

from django.apps import AppConfig


class ApplicationsWebConfig(AppConfig):
    """Configure the applications web application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "applications_web"
