"""Response DTO models for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_web import c, m, t, u


class FlextWebModelsResponses:
    """Web service response DTO models namespace."""

    class Web:
        """Web service response DTO models."""

        class AuthResponse(m.Value):
            """Authentication response model."""

            token: Annotated[str, u.Field(description="Authentication token")]
            user_id: Annotated[str, u.Field(description="User identifier")]
            authenticated: Annotated[bool, u.Field(description="Authentication status")]

        class UserResponse(m.Value):
            """User registration response model."""

            id: Annotated[str, u.Field(description="User identifier")]
            username: Annotated[str, u.Field(description="Username")]
            email: Annotated[str, u.Field(description="Email address")]
            created: Annotated[bool, u.Field(description="Creation status")]

        class ApplicationResponse(m.Value):
            """Application management response model."""

            id: Annotated[str, u.Field(description="Application identifier")]
            name: Annotated[str, u.Field(description="Application name")]
            host: Annotated[str, u.Field(description="Application host")]
            port: Annotated[t.PortNumber, u.Field(description="Application port")]
            status: Annotated[str, u.Field(description="Application status")]
            created_at: Annotated[str, u.Field(description="Creation timestamp")]

            @property
            def running(self) -> bool:
                """Whether the projected application is running."""
                is_running: bool = self.status == c.Web.Status.RUNNING.value
                return is_running

        class HealthResponse(m.Value):
            """Health check response model."""

            status: Annotated[str, u.Field(description="Health status")]
            service: Annotated[str, u.Field(description="Service name")]
            timestamp: Annotated[str, u.Field(description="Timestamp")]

        class MetricsResponse(m.Value):
            """Metrics response model."""

            service_status: Annotated[str, u.Field(description="Service status")]
            components: Annotated[
                t.StrSequence,
                u.Field(description="Service components"),
            ]

        class DashboardResponse(m.Value):
            """Dashboard response model."""

            total_applications: Annotated[
                int,
                u.Field(description="Total applications"),
            ]
            running_applications: Annotated[
                int,
                u.Field(description="Running applications"),
            ]
            service_status: Annotated[str, u.Field(description="Service status")]
            routes_initialized: Annotated[
                bool,
                u.Field(description="Routes initialization status"),
            ]
            middleware_configured: Annotated[
                bool,
                u.Field(
                    description="Middleware configuration status",
                ),
            ]
            timestamp: Annotated[str, u.Field(description="Timestamp")]

        class ServiceResponse(m.Value):
            """Generic service response model."""

            service: Annotated[str, u.Field(description="Service name")]
            capabilities: Annotated[
                t.StrSequence,
                u.Field(description="Service capabilities"),
            ]
            status: Annotated[str, u.Field(description="Service status")]
            settings: Annotated[bool, u.Field(description="Configuration status")]


__all__: list[str] = ["FlextWebModelsResponses"]
