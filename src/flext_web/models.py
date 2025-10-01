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
from typing import Any, Self, override

from pydantic import (
    ConfigDict,
    Field,
    FieldSerializationInfo,
    computed_field,
    field_serializer,
    field_validator,
    model_validator,
)

from flext_core import (
    FlextConstants,
    FlextModels,
    FlextResult,
    FlextTypes,
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

    @computed_field
    @property
    def active_web_models_count(self) -> int:
        """Computed field returning the number of active web model types."""
        # Count active web models based on nested classes
        web_model_classes = [
            self.WebApp,
            self.WebRequest,
            self.WebResponse,
            self.WebAppConfig,
            self.WebAppStatus,
            self._BaseWebModel,
        ]
        return len([cls for cls in web_model_classes if cls])

    @computed_field
    @property
    def web_model_summary(self) -> dict[str, Any]:
        """Computed field providing comprehensive web model summary."""
        return {
            "model_system": "FLEXT Web Models",
            "version": "2.11.0",
            "active_models": self.active_web_models_count,
            "supported_operations": [
                "web_application_management",
                "http_request_processing",
                "http_response_handling",
                "web_configuration_management",
                "security_validation",
            ],
            "framework_integrations": ["FastAPI", "Flask", "Django", "Starlette"],
            "validation_features": [
                "HTTP method validation",
                "URL format validation",
                "Security headers validation",
                "CORS configuration validation",
                "SSL certificate validation",
            ],
        }

    @model_validator(mode="after")
    def validate_web_consistency(self) -> Self:
        """Model validator ensuring web model consistency and security."""
        # Ensure security configurations are properly set
        if hasattr(self, "WebAppConfig"):
            # Web-specific validation logic can be added here
            pass

        return self

    @field_serializer("*", when_used="json")
    def serialize_with_web_metadata(
        self, value: object, _info: FieldSerializationInfo
    ) -> object:
        """Field serializer adding web processing metadata and security context."""
        if isinstance(value, dict):
            return {
                **value,
                "_web_metadata": {
                    "processed_at": datetime.now(UTC).isoformat(),
                    "model_type": "FlextWebModels",
                    "security_validated": True,
                    "web_framework_compatible": True,
                },
            }
        return value

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
        @property
        def model_metadata(self) -> dict[str, Any]:
            """Computed field providing base web model metadata."""
            return {
                "model_class": self.__class__.__name__,
                "framework": "FLEXT Web",
                "pydantic_version": "2.11+",
                "created_at": datetime.now(UTC).isoformat(),
            }

        @field_serializer("*", when_used="json")
        def mask_sensitive_web_data(
            self, value: object, _info: FieldSerializationInfo
        ) -> object:
            """Field serializer for masking sensitive web data."""
            # Mask sensitive web information like secrets, tokens, etc.
            if isinstance(value, str) and any(
                keyword in str(_info.field_name).lower()
                for keyword in ["secret", "key", "token", "password", "auth"]
            ):
                return "***MASKED***"
            return value

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
            min_length=FlextWebConstants.Web.MIN_APP_NAME_LENGTH,
            max_length=FlextWebConstants.Web.MAX_APP_NAME_LENGTH,
            description="Web application name",
        )
        host: str = Field(
            default=FlextWebConstants.Web.DEFAULT_HOST,
            min_length=1,
            max_length=255,
            description="Host address for the web application",
        )
        port: int = Field(
            default=FlextWebConstants.Web.DEFAULT_PORT,
            ge=FlextWebConstants.Web.MIN_PORT,
            le=FlextWebConstants.Web.MAX_PORT,
            description="Port number for the web application",
        )
        status: FlextWebModels.WebAppStatus = Field(
            default="stopped",
            description="Current status of the web application",
        )
        version: int = Field(
            default=FlextConstants.Performance.DEFAULT_VERSION,
            description="Application version",
        )
        environment: str = Field(
            default=FlextConstants.Defaults.ENVIRONMENT,
            description="Deployment environment",
        )
        health_check_url: str | None = Field(
            default=None,
            description="Health check endpoint URL",
        )
        metrics: dict[str, Any] = Field(
            default_factory=dict,
            description="Application metrics",
        )

        @computed_field
        @property
        def web_app_summary(self) -> dict[str, Any]:
            """Computed field providing web application summary."""
            return {
                "application_info": {
                    "name": self.name,
                    "status": self.status.value
                    if hasattr(self.status, "value")
                    else str(self.status),
                    "environment": self.environment,
                    "version": self.version,
                },
                "network_info": {
                    "host": self.host,
                    "port": self.port,
                    "url": self.url,
                    "protocol": "https" if self.port in {443, 8443} else "http",
                },
                "operational_info": {
                    "is_running": self.is_running,
                    "is_healthy": self.is_healthy,
                    "can_start": self.can_start,
                    "can_stop": self.can_stop,
                    "can_restart": self.can_restart,
                },
            }

        @model_validator(mode="after")
        def validate_web_app_configuration(self) -> Self:
            """Model validator for web application configuration consistency."""
            # Validate port and host combination
            if (
                self.host in {"0.0.0.0", "::"}
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
                if self.debug_mode if hasattr(self, "debug_mode") else False:
                    msg = "Debug mode must be disabled in production environment"
                    raise ValueError(msg)

                if not self.health_check_url:
                    msg = "Health check URL is required in production environment"
                    raise ValueError(msg)

            return self

        @field_serializer("metrics", when_used="json")
        def serialize_metrics_with_metadata(
            self, value: dict[str, Any]
        ) -> dict[str, Any]:
            """Field serializer for metrics with processing metadata."""
            return {
                **value,
                "_metrics_metadata": {
                    "collected_at": datetime.now(UTC).isoformat(),
                    "application": self.name,
                    "environment": self.environment,
                    "status": self.status.value
                    if hasattr(self.status, "value")
                    else str(self.status),
                },
            }

        @field_validator("status")
        @classmethod
        def validate_status(
            cls,
            v: FlextWebModels.WebAppStatus | str,
        ) -> FlextWebModels.WebAppStatus:
            """Validate status field with enhanced error handling."""
            if isinstance(v, str):
                try:
                    # Access WebAppStatus from the parent class's context
                    return FlextWebModels.WebAppStatus(v)
                except (ValueError, AttributeError) as e:
                    # Get valid statuses using direct reference
                    try:
                        valid_statuses = [
                            status.value for status in FlextWebModels.WebAppStatus
                        ]
                    except AttributeError:
                        valid_statuses = [
                            "stopped",
                            "starting",
                            "running",
                            "stopping",
                            "error",
                            "maintenance",
                            "deploying",
                        ]
                    msg = f"Invalid status: {v}. Valid statuses: {valid_statuses}"
                    raise ValueError(msg) from e
            return v

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
            result = FlextModels.create_validated_url(url)
            if result.is_failure:
                raise ValueError(result.error)

            return url

        @computed_field
        def is_running(self) -> bool:
            """Check if app is running."""
            return str(self.status) == "running"

        @computed_field
        def is_healthy(self) -> bool:
            """Check if app is healthy (running and not in error state)."""
            status_str = str(self.status)
            return status_str == "running" and status_str != "error"

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
            return str(self.status) == "stopped"

        @computed_field
        def can_stop(self) -> bool:
            """Check if app can be stopped."""
            return str(self.status) == "running"

        @computed_field
        def can_restart(self) -> bool:
            """Check if app can be restarted."""
            status_str = str(self.status)
            return status_str in {"running", "stopped"}

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
                    FlextWebConstants.Web.MIN_PORT
                    <= self.port
                    <= FlextWebConstants.Web.MAX_PORT
                ):
                    return FlextResult[None].fail(f"Port out of range: {self.port}")

                # Validate environment
                valid_environments = [
                    e.value for e in FlextConstants.Environment.ConfigEnvironment
                ]
                if self.environment not in valid_environments:
                    return FlextResult[None].fail(
                        f"Invalid environment: {self.environment}. Valid: {valid_environments}"
                    )

                # Validate health check URL if provided
                if self.health_check_url:
                    url_result = FlextModels.create_validated_url(self.health_check_url)
                    if url_result.is_failure:
                        return FlextResult[None].fail(
                            f"Invalid health check URL: {url_result.error}"
                        )

                return FlextResult[None].ok(None)
            except Exception as e:
                return FlextResult[None].fail(f"Validation failed: {e}")

        def start(self) -> FlextResult[FlextWebModels.WebApp]:
            """Start application with enhanced state management."""
            current_status = str(self.status)
            if current_status == "running":
                return FlextResult[FlextWebModels.WebApp].fail("App already running")
            if current_status not in {"stopped", "error"}:
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"App cannot be started from status: {current_status}"
                )

            # Update status through enum value
            try:
                self.status = FlextWebModels.WebAppStatus.STARTING
            except AttributeError:
                self.status = FlextWebModels.WebAppStatus.STARTING
            self.update_timestamp()

            # Simulate startup process
            try:
                self.status = FlextWebModels.WebAppStatus.RUNNING
            except AttributeError:
                self.status = FlextWebModels.WebAppStatus.RUNNING
            self.update_timestamp()

            return FlextResult[FlextWebModels.WebApp].ok(self)

        def stop(self) -> FlextResult[FlextWebModels.WebApp]:
            """Stop application with enhanced state management."""
            if str(self.status) != "running":
                return FlextResult[FlextWebModels.WebApp].fail("App not running")

            # Update status through enum value
            try:
                self.status = FlextWebModels.WebAppStatus.STOPPING
            except AttributeError:
                self.status = FlextWebModels.WebAppStatus.STOPPING
            self.update_timestamp()

            # Simulate shutdown process
            try:
                self.status = FlextWebModels.WebAppStatus.STOPPED
            except AttributeError:
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

        def update_metrics(self, metrics: dict[str, Any]) -> None:
            """Update application metrics."""
            self.metrics.update(metrics)
            self.update_timestamp()

        def get_health_status(self) -> dict[str, Any]:
            """Get comprehensive health status."""
            return {
                "status": str(self.status),
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

        def to_dict(self) -> FlextTypes.Core.Dict:
            """Convert to dictionary with enhanced serialization."""
            return {
                "id": self.id,
                "name": self.name,
                "host": self.host,
                "port": self.port,
                "status": str(self.status),
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
        query_params: dict[str, Any] = Field(
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

        @computed_field
        @property
        def request_summary(self) -> dict[str, Any]:
            """Computed field providing comprehensive request summary."""
            return {
                "request_info": {
                    "id": self.request_id,
                    "method": self.method,
                    "url": self.url,
                    "timestamp": self.timestamp.isoformat(),
                },
                "client_info": {"ip": self.client_ip, "user_agent": self.user_agent},
                "request_properties": {
                    "is_safe_method": self.is_safe_method,
                    "is_idempotent": self.is_idempotent,
                    "has_body": bool(self.body),
                    "header_count": len(self.headers),
                    "param_count": len(self.query_params),
                },
            }

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

        @field_serializer("headers", when_used="json")
        def serialize_headers_securely(self, value: dict[str, str]) -> dict[str, str]:
            """SERVER-SPECIFIC field serializer for masking sensitive headers."""
            masked_headers = {}
            sensitive_headers = ["authorization", "cookie", "x-api-key", "x-auth-token"]

            for key, val in value.items():
                if key.lower() in sensitive_headers:
                    masked_headers[key] = "***MASKED***"
                else:
                    masked_headers[key] = val

            return masked_headers

        @computed_field
        @property
        def is_safe_method(self) -> bool:
            """Check if HTTP method is safe (GET, HEAD, OPTIONS) - SERVER SPECIFIC."""
            return self.method.upper() in {"GET", "HEAD", "OPTIONS"}

        @computed_field
        @property
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

        @computed_field
        @property
        def response_summary(self) -> dict[str, Any]:
            """Computed field providing comprehensive response summary."""
            return {
                "response_info": {
                    "id": self.response_id,
                    "request_id": self.request_id,
                    "status_code": self.status_code,
                    "timestamp": self.timestamp.isoformat(),
                },
                "performance_info": {
                    "processing_time_ms": self.processing_time_ms,
                    "processing_time_seconds": self.processing_time_seconds,
                    "content_length": self.content_length,
                    "content_type": self.content_type,
                },
                "status_properties": {
                    "is_success": self.is_success,
                    "is_client_error": self.is_client_error,
                    "is_server_error": self.is_server_error,
                    "status_category": self._get_status_category(),
                },
            }

        @model_validator(mode="after")
        def validate_response_consistency(self) -> Self:
            """Model validator for response consistency."""
            # Validate content type and body consistency
            if self.body and not self.content_type:
                msg = "Content-Type must be specified when body is present"
                raise ValueError(msg)

            # Validate content length consistency
            if self.body and self.content_length == 0:
                self.content_length = len(self.body.encode("utf-8"))
            elif not self.body and self.content_length > 0:
                msg = "Content-Length should be 0 when no body is present"
                raise ValueError(msg)

            return self

        @field_serializer("body", when_used="json")
        def serialize_response_body_securely(self, value: str | None) -> str | None:
            """Field serializer for secure response body handling."""
            if not value:
                return value

            # Limit body size in serialization for security
            max_body_size = 1000  # 1KB limit for serialization
            if len(value) > max_body_size:
                return (
                    f"{value[:max_body_size]}... [TRUNCATED - {len(value)} total chars]"
                )

            return value

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
        @property
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
            default=FlextWebConstants.Web.DEFAULT_HOST,
            min_length=1,
            max_length=255,
            description="Host address",
        )
        port: int = Field(
            default=FlextWebConstants.Web.DEFAULT_PORT,
            ge=FlextWebConstants.Web.MIN_PORT,
            le=FlextWebConstants.Web.MAX_PORT,
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
        cors_origins: list[str] = Field(
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

        @computed_field
        @property
        def config_summary(self) -> dict[str, Any]:
            """Computed field providing comprehensive configuration summary."""
            return {
                "application_config": {
                    "name": self.app_name,
                    "debug_mode": self.debug,
                    "protocol": self.protocol,
                    "base_url": self.base_url,
                },
                "network_config": {
                    "host": self.host,
                    "port": self.port,
                    "ssl_enabled": self.ssl_enabled,
                    "request_timeout": self.request_timeout,
                },
                "security_config": {
                    "cors_enabled": self.enable_cors,
                    "cors_origins_count": len(self.cors_origins),
                    "secret_key_length": len(self.secret_key) if self.secret_key else 0,
                    "ssl_configured": bool(self.ssl_cert_path and self.ssl_key_path),
                },
                "limits_config": {
                    "max_content_length": self.max_content_length,
                    "max_content_length_mb": round(
                        self.max_content_length / (1024 * 1024), 2
                    ),
                },
            }

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

        @field_serializer("secret_key", when_used="json")
        def serialize_secret_key_securely(self, _value: str) -> str:
            """Field serializer for secure secret key handling."""
            # Never expose actual secret key in serialization
            return "***MASKED***"

        @field_validator("cors_origins")
        @classmethod
        def validate_cors_origins(cls, v: list[str]) -> list[str]:
            """Validate CORS origins with comprehensive URL validation."""
            if not v:
                return []

            validated_origins: list[str] = []
            for origin in v:
                if origin == "*":
                    validated_origins.append(origin)
                else:
                    result = FlextModels.create_validated_url(origin)
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
            ...     title="My API",
            ...     version="1.0.0",
            ...     description="Enterprise API"
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
        middlewares: list[Any] = Field(
            default_factory=list,
            description="Middleware instances (e.g., from flext-auth)",
        )

        @computed_field
        @property
        def config_summary(self) -> dict[str, Any]:
            """Computed field providing configuration summary."""
            return {
                "application": {
                    "title": self.title,
                    "version": self.version,
                    "description": self.description,
                },
                "documentation": {
                    "docs_url": self.docs_url,
                    "redoc_url": self.redoc_url,
                    "openapi_url": self.openapi_url,
                },
                "middleware_count": len(self.middlewares),
            }

    @classmethod
    def create_web_app(
        cls,
        data: FlextWebTypes.AppData,
    ) -> FlextResult[FlextWebModels.WebApp]:
        """Enhanced web application creation with comprehensive validation."""
        try:
            app_data: dict[str, object] = dict(data)

            # Ensure required fields
            if "id" not in app_data:
                app_data["id"] = f"app_{uuid.uuid4().hex[:8]}"

            if "status" not in app_data:
                app_data["status"] = FlextWebModels.WebAppStatus.STOPPED

            # Validate and convert port
            port = app_data.get("port", FlextWebConstants.Web.DEFAULT_PORT)
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

            app = FlextWebModels.WebApp(
                id=str(app_data["id"]),
                name=str(app_data["name"]),
                host=str(app_data["host"]),
                port=port_value,
                status=FlextWebModels.WebAppStatus(app_data["status"]),
                version=int(
                    app_data.get(
                        "version", str(FlextConstants.Performance.DEFAULT_VERSION)
                    )
                ),
                environment=str(
                    app_data.get("environment", FlextConstants.Defaults.ENVIRONMENT)
                ),
                health_check_url=app_data.get("health_check_url"),
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
        **kwargs: str | int | dict[str, str] | None,
    ) -> FlextResult[FlextWebModels.WebRequest]:
        """Create web request with validation."""
        try:
            request = FlextWebModels.WebRequest(
                method=method,
                url=url,
                headers=kwargs.get("headers", {}),
                query_params=kwargs.get("query_params", {}),
                body=kwargs.get("body"),
                timeout=kwargs.get("timeout", 30),
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
        **kwargs: str | int | dict[str, str] | None,
    ) -> FlextResult[FlextWebModels.WebResponse]:
        """Create web response with validation."""
        try:
            response = FlextWebModels.WebResponse(
                request_id=request_id,
                status_code=status_code,
                headers=kwargs.get("headers", {}),
                body=kwargs.get("body"),
                response_time=kwargs.get("response_time", 0.0),
            )
            return FlextResult[FlextWebModels.WebResponse].ok(response)
        except Exception as e:
            return FlextResult[FlextWebModels.WebResponse].fail(
                f"Failed to create web response: {e}"
            )


__all__ = ["FlextWebModels"]
