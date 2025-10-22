"""Generic HTTP API - Unified Facade with SOLID Principles.

Domain-agnostic HTTP API facade using flext-core patterns and SOLID principles.
This class serves as the main entry point for all HTTP API operations, providing
a unified interface that delegates to specialized components following proper
separation of concerns.

SOLID Principles Applied:
- Single Responsibility: Each method handles one specific API concern
- Open/Closed: Extensible through inheritance but closed for modification
- Liskov Substitution: All methods can be substituted by implementations
- Interface Segregation: Methods provide focused interfaces
- Dependency Inversion: Depends on abstractions (services, apps, configs)

Copyright (c) 2025 FLEXT Contributors. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Any

from flext_core import FlextContainer, FlextLogger, FlextResult, FlextUtilities

from flext_web.app import FlextWebApp
from flext_web.config import FlextWebConfig
from flext_web.services import FlextWebServices


class FlextWebApi:
    """Generic HTTP API facade using flext-core patterns and SOLID principles.

    This class serves as the single entry point for all HTTP API operations,
    following the "one class per module" architectural requirement. It provides
    a unified facade that delegates to specialized components (apps, services,
    configs) while maintaining proper separation of concerns.

    Architecture:
    - Main facade class: FlextWebApi (coordinates all API operations)
    - Delegation pattern: Methods delegate to specialized components
    - SOLID principles: Each method has single responsibility
    - Error handling: Complete error handling with flext-core patterns
    """

    def __init__(self) -> None:
        """Initialize with flext-core container and logging."""
        super().__init__()
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)

    # =========================================================================
    # APPLICATION MANAGEMENT - Single Responsibility: App Lifecycle
    # =========================================================================

    @classmethod
    def create_fastapi_app(
        cls, config: FlextWebConfig | dict[str, Any] | None = None
    ) -> FlextResult[Any]:
        """Create FastAPI web application with complete validation.

        Single Responsibility: Creates and configures FastAPI web applications.
        Delegates to FlextWebApp for actual app creation while providing facade-level
        validation and error handling.

        Args:
            config: Application configuration (FlextWebConfig, dict, or None)

        Returns:
            FlextResult[Any]: Success contains configured Flask app,
                              failure contains detailed error message

        """
        logger = FlextLogger(__name__)

        try:
            logger.info("Creating FastAPI application via API facade")
            result = FlextWebApp.create_fastapi_app(config)

            if result.is_success:
                logger.info("FastAPI application created successfully")
            else:
                logger.error(f"FastAPI application creation failed: {result.error}")

            return result

        except Exception as e:
            logger.exception("Unexpected error in FastAPI app creation")
            return FlextResult.fail(f"Unexpected error: {e}")

    # =========================================================================
    # SERVICE MANAGEMENT - Single Responsibility: Service Lifecycle
    # =========================================================================

    @classmethod
    def create_http_service(
        cls,
        config: FlextWebConfig | dict[str, Any] | None = None,
        **service_overrides: object,
    ) -> FlextResult[FlextWebServices]:
        """Create HTTP service with validation and dependency injection.

        Single Responsibility: Creates and configures HTTP services only.
        Uses dependency injection pattern for flexible service composition.
        Delegates to FlextWebServices for actual service creation.

        Args:
        config: Service configuration
        **service_overrides: Override specific service implementations

        Returns:
        FlextResult[FlextWebServices]: Success contains configured service,
        failure contains detailed error message

        """
        logger = FlextLogger(__name__)

        try:
            logger.info("Creating HTTP service via API facade")

            # Convert config to dict if needed
            config_dict = None
            if isinstance(config, FlextWebConfig):
                config_dict = config.model_dump()
            elif isinstance(config, dict):
                config_dict = config

            result = FlextWebServices.create_service(config_dict, **service_overrides)

            if result.is_success:
                logger.info("HTTP service created successfully")
            else:
                logger.error(f"HTTP service creation failed: {result.error}")

            return result

        except Exception as e:
            logger.exception("Unexpected error in HTTP service creation")
            return FlextResult.fail(f"Unexpected error: {e}")

    # =========================================================================
    # CONFIGURATION MANAGEMENT - Single Responsibility: Config Operations
    # =========================================================================

    @classmethod
    def create_http_config(
        cls,
        host: str | None = None,
        port: int | None = None,
        *,
        debug: bool | None = None,
        **kwargs: object,
    ) -> FlextResult[FlextWebConfig]:
        """Create HTTP configuration with defaults and validation.

        Single Responsibility: Creates and validates HTTP configurations only.
        Uses flext-web constants for secure defaults and complete validation.
        Provides flexible configuration creation with sensible defaults.

        Args:
        host: Server host (defaults to localhost)
        port: Server port (defaults to 8080)
        debug: Debug mode flag
        **kwargs: Additional configuration parameters

        Returns:
        FlextResult[FlextWebConfig]: Success contains validated config,
        failure contains validation error

        """
        logger = FlextLogger(__name__)

        try:
            # Build configuration data with secure defaults
            config_data = {
                "host": host or "localhost",
                "port": port or 8080,
                "debug": debug or False,
                **{k: v for k, v in kwargs.items() if isinstance(v, (str, int, bool))},
            }

            logger.debug(f"Creating HTTP config with data: {config_data}")

            # Create and validate configuration
            config = FlextWebConfig(**config_data)

            logger.info(
                f"HTTP config created successfully: {config.host}:{config.port}"
            )
            return FlextResult.ok(config)

        except Exception as e:
            logger.exception("HTTP config creation failed")
            return FlextResult.fail(f"Config creation failed: {e}")

    # =========================================================================
    # SYSTEM STATUS AND MONITORING - Single Responsibility: Status Operations
    # =========================================================================

    @classmethod
    def get_service_status(cls) -> FlextResult[dict[str, Any]]:
        """Get complete HTTP service status information.

        Single Responsibility: Provides system status and health information only.
        Uses flext-core container for system state and provides complete
        status reporting for monitoring and debugging.

        Returns:
        FlextResult[dict[str, Any]]: Success contains detailed status info,
        failure contains error message

        """
        logger = FlextLogger(__name__)

        try:
            container = FlextContainer.get_global()

            status_info = {
                "http_services_available": True,
                "fastapi_support": True,
                "container_initialized": container is not None,
                "api_facade_ready": True,
                "service": "flext-web-api",
                "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
            }

            logger.debug("Service status retrieved successfully")
            return FlextResult.ok(status_info)

        except Exception as e:
            logger.exception("Service status check failed")
            return FlextResult.fail(f"Status check failed: {e}")

    @classmethod
    def validate_http_config(cls, config: dict[str, Any]) -> FlextResult[bool]:
        """Validate HTTP configuration for correctness and security.

        Single Responsibility: Validates HTTP configurations only.
        Uses Pydantic models for complete validation and provides
        detailed error messages for configuration issues.

        Args:
        config: Configuration dictionary to validate

        Returns:
        FlextResult[bool]: Success contains True if valid, failure contains error

        """
        logger = FlextLogger(__name__)

        try:
            if not isinstance(config, dict) or not config:
                return FlextResult.fail("Invalid config: must be non-empty dictionary")

            logger.debug("Validating HTTP configuration")

            # Use Pydantic model for validation
            FlextWebConfig(**config)

            logger.info("HTTP configuration validation successful")
            return FlextResult.ok(True)

        except Exception as e:
            logger.exception("HTTP configuration validation failed")
            return FlextResult.fail(f"Validation failed: {e}")

    # =========================================================================
    # UTILITY METHODS - Supporting Operations
    # =========================================================================

    @classmethod
    def get_api_capabilities(cls) -> FlextResult[dict[str, Any]]:
        """Get API facade capabilities and supported operations.

        Returns:
        FlextResult[dict[str, Any]]: Success contains capabilities info

        """
        return FlextResult.ok({
            "application_management": ["create_fastapi_app"],
            "service_management": ["create_http_service"],
            "configuration_management": [
                "create_http_config",
                "validate_http_config",
            ],
            "monitoring": ["get_service_status", "get_api_capabilities"],
            "supported_frameworks": ["fastapi"],
            "supported_patterns": ["solid", "facade", "dependency_injection"],
        })


__all__ = ["FlextWebApi"]
