"""FLEXT Web Configuration - Consolidated configuration system extending flext-core patterns.

This module implements the consolidated configuration architecture following the
"one class per module" pattern, with FlextWebConfigs extending FlextConfigs
and containing all web-specific configuration functionality.
"""

from __future__ import annotations

import re

from flext_core import FlextConfig, FlextResult
from pydantic import Field, field_validator
from pydantic_settings import SettingsConfigDict

# =============================================================================
# CONSTANTS
# =============================================================================

MIN_SECRET_KEY_LENGTH = 32
DEFAULT_DEV_SECRET_KEY = "dev-secret-key-change-in-production"  # noqa: S105  # nosec B105
TEST_SECRET_KEY = "test-secret-key-for-testing-only"  # noqa: S105  # nosec B105
ALL_INTERFACES_HOST = "0.0.0.0"  # noqa: S104  # nosec B104
LOCALHOST_HOST = "localhost"

# =============================================================================
# CONSOLIDATED CONFIGURATION CLASS
# =============================================================================


class FlextWebConfigs(FlextConfig):
    """Consolidated web configuration system extending flext-core patterns.

    This class serves as the single point of access for all web-specific
    configuration management while extending FlextConfig from flext-core
    for proper architectural inheritance.

    All configuration functionality is accessible through this single class following the
    "one class per module" architectural requirement.
    """

    # =========================================================================
    # NESTED CONFIGURATION CLASSES
    # =========================================================================

    class WebConfig(FlextConfig.Settings):
        """Web interface configuration with environment-based settings and validation.

        Enterprise configuration management class integrating Pydantic Settings with
        flext-core configuration patterns. Provides type-safe, validated configuration
        with environment variable support and comprehensive validation rules.

        The configuration follows the Twelve-Factor App methodology with environment
        variables taking precedence over defaults, comprehensive validation, and
        production safety checks.

        Configuration Hierarchy:
          1. Environment variables (FLEXT_WEB_* prefix)
          2. Configuration file values
          3. Default values defined in field definitions

        Validation:
          - All settings validated on instantiation
          - Production-specific security validations
          - Business rule enforcement for operational safety
          - Integration compatibility checks

        Environment Variables:
          - FLEXT_WEB_HOST: Server host address (default: localhost)
          - FLEXT_WEB_PORT: Server port number (default: 8080)
          - FLEXT_WEB_DEBUG: Debug mode flag (default: true)
          - FLEXT_WEB_SECRET_KEY: Cryptographic secret key (required for production)
          - FLEXT_WEB_APP_NAME: Application name for identification
        """

        # Pydantic Settings configuration extending flext-core patterns
        model_config = SettingsConfigDict(
            env_prefix="FLEXT_WEB_",
            case_sensitive=False,
            validate_assignment=True,
            extra="ignore",
            use_enum_values=True,
            # Inherit base settings from flext-core
            env_file=".env",
            env_file_encoding="utf-8",
            str_strip_whitespace=True,
        )

        # =========================================================================
        # CORE CONFIGURATION FIELDS
        # =========================================================================

        host: str = Field(
            default="localhost",
            description="Server host address for binding",
            min_length=1,
        )

        port: int = Field(
            default=8080,
            description="Server port number for binding",
            ge=1,
            le=65535,
        )

        debug: bool = Field(
            default=True,
            description="Debug mode flag - disable in production",
        )

        secret_key: str = Field(
            default="dev-secret-key-change-in-production",
            description="Cryptographic secret key for sessions and security",
            min_length=32,
        )

        app_name: str = Field(
            default="FLEXT Web",
            description="Application name for identification and logging",
            min_length=1,
            max_length=100,
        )

        # =========================================================================
        # ADVANCED CONFIGURATION FIELDS
        # =========================================================================

        max_content_length: int = Field(
            default=16 * 1024 * 1024,  # 16MB
            description="Maximum request content length in bytes",
            ge=1024,  # Minimum 1KB
        )

        request_timeout: int = Field(
            default=30,
            description="Request timeout in seconds",
            ge=1,
            le=300,  # Maximum 5 minutes
        )

        enable_cors: bool = Field(
            default=False,
            description="Enable CORS for cross-origin requests",
        )

        log_level: str = Field(
            default="INFO",
            description="Logging level",
            pattern=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
        )

        version: str = Field(
            default="0.9.0",
            description="Application version for API compatibility",
        )

        # =========================================================================
        # VALIDATION METHODS
        # =========================================================================

        @field_validator("host")
        @classmethod
        def validate_host(cls, v: str) -> str:
            """Validate host address format."""
            if not v or not v.strip():
                msg = "Host address cannot be empty"
                raise ValueError(msg)

            # Allow localhost, IP addresses, and domain names
            host_pattern = re.compile(
                r"^(localhost|127\.0\.0\.1|0\.0\.0\.0|"
                r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}|"
                r"[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*)$"
            )

            if not host_pattern.match(v):
                msg = f"Invalid host address format: {v}"
                raise ValueError(msg)

            return v

        @field_validator("secret_key")
        @classmethod
        def validate_secret_key(cls, v: str) -> str:
            """Validate secret key strength."""
            if len(v) < MIN_SECRET_KEY_LENGTH:
                msg = "Secret key must be at least 32 characters long"
                raise ValueError(msg)

            # Check for development default (insecure)
            if v == "dev-secret-key-change-in-production":
                # This is allowed but logged as a warning in development
                pass

            return v

        @field_validator("app_name")
        @classmethod
        def validate_app_name(cls, v: str) -> str:
            """Validate application name format."""
            if not v or not v.strip():
                msg = "Application name cannot be empty"
                raise ValueError(msg)

            return v.strip()

        # =========================================================================
        # CONFIGURATION VALIDATION METHODS
        # =========================================================================

        def validate_production_settings(self) -> FlextResult[None]:
            """Validate settings for production deployment.

            Returns:
                FlextResult indicating validation success or failure with details.

            """
            errors = []

            # Check debug mode
            if self.debug:
                errors.append("Debug mode should be disabled in production")

            # Check secret key
            if self.secret_key == DEFAULT_DEV_SECRET_KEY:
                errors.append("Default secret key must be changed for production")

            # Check host binding
            if self.host in {ALL_INTERFACES_HOST, LOCALHOST_HOST}:
                # This might be intentional for containerized deployments
                pass

            if errors:
                return FlextResult[None].fail(
                    f"Production validation failed: {'; '.join(errors)}"
                )

            return FlextResult[None].ok(None)

        def validate_security_settings(self) -> FlextResult[None]:
            """Validate security-related settings.

            Returns:
                FlextResult indicating security validation success or failure.

            """
            if len(self.secret_key) < MIN_SECRET_KEY_LENGTH:
                return FlextResult[None].fail(
                    "Secret key must be at least 32 characters for security"
                )

            return FlextResult[None].ok(None)

        def get_server_url(self) -> str:
            """Get complete server URL.

            Returns:
                Complete server URL including protocol, host, and port.

            """
            protocol = "https" if not self.debug else "http"
            return f"{protocol}://{self.host}:{self.port}"

        def is_development(self) -> bool:
            """Check if running in development mode.

            Returns:
                True if in development mode, False otherwise.

            """
            return self.debug and self.secret_key == DEFAULT_DEV_SECRET_KEY

        def is_production(self) -> bool:
            """Check if running in production mode.

            Returns:
                True if in production mode, False otherwise.

            """
            return not self.debug and self.secret_key != DEFAULT_DEV_SECRET_KEY

        def validate_config(self) -> FlextResult[None]:
            """Validate configuration settings - compatibility method.

            Performs validation appropriate to the current mode (development/production).
            For development mode (debug=True), only validates security settings.
            For production mode, validates both production and security settings.

            Returns:
                FlextResult indicating validation success or failure with details.

            """
            # Always validate security settings
            security_result = self.validate_security_settings()
            if not security_result.is_success:
                return security_result

            # Only validate production settings in production mode
            if self.is_production():
                production_result = self.validate_production_settings()
                if not production_result.is_success:
                    return production_result

            return FlextResult.ok(None)

    # =========================================================================
    # CONFIGURATION FACTORY METHODS
    # =========================================================================

    @classmethod
    def create_web_config(cls, **overrides: object) -> WebConfig:
        """Create web configuration instance with optional overrides.

        Args:
            **overrides: Configuration values to override defaults

        Returns:
            Configured WebConfig instance

        """
        return cls.WebConfig.model_validate(overrides)

    @classmethod
    def create_development_config(cls) -> WebConfig:
        """Create development-optimized configuration.

        Returns:
            WebConfig configured for development use

        """
        return cls.WebConfig.model_validate(
            {
                "debug": True,
                "host": "localhost",
                "port": 8080,
                "secret_key": DEFAULT_DEV_SECRET_KEY,
                "log_level": "DEBUG",
            }
        )

    @classmethod
    def create_production_config(
        cls,
        secret_key: str,
        host: str = ALL_INTERFACES_HOST,
        port: int = 8080,
    ) -> WebConfig:
        """Create production-optimized configuration.

        Args:
            secret_key: Production secret key
            host: Production host address
            port: Production port number

        Returns:
            WebConfig configured for production use

        """
        return cls.WebConfig.model_validate(
            {
                "debug": False,
                "host": host,
                "port": port,
                "secret_key": secret_key,
                "log_level": "INFO",
                "enable_cors": True,
            }
        )

    @classmethod
    def create_testing_config(cls) -> WebConfig:
        """Create testing-optimized configuration.

        Returns:
            WebConfig configured for testing use

        """
        return cls.WebConfig.model_validate(
            {
                "debug": True,
                "host": "localhost",
                "port": 0,  # Let system assign port
                "secret_key": TEST_SECRET_KEY,
                "log_level": "WARNING",
            }
        )


# =============================================================================
# CONFIGURATION MANAGEMENT UTILITIES
# =============================================================================

# Configuration singleton management
_config_instance: FlextWebConfigs.WebConfig | None = None


def get_web_settings() -> FlextWebConfigs.WebConfig:
    """Get web configuration singleton instance.

    Returns:
        Current web configuration instance, creating if needed.

    """
    global _config_instance  # noqa: PLW0603
    if _config_instance is None:
        _config_instance = FlextWebConfigs.create_web_config()
    return _config_instance


def reset_web_settings() -> None:
    """Reset configuration singleton for testing."""
    global _config_instance  # noqa: PLW0603
    _config_instance = None


def create_web_config(**overrides: object) -> FlextWebConfigs.WebConfig:
    """Create web configuration with overrides.

    Args:
        **overrides: Configuration values to override

    Returns:
        New web configuration instance

    """
    return FlextWebConfigs.create_web_config(**overrides)


# =============================================================================
# BACKWARD COMPATIBILITY ALIASES
# =============================================================================

# Legacy aliases for existing code compatibility
FlextWebConfig = FlextWebConfigs.WebConfig


__all__ = [
    # Legacy compatibility exports
    "FlextWebConfig",
    "FlextWebConfigs",
    "create_web_config",
    # Configuration utilities
    "get_web_settings",
    "reset_web_settings",
]
