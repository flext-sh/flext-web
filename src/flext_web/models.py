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
from typing import Any

from flext_core import FlextResult
from pydantic import BaseModel, Field, ValidationError, field_validator

from flext_web.constants import FlextWebConstants
from flext_web.utilities import FlextWebUtilities

# HttpMethodLiteral - import from constants for centralized definition
HttpMethodLiteral = FlextWebConstants.HttpMethodLiteral


class FlextWebModels:
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
        >>> request = FlextWebModels.Http.Request(
        ...     url="https://example.com/api", method="POST", body={"key": "value"}
        ... )
        >>> # Check request properties
        >>> assert request.is_secure
        >>> assert request.has_body

    """

    # =========================================================================
    # HTTP PROTOCOL MODELS (Value Objects - immutable)
    # =========================================================================

    class Http(BaseModel):
        """HTTP protocol models for generic web communication (Layer 2: Domain).

        Contains immutable value objects for HTTP message representation
        following RFC standards. All models validate against HTTP constraints.
        """

        class Message(BaseModel):
            """Generic HTTP message base model with protocol validation.

            Represents common HTTP message structure with headers, body,
            and timestamp. Used as base for Request and Response models.

            Attributes:
                headers: HTTP headers dictionary mapping header names to values
                body: Message body as string, dict, or None for no body
                timestamp: UTC timestamp when message was created

            """

            headers: dict[str, str] = Field(
                default_factory=dict, description="HTTP headers for message"
            )
            body: str | dict[str, Any] | None = Field(
                default=None, description="Message body content (optional for GET/HEAD)"
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
                max_length=FlextWebConstants.WebValidation.URL_LENGTH_RANGE[1],
                description="Request URL",
            )
            method: HttpMethodLiteral = Field(
                default="GET",  # Use string literal, validated against HttpMethodLiteral
                description="HTTP method",
            )
            timeout: float = Field(
                default=FlextWebConstants.Http.DEFAULT_TIMEOUT_SECONDS,
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
                default=None, ge=0.0, description="Response processing time in seconds"
            )

            @property
            def is_success(self) -> bool:
                """Check if HTTP status indicates success (2xx range).

                Returns:
                    True if status code is 200-299, False otherwise

                """
                success_min, success_max = FlextWebConstants.Http.SUCCESS_RANGE
                return success_min <= self.status_code <= success_max

            @property
            def is_error(self) -> bool:
                """Check if HTTP status indicates client or server error.

                Returns:
                    True if status code >= 400, False otherwise

                """
                return self.status_code >= FlextWebConstants.Http.ERROR_MIN

    # =========================================================================
    # WEB APPLICATION MODELS (Entities - with identity)
    # =========================================================================

    class Web(BaseModel):
        """Web-specific models extending HTTP with application context.

        Contains entities and value objects specific to web applications
        including request/response tracking and web-specific metadata.
        """

        class Request(BaseModel):
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
                max_length=FlextWebConstants.WebValidation.URL_LENGTH_RANGE[1],
                description="Request URL",
            )
            method: HttpMethodLiteral = Field(
                default="GET",  # Use string literal, validated against HttpMethodLiteral
                description="HTTP method",
            )
            timeout: float = Field(
                default=FlextWebConstants.Http.DEFAULT_TIMEOUT_SECONDS,
                ge=0.0,
                le=300.0,
                description="Request timeout in seconds",
            )
            headers: dict[str, str] = Field(
                default_factory=dict, description="HTTP headers"
            )
            body: str | dict[str, Any] | None = Field(
                default=None, description="Request body content (optional for GET/HEAD)"
            )
            timestamp: datetime = Field(
                default_factory=lambda: datetime.now(UTC),
                description="Request timestamp",
            )
            request_id: str = Field(
                default_factory=lambda: str(uuid.uuid4()),
                description="Unique request identifier",
            )
            query_params: dict[str, Any] = Field(
                default_factory=dict, description="Query string parameters"
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

        class Response(BaseModel):
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
                default_factory=dict, description="HTTP response headers"
            )
            body: str | dict[str, Any] | None = Field(
                default=None, description="Response body content"
            )
            timestamp: datetime = Field(
                default_factory=lambda: datetime.now(UTC),
                description="Response timestamp",
            )
            elapsed_time: float = Field(
                default=0.0, ge=0.0, description="Response elapsed time in seconds"
            )
            response_id: str = Field(
                default_factory=lambda: str(uuid.uuid4()),
                description="Unique response identifier",
            )
            request_id: str = Field(description="Associated request identifier")
            content_type: str = Field(
                default=FlextWebConstants.Http.CONTENT_TYPE_JSON,
                description="Response content type",
            )
            content_length: int = Field(
                default=0, ge=0, description="Response body length in bytes"
            )
            processing_time_ms: float = Field(
                default=0.0, ge=0.0, description="Processing time in milliseconds"
            )

            @property
            def is_success(self) -> bool:
                """Check if web response status indicates success.

                Returns:
                    True if status code is 200-299, False otherwise

                """
                success_min, success_max = FlextWebConstants.Http.SUCCESS_RANGE
                return success_min <= self.status_code <= success_max

            @property
            def is_error(self) -> bool:
                """Check if web response status indicates error.

                Returns:
                    True if status code >= 400, False otherwise

                """
                return self.status_code >= FlextWebConstants.Http.ERROR_MIN

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

    class Application(BaseModel):
        """Application domain models with state management.

        Contains application entities with lifecycle management,
        status tracking, and event sourcing support.
        """

        # EntityStatus removed - use FlextWebConstants.WebEnvironment.Status instead
        # All status values are now centralized in constants.py

        class Entity(BaseModel):
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
                min_length=1, max_length=100, description="Application name"
            )

            @field_validator("name")
            @classmethod
            def validate_name(cls, v: str) -> str:
                """Validate application name according to business rules."""
                min_length = FlextWebConstants.WebValidation.NAME_LENGTH_RANGE[0]
                if len(v) < min_length:
                    msg = f"Name must be at least {min_length} characters"
                    raise ValueError(msg)

                max_length = FlextWebConstants.WebValidation.NAME_LENGTH_RANGE[1]
                if len(v) > max_length:  # pragma: no cover
                    msg = f"Name must be at most {max_length} characters"
                    raise ValueError(msg)

                # Check for reserved names - use constants
                reserved_names_set = set(FlextWebConstants.WebSecurity.RESERVED_NAMES)
                if v.lower() in reserved_names_set:
                    msg = f"Name '{v}' is reserved and cannot be used"
                    raise ValueError(msg)

                # Security validation - check for dangerous patterns from constants
                for pattern in FlextWebConstants.WebSecurity.DANGEROUS_PATTERNS:
                    if pattern.lower() in v.lower():
                        msg = f"Name contains dangerous pattern: {pattern}"
                        raise ValueError(msg)

                return v

            host: str = Field(
                default=FlextWebConstants.WebDefaults.HOST,
                min_length=1,
                max_length=255,
                description="Application host address",
            )
            port: int = Field(
                default=FlextWebConstants.WebDefaults.PORT,
                ge=FlextWebConstants.WebValidation.PORT_RANGE[0],
                le=FlextWebConstants.WebValidation.PORT_RANGE[1],
                description="Application port number",
            )
            status: str = Field(
                default=FlextWebConstants.WebEnvironment.Status.STOPPED.value,
                description="Current application status",
            )

            @field_validator("status")
            @classmethod
            def validate_status(cls, v: str) -> str:
                """Validate application status against allowed values from constants."""
                valid_statuses = set(FlextWebConstants.WebEnvironment.STATUSES)
                if v not in valid_statuses:
                    msg = f"Invalid status '{v}'. Must be one of: {sorted(valid_statuses)}"
                    raise ValueError(msg)
                return v

            environment: str = Field(
                default=FlextWebConstants.WebEnvironment.Name.DEVELOPMENT.value,
                description="Deployment environment",
            )
            debug_mode: bool = Field(
                default=FlextWebConstants.WebDefaults.DEBUG_MODE,
                description="Debug mode enabled flag",
            )
            version: int = Field(
                default=FlextWebConstants.WebDefaults.VERSION_INT,
                description="Application version",
            )
            metrics: dict[str, Any] = Field(
                default_factory=dict, description="Application metrics"
            )
            domain_events: list[str] = Field(
                default_factory=list, description="Domain events for event sourcing"
            )

            @property
            def is_running(self) -> bool:
                """Check if application is currently running."""
                return (
                    self.status == FlextWebConstants.WebEnvironment.Status.RUNNING.value
                )

            @property
            def is_healthy(self) -> bool:
                """Check if application is healthy and operational."""
                running = FlextWebConstants.WebEnvironment.Status.RUNNING.value
                maintenance = FlextWebConstants.WebEnvironment.Status.MAINTENANCE.value
                return self.status in {running, maintenance}

            @property
            def can_start(self) -> bool:
                """Check if application can be started."""
                return (
                    self.status == FlextWebConstants.WebEnvironment.Status.STOPPED.value
                )

            @property
            def can_stop(self) -> bool:
                """Check if application can be stopped."""
                return (
                    self.status == FlextWebConstants.WebEnvironment.Status.RUNNING.value
                )

            @property
            def can_restart(self) -> bool:
                """Check if application can be restarted."""
                running = FlextWebConstants.WebEnvironment.Status.RUNNING.value
                stopped = FlextWebConstants.WebEnvironment.Status.STOPPED.value
                error = FlextWebConstants.WebEnvironment.Status.ERROR.value
                return self.status in {running, stopped, error}

            @property
            def url(self) -> str:
                """Get the full URL for the application."""
                ssl_ports = FlextWebConstants.WebSecurity.SSL_PORTS
                protocol = (
                    FlextWebConstants.WebDefaults.HTTPS_PROTOCOL
                    if self.port in ssl_ports
                    else FlextWebConstants.WebDefaults.HTTP_PROTOCOL
                )
                return f"{protocol}://{self.host}:{self.port}"

            def validate_business_rules(self) -> FlextResult[bool]:
                """Validate application business rules (Aggregate validation).

                Fast-fail validation - no fallbacks, explicit checks only.

                Returns:
                    FlextResult[bool]: Success contains True if valid, failure with error message

                """
                min_name_length = FlextWebConstants.WebValidation.NAME_LENGTH_RANGE[0]
                if not self.name:  # pragma: no cover
                    return FlextResult[bool].fail(
                        f"App name must be at least {min_name_length} characters"
                    )
                if len(self.name) < min_name_length:
                    return FlextResult[bool].fail(
                        f"App name must be at least {min_name_length} characters"
                    )
                min_port = FlextWebConstants.WebValidation.PORT_RANGE[0]
                max_port = FlextWebConstants.WebValidation.PORT_RANGE[1]
                if self.port < min_port:
                    return FlextResult[bool].fail(
                        f"Port must be between {min_port} and {max_port}"
                    )
                if self.port > max_port:
                    return FlextResult[bool].fail(
                        f"Port must be between {min_port} and {max_port}"
                    )
                return FlextResult[bool].ok(True)

            def start(self) -> FlextResult[FlextWebModels.Application.Entity]:
                """Start the application (state transition command)."""
                running_status = FlextWebConstants.WebEnvironment.Status.RUNNING.value
                if self.status == running_status:
                    return FlextResult[FlextWebModels.Application.Entity].fail(
                        "already running"
                    )
                self.status = running_status
                # add_domain_event returns FlextResult[bool] - internal operation always succeeds
                event_result = self.add_domain_event("ApplicationStarted")
                if event_result.is_failure:  # pragma: no cover
                    return FlextResult[FlextWebModels.Application.Entity].fail(
                        f"Failed to add domain event: {event_result.error}"
                    )
                return FlextResult[FlextWebModels.Application.Entity].ok(self)

            def stop(self) -> FlextResult[FlextWebModels.Application.Entity]:
                """Stop the application (state transition command)."""
                running_status = FlextWebConstants.WebEnvironment.Status.RUNNING.value
                stopped_status = FlextWebConstants.WebEnvironment.Status.STOPPED.value
                if self.status != running_status:
                    return FlextResult[FlextWebModels.Application.Entity].fail(
                        "not running"
                    )
                self.status = stopped_status
                # add_domain_event returns FlextResult[bool] - internal operation always succeeds
                event_result = self.add_domain_event("ApplicationStopped")
                if event_result.is_failure:  # pragma: no cover
                    return FlextResult[FlextWebModels.Application.Entity].fail(
                        f"Failed to add domain event: {event_result.error}"
                    )
                return FlextResult[FlextWebModels.Application.Entity].ok(self)

            def restart(self) -> FlextResult[FlextWebModels.Application.Entity]:
                """Restart the application (state transition command)."""
                if not self.can_restart:
                    return FlextResult[FlextWebModels.Application.Entity].fail(
                        "Cannot restart in current state"
                    )
                starting_status = FlextWebConstants.WebEnvironment.Status.STARTING.value
                running_status = FlextWebConstants.WebEnvironment.Status.RUNNING.value
                self.status = starting_status
                # add_domain_event returns FlextResult[bool] - internal operation always succeeds
                restart_event_result = self.add_domain_event("ApplicationRestarting")
                if restart_event_result.is_failure:
                    return FlextResult[
                        FlextWebModels.Application.Entity
                    ].fail(  # pragma: no cover
                        f"Failed to add domain event: {restart_event_result.error}"
                    )
                self.status = running_status
                start_event_result = self.add_domain_event("ApplicationStarted")
                if start_event_result.is_failure:
                    return FlextResult[
                        FlextWebModels.Application.Entity
                    ].fail(  # pragma: no cover
                        f"Failed to add domain event: {start_event_result.error}"
                    )
                return FlextResult[FlextWebModels.Application.Entity].ok(self)

            def update_metrics(self, new_metrics: dict[str, Any]) -> FlextResult[bool]:
                """Update application metrics.

                Returns:
                    FlextResult[bool]: Success contains True if metrics updated,
                                     failure contains error message

                """
                if not isinstance(new_metrics, dict):
                    return FlextResult[bool].fail("Metrics must be a dictionary")
                self.metrics.update(new_metrics)
                # add_domain_event returns FlextResult[bool] - internal operation always succeeds
                event_result = self.add_domain_event("MetricsUpdated")
                if event_result.is_failure:  # pragma: no cover
                    return FlextResult[bool].fail(
                        f"Failed to add domain event: {event_result.error}"
                    )
                return FlextResult[bool].ok(True)

            def get_health_status(self) -> dict[str, Any]:
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

            def add_domain_event(self, event: str) -> FlextResult[bool]:
                """Add domain event for event sourcing.

                Returns:
                    FlextResult[bool]: Success contains True if event added,
                                     failure contains error message

                """
                if not isinstance(event, str):
                    return FlextResult[bool].fail("Event must be a string")
                if len(event) == 0:
                    return FlextResult[bool].fail("Event cannot be empty")
                self.domain_events.append(event)
                return FlextResult[bool].ok(True)

            @classmethod
            def format_id_from_name(cls, name: str) -> str:
                """Format application ID from name using web utilities.

                This method uses FlextWebUtilities.format_app_id directly,
                ensuring consistent ID formatting across the codebase.

                Args:
                    name: Application name to format

                Returns:
                    Formatted application ID

                Raises:
                    ValueError: If name cannot be formatted to valid ID

                """
                # Import at module level - FlextWebUtilities is used for ID formatting
                return FlextWebUtilities.format_app_id(name)

        class EntityConfig(BaseModel):
            """Application entity configuration (Value Object).

            Represents configuration settings for application entities.
            Uses Constants for defaults - Config has priority when provided.
            """

            app_name: str = Field(
                default=FlextWebConstants.WebDefaults.APP_NAME,
                min_length=FlextWebConstants.WebValidation.NAME_LENGTH_RANGE[0],
                max_length=FlextWebConstants.WebValidation.NAME_LENGTH_RANGE[1],
                description="Application name",
            )
            host: str = Field(
                default=FlextWebConstants.WebDefaults.HOST,
                min_length=1,
                max_length=255,
                description="Application host address",
            )
            port: int = Field(
                default=FlextWebConstants.WebDefaults.PORT,
                ge=FlextWebConstants.WebValidation.PORT_RANGE[0],
                le=FlextWebConstants.WebValidation.PORT_RANGE[1],
                description="Application port number",
            )
            debug: bool = Field(
                default=FlextWebConstants.WebDefaults.DEBUG_MODE,
                description="Debug mode flag",
            )
            secret_key: str = Field(
                default=FlextWebConstants.WebDefaults.SECRET_KEY,
                min_length=FlextWebConstants.WebSecurity.MIN_SECRET_KEY_LENGTH,
                description="Application secret key",
            )

    # =========================================================================
    # SERVICE REQUEST/RESPONSE MODELS - Replace dict[str, object] types
    # =========================================================================

    class Service(BaseModel):
        """Service layer request/response models replacing generic dict types."""

        class Credentials(BaseModel):
            """Authentication credentials model."""

            username: str = Field(min_length=1, description="Username")
            password: str = Field(min_length=1, description="Password")

        class UserData(BaseModel):
            """User registration data model."""

            username: str = Field(min_length=1, description="Username")
            email: str = Field(min_length=1, description="Email address")
            password: str = Field(
                default="", description="Password (empty string if not provided)"
            )

        class AppData(BaseModel):
            """Application creation data model."""

            name: str = Field(
                min_length=FlextWebConstants.WebValidation.NAME_LENGTH_RANGE[0],
                max_length=FlextWebConstants.WebValidation.NAME_LENGTH_RANGE[1],
                description="Application name",
            )
            host: str = Field(
                min_length=1, max_length=255, description="Application host"
            )
            port: int = Field(
                ge=FlextWebConstants.WebValidation.PORT_RANGE[0],
                le=FlextWebConstants.WebValidation.PORT_RANGE[1],
                description="Application port",
            )

        class EntityData(BaseModel):
            """Generic entity data model."""

            data: dict[str, Any] = Field(
                default_factory=dict, description="Entity data dictionary"
            )

        class AuthResponse(BaseModel):
            """Authentication response model."""

            token: str = Field(description="Authentication token")
            user_id: str = Field(description="User identifier")
            authenticated: bool = Field(description="Authentication status")

        class UserResponse(BaseModel):
            """User registration response model."""

            id: str = Field(description="User identifier")
            username: str = Field(description="Username")
            email: str = Field(description="Email address")
            created: bool = Field(description="Creation status")

        class AppResponse(BaseModel):
            """Application response model."""

            id: str = Field(description="Application identifier")
            name: str = Field(description="Application name")
            host: str = Field(description="Application host")
            port: int = Field(description="Application port")
            status: str = Field(description="Application status")
            created_at: str = Field(description="Creation timestamp")

        class HealthResponse(BaseModel):
            """Health check response model."""

            status: str = Field(description="Health status")
            service: str = Field(description="Service name")
            timestamp: str = Field(description="Timestamp")

        class MetricsResponse(BaseModel):
            """Metrics response model."""

            service_status: str = Field(description="Service status")
            components: list[str] = Field(description="Service components")

        class DashboardResponse(BaseModel):
            """Dashboard response model."""

            total_applications: int = Field(description="Total applications")
            running_applications: int = Field(description="Running applications")
            service_status: str = Field(description="Service status")
            routes_initialized: bool = Field(description="Routes initialization status")
            middleware_configured: bool = Field(
                description="Middleware configuration status"
            )
            timestamp: str = Field(description="Timestamp")

        class ServiceResponse(BaseModel):
            """Generic service response model."""

            service: str = Field(description="Service name")
            capabilities: list[str] = Field(description="Service capabilities")
            status: str = Field(description="Service status")
            config: bool = Field(description="Configuration status")

    # =========================================================================
    # WEB REQUEST/RESPONSE MODELS (Value Objects)
    # =========================================================================

    class WebRequest(BaseModel):
        """Web request model with complete tracking."""

        method: HttpMethodLiteral = Field(
            default="GET",  # Use string literal, validated against HttpMethodLiteral
            description="HTTP method",
        )
        url: str = Field(min_length=1, max_length=2048, description="Request URL")
        headers: dict[str, str] = Field(
            default_factory=dict, description="HTTP headers"
        )
        body: str | dict[str, Any] | None = Field(
            default=None, description="Request body (optional for GET/HEAD)"
        )
        request_id: str = Field(
            default_factory=lambda: str(uuid.uuid4()),
            description="Unique request identifier",
        )
        timestamp: datetime = Field(
            default_factory=lambda: datetime.now(UTC),
            description="Request timestamp",
        )

    class WebResponse(BaseModel):
        """Web response model with status tracking."""

        request_id: str = Field(description="Associated request identifier")
        status_code: int = Field(ge=100, le=599, description="HTTP status code")
        headers: dict[str, str] = Field(
            default_factory=dict, description="HTTP response headers"
        )
        body: str | dict[str, Any] | None = Field(
            default=None, description="Response body (optional for 204 No Content)"
        )
        response_id: str = Field(
            default_factory=lambda: str(uuid.uuid4()),
            description="Unique response identifier",
        )
        timestamp: datetime = Field(
            default_factory=lambda: datetime.now(UTC),
            description="Response timestamp",
        )

    class AppConfig(BaseModel):
        """Application configuration model."""

        title: str = Field(
            min_length=1, max_length=100, description="Application title"
        )
        version: str = Field(description="Application version")
        description: str = Field(
            min_length=1, max_length=500, description="Application description"
        )
        docs_url: str = Field(
            default=FlextWebConstants.WebApi.DOCS_URL, description="Documentation URL"
        )
        redoc_url: str = Field(
            default=FlextWebConstants.WebApi.REDOC_URL, description="ReDoc URL"
        )
        openapi_url: str = Field(
            default=FlextWebConstants.WebApi.OPENAPI_URL, description="OpenAPI URL"
        )

    # =========================================================================
    # FACTORY METHODS (Creation patterns)
    # =========================================================================

    @classmethod
    def create_web_app(
        cls,
        name: str,
        host: str = FlextWebConstants.WebDefaults.HOST,
        port: int = FlextWebConstants.WebDefaults.PORT,
        **kwargs: dict[str, object],
    ) -> FlextResult[FlextWebModels.Application.Entity]:
        """Create a web application from direct parameters.

        No dict conversion - use direct parameters for type safety.
        Pydantic validation will handle errors automatically.

        Args:
            name: Application name
            host: Application host
            port: Application port
            **kwargs: Additional entity parameters

        Returns:
            FlextResult[Application.Entity]: Success contains entity,
                                           failure contains validation error

        """
        try:
            entity = cls.Application.Entity(
                name=name,
                host=host,
                port=port,
                **kwargs,
            )
            return FlextResult.ok(entity)
        except ValidationError as e:  # pragma: no cover
            error_msg = (  # pragma: no cover
                f"Validation failed: {e.errors()[0]['msg']}"
                if e.errors()
                else str(e)  # pragma: no cover
            )
            return FlextResult.fail(error_msg)  # pragma: no cover
        except ValueError as e:  # pragma: no cover
            return FlextResult.fail(str(e))  # pragma: no cover

    @classmethod
    def create_web_request(
        cls,
        method: HttpMethodLiteral,
        url: str,
        headers: dict[str, str] | None = None,
        body: str | dict[str, Any] | None = None,
    ) -> FlextResult[WebRequest]:
        """Create a web request model.

        Args:
            method: HTTP method
            url: Request URL
            headers: Request headers (defaults to empty dict)
            body: Request body

        Returns:
            FlextResult[WebRequest]: Success contains request model,
                                    failure contains validation error

        """
        # Validate headers type - fast fail, no fallback
        if headers is not None and not isinstance(headers, dict):
            return FlextResult[FlextWebModels.WebRequest].fail(
                "Headers must be a dictionary or None"
            )

        try:
            # Use empty dict if None - headers field requires dict
            request_headers = headers if headers is not None else {}
            request = cls.WebRequest(
                method=method,
                url=url,
                headers=request_headers,
                body=body,
            )
            return FlextResult[FlextWebModels.WebRequest].ok(request)
        except ValidationError as e:  # pragma: no cover
            error_msg = (  # pragma: no cover
                f"Validation failed: {e.errors()[0]['msg']}"
                if e.errors()
                else str(e)  # pragma: no cover
            )
            return FlextResult.fail(error_msg)  # pragma: no cover
        except ValueError as e:  # pragma: no cover
            return FlextResult.fail(str(e))  # pragma: no cover

    @classmethod
    def create_web_response(
        cls,
        request_id: str,
        status_code: int,
        headers: dict[str, str] | None = None,
        body: str | dict[str, Any] | None = None,
    ) -> FlextResult[WebResponse]:
        """Create a web response model.

        Args:
            request_id: Associated request identifier
            status_code: HTTP status code
            headers: Response headers (defaults to empty dict)
            body: Response body

        Returns:
            FlextResult[WebResponse]: Success contains response model,
                                     failure contains validation error

        """
        # Validate headers type - fast fail, no fallback
        if headers is not None and not isinstance(headers, dict):
            return FlextResult[FlextWebModels.WebResponse].fail(
                "Headers must be a dictionary or None"
            )

        try:
            # Use empty dict if None - headers field requires dict
            response_headers = headers if headers is not None else {}
            response = cls.WebResponse(
                request_id=request_id,
                status_code=status_code,
                headers=response_headers,
                body=body,
            )
            return FlextResult[FlextWebModels.WebResponse].ok(response)
        except ValidationError as e:  # pragma: no cover
            error_msg = (  # pragma: no cover
                f"Validation failed: {e.errors()[0]['msg']}"
                if e.errors()
                else str(e)  # pragma: no cover
            )
            return FlextResult.fail(error_msg)  # pragma: no cover
        except ValueError as e:  # pragma: no cover
            return FlextResult.fail(str(e))  # pragma: no cover

    class FastAPI:
        """FastAPI framework-specific models for configuration conversion.

        Provides Pydantic models for FastAPI application configuration with
        validation. Used internally for FastAPI framework integration.
        """

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
                default=FlextWebConstants.WebDefaults.APP_NAME,
                min_length=FlextWebConstants.WebValidation.NAME_LENGTH_RANGE[0],
                max_length=FlextWebConstants.WebValidation.NAME_LENGTH_RANGE[1],
                description="FastAPI application title",
            )
            version: str = Field(
                default=FlextWebConstants.WebDefaults.VERSION_STRING,
                description="Application version",
            )
            description: str = Field(
                default=FlextWebConstants.WebApi.DEFAULT_DESCRIPTION,
                min_length=1,
                max_length=500,
                description="Application description",
            )
            debug: bool = Field(default=False, description="FastAPI debug mode")
            testing: bool = Field(default=False, description="FastAPI testing mode")
            middlewares: list[Any] = Field(
                default_factory=list, description="List of middleware objects"
            )
            docs_url: str = Field(
                default=FlextWebConstants.WebApi.DOCS_URL,
                description="Documentation URL",
            )
            redoc_url: str = Field(
                default=FlextWebConstants.WebApi.REDOC_URL, description="ReDoc URL"
            )
            openapi_url: str = Field(
                default=FlextWebConstants.WebApi.OPENAPI_URL, description="OpenAPI URL"
            )


__all__ = ["FlextWebModels"]
