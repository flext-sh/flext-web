"""FLEXT Web Configurations - Consolidated configuration system with enterprise patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import logging
import os
import warnings
from typing import ClassVar

from pydantic import (
    Field,
    field_validator,
    model_validator,
)

from flext_core import (
    FlextConfig,
    FlextConstants,
    FlextResult,
    FlextTypes,
)
from flext_web.constants import FlextWebConstants

# from flext_web.settings import FlextWebSettings  # Removed to fix circular import

_logger = logging.getLogger(__name__)


def _get_flext_web_settings() -> type | None:
    """Get FlextWebSettings class if available.

    Returns:
        FlextWebSettings class or None if not available

    """
    try:
        from flext_web.settings import FlextWebSettings

        return FlextWebSettings
    except ImportError:
        return None


def _web_settings_available() -> bool:
    """Check if FlextWebSettings is available.

    Returns:
        True if FlextWebSettings can be imported, False otherwise

    """
    return _get_flext_web_settings() is not None


# Settings availability flag
_web_settings_available_flag = _web_settings_available()


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

        model_config = FlextConfig.model_config.copy()
        model_config.update(
            {
                "validate_assignment": True,
                "extra": "allow",
            },
        )

        # Web service settings
        host: str = Field(
            default="localhost",
            description="Host address for web service",
        )

        port: int = Field(
            default=FlextConstants.Platform.FLEXT_API_PORT,  # Using FlextConstants as SOURCE OF TRUTH
            ge=FlextWebConstants.Web.MIN_PORT,
            le=FlextWebConstants.Web.MAX_PORT,
            description="Port number for web service",
        )

        debug: bool = Field(
            default=False,
            description="Enable debug mode",
        )

        @field_validator("debug", mode="before")
        @classmethod
        def validate_debug(cls, value: object) -> bool:
            """Validate debug field, converting string values."""
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.lower() in {"true", "1", "yes", "on"}
            # For other types, convert to bool
            return bool(value)

        @property
        def debug_bool(self) -> bool:
            """Get debug value as boolean (guaranteed to be bool after validation)."""
            # The validator ensures this is always bool, but MyPy needs help understanding this
            return bool(self.debug)

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
            default=FlextConstants.Limits.MAX_FILE_SIZE,  # Using FlextConstants as SOURCE OF TRUTH
            gt=0,
            description="Maximum request content length in bytes",
        )

        request_timeout: int = Field(
            default=FlextConstants.Network.DEFAULT_TIMEOUT,  # Using FlextConstants as SOURCE OF TRUTH
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
        def validate_host(cls, value: str) -> str:
            """Validate host address format."""
            if not value or not value.strip():
                msg = "Host address cannot be empty"
                raise ValueError(msg)

            # Basic host validation - allow localhost, IP addresses, and domain names
            host = value.strip()

            # Allow localhost and local IPs for development
            if host in {"localhost", "127.0.0.1"}:
                return host

            # For production, require explicit host configuration
            # Replace binding to all interfaces with localhost for security
            if host == FlextWebConstants.WebSpecific.ALL_INTERFACES:
                # Only allow 0.0.0.0 in development mode
                if os.getenv("FLEXT_DEVELOPMENT_MODE", "false").lower() == "true":
                    return host
                # In production, use localhost instead
                return "127.0.0.1"

            if not host.replace(".", "").replace("-", "").replace("_", "").isalnum():
                msg = f"Invalid host address format: {host}"
                raise ValueError(msg)

            return host

        @field_validator("secret_key")
        @classmethod
        def validate_secret_key(cls, value: str) -> str:
            """Validate secret key strength."""
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

            return value

        @field_validator("port")
        @classmethod
        def validate_port(cls, value: int) -> int:
            """Validate port number and check for system reserved ports."""
            min_port = FlextWebConstants.Web.MIN_PORT
            max_port = FlextWebConstants.Web.MAX_PORT
            if not (min_port <= value <= max_port):
                msg = f"Port must be between {min_port} and {max_port}, got {value}"
                raise ValueError(msg)

            # Warn about system reserved ports (1-1023) but allow them
            if value <= FlextWebConstants.WebSpecific.SYSTEM_PORTS_THRESHOLD:
                # Note: In production, this might require special permissions
                warnings.warn(
                    f"Using system reserved port {value}. May require special permissions in production.",
                    UserWarning,
                    stacklevel=2,
                )

            return value

        @model_validator(mode="before")
        @classmethod
        def load_from_env(cls, values: FlextTypes.Core.Dict) -> FlextTypes.Core.Dict:
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
            """Post-init hook to set up configuration."""
            # Initialize configuration state
            self._initialized = True

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
            if env_is_dev and not self.debug_bool:
                # Environment says dev but debug=False, check other production indicators
                return self.secret_key == FlextWebConstants.WebSpecific.DEV_SECRET_KEY
            return env_is_dev or self.debug_bool

        def is_production(self) -> bool:
            """Check if running in production environment."""
            return not self._is_development()

        def get_server_url(self) -> str:
            """Get the complete server URL."""
            return f"http://{self.host}:{self.port}"

        def validate_production_settings(
            self,
        ) -> FlextResult[None]:
            """Validate production-specific configuration settings."""
            try:
                # Log production validation start

                errors: FlextTypes.Core.StringList = []

                # Production-specific validations only
                if self.debug_bool:
                    errors.append("Debug mode must be disabled in production")

                if self.secret_key == FlextWebConstants.WebSpecific.DEV_SECRET_KEY:
                    errors.append("Default secret key must be changed for production")

                if self.host == "localhost":
                    errors.append("Host should not be 'localhost' in production")

                # Security validations
                min_key_len = FlextConstants.Validation.MIN_SECRET_KEY_LENGTH
                if len(self.secret_key) < min_key_len:
                    errors.append(
                        f"Secret key must be at least {min_key_len} characters",
                    )

                if errors:
                    # Log production validation failure
                    return FlextResult[None].fail(
                        f"Production configuration validation failed: {'; '.join(errors)}",
                    )

                # Log production validation success
                return FlextResult[None].ok(None)

            except Exception as e:
                return FlextResult[None].fail(f"Production validation error: {e}")

        def validate_config(self) -> FlextResult[None]:
            """Validate complete configuration for consistency and security."""
            try:
                errors: FlextTypes.Core.StringList = []

                # Production-specific validations
                if not self._is_development():
                    if self.debug_bool:
                        errors.append("Debug mode must be disabled in production")

                    if self.secret_key == FlextWebConstants.WebSpecific.DEV_SECRET_KEY:
                        errors.append(
                            "Default secret key must be changed for production",
                        )

                    if self.host == "localhost":
                        errors.append("Host should not be 'localhost' in production")

                # Security validations
                min_key_len = FlextConstants.Validation.MIN_SECRET_KEY_LENGTH
                if len(self.secret_key) < min_key_len:
                    errors.append(
                        f"Secret key must be at least {min_key_len} characters",
                    )

                # Network validations
                min_port = FlextWebConstants.Web.MIN_PORT
                max_port = FlextWebConstants.Web.MAX_PORT
                if self.port < min_port or self.port > max_port:
                    errors.append(
                        f"Port must be in valid range ({min_port}-{max_port})",
                    )

                if errors:
                    return FlextResult[None].fail(
                        f"Configuration validation failed: {'; '.join(errors)}",
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
                if not self.debug_bool and self.host == "localhost":
                    return FlextResult[None].fail(
                        "Production mode cannot use 'localhost' binding, use specific IP address",
                    )

                # Validate secret key strength in production
                if (
                    not self.debug_bool
                    and self.secret_key == FlextWebConstants.WebSpecific.DEV_SECRET_KEY
                ):
                    return FlextResult[None].fail(
                        "Production mode cannot use development secret key",
                    )

                # Validate CORS settings
                if self.enable_cors and not self.debug_bool:
                    return FlextResult[None].fail(
                        "CORS should be disabled in production for security",
                    )

                return FlextResult[None].ok(None)

            except Exception as e:
                return FlextResult[None].fail(f"Business rules validation error: {e}")

        @classmethod
        def create_with_validation(
            cls,
            overrides: FlextTypes.Core.Dict | None = None,
            **kwargs: object,
        ) -> FlextResult[FlextWebConfigs.WebConfig]:
            """Create WebConfig instance with validation and proper override handling."""
            try:
                # Prepare overrides dict
                all_overrides: FlextTypes.Core.Dict = {}
                if overrides:
                    all_overrides.update(overrides)
                all_overrides.update(kwargs)

                # Create instance with overrides using ternary operator
                # Use model_validate to safely handle FlextTypes.Core.Dict -> Pydantic model
                instance = cls.model_validate(all_overrides) if all_overrides else cls()

                # Validate business rules
                validation_result = instance.validate_business_rules()
                if validation_result.is_failure:
                    return FlextResult["FlextWebConfigs.WebConfig"].fail(
                        f"Business rules validation failed: {validation_result.error}",
                    )

                return FlextResult["FlextWebConfigs.WebConfig"].ok(instance)

            except Exception as e:
                return FlextResult["FlextWebConfigs.WebConfig"].fail(
                    f"Configuration creation failed: {e}",
                )

        def get_config_summary(self) -> FlextTypes.Core.Dict:
            """Get configuration summary for logging and debugging."""
            return {
                "host": self.host,
                "port": self.port,
                "debug": self.debug_bool,
                "app_name": self.app_name,
                "version": self.version,
                "enable_cors": self.enable_cors,
                "max_content_length": self.max_content_length,
                "request_timeout": self.request_timeout,
            }

        def is_development(self) -> bool:
            """Check if running in development mode."""
            return self.debug_bool

    # =============================================================================
    # FACTORY METHODS AND UTILITIES
    # =============================================================================

    @classmethod
    def _create_config_builder(cls, **overrides: object) -> FlextTypes.Core.Dict:
        """Advanced Builder pattern for configuration construction.

        Reduces complexity from 61 to ~20 by eliminating repetitive type checking
        and using functional composition with Python 3.13 features.

        Returns:
            FlextTypes.Core.Dict:: Description of return value.

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
        _factory_method: str,
        *,
        _has_overrides: bool,
    ) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Finalize configuration with validation and logging."""
        # Validate configuration
        validation_result = config.validate_config()
        if validation_result.is_failure:
            return FlextResult[FlextWebConfigs.WebConfig].fail(
                f"Configuration validation failed: {validation_result.error}",
            )

        # Log successful creation
        # Log web config creation

        return FlextResult[FlextWebConfigs.WebConfig].ok(config)

    @classmethod
    def create_web_config(
        cls,
        **overrides: object,
    ) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Create web configuration instance with optional overrides using FlextConfig patterns."""
        try:
            # Use FlextConfig's create_with_validation method
            return FlextWebConfigs.WebConfig.create_with_validation(
                overrides=dict(overrides),
            )

        except Exception as e:
            return FlextResult[FlextWebConfigs.WebConfig].fail(
                f"Configuration creation failed: {e}",
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
                "FLEXT_WEB_SECRET_KEY required for production",
            )
        return cls.create_web_config(
            host=os.getenv(
                "FLEXT_WEB_HOST",
                "127.0.0.1",  # Use localhost instead of 0.0.0.0 for security
            ),
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
        cls,
        config: FlextWebConfigs.WebConfig,
    ) -> FlextResult[None]:
        """Validate web configuration instance."""
        return config.validate_config()

    @classmethod
    def create_config_from_env(cls) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Create configuration from environment variables."""
        flext_web_settings = _get_flext_web_settings()
        if not _web_settings_available_flag or flext_web_settings is None:
            return FlextResult[FlextWebConfigs.WebConfig].fail(
                "FlextWebSettings not available - import failed",
            )

        try:
            # Use FlextWebSettings to load from environment
            settings = flext_web_settings()
            config_result = settings.to_config()
            if config_result.is_failure:
                return FlextResult[FlextWebConfigs.WebConfig].fail(
                    config_result.error or "Unknown error",
                )

            # Type narrowing for config_result.unwrap()
            config_obj = config_result.unwrap()
            if not isinstance(config_obj, cls.WebConfig):
                return FlextResult[FlextWebConfigs.WebConfig].fail(
                    "Invalid config object type returned from settings",
                )

            return FlextResult[FlextWebConfigs.WebConfig].ok(config_obj)
        except Exception as e:
            return FlextResult[FlextWebConfigs.WebConfig].fail(
                f"Failed to load config from environment: {e}",
            )

    # =============================================================================
    # FLEXT WEB CONFIGS CONFIGURATION METHODS
    # =============================================================================

    @classmethod
    def configure_web_configs_system(
        cls,
        config: FlextTypes.Core.Dict,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Configure web configurations system using FlextWebTypes.ConfigDict with validation."""
        try:
            validated_config = dict(config)

            # Validate environment using flext-core enums first
            if "environment" in config:
                env_value = config["environment"]
                valid_environments = [
                    e.value for e in FlextConstants.Environment.ConfigEnvironment
                ]
                if env_value not in valid_environments:
                    return FlextResult[FlextTypes.Core.Dict].fail(
                        f"Invalid environment '{env_value}'. Valid options: {valid_environments}",
                    )
            else:
                validated_config["environment"] = (
                    FlextConstants.Environment.ConfigEnvironment.DEVELOPMENT.value
                )

            # Core validation completed successfully

            # Get FlextWebSettings class
            flext_web_settings = _get_flext_web_settings()
            if not _web_settings_available_flag or flext_web_settings is None:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    "FlextWebSettings not available - import failed",
                )

            # Create settings using Pydantic model validation
            try:
                settings_obj = flext_web_settings.model_validate(validated_config)
                settings_res = FlextResult[FlextWebSettings].ok(settings_obj)
            except Exception as e:
                settings_res = FlextResult[FlextWebSettings].fail(
                    f"Settings validation failed: {e}",
                )
            if settings_res.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    settings_res.error or "Failed to build WebSettings",
                )
            cfg_res = settings_res.value.to_config()
            if cfg_res.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    cfg_res.error or "Failed to validate WebConfig",
                )

            # Type narrowing for cfg_res.value
            config_obj = cfg_res.value
            if not isinstance(config_obj, cls.WebConfig):
                return FlextResult[FlextTypes.Core.Dict].fail(
                    "Invalid config object type returned",
                )
            validated_config = config_obj.model_dump()

            # Web configs specific settings
            validated_config.setdefault("enable_environment_validation", True)
            validated_config.setdefault("enable_secret_validation", True)
            validated_config.setdefault("require_production_secrets", True)
            validated_config.setdefault("enable_config_caching", False)

            return FlextResult[FlextTypes.Core.Dict].ok(validated_config)

        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Failed to configure web configs system: {e}",
            )

    @classmethod
    def get_web_configs_system_config(
        cls,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Get current web configurations system configuration with runtime information."""
        try:
            config: FlextTypes.Core.Dict = {
                # Environment configuration
                "environment": FlextConstants.Environment.ConfigEnvironment.DEVELOPMENT.value,
                "log_level": FlextConstants.Config.LogLevel.INFO,
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

            return FlextResult[FlextTypes.Core.Dict].ok(config)

        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Failed to get web configs system config: {e}",
            )

    # =============================================================================
    # SINGLETON SETTINGS METHODS
    # =============================================================================

    _web_settings_instance: ClassVar[FlextWebConfigs.WebConfig | None] = None

    @classmethod
    def get_web_settings(cls) -> FlextWebConfigs.WebConfig:
        """Get singleton web settings instance."""
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
    def create_web_system_configs(cls) -> FlextResult[FlextTypes.Core.Dict]:
        """Create complete web system configurations."""
        try:
            web_config_result = cls.get_web_settings()

            system_configs = {
                "web_config": web_config_result,
                "system_info": {
                    "version": web_config_result.version,
                    "environment": "development"
                    if web_config_result.debug
                    else "production",
                    "host": web_config_result.host,
                    "port": web_config_result.port,
                },
                "feature_flags": {
                    "enable_cors": web_config_result.enable_cors,
                    "debug_mode": web_config_result.debug,
                },
            }

            return FlextResult[FlextTypes.Core.Dict].ok(system_configs)

        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Failed to create web system configs: {e}",
            )

    @classmethod
    def merge_web_config(
        cls,
        base_config: FlextWebConfigs.WebConfig,
        overrides: FlextTypes.Core.Dict,
    ) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Merge web config with override data."""
        try:
            # Get current config as dict
            config_dict = base_config.model_dump()

            # Apply overrides
            config_dict.update(overrides)

            # Create new config with merged data
            merged_config = cls.WebConfig.model_validate(config_dict)

            return FlextResult[FlextWebConfigs.WebConfig].ok(merged_config)

        except Exception as e:
            return FlextResult[FlextWebConfigs.WebConfig].fail(
                f"Failed to merge web config: {e}",
            )


__all__ = [
    "FlextWebConfigs",
]
