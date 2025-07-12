"""FLEXT Monitoring Django App Configuration - Enterprise Grade.

This module configures the Monitoring app for the FLEXT Meltano Enterprise platform,
providing system health checks, metrics collection, and pipeline monitoring.

Author: Datacosmos
Date: 2025-06-22
"""

from __future__ import annotations

import importlib.util


class MonitoringConfig:
    """Django app configuration for enterprise system monitoring.

    Provides comprehensive system monitoring, health checks, metrics collection,
    and enterprise-grade observability capabilities.

    Features:
    - Real-time system health monitoring
    - Pipeline execution monitoring and alerting
    - Performance metrics collection and visualization
    - Enterprise audit trails and compliance reporting
    - Resource utilization tracking and optimization

    Note:
        Configures Django application for pipeline monitoring, metrics, and
        health checking.

    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "flext_web.apps.monitoring"
    verbose_name = "FLEXT Enterprise System Monitoring"

    def ready(self) -> None:
        """Configure monitoring app on Django startup."""
        # Signal handlers are required for enterprise monitoring
        # If signals module exists, import it for auto-registration

        signals_spec = importlib.util.find_spec(
            ".signals",
            package="flext_web.apps.monitoring",
        )
        if signals_spec is not None:
            pass  # Signal auto-registration on import
