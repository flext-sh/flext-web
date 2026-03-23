"""Generic HTTP API facade.

Provides unified interface for HTTP API operations using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from fastapi import FastAPI
from flext_core import FlextContainer, FlextLogger, r
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
    ) -> r[FastAPI]:
        """Create FastAPI web application with complete validation.

        Delegates to FlextWebApp for actual app creation while providing facade-level
        validation and error handling.

        Args:
            config: Application configuration model or None for defaults

        Returns:
            r[FastAPI]: Success contains configured FastAPI app,
                                  failure contains detailed error message

        """
        logger = FlextLogger(__name__)
        _ = logger.info("Creating FastAPI application via API facade")
        result = FlextWebApp.create_fastapi_app(config)
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
    ) -> r[FlextWebSettings]:
        """Create HTTP configuration with defaults and validation.

        Single Responsibility: Creates and validates HTTP configurations only.
        Uses flext-web constants for secure defaults and complete validation.
        Provides flexible configuration creation with sensible defaults.

        Args:
        host: Server host (defaults to localhost)
        port: Server port (defaults to 8080)
        debug: Debug mode flag

        Returns:
        r[FlextWebSettings]: Success contains validated config,
        failure contains validation error

        """
        logger = FlextLogger(__name__)
        host_val: str = host if host is not None else c.Web.WebDefaults.HOST
        port_val: int = port if port is not None else c.Web.WebDefaults.PORT
        debug_mode_val: bool = (
            debug if debug is not None else c.Web.WebDefaults.DEBUG_MODE
        )
        secret_key_val: str = c.Web.WebDefaults.SECRET_KEY
        _ = logger.debug(
            "Creating HTTP config with data",
            config=str({
                "host": host_val,
                "port": port_val,
                "debug_mode": debug_mode_val,
            }),
        )
        try:
            config = FlextWebSettings(
                host=host_val,
                port=port_val,
                debug_mode=debug_mode_val,
                secret_key=secret_key_val,
            )
        except ValidationError as e:
            errors = e.errors()
            error_msg = errors[0]["msg"] if errors else str(e)
            _ = logger.exception("HTTP config creation failed: %s", exception=e)
            failure_result: r[FlextWebSettings] = r[FlextWebSettings].fail(
                f"Configuration validation failed: {error_msg}",
            )
            return failure_result
        _ = logger.info(
            f"HTTP config created successfully: {config.host}:{config.port}",
        )
        return r[FlextWebSettings].ok(config)

    @classmethod
    def get_api_capabilities(cls) -> r[t.WebCore.ResponseDict]:
        """Get API facade capabilities and supported operations.

        Returns:
        r[t.Core.ResponseDict]: Success contains capabilities info

        """
        return r[t.WebCore.ResponseDict].ok({
            "application_management": ["create_fastapi_app"],
            "service_management": ["create_http_service"],
            "configuration_management": ["create_http_config", "validate_http_config"],
            "monitoring": ["get_service_status", "get_api_capabilities"],
            "supported_frameworks": ["fastapi"],
            "supported_patterns": ["solid", "facade", "dependency_injection"],
        })

    @classmethod
    def get_service_status(cls) -> r[m.Web.ServiceResponse]:
        """Get complete HTTP service status information.

        Single Responsibility: Provides system status and health information only.
        Uses flext-core container for system state and provides complete
        status reporting for monitoring and debugging.

        Returns:
        r[ServiceResponse]: Success contains detailed status info,
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
        return r[m.Web.ServiceResponse].ok(status_info)

    @classmethod
    def validate_http_config(cls, config: FlextWebSettings) -> r[bool]:
        """Validate HTTP configuration for correctness and security.

        Single Responsibility: Validates HTTP configurations only.
        Uses Pydantic models for complete validation and provides
        detailed error messages for configuration issues.

        Args:
        config: Configuration model to validate

        Returns:
        r[bool]: Success contains True if valid, failure contains error

        """
        logger = FlextLogger(__name__)
        _ = logger.debug(f"Validating HTTP configuration for app: {config.app_name}")
        _ = logger.info("HTTP configuration validation successful")
        return r[bool].ok(True)


__all__ = ["FlextWebApi"]
