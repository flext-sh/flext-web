"""Enterprise monitoring Django models for data persistence.

Models for storing and tracking monitoring data including:
- Business metrics history
- Security violation logs
- Error pattern tracking
- Health check results
- Alert management
"""

from __future__ import annotations

from typing import ClassVar

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class BusinessMetricType(models.TextChoices):
    """Business metric type choices matching core monitoring system."""

    PIPELINE_PERFORMANCE = "pipeline_performance", "Pipeline Performance"
    RESOURCE_UTILIZATION = "resource_utilization", "Resource Utilization"
    PLUGIN_EFFICIENCY = "plugin_efficiency", "Plugin Efficiency"
    USER_ACTIVITY = "user_activity", "User Activity"
    SYSTEM_RELIABILITY = "system_reliability", "System Reliability"


class AlertSeverity(models.TextChoices):
    """Alert severity levels matching core monitoring system."""

    INFO = "info", "Info"
    WARNING = "warning", "Warning"
    CRITICAL = "critical", "Critical"


class SecurityThreatLevel(models.TextChoices):
    """Security threat levels matching security validation system."""

    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    CRITICAL = "critical", "Critical"


class ErrorSeverity(models.TextChoices):
    """Error severity levels matching error pattern system."""

    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    CRITICAL = "critical", "Critical"


class BusinessMetricHistory(models.Model):
    """Historical business metrics for trend analysis and reporting."""

    name = models.CharField(max_length=100, db_index=True)
    metric_type = models.CharField(
        max_length=50,
        choices=BusinessMetricType.choices,
        db_index=True,
    )
    current_value = models.FloatField()
    previous_value = models.FloatField(null=True, blank=True)
    trend_direction = models.CharField(max_length=20, default="stable")
    metadata = models.JSONField(default=dict)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        """Django model configuration."""

        ordering: ClassVar = ["-timestamp"]
        indexes: ClassVar = [
            models.Index(fields=["name", "-timestamp"]),
            models.Index(fields=["metric_type", "-timestamp"]),
        ]

    def __str__(self) -> str:
        return (
            f"{self.name}: {self.current_value} "
            f"({self.timestamp.strftime('%Y-%m-%d %H:%M')})"
        )

    @property
    def trend_percentage(self) -> float | None:
        """Calculate percentage change from previous value.

        Returns:
            Percentage change from previous to current value, or None if
            previous_value is None or 0.

        """
        if self.previous_value is None or self.previous_value == 0:
            return None
        return ((self.current_value - self.previous_value) / self.previous_value) * 100


class SecurityViolationLog(models.Model):
    """Security violation logs for compliance and monitoring."""

    violation_id = models.CharField(max_length=100, unique=True, db_index=True)
    threat_level = models.CharField(
        max_length=20,
        choices=SecurityThreatLevel.choices,
        db_index=True,
    )
    validation_type = models.CharField(max_length=50, db_index=True)
    description = models.TextField()
    source_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        db_index=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    endpoint = models.CharField(max_length=200, blank=True, default="")
    user_agent = models.TextField(blank=True, default="")
    payload = models.JSONField(default=dict)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    blocked = models.BooleanField(default=True)
    resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True, default="")

    class Meta:
        """Django model configuration."""

        ordering: ClassVar = ["-timestamp"]
        indexes: ClassVar = [
            models.Index(fields=["threat_level", "-timestamp"]),
            models.Index(fields=["validation_type", "-timestamp"]),
            models.Index(fields=["source_ip", "-timestamp"]),
        ]

    def __str__(self) -> str:
        return (
            f"Security Violation: {self.validation_type} "
            f"({self.threat_level}) - "
            f"{self.timestamp.strftime('%Y-%m-%d %H:%M')}"
        )


class ErrorPatternLog(models.Model):
    """Error pattern tracking for system reliability monitoring."""

    pattern_id = models.CharField(max_length=100, db_index=True)
    error_signature = models.CharField(max_length=500, db_index=True)
    error_message = models.TextField()
    category = models.CharField(max_length=50, db_index=True)
    severity = models.CharField(
        max_length=20,
        choices=ErrorSeverity.choices,
        db_index=True,
    )
    occurrence_count = models.PositiveIntegerField(default=1)
    first_seen = models.DateTimeField(default=timezone.now)
    last_seen = models.DateTimeField(default=timezone.now, db_index=True)
    recovery_action = models.CharField(max_length=50)
    metadata = models.JSONField(default=dict)

    class Meta:
        """Django model configuration."""

        ordering: ClassVar = ["-last_seen"]
        indexes: ClassVar = [
            models.Index(fields=["category", "-last_seen"]),
            models.Index(fields=["severity", "-last_seen"]),
            models.Index(fields=["pattern_id", "-last_seen"]),
        ]

    def __str__(self) -> str:
        return (
            f"Error Pattern: {self.category} ({self.severity}) - "
            f"{self.occurrence_count} occurrences"
        )


class SystemHealthCheck(models.Model):
    """System health check results for monitoring system components."""

    component_name = models.CharField(max_length=100, db_index=True)
    healthy = models.BooleanField(db_index=True)
    message = models.TextField()
    metadata = models.JSONField(default=dict)
    response_time_ms = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        """Django model configuration."""

        ordering: ClassVar = ["-timestamp"]
        indexes: ClassVar = [
            models.Index(fields=["component_name", "-timestamp"]),
            models.Index(fields=["healthy", "-timestamp"]),
        ]

    def __str__(self) -> str:
        status = "Healthy" if self.healthy else "Unhealthy"
        return (
            f"{self.component_name}: {status} "
            f"({self.timestamp.strftime('%Y-%m-%d %H:%M')})"
        )


class MonitoringAlert(models.Model):
    """Enterprise monitoring alerts across all systems."""

    alert_id = models.CharField(max_length=100, unique=True, db_index=True)
    severity = models.CharField(
        max_length=20,
        choices=AlertSeverity.choices,
        db_index=True,
    )
    component = models.CharField(max_length=100, db_index=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    acknowledged = models.BooleanField(default=False, db_index=True)
    acknowledged_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved = models.BooleanField(default=False, db_index=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        """Django model configuration."""

        ordering: ClassVar = ["-created_at"]
        indexes: ClassVar = [
            models.Index(fields=["severity", "-created_at"]),
            models.Index(fields=["component", "-created_at"]),
            models.Index(fields=["acknowledged", "-created_at"]),
            models.Index(fields=["resolved", "-created_at"]),
        ]

    def __str__(self) -> str:
        return (
            f"Alert: {self.title} ({self.severity}) - "
            f"{self.created_at.strftime('%Y-%m-%d %H:%M')}"
        )

    @property
    def is_active(self) -> bool:
        """Check if alert is still active (not resolved)."""
        return not self.resolved
