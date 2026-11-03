# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_web/_protocols/responses
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

from flext_web import t


class FlextWebProtocolsResponses:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class AuthResponse(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def token(self) -> str:
            """Authentication token."""
            ...

        @property
        def user_id(self) -> str:
            """User identifier."""
            ...

        @property
        def authenticated(self) -> bool:
            """Authentication status."""
            ...

    @runtime_checkable
    class UserResponse(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def id(self) -> str:
            """User identifier."""
            ...

        @property
        def username(self) -> str:
            """Username."""
            ...

        @property
        def email(self) -> str:
            """Email address."""
            ...

        @property
        def created(self) -> bool:
            """Creation status."""
            ...

    @runtime_checkable
    class ApplicationResponse(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def id(self) -> str:
            """Application identifier."""
            ...

        @property
        def name(self) -> str:
            """Application name."""
            ...

        @property
        def host(self) -> str:
            """Application host."""
            ...

        @property
        def port(self) -> t.PortNumber:
            """Application port."""
            ...

        @property
        def status(self) -> str:
            """Application status."""
            ...

        @property
        def created_at(self) -> str:
            """Creation timestamp."""
            ...

        @property
        def running(self) -> bool:
            """Whether the projected application is running."""
            ...

    @runtime_checkable
    class HealthResponse(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def status(self) -> str:
            """Health status."""
            ...

        @property
        def service(self) -> str:
            """Service name."""
            ...

        @property
        def timestamp(self) -> str:
            """Timestamp."""
            ...

    @runtime_checkable
    class MetricsResponse(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def service_status(self) -> str:
            """Service status."""
            ...

        @property
        def components(self) -> Sequence[str]:
            """Service components."""
            ...

    @runtime_checkable
    class DashboardResponse(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def total_applications(self) -> int:
            """Total applications."""
            ...

        @property
        def running_applications(self) -> int:
            """Running applications."""
            ...

        @property
        def service_status(self) -> str:
            """Service status."""
            ...

        @property
        def routes_initialized(self) -> bool:
            """Routes initialization status."""
            ...

        @property
        def middleware_configured(self) -> bool:
            """Middleware configuration status."""
            ...

        @property
        def timestamp(self) -> str:
            """Timestamp."""
            ...

    @runtime_checkable
    class ServiceResponse(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def service(self) -> str:
            """Service name."""
            ...

        @property
        def capabilities(self) -> Sequence[str]:
            """Service capabilities."""
            ...

        @property
        def status(self) -> str:
            """Service status."""
            ...

        @property
        def settings(self) -> bool:
            """Configuration status."""
            ...


__all__: list[str] = [
    "FlextWebProtocolsResponses",
]
