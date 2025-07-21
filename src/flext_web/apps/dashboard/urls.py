"""Dashboard URL configuration for Django routing.

This module defines URL patterns for the dashboard application,
mapping URLs to their corresponding views for the FLEXT Meltano
Enterprise dashboard interface.
"""

from __future__ import annotations

from django.urls import path

from flext_web.apps.dashboard import views

app_name = "dashboard"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="index"),
    path("api/stats/", views.StatsAPIView.as_view(), name="api_stats"),
]
