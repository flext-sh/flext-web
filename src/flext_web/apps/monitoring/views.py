"""Enterprise monitoring views with real-time metrics and alerting.

Comprehensive monitoring interface providing:
- Real-time business metrics visualization
- Security violation monitoring
- Error pattern analysis and recovery tracking
- Performance monitoring and alerting
- Health status dashboard with component details
"""

from __future__ import annotations

import asyncio
import functools
import operator
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from flext_core.config.domain_config import get_config
from flext_core.security.advanced_validation import AdvancedSecurityValidator
from flext_observability.health import HealthChecker
from flext_observability.metrics import MetricsCollector
from flext_observability.monitoring.business_metrics import EnterpriseBusinessMetrics
from flext_observability.monitoring.error_patterns import ProductionErrorHandler

if TYPE_CHECKING:
    from django.http import HttpRequest

# Python 3.13 type aliases for monitoring domain
MonitoringStats = dict[str, int | float | list[dict[str, Any]]]
AlertData = dict[str, str | int | float]
SecurityStats = dict[str, int | dict[str, Any]]
HealthData = dict[str, bool | dict[str, Any]]


class EnterpriseMonitoringService:
    """Unified monitoring service integrating all enterprise monitoring systems.

    Consolidates business metrics, error patterns, security validation,
    and health monitoring into a single coherent monitoring interface.
    """

    def __init__(self) -> None:
        self.config = get_config()
        self.metrics_collector = MetricsCollector()
        self.business_metrics = EnterpriseBusinessMetrics(self.metrics_collector)
        self.error_handler = ProductionErrorHandler()
        self.health_monitor = HealthChecker()
        self.security_validator = AdvancedSecurityValidator()

    async def get_comprehensive_monitoring_data(self) -> dict[str, Any]:
        """Collect comprehensive monitoring data from all enterprise systems.

        Returns:
            dict[str, Any]: Comprehensive monitoring data including business metrics,
                error patterns, security stats, health status, and consolidated alerts.

        """
        try:
            # Collect data from all monitoring systems in parallel
            business_data = await self._get_business_metrics_data()
            error_data = await self._get_error_patterns_data()
            security_data = await self._get_security_stats_data()
            health_data = await self._get_health_status_data()

            # Consolidate alerts from all systems
            all_alerts = await self._consolidate_alerts()

            return {
                "business_metrics": business_data,
                "error_patterns": error_data,
                "security_stats": security_data,
                "health_status": health_data,
                "alerts": all_alerts,
                "timestamp": datetime.now(UTC).isoformat(),
                "status": "healthy" if len(all_alerts) == 0 else "degraded",
            }

        except Exception as e:
            return {
                "error": f"Failed to collect monitoring data: {e}",
                "timestamp": datetime.now(UTC).isoformat(),
                "status": "error",
            }

    async def _get_business_metrics_data(self) -> dict[str, Any]:
        metrics = await self.business_metrics.collect_business_metrics()

        # Group metrics by type for dashboard display
        metrics_by_type = {}
        for metric in metrics:
            metric_type = metric.metric_type.value
            if metric_type not in metrics_by_type:
                metrics_by_type[metric_type] = []

            metrics_by_type[metric_type].append(
                {
                    "name": metric.name,
                    "current_value": metric.current_value,
                    "previous_value": metric.previous_value,
                    "trend_direction": metric.trend_direction,
                    "trend_percentage": metric.trend_percentage,
                    "metadata": metric.metadata,
                    "timestamp": metric.timestamp.isoformat(),
                },
            )

        return {
            "metrics_by_type": metrics_by_type,
            "summary": self.business_metrics.get_metrics_summary(),
            "active_alerts": [
                {
                    "alert_id": alert.alert_id,
                    "title": alert.title,
                    "severity": alert.severity.value,
                    "metric_value": alert.metric_value,
                    "threshold": alert.threshold,
                    "timestamp": alert.timestamp.isoformat(),
                }
                for alert in self.business_metrics.get_active_alerts()
            ],
        }

    async def _get_error_patterns_data(self) -> dict[str, Any]:
        error_stats = self.error_handler.get_error_statistics()
        recent_violations = self.error_handler.get_recent_violations(limit=20)

        return {
            "statistics": error_stats,
            "recent_violations": [
                {
                    "pattern_id": str(violation.pattern_id),
                    "error_signature": violation.error_signature[
                        :100
                    ],  # Truncate for display
                    "category": violation.category.value,
                    "severity": violation.severity.value,
                    "occurrence_count": violation.occurrence_count,
                    "recovery_action": violation.recovery_action.value,
                    "last_seen": violation.last_seen.isoformat(),
                }
                for violation in recent_violations
            ],
        }

    async def _get_security_stats_data(self) -> dict[str, Any]:
        security_stats = self.security_validator.get_security_statistics()
        recent_violations = self.security_validator.get_recent_violations(limit=15)

        return {
            "statistics": security_stats,
            "recent_violations": [
                {
                    "violation_id": violation.violation_id,
                    "threat_level": violation.threat_level.value,
                    "validation_type": violation.validation_type.value,
                    "description": violation.violation_description,
                    "source_ip": violation.source_ip,
                    "user_id": violation.user_id,
                    "timestamp": violation.timestamp.isoformat(),
                    "blocked": violation.blocked,
                }
                for violation in recent_violations
            ],
        }

    async def _get_health_status_data(self) -> dict[str, Any]:
        try:
            health_status = await self.health_monitor.check_health()

            return {
                "overall_healthy": health_status["status"] == "healthy",
                "components": {
                    component["name"]: {
                        "healthy": (
                            component["status"].value == "healthy"
                            if hasattr(component["status"], "value")
                            else component["status"] == "healthy"
                        ),
                        "message": component["message"],
                        "metadata": component["metadata"],
                        "details": component.get("details", {}),
                    }
                    for component in health_status["components"]
                },
                "timestamp": health_status["timestamp"],
            }
        except Exception:
            return {
                "overall_healthy": False,
                "components": {},
                "error": "Health monitoring unavailable",
                "timestamp": datetime.now(UTC).isoformat(),
            }

    async def _consolidate_alerts(self) -> list[dict[str, Any]]:
        # Business metric alerts
        alerts = [
            {
                "type": "business_metric",
                "id": alert.alert_id,
                "title": alert.title,
                "severity": alert.severity.value,
                "description": alert.description,
                "timestamp": alert.timestamp.isoformat(),
                "source": "business_metrics",
            }
            for alert in self.business_metrics.get_active_alerts()
        ]

        # Error pattern alerts (high severity patterns)
        alerts.extend(
            {
                "type": "error_pattern",
                "id": str(violation.pattern_id),
                "title": f"Error Pattern: {violation.category.value.title()}",
                "severity": violation.severity.value,
                "description": f"Pattern detected {violation.occurrence_count} times",
                "timestamp": violation.last_seen.isoformat(),
                "source": "error_patterns",
            }
            for violation in self.error_handler.get_recent_violations(limit=5)
            if violation.severity.value in {"high", "critical"}
        )

        # Security violation alerts
        alerts.extend(
            {
                "type": "security_violation",
                "id": violation.violation_id,
                "title": f"Security: {violation.validation_type.value.replace('_', ' ').title()}",
                "severity": violation.threat_level.value,
                "description": violation.violation_description,
                "timestamp": violation.timestamp.isoformat(),
                "source": "security_validation",
            }
            for violation in self.security_validator.get_recent_violations(limit=5)
            if violation.threat_level.value in {"high", "critical"}
        )

        # Sort alerts by timestamp (most recent first)
        alerts.sort(key=operator.itemgetter("timestamp"), reverse=True)

        return alerts[:20]  # Return top 20 alerts


@functools.lru_cache(maxsize=1)
def get_monitoring_service() -> EnterpriseMonitoringService:
    return EnterpriseMonitoringService()


class MonitoringDashboardView(LoginRequiredMixin, TemplateView):
    """Main monitoring dashboard providing comprehensive enterprise monitoring.

    Features:
        - Real-time business metrics visualization
        - Security violation monitoring and alerting
        - Error pattern analysis and recovery tracking
        - System health monitoring with component details
        - Consolidated alerting across all monitoring systems
    """

    template_name = "monitoring/dashboard.html"

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        """Get context data for the monitoring dashboard template.

        Args:
            **kwargs: Additional keyword arguments passed to the view.

        Returns:
            dict[str, object]: Context data including comprehensive monitoring information.

        """
        context = super().get_context_data(**kwargs)

        # Get comprehensive monitoring data
        monitoring_service = get_monitoring_service()
        monitoring_data = asyncio.run(
            monitoring_service.get_comprehensive_monitoring_data(),
        )

        context.update(monitoring_data)

        return context


class BusinessMetricsAPIView(LoginRequiredMixin, View):
    """API endpoint for real-time business metrics data."""

    def get(self, _request: HttpRequest, *_args: object, **_kwargs: object) -> JsonResponse:
        """Handle GET request for business metrics API endpoint.

        Args:
            _request: The HTTP request object (unused).
            *_args: Additional positional arguments (unused).
            **_kwargs: Additional keyword arguments (unused).

        Returns:
            JsonResponse: JSON response containing business metrics data or error information.

        """
        try:
            monitoring_service = get_monitoring_service()
            business_data = asyncio.run(monitoring_service._get_business_metrics_data())

            return JsonResponse(
                {
                    "status": "success",
                    "data": business_data,
                    "timestamp": datetime.now(UTC).isoformat(),
                },
            )

        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now(UTC).isoformat(),
                },
                status=500,
            )


class SecurityMonitoringAPIView(LoginRequiredMixin, View):
    """API endpoint for real-time security monitoring data."""

    def get(self, _request: HttpRequest, *_args: object, **_kwargs: object) -> JsonResponse:
        """Handle GET request for security monitoring API endpoint.

        Args:
            _request: The HTTP request object (unused).
            *_args: Additional positional arguments (unused).
            **_kwargs: Additional keyword arguments (unused).

        Returns:
            JsonResponse: JSON response containing security monitoring data or error information.

        """
        try:
            monitoring_service = get_monitoring_service()
            security_data = asyncio.run(monitoring_service._get_security_stats_data())

            return JsonResponse(
                {
                    "status": "success",
                    "data": security_data,
                    "timestamp": datetime.now(UTC).isoformat(),
                },
            )

        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now(UTC).isoformat(),
                },
                status=500,
            )


class ErrorPatternsAPIView(LoginRequiredMixin, View):
    """API endpoint for error patterns and recovery data."""

    def get(self, _request: HttpRequest, *_args: object, **_kwargs: object) -> JsonResponse:
        """Handle GET request for error patterns API endpoint.

        Args:
            _request: The HTTP request object (unused).
            *_args: Additional positional arguments (unused).
            **_kwargs: Additional keyword arguments (unused).

        Returns:
            JsonResponse: JSON response containing error patterns data or error information.

        """
        try:
            monitoring_service = get_monitoring_service()
            error_data = asyncio.run(monitoring_service._get_error_patterns_data())

            return JsonResponse(
                {
                    "status": "success",
                    "data": error_data,
                    "timestamp": datetime.now(UTC).isoformat(),
                },
            )

        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now(UTC).isoformat(),
                },
                status=500,
            )


class HealthStatusAPIView(LoginRequiredMixin, View):
    """API endpoint for comprehensive health status monitoring."""

    def get(self, _request: HttpRequest, *_args: object, **_kwargs: object) -> JsonResponse:
        """Handle GET request for health status API endpoint.

        Args:
            _request: The HTTP request object (unused).
            *_args: Additional positional arguments (unused).
            **_kwargs: Additional keyword arguments (unused).

        Returns:
            JsonResponse: JSON response containing health status data or error information.

        """
        try:
            monitoring_service = get_monitoring_service()
            health_data = asyncio.run(monitoring_service._get_health_status_data())

            return JsonResponse(
                {
                    "status": "success",
                    "data": health_data,
                    "timestamp": datetime.now(UTC).isoformat(),
                },
            )

        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now(UTC).isoformat(),
                },
                status=500,
            )


class AlertsAPIView(LoginRequiredMixin, View):
    """API endpoint for consolidated alerts across all monitoring systems."""

    def get(self, _request: HttpRequest, *_args: object, **_kwargs: object) -> JsonResponse:
        """Handle GET request for alerts API endpoint.

        Args:
            _request: The HTTP request object (unused).
            *_args: Additional positional arguments (unused).
            **_kwargs: Additional keyword arguments (unused).

        Returns:
            JsonResponse: JSON response containing consolidated alerts data or error information.

        """
        try:
            monitoring_service = get_monitoring_service()
            alerts = asyncio.run(monitoring_service._consolidate_alerts())

            return JsonResponse(
                {
                    "status": "success",
                    "data": {
                        "alerts": alerts,
                        "count": len(alerts),
                        "critical_count": len(
                            [a for a in alerts if a["severity"] == "critical"],
                        ),
                        "high_count": len(
                            [a for a in alerts if a["severity"] == "high"],
                        ),
                    },
                    "timestamp": datetime.now(UTC).isoformat(),
                },
            )

        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now(UTC).isoformat(),
                },
                status=500,
            )


class MonitoringStatsAPIView(LoginRequiredMixin, View):
    """API endpoint for comprehensive monitoring statistics."""

    def get(self, _request: HttpRequest, *_args: object, **_kwargs: object) -> JsonResponse:
        """Handle GET request for monitoring statistics API endpoint.

        Args:
            _request: The HTTP request object (unused).
            *_args: Additional positional arguments (unused).
            **_kwargs: Additional keyword arguments (unused).

        Returns:
            JsonResponse: JSON response containing comprehensive monitoring statistics or error information.

        """
        try:
            monitoring_service = get_monitoring_service()
            monitoring_data = asyncio.run(
                monitoring_service.get_comprehensive_monitoring_data(),
            )

            # Calculate summary statistics
            stats = {
                "business_metrics_count": len(
                    monitoring_data.get("business_metrics", {}).get(
                        "metrics_by_type",
                        {},
                    ),
                ),
                "active_alerts_count": len(monitoring_data.get("alerts", [])),
                "security_violations_count": monitoring_data.get("security_stats", {})
                .get("statistics", {})
                .get("total_violations", 0),
                "error_patterns_count": monitoring_data.get("error_patterns", {})
                .get("statistics", {})
                .get("summary", {})
                .get("total_error_patterns", 0),
                "health_status": (
                    "healthy"
                    if monitoring_data.get("health_status", {}).get(
                        "overall_healthy",
                        False,
                    )
                    else "degraded"
                ),
                "last_updated": monitoring_data.get("timestamp"),
            }

            return JsonResponse(
                {
                    "status": "success",
                    "data": stats,
                    "timestamp": datetime.now(UTC).isoformat(),
                },
            )

        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now(UTC).isoformat(),
                },
                status=500,
            )
