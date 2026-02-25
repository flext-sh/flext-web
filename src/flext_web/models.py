"""FLEXT Web models for web applications.

Provides Pydantic models for web-based applications with validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import uuid
from collections.abc import Mapping
from datetime import UTC, datetime

from flext_core import (
    FlextModels,
    r,
    t,
    u,
)
from pydantic import BaseModel, Field, ValidationError, field_validator

from .constants import c


class FlextWebModels(FlextModels):
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

        class Message(FlextModels.Value):
            """Generic HTTP message base model with protocol validation.

            Represents common HTTP message structure with headers, body,
            and timestamp. Used as base for Request and Response models.

            Attributes:
                headers: HTTP headers dictionary mapping header names to values
                body: Message body as string, dict, or None for no body
                timestamp: UTC timestamp when message was created

            """

            headers: dict[str, str] = Field(
                default_factory=dict,
                description="HTTP headers for message",
            )
            body: str | dict[str, t.ConfigMapValue] | None = Field(
                default=None,
                description="Message body content (optional for GET/HEAD)",
            )
            timestamp: datetime = Field(
                default_factory=lambda: datetime.now(UTC),
                description="UTC timestamp of message creation",
            )

        class Request(Message):
            """HTTP request model with complete validation.

            Represents a complete HTTP request following HTTP specifications
            with full validation of URL, method, and timeout parameters.

            Attributes:
            url: Request URL with length validation
            method: HTTP method (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
            timeout: Request timeout in seconds (0-300)

            """

            url: str = Field(
                min_length=1,
                max_length=c.Web.WebValidation.URL_LENGTH_RANGE[1],
                description="Request URL",
            )
            method: c.Web.Literals.HttpMethodLiteral = Field(
                default="GET",
                description="HTTP method",
            )
            timeout: float = Field(
                default=c.Web.Http.DEFAULT_TIMEOUT_SECONDS,
                ge=0.0,
                le=c.Web.WebValidation.REQUEST_TIMEOUT_MAX,
                description="Request timeout in seconds",
            )

            @property
            def has_body(self) -> bool:
                """Check if HTTP request has a message body.

                Returns:
                True if body is not None, False otherwise

                """
                return self.body is not None

            @property
            def is_secure(self) -> bool:
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

            status_code: int = Field(
                ge=c.Web.StatusCode.CONTINUE.value,
                le=c.Web.StatusCode.GATEWAY_TIMEOUT.value,
                description="HTTP status code",
            )
            elapsed_time: float | None = Field(
                default=None,
                ge=0.0,
                description="Response processing time in seconds",
            )

            @property
            def is_success(self) -> bool:
                """Check if HTTP status indicates success (2xx range).

                Returns:
                    True if status code in range(*c.SUCCESS_RANGE), False otherwise

                """
                success_min, success_max = c.Web.SUCCESS_RANGE
                return success_min <= self.status_code <= success_max

            @property
            def is_error(self) -> bool:
                """Check if HTTP status indicates client or server error.

                Returns:
                    True if status_code >= c.ERROR_MIN, False otherwise

                """
                return self.status_code >= c.Web.ERROR_MIN

        class AppRequest(FlextModels.Value):
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

            url: str = Field(
                min_length=1,
                max_length=c.Web.WebValidation.URL_LENGTH_RANGE[1],
                description="Request URL",
            )
            method: c.Web.Literals.HttpMethodLiteral = Field(
                default="GET",
                description="HTTP method",
            )
            timeout: float = Field(
                default=c.Web.Http.DEFAULT_TIMEOUT_SECONDS,
                ge=0.0,
                le=c.Web.WebValidation.REQUEST_TIMEOUT_MAX,
                description="Request timeout in seconds",
            )

            headers: dict[str, str] = Field(
                default_factory=dict,
                description="HTTP headers",
            )
            body: str | dict[str, t.ConfigMapValue] | None = Field(
                default=None,
                description="Request body content (optional for GET/HEAD)",
            )
            timestamp: datetime = Field(
                default_factory=lambda: datetime.now(UTC),
                description="Request timestamp",
            )
            request_id: str = Field(
                default_factory=lambda: str(uuid.uuid4()),
                description="Unique request identifier",
            )
            query_params: dict[str, t.ConfigMapValue] = Field(
                default_factory=dict,
                description="Query string parameters",
            )
            client_ip: str = Field(default="", description="Client IP address")
            user_agent: str = Field(default="", description="Client user agent")

            @property
            def has_body(self) -> bool:
                """Check if web request has a message body.

                Returns:
                    True if body is not None, False otherwise

                """
                return self.body is not None

            @property
            def is_secure(self) -> bool:
                """Check if web request uses HTTPS protocol.

                Returns:
                    True if URL starts with 'https://', False otherwise

                """
                return self.url.startswith("https://")

        class AppResponse(FlextModels.Value):
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

            status_code: int = Field(
                ge=c.Web.StatusCode.CONTINUE.value,
                le=c.Web.StatusCode.GATEWAY_TIMEOUT.value,
                description="HTTP status code",
            )
            headers: dict[str, str] = Field(
                default_factory=dict,
                description="HTTP response headers",
            )
            body: str | dict[str, t.ConfigMapValue] | None = Field(
                default=None,
                description="Response body content",
            )
            timestamp: datetime = Field(
                default_factory=lambda: datetime.now(UTC),
                description="Response timestamp",
            )
            elapsed_time: float = Field(
                default=0.0,
                ge=0.0,
                description="Response elapsed time in seconds",
            )
            response_id: str = Field(
                default_factory=lambda: str(uuid.uuid4()),
                description="Unique response identifier",
            )
            request_id: str = Field(description="Associated request identifier")
            content_type: c.Web.Literals.ContentTypeLiteral | str = Field(
                default=c.Web.Http.CONTENT_TYPE_JSON,
                description="Response content type",
            )
            content_length: int = Field(
                default=0,
                ge=0,
                description="Response body length in bytes",
            )
            processing_time_ms: float = Field(
                default=0.0,
                ge=0.0,
                description="Processing time in milliseconds",
            )

            @property
            def is_success(self) -> bool:
                """Check if web response status indicates success.

                Returns:
                    True if status code in range(*c.SUCCESS_RANGE), False otherwise

                """
                success_min, success_max = c.Web.SUCCESS_RANGE
                return success_min <= self.status_code <= success_max

            @property
            def is_error(self) -> bool:
                """Check if web response status indicates error.

                Returns:
                    True if status_code >= c.ERROR_MIN, False otherwise

                """
                return self.status_code >= c.Web.ERROR_MIN

            @property
            def processing_time_seconds(self) -> float:
                """Convert processing time from milliseconds to seconds.

                Returns:
                    Processing time in seconds

                """
                return self.processing_time_ms / 1000  # Convert ms to seconds

        # APPLICATION MODELS (Aggregates - consistency boundaries)

        # EntityStatus removed - use c.Web.Status instead
        # All status values are now centralized in constants.py

        class Entity(FlextModels.Entity):
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

            id: str = Field(
                default_factory=lambda: str(uuid.uuid4()),
                description="Unique application identifier",
            )
            name: str = Field(
                min_length=1,
                max_length=c.Web.WebServer.MAX_APP_NAME_LENGTH,
                description="Application name",
            )

            @field_validator("name", mode="before")
            @classmethod
            def validate_name(cls, v: str) -> str:
                """Validate application name using u.guard() DSL pattern."""
                min_length = c.Web.WebValidation.NAME_LENGTH_RANGE[0]
                max_length = c.Web.WebValidation.NAME_LENGTH_RANGE[1]
                reserved_names_set = set(c.Web.WebSecurity.RESERVED_NAMES)

                # Validate name length using lambda-based guard
                # Type narrowing: v is str from pydantic validation, use explicit str check
                name_length_validated = u.guard(
                    v,
                    lambda s: min_length <= len(s) <= max_length,
                    return_value=True,
                )
                if name_length_validated is None:
                    error_msg = (
                        f"Name must be between {min_length} and {max_length} characters"
                    )
                    raise ValueError(error_msg)

                # Use u.guard() + u.in_() for unified membership validation (DSL pattern)
                name_not_reserved = u.guard(
                    v.lower(),
                    lambda n: n not in reserved_names_set,
                    return_value=True,
                )
                if name_not_reserved is None:
                    error_msg = f"Name '{v}' is reserved and cannot be used"
                    raise ValueError(error_msg)

                # Use u.find() for unified pattern validation (DSL pattern)
                dangerous_patterns = c.Web.WebSecurity.DANGEROUS_PATTERNS
                dangerous_found = u.find(
                    dangerous_patterns,
                    lambda value: value.lower() in v.lower(),
                )
                if dangerous_found:
                    error_msg = f"Name contains dangerous pattern: {dangerous_found}"
                    raise ValueError(error_msg)

                return v

            host: str = Field(
                default=c.Web.WebDefaults.HOST,
                min_length=1,
                max_length=c.Web.WebSecurity.MAX_HOST_LENGTH,
                description="Application host address",
            )
            port: int = Field(
                default=c.Web.WebDefaults.PORT,
                ge=c.Web.WebValidation.PORT_RANGE[0],
                le=c.Web.WebValidation.PORT_RANGE[1],
                description="Application port number",
            )
            status: c.Web.Literals.ApplicationStatusLiteral = Field(
                default=c.Web.Status.STOPPED.value,
                description="Current application status",
            )

            environment: str = Field(
                default=c.Web.Name.DEVELOPMENT.value,
                description="Deployment environment",
            )
            debug_mode: bool = Field(
                default=c.Web.WebDefaults.DEBUG_MODE,
                description="Debug mode enabled flag",
            )
            version: int = Field(
                default=c.Web.WebDefaults.VERSION_INT,
                description="Application version",
            )
            metrics: dict[str, t.ConfigMapValue] = Field(
                default_factory=dict,
                description="Application metrics",
            )
            # Note: domain_events is inherited from Entry with type list[DomainEvent]
            # Use add_event() method to add events instead of direct list manipulation
            web_events: list[str] = Field(
                default_factory=list,
                description="Web-specific events (application lifecycle)",
            )

            @property
            def is_running(self) -> bool:
                """Check if application is currently running."""
                return self.status == c.Web.Status.RUNNING.value

            @property
            def is_healthy(self) -> bool:
                """Check if application is healthy and operational."""
                running = c.Web.Status.RUNNING.value
                maintenance = c.Web.Status.MAINTENANCE.value
                return self.status in {running, maintenance}

            @property
            def can_start(self) -> bool:
                """Check if application can be started."""
                return self.status == c.Web.Status.STOPPED.value

            @property
            def can_stop(self) -> bool:
                """Check if application can be stopped."""
                return self.status == c.Web.Status.RUNNING.value

            @property
            def can_restart(self) -> bool:
                """Check if application can be restarted using u.in_() DSL pattern."""
                running = c.Web.Status.RUNNING.value
                stopped = c.Web.Status.STOPPED.value
                error = c.Web.Status.ERROR.value
                # Use u.in_() for unified membership check (DSL pattern)
                return self.status in {running, stopped, error}

            @property
            def url(self) -> str:
                """Get the full URL with conditional protocol selection."""
                ssl_ports = c.Web.WebSecurity.SSL_PORTS
                protocol = (
                    c.Web.WebDefaults.HTTPS_PROTOCOL
                    if u.in_(self.port, ssl_ports)
                    else c.Web.WebDefaults.HTTP_PROTOCOL
                )
                return f"{protocol}://{self.host}:{self.port}"

            def validate_business_rules(self) -> r[bool]:
                """Validate application business rules (Aggregate validation).

                Fast-fail validation - no fallbacks, explicit checks only.

                Returns:
                    r[bool]: Success contains True if valid, failure with error message

                """
                # Validate name minimum length using lambda-based guard
                min_name_length = c.Web.WebValidation.NAME_LENGTH_RANGE[0]
                name_validated = u.guard(
                    self.name,
                    lambda s: len(s) >= min_name_length,
                    return_value=True,
                )
                if name_validated is None:
                    return r[bool].fail(
                        f"App name must be at least {min_name_length} characters",
                    )

                # Use u.guard() for unified port range validation (DSL pattern)
                min_port = c.Web.WebValidation.PORT_RANGE[0]
                max_port = c.Web.WebValidation.PORT_RANGE[1]
                # Use u.guard() with combined check for unified error message (DSL pattern)
                port_validated = u.guard(
                    self.port,
                    lambda p: min_port <= p <= max_port,
                    return_value=True,
                )
                if port_validated is None:
                    return r[bool].fail(
                        f"Port must be between {min_port} and {max_port}",
                    )
                return r[bool].ok(value=True)

            def start(self) -> r[FlextWebModels.Web.Entity]:
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
                if event_result.is_failure:  # pragma: no cover
                    return r[FlextWebModels.Web.Entity].fail(
                        f"Failed to add web event: {event_result.error}",
                    )
                return r[FlextWebModels.Web.Entity].ok(self)

            def stop(self) -> r[FlextWebModels.Web.Entity]:
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
                if event_result.is_failure:  # pragma: no cover
                    return r[FlextWebModels.Web.Entity].fail(
                        f"Failed to add web event: {event_result.error}",
                    )
                return r[FlextWebModels.Web.Entity].ok(self)

            def restart(self) -> r[FlextWebModels.Web.Entity]:
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
                if restart_event_result.is_failure:  # pragma: no cover
                    return r[FlextWebModels.Web.Entity].fail(
                        f"Failed to add web event: {restart_event_result.error}",
                    )
                self.status = running_status
                start_event_result = self.add_web_event("ApplicationStarted")
                if start_event_result.is_failure:  # pragma: no cover
                    return r[FlextWebModels.Web.Entity].fail(
                        f"Failed to add web event: {start_event_result.error}",
                    )
                return r[FlextWebModels.Web.Entity].ok(self)

            def update_metrics(
                self,
                new_metrics: Mapping[str, t.ConfigMapValue],
            ) -> r[bool]:
                """Update application metrics.

                Returns:
                    r[bool]: Success contains True if metrics updated,
                                    failure contains error message

                """
                # Validate and update metrics
                self.metrics.update(new_metrics)
                # Add web lifecycle event
                event_result = self.add_web_event("MetricsUpdated")
                if event_result.is_failure:  # pragma: no cover
                    return r[bool].fail(
                        f"Failed to add web event: {event_result.error}"
                    )
                return r[bool].ok(value=True)

            def get_health_status(self) -> Mapping[str, t.ConfigMapValue]:
                """Get comprehensive health status."""
                return {
                    "status": self.status,
                    "is_running": self.is_running,
                    "is_healthy": self.is_healthy,
                    "url": self.url,
                    "version": self.version,
                    "environment": self.environment,
                }

            def __str__(self) -> str:
                """Return string representation of the application."""
                return f"{self.name} ({self.url}) - {self.status}"

            def add_web_event(
                self,
                event_name: str,
            ) -> r[bool]:
                """Add web-specific event (not domain event).

                This is for web application lifecycle events, not DDD domain events.
                Use parent's add_domain_event() for actual domain events.

                Returns:
                    r[bool]: Success contains True if event added,
                                    failure contains error message

                """
                # Validate event name is non-empty string
                if not event_name.strip():
                    return r[bool].fail("Event name cannot be empty")
                self.web_events.append(event_name)
                return r[bool].ok(value=True)

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
                # Import at module level - u is used for ID formatting
                return u.format_app_id(name)

        class EntityConfig(FlextModels.Value):
            """Application entity configuration (Value Object).

            Represents configuration settings for application entities.
            Uses Constants for defaults - Config has priority when provided.
            """

            app_name: str = Field(
                default=c.Web.WebDefaults.APP_NAME,
                min_length=c.Web.WebValidation.NAME_LENGTH_RANGE[0],
                max_length=c.Web.WebValidation.NAME_LENGTH_RANGE[1],
                description="Application name",
            )
            host: str = Field(
                default=c.Web.WebDefaults.HOST,
                min_length=1,
                max_length=c.Web.WebSecurity.MAX_HOST_LENGTH,
                description="Application host address",
            )
            port: int = Field(
                default=c.Web.WebDefaults.PORT,
                ge=c.Web.WebValidation.PORT_RANGE[0],
                le=c.Web.WebValidation.PORT_RANGE[1],
                description="Application port number",
            )
            debug: bool = Field(
                default=c.Web.WebDefaults.DEBUG_MODE,
                description="Debug mode flag",
            )
            secret_key: str = Field(
                default=c.Web.WebDefaults.SECRET_KEY,
                min_length=c.Web.WebSecurity.MIN_SECRET_KEY_LENGTH,
                description="Application secret key",
            )

        class Credentials(FlextModels.Value):
            """Authentication credentials model."""

            username: str = Field(min_length=1, description="Username")
            password: str = Field(min_length=1, description="Password")

        class UserData(FlextModels.Value):
            """User registration data model."""

            username: str = Field(min_length=1, description="Username")
            email: str = Field(min_length=1, description="Email address")
            password: str = Field(
                default="",
                description="Password (empty string if not provided)",
            )

        class AppData(FlextModels.Value):
            """Application creation data model."""

            name: str = Field(
                min_length=c.Web.WebValidation.NAME_LENGTH_RANGE[0],
                max_length=c.Web.WebValidation.NAME_LENGTH_RANGE[1],
                description="Application name",
            )
            host: str = Field(
                min_length=1,
                max_length=c.Web.WebSecurity.MAX_HOST_LENGTH,
                description="Application host",
            )
            port: int = Field(
                ge=c.Web.WebValidation.PORT_RANGE[0],
                le=c.Web.WebValidation.PORT_RANGE[1],
                description="Application port",
            )

        class EntityData(FlextModels.Value):
            """Generic entity data model."""

            data: dict[str, t.ConfigMapValue] = Field(
                default_factory=dict,
                description="Entity data dictionary",
            )

        class AuthResponse(FlextModels.Value):
            """Authentication response model."""

            token: str = Field(description="Authentication token")
            user_id: str = Field(description="User identifier")
            authenticated: bool = Field(description="Authentication status")

        class UserResponse(FlextModels.Value):
            """User registration response model."""

            id: str = Field(description="User identifier")
            username: str = Field(description="Username")
            email: str = Field(description="Email address")
            created: bool = Field(description="Creation status")

        class ApplicationResponse(FlextModels.Value):
            """Application management response model."""

            id: str = Field(description="Application identifier")
            name: str = Field(description="Application name")
            host: str = Field(description="Application host")
            port: int = Field(description="Application port")
            status: str = Field(description="Application status")
            created_at: str = Field(description="Creation timestamp")

        class HealthResponse(FlextModels.Value):
            """Health check response model."""

            status: str = Field(description="Health status")
            service: str = Field(description="Service name")
            timestamp: str = Field(description="Timestamp")

        class MetricsResponse(FlextModels.Value):
            """Metrics response model."""

            service_status: str = Field(description="Service status")
            components: list[str] = Field(description="Service components")

        class DashboardResponse(FlextModels.Value):
            """Dashboard response model."""

            total_applications: int = Field(description="Total applications")
            running_applications: int = Field(description="Running applications")
            service_status: str = Field(description="Service status")
            routes_initialized: bool = Field(description="Routes initialization status")
            middleware_configured: bool = Field(
                description="Middleware configuration status",
            )
            timestamp: str = Field(description="Timestamp")

        class ServiceResponse(FlextModels.Value):
            """Generic service response model."""

            service: str = Field(description="Service name")
            capabilities: list[str] = Field(description="Service capabilities")
            status: str = Field(description="Service status")
            config: bool = Field(description="Configuration status")

        class WebRequest(FlextModels.Value):
            """Web request model with complete tracking."""

            method: c.Web.Literals.HttpMethodLiteral = Field(
                default="GET",  # Default HTTP method
                description="HTTP method",
            )
            url: str = Field(
                min_length=1,
                max_length=c.Web.WebValidation.MAX_URL_LENGTH,
                description="Request URL",
            )
            headers: dict[str, str] = Field(
                default_factory=dict,
                description="HTTP headers",
            )
            body: str | dict[str, t.ConfigMapValue] | None = Field(
                default=None,
                description="Request body (optional for GET/HEAD)",
            )
            request_id: str = Field(
                default_factory=lambda: str(uuid.uuid4()),
                description="Unique request identifier",
            )
            timestamp: datetime = Field(
                default_factory=lambda: datetime.now(UTC),
                description="Request timestamp",
            )

        class WebResponse(FlextModels.Value):
            """Web response model with status tracking."""

            request_id: str = Field(description="Associated request identifier")
            status_code: int = Field(
                ge=c.Web.StatusCode.CONTINUE.value,
                le=c.Web.StatusCode.GATEWAY_TIMEOUT.value,
                description="HTTP status code",
            )
            headers: dict[str, str] = Field(
                default_factory=dict,
                description="HTTP response headers",
            )
            body: str | dict[str, t.ConfigMapValue] | None = Field(
                default=None,
                description="Response body (optional for 204 No Content)",
            )
            response_id: str = Field(
                default_factory=lambda: str(uuid.uuid4()),
                description="Unique response identifier",
            )
            timestamp: datetime = Field(
                default_factory=lambda: datetime.now(UTC),
                description="Response timestamp",
            )

        class AppConfig(FlextModels.Value):
            """Application configuration model."""

            title: str = Field(
                min_length=1,
                max_length=c.Web.WebServer.MAX_APP_NAME_LENGTH,
                description="Application title",
            )
            version: str = Field(description="Application version")
            description: str = Field(
                min_length=1,
                max_length=c.Web.WebSecurity.MAX_DESCRIPTION_LENGTH,
                description="Application description",
            )
            docs_url: str = Field(
                default=c.Web.WebApi.DOCS_URL,
                description="Documentation URL",
            )
            redoc_url: str = Field(
                default=c.Web.WebApi.REDOC_URL,
                description="ReDoc URL",
            )
            openapi_url: str = Field(
                default=c.Web.WebApi.OPENAPI_URL,
                description="OpenAPI URL",
            )

        # FACTORY METHODS (Creation patterns)

        @classmethod
        def create_web_app(
            cls,
            name: str,
            host: str = c.Web.WebDefaults.HOST,
            port: int = c.Web.WebDefaults.PORT,
        ) -> r[FlextWebModels.Web.Entity]:
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
            try:
                entity = cls.Entity(
                    name=name,
                    host=host,
                    port=port,
                )
                return r.ok(entity)
            except ValidationError as e:  # pragma: no cover
                error_msg = (  # pragma: no cover
                    f"Validation failed: {e.errors()[0]['msg']}"
                    if e.errors()
                    else str(e)  # pragma: no cover
                )
                return r.fail(error_msg)  # pragma: no cover
            except ValueError as e:  # pragma: no cover
                return r.fail(str(e))  # pragma: no cover

        @classmethod
        def create_web_request(
            cls,
            method: c.Web.Literals.HttpMethodLiteral,
            url: str,
            headers: dict[str, str] | None = None,
            body: str | dict[str, t.ConfigMapValue] | None = None,
        ) -> r[WebRequest]:
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
            headers_validated = headers or {}

            # Use u.try_() for unified error handling (DSL pattern)
            def create_request() -> FlextWebModels.Web.WebRequest:
                """Create request model."""
                return cls.WebRequest(
                    method=method,
                    url=url,
                    headers=headers_validated,
                    body=body,
                )

            # Use u.try_() with custom exception handling for better error messages
            try:
                request = create_request()
                return r[FlextWebModels.Web.WebRequest].ok(request)
            except Exception as exc:
                # Use u.err() pattern for unified error extraction (DSL pattern)
                return r[FlextWebModels.Web.WebRequest].fail(
                    f"Failed to create web request: {exc}",
                )

        @classmethod
        def create_web_response(
            cls,
            request_id: str,
            status_code: int,
            headers: dict[str, str] | None = None,
            body: str | dict[str, t.ConfigMapValue] | None = None,
        ) -> r[WebResponse]:
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
            headers_validated = headers or {}

            # Use u.try_() for unified error handling (DSL pattern)
            def create_response() -> FlextWebModels.Web.WebResponse:
                """Create response model."""
                return cls.WebResponse(
                    request_id=request_id,
                    status_code=status_code,
                    headers=headers_validated,
                    body=body,
                )

            # Use u.try_() with custom exception handling for better error messages
            try:
                response = create_response()
                return r[FlextWebModels.Web.WebResponse].ok(response)
            except Exception as exc:
                # Use u.err() pattern for unified error extraction (DSL pattern)
                return r[FlextWebModels.Web.WebResponse].fail(
                    f"Failed to create web response: {exc}",
                )

        class FastAPIAppConfig(BaseModel):
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

            title: str = Field(
                default=c.Web.WebDefaults.APP_NAME,
                min_length=c.Web.WebValidation.NAME_LENGTH_RANGE[0],
                max_length=c.Web.WebValidation.NAME_LENGTH_RANGE[1],
                description="FastAPI application title",
            )
            version: str = Field(
                default=c.Web.WebDefaults.VERSION_STRING,
                description="Application version",
            )
            description: str = Field(
                default=c.Web.WebApi.DEFAULT_DESCRIPTION,
                min_length=1,
                max_length=c.Web.WebSecurity.MAX_DESCRIPTION_LENGTH,
                description="Application description",
            )
            debug: bool = Field(default=False, description="FastAPI debug mode")
            testing: bool = Field(default=False, description="FastAPI testing mode")
            middlewares: list[t.ConfigMapValue] = Field(
                default_factory=list,
                description="List of middleware objects",
            )
            docs_url: str = Field(
                default=c.Web.WebApi.DOCS_URL,
                description="Documentation URL",
            )
            redoc_url: str = Field(
                default=c.Web.WebApi.REDOC_URL,
                description="ReDoc URL",
            )
            openapi_url: str = Field(
                default=c.Web.WebApi.OPENAPI_URL,
                description="OpenAPI URL",
            )


m = FlextWebModels

__all__ = ["FlextWebModels", "m"]
