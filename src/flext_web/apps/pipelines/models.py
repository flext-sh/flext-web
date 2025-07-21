"""Django models for pipeline management using flext-core patterns.

MIGRATED TO FLEXT-CORE:
Uses flext-core DomainValueObject and StrEnum patterns
for structured data and type safety.
"""

from __future__ import annotations

import uuid
from enum import StrEnum
from typing import Any, ClassVar

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from flext_core.domain import DomainValueObject


class PipelineConfiguration(DomainValueObject):
    """Pipeline configuration value object using flext-core patterns."""

    def __init__(self, **data: Any) -> None:
        """Initialize pipeline configuration."""
        super().__init__()
        self._data = data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PipelineConfiguration:
        """Create from dictionary."""
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self._data


class PipelineType(StrEnum):
    """Pipeline type enumeration using flext-core StrEnum."""

    ETL = "etl"
    ELT = "elt"
    STREAMING = "streaming"
    BATCH = "batch"
    REAL_TIME = "real_time"


class PipelineStatus(StrEnum):
    """Pipeline status enumeration using flext-core StrEnum."""

    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    DISABLED = "disabled"
    ARCHIVED = "archived"


class ExecutionStatus(StrEnum):
    """Execution status enumeration using flext-core StrEnum."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class PluginType(StrEnum):
    """Plugin type enumeration using flext-core StrEnum."""

    EXTRACTOR = "extractor"
    LOADER = "loader"
    TRANSFORMER = "transformer"
    ORCHESTRATOR = "orchestrator"
    UTILITY = "utility"


# Pipeline configuration will be stored as JSONField in Django models


class PipelineWeb(models.Model):
    """Data pipeline model for ETL/ELT operations using flext-core patterns."""

    id: models.UUIDField[uuid.UUID, uuid.UUID] = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name: models.CharField[str, str] = models.CharField(max_length=255, unique=True)
    description: models.TextField[str, str] = models.TextField(blank=True)

    # Project relationship
    project: models.ForeignKey[Any, Any] = models.ForeignKey(
        "projects.MeltanoProject",
        on_delete=models.CASCADE,
        related_name="pipelines",
        help_text="Project this pipeline belongs to",
    )

    # Pipeline components
    extractor: models.CharField[str, str] = models.CharField(max_length=255)
    loader: models.CharField[str, str] = models.CharField(max_length=255)
    transform: models.CharField[str, str] = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional transformer plugin",
    )

    # Pipeline configuration and metadata
    pipeline_type: models.CharField[str, str] = models.CharField(
        max_length=20,
        choices=[(ptype.value, ptype.value.title()) for ptype in PipelineType],
        default=PipelineType.ETL.value,
    )
    config: models.JSONField[dict[str, Any], dict[str, Any]] = models.JSONField(
        default=dict,
        help_text=(
            "Pipeline configuration including extractor, loader, and transform settings"
        ),
    )
    schedule: models.CharField[str, str] = models.CharField(
        max_length=255,
        blank=True,
        help_text="Cron expression for scheduled execution",
    )

    # Status and lifecycle
    status: models.CharField[str, str] = models.CharField(
        max_length=20,
        choices=[(status.value, status.value.title()) for status in PipelineStatus],
        default=PipelineStatus.DRAFT.value,
    )
    is_active: models.BooleanField[bool, bool] = models.BooleanField(
        default=True,
        help_text="Whether pipeline is enabled for execution",
    )

    # Execution tracking
    last_run: models.DateTimeField[Any | None, Any | None] = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp of last execution",
    )
    last_status: models.CharField[str, str] = models.CharField(
        max_length=20,
        choices=[(status.value, status.value.title()) for status in ExecutionStatus],
        blank=True,
        help_text="Status of last execution",
    )

    # Audit fields
    created_by: models.ForeignKey[User, User] = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_pipelines",
    )
    created_at: models.DateTimeField[Any, Any] = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField[Any, Any] = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta configuration for PipelineWeb model."""

        db_table = "flext_pipelines"
        ordering: ClassVar[list[str]] = ["-created_at"]
        verbose_name = "Pipeline"
        verbose_name_plural = "Pipelines"
        indexes: ClassVar[list[models.Index]] = [
            models.Index(fields=["status"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["last_run"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.pipeline_type_enum.value.title()})"

    def get_absolute_url(self) -> str:
        """Get the absolute URL for this pipeline instance.

        Returns:
            str: Absolute URL to the pipeline detail view.

        """
        return reverse("pipelines:detail", kwargs={"pk": self.pk})

    @property
    def pipeline_type_enum(self) -> PipelineType:
        """Get the pipeline type as an enum value.

        Returns:
            PipelineType: The pipeline type enum value.

        """
        return PipelineType(self.pipeline_type)

    @property
    def status_enum(self) -> PipelineStatus:
        """Get the pipeline status as an enum value.

        Returns:
            PipelineStatus: The pipeline status enum value.

        """
        return PipelineStatus(self.status)

    @property
    def last_status_enum(self) -> ExecutionStatus | None:
        """Get the last execution status as an enum value.

        Returns:
            ExecutionStatus | None: The last execution status enum value, or
            None if not set.

        """
        return ExecutionStatus(self.last_status) if self.last_status else None

    @property
    def config_object(self) -> PipelineConfiguration:
        """Get the pipeline configuration as a structured object.

        Returns:
            PipelineConfiguration: The pipeline configuration as a domain value object.

        """
        return PipelineConfiguration.from_dict(self.config)

    def update_config(self, config: PipelineConfiguration) -> None:
        """Update the pipeline configuration with a new configuration object.

        Args:
            config: New pipeline configuration to store.

        """
        self.config = config.to_dict()
