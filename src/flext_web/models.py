"""FLEXT Web Models - Domain-Driven Design models for web applications (Layer 2: Domain).

This module provides complete domain-driven design models for web-based applications
following flext-core patterns and Pydantic v2 standards. All models implement proper
entity/value object distinction and include complete validation.

Architecture Layer: Layer 2 (Domain)
- Entities: Models with identity (WebApplication, HttpRequest, etc.)
- Value Objects: Immutable models without identity
- Commands: Request objects for operations
- Queries: Request objects for data retrieval

Pydantic Features Used:
- Model validation with Field constraints
- Computed fields for derived properties
- Validators for business rule enforcement
- Alias support for alternative field names
- Model serialization with custom strategies

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

# EventDataMapping imported via flext_core.typings.t
from pydantic import BaseModel, Field, ValidationError, field_validator

from flext import FlextUtilities as flext_u, m as m_core, r
from flext_web.constants import c

# c.Web.HttpMethodLiteral is accessed via c.Web.c.Web.HttpMethodLiteral


class FlextWebModels(m_core):
    """Domain-driven design model collection for web applications (Layer 2: Domain).

    Organizes web models using flext-core DDD patterns:
    - Entities: Models with identity and lifecycle
    - Value Objects: Immutable models without identity
    - Commands: Request objects triggering operations
    - Queries: Request objects for data retrieval

    All models use Pydantic v2 with complete validation and follow
    SOLID principles for maintainability and type safety.

    Example:
        >>> # Create HTTP message value objects
        >>> request = FlextWebModels.Web.Request(
        ...     url="https://example.com/api", method="POST", body={"key": "value"}
        ... )
        >>> # Check request properties
        >>> assert request.is_secure

    """

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Warn when FlextWebModels is subclassed directly."""
        super().__init_subclass__(**kwargs)
        flext_u.Deprecation.warn_once(
            f"subclass:{cls.__name__}",
            "Subclassing FlextWebModels is deprecated. Use FlextModels directly with composition instead.",
        )

    class Web:
        """Web application models for HTTP protocol and application entities.

        Contains HTTP message models, application entities, and web-specific
        domain objects used throughout the FLEXT web ecosystem.

        Models are immutable value objects (frozen=True) following domain-driven
        design principles with Pydantic v2 validation.
        """

        # =========================================================================
        # HTTP PROTOCOL MODELS (Value Objects - immutable)
        # =========================================================================

        class Message(m_core.Value):
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
            body: str | dict[str, object] | None = Field(
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
            method: c.Web.HttpMethodLiteral = Field(
                default=c.Web.Http.Method.GET,  # Use StrEnum value
                description="HTTP method",
            )
            timeout: float = Field(
                default=c.Web.Http.DEFAULT_TIMEOUT_SECONDS,
                ge=0.0,
                le=300.0,
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

            status_code: int = Field(ge=100, le=599, description="HTTP status code")
            elapsed_time: float | None = Field(
                default=None,
                ge=0.0,
                description="Response processing time in seconds",
            )

            @property
            def is_success(self) -> bool:
                """Check if HTTP status indicates success (2xx range).

                Returns:
                    True if status code is 200-299, False otherwise

                """
                success_min, success_max = c.Web.Http.SUCCESS_RANGE
                return success_min <= self.status_code <= success_max

            @property
            def is_error(self) -> bool:
                """Check if HTTP status indicates client or server error.

                Returns:
                    True if status code >= 400, False otherwise

                """
                return self.status_code >= c.Web.Http.ERROR_MIN

        # =========================================================================
        # WEB APPLICATION MODELS (Entities - with identity)
        # =========================================================================

        class AppRequest(m_core.Value):
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
            method: c.Web.HttpMethodLiteral = Field(
                default=c.Web.Http.Method.GET,  # Use StrEnum value
                description="HTTP method",
            )
            timeout: float = Field(
                default=c.Web.Http.DEFAULT_TIMEOUT_SECONDS,
                ge=0.0,
                le=300.0,
                description="Request timeout in seconds",
            )
            headers: dict[str, str] = Field(
                default_factory=dict,
                description="HTTP headers",
            )
            body: str | dict[str, object] | None = Field(
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
            query_params: dict[str, object] = Field(
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

        class AppResponse(m_core.Value):
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

            status_code: int = Field(ge=100, le=599, description="HTTP status code")
            headers: dict[str, str] = Field(
                default_factory=dict,
                description="HTTP response headers",
            )
            body: str | dict[str, object] | None = Field(
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
            content_type: c.Web.ContentTypeLiteral | str = Field(
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
                    True if status code is 200-299, False otherwise

                """
                success_min, success_max = c.Web.Http.SUCCESS_RANGE
                return success_min <= self.status_code <= success_max

            @property
            def is_error(self) -> bool:
                """Check if web response status indicates error.

                Returns:
                    True if status code >= 400, False otherwise

                """
                return self.status_code >= c.Web.Http.ERROR_MIN

            @property
            def processing_time_seconds(self) -> float:
                """Convert processing time from milliseconds to seconds.

                Returns:
                    Processing time in seconds

                """
                return self.processing_time_ms / 1000.0

        # =========================================================================
        # APPLICATION MODELS (Aggregates - consistency boundaries)
        # =========================================================================

        # EntityStatus removed - use c.Web.WebEnvironment.Status instead
        # All status values are now centralized in constants.py

        class Entity(m_core.Entity):
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
                max_length=100,
                description="Application name",
            )

            @field_validator("name")
            @classmethod
            def validate_name(cls, v: str) -> str:
                """Validate application name using u.guard() DSL pattern."""
                min_length = c.Web.WebValidation.NAME_LENGTH_RANGE[0]
                max_length = c.Web.WebValidation.NAME_LENGTH_RANGE[1]
                reserved_names_set = set(c.Web.WebSecurity.RESERVED_NAMES)

                # Use flext_u.guard() + flext_u.V.string.length() for unified length validation (DSL pattern)
                name_length_validated = flext_u.guard(
                    v,
                    flext_u.V.string.length(min_length, max_length),
                    error_message=f"Name must be between {min_length} and {max_length} characters",
                    return_value=True,
                )
                if name_length_validated is None:
                    error_msg = (
                        f"Name must be between {min_length} and {max_length} characters"
                    )
                    raise ValueError(error_msg)

                # Use flext_u.guard() + flext_u.in_() for unified membership validation (DSL pattern)
                name_not_reserved = flext_u.guard(
                    v.lower(),
                    lambda n: not flext_u.in_(n, reserved_names_set),
                    error_message=f"Name '{v}' is reserved and cannot be used",
                    return_value=True,
                )
                if name_not_reserved is None:
                    error_msg = f"Name '{v}' is reserved and cannot be used"
                    raise ValueError(error_msg)

                # Use flext_u.find() for unified pattern validation (DSL pattern)
                dangerous_patterns = c.Web.WebSecurity.DANGEROUS_PATTERNS
                dangerous_found = flext_u.find(
                    dangerous_patterns,
                    lambda p: p.lower() in v.lower(),
                )
                if dangerous_found:
                    error_msg = f"Name contains dangerous pattern: {dangerous_found}"
                    raise ValueError(error_msg)

                return v

            host: str = Field(
                default=c.Web.WebDefaults.HOST,
                min_length=1,
                max_length=255,
                description="Application host address",
            )
            port: int = Field(
                default=c.Web.WebDefaults.PORT,
                ge=c.Web.WebValidation.PORT_RANGE[0],
                le=c.Web.WebValidation.PORT_RANGE[1],
                description="Application port number",
            )
            status: c.Web.ApplicationStatusLiteral | str = Field(
                default=c.Web.WebEnvironment.Status.STOPPED.value,
                description="Current application status",
            )

            @field_validator("status")
            @classmethod
            def validate_status(cls, v: str) -> str:
                """Validate application status against allowed values from constants."""
                valid_statuses = set(c.Web.WebEnvironment.STATUSES)
                if v not in valid_statuses:
                    msg = f"Invalid status '{v}'. Must be one of: {sorted(valid_statuses)}"
                    raise ValueError(msg)
                return v

            environment: str = Field(
                default=c.Web.WebEnvironment.Name.DEVELOPMENT.value,
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
            metrics: dict[str, object] = Field(
                default_factory=dict,
                description="Application metrics",
            )
            domain_events: list[str] = Field(
                default_factory=list,
                description="Domain events for event sourcing",
            )

            @property
            def is_running(self) -> bool:
                """Check if application is currently running."""
                return self.status == c.Web.WebEnvironment.Status.RUNNING.value

            @property
            def is_healthy(self) -> bool:
                """Check if application is healthy and operational."""
                running = c.Web.WebEnvironment.Status.RUNNING.value
                maintenance = c.Web.WebEnvironment.Status.MAINTENANCE.value
                return self.status in {running, maintenance}

            @property
            def can_start(self) -> bool:
                """Check if application can be started."""
                return self.status == c.Web.WebEnvironment.Status.STOPPED.value

            @property
            def can_stop(self) -> bool:
                """Check if application can be stopped."""
                return self.status == c.Web.WebEnvironment.Status.RUNNING.value

            @property
            def can_restart(self) -> bool:
                """Check if application can be restarted using flext_u.in_() DSL pattern."""
                running = c.Web.WebEnvironment.Status.RUNNING.value
                stopped = c.Web.WebEnvironment.Status.STOPPED.value
                error = c.Web.WebEnvironment.Status.ERROR.value
                # Use flext_u.in_() for unified membership check (DSL pattern)
                return flext_u.in_(self.status, {running, stopped, error})

            @property
            def url(self) -> str:
                """Get the full URL with conditional protocol selection."""
                ssl_ports = c.Web.WebSecurity.SSL_PORTS
                protocol = (
                    c.Web.WebDefaults.HTTPS_PROTOCOL
                    if flext_u.in_(self.port, ssl_ports)
                    else c.Web.WebDefaults.HTTP_PROTOCOL
                )
                return f"{protocol}://{self.host}:{self.port}"

            def validate_business_rules(self) -> r[bool]:
                """Validate application business rules (Aggregate validation).

                Fast-fail validation - no fallbacks, explicit checks only.

                Returns:
                    r[bool]: Success contains True if valid, failure with error message

                """
                # Use flext_u.guard() + flext_u.V.string.min_length() for unified validation (DSL pattern)
                min_name_length = c.Web.WebValidation.NAME_LENGTH_RANGE[0]
                name_validated = flext_u.guard(
                    self.name,
                    str,
                    flext_u.V.string.min_length(min_name_length),
                    error_message=f"App name must be at least {min_name_length} characters",
                    return_value=True,
                )
                if name_validated is None:
                    return r[bool].fail(
                        f"App name must be at least {min_name_length} characters",
                    )

                # Use flext_u.guard() for unified port range validation (DSL pattern)
                min_port = c.Web.WebValidation.PORT_RANGE[0]
                max_port = c.Web.WebValidation.PORT_RANGE[1]
                # Use flext_u.guard() with combined check for unified error message (DSL pattern)
                port_validated = flext_u.guard(
                    self.port,
                    lambda p: min_port <= p <= max_port,
                    error_message=f"Port must be between {min_port} and {max_port}",
                    return_value=True,
                )
                if port_validated is None:
                    return r[bool].fail(
                        f"Port must be between {min_port} and {max_port}",
                    )
                return r[bool].ok(True)

            def start(self) -> r[FlextWebModels.Web.Entity]:
                """Start the application."""
                running_status = c.Web.WebEnvironment.Status.RUNNING.value
                already_running = self.status == running_status
                if already_running:
                    return r[FlextWebModels.Web.Entity].fail(
                        "already running",
                    )
                self.status = running_status
                # Use flext_u.val() for unified result unwrapping (DSL pattern)
                event_result = self.add_domain_event("ApplicationStarted")
                if event_result.is_failure:  # pragma: no cover
                    error_msg = (
                        f"Failed to add domain event: {flext_u.err(event_result)}"
                    )
                    return r[FlextWebModels.Web.Entity].fail(
                        error_msg,
                    )
                return r[FlextWebModels.Web.Entity].ok(self)

            def stop(self) -> r[FlextWebModels.Web.Entity]:
                """Stop the application."""
                running_status = c.Web.WebEnvironment.Status.RUNNING.value
                stopped_status = c.Web.WebEnvironment.Status.STOPPED.value
                not_running = self.status != running_status
                if not_running:
                    return r[FlextWebModels.Web.Entity].fail(
                        "not running",
                    )
                self.status = stopped_status
                # Use flext_u.val() + flext_u.err() for unified result handling (DSL pattern)
                event_result = self.add_domain_event("ApplicationStopped")
                if event_result.is_failure:  # pragma: no cover
                    error_msg = (
                        f"Failed to add domain event: {flext_u.err(event_result)}"
                    )
                    return r[FlextWebModels.Web.Entity].fail(
                        error_msg,
                    )
                return r[FlextWebModels.Web.Entity].ok(self)

            def restart(self) -> r[FlextWebModels.Web.Entity]:
                """Restart the application."""
                can_restart_validated = self.can_restart
                if not can_restart_validated:
                    return r[FlextWebModels.Web.Entity].fail(
                        "Cannot restart in current state",
                    )
                starting_status = c.Web.WebEnvironment.Status.STARTING.value
                running_status = c.Web.WebEnvironment.Status.RUNNING.value
                self.status = starting_status
                # Use flext_u.val() + flext_u.err() for unified result handling (DSL pattern)
                restart_event_result = self.add_domain_event("ApplicationRestarting")
                if restart_event_result.is_failure:  # pragma: no cover
                    error_msg = f"Failed to add domain event: {flext_u.err(restart_event_result)}"
                    return r[FlextWebModels.Web.Entity].fail(
                        error_msg,
                    )
                self.status = running_status
                start_event_result = self.add_domain_event("ApplicationStarted")
                if start_event_result.is_failure:  # pragma: no cover
                    error_msg = (
                        f"Failed to add domain event: {flext_u.err(start_event_result)}"
                    )
                    return r[FlextWebModels.Web.Entity].fail(
                        error_msg,
                    )
                return r[FlextWebModels.Web.Entity].ok(self)

            def update_metrics(
                self,
                new_metrics: dict[str, object],
            ) -> r[bool]:
                """Update application metrics.

                Returns:
                    r[bool]: Success contains True if metrics updated,
                                    failure contains error message

                """
                # Use flext_u.guard() for unified type validation (DSL pattern)
                metrics_validated = flext_u.guard(new_metrics, dict, return_value=True)
                if metrics_validated is None:
                    return r[bool].fail("Metrics must be a dictionary")
                self.metrics.update(metrics_validated)
                # Use flext_u.val() + flext_u.err() for unified result handling (DSL pattern)
                event_result = self.add_domain_event("MetricsUpdated")
                if event_result.is_failure:  # pragma: no cover
                    error_msg = (
                        f"Failed to add domain event: {flext_u.err(event_result)}"
                    )
                    return r[bool].fail(error_msg)
                return r[bool].ok(True)

            def get_health_status(self) -> dict[str, object]:
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

            def add_domain_event(
                self,
                event_name: str,
                _data: object | None = None,
            ) -> r[bool]:
                """Add domain event for event sourcing.

                Returns:
                    r[bool]: Success contains True if event added,
                                    failure contains error message

                """
                # Use flext_u.guard() for unified validation (DSL pattern)
                # First check type, then check non-empty
                event_type_validated = flext_u.guard(event_name, str, return_value=True)
                if event_type_validated is None:
                    return r[bool].fail("Event must be a string")
                event_validated = flext_u.guard(
                    event_type_validated,
                    "non_empty",
                    return_value=True,
                )
                if event_validated is None:
                    return r[bool].fail("Event cannot be empty")
                self.domain_events.append(event_validated)
                return r[bool].ok(True)

            @classmethod
            def format_id_from_name(cls, name: str) -> str:
                """Format application ID from name using web utilities.

                This method uses flext_u.format_app_id directly,
                ensuring consistent ID formatting across the codebase.

                Args:
                    name: Application name to format

                Returns:
                    Formatted application ID

                Raises:
                    ValueError: If name cannot be formatted to valid ID

                """
                # Import at module level - flext_u is used for ID formatting
                return flext_u.format_app_id(name)

        class EntityConfig(m_core.Value):
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
                max_length=255,
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

        # =========================================================================
        # SERVICE REQUEST/RESPONSE MODELS - Replace dict[str, object] types
        # =========================================================================

        class Credentials(m_core.Value):
            """Authentication credentials model."""

            username: str = Field(min_length=1, description="Username")
            password: str = Field(min_length=1, description="Password")

        class UserData(m_core.Value):
            """User registration data model."""

            username: str = Field(min_length=1, description="Username")
            email: str = Field(min_length=1, description="Email address")
            password: str = Field(
                default="",
                description="Password (empty string if not provided)",
            )

        class AppData(m_core.Value):
            """Application creation data model."""

            name: str = Field(
                min_length=c.Web.WebValidation.NAME_LENGTH_RANGE[0],
                max_length=c.Web.WebValidation.NAME_LENGTH_RANGE[1],
                description="Application name",
            )
            host: str = Field(
                min_length=1,
                max_length=255,
                description="Application host",
            )
            port: int = Field(
                ge=c.Web.WebValidation.PORT_RANGE[0],
                le=c.Web.WebValidation.PORT_RANGE[1],
                description="Application port",
            )

        class EntityData(m_core.Value):
            """Generic entity data model."""

            data: dict[str, object] = Field(
                default_factory=dict,
                description="Entity data dictionary",
            )

        class AuthResponse(m_core.Value):
            """Authentication response model."""

            token: str = Field(description="Authentication token")
            user_id: str = Field(description="User identifier")
            authenticated: bool = Field(description="Authentication status")

        class UserResponse(m_core.Value):
            """User registration response model."""

            id: str = Field(description="User identifier")
            username: str = Field(description="Username")
            email: str = Field(description="Email address")
            created: bool = Field(description="Creation status")

        class ApplicationResponse(m_core.Value):
            """Application management response model."""

            id: str = Field(description="Application identifier")
            name: str = Field(description="Application name")
            host: str = Field(description="Application host")
            port: int = Field(description="Application port")
            status: str = Field(description="Application status")
            created_at: str = Field(description="Creation timestamp")

        class HealthResponse(m_core.Value):
            """Health check response model."""

            status: str = Field(description="Health status")
            service: str = Field(description="Service name")
            timestamp: str = Field(description="Timestamp")

        class MetricsResponse(m_core.Value):
            """Metrics response model."""

            service_status: str = Field(description="Service status")
            components: list[str] = Field(description="Service components")

        class DashboardResponse(m_core.Value):
            """Dashboard response model."""

            total_applications: int = Field(description="Total applications")
            running_applications: int = Field(description="Running applications")
            service_status: str = Field(description="Service status")
            routes_initialized: bool = Field(description="Routes initialization status")
            middleware_configured: bool = Field(
                description="Middleware configuration status",
            )
            timestamp: str = Field(description="Timestamp")

        class ServiceResponse(m_core.Value):
            """Generic service response model."""

            service: str = Field(description="Service name")
            capabilities: list[str] = Field(description="Service capabilities")
            status: str = Field(description="Service status")
            config: bool = Field(description="Configuration status")

        # =========================================================================
        # WEB REQUEST/RESPONSE MODELS (Value Objects)
        # =========================================================================

        class WebRequest(m_core.Value):
            """Web request model with complete tracking."""

            method: c.Web.HttpMethodLiteral = Field(
                default="GET",  # Default HTTP method
                description="HTTP method",
            )
            url: str = Field(min_length=1, max_length=2048, description="Request URL")
            headers: dict[str, str] = Field(
                default_factory=dict,
                description="HTTP headers",
            )
            body: str | dict[str, object] | None = Field(
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

        class WebResponse(m_core.Value):
            """Web response model with status tracking."""

            request_id: str = Field(description="Associated request identifier")
            status_code: int = Field(ge=100, le=599, description="HTTP status code")
            headers: dict[str, str] = Field(
                default_factory=dict,
                description="HTTP response headers",
            )
            body: str | dict[str, object] | None = Field(
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

        class AppConfig(m_core.Value):
            """Application configuration model."""

            title: str = Field(
                min_length=1,
                max_length=100,
                description="Application title",
            )
            version: str = Field(description="Application version")
            description: str = Field(
                min_length=1,
                max_length=500,
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

        # =========================================================================
        # FACTORY METHODS (Creation patterns)
        # =========================================================================

        @classmethod
        def create_web_app(
            cls,
            name: str,
            host: str = c.Web.WebDefaults.HOST,
            port: int = c.Web.WebDefaults.PORT,
            **kwargs,
        ) -> r[FlextWebModels.Web.Entity]:
            """Create a web application from direct parameters.

            No dict conversion - use direct parameters for type safety.
            Pydantic validation will handle errors automatically.

            Args:
                name: Application name
                host: Application host
                port: Application port
                **kwargs: Additional entity parameters

            Returns:
                r[Web.Entity]: Success contains entity,
                                            failure contains validation error

            """
            try:
                entity = cls.Entity(
                    name=name,
                    host=host,
                    port=port,
                    **kwargs,
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
            method: c.Web.HttpMethodLiteral,
            url: str,
            headers: dict[str, str] | None = None,
            body: str | dict[str, object] | None = None,
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
            # Use flext_u.guard() for unified headers validation (DSL pattern)
            # Validate headers - must be dict or None
            if headers is not None and not isinstance(headers, dict):
                return r[FlextWebModels.WebRequest].fail(
                    "Headers must be a dictionary or None",
                )
            headers_validated = headers if isinstance(headers, dict) else {}

            # Use flext_u.try_() for unified error handling (DSL pattern)
            def create_request() -> FlextWebModels.WebRequest:
                """Create request model."""
                return cls.WebRequest(
                    method=method,
                    url=url,
                    headers=headers_validated,
                    body=body,
                )

            # Use flext_u.try_() with custom exception handling for better error messages
            try:
                request = create_request()
                return r[FlextWebModels.WebRequest].ok(request)
            except Exception as exc:
                # Use flext_u.err() pattern for unified error extraction (DSL pattern)
                return r[FlextWebModels.WebRequest].fail(
                    f"Failed to create web request: {exc}",
                )

        @classmethod
        def create_web_response(
            cls,
            request_id: str,
            status_code: int,
            headers: dict[str, str] | None = None,
            body: str | dict[str, object] | None = None,
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
            # Use flext_u.guard() for unified headers validation (DSL pattern)
            # Validate headers - must be dict or None
            if headers is not None and not isinstance(headers, dict):
                return r[FlextWebModels.WebResponse].fail(
                    "Headers must be a dictionary or None",
                )
            headers_validated = headers if isinstance(headers, dict) else {}

            # Use flext_u.try_() for unified error handling (DSL pattern)
            def create_response() -> FlextWebModels.WebResponse:
                """Create response model."""
                return cls.WebResponse(
                    request_id=request_id,
                    status_code=status_code,
                    headers=headers_validated,
                    body=body,
                )

            # Use flext_u.try_() with custom exception handling for better error messages
            try:
                response = create_response()
                return r[FlextWebModels.WebResponse].ok(response)
            except Exception as exc:
                # Use flext_u.err() pattern for unified error extraction (DSL pattern)
                return r[FlextWebModels.WebResponse].fail(
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
                max_length=500,
                description="Application description",
            )
            debug: bool = Field(default=False, description="FastAPI debug mode")
            testing: bool = Field(default=False, description="FastAPI testing mode")
            middlewares: list[object] = Field(
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
m_web = FlextWebModels

__all__ = ["FlextWebModels", "m", "m_web"]
