"""FLEXT Web Configurations - Consolidated configuration system with enterprise patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any, ClassVar, Self

from pydantic import (
    Field,
    SettingsConfigDict,
    computed_field,
    field_validator,
    model_validator,
)

from flext_core import (
    FlextConfig,
    FlextConstants,
    FlextLogger,
    FlextModels,
    FlextResult,
)
from flext_web.constants import FlextWebConstants

_logger = FlextLogger(__name__)

# Import FlextWebSettings at module level to avoid conditional imports
try:
    from flext_web.settings import FlextWebSettings

    _FlextWebSettings = FlextWebSettings
except ImportError:
    _FlextWebSettings = None


def _get_flext_web_settings() -> type | None:
    """Get FlextWebSettings class if available.

    Returns:
        FlextWebSettings class or None if not available

    """
    return _FlextWebSettings


def _web_settings_available() -> bool:
    """Check if FlextWebSettings is available.

    Returns:
        True if FlextWebSettings can be imported, False otherwise

    """
    return _get_flext_web_settings() is not None


# Settings availability flag
_web_settings_available_flag = _web_settings_available()


class FlextWebConfigs:
    """Enhanced FLEXT web configuration system providing all configuration functionality.

    This is the complete web configuration system for the FLEXT Web ecosystem, providing
    unified configuration patterns built on flext-core foundation with web-specific
    settings and validation. All configuration types are organized as nested classes
    within this single container for consistent management and easy access with
    enhanced Pydantic 2.11 features.
    """

    # =============================================================================
    # ENHANCED WEB CONFIGURATION CLASSES
    # =============================================================================

    class WebConfig(FlextConfig):
        """Enhanced web service configuration with Pydantic 2.11 features.

        Enterprise-grade configuration class providing comprehensive web service
        settings with environment variable integration, type-safe validation,
        security-focused secret management, and enhanced Pydantic 2.11 capabilities.
        """

        model_config = SettingsConfigDict(
            # Inherit from FlextConfig and enhance with Pydantic 2.11 features
            env_prefix="FLEXT_WEB_",
            case_sensitive=False,
            env_file=".env",
            env_file_encoding="utf-8",
            env_nested_delimiter="__",
            extra="ignore",
            use_enum_values=True,
            frozen=False,
            # Enhanced Pydantic 2.11 features
            arbitrary_types_allowed=True,
            validate_return=True,
            serialize_by_alias=True,
            populate_by_name=True,
            ser_json_timedelta="iso8601",
            ser_json_bytes="base64",
            str_strip_whitespace=True,
            defer_build=False,
            coerce_numbers_to_str=False,
            validate_default=True,
            enable_decoding=True,
            nested_model_default_partial_update=True,
            cli_parse_args=False,
            cli_avoid_json=True,
            # Custom encoders for complex types
            json_encoders={
                Path: str,
                datetime: lambda dt: dt.isoformat(),
            },
        )

        # Enhanced web service settings with comprehensive validation
        host: str = Field(
            default="localhost",
            description="Host address for web service",
            min_length=1,
            max_length=255,
        )

        port: int = Field(
            default=FlextConstants.Platform.FLEXT_API_PORT,
            ge=FlextWebConstants.Web.MIN_PORT,
            le=FlextWebConstants.Web.MAX_PORT,
            description="Port number for web service",
        )

        debug: bool = Field(
            default=False,
            description="Enable debug mode",
        )

        secret_key: str | None = Field(
            default=FlextWebConstants.WebSpecific.DEV_SECRET_KEY,
            min_length=FlextConstants.Validation.MIN_SECRET_KEY_LENGTH,
            description="Flask secret key for sessions",
        )

        app_name: str = Field(
            default="FLEXT Web",
            min_length=1,
            max_length=255,
            description="Application name",
        )

        version: str = Field(
            default=FlextConstants.Core.VERSION,
            description="Application version",
        )

        # Enhanced advanced settings
        max_content_length: int = Field(
            default=FlextConstants.Limits.MAX_FILE_SIZE,
            gt=0,
            description="Maximum request content length in bytes",
        )

        request_timeout: int = Field(
            default=FlextConstants.Network.DEFAULT_TIMEOUT,
            gt=0,
            le=FlextConstants.Performance.DEFAULT_TIMEOUT_LIMIT,
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

        # Enhanced SSL/TLS configuration
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

        # Enhanced security settings
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

        # Enhanced logging configuration
        log_level: str = Field(
            default=FlextConstants.Logging.DEFAULT_LEVEL,
            description="Logging level",
        )

        log_format: str = Field(
            default=FlextConstants.Logging.DEFAULT_FORMAT,
            description="Log message format",
        )

        # Enhanced validation methods with Pydantic 2.11 features
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
            # For other types, convert to bool
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
            if host in {"localhost", FlextConstants.Platform.LOOPBACK_IP}:
                return host

            # Security validation for production
            if host == FlextWebConstants.WebSpecific.ALL_INTERFACES:
                # Only allow 0.0.0.0 in development mode
                if os.getenv("FLEXT_DEVELOPMENT_MODE", "false").lower() == "true":
                    return host
                # In production, use localhost instead
                return FlextConstants.Platform.LOOPBACK_IP

            # Use flext-core validation
            result = FlextModels.Validation.validate_hostname(host)
            if result.is_failure:
                raise ValueError(result.error)

            return result.unwrap()

        @field_validator("secret_key")
        @classmethod
        def validate_secret_key(cls, value: str | None) -> str:
            """Enhanced secret key validation with security checks."""
            if value is None:
                msg = "Secret key cannot be None"
                raise ValueError(msg)

            if len(value) < FlextConstants.Validation.MIN_SECRET_KEY_LENGTH:
                msg = f"Secret key must be at least {FlextConstants.Validation.MIN_SECRET_KEY_LENGTH} characters long"
                raise ValueError(msg)

            # Check for default development key in production-like environments
            if (
                value == FlextWebConstants.WebSpecific.DEV_SECRET_KEY
                and not cls._is_development_env()
            ):
                msg = "Must change default secret key for production"
                raise ValueError(msg)

            # Additional security checks
            if value.lower() in {"password", "secret", "key", "123456", "REDACTED_LDAP_BIND_PASSWORD"}:
                msg = "Secret key is too weak"
                raise ValueError(msg)

            return value

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
                        error_msg = f"Invalid CORS origin: {origin}"
                        raise ValueError(error_msg)
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
            valid_levels = FlextConstants.Logging.VALID_LEVELS
            if v.upper() not in valid_levels:
                msg = f"Invalid log level: {v}. Valid levels: {valid_levels}"
                raise ValueError(msg)
            return v.upper()

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

        # Enhanced computed fields
        @computed_field
        def debug_bool(self) -> bool:
            """Get debug value as boolean (guaranteed to be bool after validation)."""
            return bool(self.debug)

        @computed_field
        def protocol(self) -> str:
            """Get protocol based on SSL configuration."""
            return "https" if self.ssl_enabled else "http"

        @computed_field
        def base_url(self) -> str:
            """Get base URL."""
            return f"{self.protocol}://{self.host}:{self.port}"

        @computed_field
        def is_development(self) -> bool:
            """Check if running in development mode."""
            return self.debug_bool or self._is_development_env()

        @computed_field
        def is_production(self) -> bool:
            """Check if running in production mode."""
            return not self.is_development

        # Enhanced validation methods
        def validate_production_settings(self) -> FlextResult[None]:
            """Enhanced production-specific configuration validation."""
            try:
                errors: list[str] = []

                # Production-specific validations
                if self.debug_bool:
                    errors.append("Debug mode must be disabled in production")

                if self.secret_key == FlextWebConstants.WebSpecific.DEV_SECRET_KEY:
                    errors.append("Default secret key must be changed for production")

                if self.host == "localhost":
                    errors.append("Host should not be 'localhost' in production")

                if self.enable_cors and "*" in self.cors_origins:
                    errors.append(
                        "Wildcard CORS origin should not be used in production"
                    )

                if not self.ssl_enabled:
                    errors.append("SSL should be enabled in production")

                if not self.session_cookie_secure:
                    errors.append("Session cookies should be secure in production")

                # Security validations
                min_key_len = FlextConstants.Validation.MIN_SECRET_KEY_LENGTH
                if self.secret_key and len(self.secret_key) < min_key_len:
                    errors.append(
                        f"Secret key must be at least {min_key_len} characters"
                    )

                if errors:
                    return FlextResult[None].fail(
                        f"Production configuration validation failed: {'; '.join(errors)}"
                    )

                return FlextResult[None].ok(None)

            except Exception as e:
                return FlextResult[None].fail(f"Production validation error: {e}")

        def validate_config(self) -> FlextResult[None]:
            """Enhanced complete configuration validation."""
            try:
                errors: list[str] = []

                # Environment-specific validations
                if not self.is_development:
                    prod_result = self.validate_production_settings()
                    if prod_result.is_failure:
                        errors.append(
                            prod_result.error or "Production validation failed"
                        )

                # Network validations
                min_port = FlextWebConstants.Web.MIN_PORT
                max_port = FlextWebConstants.Web.MAX_PORT
                if self.port < min_port or self.port > max_port:
                    errors.append(
                        f"Port must be in valid range ({min_port}-{max_port})"
                    )

                # Security validations
                if (
                    self.secret_key
                    and len(self.secret_key)
                    < FlextConstants.Validation.MIN_SECRET_KEY_LENGTH
                ):
                    errors.append("Secret key is too short")

                # SSL validations - combine nested if statements
                if self.ssl_enabled and (
                    not self.ssl_cert_path or not self.ssl_key_path
                ):
                    errors.append(
                        "SSL certificate and key paths are required when SSL is enabled"
                    )

                if errors:
                    return FlextResult[None].fail(
                        f"Configuration validation failed: {'; '.join(errors)}"
                    )

                return FlextResult[None].ok(None)

            except Exception as e:
                return FlextResult[None].fail(f"Configuration validation error: {e}")

        def validate_business_rules(self) -> FlextResult[None]:
            """Enhanced web-specific business rules validation."""
            try:
                # Validate production constraints
                if not self.debug_bool and self.host == "localhost":
                    return FlextResult[None].fail(
                        "Production mode cannot use 'localhost' binding, use specific IP address"
                    )

                # Validate secret key strength in production
                if (
                    not self.debug_bool
                    and self.secret_key == FlextWebConstants.WebSpecific.DEV_SECRET_KEY
                ):
                    return FlextResult[None].fail(
                        "Production mode cannot use development secret key"
                    )

                # Validate CORS settings
                if (
                    self.enable_cors
                    and not self.debug_bool
                    and "*" in self.cors_origins
                ):
                    return FlextResult[None].fail(
                        "Wildcard CORS should be disabled in production for security"
                    )

                # Validate SSL requirements
                if not self.debug_bool and not self.ssl_enabled:
                    return FlextResult[None].fail("SSL should be enabled in production")

                return FlextResult[None].ok(None)

            except Exception as e:
                return FlextResult[None].fail(f"Business rules validation error: {e}")

        @classmethod
        def _is_development_env(cls) -> bool:
            """Check if running in development environment."""
            env = os.getenv("FLEXT_WEB_ENVIRONMENT", "development").lower()
            return env in {"development", "dev", "local"}

        def get_server_url(self) -> str:
            """Get the complete server URL."""
            return f"{self.protocol}://{self.host}:{self.port}"

        def get_config_summary(self) -> dict[str, Any]:
            """Get enhanced configuration summary."""
            return {
                "host": self.host,
                "port": self.port,
                "debug": self.debug_bool,
                "app_name": self.app_name,
                "version": self.version,
                "enable_cors": self.enable_cors,
                "cors_origins": self.cors_origins,
                "ssl_enabled": self.ssl_enabled,
                "protocol": self.protocol,
                "base_url": self.base_url,
                "max_content_length": self.max_content_length,
                "request_timeout": self.request_timeout,
                "session_cookie_secure": self.session_cookie_secure,
                "session_cookie_httponly": self.session_cookie_httponly,
                "session_cookie_samesite": self.session_cookie_samesite,
                "log_level": self.log_level,
                "is_development": self.is_development,
                "is_production": self.is_production,
            }

        @classmethod
        def create_with_validation(
            cls,
            overrides: dict[str, str | int | bool | list[str] | None] | None = None,
            **kwargs: str | int | bool | list[str] | None,
        ) -> FlextResult[FlextWebConfigs.WebConfig]:
            """Enhanced WebConfig creation with comprehensive validation."""
            try:
                # Prepare overrides dict
                all_overrides: dict[str, str | int | bool | list[str] | None] = {}
                if overrides:
                    all_overrides.update(overrides)
                all_overrides.update(kwargs)

                # Create instance with overrides
                instance = cls.model_validate(all_overrides) if all_overrides else cls()

                # Validate business rules
                validation_result = instance.validate_business_rules()
                if validation_result.is_failure:
                    return FlextResult[FlextWebConfigs.WebConfig].fail(
                        f"Business rules validation failed: {validation_result.error}"
                    )

                # Validate complete configuration
                config_result = instance.validate_config()
                if config_result.is_failure:
                    return FlextResult[FlextWebConfigs.WebConfig].fail(
                        f"Configuration validation failed: {config_result.error}"
                    )

                return FlextResult[FlextWebConfigs.WebConfig].ok(instance)

            except Exception as e:
                return FlextResult[FlextWebConfigs.WebConfig].fail(
                    f"Configuration creation failed: {e}"
                )

    # =============================================================================
    # ENHANCED FACTORY METHODS AND UTILITIES
    # =============================================================================

    @classmethod
    def _create_config_builder(
        cls, **overrides: str | int | bool | list[str] | None
    ) -> dict[str, str | int | bool | list[str] | None]:
        """Enhanced Builder pattern for configuration construction."""
        # Enhanced configuration schema with comprehensive defaults
        config_schema = {
            "host": "localhost",
            "port": FlextWebConstants.Web.DEFAULT_PORT,
            "debug": True,
            "secret_key": FlextWebConstants.WebSpecific.DEV_SECRET_KEY,
            "app_name": "FLEXT Web",
            "version": FlextConstants.Core.VERSION,
            "max_content_length": FlextConstants.Limits.MAX_FILE_SIZE,
            "request_timeout": FlextConstants.Network.DEFAULT_TIMEOUT,
            "enable_cors": False,
            "cors_origins": [],
            "ssl_enabled": False,
            "ssl_cert_path": None,
            "ssl_key_path": None,
            "session_cookie_secure": False,
            "session_cookie_httponly": True,
            "session_cookie_samesite": "Lax",
            "log_level": FlextConstants.Logging.DEFAULT_LEVEL,
            "log_format": FlextConstants.Logging.DEFAULT_FORMAT,
        }

        # Build configuration using overrides
        return {
            key: overrides.get(key, default) for key, default in config_schema.items()
        }

    @classmethod
    def create_web_config(
        cls,
        **overrides: str | int | bool | list[str] | None,
    ) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Enhanced web configuration creation with comprehensive validation."""
        try:
            return FlextWebConfigs.WebConfig.create_with_validation(
                overrides=dict(overrides)
            )
        except Exception as e:
            return FlextResult.fail(f"Configuration creation failed: {e}")

    @classmethod
    def create_development_config(cls) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Create enhanced development configuration."""
        return cls.create_web_config(
            host="localhost",
            port=FlextWebConstants.Web.DEFAULT_PORT,
            debug=True,
            secret_key=FlextWebConstants.WebSpecific.DEV_ENVIRONMENT_KEY,
            enable_cors=True,
            cors_origins=["*"],
            ssl_enabled=False,
            session_cookie_secure=False,
            log_level=FlextConstants.Logging.DEBUG,
        )

    @classmethod
    def create_production_config(cls) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Create enhanced production configuration."""
        secret_key = os.getenv("FLEXT_WEB_SECRET_KEY")
        if not secret_key:
            return FlextResult.fail("FLEXT_WEB_SECRET_KEY required for production")

        ssl_cert = os.getenv("FLEXT_WEB_SSL_CERT_PATH")
        ssl_key = os.getenv("FLEXT_WEB_SSL_KEY_PATH")

        return cls.create_web_config(
            host=os.getenv("FLEXT_WEB_HOST", FlextConstants.Platform.LOOPBACK_IP),
            port=int(
                os.getenv("FLEXT_WEB_PORT", str(FlextWebConstants.Web.DEFAULT_PORT))
            ),
            debug=False,
            secret_key=secret_key,
            enable_cors=False,
            cors_origins=[],
            ssl_enabled=bool(ssl_cert and ssl_key),
            ssl_cert_path=ssl_cert,
            ssl_key_path=ssl_key,
            session_cookie_secure=True,
            session_cookie_httponly=True,
            session_cookie_samesite="Strict",
            log_level=FlextConstants.Logging.WARNING,
        )

    @classmethod
    def create_test_config(cls) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Create enhanced test configuration."""
        return cls.create_web_config(
            host="localhost",
            port=0,  # Let OS assign port
            debug=False,
            secret_key=FlextWebConstants.WebSpecific.TEST_ENVIRONMENT_KEY,
            enable_cors=True,
            cors_origins=["*"],
            ssl_enabled=False,
            request_timeout=5,
            log_level=FlextConstants.Logging.INFO,
        )

    @classmethod
    def validate_web_config(
        cls, config: FlextWebConfigs.WebConfig
    ) -> FlextResult[None]:
        """Validate web configuration instance."""
        return config.validate_config()

    @classmethod
    def create_config_from_env(cls) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Create enhanced configuration from environment variables."""
        try:
            # Create configuration from environment
            config = cls.WebConfig()

            # Validate the configuration
            validation_result = config.validate_config()
            if validation_result.is_failure:
                return FlextResult.fail(
                    f"Environment configuration validation failed: {validation_result.error}"
                )

            return FlextResult.ok(config)
        except Exception as e:
            return FlextResult.fail(f"Failed to load config from environment: {e}")

    # =============================================================================
    # ENHANCED SINGLETON SETTINGS METHODS
    # =============================================================================

    _web_settings_instance: ClassVar[FlextWebConfigs.WebConfig | None] = None

    @classmethod
    def get_web_settings(cls) -> FlextWebConfigs.WebConfig:
        """Get enhanced singleton web settings instance."""
        if cls._web_settings_instance is None:
            # Create default settings from environment
            config_result = cls.create_config_from_env()
            if config_result.is_failure:
                # Fallback to development config if env loading fails
                config_result = cls.create_development_config()

            if config_result.is_failure:
                # Last resort - create minimal config
                cls._web_settings_instance = cls.WebConfig()
            else:
                cls._web_settings_instance = config_result.value

        return cls._web_settings_instance

    @classmethod
    def reset_web_settings(cls) -> None:
        """Reset singleton web settings instance."""
        cls._web_settings_instance = None

    @classmethod
    def create_web_system_configs(cls) -> FlextResult[dict[str, Any]]:
        """Create enhanced complete web system configurations."""
        try:
            web_config_result = cls.get_web_settings()

            system_configs: dict[str, Any] = {
                "web_config": web_config_result,
                "system_info": {
                    "version": web_config_result.version,
                    "environment": "development"
                    if web_config_result.debug
                    else "production",
                    "host": web_config_result.host,
                    "port": web_config_result.port,
                    "protocol": web_config_result.protocol,
                    "base_url": web_config_result.base_url,
                },
                "feature_flags": {
                    "enable_cors": web_config_result.enable_cors,
                    "debug_mode": web_config_result.debug,
                    "ssl_enabled": web_config_result.ssl_enabled,
                },
                "security_settings": {
                    "session_cookie_secure": web_config_result.session_cookie_secure,
                    "session_cookie_httponly": web_config_result.session_cookie_httponly,
                    "session_cookie_samesite": web_config_result.session_cookie_samesite,
                },
                "performance_settings": {
                    "max_content_length": web_config_result.max_content_length,
                    "request_timeout": web_config_result.request_timeout,
                },
            }

            return FlextResult.ok(system_configs)

        except Exception as e:
            return FlextResult.fail(f"Failed to create web system configs: {e}")

    @classmethod
    def merge_web_config(
        cls,
        base_config: FlextWebConfigs.WebConfig,
        overrides: dict[str, Any],
    ) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Enhanced web config merging with validation."""
        try:
            # Get current config as dict
            config_dict: dict[str, Any] = base_config.model_dump()

            # Apply overrides
            config_dict.update(overrides)

            # Create new config with merged data
            merged_config = cls.WebConfig.model_validate(config_dict)

            # Validate the merged configuration
            validation_result = merged_config.validate_config()
            if validation_result.is_failure:
                return FlextResult.fail(
                    f"Merged configuration validation failed: {validation_result.error}"
                )

            return FlextResult.ok(merged_config)

        except Exception as e:
            return FlextResult.fail(f"Failed to merge web config: {e}")


__all__ = [
    "FlextWebConfigs",
]
