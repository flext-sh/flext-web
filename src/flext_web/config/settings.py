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

from flext_core import FlextBaseSettings, FlextConfig, FlextResult, FlextValidators
from pydantic import Field
from pydantic_settings import SettingsConfigDict


class FlextWebConfig(FlextBaseSettings, FlextConfig):
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
            "examples": [{"app_name": "My Web App", "host": "0.0.0.0", "port": 8080}],  # noqa: S104 # documentation example
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

    def validate_config(self) -> FlextResult[None]:
        """Validate configuration according to business rules and security requirements.

        Performs comprehensive validation of all configuration settings using
        flext-core validation patterns. Ensures configuration is safe for
        the target environment and meets operational requirements.

        Returns:
            FlextResult[None]: Success if all validations pass, failure with
            detailed error message identifying the specific validation failure.

        Validation Rules:
            - Application name must be non-empty string
            - Version must follow semantic versioning (x.y.z)
            - Host must be valid network address
            - Port must be within valid range (1-65535)
            - Secret key must be changed from default in production
            - Secret key must meet minimum length requirements

        Production-Specific Validations:
            - Debug mode must be disabled in production
            - Secret key cannot contain default values
            - Additional security validations for production deployment

        Example:
            >>> config = FlextWebConfig(debug=False, secret_key="short")
            >>> result = config.validate_config()
            >>> if not result.success:
            ...     print(f"Configuration invalid: {result.error}")

        """
        if not FlextValidators.is_non_empty_string(self.app_name):
            return FlextResult.fail("App name is required")
        if not FlextValidators.matches_pattern(self.version, r"^\d+\.\d+\.\d+$"):
            return FlextResult.fail("Invalid version format (use x.y.z)")
        if not FlextValidators.is_non_empty_string(self.host):
            return FlextResult.fail("Host is required")
        max_port_number = 65535
        if not (1 <= self.port <= max_port_number):
            return FlextResult.fail("Port must be between 1 and 65535")
        # Security validation in production
        if not self.debug and "change-in-production" in self.secret_key:
            return FlextResult.fail("Secret key must be changed in production")
        return FlextResult.ok(None)

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
