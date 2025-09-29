"""FLEXT Web Configuration - Settings using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
import warnings
from pathlib import Path
from typing import Any, Self

from pydantic import Field, SecretStr, computed_field, field_validator, model_validator
from pydantic_settings import SettingsConfigDict

from flext_core import FlextConfig, FlextConstants, FlextModels, FlextResult
from flext_web.constants import FlextWebConstants


class FlextWebConfig(FlextConfig):
    """Single Pydantic 2 Settings class for flext-web extending FlextConfig.

    Follows standardized pattern:
    - Extends FlextConfig from flext-core directly (no nested classes)
    - Flat class structure with all fields at top level
    - All defaults from FlextWebConstants
    - SecretStr for sensitive data
    - Uses enhanced singleton pattern with inverse dependency injection
    - Uses Pydantic 2.11+ features (field_validator, model_validator)
    """

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_WEB_",
        case_sensitive=False,
        extra="allow",
        # Inherit enhanced Pydantic 2.11+ features from FlextConfig
        validate_assignment=True,
        str_strip_whitespace=True,
        json_schema_extra={
            "title": "FLEXT Web Configuration",
            "description": "Enterprise web service configuration extending FlextConfig",
        },
    )

    # Web service configuration using FlextWebConstants for defaults
    host: str = Field(
        default=FlextWebConstants.Web.DEFAULT_HOST,
        description="Host address for web service",
        min_length=1,
        max_length=255,
    )

    port: int = Field(
        default=FlextWebConstants.Web.DEFAULT_PORT,
        ge=FlextWebConstants.Web.MIN_PORT,
        le=FlextWebConstants.Web.MAX_PORT,
        description="Port number for web service",
    )

    debug: bool = Field(
        default=False,
        description="Enable debug mode",
    )

    development_mode: bool = Field(
        default=False,
        description="Enable development mode with additional features",
    )

    web_environment: str = Field(
        default="development",
        description="Web environment setting (development, testing, production)",
    )

    secret_key: SecretStr | None = Field(
        default=SecretStr(FlextWebConstants.WebSpecific.DEV_SECRET_KEY),
        min_length=32,
        description="Flask secret key for sessions",
    )

    app_name: str = Field(
        default="FLEXT Web",
        min_length=FlextWebConstants.Web.MIN_APP_NAME_LENGTH,
        max_length=FlextWebConstants.Web.MAX_APP_NAME_LENGTH,
        description="Application name",
    )

    version: str = Field(
        default=FlextConstants.Core.VERSION,
        description="Application version",
    )

    # Advanced web settings
    max_content_length: int = Field(
        default=FlextConstants.Logging.MAX_FILE_SIZE,  # 16MB
        gt=0,
        description="Maximum request content length in bytes",
    )

    request_timeout: int = Field(
        default=FlextConstants.Network.DEFAULT_TIMEOUT,
        gt=0,
        le=600,
        description="Request timeout in seconds",
    )

    enable_cors: bool = Field(
        default=False,
        description="Enable CORS support",
    )

    cors_origins: list[str] = Field(
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
            FlextWebConstants.Web.DEFAULT_HOST,
            FlextWebConstants.WebSpecific.LOCALHOST_IP,
        }:
            return host

        # Security validation for production
        if host == FlextWebConstants.WebSpecific.ALL_INTERFACES:
            # Only allow 0.0.0.0 in development mode
            config = cls.get_or_create_shared_instance(project_name="flext-web")
            # Cast to FlextWebConfig to access development_mode
            if isinstance(config, cls) and config.development_mode:
                return host
            # In production, use localhost instead
            return FlextWebConstants.WebSpecific.LOCALHOST_IP

        # Use flext-core validation
        result = FlextModels.Validation.validate_hostname(host)
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

        if len(secret_value) < FlextWebConstants.Web.MIN_SECRET_KEY_LENGTH:
            msg = "Secret key must be at least 32 characters long"
            raise ValueError(msg)

        # Check for default development key in production-like environments
        if (
            secret_value == FlextWebConstants.WebSpecific.DEV_SECRET_KEY
            and not cls._is_development_env()
        ):
            msg = "Must change default secret key for production"
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
        min_port = FlextWebConstants.Web.MIN_PORT
        max_port = FlextWebConstants.Web.MAX_PORT
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
    def validate_cors_origins(cls, v: list[str]) -> list[str]:
        """Validate CORS origins with comprehensive URL validation."""
        if not v:
            return []

        validated_origins: list[str] = []
        for origin in v:
            if origin == "*":
                validated_origins.append(origin)
            else:
                # Validate URL format
                result = FlextModels.create_validated_url(origin)
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
    @property
    def protocol(self) -> str:
        """Get protocol based on SSL configuration."""
        return "https" if self.ssl_enabled else "http"

    @computed_field
    @property
    def base_url(self) -> str:
        """Get base URL."""
        return f"{self.protocol}://{self.host}:{self.port}"

    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.debug or self._is_development_env()

    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.is_development

    @classmethod
    def _is_development_env(cls) -> bool:
        """Check if running in development environment."""
        # Use environment variable directly to avoid circular dependency
        web_env = os.getenv("FLEXT_WEB_WEB_ENVIRONMENT", "development").lower()
        return web_env in {"development", "dev", "local"}

    def get_server_config(self) -> dict[str, Any]:
        """Get server configuration."""
        return {
            "host": self.host,
            "port": self.port,
            "debug": self.debug,
            "protocol": self.protocol,
            "base_url": self.base_url,
            "ssl_enabled": self.ssl_enabled,
        }

    def get_security_config(self) -> dict[str, Any]:
        """Get security configuration."""
        return {
            "session_cookie_secure": self.session_cookie_secure,
            "session_cookie_httponly": self.session_cookie_httponly,
            "session_cookie_samesite": self.session_cookie_samesite,
            "enable_cors": self.enable_cors,
            "cors_origins": self.cors_origins,
            "ssl_enabled": self.ssl_enabled,
        }

    @classmethod
    def create_for_environment(
        cls, environment: str, **overrides: object
    ) -> FlextWebConfig:
        """Create configuration for specific environment using enhanced singleton pattern."""
        return cls.get_or_create_shared_instance(
            project_name="flext-web", environment=environment, **overrides
        )

    @classmethod
    def create_default(cls) -> FlextWebConfig:
        """Create default configuration instance using enhanced singleton pattern."""
        return cls.get_or_create_shared_instance(project_name="flext-web")

    @classmethod
    def get_global_instance(cls) -> FlextWebConfig:
        """Get the global singleton instance using enhanced FlextConfig pattern."""
        return cls.get_or_create_shared_instance(project_name="flext-web")

    @classmethod
    def reset_global_instance(cls) -> None:
        """Reset the global FlextWebConfig instance (mainly for testing)."""
        # Use the enhanced FlextConfig reset mechanism
        super().reset_global_instance()

    # Factory methods for compatibility (simplified from the wrapper)
    @classmethod
    def create_web_config(cls, **overrides: object) -> FlextResult[FlextWebConfig]:
        """Create web configuration instance with optional overrides."""
        try:
            config = cls(**overrides)
            return FlextResult[FlextWebConfig].ok(config)
        except Exception as e:
            return FlextResult[FlextWebConfig].fail(f"Failed to create web config: {e}")

    # Business rules validation
    def validate_business_rules(self) -> FlextResult[None]:
        """Validate web configuration business rules."""
        try:
            # Validate web-specific business rules
            if self.ssl_enabled and not self.ssl_cert_path:
                return FlextResult[None].fail(
                    "SSL certificate path required when SSL is enabled"
                )

            if self.enable_cors and not self.cors_origins:
                return FlextResult[None].fail(
                    "CORS origins required when CORS is enabled"
                )

            if self.debug and self.web_environment == "production":
                return FlextResult[None].fail(
                    "Debug mode should not be enabled in production"
                )

            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(f"Business rules validation failed: {e}")

    # Project identification
    project_name: str = Field(
        default="flext-web",
        description="Project name",
    )
    project_version: str = Field(
        default="0.9.0",
        description="Project version",
    )


# REMOVED: FlextWebSettings was a wrapper class - use FlextWebConfig directly


__all__ = [
    "FlextWebConfig",
]
