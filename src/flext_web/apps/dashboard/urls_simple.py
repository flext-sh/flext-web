"""Simple dashboard URL configuration for testing Django functionality."""

from __future__ import annotations

from django.urls import path

from flext_web.apps.dashboard.views_simple import (
    DashboardView,
    StatsAPIView,
    simple_dashboard_view,
)

app_name = "dashboard"

urlpatterns = [
    path("", simple_dashboard_view, name="simple"),
    path("dashboard/", DashboardView.as_view(), name="index"),
    path("api/stats/", StatsAPIView.as_view(), name="api_stats"),
]
