"""FLEXT Web Configuration - Settings using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import Self

from flext_core import FlextCore
from pydantic import (
    Field,
    SecretStr,
    computed_field,
    field_validator,
    model_validator,
)
from pydantic_settings import SettingsConfigDict

from flext_web.constants import FlextWebConstants


class FlextWebConfig(FlextCore.Config):
    """Enhanced Pydantic 2.11 Settings class for flext-web extending FlextCore.Config.

    Leverages all FlextCore.Config advanced features:
    - Protocol inheritance (Infrastructure.Configurable, etc.)
    - Enhanced Pydantic 2.11+ features (validate_return, arbitrary_types, etc.)
    - Advanced serialization (ser_json_timedelta, ser_json_bytes)
    - Computed fields and validation
    - Web-specific configuration extending core patterns

    **NEW FEATURES INTEGRATION**:
    - Inherits all FlextCore.Config Pydantic 2.11+ enhancements
    - Web-specific field extensions with proper defaults
    - Enhanced validation using FlextWebConstants
    - Computed fields for web-specific derived configuration
    - Protocol implementations for web service configuration
    """

    # Web-specific model configuration
    model_config = SettingsConfigDict(
        validate_assignment=True,
        str_strip_whitespace=True,
        arbitrary_types_allowed=True,
        validate_return=True,
        extra="forbid",
        frozen=False,
        json_schema_extra={
            "title": "FLEXT Web Configuration",
            "description": "Enterprise web service configuration",
            "category": "web",
        },
    )

    # Web service configuration using FlextWebConstants for defaults
    host: str = Field(
        default=FlextWebConstants.WebServer.DEFAULT_HOST,
        description="Host address for web service",
        min_length=1,
        max_length=255,
    )

    port: int = Field(
        default=FlextWebConstants.WebServer.DEFAULT_PORT,
        ge=FlextWebConstants.WebServer.MIN_PORT,
        le=FlextWebConstants.WebServer.MAX_PORT,
        description="Port number for web service",
    )

    debug: bool = Field(
        default=False,
        description="Enable debug mode",
    )

    secret_key: SecretStr | None = Field(
        default=SecretStr(FlextWebConstants.WebSpecific.DEFAULT_SECRET_KEY),
        min_length=32,
        description="Flask secret key for sessions",
    )

    app_name: str = Field(
        default="FLEXT Web",
        min_length=FlextWebConstants.WebServer.MIN_APP_NAME_LENGTH,
        max_length=FlextWebConstants.WebServer.MAX_APP_NAME_LENGTH,
        description="Application name",
    )

    version: str = Field(
        default=FlextCore.Constants.VERSION,
        description="Application version",
    )

    # Advanced web settings
    max_content_length: int = Field(
        default=FlextCore.Constants.Logging.MAX_FILE_SIZE,  # 16MB
        gt=0,
        description="Maximum request content length in bytes",
    )

    request_timeout: int = Field(
        default=FlextCore.Constants.Network.DEFAULT_TIMEOUT,
        gt=0,
        le=600,
        description="Request timeout in seconds",
    )

    enable_cors: bool = Field(
        default=False,
        description="Enable CORS support",
    )

    cors_origins: FlextCore.Types.StringList = Field(
        default_factory=list,
        description="CORS allowed origins",
    )

    # SSL/TLS configuration
    ssl_enabled: bool = Field(
        default=False,
        description="Enable SSL/TLS",
    )

    ssl_cert_path: str | None = Field(
        default=None,
        description="SSL certificate file path",
    )

    ssl_key_path: str | None = Field(
        default=None,
        description="SSL private key file path",
    )

    # Security settings
    session_cookie_secure: bool = Field(
        default=False,
        description="Secure session cookies",
    )

    session_cookie_httponly: bool = Field(
        default=True,
        description="HTTP-only session cookies",
    )

    session_cookie_samesite: str = Field(
        default="Lax",
        description="SameSite attribute for session cookies",
    )

    # Logging configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level",
    )

    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log message format",
    )

    @field_validator("debug", mode="before")
    @classmethod
    def validate_debug(cls, value: object) -> bool:
        """Enhanced debug field validation with comprehensive type conversion."""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in {"true", "1", "yes", "on", "enabled"}
        if isinstance(value, int):
            return bool(value)
        return bool(value)

    @field_validator("host")
    @classmethod
    def validate_host(cls, value: str) -> str:
        """Enhanced host address validation with security checks."""
        if not value or not value.strip():
            msg = "Host address cannot be empty"
            raise ValueError(msg)

        host = value.strip()

        # Allow localhost and local IPs for development
        if host in {
            FlextWebConstants.WebServer.DEFAULT_HOST,
            FlextWebConstants.WebSpecific.LOCALHOST_IP,
        }:
            return host

        # Security validation - restrict 0.0.0.0 for security
        if host == FlextWebConstants.WebSpecific.ALL_INTERFACES:
            return FlextWebConstants.WebSpecific.LOCALHOST_IP

        # Use flext-core validation
        result = FlextCore.Models.Validation.validate_hostname(host)
        if result.is_failure:
            raise ValueError(result.error)

        return result.unwrap()

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, value: SecretStr | None) -> SecretStr:
        """Enhanced secret key validation with security checks."""
        if value is None:
            msg = "Secret key cannot be None"
            raise ValueError(msg)

        # Extract actual value from SecretStr
        secret_value = (
            value.get_secret_value() if isinstance(value, SecretStr) else str(value)
        )

        if len(secret_value) < FlextWebConstants.WebServer.MIN_SECRET_KEY_LENGTH:
            msg = "Secret key must be at least 32 characters long"
            raise ValueError(msg)

        # Check for default key
        if secret_value == FlextWebConstants.WebSpecific.DEFAULT_SECRET_KEY:
            msg = "Must change default secret key"
            raise ValueError(msg)

        # Additional security checks
        if secret_value.lower() in {"password", "secret", "key", "123456", "REDACTED_LDAP_BIND_PASSWORD"}:
            msg = "Secret key is too weak"
            raise ValueError(msg)

        return value if isinstance(value, SecretStr) else SecretStr(secret_value)

    @field_validator("port")
    @classmethod
    def validate_port(cls, value: int) -> int:
        """Enhanced port validation with security checks."""
        min_port = FlextWebConstants.WebServer.MIN_PORT
        max_port = FlextWebConstants.WebServer.MAX_PORT
        if not (min_port <= value <= max_port):
            msg = f"Port must be between {min_port} and {max_port}, got {value}"
            raise ValueError(msg)

        # Warn about system reserved ports (1-1023) but allow them
        if value <= FlextWebConstants.WebSpecific.SYSTEM_PORTS_THRESHOLD:
            warnings.warn(
                f"Using system reserved port {value}. May require special permissions in production.",
                UserWarning,
                stacklevel=2,
            )

        return value

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
                # Validate URL format
                result = FlextCore.Models.Validation.validate_url(origin)
                if result.is_failure:
                    msg = f"Invalid CORS origin: {origin}"
                    raise ValueError(msg)
                validated_origins.append(result.unwrap())
        return validated_origins

    @field_validator("session_cookie_samesite")
    @classmethod
    def validate_samesite(cls, v: str) -> str:
        """Validate SameSite attribute."""
        valid_values = {"Strict", "Lax", "None"}
        if v not in valid_values:
            msg = f"Invalid SameSite value: {v}. Valid values: {valid_values}"
            raise ValueError(msg)
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in valid_levels:
            msg = f"Invalid log level: {v}. Valid levels: {valid_levels}"
            raise ValueError(msg)
        return v.upper()

    @model_validator(mode="after")
    def validate_ssl_config(self) -> Self:
        """Validate SSL configuration."""
        if self.ssl_enabled:
            if not self.ssl_cert_path or not self.ssl_key_path:
                msg = "SSL certificate and key paths are required when SSL is enabled"
                raise ValueError(msg)

            # Validate file paths exist
            if not Path(self.ssl_cert_path).exists():
                msg = f"SSL certificate file not found: {self.ssl_cert_path}"
                raise ValueError(msg)

            if not Path(self.ssl_key_path).exists():
                msg = f"SSL key file not found: {self.ssl_key_path}"
                raise ValueError(msg)

        return self

    @model_validator(mode="after")
    def validate_cors_config(self) -> Self:
        """Validate CORS configuration."""
        # CORS enabled without origins should fail
        if self.enable_cors and not self.cors_origins:
            msg = "CORS origins required when CORS is enabled"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def validate_security_settings(self) -> Self:
        """Validate security-related settings."""
        # SSL and cookie security consistency
        if self.ssl_enabled and not self.session_cookie_secure:
            warnings.warn(
                "SSL is enabled but session cookies are not marked as secure",
                UserWarning,
                stacklevel=2,
            )

        # CORS and SSL consistency
        if self.enable_cors and self.ssl_enabled:
            for origin in self.cors_origins:
                if origin != "*" and not origin.startswith("https://"):
                    warnings.warn(
                        f"CORS origin {origin} should use HTTPS when SSL is enabled",
                        UserWarning,
                        stacklevel=2,
                    )

        return self

    @computed_field
    def protocol(self) -> str:
        """Get protocol based on SSL configuration."""
        return "https" if self.ssl_enabled else "http"

    @computed_field
    def base_url(self) -> str:
        """Get base URL for web service."""
        return f"{self.protocol}://{self.host}:{self.port}"

    def get_server_config(self) -> FlextCore.Types.Dict:
        """Get server configuration."""
        return {
            "host": self.host,
            "port": self.port,
            "debug": self.debug,
            "protocol": self.protocol,
            "base_url": self.base_url,
            "ssl_enabled": self.ssl_enabled,
        }

    def get_security_config(self) -> FlextCore.Types.Dict:
        """Get security configuration."""
        return {
            "session_cookie_secure": self.session_cookie_secure,
            "session_cookie_httponly": self.session_cookie_httponly,
            "session_cookie_samesite": self.session_cookie_samesite,
            "enable_cors": self.enable_cors,
            "cors_origins": self.cors_origins,
            "ssl_enabled": self.ssl_enabled,
        }

    # Factory methods for compatibility (simplified from the wrapper)
    @classmethod
    def create_web_config(cls, **overrides: object) -> FlextCore.Result[FlextWebConfig]:
        """Create web configuration instance with optional overrides."""
        # Input validation - fail fast for invalid overrides
        if not overrides:
            return FlextCore.Result[FlextWebConfig].fail(
                "Overrides dictionary cannot be empty"
            )

        # Create config with Pydantic validation - let exceptions be handled explicitly
        try:
            # Pydantic will validate the types at runtime, so we suppress type checking here
            config = cls(**overrides)
            # Ensure it's properly typed as FlextWebConfig
            if not isinstance(config, cls):
                return FlextCore.Result[FlextWebConfig].fail(
                    f"Failed to create proper {cls.__name__} instance"
                )
            return FlextCore.Result[FlextWebConfig].ok(config)
        except Exception as e:
            # Log validation failure and return result
            logger = FlextCore.Logger(__name__)
            logger.warning("Web config creation failed", error=str(e))
            return FlextCore.Result[FlextWebConfig].fail(
                f"Failed to create web config: {e}"
            )

    # Business rules validation
    def validate_business_rules(self) -> FlextCore.Result[None]:
        """Validate web configuration business rules.

        Validates web-specific business rules for configuration consistency.
        """
        # Web-specific business rules validation - explicit returns, no try/except needed

        # SSL configuration validation
        if self.ssl_enabled:
            if not self.ssl_cert_path:
                return FlextCore.Result[None].fail(
                    "SSL certificate path required when SSL is enabled"
                )
            if not self.ssl_key_path:
                return FlextCore.Result[None].fail(
                    "SSL private key path required when SSL is enabled"
                )

        # CORS configuration validation
        if self.enable_cors and not self.cors_origins:
            return FlextCore.Result[None].fail(
                "CORS origins required when CORS is enabled"
            )

        # Security validation
        if self.debug and not self.secret_key:
            return FlextCore.Result[None].fail(
                "Secret key required when debug mode is enabled"
            )
        if self.enable_cors and "*" in self.cors_origins:
            return FlextCore.Result[None].fail("Wildcard CORS origins not recommended")

        # Session security validation
        if self.ssl_enabled and not self.session_cookie_secure:
            return FlextCore.Result[None].fail(
                "Session cookies must be secure when SSL is enabled"
            )

        # Port security validation
        if (
            self.host == FlextWebConstants.WebSpecific.ALL_INTERFACES
            and self.port <= FlextWebConstants.WebSpecific.SYSTEM_PORTS_THRESHOLD
        ):
            return FlextCore.Result[None].fail(
                f"Binding to all interfaces (0.0.0.0) with system port {self.port} is not allowed"
            )

        return FlextCore.Result[None].ok(None)

    # Web-specific project identification (extends base project fields)
    project_name: str = Field(
        default="flext-web",
        description="Web project name (overrides base FlextCore.Config)",
    )


__all__ = [
    "FlextWebConfig",
]
