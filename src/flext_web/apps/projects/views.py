"""FLEXT Projects Views - Enterprise Project Management Interface.

This module provides Django views for enterprise project management,
implementing comprehensive CRUD operations and project lifecycle management.
"""

from __future__ import annotations

from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView

from flext_web.models import MeltanoProject, ProjectTemplate


class ProjectListView(LoginRequiredMixin, ListView):
    """View to display a list of all projects."""

    model = MeltanoProject
    template_name = "projects/list.html"
    context_object_name = "projects"
    paginate_by = 20

    def get_queryset(self):
        """Get the queryset of active projects ordered by creation date.

        Returns:
            QuerySet: Active MeltanoProject instances with related templates.

        """
        return (
            MeltanoProject.objects.filter(
                is_active=True,
            )
            .select_related("template")
            .order_by("-created_at")
        )


class ProjectDetailView(LoginRequiredMixin, DetailView):
    """View to display details of a single project."""

    model = MeltanoProject
    template_name = "projects/detail.html"
    context_object_name = "project"

    def get_object(self):
        """Get the specific project object for the detail view.

        Returns:
            MeltanoProject: The project instance with related template data.

        Raises:
            Http404: If the project is not found or is inactive.

        """
        return get_object_or_404(
            MeltanoProject.objects.select_related("template"),
            pk=self.kwargs["pk"],
            is_active=True,
        )


class ProjectTemplateListView(LoginRequiredMixin, ListView):
    """View to display available project templates."""

    model = ProjectTemplate
    template_name = "projects/templates.html"
    context_object_name = "templates"

    def get_queryset(self):
        """Get the queryset of active project templates ordered by category.

        Returns:
            QuerySet: Active ProjectTemplate instances ordered by category and name.

        """
        return ProjectTemplate.objects.filter(
            is_active=True,
        ).order_by("category", "name")


class ProjectDashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard view for project overview."""

    template_name = "projects/dashboard.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get context data for the project dashboard template.

        Args:
            **kwargs: Additional keyword arguments passed to the view.

        Returns:
            dict[str, Any]: Context data including recent projects and statistics.

        """
        context = super().get_context_data(**kwargs)

        # Get user's recent projects
        recent_projects = MeltanoProject.objects.filter(
            is_active=True,
        ).order_by(
            "-updated_at",
        )[:5]

        # Get project statistics
        total_projects = MeltanoProject.objects.filter(is_active=True).count()
        active_templates = ProjectTemplate.objects.filter(is_active=True).count()

        context.update(
            {
                "recent_projects": recent_projects,
                "total_projects": total_projects,
                "active_templates": active_templates,
            },
        )

        return context
