"""Application entity models for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import uuid
from collections.abc import MutableSequence
from typing import Annotated, override

from flext_cli import m, p, r, t, u
from flext_web.constants import c


class FlextWebModelsEntity:
    """Web application entity models namespace."""

    class Web:
        """Web application entity and configuration models."""

        class Entity(m.Entity):
            """Application entity with identity and lifecycle (Aggregate Root).

            Represents a web application as a domain entity with identity,
            state management, and event sourcing capabilities.

            Attributes:
                id: Unique application identifier
                name: Application name
                host: Application host address
                port: Application port number
                status: Current application status
                environment: Deployment environment
                debug_mode: Debug mode flag
                version: Application version
                metrics: Application metrics dictionary
                domain_events: List of domain events

            """

            id: Annotated[
                str,
                u.Field(
                    description="Unique application identifier",
                ),
            ] = u.Field(default_factory=lambda: str(uuid.uuid4()))
            name: Annotated[
                str,
                u.Field(
                    min_length=1,
                    max_length=c.Web.VALIDATION_NAME_LENGTH_RANGE[1],
                    description="Application name",
                ),
            ]

            @u.field_validator("name", mode="before")
            @classmethod
            def validate_name(cls, v: str) -> str:
                """Validate application name."""
                min_length = c.Web.VALIDATION_NAME_LENGTH_RANGE[0]
                max_length = c.Web.VALIDATION_NAME_LENGTH_RANGE[1]
                reserved_names = c.Web.SECURITY_RESERVED_NAMES

                if not (min_length <= len(v) <= max_length):
                    msg = (
                        f"Name must be between {min_length} and {max_length} characters"
                    )
                    raise ValueError(msg)

                if v.lower() in reserved_names:
                    msg = f"Name '{v}' is reserved and cannot be used"
                    raise ValueError(msg)

                dangerous_patterns = c.Web.SECURITY_DANGEROUS_PATTERNS
                for pattern in dangerous_patterns:
                    if pattern.lower() in v.lower():
                        msg = f"Name contains dangerous pattern: {pattern}"
                        raise ValueError(msg)

                return v

            host: Annotated[
                str,
                u.Field(
                    min_length=1,
                    max_length=c.Web.SECURITY_MAX_HOST_LENGTH,
                    description="Application host address",
                ),
            ] = c.Web.DEFAULT_HOST
            port: Annotated[
                t.PortNumber,
                u.Field(
                    description="Application port number",
                ),
            ] = c.Web.DEFAULT_PORT
            status: Annotated[
                c.Web.Status | str,
                u.Field(
                    description="Current application status",
                ),
            ] = c.Web.Status.STOPPED.value

            @u.field_validator("status", mode="before")
            @classmethod
            def validate_status(cls, v: str) -> str:
                """Validate application status against allowed values from constants."""
                valid_statuses = set(c.Web.STATUSES)
                if v not in valid_statuses:
                    msg = f"Invalid status '{v}'. Must be one of: {sorted(valid_statuses)}"
                    raise ValueError(msg)
                return v

            environment: Annotated[
                str,
                u.Field(
                    description="Deployment environment",
                ),
            ] = c.Web.Name.DEVELOPMENT.value
            debug_mode: Annotated[
                bool,
                u.Field(
                    description="Debug mode enabled flag",
                ),
            ] = c.Web.DEFAULT_DEBUG_MODE
            metrics: Annotated[
                t.MutableJsonMapping,
                u.Field(
                    description="Application metrics",
                ),
            ] = u.Field(default_factory=dict)
            web_events: Annotated[
                MutableSequence[str],
                u.Field(
                    description="Web-specific events (application lifecycle)",
                ),
            ] = u.Field(default_factory=list)

            @override
            def __str__(self) -> str:
                """Return string representation of the application."""
                return f"{self.name} ({self.url}) - {self.status}"

            @property
            def can_restart(self) -> bool:
                """Check if application can be restarted using u.in_() DSL pattern."""
                running = c.Web.Status.RUNNING.value
                stopped = c.Web.Status.STOPPED.value
                error = c.Web.Status.ERROR.value
                restartable: bool = self.status in {running, stopped, error}
                return restartable

            @property
            def can_start(self) -> bool:
                """Check if application can be started."""
                can_start: bool = self.status == c.Web.Status.STOPPED.value
                return can_start

            @property
            def can_stop(self) -> bool:
                """Check if application can be stopped."""
                can_stop: bool = self.status == c.Web.Status.RUNNING.value
                return can_stop

            @property
            def healthy(self) -> bool:
                """Check if application is healthy and operational."""
                running = c.Web.Status.RUNNING.value
                maintenance = c.Web.Status.MAINTENANCE.value
                is_healthy: bool = self.status in {running, maintenance}
                return is_healthy

            @property
            def running(self) -> bool:
                """Check if application is currently running."""
                is_running: bool = self.status == c.Web.Status.RUNNING.value
                return is_running

            @property
            def url(self) -> str:
                """Get the full URL with conditional protocol selection."""
                ssl_ports = c.Web.SECURITY_SSL_PORTS
                protocol = (
                    c.Web.DEFAULT_HTTPS_PROTOCOL
                    if u.in_(self.port, ssl_ports)
                    else c.Web.DEFAULT_HTTP_PROTOCOL
                )
                return f"{protocol}://{self.host}:{self.port}"

            @classmethod
            def format_id_from_name(cls, name: str) -> str:
                """Format application ID from name using web utilities.

                This method uses u.format_app_id directly,
                ensuring consistent ID formatting across the codebase.

                Args:
                    name: Application name to format

                Returns:
                    Formatted application ID

                Raises:
                    ValueError: If name cannot be formatted to valid ID

                """
                return u.format_app_id(name)

            def add_web_event(
                self,
                event_name: str,
            ) -> p.Result[bool]:
                """Add web-specific event (not domain event).

                This is for web application lifecycle events, not DDD domain events.
                Use parent's add_domain_event() for actual domain events.

                Returns:
                    r[bool]: Success contains True if event added,
                                    failure contains error message

                """
                if not event_name.strip():
                    return r[bool].fail("Event name cannot be empty")
                self.web_events.append(event_name)
                return r[bool].ok(value=True)

            def add_domain_event(
                self,
                event_type: str,
                data: m.ConfigMap
                | t.MappingKV[str, t.JsonPayload | None]
                | None = None,
            ) -> p.Result[m.Entry]:
                """Create and buffer a domain event for this web application entity."""
                if not event_type.strip():
                    return r[m.Entry].fail(
                        "Domain event name must be a non-empty string",
                    )
                if event_type.isdigit():
                    return r[m.Entry].fail(
                        "Domain event name cannot be numeric-only",
                    )
                entry = u.add_domain_event(
                    self,
                    event_type=event_type,
                    data=data,
                    aggregate_id=self.id,
                )
                return r[m.Entry].ok(entry)

            def health_status(self) -> t.ConfigurationMapping:
                """Get comprehensive health status."""
                return {
                    "status": self.status,
                    "running": self.running,
                    "healthy": self.healthy,
                    "url": self.url,
                    "version": self.version,
                    "environment": self.environment,
                }

            def restart(self) -> p.Result[FlextWebModelsEntity.Web.Entity]:
                """Restart the application."""
                can_restart_validated = self.can_restart
                if not can_restart_validated:
                    return r[FlextWebModelsEntity.Web.Entity].fail(
                        "Cannot restart in current state",
                    )
                starting_status = c.Web.Status.STARTING.value
                running_status = c.Web.Status.RUNNING.value
                self.status = starting_status
                restart_event_result = self.add_web_event("ApplicationRestarting")
                if restart_event_result.failure:  # pragma: no cover
                    return r[FlextWebModelsEntity.Web.Entity].fail(
                        f"Failed to add web event: {restart_event_result.error}",
                    )
                self.status = running_status
                start_event_result = self.add_web_event("ApplicationStarted")
                if start_event_result.failure:  # pragma: no cover
                    return r[FlextWebModelsEntity.Web.Entity].fail(
                        f"Failed to add web event: {start_event_result.error}",
                    )
                return r[FlextWebModelsEntity.Web.Entity].ok(self)

            def start(self) -> p.Result[FlextWebModelsEntity.Web.Entity]:
                """Start the application."""
                running_status = c.Web.Status.RUNNING.value
                already_running = self.status == running_status
                if already_running:
                    return r[FlextWebModelsEntity.Web.Entity].fail(
                        "already running",
                    )
                self.status = running_status
                event_result = self.add_web_event("ApplicationStarted")
                if event_result.failure:  # pragma: no cover
                    return r[FlextWebModelsEntity.Web.Entity].fail(
                        f"Failed to add web event: {event_result.error}",
                    )
                return r[FlextWebModelsEntity.Web.Entity].ok(self)

            def stop(self) -> p.Result[FlextWebModelsEntity.Web.Entity]:
                """Stop the application."""
                running_status = c.Web.Status.RUNNING.value
                stopped_status = c.Web.Status.STOPPED.value
                not_running = self.status != running_status
                if not_running:
                    return r[FlextWebModelsEntity.Web.Entity].fail(
                        "not running",
                    )
                self.status = stopped_status
                event_result = self.add_web_event("ApplicationStopped")
                if event_result.failure:  # pragma: no cover
                    return r[FlextWebModelsEntity.Web.Entity].fail(
                        f"Failed to add web event: {event_result.error}",
                    )
                return r[FlextWebModelsEntity.Web.Entity].ok(self)

            def update_metrics(self, new_metrics: t.JsonMapping) -> p.Result[bool]:
                """Update application metrics.

                Returns:
                    r[bool]: Success contains True if metrics updated,
                                    failure contains error message

                """
                supported_metrics = {
                    "requests",
                    "errors",
                    "uptime",
                    "avg_response_time_ms",
                }
                if not all(key in supported_metrics for key in new_metrics):
                    return r[bool].fail(
                        "Metrics must be a dict of supported metric keys",
                    )
                self.metrics.update(new_metrics)
                event_result = self.add_web_event("MetricsUpdated")
                if event_result.failure:  # pragma: no cover
                    return r[bool].fail(
                        f"Failed to add web event: {event_result.error}",
                    )
                return r[bool].ok(value=True)

            def validate_business_rules(self) -> p.Result[bool]:
                """Validate application business rules (Aggregate validation).

                Fast-fail validation - no fallbacks, explicit checks only.

                Returns:
                    r[bool]: Success contains True if valid, failure with error message

                """
                min_name_length = c.Web.VALIDATION_NAME_LENGTH_RANGE[0]
                if len(self.name) < min_name_length:
                    return r[bool].fail(
                        f"App name must be at least {min_name_length} characters",
                    )

                min_port = c.Web.VALIDATION_PORT_RANGE[0]
                max_port = c.Web.VALIDATION_PORT_RANGE[1]
                if not (min_port <= self.port <= max_port):
                    return r[bool].fail(
                        f"Port must be between {min_port} and {max_port}",
                    )
                return r[bool].ok(value=True)

            @classmethod
            def create_application(
                cls,
                settings: FlextWebModelsEntity.Web.EntityConfig,
            ) -> p.Result[FlextWebModelsEntity.Web.Entity]:
                """Build an :class:`Entity` from an ``EntityConfig`` snapshot."""
                return r[FlextWebModelsEntity.Web.Entity].create_from_callable(
                    lambda: cls(
                        name=settings.app_name,
                        host=settings.host,
                        port=settings.port,
                        status=getattr(
                            settings,
                            "status",
                            c.Web.Status.STOPPED.value,
                        ),
                        environment=getattr(
                            settings,
                            "environment",
                            c.Web.Name.DEVELOPMENT.value,
                        ),
                        debug_mode=getattr(settings, "debug_mode", False),
                        version=getattr(settings, "version", 0),
                        domain_events=[],
                    ),
                )

        class EntityConfig(m.Value):
            """Application entity configuration (Value Object).

            Represents configuration settings for application entities.
            Uses Constants for defaults - Config has priority when provided.
            """

            app_name: Annotated[
                str,
                u.Field(
                    min_length=c.Web.VALIDATION_NAME_LENGTH_RANGE[0],
                    max_length=c.Web.VALIDATION_NAME_LENGTH_RANGE[1],
                    description="Application name",
                ),
            ] = c.Web.DEFAULT_APP_NAME
            host: Annotated[
                str,
                u.Field(
                    min_length=1,
                    max_length=c.Web.SECURITY_MAX_HOST_LENGTH,
                    description="Application host address",
                ),
            ] = c.Web.DEFAULT_HOST
            port: Annotated[
                t.PortNumber,
                u.Field(
                    description="Application port number",
                ),
            ] = c.Web.DEFAULT_PORT
            debug: Annotated[
                bool,
                u.Field(
                    description="Debug mode flag",
                ),
            ] = c.Web.DEFAULT_DEBUG_MODE
            secret_key: Annotated[
                str,
                u.Field(
                    min_length=c.Web.SECURITY_MIN_SECRET_KEY_LENGTH,
                    description="Application secret key",
                ),
            ] = c.Web.DEFAULT_SECRET_KEY


__all__: list[str] = ["FlextWebModelsEntity"]
