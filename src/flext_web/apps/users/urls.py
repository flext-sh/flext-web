"""FLEXT Users URL Configuration - Enterprise User Management.

This module defines URL patterns for the FLEXT Users app,
providing RESTful endpoints for enterprise user management operations.

Author: FLEXT Team
Date: 2025-07-13
"""

from __future__ import annotations

from django.urls import path

from flext_web.apps.users import views

app_name = "users"

urlpatterns = [
    # Authentication views
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    # User management views
    path("", views.UserListView.as_view(), name="list"),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("settings/", views.UserSettingsView.as_view(), name="settings"),
    path("<uuid:pk>/", views.UserDetailView.as_view(), name="detail"),
    path("<uuid:pk>/edit/", views.UserUpdateView.as_view(), name="update"),
    # API endpoints
    path("api/users/", views.UserAPIView.as_view(), name="api-users"),
    path(
        "api/users/<uuid:pk>/",
        views.UserDetailAPIView.as_view(),
        name="api-user-detail",
    ),
]
