"""FLEXT Web Models.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
import uuid
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Self, override

from flext_core import (
    FlextConstants,
    FlextModels,
    FlextResult,
    FlextTypes,
)
from pydantic import (
    ConfigDict,
    Field,
    computed_field,
    field_validator,
    model_validator,
)

from flext_web.constants import FlextWebConstants
from flext_web.typings import FlextWebTypes


class FlextWebModels(FlextModels):
    """Enhanced FLEXT web model system with FlextMixins integration.

    Inherits from FlextModels to avoid duplication and ensure consistency
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
    class _BaseWebModel(FlextModels.ArbitraryTypesModel):
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
        def model_metadata(self) -> FlextTypes.Dict:
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

    class WebApp(FlextModels.Entity):
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
        status: FlextWebModels.WebAppStatus = Field(
            default="stopped",  # type: ignore[assignment]
            description="Current status of the web application",
        )
        version: int = Field(
            default=1,
            description="Application version",
        )
        environment: str = Field(
            default="development",
            description="Deployment environment",
        )
        health_check_url: str | None = Field(
            default=None,
            description="Health check endpoint URL",
        )
        debug_mode: bool = Field(
            default=False,
            description="Debug mode flag",
        )
        metrics: FlextTypes.Dict = Field(
            default_factory=dict,
            description="Application metrics",
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
        def validate_status(cls, v: object) -> FlextWebModels.WebAppStatus:
            """Validate status field with enhanced error handling."""
            # Handle enum values directly
            if isinstance(v, FlextWebModels.WebAppStatus):
                return v

            # Handle string values
            if isinstance(v, str):
                # Use the actual enum
                try:
                    return FlextWebModels.WebAppStatus(v)
                except ValueError as e:
                    valid_values = [
                        status.value for status in FlextWebModels.WebAppStatus
                    ]
                    msg = f"Invalid status: {v}. Valid values: {valid_values}"
                    raise ValueError(msg) from e

            type_name = type(v).__name__
            msg = f"Invalid status type: {type_name}. Must be str or FlextWebModels.WebAppStatus"
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
            result = FlextModels.Validation.validate_hostname(host)
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
            result = FlextModels.Validation.validate_url(url)
            if result.is_failure:
                raise ValueError(result.error)

            return url

        @computed_field
        def is_running(self) -> bool:
            """Check if app is running."""
            return self.status == FlextWebModels.WebAppStatus.RUNNING

        @computed_field
        def is_healthy(self) -> bool:
            """Check if app is healthy (running state)."""
            return self.status == FlextWebModels.WebAppStatus.RUNNING

        @computed_field
        def url(self) -> str:
            """Get app URL with proper protocol detection."""
            # Standard HTTPS ports
            https_ports = {
                FlextConstants.Http.HTTPS_PORT,
                FlextConstants.Http.HTTPS_ALT_PORT,
            }
            protocol = "https" if self.port in https_ports else "http"
            return f"{protocol}://{self.host}:{self.port}"

        @computed_field
        def can_start(self) -> bool:
            """Check if app can be started."""
            return self.status == FlextWebModels.WebAppStatus.STOPPED

        @computed_field
        def can_stop(self) -> bool:
            """Check if app can be stopped."""
            return self.status == FlextWebModels.WebAppStatus.RUNNING

        @computed_field
        def can_restart(self) -> bool:
            """Check if app can be restarted."""
            return self.status in {
                FlextWebModels.WebAppStatus.RUNNING,
                FlextWebModels.WebAppStatus.STOPPED,
            }

        def validate_business_rules(self) -> FlextResult[None]:
            """Enhanced business rules validation."""
            try:
                # Validate name field
                name = (self.name or "").strip()
                if not name:
                    return FlextResult[None].fail("Application name is required")

                # Validate host field
                host = (self.host or "").strip()
                if not host:
                    return FlextResult[None].fail("Host address is required")

                # Validate port range
                if not (
                    FlextWebConstants.WebServer.MIN_PORT
                    <= self.port
                    <= FlextWebConstants.WebServer.MAX_PORT
                ):
                    return FlextResult[None].fail(f"Port out of range: {self.port}")

                # Validate environment
                valid_environments = ["development", "staging", "production", "test"]
                if self.environment not in valid_environments:
                    return FlextResult[None].fail(
                        f"Invalid environment: {self.environment}. Valid: {valid_environments}"
                    )

                # Validate health check URL if provided
                if self.health_check_url:
                    url_result = FlextModels.Validation.validate_url(
                        self.health_check_url
                    )
                    if url_result.is_failure:
                        return FlextResult[None].fail(
                            f"Invalid health check URL: {url_result.error}"
                        )

                return FlextResult[None].ok(None)
            except Exception as e:
                return FlextResult[None].fail(f"Validation failed: {e}")

        def start(self) -> FlextResult[FlextWebModels.WebApp]:
            """Start application with enhanced state management."""
            if self.status == FlextWebModels.WebAppStatus.RUNNING:
                return FlextResult[FlextWebModels.WebApp].fail("App already running")
            if self.status not in {
                FlextWebModels.WebAppStatus.STOPPED,
                FlextWebModels.WebAppStatus.ERROR,
            }:
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"App cannot be started from status: {self.status}"
                )

            # Update status through enum value
            self.status = FlextWebModels.WebAppStatus.STARTING
            self.update_timestamp()

            # Simulate startup process
            self.status = FlextWebModels.WebAppStatus.RUNNING
            self.update_timestamp()

            return FlextResult[FlextWebModels.WebApp].ok(self)

        def stop(self) -> FlextResult[FlextWebModels.WebApp]:
            """Stop application with enhanced state management."""
            if self.status != FlextWebModels.WebAppStatus.RUNNING:
                return FlextResult[FlextWebModels.WebApp].fail("App not running")

            # Update status through enum value
            self.status = FlextWebModels.WebAppStatus.STOPPING
            self.update_timestamp()

            # Simulate shutdown process
            self.status = FlextWebModels.WebAppStatus.STOPPED
            self.update_timestamp()

            return FlextResult[FlextWebModels.WebApp].ok(self)

        def restart(self) -> FlextResult[FlextWebModels.WebApp]:
            """Restart application."""
            if not self.can_restart:
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"App cannot be restarted from status: {self.status}"
                )

            # Stop first
            stop_result = self.stop()
            if stop_result.is_failure:
                return stop_result

            # Start again
            return self.start()

        def update_metrics(self, metrics: FlextTypes.Dict) -> None:
            """Update application metrics."""
            self.metrics.update(metrics)
            self.update_timestamp()

        def get_health_status(self) -> FlextTypes.Dict:
            """Get comprehensive health status."""
            return {
                "status": self.status.value,
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

        def to_dict(self) -> FlextTypes.Dict:
            """Convert to dictionary with enhanced serialization."""
            return {
                "id": self.id,
                "name": self.name,
                "host": self.host,
                "port": self.port,
                "status": self.status.value,
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
            return f"{self.name} ({self.host}:{self.port}) [{self.status.value}]"

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
    class WebRequest(FlextModels.HttpRequest):
        """Enhanced web request model extending flext-core HttpRequest base.

        Inherits from flext-core:
            - url: Request URL
            - method: HTTP method (GET, POST, etc.)
            - headers: Request headers
            - body: Request body
            - timeout: Request timeout
            - has_body: Computed field - check if request has body
            - is_secure: Computed field - check if request uses HTTPS
            - validate_method: Validates HTTP method against centralized constants
            - validate_request_consistency: Cross-field validation

        Server-specific additions:
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
        query_params: FlextTypes.Dict = Field(
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

    class WebResponse(FlextModels.HttpResponse):
        """Enhanced web response model extending flext-core HttpResponse base.

        Inherits from flext-core:
            - status_code: HTTP status code
            - headers: Response headers
            - body: Response body
            - elapsed_time: Request/response elapsed time
            - is_success: Computed field - check if response is successful (2xx)
            - is_client_error: Computed field - check if response is client error (4xx)
            - is_server_error: Computed field - check if response is server error (5xx)

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
                    import json

                    self.content_length = len(json.dumps(self.body).encode("utf-8"))
                else:
                    # For other types, convert to string
                    self.content_length = len(str(self.body).encode("utf-8"))
            elif not self.body and self.content_length > 0:
                msg = "Content-Length should be 0 when no body is present"
                raise ValueError(msg)

            return self

        def _get_status_category(self) -> str:
            """Get HTTP status code category - SERVER SPECIFIC."""
            if (
                FlextConstants.Http.HTTP_INFORMATIONAL_MIN
                <= self.status_code
                <= FlextConstants.Http.HTTP_INFORMATIONAL_MAX
            ):
                return "informational"
            if (
                FlextConstants.Http.HTTP_SUCCESS_MIN
                <= self.status_code
                <= FlextConstants.Http.HTTP_SUCCESS_MAX
            ):
                return "success"
            if (
                FlextConstants.Http.HTTP_REDIRECTION_MIN
                <= self.status_code
                <= FlextConstants.Http.HTTP_REDIRECTION_MAX
            ):
                return "redirection"
            if (
                FlextConstants.Http.HTTP_CLIENT_ERROR_MIN
                <= self.status_code
                <= FlextConstants.Http.HTTP_CLIENT_ERROR_MAX
            ):
                return "client_error"
            if (
                FlextConstants.Http.HTTP_SERVER_ERROR_MIN
                <= self.status_code
                <= FlextConstants.Http.HTTP_SERVER_ERROR_MAX
            ):
                return "server_error"
            return "unknown"

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
            min_length=FlextConstants.Validation.MIN_SECRET_KEY_LENGTH,
        )
        max_content_length: int = Field(
            default=FlextConstants.Limits.MAX_FILE_SIZE,
            gt=0,
            description="Maximum content length",
        )
        request_timeout: int = Field(
            default=FlextConstants.Network.DEFAULT_TIMEOUT,
            gt=0,
            description="Request timeout in seconds",
        )
        enable_cors: bool = Field(
            default=False,
            description="Enable CORS",
        )
        cors_origins: FlextTypes.StringList = Field(
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
            cls, v: FlextTypes.StringList
        ) -> FlextTypes.StringList:
            """Validate CORS origins with comprehensive URL validation."""
            if not v:
                return []

            validated_origins: FlextTypes.StringList = []
            for origin in v:
                if origin == "*":
                    validated_origins.append(origin)
                else:
                    result = FlextModels.Validation.validate_url(origin)
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
        middlewares: FlextTypes.List = Field(
            default_factory=list,
            description="Middleware instances (e.g., from flext-auth)",
        )

    @classmethod
    def create_web_app(
        cls,
        data: FlextWebTypes.AppData,
    ) -> FlextResult[FlextWebModels.WebApp]:
        """Enhanced web application creation with comprehensive validation."""
        try:
            app_data: FlextTypes.Dict = dict(data)

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
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"Invalid port type: {type(port)}"
                )

            # Create app with validated data
            port_value = app_data["port"]
            if not isinstance(port_value, int):
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"Port validation failed: expected int, got {type(port_value)}"
                )

            # Convert status to enum
            status_str = str(app_data["status"])
            status = FlextWebModels.WebAppStatus(status_str)

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
                            "version", FlextConstants.Performance.DEFAULT_VERSION
                        )
                    )
                ),
                environment=str(
                    app_data.get("environment", FlextConstants.Defaults.ENVIRONMENT)
                ),
                health_check_url=health_check_url_str,
            )

            # Validate business rules
            validation_result = app.validate_business_rules()
            if validation_result.is_failure:
                return FlextResult[FlextWebModels.WebApp].fail(
                    validation_result.error or "Validation failed"
                )

            return FlextResult[FlextWebModels.WebApp].ok(app)

        except Exception as e:
            return FlextResult[FlextWebModels.WebApp].fail(f"App creation failed: {e}")

    @classmethod
    def create_web_request(
        cls,
        method: str,
        url: str,
        **kwargs: str | int | FlextTypes.StringDict | None,
    ) -> FlextResult[FlextWebModels.WebRequest]:
        """Create web request with validation."""
        try:
            # Extract and type-cast parameters
            headers = kwargs.get("headers", {})
            if not isinstance(headers, dict):
                headers = {}

            query_params = kwargs.get("query_params", {})
            if not isinstance(query_params, dict):
                query_params = {}
            # Convert to proper type for FlextTypes.Dict
            query_params = dict(query_params.items())  # type: ignore[arg-type]

            body = kwargs.get("body")
            # Convert body to proper type for WebRequest
            if body is not None and not isinstance(body, (str, dict)):
                body = str(body)  # type: ignore[assignment]
            elif isinstance(body, dict):
                # Convert dict[str, str] to dict[str, object]
                body = dict(body.items())  # type: ignore[assignment]
            timeout_raw = kwargs.get("timeout", 30)
            timeout = 30.0
            if timeout_raw is not None:
                try:
                    timeout = float(timeout_raw)  # type: ignore[arg-type]
                except (ValueError, TypeError):
                    timeout = 30.0

            request = FlextWebModels.WebRequest(
                method=method,
                url=url,
                headers=headers,
                query_params=query_params,  # type: ignore[arg-type]
                body=body,  # type: ignore[arg-type]
                timeout=timeout,
            )
            return FlextResult[FlextWebModels.WebRequest].ok(request)
        except Exception as e:
            return FlextResult[FlextWebModels.WebRequest].fail(
                f"Failed to create web request: {e}"
            )

    @classmethod
    def create_web_response(
        cls,
        request_id: str,
        status_code: int,
        **kwargs: str | int | FlextTypes.StringDict | None,
    ) -> FlextResult[FlextWebModels.WebResponse]:
        """Create web response with validation."""
        try:
            # Extract and type-cast parameters
            headers = kwargs.get("headers", {})
            if not isinstance(headers, dict):
                headers = {}

            body = kwargs.get("body")
            # Convert body to proper type for WebResponse
            if body is not None and not isinstance(body, (str, dict)):
                body = str(body)  # type: ignore[assignment]
            elif isinstance(body, dict):
                # Convert dict[str, str] to dict[str, object]
                body = dict(body.items())  # type: ignore[assignment]
            elapsed_time_raw = kwargs.get("elapsed_time", 0.0)
            elapsed_time = 0.0
            if elapsed_time_raw is not None:
                try:
                    elapsed_time = float(elapsed_time_raw)  # type: ignore[arg-type]
                except (ValueError, TypeError):
                    elapsed_time = 0.0

            response = FlextWebModels.WebResponse(
                request_id=request_id,
                status_code=status_code,
                headers=headers,
                body=body,  # type: ignore[arg-type]
                elapsed_time=elapsed_time,
            )
            return FlextResult[FlextWebModels.WebResponse].ok(response)
        except Exception as e:
            return FlextResult[FlextWebModels.WebResponse].fail(
                f"Failed to create web response: {e}"
            )


__all__ = ["FlextWebModels"]
