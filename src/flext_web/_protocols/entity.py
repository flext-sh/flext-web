# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_web/_protocols/entity
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

if TYPE_CHECKING:
    from flext_cli import p

    from flext_web import c, t


class FlextWebProtocolsEntity:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class Entity(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """Uncommitted domain events for event sourcing."""
            ...

        id: str
        name: str
        host: str
        port: t.PortNumber
        status: c.Web.Status | str
        environment: str
        debug_mode: bool
        metrics: MutableMapping[str, t.Scalar]
        web_events: MutableSequence[str]

        @property
        def can_restart(self) -> bool:
            """Whether application can be restarted using u.in_() DSL pattern."""
            ...

        @property
        def can_start(self) -> bool:
            """Whether application can be started."""
            ...

        @property
        def can_stop(self) -> bool:
            """Whether application can be stopped."""
            ...

        @property
        def healthy(self) -> bool:
            """Whether application is healthy and operational."""
            ...

        @property
        def running(self) -> bool:
            """Whether application is currently running."""
            ...

        @property
        def url(self) -> str:
            """Full URL with conditional protocol selection."""
            ...

        def add_web_event(self, event_name: str) -> p.Result[bool]:
            """Add web-specific event (not domain event)."""
            ...

        def add_domain_event(
            self,
            event_type: str,
            data: p.ConfigMap | Mapping[str, t.JsonPayload | None] | None = None,
        ) -> p.Result[p.DomainEvent]:
            """Create and buffer a domain event for this web application entity."""
            ...

        def health_status(self) -> t.ConfigurationMapping:
            """Get comprehensive health status."""
            ...

        def restart(self) -> p.Result[FlextWebProtocolsEntity.Entity]:
            """Restart the application."""
            ...

        def start(self) -> p.Result[FlextWebProtocolsEntity.Entity]:
            """Start the application."""
            ...

        def stop(self) -> p.Result[FlextWebProtocolsEntity.Entity]:
            """Stop the application."""
            ...

        def update_metrics(
            self, new_metrics: MutableMapping[str, t.Scalar] | Mapping[str, str]
        ) -> p.Result[bool]:
            """Update application metrics."""
            ...

        def validate_business_rules(self) -> p.Result[bool]:
            """Validate application business rules (Aggregate validation)."""
            ...

    @runtime_checkable
    class EntityConfig(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def app_name(self) -> str:
            """Application name."""
            ...

        @property
        def host(self) -> str:
            """Application host address."""
            ...

        @property
        def port(self) -> t.PortNumber:
            """Application port number."""
            ...

        @property
        def debug(self) -> bool:
            """Debug mode flag."""
            ...

        @property
        def secret_key(self) -> str:
            """Application secret key."""
            ...


__all__: list[str] = [
    "FlextWebProtocolsEntity",
]
