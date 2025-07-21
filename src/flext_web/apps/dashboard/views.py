"""Dashboard views with enterprise architecture patterns.

Implementation features:
    - Eliminated lazy imports for better dependency management
    - Unified configuration through domain_config.py
    - gRPC client consolidation with proper resource management
    - Python 3.13 type system throughout
    - Minimal code duplication with shared gRPC client service
    - Strategic TYPE_CHECKING for optimal imports
"""

from __future__ import annotations

import functools
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

import grpc
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

# Import gRPC with fallback for testing environments
try:
    from flext_grpc.client import FlextGrpcClientBase  # type: ignore[import-untyped]
    from google.protobuf import empty_pb2

    GRPC_AVAILABLE = True
except ImportError:
    FlextGrpcClientBase = None
    empty_pb2 = None  # type: ignore[assignment]
    GRPC_AVAILABLE = False

# Unified gRPC client and configuration from canonical implementation
from flext_core.config import get_config
from flext_core.domain.shared_models import SecurityConfig

if TYPE_CHECKING:
    from django.http import HttpRequest
    from flext_grpc.proto import flext_pb2
else:
    # Real imports at runtime - NO LAZY LOADING VIOLATIONS
    from flext_grpc.proto import flext_pb2

# Python 3.13 type aliases for dashboard domain
DashboardStats = dict[str, int | float]
HealthStatus = dict[str, bool | dict[str, Any]]
ExecutionData = dict[str, str | None]


if GRPC_AVAILABLE and FlextGrpcClientBase is not None:

    class FlextDashboardGrpcClient(FlextGrpcClientBase):  # type: ignore[misc]
        """Dashboard gRPC client extending base with dashboard-specific functionality.

        Inherits from FlextGrpcClientBase to eliminate duplication while providing
        specialized dashboard data formatting and retrieval methods.
        Renamed from FlextGrpcClient to avoid conflict with CLI FlextGrpcClient.
        """

        def __init__(self) -> None:
            super().__init__()

        def get_dashboard_data(self) -> dict[str, Any]:
            """Get complete dashboard data from gRPC server.

            Returns:
                Dictionary containing stats, health, recent_executions, and error.

            """
            try:
                with self._create_channel() as channel:
                    stub = self._create_stub(channel)

                    # Get all data in parallel using gRPC streaming if available:
                    stats_response = stub.GetSystemStats(empty_pb2.Empty())
                    health_response = stub.HealthCheck(empty_pb2.Empty())
                    get_config(SecurityConfig)  # type: ignore[type-var]
                    executions_response = stub.ListExecutions(
                        flext_pb2.ListExecutionsRequest(  # type: ignore[attr-defined]
                            limit=50,  # Default execution limit
                            offset=0,
                        ),
                    )

                    # Format dashboard data
                    return {
                        "stats": self._format_stats(stats_response),
                        "health": self._format_health(health_response),
                        "recent_executions": self._format_executions(
                            getattr(executions_response, "executions", []),
                        ),
                        "error": None,
                    }

            except grpc.RpcError as e:
                return {
                    "stats": self._get_default_stats(),
                    "health": self._get_default_health(),
                    "recent_executions": [],
                    "error": f"Unable to connect to FLEXT daemon: {e.details()}",
                }

        def get_stats_only(self) -> dict[str, Any]:
            """Get system statistics and execution data for API endpoints.

            Returns:
                Dictionary containing stats, health, and recent executions.

            """
            try:
                with self._create_channel() as channel:
                    stub = self._create_stub(channel)

                    # Parallel requests for minimal latency
                    stats_response = stub.GetSystemStats(empty_pb2.Empty())
                    health_response = stub.HealthCheck(empty_pb2.Empty())
                    get_config(SecurityConfig)  # type: ignore[type-var]
                    executions_response = stub.ListExecutions(
                        flext_pb2.ListExecutionsRequest(  # type: ignore[attr-defined]
                            limit=50,  # Default recent executions limit
                            offset=0,
                        ),
                    )

                    return {
                        "stats": {
                            **self._format_stats(stats_response),
                            "uptime_seconds": getattr(
                                stats_response, "uptime_seconds", 0,
                            ),
                        },
                        "health": self._format_health(health_response),
                        "recent_executions": [
                            {
                                **self._format_execution(execution),
                                "started_at": (
                                    execution.started_at.ToDatetime().isoformat()
                                    if hasattr(execution, "started_at")
                                    and execution.started_at
                                    and hasattr(execution.started_at, "ToDatetime")
                                    else None
                                ),
                            }
                            for execution in getattr(
                                executions_response, "executions", [],
                            )
                        ],
                    }

            except grpc.RpcError as e:
                return {
                    "error": f"gRPC error: {e.details()}",
                    "status_code": 503,
                }

        def _format_stats(self, stats_response: object) -> DashboardStats:
            return {
                "active_pipelines": getattr(stats_response, "active_pipelines", 0),
                "total_executions": getattr(stats_response, "total_executions", 0),
                "success_rate": round(getattr(stats_response, "success_rate", 0.0), 1),
                "cpu_usage": round(getattr(stats_response, "cpu_usage", 0.0), 1),
                "memory_usage": round(getattr(stats_response, "memory_usage", 0.0), 1),
            }

        def _format_health(self, health_response: object) -> HealthStatus:
            components = {}
            if hasattr(health_response, "components"):
                for name, comp in health_response.components.items():
                    components[name] = {
                        "healthy": getattr(comp, "healthy", False),
                        "message": getattr(comp, "message", ""),
                        "metadata": dict(getattr(comp, "metadata", {})),
                    }

            return {
                "healthy": getattr(health_response, "healthy", False),
                "components": components,
            }

        def _format_executions(self, executions: list[Any]) -> list[ExecutionData]:
            return [self._format_execution(execution) for execution in executions]

        def _format_execution(self, execution: object) -> ExecutionData:
            started_at_str = None
            if (hasattr(execution, "started_at")
                and execution.started_at
                and hasattr(execution.started_at, "ToDatetime")):
                try:
                    started_at_str = execution.started_at.ToDatetime().isoformat()
                except Exception:
                    started_at_str = None

            return {
                "id": getattr(execution, "id", ""),
                "pipeline_name": getattr(execution, "pipeline_id", ""),
                "status": getattr(execution, "status", "unknown"),
                "started_at": started_at_str,
                "duration": self._calculate_duration(execution),
            }

        def _calculate_duration(self, execution: object) -> str | None:
            if not hasattr(execution, "started_at") or not execution.started_at:
                return None

            try:
                start_time = (
                    execution.started_at.ToDatetime()
                    if hasattr(execution.started_at, "ToDatetime")
                    else datetime.now(UTC)
                )
            except Exception:
                start_time = datetime.now(UTC)

            try:
                end_time = (
                    execution.completed_at.ToDatetime()
                    if hasattr(execution, "completed_at")
                    and execution.completed_at
                    and hasattr(execution.completed_at, "ToDatetime")
                    else datetime.now(UTC)
                )
            except Exception:
                end_time = datetime.now(UTC)

            duration = end_time - start_time
            total_seconds = int(duration.total_seconds())

            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            if hours > 0:
                return f"{hours}h {minutes}m"
            if minutes > 0:
                return f"{minutes}m {seconds}s"
            return f"{seconds}s"

        def _get_default_stats(self) -> DashboardStats:
            return {
                "active_pipelines": 0,
                "total_executions": 0,
                "success_rate": 0,
                "cpu_usage": 0,
                "memory_usage": 0,
            }

        def _get_default_health(self) -> HealthStatus:
            return {
                "healthy": False,
                "components": {},
            }

else:
    # Fallback class when gRPC is not available
    class FlextDashboardGrpcClient:  # type: ignore[no-redef]
        """Fallback dashboard client when gRPC is not available."""

        def __init__(self) -> None:
            pass

        def get_dashboard_data(self) -> dict[str, Any]:
            """Return fallback dashboard data."""
            return {
                "stats": {"pipelines": 0, "executions": 0, "active_connections": 0},
                "health": {"healthy": False, "components": {}},
                "recent_executions": [],
                "error": "gRPC service not available - running in fallback mode",
            }

        def get_stats_only(self) -> dict[str, Any]:
            """Return fallback stats data."""
            return {
                "stats": {"pipelines": 0, "executions": 0, "active_connections": 0},
                "health": {"healthy": False, "components": {}},
                "recent_executions": [],
                "error": "gRPC service not available",
            }


@functools.lru_cache(maxsize=1)
def get_grpc_client() -> FlextDashboardGrpcClient:
    """Get gRPC client with fallback support."""
    return FlextDashboardGrpcClient()


class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard view providing comprehensive system overview.

    This view renders the main dashboard template with real-time system statistics,
    health monitoring data, and recent execution information using unified gRPC client.

    Features:
        - Real-time system metrics display
        - Health status monitoring
        - Recent pipeline execution history
        - Unified gRPC client for data retrieval
    """

    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        """Get context data for dashboard template rendering.

        Args:
            **kwargs: Additional context arguments.

        Returns:
            Context dictionary with dashboard data for template rendering.

        """
        context = super().get_context_data(**kwargs)

        # Get all dashboard data through unified client
        dashboard_data = get_grpc_client().get_dashboard_data()
        context.update(dashboard_data)

        return context


class StatsAPIView(LoginRequiredMixin, View):
    """API endpoint for real-time system statistics retrieval.

    This view provides a JSON API endpoint for retrieving current system
    statistics without full page reload, enabling real-time dashboard updates.

    Features:
        - Real-time system metrics API
        - JSON response format
        - Error handling with appropriate status codes
        - Unified gRPC client integration
    """

    def get(
        self,
        _request: HttpRequest,
        *_args: object,
        **_kwargs: object,
    ) -> JsonResponse:
        """Handle GET requests for real-time statistics API.

        Args:
            _request: HTTP request object.
            *_args: Additional positional arguments.
            **_kwargs: Additional keyword arguments.

        Returns:
            JSON response with current system statistics or error information.

        """
        try:
            grpc_client = get_grpc_client()
            stats_data = grpc_client.get_stats_only()

            # Handle error response
            if "error" in stats_data:
                return JsonResponse(
                    {"error": stats_data["error"]},
                    status=stats_data.get("status_code", 503),
                )

            return JsonResponse(stats_data)
        except Exception as e:
            # Handle unexpected exceptions
            return JsonResponse(
                {"error": f"Unexpected error: {e}"},
                status=500,
            )


# ZERO TOLERANCE CONSOLIDATION: Backward compatibility alias
FlextGrpcClient = FlextDashboardGrpcClient
