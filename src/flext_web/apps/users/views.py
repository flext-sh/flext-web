"""FLEXT Users Views - Enterprise User Management Interface.
This module provides Django views for enterprise user management,
implementing comprehensive user operations and profile management.
Author: FLEXT Team
Date: 2025-07-13.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, cast

if TYPE_CHECKING:
    from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

User = get_user_model()


class UserLoginView(LoginView):
    """User login view."""

    template_name = "users/login.html"
    success_url = reverse_lazy("dashboard:index")
    redirect_authenticated_user = True

    def form_invalid(self, form: Any) -> HttpResponse:
        """Add custom error message for invalid login."""
        form.add_error(None, "Invalid username or password")
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    """User logout view."""

    next_page = reverse_lazy("users:login")


class UserListView(LoginRequiredMixin, ListView[AbstractUser]):
    """View to display a list of all users."""

    model = User
    template_name = "users/list.html"
    context_object_name = "users"
    paginate_by = 20


class UserDetailView(LoginRequiredMixin, DetailView[AbstractUser]):
    """View to display user details."""

    model = User
    template_name = "users/detail.html"
    context_object_name = "user"


class UserUpdateView(LoginRequiredMixin, UpdateView[Any, Any]):
    """View to update user details."""

    model = User
    template_name = "users/update.html"
    fields: ClassVar[list[str]] = ["first_name", "last_name", "email"]
    context_object_name = "user"


class UserProfileView(LoginRequiredMixin, DetailView[Any]):
    """View to display user profile."""

    template_name = "users/profile.html"
    context_object_name = "user"

    def get_object(
        self, queryset: QuerySet[AbstractUser] | None = None,
    ) -> AbstractUser:
        return cast("AbstractUser", self.request.user)


class UserSettingsView(LoginRequiredMixin, TemplateView):
    """View to display user settings."""

    template_name = "users/settings.html"


class UserAPIView(LoginRequiredMixin, TemplateView):
    """API view for user operations."""

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        users = User.objects.all()
        data = [
            {
                "id": str(getattr(user, "id", "unknown")),
                "username": getattr(user, "username", user.get_username()),
                "email": getattr(user, "email", ""),
                "first_name": getattr(user, "first_name", ""),
                "last_name": getattr(user, "last_name", ""),
                "is_active": user.is_active,
            }
            for user in users
        ]
        return JsonResponse({"users": data})


class UserDetailAPIView(LoginRequiredMixin, DetailView[Any]):
    """API view for individual user details."""

    model = User

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        user = self.get_object()
        data = {
            "id": str(getattr(user, "id", "unknown")),
            "username": getattr(user, "username", user.get_username()),
            "email": getattr(user, "email", ""),
            "first_name": getattr(user, "first_name", ""),
            "last_name": getattr(user, "last_name", ""),
            "is_active": user.is_active,
            "date_joined": user.date_joined.isoformat() if hasattr(user, "date_joined") and user.date_joined else None,
            "last_login": user.last_login.isoformat() if user.last_login else None,
        }
        return JsonResponse(data)
