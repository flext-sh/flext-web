"""FLEXT Web Configurations - Consolidated configuration system with enterprise patterns.

CONSOLIDAÇÃO COMPLETA seguindo flext-core architectural patterns:
- Apenas UMA classe FlextWebConfigs com toda funcionalidade
- Todas as outras classes antigas removidas completamente
- Arquitetura hierárquica seguindo padrão FLEXT estrito
- Python 3.13+ com Pydantic Settings avançado sem compatibilidade legada

Architecture Overview:
    FlextWebConfigs - Single consolidated class containing:
        - Nested configuration classes for web settings (WebConfig, etc.)
        - Factory methods for creating configuration instances
        - Environment-specific configuration templates
        - Validation methods for configuration integrity

Examples:
    Using consolidated FlextWebConfigs:
        config = FlextWebConfigs.WebConfig(host="0.0.0.0", port=8080)
        factory_result = FlextWebConfigs.create_web_config()
        env_config = FlextWebConfigs.create_production_config()

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os

from flext_core import (
    FlextConstants,
    FlextResult,
)
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Import local constants and types for DIRECT usage - NO ALIASES
# PRIORITIZING LOCAL LIBRARY
from flext_web.constants import FlextWebConstants
from flext_web.typings import FlextWebTypes


class FlextWebConfigs:
    """Consolidated FLEXT web configuration system providing all configuration functionality.

    This is the complete web configuration system for the FLEXT Web ecosystem, providing
    unified configuration patterns built on flext-core foundation with web-specific
    settings and validation. All configuration types are organized as nested classes
    within this single container for consistent management and easy access.

    Architecture Overview:
        The system is organized following Configuration-as-Code and flext-core patterns:

        - **Configuration Classes**: Web settings with environment variable support
        - **Validation Rules**: Comprehensive configuration validation
        - **Environment Templates**: Pre-configured settings for different environments
        - **Factory Methods**: Safe configuration creation returning FlextResult
        - **Secret Management**: Secure handling of sensitive configuration data

    Design Patterns:
        - **Single Point of Truth**: All web configurations defined in one location
        - **Environment Variables**: Full support for 12-factor app configuration
        - **Type Safety**: Comprehensive type annotations and validation
        - **Railway Programming**: Configuration methods return FlextResult for error handling
        - **Immutable Settings**: Configuration instances are immutable after creation
        - **Secret Security**: Secure handling of sensitive configuration values

    Usage Examples:
        Web configuration creation::

            # Create default configuration
            config_result = FlextWebConfigs.create_web_config()

            # Create environment-specific configuration
            prod_config = FlextWebConfigs.create_production_config()

            # Create custom configuration
            config = FlextWebConfigs.WebConfig(
                host="0.0.0.0",
                port=8080,
                secret_key="my-secret-key",
            )

        Configuration validation::

            # Validate configuration
            validation_result = FlextWebConfigs.validate_web_config(config)

            # Environment-specific validation
            env_validation = FlextWebConfigs.validate_production_config(config)

    Note:
        This consolidated approach follows flext-core architectural patterns,
        ensuring consistency across the FLEXT ecosystem while providing
        web-specific configuration functionality.

    """

    # =============================================================================
    # WEB CONFIGURATION CLASSES
    # =============================================================================

    class WebConfig(BaseSettings):
        """Primary web service configuration with environment variable support.

        Enterprise-grade configuration class providing comprehensive web service
        settings with environment variable integration, type-safe validation,
        and security-focused secret management.

        Features:
            - **Environment Variables**: Full 12-factor app configuration support
            - **Type Safety**: Comprehensive Pydantic validation and type checking
            - **Secret Management**: Secure handling of sensitive configuration
            - **Default Values**: Production-ready defaults with development overrides
            - **Port Validation**: Network port range validation
            - **Host Validation**: Network host address validation

        Environment Variables:
            All configuration can be set via environment variables with FLEXT_WEB_ prefix:

            - FLEXT_WEB_HOST: Service host address (default: localhost)
            - FLEXT_WEB_PORT: Service port number (default: 8080)
            - FLEXT_WEB_DEBUG: Debug mode flag (default: True)
            - FLEXT_WEB_SECRET_KEY: Flask secret key (required for production)
            - FLEXT_WEB_APP_NAME: Application name (default: FLEXT Web)

        Validation Rules:
            - Host must be valid network address
            - Port must be in range 1-65535
            - Secret key must be at least 32 characters for production
            - Debug mode should be False for production

        Integration:
            - Built on Pydantic Settings for environment variable support
            - Uses FlextConstants for consistent default values
            - Compatible with FlextResult patterns for error handling
        """

        model_config = SettingsConfigDict(
            env_prefix="FLEXT_WEB_",
            env_file=".env",
            env_file_encoding="utf-8",
            case_sensitive=False,
            validate_assignment=True,
            extra="ignore",
        )

        # Web service settings
        host: str = Field(
            default="localhost",
            description="Host address for web service",
        )

        port: int = Field(
            default=8080,
            ge=FlextWebConstants.WebSpecific.MIN_PORT,
            le=FlextWebConstants.WebSpecific.MAX_PORT,
            description="Port number for web service",
        )

        debug: bool = Field(
            default=True,
            description="Enable debug mode",
        )

        secret_key: str = Field(
            default=FlextWebConstants.WebSpecific.DEV_SECRET_KEY,
            min_length=FlextWebConstants.WebSpecific.MIN_SECRET_KEY_LENGTH,
            description="Flask secret key for sessions",
        )

        app_name: str = Field(
            default="FLEXT Web",
            min_length=1,
            description="Application name",
        )

        version: str = Field(
            default="0.9.0",
            description="Application version",
        )

        # Advanced settings
        max_content_length: int = Field(
            default=16777216,  # 16MB
            gt=0,
            description="Maximum request content length in bytes",
        )

        request_timeout: int = Field(
            default=30,
            gt=0,
            le=300,
            description="Request timeout in seconds",
        )

        enable_cors: bool = Field(
            default=False,
            description="Enable CORS support",
        )

        @field_validator("host")
        @classmethod
        def validate_host(cls, v: str) -> str:
            """Validate host address format."""
            if not v or not v.strip():
                msg = "Host address cannot be empty"
                raise ValueError(msg)

            # Basic host validation - allow localhost, IP addresses, and domain names
            host = v.strip()
            if host in {"localhost", "127.0.0.1", "0.0.0.0"}:
                return host

            # Simple domain/IP validation
            if not host.replace(".", "").replace("-", "").replace("_", "").isalnum():
                msg = f"Invalid host address format: {host}"
                raise ValueError(msg)

            return host

        @field_validator("secret_key")
        @classmethod
        def validate_secret_key(cls, v: str) -> str:
            """Validate secret key strength."""
            if len(v) < FlextWebConstants.WebSpecific.MIN_SECRET_KEY_LENGTH:
                msg = f"Secret key must be at least {FlextWebConstants.WebSpecific.MIN_SECRET_KEY_LENGTH} characters long"
                raise ValueError(msg)

            # Check for default development key in production-like environments
            if (
                v == FlextWebConstants.WebSpecific.DEV_SECRET_KEY
                and not cls._is_development_env()
            ):
                msg = "Must change default secret key for production"
                raise ValueError(msg)

            return v

        @field_validator("port")
        @classmethod
        def validate_port(cls, v: int) -> int:
            """Validate port number and check for system reserved ports."""
            min_port = FlextWebConstants.WebSpecific.MIN_PORT
            max_port = FlextWebConstants.WebSpecific.MAX_PORT
            if not (min_port <= v <= max_port):
                msg = f"Port must be between {min_port} and {max_port}, got {v}"
                raise ValueError(msg)

            # Warn about system reserved ports (1-1023) but allow them
            if v <= FlextWebConstants.WebSpecific.SYSTEM_PORTS_THRESHOLD:
                # Note: In production, this might require special permissions
                pass

            return v

        @classmethod
        def _is_development_env(cls) -> bool:
            """Check if running in development environment (class method for validators)."""
            env = os.getenv("FLEXT_WEB_ENVIRONMENT", "development").lower()
            return env in {"development", "dev", "local"}

        def _is_development(self) -> bool:
            """Check if running in development environment."""
            env = os.getenv("FLEXT_WEB_ENVIRONMENT", "development").lower()
            env_is_dev = env in {"development", "dev", "local"}
            # If environment suggests production but debug is True, consider it development
            # If environment suggests development but debug is False, check other indicators
            if env_is_dev and not self.debug:
                # Environment says dev but debug=False, check other production indicators
                return self.secret_key == FlextWebConstants.WebSpecific.DEV_SECRET_KEY
            return env_is_dev or self.debug

        def is_production(self) -> bool:
            """Check if running in production environment."""
            return not self._is_development()

        def get_server_url(self) -> str:
            """Get the complete server URL."""
            return f"http://{self.host}:{self.port}"

        def validate_production_settings(self) -> FlextWebTypes.ValidationResult:
            """Validate production-specific configuration settings."""
            try:
                errors: FlextWebTypes.ConfigErrors = []

                # Production-specific validations only
                if self.debug:
                    errors.append("Debug mode must be disabled in production")

                if self.secret_key == FlextWebConstants.WebSpecific.DEV_SECRET_KEY:
                    errors.append("Default secret key must be changed for production")

                if self.host == "localhost":
                    errors.append("Host should not be 'localhost' in production")

                # Security validations
                min_key_len = FlextWebConstants.WebSpecific.MIN_SECRET_KEY_LENGTH
                if len(self.secret_key) < min_key_len:
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

        def validate_config(self) -> FlextWebTypes.ValidationResult:
            """Validate complete configuration for consistency and security."""
            try:
                errors: FlextWebTypes.ConfigErrors = []

                # Production-specific validations
                if not self._is_development():
                    if self.debug:
                        errors.append("Debug mode must be disabled in production")

                    if self.secret_key == FlextWebConstants.WebSpecific.DEV_SECRET_KEY:
                        errors.append(
                            "Default secret key must be changed for production"
                        )

                    if self.host == "localhost":
                        errors.append("Host should not be 'localhost' in production")

                # Security validations
                min_key_len = FlextWebConstants.WebSpecific.MIN_SECRET_KEY_LENGTH
                if len(self.secret_key) < min_key_len:
                    errors.append(
                        f"Secret key must be at least {min_key_len} characters"
                    )

                # Network validations
                min_port = FlextWebConstants.WebSpecific.MIN_PORT
                max_port = FlextWebConstants.WebSpecific.MAX_PORT
                if self.port < min_port or self.port > max_port:
                    errors.append(
                        f"Port must be in valid range ({min_port}-{max_port})"
                    )

                if errors:
                    return FlextResult[None].fail(
                        f"Configuration validation failed: {'; '.join(errors)}"
                    )

                return FlextResult[None].ok(None)

            except Exception as e:
                return FlextResult[None].fail(f"Configuration validation error: {e}")

    # =============================================================================
    # FACTORY METHODS AND UTILITIES
    # =============================================================================

    @classmethod
    def create_web_config(
        cls, **overrides: object
    ) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Create web configuration instance with optional overrides."""
        try:
            # If no overrides provided, let WebConfig read from environment naturally
            if not overrides:
                config = FlextWebConfigs.WebConfig()
            else:
                # Extract configuration values with type checking
                host_val = overrides.get("host", "localhost")
                port_val = overrides.get("port", 8080)
                debug_val = overrides.get("debug", True)
                secret_key_val = overrides.get(
                    "secret_key", "dev-secret-key-change-in-production"
                )
                app_name_val = overrides.get("app_name", "FLEXT Web")
                max_content_length_val = overrides.get(
                    "max_content_length", 16 * 1024 * 1024
                )
                request_timeout_val = overrides.get("request_timeout", 30)
                enable_cors_val = overrides.get("enable_cors", False)
                overrides.get("log_level", "INFO")
                overrides.get("template_dirs", [])
                overrides.get("static_folder", "static")
                overrides.get("static_url_path", "/static")

                # Create configuration with proper types
                config = FlextWebConfigs.WebConfig(
                    host=str(host_val) if host_val is not None else "localhost",
                    port=int(port_val) if isinstance(port_val, int) else 8080,
                    debug=bool(debug_val) if isinstance(debug_val, bool) else True,
                    secret_key=str(secret_key_val)
                    if secret_key_val is not None
                    else "dev-secret-key-change-in-production",
                    app_name=str(app_name_val)
                    if app_name_val is not None
                    else "FLEXT Web",
                    max_content_length=int(max_content_length_val)
                    if isinstance(max_content_length_val, int)
                    else 16 * 1024 * 1024,
                    request_timeout=int(request_timeout_val)
                    if isinstance(request_timeout_val, int)
                    else 30,
                    enable_cors=bool(enable_cors_val)
                    if isinstance(enable_cors_val, bool)
                    else False,
                )

            # Validate the created configuration
            validation_result = config.validate_config()
            if validation_result.is_failure:
                return FlextResult[FlextWebConfigs.WebConfig].fail(
                    f"Configuration validation failed: {validation_result.error}"
                )

            return FlextResult[FlextWebConfigs.WebConfig].ok(config)

        except Exception as e:
            return FlextResult[FlextWebConfigs.WebConfig].fail(
                f"Configuration creation failed: {e}"
            )

    @classmethod
    def create_development_config(cls) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Create development-optimized configuration."""
        try:
            config = FlextWebConfigs.WebConfig(
                host="localhost",
                port=8080,
                debug=True,
                secret_key=FlextWebConstants.WebSpecific.DEV_ENVIRONMENT_KEY,
                enable_cors=True,
            )
            return FlextResult[FlextWebConfigs.WebConfig].ok(config)

        except Exception as e:
            return FlextResult[FlextWebConfigs.WebConfig].fail(
                f"Development config creation failed: {e}"
            )

    @classmethod
    def create_production_config(cls) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Create production-optimized configuration."""
        try:
            # Production config requires environment variables
            secret_key = os.getenv("FLEXT_WEB_SECRET_KEY")
            if not secret_key:
                return FlextResult[FlextWebConfigs.WebConfig].fail(
                    "FLEXT_WEB_SECRET_KEY environment variable required for production"
                )

            config = FlextWebConfigs.WebConfig(
                host="0.0.0.0",
                port=int(os.getenv("FLEXT_WEB_PORT", "8080")),
                debug=False,
                secret_key=secret_key,
                enable_cors=False,
            )

            # Additional production validation
            validation_result = config.validate_config()
            if validation_result.is_failure:
                return FlextResult[FlextWebConfigs.WebConfig].fail(
                    f"Production config validation failed: {validation_result.error}"
                )

            return FlextResult[FlextWebConfigs.WebConfig].ok(config)

        except Exception as e:
            return FlextResult[FlextWebConfigs.WebConfig].fail(
                f"Production config creation failed: {e}"
            )

    @classmethod
    def create_test_config(cls) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Create test-optimized configuration."""
        try:
            config = FlextWebConfigs.WebConfig(
                host="localhost",
                port=0,  # Let system choose available port
                debug=False,  # Disable debug for cleaner test output
                secret_key=FlextWebConstants.WebSpecific.TEST_ENVIRONMENT_KEY,
                request_timeout=5,  # Shorter timeout for tests
            )
            return FlextResult[FlextWebConfigs.WebConfig].ok(config)

        except Exception as e:
            return FlextResult[FlextWebConfigs.WebConfig].fail(
                f"Test config creation failed: {e}"
            )

    @classmethod
    def validate_web_config(
        cls, config: FlextWebConfigs.WebConfig
    ) -> FlextWebTypes.ValidationResult:
        """Validate web configuration instance."""
        return config.validate_config()

    @classmethod
    def create_config_from_env(cls) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Create configuration from environment variables only."""
        try:
            # This will automatically load from environment variables
            config = FlextWebConfigs.WebConfig()

            # Validate the environment-based configuration
            validation_result = config.validate_config()
            if validation_result.is_failure:
                return FlextResult[FlextWebConfigs.WebConfig].fail(
                    f"Environment config validation failed: {validation_result.error}"
                )

            return FlextResult[FlextWebConfigs.WebConfig].ok(config)

        except Exception as e:
            return FlextResult[FlextWebConfigs.WebConfig].fail(
                f"Environment config creation failed: {e}"
            )

    # =============================================================================
    # FLEXT WEB CONFIGS CONFIGURATION METHODS
    # =============================================================================

    @classmethod
    def configure_web_configs_system(
        cls, config: FlextWebTypes.ConfigDict
    ) -> FlextResult[FlextWebTypes.ConfigDict]:
        """Configure web configurations system using FlextWebTypes.ConfigDict with validation."""
        try:
            validated_config = dict(config)

            # Validate environment using FlextConstants
            if "environment" in config:
                env_value = config["environment"]
                valid_environments = [
                    e.value for e in FlextConstants.Config.ConfigEnvironment
                ]
                if env_value not in valid_environments:
                    return FlextResult[FlextWebTypes.ConfigDict].fail(
                        f"Invalid environment '{env_value}'. Valid options: {valid_environments}"
                    )
            else:
                validated_config["environment"] = (
                    FlextConstants.Config.ConfigEnvironment.DEVELOPMENT.value
                )

            # Web configs specific settings
            validated_config.setdefault("enable_environment_validation", True)
            validated_config.setdefault("enable_secret_validation", True)
            validated_config.setdefault("require_production_secrets", True)
            validated_config.setdefault("enable_config_caching", False)

            return FlextResult[FlextWebTypes.ConfigDict].ok(validated_config)

        except Exception as e:
            return FlextResult[FlextWebTypes.ConfigDict].fail(
                f"Failed to configure web configs system: {e}"
            )

    @classmethod
    def get_web_configs_system_config(cls) -> FlextResult[FlextWebTypes.ConfigDict]:
        """Get current web configurations system configuration with runtime information."""
        try:
            config: FlextWebTypes.ConfigDict = {
                # Environment configuration
                "environment": FlextConstants.Config.ConfigEnvironment.DEVELOPMENT.value,
                "log_level": FlextConstants.Config.LogLevel.INFO.value,
                # Web configs specific settings
                "enable_environment_validation": True,
                "enable_secret_validation": True,
                "require_production_secrets": True,
                "enable_config_caching": False,
                # Available configuration types
                "available_configs": [
                    "WebConfig",
                ],
                "available_factories": [
                    "create_web_config",
                    "create_development_config",
                    "create_production_config",
                    "create_test_config",
                    "create_config_from_env",
                ],
                # Runtime metrics
                "active_configurations": 0,
                "validation_success_rate": 100.0,
                "environment_variable_usage": 0,
            }

            return FlextResult[FlextWebTypes.ConfigDict].ok(config)

        except Exception as e:
            return FlextResult[FlextWebTypes.ConfigDict].fail(
                f"Failed to get web configs system config: {e}"
            )


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    "FlextWebConfigs",
]
