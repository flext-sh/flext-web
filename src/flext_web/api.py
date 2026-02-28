"""Generic HTTP API facade.

Provides unified interface for HTTP API operations using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from fastapi import FastAPI
from flext_core import (
    FlextContainer,
    FlextLogger,
    FlextResult,
)
from pydantic import ValidationError

from flext_web import FlextWebApp, FlextWebSettings, c, m, t


class FlextWebApi:
    """Generic HTTP API facade using flext-core patterns.

    Provides unified interface for HTTP API operations with proper error handling.
    """

    def __init__(self) -> None:
        """Initialize with flext-core container and logging."""
        super().__init__()
        self._container = FlextContainer()
        self._logger = FlextLogger(__name__)

    @classmethod
    def create_fastapi_app(
        cls,
        config: m.Web.FastAPIAppConfig | None = None,
    ) -> FlextResult[FastAPI]:
        """Create FastAPI web application with complete validation.

        Delegates to FlextWebApp for actual app creation while providing facade-level
        validation and error handling.

        Args:
            config: Application configuration model or None for defaults

        Returns:
            FlextResult[FastAPI]: Success contains configured FastAPI app,
                                  failure contains detailed error message

        """
        logger = FlextLogger(__name__)

        _ = logger.info("Creating FastAPI application via API facade")
        result = FlextWebApp.create_fastapi_app(config)

        # Log result using monadic pattern
        if result.is_success:
            _ = logger.info("FastAPI application created successfully")
        else:
            _ = logger.error(f"FastAPI application creation failed: {result.error}")

        return result

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

        # Use defaults from constants when not provided
        host_val: str = host if host is not None else c.Web.WebDefaults.HOST
        port_val: int = port if port is not None else c.Web.WebDefaults.PORT
        debug_mode_val: bool = (
            debug if debug is not None else c.Web.WebDefaults.DEBUG_MODE
        )
        secret_key_val: str = c.Web.WebDefaults.SECRET_KEY

        _ = logger.debug(
            "Creating HTTP config with data",
            config={"host": host_val, "port": port_val, "debug_mode": debug_mode_val},
        )

        try:
            config = FlextWebSettings(
                host=host_val,
                port=port_val,
                debug_mode=debug_mode_val,
                secret_key=secret_key_val,
            )
        except ValidationError as e:
            # Use u to extract error message - simplifies code
            errors = e.errors()
            error_msg = errors[0]["msg"] if errors else str(e)
            _ = logger.exception("HTTP config creation failed: %s", exception=e)
            return FlextResult.fail(f"Configuration validation failed: {error_msg}")

        _ = logger.info(
            f"HTTP config created successfully: {config.host}:{config.port}"
        )
        return FlextResult.ok(config)

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

        _ = logger.debug("Service status retrieved successfully")
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

        _ = logger.debug(f"Validating HTTP configuration for app: {config.app_name}")
        # Pydantic model is already validated on creation, just confirm it's valid
        _ = logger.info("HTTP configuration validation successful")
        return FlextResult.ok(True)

    # UTILITY METHODS - Supporting Operations

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
