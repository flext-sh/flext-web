"""Response DTO models for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_cli import m

from flext_web import c, t


class FlextWebModelsResponses:
    """Web service response DTO models."""

    class AuthResponse(m.Value):
        """Authentication response model."""

        token: Annotated[str, m.Field(description="Authentication token")]
        user_id: Annotated[str, m.Field(description="User identifier")]
        authenticated: Annotated[bool, m.Field(description="Authentication status")]

    class UserResponse(m.Value):
        """User registration response model."""

        id: Annotated[str, m.Field(description="User identifier")]
        username: Annotated[str, m.Field(description="Username")]
        email: Annotated[str, m.Field(description="Email address")]
        created: Annotated[bool, m.Field(description="Creation status")]

    class ApplicationResponse(m.Value):
        """Application management response model."""

        id: Annotated[str, m.Field(description="Application identifier")]
        name: Annotated[str, m.Field(description="Application name")]
        host: Annotated[str, m.Field(description="Application host")]
        port: Annotated[t.PortNumber, m.Field(description="Application port")]
        status: Annotated[str, m.Field(description="Application status")]
        created_at: Annotated[str, m.Field(description="Creation timestamp")]

        @property
        def running(self) -> bool:
            """Whether the projected application is running."""
            is_running: bool = self.status == c.Web.Status.RUNNING.value
            return is_running

    class HealthResponse(m.Value):
        """Health check response model."""

        status: Annotated[str, m.Field(description="Health status")]
        service: Annotated[str, m.Field(description="Service name")]
        timestamp: Annotated[str, m.Field(description="Timestamp")]

    class MetricsResponse(m.Value):
        """Metrics response model."""

        service_status: Annotated[str, m.Field(description="Service status")]
        components: Annotated[t.StrSequence, m.Field(description="Service components")]

    class DashboardResponse(m.Value):
        """Dashboard response model."""

        total_applications: Annotated[int, m.Field(description="Total applications")]
        running_applications: Annotated[
            int,
            m.Field(description="Running applications"),
        ]
        service_status: Annotated[str, m.Field(description="Service status")]
        routes_initialized: Annotated[
            bool,
            m.Field(description="Routes initialization status"),
        ]
        middleware_configured: Annotated[
            bool,
            m.Field(description="Middleware configuration status"),
        ]
        timestamp: Annotated[str, m.Field(description="Timestamp")]

    class ServiceResponse(m.Value):
        """Generic service response model."""

        service: Annotated[str, m.Field(description="Service name")]
        capabilities: Annotated[
            t.StrSequence,
            m.Field(description="Service capabilities"),
        ]
        status: Annotated[str, m.Field(description="Service status")]
        settings: Annotated[bool, m.Field(description="Configuration status")]


__all__: list[str] = ["FlextWebModelsResponses"]
