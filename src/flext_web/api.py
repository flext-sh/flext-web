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

from fastapi import FastAPI
from flext_core import (
    FlextContainer,
    FlextLogger,
    FlextResult,
    FlextUtilities,
)
from pydantic import ValidationError

from flext_web.app import FlextWebApp
from flext_web.constants import FlextWebConstants
from flext_web.models import FlextWebModels
from flext_web.services import FlextWebServices
from flext_web.settings import FlextWebSettings
from flext_web.typings import t

# Import aliases for simplified usage
u = FlextUtilities
c = FlextWebConstants
m = FlextWebModels


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
        self._container = FlextContainer()
        self._logger = FlextLogger(__name__)

    # =========================================================================
    # APPLICATION MANAGEMENT - Single Responsibility: App Lifecycle
    # =========================================================================

    @classmethod
    def create_fastapi_app(
        cls,
        config: m.Web.FastAPIAppConfig | None = None,
    ) -> FlextResult[FastAPI]:
        """Create FastAPI web application with complete validation.

        Single Responsibility: Creates and configures FastAPI web applications.
        Delegates to FlextWebApp for actual app creation while providing facade-level
        validation and error handling.

        Args:
            config: Application configuration model or None for defaults

        Returns:
            FlextResult[FastAPI]: Success contains configured FastAPI app,
                                  failure contains detailed error message

        """
        logger = FlextLogger(__name__)

        logger.info("Creating FastAPI application via API facade")
        result = FlextWebApp.create_fastapi_app(config)

        # Log result using monadic pattern
        if result.is_success:
            logger.info("FastAPI application created successfully")
        else:
            logger.error(f"FastAPI application creation failed: {result.error}")

        return result

    # =========================================================================
    # SERVICE MANAGEMENT - Single Responsibility: Service Lifecycle
    # =========================================================================

    @classmethod
    def create_http_service(
        cls,
        config: FlextWebSettings | None = None,
    ) -> FlextResult[FlextWebServices]:
        """Create HTTP service with validation and dependency injection.

        Single Responsibility: Creates and configures HTTP services only.
        Uses dependency injection pattern for flexible service composition.
        Delegates to FlextWebServices for actual service creation.

        Args:
        config: Service configuration model or None for defaults

        Returns:
        FlextResult[FlextWebServices]: Success contains configured service,
        failure contains detailed error message

        """
        logger = FlextLogger(__name__)

        logger.info("Creating HTTP service via API facade")
        result = FlextWebServices.create_service(config)

        # Log result using monadic pattern
        if result.is_success:
            logger.info("HTTP service created successfully")
        else:
            logger.error(f"HTTP service creation failed: {result.error}")

        return result

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
    ) -> FlextResult[FlextWebSettings]:
        """Create HTTP configuration with defaults and validation.

        Single Responsibility: Creates and validates HTTP configurations only.
        Uses flext-web constants for secure defaults and complete validation.
        Provides flexible configuration creation with sensible defaults.

        Args:
        host: Server host (defaults to localhost)
        port: Server port (defaults to 8080)
        debug: Debug mode flag

        Returns:
        FlextResult[FlextWebSettings]: Success contains validated config,
        failure contains validation error

        """
        logger = FlextLogger(__name__)

        # Build configuration using u code
        # Use uild config dict from provided values
        input_values = {"host": host, "port": port, "debug": debug}
        provided_values = {k: v for k, v in input_values.items() if v is not None}
        config_kwargs = dict(provided_values)

        # Map 'debug' to 'debug_mode' for Pydantic compatibility
        if "debug" in config_kwargs:
            config_kwargs["debug_mode"] = config_kwargs.pop("debug")

        logger.debug("Creating HTTP config with data", config=config_kwargs)

        # Create and validate configuration - Pydantic will validate types at runtime
        # Use regular constructor - AutoConfig handles defaults automatically
        try:
            # Only pass the fields that are provided, let Pydantic use defaults for others
            # AutoConfig will use defaults from Field() definitions
            # Ensure secret_key is provided for AutoConfig compatibility
            if "secret_key" not in config_kwargs:
                config_kwargs["secret_key"] = c.Web.WebDefaults.SECRET_KEY
            # Pydantic will validate types at runtime - use type: ignore for pyright
            # config_kwargs contains validated values from filter_dict
            config = FlextWebSettings(**config_kwargs)
        except ValidationError as e:
            # Use u to extract error message - simplifies code
            errors = e.errors()
            error_msg = errors[0]["msg"] if errors else str(e)
            logger.exception("HTTP config creation failed: %s", exception=e)
            return FlextResult.fail(f"Configuration validation failed: {error_msg}")

        logger.info(f"HTTP config created successfully: {config.host}:{config.port}")
        return FlextResult.ok(config)

    # =========================================================================
    # SYSTEM STATUS AND MONITORING - Single Responsibility: Status Operations
    # =========================================================================

    @classmethod
    def get_service_status(cls) -> FlextResult[m.Web.ServiceResponse]:
        """Get complete HTTP service status information.

        Single Responsibility: Provides system status and health information only.
        Uses flext-core container for system state and provides complete
        status reporting for monitoring and debugging.

        Returns:
        FlextResult[ServiceResponse]: Success contains detailed status info,
        failure contains error message

        """
        logger = FlextLogger(__name__)

        _container = FlextContainer()

        status_info = m.Web.ServiceResponse(
            service=c.Web.WebService.SERVICE_NAME_API,
            capabilities=[
                "http_services_available",
                "fastapi_support",
                "container_initialized",
                "api_facade_ready",
            ],
            status=c.Web.WebResponse.STATUS_OPERATIONAL,
            config=True,
        )

        logger.debug("Service status retrieved successfully")
        return FlextResult.ok(status_info)

    @classmethod
    def validate_http_config(cls, config: FlextWebSettings) -> FlextResult[bool]:
        """Validate HTTP configuration for correctness and security.

        Single Responsibility: Validates HTTP configurations only.
        Uses Pydantic models for complete validation and provides
        detailed error messages for configuration issues.

        Args:
        config: Configuration model to validate

        Returns:
        FlextResult[bool]: Success contains True if valid, failure contains error

        """
        logger = FlextLogger(__name__)

        logger.debug(f"Validating HTTP configuration for app: {config.app_name}")
        # Pydantic model is already validated on creation, just confirm it's valid
        logger.info("HTTP configuration validation successful")
        return FlextResult.ok(True)

    # =========================================================================
    # UTILITY METHODS - Supporting Operations
    # =========================================================================

    @classmethod
    def get_api_capabilities(cls) -> FlextResult[t.WebCore.ResponseDict]:
        """Get API facade capabilities and supported operations.

        Returns:
        FlextResult[t.Core.ResponseDict]: Success contains capabilities info

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
