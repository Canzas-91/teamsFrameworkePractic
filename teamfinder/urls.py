"""Root URL configuration for the team finder."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("teams/", include("teams_web.urls")),
    path("applications/", include("applications_web.urls")),
]
