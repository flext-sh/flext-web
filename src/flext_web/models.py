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
from typing import Any, Self

from pydantic import ConfigDict, Field, computed_field, field_validator, model_validator

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
            default="localhost",
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
            default_factory=lambda: FlextWebModels.WebAppStatus.STOPPED,  # type: ignore[attr-defined]
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

        @field_validator("status")
        @classmethod
        def validate_status(
            cls,
            v: FlextWebModels.WebAppStatus | str,
        ) -> FlextWebModels.WebAppStatus:
            """Validate status field with enhanced error handling."""
            if isinstance(v, str):
                try:
                    return FlextWebModels.WebAppStatus(v)
                except ValueError as e:
                    valid_statuses = [
                        status.value for status in FlextWebModels.WebAppStatus
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
            if host.lower() in {"localhost", "127.0.0.1", "::", "::1"}:
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
            return self.status == FlextWebModels.WebAppStatus.RUNNING

        @computed_field
        def is_healthy(self) -> bool:
            """Check if app is healthy (running and not in error state)."""
            return (
                self.status == FlextWebModels.WebAppStatus.RUNNING
                and self.status != FlextWebModels.WebAppStatus.ERROR
            )

        @computed_field
        def url(self) -> str:
            """Get app URL with proper protocol detection."""
            # Standard HTTPS ports
            https_ports = {443, 8443}
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
                    FlextWebConstants.Web.MIN_PORT
                    <= self.port
                    <= FlextWebConstants.Web.MAX_PORT
                ):
                    return FlextResult[None].fail(f"Port out of range: {self.port}")

                # Validate environment
                valid_environments = [
                    e.value for e in list(FlextConstants.Environment.ConfigEnvironment)
                ]  # type: ignore[misc]
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
            if self.status == FlextWebModels.WebAppStatus.RUNNING:
                return FlextResult[FlextWebModels.WebApp].fail("App already running")
            if self.status not in {
                FlextWebModels.WebAppStatus.STOPPED,
                FlextWebModels.WebAppStatus.ERROR,
            }:
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"App cannot be started from status: {self.status.value}"
                )

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
                    f"App cannot be restarted from status: {self.status.value}"
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

        def to_dict(self) -> FlextTypes.Core.Dict:
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

        def __str__(self) -> str:
            """String representation of the WebApp."""
            return f"{self.name} ({self.host}:{self.port}) [{self.status.value}]"

        def __repr__(self) -> str:
            """Detailed string representation."""
            return (
                f"WebApp(id='{self.id}', name='{self.name}', "
                f"host='{self.host}', port={self.port}, "
                f"status='{self.status.value}', version='{self.version}')"
            )

        def model_post_init(self, __context: object, /) -> None:
            """Post-init setup with enhanced initialization."""
            super().model_post_init(__context)
            # Initialize webapp-specific state
            if not self.metrics:
                self.metrics = {
                    "startup_time": None,
                    "request_count": 0,
                    "error_count": 0,
                    "last_request": None,
                }

    # Enhanced Web Request Models
    class WebRequest(_BaseWebModel):
        """Enhanced web request model with comprehensive tracking."""

        request_id: str = Field(
            default_factory=lambda: str(uuid.uuid4()),
            description="Unique request identifier",
        )
        method: str = Field(
            description="HTTP method",
            min_length=1,
            max_length=10,
        )
        url: str = Field(
            description="Request URL",
            min_length=1,
        )
        headers: dict[str, str] = Field(
            default_factory=dict,
            description="Request headers",
        )
        query_params: dict[str, Any] = Field(
            default_factory=dict,
            description="Query parameters",
        )
        body: str | None = Field(
            default=None,
            description="Request body",
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

        @field_validator("method")
        @classmethod
        def validate_method(cls, v: str) -> str:
            """Validate HTTP method."""
            result = FlextModels.create_validated_http_method(v)
            if result.is_failure:
                raise ValueError(result.error)
            return result.unwrap()

        @field_validator("url")
        @classmethod
        def validate_url(cls, v: str) -> str:
            """Validate URL format."""
            result = FlextModels.create_validated_url(v)
            if result.is_failure:
                raise ValueError(result.error)
            return result.unwrap()

        @computed_field
        def is_safe_method(self) -> bool:
            """Check if HTTP method is safe (GET, HEAD, OPTIONS)."""
            return self.method.upper() in {"GET", "HEAD", "OPTIONS"}

        @computed_field
        def is_idempotent(self) -> bool:
            """Check if HTTP method is idempotent."""
            return self.method.upper() in {"GET", "HEAD", "PUT", "DELETE", "OPTIONS"}

    class WebResponse(_BaseWebModel):
        """Enhanced web response model with comprehensive tracking."""

        response_id: str = Field(
            default_factory=lambda: str(uuid.uuid4()),
            description="Unique response identifier",
        )
        request_id: str = Field(
            description="Associated request identifier",
        )
        status_code: int = Field(
            description="HTTP status code",
            ge=100,
            le=599,
        )
        headers: dict[str, str] = Field(
            default_factory=dict,
            description="Response headers",
        )
        body: str | None = Field(
            default=None,
            description="Response body",
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

        @field_validator("status_code")
        @classmethod
        def validate_status_code(cls, v: int) -> int:
            """Validate HTTP status code."""
            result = FlextModels.create_validated_http_status(v)
            if result.is_failure:
                raise ValueError(result.error)
            return result.unwrap()

        @computed_field
        def is_success(self) -> bool:
            """Check if response indicates success."""
            return 200 <= self.status_code < 300

        @computed_field
        def is_client_error(self) -> bool:
            """Check if response indicates client error."""
            return 400 <= self.status_code < 500

        @computed_field
        def is_server_error(self) -> bool:
            """Check if response indicates server error."""
            return 500 <= self.status_code < 600

        @computed_field
        def processing_time_seconds(self) -> float:
            """Get processing time in seconds."""
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
            default="localhost",
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
                ),  # type: ignore[arg-type]
                environment=str(
                    app_data.get("environment", FlextConstants.Defaults.ENVIRONMENT)
                ),
                health_check_url=app_data.get("health_check_url"),
                domain_events=[],
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
