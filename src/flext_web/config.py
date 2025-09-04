"""FLEXT Web Configurations - Consolidated configuration system with enterprise patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os
import warnings
from typing import ClassVar

from flext_core import (
    FlextConfig,
    FlextConstants,
    FlextMixins,
    FlextResult,
)
from pydantic import (
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from flext_web.constants import FlextWebConstants
from flext_web.typings import FlextWebTypes


class FlextWebConfigs:
    """Consolidated FLEXT web configuration system providing all configuration functionality.

    This is the complete web configuration system for the FLEXT Web ecosystem, providing
    unified configuration patterns built on flext-core foundation with web-specific
    settings and validation. All configuration types are organized as nested classes
    within this single container for consistent management and easy access.


    """

    # =============================================================================
    # WEB CONFIGURATION CLASSES
    # =============================================================================

    class WebConfig(FlextConfig):
        """Primary web service configuration with environment variable support.

        Enterprise-grade configuration class providing comprehensive web service
        settings with environment variable integration, type-safe validation,
        and security-focused secret management.
        """

        model_config: ClassVar[ConfigDict] = ConfigDict(
            validate_assignment=True,
            extra="allow",
        )

        # Web service settings
        host: str = Field(
            default="localhost",
            description="Host address for web service",
        )

        port: int = Field(
            default=8080,
            ge=FlextConstants.Web.MIN_PORT,
            le=FlextConstants.Web.MAX_PORT,
            description="Port number for web service",
        )

        debug: bool = Field(
            default=True,
            description="Enable debug mode",
        )

        secret_key: str = Field(
            default=FlextWebConstants.WebSpecific.DEV_SECRET_KEY,
            min_length=FlextConstants.Validation.MIN_SECRET_KEY_LENGTH,
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
            default=16777216,
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
            # Note: 0.0.0.0 binding is intentionally allowed for development/container deployments
            host = v.strip()
            if host in {"localhost", "127.0.0.1", "0.0.0.0"}:  # nosec B104  # noqa: S104
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
            if len(v) < FlextConstants.Validation.MIN_SECRET_KEY_LENGTH:
                msg = f"Secret key must be at least {FlextConstants.Validation.MIN_SECRET_KEY_LENGTH} characters long"
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
            min_port = FlextConstants.Web.MIN_PORT
            max_port = FlextConstants.Web.MAX_PORT
            if not (min_port <= v <= max_port):
                msg = f"Port must be between {min_port} and {max_port}, got {v}"
                raise ValueError(msg)

            # Warn about system reserved ports (1-1023) but allow them
            if v <= FlextWebConstants.WebSpecific.SYSTEM_PORTS_THRESHOLD:
                # Note: In production, this might require special permissions
                warnings.warn(
                    f"Using system reserved port {v}. May require special permissions in production.",
                    UserWarning,
                    stacklevel=2
                )

            return v

        @model_validator(mode="before")
        @classmethod
        def load_from_env(cls, values: dict[str, object]) -> dict[str, object]:
            """Load configuration from environment variables with proper validation."""
            # Only load from env if not explicitly provided
            # Convert to set for more reliable membership testing
            provided_fields = set(values.keys())

            env_mapping = {
                "host": ("FLEXT_WEB_HOST", str),
                "port": ("FLEXT_WEB_PORT", int),
                "debug": ("FLEXT_WEB_DEBUG", bool),
                "secret_key": ("FLEXT_WEB_SECRET_KEY", str),
                "app_name": ("FLEXT_WEB_APP_NAME", str),
                "max_content_length": ("FLEXT_WEB_MAX_CONTENT_LENGTH", int),
                "request_timeout": ("FLEXT_WEB_REQUEST_TIMEOUT", int),
                "enable_cors": ("FLEXT_WEB_ENABLE_CORS", bool),
            }

            for field_name, (env_var, field_type) in env_mapping.items():
                # Skip if field was explicitly provided
                if field_name in provided_fields:
                    continue
                # Only load from env if env var exists
                if env_var in os.environ:
                    env_value = os.environ[env_var]
                    try:
                        if field_type is int:
                            values[field_name] = int(env_value)
                        elif field_type is bool:
                            if env_value.lower() not in {"true", "false"}:
                                msg = f"Boolean must be 'true' or 'false', got '{env_value}'"
                                raise ValueError(msg)
                            values[field_name] = env_value.lower() == "true"
                        else:  # str
                            values[field_name] = env_value
                    except ValueError as e:
                        msg = f"Invalid {field_type.__name__} value for {env_var}: {env_value}"
                        raise ValueError(msg) from e

            return values

        def model_post_init(self, __context: object, /) -> None:
            """Post-init hook to set up FlextMixins functionality."""
            # Initialize FlextMixins features
            FlextMixins.create_timestamp_fields(self)
            FlextMixins.ensure_id(self)
            FlextMixins.initialize_validation(self)
            FlextMixins.initialize_state(self, "configured")

            # Log configuration creation with security-safe logging
            FlextMixins.log_operation(
                self,
                "config_initialized",
                host=self.host,
                port=self.port,
                debug=self.debug,
                is_production=self.is_production(),
                # Exclude secret_key from logs for security
            )

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

        def validate_production_settings(
            self,
        ) -> FlextWebTypes.ValidationResult:
            """Validate production-specific configuration settings."""
            try:
                FlextMixins.log_operation(
                    self,
                    "validate_production_settings",
                    is_production=self.is_production(),
                )

                errors: FlextWebTypes.ConfigErrors = []

                # Production-specific validations only
                if self.debug:
                    errors.append("Debug mode must be disabled in production")

                if self.secret_key == FlextWebConstants.WebSpecific.DEV_SECRET_KEY:
                    errors.append("Default secret key must be changed for production")

                if self.host == "localhost":
                    errors.append("Host should not be 'localhost' in production")

                # Security validations
                min_key_len = FlextConstants.Validation.MIN_SECRET_KEY_LENGTH
                if len(self.secret_key) < min_key_len:
                    errors.append(
                        f"Secret key must be at least {min_key_len} characters"
                    )

                if errors:
                    FlextMixins.log_operation(
                        self, "production_validation_failed", error_count=len(errors)
                    )
                    return FlextResult[None].fail(
                        f"Production configuration validation failed: {'; '.join(errors)}"
                    )

                FlextMixins.log_operation(
                    self, "production_validation_success", validated=True
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
                min_key_len = FlextConstants.Validation.MIN_SECRET_KEY_LENGTH
                if len(self.secret_key) < min_key_len:
                    errors.append(
                        f"Secret key must be at least {min_key_len} characters"
                    )

                # Network validations
                min_port = FlextConstants.Web.MIN_PORT
                max_port = FlextConstants.Web.MAX_PORT
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
        # FLEXT CONFIG METHODS - Inherited and specialized
        # =============================================================================

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate web-specific business rules."""
            try:
                # Validate production constraints - only block 'localhost', 127.0.0.1 is valid for containers
                if not self.debug and self.host == "localhost":
                    return FlextResult[None].fail(
                        "Production mode cannot use 'localhost' binding, use specific IP address"
                    )

                # Validate secret key strength in production
                if (
                    not self.debug
                    and self.secret_key == FlextWebConstants.WebSpecific.DEV_SECRET_KEY
                ):
                    return FlextResult[None].fail(
                        "Production mode cannot use development secret key"
                    )

                # Validate CORS settings
                if self.enable_cors and not self.debug:
                    return FlextResult[None].fail(
                        "CORS should be disabled in production for security"
                    )

                return FlextResult[None].ok(None)

            except Exception as e:
                return FlextResult[None].fail(f"Business rules validation error: {e}")

        @classmethod
        def create_with_validation(
            cls,
            overrides: dict[str, object] | None = None,
            **kwargs: object,
        ) -> FlextResult[FlextWebConfigs.WebConfig]:
            """Create WebConfig instance with validation and proper override handling."""
            try:
                # Prepare overrides dict
                all_overrides: dict[str, object] = {}
                if overrides:
                    all_overrides.update(overrides)
                all_overrides.update(kwargs)

                # Create instance with overrides using ternary operator
                instance = cls(**all_overrides) if all_overrides else cls()  # type: ignore[arg-type]

                # Validate business rules
                validation_result = instance.validate_business_rules()
                if validation_result.is_failure:
                    return FlextResult["FlextWebConfigs.WebConfig"].fail(
                        f"Business rules validation failed: {validation_result.error}"
                    )

                return FlextResult["FlextWebConfigs.WebConfig"].ok(instance)

            except Exception as e:
                return FlextResult["FlextWebConfigs.WebConfig"].fail(
                    f"Configuration creation failed: {e}"
                )

        def get_config_summary(self) -> dict[str, object]:
            """Get configuration summary for logging and debugging."""
            return {
                "host": self.host,
                "port": self.port,
                "debug": self.debug,
                "app_name": self.app_name,
                "version": self.version,
                "enable_cors": self.enable_cors,
                "max_content_length": self.max_content_length,
                "request_timeout": self.request_timeout,
            }

        def is_development(self) -> bool:
            """Check if running in development mode."""
            return self.debug

    # =============================================================================
    # FACTORY METHODS AND UTILITIES
    # =============================================================================

    @classmethod
    def _create_config_builder(cls, **overrides: object) -> dict[str, object]:
        """Advanced Builder pattern for configuration construction.

        Reduces complexity from 61 to ~20 by eliminating repetitive type checking
        and using functional composition with Python 3.13 features.
        """
        # Configuration schema with defaults
        config_schema = {
            "host": "localhost",
            "port": 8080,
            "debug": True,
            "secret_key": "dev-secret-key-change-in-production",
            "app_name": "FLEXT Web",
            "max_content_length": 16 * 1024 * 1024,
            "request_timeout": 30,
            "enable_cors": False,
        }

        # Build configuration using overrides
        return {
            key: overrides.get(key, default) for key, default in config_schema.items()
        }

    @classmethod
    def _validate_and_finalize_config(
        cls,
        config: FlextWebConfigs.WebConfig,
        factory_method: str,
        *,
        has_overrides: bool,
    ) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Finalize configuration with validation and logging."""
        # Validate configuration
        validation_result = config.validate_config()
        if validation_result.is_failure:
            return FlextResult[FlextWebConfigs.WebConfig].fail(
                f"Configuration validation failed: {validation_result.error}"
            )

        # Log successful creation
        FlextMixins.log_operation(
            config,
            "web_config_created",
            factory_method=factory_method,
            has_overrides=has_overrides,
        )

        return FlextResult[FlextWebConfigs.WebConfig].ok(config)

    @classmethod
    def create_web_config(
        cls, **overrides: object
    ) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Create web configuration instance with optional overrides using FlextConfig patterns."""
        try:
            # Use FlextConfig's create_with_validation method
            return FlextWebConfigs.WebConfig.create_with_validation(
                overrides=dict(overrides)
            )

        except Exception as e:
            return FlextResult[FlextWebConfigs.WebConfig].fail(
                f"Configuration creation failed: {e}"
            )

    # Consolidated factory methods using aliases - reduces duplication
    @classmethod
    def create_development_config(cls) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Create development configuration."""
        return cls.create_web_config(
            host="localhost",
            port=8080,
            debug=True,
            secret_key=FlextWebConstants.WebSpecific.DEV_ENVIRONMENT_KEY,
            enable_cors=True,
        )

    @classmethod
    def create_production_config(cls) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Create production configuration."""
        secret_key = os.getenv("FLEXT_WEB_SECRET_KEY")
        if not secret_key:
            return FlextResult[FlextWebConfigs.WebConfig].fail(
                "FLEXT_WEB_SECRET_KEY required for production"
            )
        return cls.create_web_config(
            host=os.getenv("FLEXT_WEB_HOST", "0.0.0.0"),  # Use 0.0.0.0 for production binding  # noqa: S104
            port=int(os.getenv("FLEXT_WEB_PORT", "8080")),
            debug=False,
            secret_key=secret_key,
            enable_cors=False,
        )

    @classmethod
    def create_test_config(cls) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Create test configuration."""
        return cls.create_web_config(
            host="localhost",
            port=0,
            debug=False,
            secret_key=FlextWebConstants.WebSpecific.TEST_ENVIRONMENT_KEY,
            request_timeout=5,
        )

    @classmethod
    def validate_web_config(
        cls, config: FlextWebConfigs.WebConfig
    ) -> FlextWebTypes.ValidationResult:
        """Validate web configuration instance."""
        return config.validate_config()

    @classmethod
    def create_config_from_env(cls) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Create configuration from environment variables."""
        return FlextWebConfigs.WebConfig.create_with_validation()

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
    def get_web_configs_system_config(
        cls,
    ) -> FlextResult[FlextWebTypes.ConfigDict]:
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


__all__ = [
    "FlextWebConfigs",
]
