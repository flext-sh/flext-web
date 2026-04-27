"""FLEXT Web models for web applications.

Provides Pydantic models for web-based applications with validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import uuid
from collections.abc import (
    Mapping,
    MutableSequence,
)
from datetime import UTC, datetime
from threading import Thread
from typing import Annotated, ClassVar, override
from wsgiref.simple_server import WSGIServer

import uvicorn
from flext_cli import m, p, t

from flext_web import c, r, u


class FlextWebModels(m):
    """Web application models collection.

    Provides Pydantic models for web applications with validation.
    """

    class Web:
        """Web application models for HTTP protocol and application entities.

        Contains HTTP message models, application entities, and web-specific
        domain objects used throughout the FLEXT web ecosystem.

        Models are immutable value objects (frozen=True) following domain-driven
        design principles with Pydantic v2 validation.
        """

        class Message(m.Value):
            """Generic HTTP message base model with protocol validation.

            Represents common HTTP message structure with headers, body,
            and timestamp. Used as base for Request and Response models.

            Attributes:
                headers: HTTP headers dictionary mapping header names to values
                body: Message body as string, dict, or None for no body
                timestamp: UTC timestamp when message was created

            """

            headers: Annotated[
                t.MutableStrMapping,
                u.Field(
                    description="HTTP headers for message",
                ),
            ] = u.Field(default_factory=dict)
            body: Annotated[
                str | t.ScalarMapping | None,
                u.Field(
                    description="Message body content (optional for GET/HEAD)",
                ),
            ] = None
            timestamp: Annotated[
                datetime,
                u.Field(
                    description="UTC timestamp of message creation",
                ),
            ] = u.Field(default_factory=lambda: datetime.now(UTC))

        class Request(Message):
            """HTTP request model with complete validation.

            Represents a complete HTTP request following HTTP specifications
            with full validation of URL, method, and timeout parameters.

            Attributes:
            url: Request URL with length validation
            method: HTTP method (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
            timeout: Request timeout in seconds (0-300)

            """

            url: Annotated[
                str,
                u.Field(
                    min_length=1,
                    max_length=c.Web.VALIDATION_URL_LENGTH_RANGE[1],
                    description="Request URL",
                ),
            ]
            method: Annotated[
                c.Web.Method,
                u.BeforeValidator(str.upper),
                u.Field(
                    description="HTTP method (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)",
                ),
            ] = c.Web.Method.GET
            timeout: Annotated[
                t.PositiveTimeout,
                u.Field(
                    description="Request timeout in seconds",
                ),
            ] = c.Web.DEFAULT_TIMEOUT_SECONDS

            @property
            def has_body(self) -> bool:
                """Check if HTTP request has a message body.

                Returns:
                True if body is not None, False otherwise

                """
                return self.body is not None

            @property
            def secure(self) -> bool:
                """Check if HTTP request uses HTTPS protocol.

                Returns:
                True if URL starts with 'https://', False otherwise

                """
                return self.url.startswith("https://")

        class Response(Message):
            """HTTP response model with status validation.

            Represents a complete HTTP response with status code validation
            and response-specific properties.

            Attributes:
            status_code: HTTP status code (100-599)
            elapsed_time: Time taken to process response in seconds

            """

            status_code: Annotated[
                t.HttpStatusCode,
                u.Field(
                    ...,
                    description="HTTP status code",
                ),
            ]
            elapsed_time: Annotated[
                t.NonNegativeFloat | None,
                u.Field(
                    description="Response processing time in seconds",
                ),
            ] = None

            @property
            def error(self) -> bool:
                """Check if HTTP status indicates client or server error.

                Returns:
                    True if status_code >= c.ERROR_MIN, False otherwise

                """
                return bool(self.status_code >= c.Web.ERROR_MIN)

            @property
            def success(self) -> bool:
                """Check if HTTP status indicates success (2xx range).

                Returns:
                    True if status code in range(*c.SUCCESS_RANGE), False otherwise

                """
                success_min, success_max = c.Web.SUCCESS_RANGE
                return bool(success_min <= self.status_code <= success_max)

        class AppRequest(m.Value):
            """Web request entity with tracking and context information.

            Extends generic HTTP request with web application-specific fields
            for request tracking, client identification, and analysis.

            Attributes:
                url: Request URL
                method: HTTP method
                timeout: Request timeout
                headers: HTTP headers
                body: Message body
                timestamp: Request timestamp
                request_id: Unique request identifier
                query_params: Query string parameters
                client_ip: Client IP address
                user_agent: Client user agent string

            """

            url: Annotated[
                str,
                u.Field(
                    min_length=1,
                    max_length=c.Web.VALIDATION_URL_LENGTH_RANGE[1],
                    description="Request URL",
                ),
            ]
            method: Annotated[
                c.Web.Method,
                u.BeforeValidator(str.upper),
                u.Field(
                    description="HTTP method (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)",
                ),
            ] = c.Web.Method.GET
            timeout: Annotated[
                t.PositiveTimeout,
                u.Field(
                    description="Request timeout in seconds",
                ),
            ] = c.Web.DEFAULT_TIMEOUT_SECONDS

            headers: Annotated[
                t.MutableStrMapping,
                u.Field(
                    description="HTTP headers",
                ),
            ] = u.Field(default_factory=dict)
            body: Annotated[
                str | t.ScalarMapping | None,
                u.Field(
                    description="Request body content (optional for GET/HEAD)",
                ),
            ] = None
            timestamp: Annotated[
                datetime,
                u.Field(
                    description="Request timestamp",
                ),
            ] = u.Field(default_factory=lambda: datetime.now(UTC))
            request_id: Annotated[
                str,
                u.Field(
                    description="Unique request identifier",
                ),
            ] = u.Field(default_factory=lambda: str(uuid.uuid4()))
            query_params: Annotated[
                t.MutableConfigurationMapping,
                u.Field(
                    description="Query string parameters",
                ),
            ] = u.Field(default_factory=dict)
            client_ip: Annotated[
                str,
                u.Field(description="Client IP address"),
            ] = ""
            user_agent: Annotated[
                str,
                u.Field(description="Client user agent"),
            ] = ""

            @property
            def has_body(self) -> bool:
                """Check if web request has a message body.

                Returns:
                    True if body is not None, False otherwise

                """
                return self.body is not None

            @property
            def secure(self) -> bool:
                """Check if web request uses HTTPS protocol.

                Returns:
                    True if URL starts with 'https://', False otherwise

                """
                return self.url.startswith("https://")

        class AppResponse(m.Value):
            """Web response entity with tracking and performance metrics.

            Extends generic HTTP response with web application-specific fields
            for response tracking, performance monitoring, and client context.

            Attributes:
                status_code: HTTP status code
                headers: HTTP response headers
                body: Response body content
                timestamp: Response timestamp
                elapsed_time: Response processing time
                response_id: Unique response identifier
                request_id: Associated request identifier
                content_type: Response content type
                content_length: Response body length in bytes
                processing_time_ms: Processing time in milliseconds

            """

            status_code: Annotated[
                t.HttpStatusCode,
                u.Field(
                    ...,
                    description="HTTP status code",
                ),
            ]
            headers: Annotated[
                t.MutableStrMapping,
                u.Field(
                    description="HTTP response headers",
                ),
            ] = u.Field(default_factory=dict)
            body: Annotated[
                str | t.ScalarMapping | None,
                u.Field(
                    description="Response body content",
                ),
            ] = None
            timestamp: Annotated[
                datetime,
                u.Field(
                    description="Response timestamp",
                ),
            ] = u.Field(default_factory=lambda: datetime.now(UTC))
            elapsed_time: Annotated[
                t.NonNegativeFloat,
                u.Field(
                    description="Response elapsed time in seconds",
                ),
            ] = 0.0
            response_id: Annotated[
                str,
                u.Field(
                    description="Unique response identifier",
                ),
            ] = u.Field(default_factory=lambda: str(uuid.uuid4()))
            request_id: Annotated[
                str,
                u.Field(description="Associated request identifier"),
            ]
            content_type: Annotated[
                str,
                u.Field(
                    description="Response content type",
                ),
            ] = c.Web.HTTP_CONTENT_TYPE_JSON
            content_length: Annotated[
                t.NonNegativeInt,
                u.Field(
                    description="Response body length in bytes",
                ),
            ] = 0
            processing_time_ms: Annotated[
                t.NonNegativeFloat,
                u.Field(
                    description="Processing time in milliseconds",
                ),
            ] = 0.0

            @property
            def error(self) -> bool:
                """Check if web response status indicates error.

                Returns:
                    True if status_code >= c.ERROR_MIN, False otherwise

                """
                return bool(self.status_code >= c.Web.ERROR_MIN)

            @property
            def success(self) -> bool:
                """Check if web response status indicates success.

                Returns:
                    True if status code in range(*c.SUCCESS_RANGE), False otherwise

                """
                success_min, success_max = c.Web.SUCCESS_RANGE
                return bool(success_min <= self.status_code <= success_max)

            @property
            def processing_time_seconds(self) -> float:
                """Convert processing time from milliseconds to seconds.

                Returns:
                    Processing time in seconds

                """
                return float(self.processing_time_ms / 1000)

        # APPLICATION MODELS (Aggregates - consistency boundaries)

        # EntityStatus removed - use c.Web.Status instead
        # All status values are now centralized in constants.py

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
                    max_length=c.Web.SERVER_MAX_APP_NAME_LENGTH,
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
            # Note: domain_events is inherited from Entry with type Sequence[DomainEvent]
            # Use add_event() method to add events instead of direct list manipulation
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
                # Use u.in_() for unified membership check (DSL pattern)
                return self.status in {running, stopped, error}

            @property
            def can_start(self) -> bool:
                """Check if application can be started."""
                return bool(self.status == c.Web.Status.STOPPED.value)

            @property
            def can_stop(self) -> bool:
                """Check if application can be stopped."""
                return bool(self.status == c.Web.Status.RUNNING.value)

            @property
            def healthy(self) -> bool:
                """Check if application is healthy and operational."""
                running = c.Web.Status.RUNNING.value
                maintenance = c.Web.Status.MAINTENANCE.value
                return self.status in {running, maintenance}

            @property
            def running(self) -> bool:
                """Check if application is currently running."""
                return bool(self.status == c.Web.Status.RUNNING.value)

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
                # Import at module level - flext_u is used for ID formatting
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
                data: m.ConfigMap | Mapping[str, t.JsonPayload | None] | None = None,
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
                    aggregate_id=str(self.id),
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

            def restart(self) -> p.Result[FlextWebModels.Web.Entity]:
                """Restart the application."""
                can_restart_validated = self.can_restart
                if not can_restart_validated:
                    return r[FlextWebModels.Web.Entity].fail(
                        "Cannot restart in current state",
                    )
                starting_status = c.Web.Status.STARTING.value
                running_status = c.Web.Status.RUNNING.value
                self.status = starting_status
                # Add web lifecycle events
                restart_event_result = self.add_web_event("ApplicationRestarting")
                if restart_event_result.failure:  # pragma: no cover
                    return r[FlextWebModels.Web.Entity].fail(
                        f"Failed to add web event: {restart_event_result.error}",
                    )
                self.status = running_status
                start_event_result = self.add_web_event("ApplicationStarted")
                if start_event_result.failure:  # pragma: no cover
                    return r[FlextWebModels.Web.Entity].fail(
                        f"Failed to add web event: {start_event_result.error}",
                    )
                return r[FlextWebModels.Web.Entity].ok(self)

            def start(self) -> p.Result[FlextWebModels.Web.Entity]:
                """Start the application."""
                running_status = c.Web.Status.RUNNING.value
                already_running = self.status == running_status
                if already_running:
                    return r[FlextWebModels.Web.Entity].fail(
                        "already running",
                    )
                self.status = running_status
                # Add web lifecycle event
                event_result = self.add_web_event("ApplicationStarted")
                if event_result.failure:  # pragma: no cover
                    return r[FlextWebModels.Web.Entity].fail(
                        f"Failed to add web event: {event_result.error}",
                    )
                return r[FlextWebModels.Web.Entity].ok(self)

            def stop(self) -> p.Result[FlextWebModels.Web.Entity]:
                """Stop the application."""
                running_status = c.Web.Status.RUNNING.value
                stopped_status = c.Web.Status.STOPPED.value
                not_running = self.status != running_status
                if not_running:
                    return r[FlextWebModels.Web.Entity].fail(
                        "not running",
                    )
                self.status = stopped_status
                # Add web lifecycle event
                event_result = self.add_web_event("ApplicationStopped")
                if event_result.failure:  # pragma: no cover
                    return r[FlextWebModels.Web.Entity].fail(
                        f"Failed to add web event: {event_result.error}",
                    )
                return r[FlextWebModels.Web.Entity].ok(self)

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
                # Add web lifecycle event
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

        class Credentials(m.Value):
            """Authentication credentials model."""

            username: Annotated[str, u.Field(min_length=1, description="Username")]
            password: Annotated[str, u.Field(min_length=1, description="Password")]

        class UserData(m.Value):
            """User registration data model."""

            username: Annotated[str, u.Field(min_length=1, description="Username")]
            email: Annotated[str, u.Field(min_length=1, description="Email address")]
            password: Annotated[
                str,
                u.Field(
                    description="Password (empty string if not provided)",
                ),
            ] = ""

        class AppData(m.Value):
            """Application creation data model."""

            name: Annotated[
                str,
                u.Field(
                    min_length=c.Web.VALIDATION_NAME_LENGTH_RANGE[0],
                    max_length=c.Web.VALIDATION_NAME_LENGTH_RANGE[1],
                    description="Application name",
                ),
            ]
            host: Annotated[
                str,
                u.Field(
                    min_length=1,
                    max_length=c.Web.SECURITY_MAX_HOST_LENGTH,
                    description="Application host",
                ),
            ]
            port: Annotated[
                t.PortNumber,
                u.Field(
                    ...,
                    description="Application port",
                ),
            ]

        class EntityData(m.Value):
            """Generic entity data model."""

            data: Annotated[
                t.MutableConfigurationMapping,
                u.Field(
                    description="Entity data dictionary",
                ),
            ] = u.Field(default_factory=dict)

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
                """Return whether the projected application is running."""
                return bool(self.status == c.Web.Status.RUNNING.value)

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
                int, u.Field(description="Total applications")
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

        class WebRequest(m.Value):
            """Web request model with complete tracking."""

            method: Annotated[
                c.Web.Method,
                u.Field(
                    description="HTTP method",
                ),
            ] = c.Web.Method.GET
            url: Annotated[
                str,
                u.Field(
                    min_length=1,
                    max_length=c.Web.VALIDATION_MAX_URL_LENGTH,
                    description="Request URL",
                ),
            ]
            headers: Annotated[
                t.MutableStrMapping,
                u.Field(
                    description="HTTP headers",
                ),
            ] = u.Field(default_factory=dict)
            body: Annotated[
                str | t.JsonValue | None,
                u.Field(
                    description="Request body (optional for GET/HEAD)",
                ),
            ] = None
            request_id: Annotated[
                str,
                u.Field(
                    description="Unique request identifier",
                ),
            ] = u.Field(default_factory=lambda: str(uuid.uuid4()))
            timestamp: Annotated[
                datetime,
                u.Field(
                    description="Request timestamp",
                ),
            ] = u.Field(default_factory=lambda: datetime.now(UTC))

        class WebResponse(m.Value):
            """Web response model with status tracking."""

            request_id: Annotated[
                str,
                u.Field(description="Associated request identifier"),
            ]
            status_code: Annotated[
                int,
                u.Field(
                    ge=c.Web.StatusCode.CONTINUE.value,
                    le=c.Web.StatusCode.GATEWAY_TIMEOUT.value,
                    description="HTTP status code",
                ),
            ]
            headers: Annotated[
                t.MutableStrMapping,
                u.Field(
                    description="HTTP response headers",
                ),
            ] = u.Field(default_factory=dict)
            body: Annotated[
                str | t.JsonValue | None,
                u.Field(
                    description="Response body (optional for 204 No Content)",
                ),
            ] = None
            response_id: Annotated[
                str,
                u.Field(
                    description="Unique response identifier",
                ),
            ] = u.Field(default_factory=lambda: str(uuid.uuid4()))
            timestamp: Annotated[
                datetime,
                u.Field(
                    description="Response timestamp",
                ),
            ] = u.Field(default_factory=lambda: datetime.now(UTC))

        class AppConfig(m.Value):
            """Application configuration model."""

            title: Annotated[
                str,
                u.Field(
                    min_length=1,
                    max_length=c.Web.SERVER_MAX_APP_NAME_LENGTH,
                    description="Application title",
                ),
            ]
            version: Annotated[str, u.Field(description="Application version")]
            description: Annotated[
                str,
                u.Field(
                    min_length=1,
                    max_length=c.Web.SECURITY_MAX_DESCRIPTION_LENGTH,
                    description="Application description",
                ),
            ]
            docs_url: Annotated[
                str,
                u.Field(
                    description="Documentation URL",
                ),
            ] = c.Web.API_DOCS_URL
            redoc_url: Annotated[
                str,
                u.Field(
                    description="ReDoc URL",
                ),
            ] = c.Web.API_REDOC_URL
            openapi_url: Annotated[
                str,
                u.Field(
                    description="OpenAPI URL",
                ),
            ] = c.Web.API_OPENAPI_URL

        # FACTORY METHODS (Creation patterns)

        @classmethod
        def create_web_app(
            cls,
            name: str,
            host: str = c.Web.DEFAULT_HOST,
            port: int = c.Web.DEFAULT_PORT,
        ) -> p.Result[FlextWebModels.Web.Entity]:
            """Create a web application from direct parameters.

            No dict conversion - use direct parameters for type safety.
            Pydantic validation will handle errors automatically.

            Args:
                name: Application name
                host: Application host
                port: Application port

            Returns:
                r[Web.Entity]: Success contains entity,
                                            failure contains validation error

            """
            entity = cls.Entity(
                id=str(uuid.uuid4()),
                name=name,
                host=host,
                port=port,
                status=c.Web.Status.STOPPED.value,
                environment=c.Web.Name.DEVELOPMENT.value,
                debug_mode=False,
                metrics={},
                web_events=[],
            )
            return r[FlextWebModels.Web.Entity].ok(entity)

        @classmethod
        def create_web_request(
            cls,
            method: c.Web.Method,
            url: str,
            headers: t.StrMapping | None = None,
            body: str | t.JsonValue | None = None,
        ) -> p.Result[WebRequest]:
            """Create a web request model.

            Args:
                method: HTTP method
                url: Request URL
                headers: Request headers (defaults to empty dict)
                body: Request body

            Returns:
                r[WebRequest]: Success contains request model,
                                        failure contains validation error

            """
            headers_validated: t.StrMapping = headers or {}

            # Use u.try_() for unified error handling (DSL pattern)
            def create_request() -> FlextWebModels.Web.WebRequest:
                """Create request model."""
                validated: FlextWebModels.Web.WebRequest = (
                    cls.WebRequest.model_validate({
                        "method": method,
                        "url": url,
                        "headers": dict(headers_validated),
                        "body": body,
                        "request_id": str(uuid.uuid4()),
                        "timestamp": datetime.now(UTC),
                    })
                )
                return validated

            result = u.try_(
                create_request,
                catch=Exception,
            )
            return result.map_error(lambda exc: f"Failed to create web request: {exc}")

        @classmethod
        def create_web_response(
            cls,
            request_id: str,
            status_code: int,
            headers: t.StrMapping | None = None,
            body: str | t.JsonValue | None = None,
        ) -> p.Result[WebResponse]:
            """Create a web response model.

            Args:
                request_id: Associated request identifier
                status_code: HTTP status code
                headers: Response headers (defaults to empty dict)
                body: Response body

            Returns:
                 r[WebResponse]: Success contains response model,
                                          failure contains validation error

            """
            headers_validated: t.StrMapping = headers or {}

            # Use u.try_() for unified error handling (DSL pattern)
            def create_response() -> FlextWebModels.Web.WebResponse:
                """Create response model."""
                validated: FlextWebModels.Web.WebResponse = (
                    cls.WebResponse.model_validate({
                        "request_id": request_id,
                        "status_code": status_code,
                        "headers": dict(headers_validated),
                        "body": body,
                        "response_id": str(uuid.uuid4()),
                        "timestamp": datetime.now(UTC),
                    })
                )
                return validated

            result = u.try_(
                create_response,
                catch=Exception,
            )
            return result.map_error(lambda exc: f"Failed to create web response: {exc}")

        class FastAPIAppConfig(m.BaseModel):
            """FastAPI application configuration model (Value Object).

            Represents FastAPI application configuration in Pydantic format
            for validation and type safety before passing to FastAPI.

            Attributes:
                title: FastAPI application title
                version: Application version
                description: Application description
                debug: Debug mode flag
                testing: Testing mode flag
                middlewares: List of middleware objects to apply
                docs_url: Swagger UI docs URL
                redoc_url: ReDoc URL
                openapi_url: OpenAPI schema URL

            """

            title: Annotated[
                str,
                u.Field(
                    min_length=c.Web.VALIDATION_NAME_LENGTH_RANGE[0],
                    max_length=c.Web.VALIDATION_NAME_LENGTH_RANGE[1],
                    description="FastAPI application title",
                ),
            ] = c.Web.DEFAULT_APP_NAME
            version: Annotated[
                str,
                u.Field(
                    description="Application version",
                ),
            ] = c.Web.DEFAULT_VERSION_STRING
            description: Annotated[
                str,
                u.Field(
                    min_length=1,
                    max_length=c.Web.SECURITY_MAX_DESCRIPTION_LENGTH,
                    description="Application description",
                ),
            ] = c.Web.API_DEFAULT_DESCRIPTION
            debug: Annotated[
                bool,
                u.Field(description="FastAPI debug mode"),
            ] = False
            testing: Annotated[
                bool,
                u.Field(description="FastAPI testing mode"),
            ] = False
            middlewares: Annotated[
                t.StrSequence,
                u.Field(
                    description="List of middleware objects",
                ),
            ] = u.Field(default_factory=list)
            docs_url: Annotated[
                str,
                u.Field(
                    description="Documentation URL",
                ),
            ] = c.Web.API_DOCS_URL
            redoc_url: Annotated[
                str,
                u.Field(
                    description="ReDoc URL",
                ),
            ] = c.Web.API_REDOC_URL
            openapi_url: Annotated[
                str,
                u.Field(
                    description="OpenAPI URL",
                ),
            ] = c.Web.API_OPENAPI_URL

        class SystemInfo(m.BaseModel):
            """System information response model."""

            service_name: Annotated[str, u.Field(description="Service name")]
            service_type: Annotated[str, u.Field(description="Service type")]
            architecture: Annotated[str, u.Field(description="Architecture pattern")]
            patterns: Annotated[
                t.StrSequence,
                u.Field(description="Design patterns used"),
            ]
            integrations: Annotated[
                t.StrSequence,
                u.Field(description="Integrated components"),
            ]
            capabilities: Annotated[
                t.StrSequence,
                u.Field(description="Service capabilities"),
            ]

        class HealthStatus(m.BaseModel):
            """Health status response model."""

            status: Annotated[str, u.Field(description="Health status")]
            service: Annotated[str, u.Field(description="Service name")]
            version: Annotated[str, u.Field(description="Service version")]
            timestamp: Annotated[str, u.Field(description="Status timestamp")]
            components: Annotated[
                t.StrMapping, u.Field(description="Component statuses")
            ]

        class AppRuntimeInfo(m.ArbitraryTypesModel):
            """Runtime information for a running web application.

            Tracks the server instance, daemon thread, and runner type
            for each started application so it can be stopped cleanly.
            """

            model_config: ClassVar[m.ConfigDict] = m.ConfigDict(
                arbitrary_types_allowed=True,
                frozen=True,
                extra="forbid",
            )
            runner: Annotated[
                str,
                u.Field(description="Runtime runner name (uvicorn, werkzeug)"),
            ]
            server: Annotated[
                uvicorn.Server | WSGIServer,
                u.Field(description="Server instance for lifecycle management"),
            ]
            thread: Annotated[
                Thread,
                u.Field(description="Daemon thread running the server"),
            ]


m = FlextWebModels

__all__: list[str] = ["FlextWebModels", "m"]
