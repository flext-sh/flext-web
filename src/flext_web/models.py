"""FLEXT Web Models - Domain-Driven Design models for web applications (Layer 2: Domain).

This module provides complete domain-driven design models for web-based applications
following flext-core patterns and Pydantic v2 standards. All models implement proper
entity/value object distinction and include comprehensive validation.

**Architecture Layer**: Layer 2 (Domain)
- **Entities**: Models with identity (WebApplication, HttpRequest, etc.)
- **Value Objects**: Immutable models without identity
- **Commands**: Request objects for operations
- **Queries**: Request objects for data retrieval

**Pydantic Features Used**:
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
from enum import Enum
from typing import Any, Literal

from flext_core import FlextResult
from pydantic import BaseModel, Field, computed_field, field_validator

from flext_web.constants import FlextWebConstants


class FlextWebModels:
    """Domain-driven design model collection for web applications (Layer 2: Domain).

    Organizes web models using flext-core DDD patterns:
    - **Entities**: Models with identity and lifecycle
    - **Value Objects**: Immutable models without identity
    - **Commands**: Request objects triggering operations
    - **Queries**: Request objects for data retrieval

    All models use Pydantic v2 with comprehensive validation and follow
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
                default=None, description="Message body content"
            )
            timestamp: datetime = Field(
                default_factory=lambda: datetime.now(UTC),
                description="UTC timestamp of message creation",
            )

        class Request(Message):
            """HTTP request model with comprehensive validation.

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
            method: Literal[
                "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"
            ] = Field(default="GET", description="HTTP method")
            timeout: float = Field(
                default=30.0, ge=0.0, le=300.0, description="Request timeout in seconds"
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
                return (
                    FlextWebConstants.Http.HttpStatus.SUCCESS_MIN
                    <= self.status_code
                    <= FlextWebConstants.Http.HttpStatus.SUCCESS_MAX
                )

            @property
            def is_error(self) -> bool:
                """Check if HTTP status indicates client or server error.

                Returns:
                    True if status code >= 400, False otherwise

                """
                return self.status_code >= FlextWebConstants.Http.HttpStatus.ERROR_MIN

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
            method: Literal[
                "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"
            ] = Field(default="GET", description="HTTP method")
            timeout: float = Field(
                default=30.0, ge=0.0, le=300.0, description="Request timeout in seconds"
            )
            headers: dict[str, str] = Field(
                default_factory=dict, description="HTTP headers"
            )
            body: str | dict[str, Any] | None = Field(
                default=None, description="Request body content"
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
            client_ip: str | None = Field(default=None, description="Client IP address")
            user_agent: str | None = Field(
                default=None, description="Client user agent"
            )

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
            elapsed_time: float | None = Field(
                default=None, ge=0.0, description="Response elapsed time in seconds"
            )
            response_id: str = Field(
                default_factory=lambda: str(uuid.uuid4()),
                description="Unique response identifier",
            )
            request_id: str = Field(description="Associated request identifier")
            content_type: str | None = Field(
                default=None, description="Response content type"
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
                return (
                    FlextWebConstants.Http.HttpStatus.SUCCESS_MIN
                    <= self.status_code
                    <= FlextWebConstants.Http.HttpStatus.SUCCESS_MAX
                )

            @property
            def is_error(self) -> bool:
                """Check if web response status indicates error.

                Returns:
                    True if status code >= 400, False otherwise

                """
                return self.status_code >= FlextWebConstants.Http.HttpStatus.ERROR_MIN

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

        class EntityStatus(Enum):
            """Application status enumeration for state management.

            Defines all possible application states and lifecycle transitions.
            """

            STOPPED = "stopped"
            STARTING = "starting"
            RUNNING = "running"
            STOPPING = "stopping"
            ERROR = "error"
            MAINTENANCE = "maintenance"
            DEPLOYING = "deploying"

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
                if len(v) > max_length:
                    msg = f"Name must be at most {max_length} characters"
                    raise ValueError(msg)

                # Check for reserved names
                reserved_names = {"REDACTED_LDAP_BIND_PASSWORD", "root", "api", "system", "config", "health"}
                if v.lower() in reserved_names:
                    msg = f"Name '{v}' is reserved and cannot be used"
                    raise ValueError(msg)

                # Security validation - check for dangerous patterns
                dangerous_patterns = [
                    "<script",
                    "javascript:",
                    "data:text/html",
                    "'; DROP TABLE",
                    "--",
                    "/*",
                    "*/",
                ]
                for pattern in dangerous_patterns:
                    if pattern.lower() in v.lower():
                        msg = f"Name contains dangerous pattern: {pattern}"
                        raise ValueError(msg)

                return v

            host: str = Field(
                default="localhost",
                min_length=1,
                max_length=255,
                description="Application host address",
            )
            port: int = Field(
                default=8080, ge=1, le=65535, description="Application port number"
            )
            status: str = Field(
                default="stopped", description="Current application status"
            )

            @field_validator("status")
            @classmethod
            def validate_status(cls, v: str) -> str:
                """Validate application status against allowed values."""
                valid_statuses = {
                    "stopped",
                    "starting",
                    "running",
                    "stopping",
                    "error",
                    "maintenance",
                    "deploying",
                }
                if v not in valid_statuses:
                    msg = f"Invalid status '{v}'. Must be one of: {sorted(valid_statuses)}"
                    raise ValueError(msg)
                return v

            environment: str = Field(
                default="development", description="Deployment environment"
            )
            debug_mode: bool = Field(
                default=False, description="Debug mode enabled flag"
            )
            version: int = Field(default=1, description="Application version")
            metrics: dict[str, Any] = Field(
                default_factory=dict, description="Application metrics"
            )
            domain_events: list[str] = Field(
                default_factory=list, description="Domain events for event sourcing"
            )

            @computed_field
            @property
            def is_running(self) -> bool:
                """Check if application is currently running."""
                return self.status == "running"

            @computed_field
            @property
            def is_healthy(self) -> bool:
                """Check if application is healthy and operational."""
                return self.status in {"running", "maintenance"}

            @computed_field
            @property
            def can_start(self) -> bool:
                """Check if application can be started."""
                return self.status == "stopped"

            @computed_field
            @property
            def can_stop(self) -> bool:
                """Check if application can be stopped."""
                return self.status == "running"

            @computed_field
            @property
            def can_restart(self) -> bool:
                """Check if application can be restarted."""
                return self.status in {"running", "stopped", "error"}

            @property
            def url(self) -> str:
                """Get the full URL for the application."""
                protocol = "https" if self.port in {443, 8443} else "http"
                return f"{protocol}://{self.host}:{self.port}"

            def validate_business_rules(self) -> FlextResult[None]:
                """Validate application business rules (Aggregate validation)."""
                if (
                    not self.name
                    or len(self.name)
                    < FlextWebConstants.WebValidation.NAME_LENGTH_RANGE[0]
                ):
                    return FlextResult[None].fail(
                        f"App name must be at least {FlextWebConstants.WebValidation.NAME_LENGTH_RANGE[0]} characters"
                    )
                if (
                    self.port < FlextWebConstants.WebValidation.PORT_RANGE[0]
                    or self.port > FlextWebConstants.WebValidation.PORT_RANGE[1]
                ):
                    return FlextResult[None].fail(
                        f"Port must be between {FlextWebConstants.WebValidation.PORT_RANGE[0]} and {FlextWebConstants.WebValidation.PORT_RANGE[1]}"
                    )
                return FlextResult[None].ok(None)

            def start(self) -> FlextResult[Any]:
                """Start the application (state transition command)."""
                if self.status == "running":
                    return FlextResult.fail("already running")
                self.status = "running"
                self.add_domain_event("ApplicationStarted")
                return FlextResult.ok(self)

            def stop(self) -> FlextResult[Any]:
                """Stop the application (state transition command)."""
                if self.status != "running":
                    return FlextResult.fail("not running")
                self.status = "stopped"
                self.add_domain_event("ApplicationStopped")
                return FlextResult.ok(self)

            def restart(self) -> FlextResult[Any]:
                """Restart the application (state transition command)."""
                if not self.can_restart:
                    return FlextResult.fail("Cannot restart in current state")
                self.status = "starting"
                self.add_domain_event("ApplicationRestarting")
                self.status = "running"
                self.add_domain_event("ApplicationStarted")
                return FlextResult.ok(self)

            def update_metrics(self, new_metrics: dict[str, Any]) -> None:
                """Update application metrics."""
                self.metrics.update(new_metrics)
                self.add_domain_event("MetricsUpdated")

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

            def to_dict(self) -> dict[str, Any]:
                """Convert entity to dictionary representation."""
                return self.model_dump()

            def __str__(self) -> str:
                """Return string representation of the application."""
                return f"{self.name} ({self.url}) - {self.status}"

            def add_domain_event(self, event: str) -> None:
                """Add domain event for event sourcing."""
                self.domain_events.append(event)

        class EntityConfig(BaseModel):
            """Application entity configuration (Value Object).

            Represents configuration settings for application entities.
            """

            app_name: str = Field(
                min_length=1, max_length=100, description="Application name"
            )
            host: str = Field(
                default="localhost",
                min_length=1,
                max_length=255,
                description="Application host address",
            )
            port: int = Field(
                default=8080, ge=1, le=65535, description="Application port number"
            )
            debug: bool = Field(default=False, description="Debug mode flag")
            secret_key: str = Field(min_length=32, description="Application secret key")

    # =========================================================================
    # WEB REQUEST/RESPONSE MODELS (Value Objects)
    # =========================================================================

    class WebRequest(BaseModel):
        """Web request model with comprehensive tracking."""

        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"] = (
            Field(default="GET", description="HTTP method")
        )
        url: str = Field(min_length=1, max_length=2048, description="Request URL")
        headers: dict[str, str] = Field(
            default_factory=dict, description="HTTP headers"
        )
        body: str | dict[str, Any] | None = Field(
            default=None, description="Request body"
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
            default=None, description="Response body"
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
        docs_url: str = Field(default="/docs", description="Documentation URL")
        redoc_url: str = Field(default="/redoc", description="ReDoc URL")
        openapi_url: str = Field(default="/openapi.json", description="OpenAPI URL")

    # =========================================================================
    # FACTORY METHODS (Creation patterns)
    # =========================================================================

    @classmethod
    def create_web_app(
        cls, app_data: dict[str, Any]
    ) -> FlextResult[FlextWebModels.Application.Entity]:
        """Create a web application from data dictionary."""
        try:
            entity = cls.Application.Entity(**app_data)
            return FlextResult.ok(entity)
        except Exception as e:
            return FlextResult.fail(f"Failed to create web app: {e}")

    @classmethod
    def create_web_request(
        cls,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
        url: str,
        headers: dict[str, str] | None = None,
        body: str | dict[str, Any] | None = None,
    ) -> FlextResult[WebRequest]:
        """Create a web request model."""
        try:
            request = cls.WebRequest(
                method=method,
                url=url,
                headers=headers or {},
                body=body,
            )
            return FlextResult.ok(request)
        except Exception as e:
            return FlextResult.fail(f"Failed to create web request: {e}")

    @classmethod
    def create_web_response(
        cls,
        request_id: str,
        status_code: int,
        headers: dict[str, str] | None = None,
        body: str | dict[str, Any] | None = None,
    ) -> FlextResult[WebResponse]:
        """Create a web response model."""
        try:
            response = cls.WebResponse(
                request_id=request_id,
                status_code=status_code,
                headers=headers or {},
                body=body,
            )
            return FlextResult.ok(response)
        except Exception as e:
            return FlextResult.fail(f"Failed to create web response: {e}")

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
            version: str = Field(default="1.0.0", description="Application version")
            description: str = Field(
                default="Generic HTTP Service",
                min_length=1,
                max_length=500,
                description="Application description",
            )
            debug: bool = Field(default=False, description="FastAPI debug mode")
            testing: bool = Field(default=False, description="FastAPI testing mode")
            middlewares: list[Any] = Field(
                default_factory=list, description="List of middleware objects"
            )
            docs_url: str | None = Field(
                default="/docs", description="Documentation URL"
            )
            redoc_url: str | None = Field(default="/redoc", description="ReDoc URL")
            openapi_url: str | None = Field(
                default="/openapi.json", description="OpenAPI URL"
            )


__all__ = ["FlextWebModels"]
