"""FLEXT Projects Django Admin Configuration - Enterprise Administration.

This module configures Django REDACTED_LDAP_BIND_PASSWORD interface for enterprise project management,
providing comprehensive REDACTED_LDAP_BIND_PASSWORDistrative capabilities for production environments.
"""

from __future__ import annotations

from typing import ClassVar

from django.contrib import REDACTED_LDAP_BIND_PASSWORD

# from flext_web.models import (
#     MeltanoProject,
#     ProjectDeployment,
#     ProjectMembership,
#     ProjectTemplate,
# )
from .models import (
    MeltanoProject,
    ProjectDeployment,
    ProjectMembership,
    ProjectTemplate,
)


@REDACTED_LDAP_BIND_PASSWORD.register(ProjectTemplate)
class ProjectTemplateAdmin(REDACTED_LDAP_BIND_PASSWORD.ModelAdmin):
    """Django REDACTED_LDAP_BIND_PASSWORD configuration for ProjectTemplate model.

    Provides comprehensive template management with enterprise features
    including versioning, category filtering, and template validation.
    """

    list_display: ClassVar[list[str]] = [
        "name",
        "category",
        "version",
        "is_active",
        "created_at",
    ]
    list_filter: ClassVar[list[str]] = ["category", "is_active", "created_at"]
    search_fields: ClassVar[list[str]] = ["name", "description", "category"]
    readonly_fields: ClassVar[list[str]] = ["id", "created_at", "updated_at"]


class ProjectMembershipInline(REDACTED_LDAP_BIND_PASSWORD.TabularInline):
    """Inline REDACTED_LDAP_BIND_PASSWORD for project memberships."""

    model = ProjectMembership
    extra: ClassVar[int] = 0
    readonly_fields: ClassVar[list[str]] = ["id", "created_at", "created_by"]


@REDACTED_LDAP_BIND_PASSWORD.register(MeltanoProject)
class MeltanoProjectAdmin(REDACTED_LDAP_BIND_PASSWORD.ModelAdmin):
    """Django REDACTED_LDAP_BIND_PASSWORD configuration for MeltanoProject model."""

    list_display: ClassVar[list[str]] = [
        "name",
        "template",
        "status",
        "is_active",
        "created_at",
    ]
    list_filter: ClassVar[list[str]] = ["template", "status", "is_active"]
    search_fields: ClassVar[list[str]] = ["name", "description"]
    inlines = [ProjectMembershipInline]


@REDACTED_LDAP_BIND_PASSWORD.register(ProjectDeployment)
class ProjectDeploymentAdmin(REDACTED_LDAP_BIND_PASSWORD.ModelAdmin):
    """Django REDACTED_LDAP_BIND_PASSWORD configuration for ProjectDeployment model."""

    list_display: ClassVar[list[str]] = [
        "project",
        "environment",
        "status",
        "deployed_at",
    ]
    list_filter: ClassVar[list[str]] = ["environment", "status", "deployed_at"]
    readonly_fields: ClassVar[list[str]] = ["id", "deployed_at", "deployed_by"]
