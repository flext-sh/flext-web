"""Simplified dashboard views for testing Django functionality.

This module provides basic dashboard views without external gRPC dependencies,
allowing testing of Django core functionality and template rendering.
"""

from __future__ import annotations

from typing import Any

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


class DashboardView(TemplateView):
    """Main dashboard view with simplified functionality for testing."""

    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get context data for dashboard template rendering."""
        context = super().get_context_data(**kwargs)

        # Provide mock data for testing
        context.update(
            {
                "stats": {
                    "active_pipelines": 5,
                    "total_executions": 42,
                    "success_rate": 95.2,
                    "cpu_usage": 23.1,
                    "memory_usage": 67.8,
                },
                "health": {
                    "healthy": True,
                    "components": {
                        "database": {"healthy": True, "message": "Connected"},
                        "redis": {"healthy": True, "message": "Connected"},
                    },
                },
                "recent_executions": [
                    {
                        "id": "exec-001",
                        "pipeline_name": "Customer ETL",
                        "status": "success",
                        "started_at": "2025-07-11T01:00:00Z",
                        "duration": "2m 34s",
                    },
                    {
                        "id": "exec-002",
                        "pipeline_name": "Sales Analytics",
                        "status": "running",
                        "started_at": "2025-07-11T01:15:00Z",
                        "duration": "45s",
                    },
                ],
                "error": None,
            },
        )

        return context


class StatsAPIView(View):
    """API endpoint for real-time system statistics retrieval."""

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """Handle GET requests for real-time statistics API."""
        # Return mock stats data for testing
        stats_data = {
            "stats": {
                "active_pipelines": 5,
                "total_executions": 42,
                "success_rate": 95.2,
                "cpu_usage": 23.1,
                "memory_usage": 67.8,
                "uptime_seconds": 86400,
            },
            "health": {
                "healthy": True,
                "components": {
                    "database": {"healthy": True, "message": "Connected"},
                    "redis": {"healthy": True, "message": "Connected"},
                },
            },
            "recent_executions": [
                {
                    "id": "exec-001",
                    "pipeline_name": "Customer ETL",
                    "status": "success",
                    "started_at": "2025-07-11T01:00:00Z",
                    "duration": "2m 34s",
                },
            ],
        }

        return JsonResponse(stats_data)


def simple_dashboard_view(request):
    """Simple function-based view for testing basic Django functionality."""
    context = {
        "title": "FLEXT Web Dashboard",
        "message": "Django application is working correctly!",
        "user": request.user if request.user.is_authenticated else None,
    }

    return render(request, "dashboard/simple.html", context)
