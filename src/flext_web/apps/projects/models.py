"""Django models for project management using flext-core patterns.

MIGRATED TO FLEXT-CORE:
Uses flext-core DomainValueObject and StrEnum patterns for structured data and
type safety.
"""

from __future__ import annotations

import uuid
from enum import StrEnum
from typing import TYPE_CHECKING, Any, ClassVar

if TYPE_CHECKING:
    from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class ProjectRole(StrEnum):
    """Project role enumeration using flext-core StrEnum."""

    VIEWER = "viewer"
    DEVELOPER = "developer"
    ADMIN = "REDACTED_LDAP_BIND_PASSWORD"
    OWNER = "owner"


class ProjectStatus(StrEnum):
    """Project status enumeration using flext-core StrEnum."""

    DRAFT = "draft"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"


class DeploymentEnvironment(StrEnum):
    """Deployment environment enumeration using flext-core StrEnum."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class ProjectTemplate(models.Model):
    """Project template model for standardized project creation."""

    id: models.UUIDField[uuid.UUID, uuid.UUID] = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name: models.CharField[str, str] = models.CharField(max_length=255, unique=True)
    description: models.TextField[str, str] = models.TextField()
    category: models.CharField[str, str] = models.CharField(max_length=100)
    version: models.CharField[str, str] = models.CharField(max_length=50, default="1.0.0")

    # Template configuration
    template_config: models.JSONField[dict[str, Any], dict[str, Any]] = models.JSONField(
        default=dict,
        help_text="Template configuration and default settings",
    )

    # Status
    is_active: models.BooleanField[bool, bool] = models.BooleanField(default=True)

    # Audit fields
    created_at: models.DateTimeField[datetime, datetime] = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField[datetime, datetime] = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta configuration for ProjectTemplate model."""

        db_table = "flext_project_templates"
        ordering: ClassVar[list[str]] = ["category", "name"]
        verbose_name = "Project Template"
        verbose_name_plural = "Project Templates"

    def __str__(self) -> str:
        return f"{self.name} (v{self.version})"


class MeltanoProject(models.Model):
    """Meltano project model with enterprise features."""

    id: models.UUIDField[uuid.UUID, uuid.UUID] = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name: models.CharField[str, str] = models.CharField(max_length=255, unique=True)
    description: models.TextField[str, str] = models.TextField(blank=True)

    # Project relationship
    template: models.ForeignKey[ProjectTemplate, ProjectTemplate] = models.ForeignKey(
        ProjectTemplate,
        on_delete=models.PROTECT,
        related_name="projects",
    )

    # Project configuration
    project_config: models.JSONField[dict[str, Any], dict[str, Any]] = models.JSONField(
        default=dict,
        help_text="Project-specific configuration",
    )

    # Status
    status: models.CharField[str, str] = models.CharField(
        max_length=20,
        choices=[(status.value, status.value.title()) for status in ProjectStatus],
        default=ProjectStatus.DRAFT.value,
    )
    is_active: models.BooleanField[bool, bool] = models.BooleanField(default=True)

    # Audit fields
    created_by: models.ForeignKey[User, User] = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_projects",
    )
    created_at: models.DateTimeField[datetime, datetime] = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField[datetime, datetime] = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta configuration for MeltanoProject model."""

        db_table = "flext_meltano_projects"
        ordering: ClassVar[list[str]] = ["-created_at"]
        verbose_name = "Meltano Project"
        verbose_name_plural = "Meltano Projects"

    def __str__(self) -> str:
        return str(self.name)


class ProjectMembership(models.Model):
    """Project team membership model."""

    id: models.UUIDField[uuid.UUID, uuid.UUID] = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    project: models.ForeignKey[MeltanoProject, MeltanoProject] = models.ForeignKey(
        MeltanoProject,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    user: models.ForeignKey[User, User] = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="project_memberships",
    )
    role: models.CharField[str, str] = models.CharField(
        max_length=20,
        choices=[(role.value, role.value.title()) for role in ProjectRole],
        default=ProjectRole.VIEWER.value,
    )

    # Audit fields
    created_by: models.ForeignKey[User, User] = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_memberships",
    )
    created_at: models.DateTimeField[datetime, datetime] = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta configuration for ProjectMembership model."""

        db_table = "flext_project_memberships"
        unique_together: ClassVar[list[str]] = ["project", "user"]
        verbose_name = "Project Membership"
        verbose_name_plural = "Project Memberships"

    def __str__(self) -> str:
        return f"{self.user.username} - {self.project.name} ({self.role})"


class ProjectDeployment(models.Model):
    """Project deployment tracking model."""

    id: models.UUIDField[uuid.UUID, uuid.UUID] = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    project: models.ForeignKey[MeltanoProject, MeltanoProject] = models.ForeignKey(
        MeltanoProject,
        on_delete=models.CASCADE,
        related_name="deployments",
    )
    environment: models.CharField[str, str] = models.CharField(
        max_length=20,
        choices=[(env.value, env.value.title()) for env in DeploymentEnvironment],
    )
    status: models.CharField[str, str] = models.CharField(max_length=50, default="deployed")

    # Deployment metadata
    deployed_at: models.DateTimeField[datetime, datetime] = models.DateTimeField(default=timezone.now)
    deployed_by: models.ForeignKey[User, User] = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="deployments",
    )

    class Meta:
        """Meta configuration for ProjectDeployment model."""

        db_table = "flext_project_deployments"
        ordering: ClassVar[list[str]] = ["-deployed_at"]
        verbose_name = "Project Deployment"
        verbose_name_plural = "Project Deployments"

    def __str__(self) -> str:
        return f"{self.project.name} - {self.environment} ({self.status})"
