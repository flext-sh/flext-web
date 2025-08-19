"""FLEXT Web Configuration Settings - Enterprise configuration management.

This module implements configuration management for the FLEXT Web Interface using
Pydantic Settings with flext-core integration for comprehensive validation and
environment variable support following enterprise patterns.

The configuration follows Twelve-Factor App methodology with environment variables
taking precedence over defaults, comprehensive validation, and production safety checks.

Key Components:
    - FlextWebConfig: Main configuration class with validation and environment support

Integration:
    - Built on flext-core FlextConfig patterns
    - Uses Pydantic Settings for type safety and validation
    - Supports environment variables with FLEXT_WEB_ prefix
"""

from __future__ import annotations

import re

from flext_core import FlextBaseConfigModel, FlextResult, FlextValidators
from pydantic import Field, field_validator
from pydantic_settings import SettingsConfigDict


class FlextWebConfig(FlextBaseConfigModel):
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
      FLEXT_WEB_APP_NAME: Application display name
      FLEXT_WEB_VERSION: Application version string
      FLEXT_WEB_DEBUG: Debug mode (true/false)
      FLEXT_WEB_HOST: Server bind address
      FLEXT_WEB_PORT: Server listen port
      FLEXT_WEB_SECRET_KEY: Cryptographic secret key (required in production)

    Example:
      Environment-based configuration:

      >>> import os
      >>> os.environ["FLEXT_WEB_HOST"] = "0.0.0.0"
      >>> os.environ["FLEXT_WEB_PORT"] = "8080"
      >>> os.environ["FLEXT_WEB_DEBUG"] = "false"
      >>> config = FlextWebConfig()
      >>> print(f"Server: {config.get_server_url()}")
      >>> print(f"Production: {config.is_production()}")

    """

    model_config = SettingsConfigDict(
        frozen=True,  # Ensure immutability for configuration
        env_prefix="FLEXT_WEB_",
        case_sensitive=False,
        validate_assignment=True,
        extra="ignore",  # Ignore extra environment variables not defined as fields
        json_schema_extra={
            "description": "Web interface configuration",
            "examples": [{"app_name": "My Web App", "host": "localhost", "port": 8080}],
        },
    )

    app_name: str = Field(default="FLEXT Web", description="Application name")
    version: str = Field(default="0.9.0", description="Application version")
    debug: bool = Field(default=True, description="Debug mode")

    # Server settings
    host: str = Field(default="localhost", description="Server host")
    port: int = Field(default=8080, ge=1, le=65535, description="Server port")

    # Security settings
    secret_key: str = Field(
        default="change-in-production-" + "x" * 32,
        min_length=32,
        description="Secret key for cryptographic operations",
    )

    @field_validator("app_name")
    @classmethod
    def validate_app_name(cls, v: str) -> str:
        """Validate application name is non-empty and properly formatted."""
        if not FlextValidators.is_non_empty_string(v):
            msg = "App name is required"
            raise ValueError(msg)
        return v

    @field_validator("version")
    @classmethod
    def validate_version_format(cls, v: str) -> str:
        """Validate version follows semantic versioning pattern."""
        pattern = r"^\d+\.\d+\.\d+$"
        if not re.fullmatch(pattern, v):
            msg = "Invalid version format (use x.y.z)"
            raise ValueError(msg)
        return v

    @field_validator("host")
    @classmethod
    def validate_host(cls, v: str) -> str:
        """Validate host address is non-empty."""
        if not FlextValidators.is_non_empty_string(v):
            msg = "Host is required"
            raise ValueError(msg)
        return v

    @field_validator("port")
    @classmethod
    def validate_port_range(cls, v: int) -> int:
        """Validate port is within valid range."""
        max_port_number = 65535
        if not (1 <= v <= max_port_number):
            msg = "Port must be between 1 and 65535"
            raise ValueError(msg)
        return v

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Validate secret key meets security requirements."""
        min_key_length = 32
        if len(v) < min_key_length:
            msg = f"Secret key must be at least {min_key_length} characters"
            raise ValueError(msg)
        return v

    def _validate_security(self) -> str | None:
        """Additional business rule validation for production security."""
        if not self.debug and "change-in-production" in self.secret_key:
            return "Secret key must be changed in production"
        return None

    def validate_config(self) -> FlextResult[None]:
        """Validate configuration according to business rules and security requirements.

        Note: Basic field validations are now handled by @field_validator decorators.
        This method performs additional business rule validations.
        """
        # Additional business rule validation
        error = self._validate_security()
        if error:
            return FlextResult[None].fail(error)
        return FlextResult[None].ok(None)

    def is_production(self) -> bool:
        """Check if configuration is set for production environment.

        Determines if the current configuration represents a production
        deployment based on debug mode setting. Used for conditional
        behavior and validation rules.

        Returns:
            bool: True if debug mode is disabled (production), False if
            debug mode is enabled (development/testing).

        Note:
            Production mode enables:
            - Stricter security validations
            - Performance optimizations
            - Reduced logging verbosity
            - Enhanced error handling

        Example:
            >>> config = FlextWebConfig(debug=False)
            >>> if config.is_production():
            ...     print("Running in production mode")

        """
        return not self.debug

    def get_server_url(self) -> str:
        """Get complete server URL for the web interface.

        Constructs the full HTTP URL for accessing the web interface based on
        the configured host and port settings. Used for service registration,
        health checks, and client connection information.

        Returns:
            str: Complete HTTP URL in format "http://host:port"

        Note:
            This method always returns HTTP URLs. For production deployments
            with HTTPS termination, configure reverse proxy or load balancer
            to handle SSL/TLS termination.

        Example:
            >>> config = FlextWebConfig(host="0.0.0.0", port=8080)
            >>> url = config.get_server_url()
            >>> print(f"Web interface available at: {url}")

        """
        return f"http://{self.host}:{self.port}"
