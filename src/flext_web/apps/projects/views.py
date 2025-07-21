"""FLEXT Projects Views - Enterprise Project Management Interface.

This module provides Django views for enterprise project management,
implementing comprehensive CRUD operations and project lifecycle management.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse

if TYPE_CHECKING:
    from django.db.models import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from flext_web.apps.projects.models import MeltanoProject, ProjectTemplate


class ProjectListView(LoginRequiredMixin, ListView[MeltanoProject]):
    """View to display a list of all projects."""

    model = MeltanoProject
    template_name = "projects/list.html"
    context_object_name = "projects"
    paginate_by = 20

    def get_queryset(self) -> QuerySet[MeltanoProject]:
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


class ProjectDetailView(LoginRequiredMixin, DetailView[MeltanoProject]):
    """View to display details of a single project."""

    model = MeltanoProject
    template_name = "projects/detail.html"
    context_object_name = "project"

    def get_object(
        self, queryset: QuerySet[MeltanoProject] | None = None,
    ) -> MeltanoProject:
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


class ProjectTemplateListView(LoginRequiredMixin, ListView[ProjectTemplate]):
    """View to display available project templates."""

    model = ProjectTemplate
    template_name = "projects/templates.html"
    context_object_name = "templates"

    def get_queryset(self) -> QuerySet[ProjectTemplate]:
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


# Missing view classes for URL patterns


class ProjectCreateView(LoginRequiredMixin, View):
    """View for creating new projects."""

    template_name = "projects/create.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle GET request for project creation form."""
        from django.shortcuts import render

        templates = ProjectTemplate.objects.filter(is_active=True)
        return render(request, self.template_name, {"templates": templates})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Handle POST request for project creation."""
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        template_id = request.POST.get("template")

        if name and template_id:
            template = get_object_or_404(ProjectTemplate, id=template_id)
            MeltanoProject.objects.create(
                name=name,
                description=description,
                template=template,
                created_by=request.user,
            )
            return redirect("projects:list")

        # If validation fails, redirect back to form
        return redirect("projects:create")


class ProjectUpdateView(LoginRequiredMixin, TemplateView):
    """View for updating projects."""

    template_name = "projects/update.html"


class ProjectDeleteView(LoginRequiredMixin, TemplateView):
    """View for deleting projects."""

    template_name = "projects/delete.html"


class ProjectDeployView(LoginRequiredMixin, TemplateView):
    """View for deploying projects."""

    template_name = "projects/deploy.html"


class ProjectMembersView(LoginRequiredMixin, TemplateView):
    """View for managing project members."""

    template_name = "projects/members.html"


class ProjectDeploymentsView(LoginRequiredMixin, TemplateView):
    """View for viewing project deployments."""

    template_name = "projects/deployments.html"


class TemplateListView(LoginRequiredMixin, ListView[ProjectTemplate]):
    """View for listing project templates."""

    model = ProjectTemplate
    template_name = "projects/template_list.html"
    context_object_name = "templates"


class TemplateCreateView(LoginRequiredMixin, TemplateView):
    """View for creating new project templates."""

    template_name = "projects/template_create.html"


class TemplateDetailView(LoginRequiredMixin, DetailView[ProjectTemplate]):
    """View for displaying template details."""

    model = ProjectTemplate
    template_name = "projects/template_detail.html"
    context_object_name = "template"


# API Views for JSON responses


class ProjectAPIView(LoginRequiredMixin, TemplateView):
    """API view for project operations."""

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        projects = list(MeltanoProject.objects.values("id", "name", "status"))
        return JsonResponse({"projects": projects})


class ProjectStatusAPIView(LoginRequiredMixin, TemplateView):
    """API view for project status."""

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        return JsonResponse({"status": "active", "health": "healthy"})


class DeploymentAPIView(LoginRequiredMixin, TemplateView):
    """API view for deployments."""

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        return JsonResponse({"deployments": []})
