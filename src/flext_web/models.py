"""FLEXT Web Models.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
import re
import uuid
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Annotated, Self, override

from flext_core import FlextCore
from pydantic import (
    ConfigDict,
    Field,
    computed_field,
    field_validator,
    model_validator,
)

from flext_web.constants import FlextWebConstants
from flext_web.typings import FlextWebTypes


class FlextWebModels(FlextCore.Models):
    """Enhanced FLEXT web model system with FlextCore.Mixins integration.

    Inherits from FlextCore.Models to avoid duplication and ensure consistency
    with enhanced Pydantic 2.11 features and comprehensive validation.
    """

    model_config = ConfigDict(
        # Enhanced Pydantic 2.11 enterprise features
        validate_assignment=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        extra="forbid",
        frozen=False,
        validate_return=True,
        ser_json_timedelta="iso8601",
        ser_json_bytes="base64",
        hide_input_in_errors=True,
        json_schema_extra={
            "examples": [
                {
                    "web_application": {
                        "name": "enterprise-web-app",
                        "host": "production.flext.com",
                        "port": 8080,
                        "status": "running",
                    },
                    "web_request": {
                        "method": "POST",
                        "url": "/api/v1/applications",
                        "headers": {"Content-Type": "application/json"},
                    },
                    "web_response": {"status_code": 201, "processing_time_ms": 45.6},
                }
            ],
            "enterprise_features": [
                "Web application lifecycle management",
                "HTTP request/response processing",
                "Security validation and headers",
                "Performance monitoring",
                "CORS and CSRF protection",
            ],
        },
    )

    # Enhanced base models with Pydantic 2.11 features
    class _BaseWebModel(FlextCore.Models.ArbitraryTypesModel):
        """Base web model with enhanced Pydantic 2.11 configuration."""

        model_config = ConfigDict(
            # Enhanced Pydantic 2.11 features
            validate_assignment=True,
            use_enum_values=True,
            arbitrary_types_allowed=True,
            validate_return=True,
            ser_json_timedelta="iso8601",
            ser_json_bytes="base64",
            serialize_by_alias=True,
            populate_by_name=True,
            str_strip_whitespace=True,
            defer_build=False,
            coerce_numbers_to_str=False,
            validate_default=True,
            # Custom encoders for complex types
            json_encoders={
                Path: str,
                datetime: lambda dt: dt.isoformat(),
            },
        )

        @computed_field
        def model_metadata(self) -> FlextCore.Types.Dict:
            """Computed field providing base web model metadata."""
            return {
                "model_class": self.__class__.__name__,
                "framework": "FLEXT Web",
                "pydantic_version": "2.11+",
                "created_at": datetime.now(UTC).isoformat(),
            }

    class WebAppStatus(Enum):
        """Enhanced web application status enumeration."""

        STOPPED = "stopped"
        STARTING = "starting"
        RUNNING = "running"
        STOPPING = "stopping"
        ERROR = "error"
        MAINTENANCE = "maintenance"
        DEPLOYING = "deploying"

    class WebApp(FlextCore.Models.Entity):
        """Enhanced web application domain entity with comprehensive validation."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            # Enhanced Pydantic 2.11 features
            arbitrary_types_allowed=True,
            validate_return=True,
            ser_json_timedelta="iso8601",
            ser_json_bytes="base64",
            serialize_by_alias=True,
            populate_by_name=True,
            str_strip_whitespace=True,
            defer_build=False,
            coerce_numbers_to_str=False,
            validate_default=True,
        )

        name: str = Field(
            ...,
            min_length=FlextWebConstants.WebServer.MIN_APP_NAME_LENGTH,
            max_length=FlextWebConstants.WebServer.MAX_APP_NAME_LENGTH,
            description="Web application name",
        )
        host: str = Field(
            default=FlextWebConstants.WebServer.DEFAULT_HOST,
            min_length=1,
            max_length=255,
            description="Host address for the web application",
        )
        port: int = Field(
            default=FlextWebConstants.WebServer.DEFAULT_PORT,
            ge=FlextWebConstants.WebServer.MIN_PORT,
            le=FlextWebConstants.WebServer.MAX_PORT,
            description="Port number for the web application",
        )
        status: str = Field(
            default="stopped",
            description="Current status of the web application",
        )
        version: int = Field(
            default=1,
            description="Application version",
        )
        health_check_url: str | None = Field(
            default=None,
            description="Health check endpoint URL",
        )
        debug_mode: bool = Field(
            default=False,
            description="Debug mode flag",
        )
        metrics: FlextCore.Types.Dict = Field(
            default_factory=dict,
            description="Application metrics",
        )
        environment: str = Field(
            default="development",
            description="Deployment environment",
        )

        @model_validator(mode="after")
        def validate_web_app_configuration(self) -> Self:
            """Model validator for web application configuration consistency."""
            # Validate port and host combination
            if (
                self.host in {FlextWebConstants.WebSpecific.ALL_INTERFACES, "::"}
                and self.port <= FlextWebConstants.WebSpecific.PRIVILEGED_PORTS_MAX
            ):
                if self.environment == "development":
                    # Allow in development but warn
                    pass
                else:
                    msg = "Binding to all interfaces on privileged ports requires proper configuration"
                    raise ValueError(msg)

            # Validate environment-specific requirements
            if self.environment == "production":
                if self.debug_mode:
                    msg = "Debug mode must be disabled in production environment"
                    raise ValueError(msg)

                if not self.health_check_url:
                    msg = "Health check URL is required in production environment"
                    raise ValueError(msg)

            return self

        @field_validator("status")
        @classmethod
        def validate_status(cls, v: object) -> str:
            """Validate status field with enhanced error handling."""
            # Handle string values
            if isinstance(v, str):
                # Check if it's a valid status value
                valid_values = [status.value for status in FlextWebModels.WebAppStatus]
                if v in valid_values:
                    return v
                msg = f"Invalid status: {v}. Valid values: {valid_values}"
                raise ValueError(msg)

            # Handle enum values
            if hasattr(v, "value") and isinstance(v.value, str):
                return v.value

            type_name = type(v).__name__
            msg = f"Invalid status type: {type_name}. Must be str or WebAppStatus"
            raise ValueError(msg)

        @field_validator("name")
        @classmethod
        def validate_name(cls, v: str) -> str:
            """Enhanced name validation with security checks."""
            name = (v or "").strip()
            if not name:
                msg = "Name cannot be empty"
                raise ValueError(msg)

            # Check reserved names
            reserved = {"REDACTED_LDAP_BIND_PASSWORD", "root", "api", "system", "config", "health"}
            if name.lower() in reserved:
                msg = f"Name '{name}' is reserved"
                raise ValueError(msg)

            # Security validation - check for dangerous characters
            dangerous_patterns = [
                r"<[^>]*>",  # HTML tags
                r"javascript:",  # JavaScript protocol
                r"data:",  # Data protocol
                r"vbscript:",  # VBScript protocol
            ]

            for pattern in dangerous_patterns:
                if re.search(pattern, name, re.IGNORECASE):
                    msg = f"Name contains potentially dangerous content: {name}"
                    raise ValueError(msg)

            # Check for SQL injection patterns
            sql_patterns = [r"'.*--", r"'.*;", r"union.*select", r"drop.*table"]
            for pattern in sql_patterns:
                if re.search(pattern, name, re.IGNORECASE):
                    msg = f"Name contains SQL injection patterns: {name}"
                    raise ValueError(msg)

            return name

        @field_validator("host")
        @classmethod
        def validate_host(cls, v: str) -> str:
            """Enhanced host validation with comprehensive format checking."""
            host = (v or "").strip()
            if not host:
                msg = "Host cannot be empty"
                raise ValueError(msg)

            # Use flext-core validation utilities
            result = FlextCore.Models.Validation.validate_hostname(host)
            if result.is_failure:
                raise ValueError(result.error)

            # Additional security checks
            if host.lower() in {"localhost", "127.0.0.1", ":: , ::1"}:
                return host

            # Validate against known malicious patterns
            malicious_patterns = [
                r"\.\.",  # Directory traversal
                r"//",  # Protocol confusion
                r"@",  # User info in URL
            ]

            for pattern in malicious_patterns:
                if re.search(pattern, host):
                    msg = f"Host contains potentially malicious pattern: {host}"
                    raise ValueError(msg)

            return host

        @field_validator("health_check_url")
        @classmethod
        def validate_health_check_url(cls, v: str | None) -> str | None:
            """Validate health check URL format."""
            if v is None:
                return None

            url = v.strip()
            if not url:
                return None

            # Basic URL validation
            result = FlextCore.Models.Validation.validate_url(url)
            if result.is_failure:
                raise ValueError(result.error)

            return url

        @computed_field
        def is_running(self) -> bool:
            """Check if app is running."""
            return self.status == "running"

        @computed_field
        def is_healthy(self) -> bool:
            """Check if app is healthy (running state)."""
            return self.status == "running"

        @computed_field
        def url(self) -> str:
            """Get app URL with proper protocol detection."""
            # Standard HTTPS ports
            https_ports = {
                FlextCore.Constants.Http.HTTPS_PORT,
                FlextCore.Constants.Http.HTTPS_ALT_PORT,
            }
            protocol = "https" if self.port in https_ports else "http"
            return f"{protocol}://{self.host}:{self.port}"

        @computed_field
        def can_start(self) -> bool:
            """Check if app can be started."""
            return self.status == "stopped"

        @computed_field
        def can_stop(self) -> bool:
            """Check if app can be stopped."""
            return self.status == "running"

        @computed_field
        def can_restart(self) -> bool:
            """Check if app can be restarted."""
            return self.status in {"running", "stopped"}

        def validate_business_rules(self) -> FlextCore.Result[None]:
            """Enhanced business rules validation."""
            try:
                # Validate name field
                name = (self.name or "").strip()
                if not name:
                    return FlextCore.Result[None].fail("Application name is required")

                # Validate host field
                host = (self.host or "").strip()
                if not host:
                    return FlextCore.Result[None].fail("Host address is required")

                # Validate port range
                if not (
                    FlextWebConstants.WebServer.MIN_PORT
                    <= self.port
                    <= FlextWebConstants.WebServer.MAX_PORT
                ):
                    return FlextCore.Result[None].fail(
                        f"Port out of range: {self.port}"
                    )

                # Validate environment
                valid_environments = ["development", "staging", "production", "test"]
                if self.environment not in valid_environments:
                    return FlextCore.Result[None].fail(
                        f"Invalid environment: {self.environment}. Valid: {valid_environments}"
                    )

                # Validate health check URL if provided
                if self.health_check_url:
                    url_result = FlextCore.Models.Validation.validate_url(
                        self.health_check_url
                    )
                    if url_result.is_failure:
                        return FlextCore.Result[None].fail(
                            f"Invalid health check URL: {url_result.error}"
                        )

                return FlextCore.Result[None].ok(None)
            except Exception as e:
                return FlextCore.Result[None].fail(f"Validation failed: {e}")

        def start(self) -> FlextCore.Result[FlextWebModels.WebApp]:
            """Start application with enhanced state management."""
            if self.status == "running":
                return FlextCore.Result[FlextWebModels.WebApp].fail(
                    "App already running"
                )
            if self.status not in {"stopped", "error"}:
                return FlextCore.Result[FlextWebModels.WebApp].fail(
                    f"App cannot be started from status: {self.status}"
                )

            # Update status through string value
            self.status = "starting"
            self.update_timestamp()

            # Simulate startup process
            self.status = "running"
            self.update_timestamp()

            return FlextCore.Result[FlextWebModels.WebApp].ok(self)

        def stop(self) -> FlextCore.Result[FlextWebModels.WebApp]:
            """Stop application with enhanced state management."""
            if self.status != "running":
                return FlextCore.Result[FlextWebModels.WebApp].fail("App not running")

            # Update status through string value
            self.status = "stopping"
            self.update_timestamp()

            # Simulate shutdown process
            self.status = "stopped"
            self.update_timestamp()

            return FlextCore.Result[FlextWebModels.WebApp].ok(self)

        def restart(self) -> FlextCore.Result[FlextWebModels.WebApp]:
            """Restart application."""
            if not self.can_restart:
                return FlextCore.Result[FlextWebModels.WebApp].fail(
                    f"App cannot be restarted from status: {self.status}"
                )

            # Stop first
            stop_result = self.stop()
            if stop_result.is_failure:
                return stop_result

            # Start again
            return self.start()

        def update_metrics(self, metrics: FlextCore.Types.Dict) -> None:
            """Update application metrics."""
            self.metrics.update(metrics)
            self.update_timestamp()

        def get_health_status(self) -> FlextCore.Types.Dict:
            """Get comprehensive health status."""
            return {
                "status": self.status,
                "is_running": self.is_running,
                "is_healthy": self.is_healthy,
                "url": self.url,
                "version": self.version,
                "environment": self.environment,
                "health_check_url": self.health_check_url,
                "last_updated": self.updated_at.isoformat()
                if self.updated_at
                else None,
                "metrics": self.metrics,
            }

        def to_dict(self) -> FlextCore.Types.Dict:
            """Convert to dictionary with enhanced serialization."""
            return {
                "id": self.id,
                "name": self.name,
                "host": self.host,
                "port": self.port,
                "status": self.status,
                "version": self.version,
                "environment": self.environment,
                "health_check_url": self.health_check_url,
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "metrics": self.metrics,
            }

        @override
        def __str__(self) -> str:
            """String representation of the WebApp."""
            return f"{self.name} ({self.host}:{self.port}) [{self.status}]"

        @override
        def __repr__(self) -> str:
            """Detailed string representation."""
            return (
                f"WebApp(id='{self.id}', name='{self.name}', "
                f"host='{self.host}', port={self.port}, "
                f"status='{self.status}', version='{self.version}')"
            )

        def model_post_init(self, __context: object, /) -> None:
            """Post-init setup with enhanced initialization."""
            super().model_post_init(__context)
            # Initialize webapp-specific state
            if not self.metrics:
                self.metrics = {
                    "startup_time": "None",
                    "request_count": 0,
                    "error_count": 0,
                    "last_request": "None",
                }

    # Enhanced Web Request Models

    class HttpResponse(FlextCore.Models.Entity):
        """Base HTTP response model for web applications.

        Provides HTTP status code validation, success/error checking, and response
        metadata with comprehensive Pydantic 2.11 validation.

        This model serves as the foundation for WebResponse in flext-web,
        providing core HTTP response functionality with computed fields for
        status code classification.

        Attributes:
            status_code: HTTP status code (100-599)
            headers: HTTP response headers
            body: Response body (string, dict, or None)
            elapsed_time: Request/response elapsed time in seconds

        Computed Fields:
            is_success: True if status code is 2xx
            is_client_error: True if status code is 4xx
            is_server_error: True if status code is 5xx
            is_redirect: True if status code is 3xx
            is_informational: True if status code is 1xx

        Examples:
            >>> response = HttpResponse(
            ...     status_code=200,
            ...     headers={"Content-Type": "application/json"},
            ...     body={"result": "success"},
            ...     elapsed_time=0.123,
            ... )
            >>> response.is_success
            True
            >>> response.is_client_error
            False

        """

        status_code: Annotated[
            int,
            Field(
                ge=100,
                le=599,
                description="HTTP status code",
                examples=[200, 201, 400, 404, 500],
            ),
        ]
        headers: Annotated[
            dict[str, str],
            Field(
                default_factory=dict,
                description="HTTP response headers",
                examples=[
                    {"Content-Type": "application/json"},
                    {"Content-Type": "text/html", "Cache-Control": "no-cache"},
                ],
            ),
        ] = Field(default_factory=dict)
        body: Annotated[
            str | dict[str, object] | None,
            Field(
                default=None,
                description="Response body (string, dict, or None)",
                examples=["Success", {"result": "ok"}, None],
            ),
        ] = None
        elapsed_time: Annotated[
            float | None,
            Field(
                default=None,
                ge=0.0,
                description="Request/response elapsed time in seconds",
                examples=[0.123, 1.456, None],
            ),
        ] = None

        @computed_field
        @property
        def is_success(self) -> bool:
            """Check if response indicates success (2xx status codes).

            Returns:
                True if status code is in range 200-299

            Examples:
                >>> HttpResponse(status_code=200).is_success
                True
                >>> HttpResponse(status_code=404).is_success
                False

            """
            return (
                FlextWebConstants.HttpStatus.OK
                <= self.status_code
                <= FlextWebConstants.HttpStatus.SUCCESS_MAX
            )

        @computed_field
        @property
        def is_client_error(self) -> bool:
            """Check if response indicates client error (4xx status codes).

            Returns:
                True if status code is in range 400-499

            Examples:
                >>> HttpResponse(status_code=404).is_client_error
                True

            """
            return (
                FlextWebConstants.HttpStatus.BAD_REQUEST
                <= self.status_code
                <= FlextWebConstants.HttpStatus.CLIENT_ERROR_MAX
            )

        @computed_field
        @property
        def is_server_error(self) -> bool:
            """Check if response indicates server error (5xx status codes).

            Returns:
                True if status code is in range 500-599

            Examples:
                >>> HttpResponse(status_code=500).is_server_error
                True

            """
            return (
                FlextWebConstants.HttpStatus.INTERNAL_SERVER_ERROR
                <= self.status_code
                <= FlextWebConstants.HttpStatus.SERVER_ERROR_MAX
            )

        @computed_field
        @property
        def is_redirect(self) -> bool:
            """Check if response indicates redirect (3xx status codes).

            Returns:
                True if status code is in range 300-399

            Examples:
                >>> HttpResponse(status_code=301).is_redirect
                True

            """
            return (
                FlextWebConstants.HttpStatus.MULTIPLE_CHOICES
                <= self.status_code
                <= FlextWebConstants.HttpStatus.REDIRECTION_MAX
            )

        @computed_field
        @property
        def is_informational(self) -> bool:
            """Check if response is informational (1xx status codes).

            Returns:
                True if status code is in range 100-199

            Examples:
                >>> HttpResponse(status_code=100).is_informational
                True

            """
            return (
                FlextWebConstants.HttpStatus.CONTINUE
                <= self.status_code
                <= FlextWebConstants.HttpStatus.INFORMATIONAL_MAX
            )

        @field_validator("status_code")
        @classmethod
        def validate_status_code(cls, v: int) -> int:
            """Validate HTTP status code is in valid range."""
            if not (
                FlextWebConstants.HttpStatus.CONTINUE
                <= v
                <= FlextWebConstants.HttpStatus.SERVER_ERROR_MAX
            ):
                msg = (
                    f"Invalid HTTP status code: {v}. Must be between "
                    f"{FlextWebConstants.HttpStatus.CONTINUE} and "
                    f"{FlextWebConstants.HttpStatus.SERVER_ERROR_MAX}"
                )
                raise ValueError(msg)
            return v

        @model_validator(mode="after")
        def validate_response_consistency(self) -> Self:
            """Cross-field validation for HTTP response consistency."""
            # 204 No Content should not have a body
            if (
                self.status_code == FlextWebConstants.HttpStatus.NO_CONTENT
                and self.body is not None
            ):
                msg = "HTTP 204 No Content responses should not have a body"
                raise ValueError(msg)

            # Validate elapsed time
            if self.elapsed_time is not None and self.elapsed_time < 0:
                msg = "Elapsed time cannot be negative"
                raise ValueError(msg)

            return self

    class HttpRequest(FlextCore.Models.Command):
        """Base HTTP request model - foundation for web server requests.

        Shared HTTP request primitive for web server request handling.
        Provides common request validation, method checking, and URL validation.

        USAGE: Foundation for web server request handling
        EXTENDS: FlextCore.Models.Command (represents a request action/command)

        Usage example:
            from flext_web import FlextWebModels

            # Create HTTP request
            request = FlextWebModels.HttpRequest(
                url="https://api.example.com/users",
                method="GET",
                headers={"Authorization": "Bearer token"},
                timeout=30.0
            )

            # Validate method
            if request.method in {"GET", "HEAD", "OPTIONS"}:
                print("Safe HTTP method")
        """

        url: Annotated[
            str,
            Field(
                description="Request URL - can be absolute (http://example.com/api) or relative (/api/users)",
                examples=[
                    "https://api.example.com/users",
                    "/api/v1/users",
                    "http://localhost:8000/health",
                ],
            ),
        ]
        method: Annotated[
            str,
            Field(
                default="GET",
                description="HTTP method - automatically converted to uppercase",
                examples=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
            ),
        ]
        headers: Annotated[
            dict[str, str],
            Field(
                default_factory=dict,
                description="HTTP request headers - key-value pairs",
                examples=[
                    {
                        "Authorization": "Bearer token123",
                        "Content-Type": "application/json",
                    },
                    {"User-Agent": "FlextClient/1.0", "Accept": "application/json"},
                ],
            ),
        ]
        body: Annotated[
            str | dict[str, object] | None,
            Field(
                default=None,
                description="Request body - can be string, dict, or None",
                examples=[
                    '{"username": "john", "email": "john@example.com"}',
                    {"username": "john", "email": "john@example.com"},
                    None,
                ],
            ),
        ]
        timeout: Annotated[
            float,
            Field(
                default=30.0,
                ge=0.0,
                le=300.0,
                description="Request timeout in seconds - must be between 0 and 300",
                examples=[30.0, 60.0, 120.0],
            ),
        ]

        @computed_field
        @property
        def has_body(self) -> bool:
            """Check if request has a body."""
            return self.body is not None

        @computed_field
        @property
        def is_secure(self) -> bool:
            """Check if request uses HTTPS."""
            return self.url.startswith("https://")

        @field_validator("method")
        @classmethod
        def validate_method(cls, v: str) -> str:
            """Validate HTTP method using centralized constants."""
            method_upper = v.upper()
            valid_methods = {
                "GET",
                "POST",
                "PUT",
                "DELETE",
                "PATCH",
                "HEAD",
                "OPTIONS",
            }
            if method_upper not in valid_methods:
                error_msg = f"Invalid HTTP method: {v}. Valid methods: {valid_methods}"
                raise FlextCore.Exceptions.ValidationError(
                    error_msg,
                    field="method",
                    value=v,
                )
            return method_upper

        @field_validator("url")
        @classmethod
        def validate_url(cls, v: str) -> str:
            """Validate URL format using centralized validation."""
            if not v or not v.strip():
                error_msg = "URL cannot be empty"
                raise FlextCore.Exceptions.ValidationError(
                    error_msg,
                    field="url",
                    value=v,
                )

            # Allow relative URLs (starting with /)
            if v.strip().startswith("/"):
                return v.strip()

            # Validate absolute URLs with Pydantic 2 direct validation
            from urllib.parse import urlparse

            parsed = urlparse(v.strip())
            if not parsed.scheme or not parsed.netloc:
                error_msg = "URL must have scheme and domain"
                raise FlextCore.Exceptions.ValidationError(
                    error_msg, field="url", value=v
                )

            if parsed.scheme not in {"http", "https"}:
                error_msg = "URL must start with http:// or https://"
                raise FlextCore.Exceptions.ValidationError(
                    error_msg, field="url", value=v
                )

            return v.strip()

        @model_validator(mode="after")
        def validate_request_consistency(self) -> Self:
            """Cross-field validation for HTTP request consistency."""
            # Methods without body should not have a body
            methods_without_body = {
                "GET",
                "HEAD",
                "DELETE",
            }
            if self.method in methods_without_body and self.body is not None:
                error_msg = f"HTTP {self.method} requests should not have a body"
                raise FlextCore.Exceptions.ValidationError(
                    error_msg,
                    field="body",
                    metadata={
                        "validation_details": f"Method {self.method} should not have body"
                    },
                )

            # Methods with body should have Content-Type header
            if self.method in {"POST", "PUT", "PATCH"} and self.body:
                headers_lower = {k.lower(): v for k, v in self.headers.items()}
                if "content-type" not in headers_lower:
                    # Auto-add Content-Type based on body type
                    if isinstance(self.body, dict):
                        self.headers["Content-Type"] = "application/json"
                    else:
                        self.headers["Content-Type"] = "text/plain"

            return self

    class WebRequest(HttpRequest):
        """Enhanced web request model for web server requests.

        Extends HttpRequest with server-specific tracking fields for web applications.

        Inherits from HttpRequest:
            - url: Request URL
            - method: HTTP method (GET, POST, etc.)
            - headers: Request headers
            - body: Request body
            - timeout: Request timeout
            - has_body: Computed field
            - is_secure: Computed field
            - validate_method: Method validator
            - validate_url: URL validator
            - validate_request_consistency: Cross-field validator

        Adds server-specific fields:
            - request_id: Unique request identifier
            - query_params: Query parameters
            - client_ip: Client IP address
            - user_agent: User agent string
            - timestamp: Request timestamp
        """

        # SERVER-SPECIFIC fields for request tracking
        request_id: str = Field(
            default_factory=lambda: str(uuid.uuid4()),
            description="Unique request identifier",
        )
        query_params: dict[str, object] = Field(
            default_factory=dict,
            description="Query parameters",
        )
        client_ip: str | None = Field(
            default=None,
            description="Client IP address",
        )
        user_agent: str | None = Field(
            default=None,
            description="User agent string",
        )
        timestamp: datetime = Field(
            default_factory=lambda: datetime.now(UTC),
            description="Request timestamp",
        )

        @model_validator(mode="after")
        def validate_request_consistency_server_specific(self) -> Self:
            """SERVER-SPECIFIC model validator for additional web server requirements."""
            # Server-specific validation: require Content-Type for POST/PUT/PATCH
            if self.method.upper() in {"POST", "PUT", "PATCH"} and self.body:
                content_type = self.headers.get("Content-Type", "").lower()
                if not content_type:
                    msg = "Content-Type header required for requests with body"
                    raise ValueError(msg)

            return self

        @computed_field
        def is_safe_method(self) -> bool:
            """Check if HTTP method is safe (GET, HEAD, OPTIONS) - SERVER SPECIFIC."""
            return self.method.upper() in {"GET", "HEAD", "OPTIONS"}

        @computed_field
        def is_idempotent(self) -> bool:
            """Check if HTTP method is idempotent - SERVER SPECIFIC."""
            return self.method.upper() in {"GET", "HEAD", "PUT", "DELETE", "OPTIONS"}

    class WebResponse(HttpResponse):
        """Enhanced web response model extending HttpResponse base.

        Inherits from HttpResponse:
            - status_code: HTTP status code
            - headers: Response headers
            - body: Response body
            - elapsed_time: Request/response elapsed time
            - is_success: Computed field - check if response is successful (2xx)
            - is_client_error: Computed field - check if response is client error (4xx)
            - is_server_error: Computed field - check if response is server error (5xx)
            - is_redirect: Computed field - check if response is redirect (3xx)
            - is_informational: Computed field - check if response is informational (1xx)

        Server-specific additions:
            - response_id: Unique response identifier
            - request_id: Associated request identifier
            - content_type: Content type
            - content_length: Content length in bytes
            - processing_time_ms: Processing time in milliseconds
            - timestamp: Response timestamp
        """

        # SERVER-SPECIFIC fields for response tracking
        response_id: str = Field(
            default_factory=lambda: str(uuid.uuid4()),
            description="Unique response identifier",
        )
        request_id: str = Field(
            description="Associated request identifier",
        )
        content_type: str | None = Field(
            default=None,
            description="Content type",
        )
        content_length: int = Field(
            default=0,
            ge=0,
            description="Content length in bytes",
        )
        processing_time_ms: float = Field(
            default=0.0,
            ge=0.0,
            description="Processing time in milliseconds",
        )
        timestamp: datetime = Field(
            default_factory=lambda: datetime.now(UTC),
            description="Response timestamp",
        )

        @model_validator(mode="after")
        def validate_response_consistency(self) -> Self:
            """Model validator for response consistency."""
            # Validate content type and body consistency
            if self.body and not self.content_type:
                msg = "Content-Type must be specified when body is present"
                raise ValueError(msg)

            # Validate content length consistency
            if self.body and self.content_length == 0:
                if isinstance(self.body, str):
                    self.content_length = len(self.body.encode("utf-8"))
                elif isinstance(self.body, dict):
                    # For dict bodies, calculate length as if JSON serialized
                    self.content_length = len(json.dumps(self.body).encode("utf-8"))
                else:
                    # For other types, convert to string
                    self.content_length = len(str(self.body).encode("utf-8"))
            elif not self.body and self.content_length > 0:
                msg = "Content-Length should be 0 when no body is present"
                raise ValueError(msg)

            return self

        # SERVER-SPECIFIC computed field (processing_time_seconds)
        # Inherited from base: is_success, is_client_error, is_server_error, validate_status_code
        @computed_field
        def processing_time_seconds(self) -> float:
            """Get processing time in seconds - SERVER SPECIFIC."""
            return self.processing_time_ms / 1000.0

    # Enhanced Web Application Configuration Models
    class WebAppConfig(_BaseWebModel):
        """Enhanced web application configuration model."""

        app_name: str = Field(
            default="FLEXT Web Application",
            min_length=1,
            max_length=255,
            description="Application name",
        )
        host: str = Field(
            default=FlextWebConstants.WebServer.DEFAULT_HOST,
            min_length=1,
            max_length=255,
            description="Host address",
        )
        port: int = Field(
            default=FlextWebConstants.WebServer.DEFAULT_PORT,
            ge=FlextWebConstants.WebServer.MIN_PORT,
            le=FlextWebConstants.WebServer.MAX_PORT,
            description="Port number",
        )
        debug: bool = Field(
            default=False,
            description="Debug mode",
        )
        secret_key: str = Field(
            description="Secret key for sessions",
            min_length=FlextCore.Constants.Validation.MIN_SECRET_KEY_LENGTH,
        )
        max_content_length: int = Field(
            default=FlextCore.Constants.Limits.MAX_FILE_SIZE,
            gt=0,
            description="Maximum content length",
        )
        request_timeout: int = Field(
            default=FlextCore.Constants.Network.DEFAULT_TIMEOUT,
            gt=0,
            description="Request timeout in seconds",
        )
        enable_cors: bool = Field(
            default=False,
            description="Enable CORS",
        )
        cors_origins: FlextCore.Types.StringList = Field(
            default_factory=list,
            description="CORS allowed origins",
        )
        ssl_enabled: bool = Field(
            default=False,
            description="Enable SSL/TLS",
        )
        ssl_cert_path: str | None = Field(
            default=None,
            description="SSL certificate path",
        )
        ssl_key_path: str | None = Field(
            default=None,
            description="SSL private key path",
        )

        @model_validator(mode="after")
        def validate_web_app_config_consistency(self) -> Self:
            """Model validator for web application configuration consistency."""
            # Validate SSL configuration consistency
            if self.ssl_enabled:
                if not self.ssl_cert_path or not self.ssl_key_path:
                    msg = "SSL certificate and key paths required when SSL is enabled"
                    raise ValueError(msg)

                # Validate file paths exist
                if not Path(self.ssl_cert_path).exists():
                    msg = f"SSL certificate file not found: {self.ssl_cert_path}"
                    raise ValueError(msg)

                if not Path(self.ssl_key_path).exists():
                    msg = f"SSL key file not found: {self.ssl_key_path}"
                    raise ValueError(msg)

            # Validate CORS configuration
            if self.enable_cors and not self.cors_origins:
                msg = "CORS origins must be specified when CORS is enabled"
                raise ValueError(msg)

            # Validate debug mode restrictions
            if self.debug and self.ssl_enabled:
                msg = "Debug mode should not be enabled with SSL in production"
                raise ValueError(msg)

            return self

        @field_validator("cors_origins")
        @classmethod
        def validate_cors_origins(
            cls, v: FlextCore.Types.StringList
        ) -> FlextCore.Types.StringList:
            """Validate CORS origins with comprehensive URL validation."""
            if not v:
                return []

            validated_origins: FlextCore.Types.StringList = []
            for origin in v:
                if origin == "*":
                    validated_origins.append(origin)
                else:
                    result = FlextCore.Models.Validation.validate_url(origin)
                    if result.is_failure:
                        error_msg = f"Invalid CORS origin: {origin}"
                        raise ValueError(error_msg)
                    validated_origins.append(result.unwrap())
            return validated_origins

        @model_validator(mode="after")
        def validate_ssl_config(self) -> Self:
            """Validate SSL configuration."""
            if self.ssl_enabled:
                if not self.ssl_cert_path or not self.ssl_key_path:
                    msg = (
                        "SSL certificate and key paths are required when SSL is enabled"
                    )
                    raise ValueError(msg)

                # Validate file paths exist
                if not Path(self.ssl_cert_path).exists():
                    msg = f"SSL certificate file not found: {self.ssl_cert_path}"
                    raise ValueError(msg)

                if not Path(self.ssl_key_path).exists():
                    msg = f"SSL key file not found: {self.ssl_key_path}"
                    raise ValueError(msg)

            return self

        @computed_field
        def protocol(self) -> str:
            """Get protocol based on SSL configuration."""
            return "https" if self.ssl_enabled else "http"

        @computed_field
        def base_url(self) -> str:
            """Get base URL."""
            return f"{self.protocol}://{self.host}:{self.port}"

    class AppConfig(_BaseWebModel):
        """FastAPI application configuration model.

        Simplified configuration for FastAPI application creation via create_fastapi_app().
        For more comprehensive web configuration, use WebAppConfig.

        Example:
            >>> from flext_web.models import FlextWebModels
            >>> config = FlextWebModels.AppConfig(
            ...     title="My API", version="1.0.0", description="Enterprise API"
            ... )

        """

        title: str = Field(
            default="FlextWeb API",
            min_length=1,
            max_length=255,
            description="Application title",
        )
        version: str = Field(
            default="1.0.0",
            min_length=1,
            max_length=50,
            description="Application version",
        )
        description: str = Field(
            default="FlextWeb FastAPI Application",
            min_length=1,
            max_length=1000,
            description="Application description",
        )
        docs_url: str = Field(
            default="/docs",
            description="Documentation URL",
        )
        redoc_url: str = Field(
            default="/redoc",
            description="ReDoc URL",
        )
        openapi_url: str = Field(
            default="/openapi.json",
            description="OpenAPI JSON URL",
        )
        middlewares: FlextCore.Types.List = Field(
            default_factory=list,
            description="Middleware instances (e.g., from flext-auth)",
        )

    @classmethod
    def create_web_app(
        cls,
        data: FlextWebTypes.AppData,
    ) -> FlextCore.Result[FlextWebModels.WebApp]:
        """Enhanced web application creation with comprehensive validation."""
        try:
            app_data: FlextCore.Types.Dict = dict(data)

            # Ensure required fields
            if "id" not in app_data:
                app_data["id"] = f"app_{uuid.uuid4().hex[:8]}"

            if "status" not in app_data:
                app_data["status"] = "stopped"

            # Validate and convert port
            port = app_data.get("port", FlextWebConstants.WebServer.DEFAULT_PORT)
            if isinstance(port, str) and port.isdigit():
                app_data["port"] = int(port)
            elif not isinstance(port, int):
                return FlextCore.Result[FlextWebModels.WebApp].fail(
                    f"Invalid port type: {type(port)}"
                )

            # Create app with validated data
            port_value = app_data["port"]
            if not isinstance(port_value, int):
                return FlextCore.Result[FlextWebModels.WebApp].fail(
                    f"Port validation failed: expected int, got {type(port_value)}"
                )

            # Status is now a string field
            status = str(app_data["status"])

            # Convert health_check_url properly
            health_check_url = app_data.get("health_check_url")
            health_check_url_str = (
                str(health_check_url) if health_check_url is not None else None
            )

            app = FlextWebModels.WebApp(
                id=str(app_data["id"]),
                name=str(app_data["name"]),
                host=str(app_data["host"]),
                port=port_value,
                status=status,
                version=int(
                    str(
                        app_data.get(
                            "version", FlextCore.Constants.Performance.DEFAULT_VERSION
                        )
                    )
                ),
                environment=str(app_data.get("environment", "development")),
                health_check_url=health_check_url_str,
            )

            # Validate business rules
            validation_result = app.validate_business_rules()
            if validation_result.is_failure:
                return FlextCore.Result[FlextWebModels.WebApp].fail(
                    validation_result.error or "Validation failed"
                )

            return FlextCore.Result[FlextWebModels.WebApp].ok(app)

        except Exception as e:
            return FlextCore.Result[FlextWebModels.WebApp].fail(
                f"App creation failed: {e}"
            )

    @classmethod
    def create_web_request(
        cls,
        method: str,
        url: str,
        **kwargs: str | int | FlextCore.Types.StringDict | None,
    ) -> FlextCore.Result[FlextWebModels.WebRequest]:
        """Create web request with validation."""
        try:
            # Extract and type-cast parameters
            headers = kwargs.get("headers", {})
            if not isinstance(headers, dict):
                headers = {}

            query_params = kwargs.get("query_params", {})
            if not isinstance(query_params, dict):
                query_params = {}
            # Convert to proper type for FlextCore.Types.Dict
            query_params = dict(query_params.items())

            body = kwargs.get("body")
            # Convert body to proper type for WebRequest
            if body is not None and not isinstance(body, (str, dict)):
                body = str(body)
            elif isinstance(body, dict):
                # Convert dict[str, str] to FlextCore.Types.Dict
                body = dict(body.items())
            timeout_raw = kwargs.get("timeout", 30)
            timeout = 30.0
            if timeout_raw is not None and isinstance(timeout_raw, (int, float, str)):
                try:
                    timeout = float(timeout_raw)
                except (ValueError, TypeError):
                    timeout = 30.0
                # For other types (like dict), keep default timeout

            request = FlextWebModels.WebRequest(
                method=method,
                url=url,
                headers=headers,
                query_params=query_params,
                body=body,
                timeout=timeout,
            )
            return FlextCore.Result[FlextWebModels.WebRequest].ok(request)
        except Exception as e:
            return FlextCore.Result[FlextWebModels.WebRequest].fail(
                f"Failed to create web request: {e}"
            )

    @classmethod
    def create_web_response(
        cls,
        request_id: str,
        status_code: int,
        **kwargs: str | int | FlextCore.Types.StringDict | None,
    ) -> FlextCore.Result[FlextWebModels.WebResponse]:
        """Create web response with validation."""
        try:
            # Extract and type-cast parameters
            headers = kwargs.get("headers", {})
            if not isinstance(headers, dict):
                headers = {}

            body = kwargs.get("body")
            # Convert body to proper type for WebResponse
            if body is not None and not isinstance(body, (str, dict)):
                body = str(body)
            elif isinstance(body, dict):
                # Convert dict[str, str] to FlextCore.Types.Dict
                body = dict(body.items())
            elapsed_time_raw = kwargs.get("elapsed_time", 0.0)
            elapsed_time = 0.0
            if elapsed_time_raw is not None and isinstance(
                elapsed_time_raw, (int, float, str)
            ):
                try:
                    elapsed_time = float(elapsed_time_raw)
                except (ValueError, TypeError):
                    elapsed_time = 0.0

            response = FlextWebModels.WebResponse(
                request_id=request_id,
                status_code=status_code,
                headers=headers,
                body=body,
                elapsed_time=elapsed_time,
            )
            return FlextCore.Result[FlextWebModels.WebResponse].ok(response)
        except Exception as e:
            return FlextCore.Result[FlextWebModels.WebResponse].fail(
                f"Failed to create web response: {e}"
            )


__all__ = ["FlextWebModels"]

# Rebuild models for Pydantic v2 forward references
# Note: Rebuild in correct order - base classes first, then derived classes
try:
    FlextWebModels.HttpRequest.model_rebuild()
    FlextWebModels.HttpResponse.model_rebuild()
    FlextWebModels.WebRequest.model_rebuild()
    FlextWebModels.WebResponse.model_rebuild()
except Exception as e:
    # If rebuild fails, models can still be used
    import warnings

    warnings.warn(f"Model rebuild failed: {e}", stacklevel=2)
