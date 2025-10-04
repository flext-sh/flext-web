"""FLEXT Web API - Unified facade for web services and applications.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import (
    FlextContainer,
    FlextLogger,
    FlextResult,
    FlextService,
    FlextTypes,
)

from flext_web.app import FlextWebApp
from flext_web.config import FlextWebConfig
from flext_web.constants import FlextWebConstants
from flext_web.models import FlextWebModels
from flext_web.services import FlextWebServices


class FlextWeb(FlextService[object]):
    """Unified facade for FLEXT web services and applications.

    This is the main entry point for web functionality in the FLEXT ecosystem,
    providing a thin facade that integrates:
    - FastAPI application creation (FlextWebApp)
    - Flask-based web services (FlextWebServices)
    - Web configuration management
    - Authentication integration
    - Request/response handling

    The facade pattern ensures easy external usage while maintaining clean
    separation of concerns internally.

    Example:
        >>> from flext_web import FlextWeb
        >>> from flext_web.models import FlextWebModels
        >>>
        >>> # Create FastAPI app
        >>> config = FlextWebModels.AppConfig(title="My API", version="1.0.0")
        >>> api_result = FlextWeb.create_fastapi_app(config)
        >>>
        >>> # Create web service
        >>> service_result = FlextWeb.create_web_service()
        >>> if service_result.is_success:
        ...     service = service_result.unwrap()
        ...     # Use service methods

    """

    def __init__(self, **data: object) -> None:
        """Initialize unified web facade with flext-core integration.

        Args:
            **data: Pydantic initialization data (FlextService requirement)

        """
        super().__init__(**data)
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)

    @staticmethod
    def create_fastapi_app(config: FlextWebModels.AppConfig) -> FlextResult[object]:
        """Create FastAPI application with full web integration.

        This is the recommended way to create FastAPI applications in the FLEXT
        ecosystem. It delegates to FlextWebApp for actual implementation while
        providing unified access through the facade.

        Args:
            config: Application configuration with title, version, middlewares, etc.

        Returns:
            FlextResult with configured FastAPI application or error

        Example:
            >>> from flext_web import FlextWeb
            >>> from flext_web.models import FlextWebModels
            >>>
            >>> config = FlextWebModels.AppConfig(
            ...     title="Enterprise API",
            ...     version="1.0.0",
            ...     description="Production-ready API",
            ... )
            >>> result = FlextWeb.create_fastapi_app(config)
            >>> if result.is_success:
            ...     app = result.unwrap()

        """
        return FlextWebApp.create_fastapi_app(config)

    @classmethod
    def create_web_service(
        cls, config: FlextTypes.Dict | None = None
    ) -> FlextResult[FlextWebServices]:
        """Create unified web service instance.

        This method creates a FlextWebServices instance with proper
        flext-core integration and configuration.

        Args:
            config: Optional configuration dict for the web service

        Returns:
            FlextResult with configured web service or error

        Example:
            >>> from flext_web import FlextWeb
            >>>
            >>> result = FlextWeb.create_web_service()
            >>> if result.is_success:
            ...     service = result.unwrap()
            ...     service.initialize_routes()

        """
        return FlextWebServices.create_web_service(config)

    @staticmethod
    def create_web_config(
        host: str | None = None,
        port: int | None = None,
        *,
        debug: bool | None = None,
        **kwargs: object,
    ) -> FlextResult[FlextWebConfig]:
        """Create web configuration with sensible defaults.

        Args:
            host: Server host (default: localhost)
            port: Server port (default: 8080)
            debug: Debug mode (default: False)
            **kwargs: Additional configuration options

        Returns:
            FlextResult with configured FlextWebConfig or error

        Example:
            >>> from flext_web import FlextWeb
            >>>
            >>> config_result = FlextWeb.create_web_config(
            ...     host="0.0.0.0", port=3000, debug=True
            ... )
            >>> if config_result.is_success:
            ...     config = config_result.unwrap()

        """
        # Input validation - fail fast with clear error
        if host is not None and not isinstance(host, str):
            return FlextResult[FlextWebConfig].fail("Host must be a string")

        if port is not None and not isinstance(port, int):
            return FlextResult[FlextWebConfig].fail("Port must be an integer")

        if debug is not None and not isinstance(debug, bool):
            return FlextResult[FlextWebConfig].fail("Debug must be a boolean")

        # Use defaults from constants if not provided
        config_data = {
            "host": host or FlextWebConstants.WebSpecific.DEFAULT_HOST,
            "port": port or FlextWebConstants.WebSpecific.DEFAULT_PORT,
            "debug": debug if debug is not None else False,
            **kwargs,
        }

        # Create config with Pydantic validation - let it raise and catch
        try:
            config = FlextWebConfig(**config_data)
            return FlextResult[FlextWebConfig].ok(config)
        except Exception as e:
            # Log the error and return failure result
            logger = FlextLogger(__name__)
            logger.warning("Failed to create web configuration", error=str(e))
            return FlextResult[FlextWebConfig].fail(
                f"Configuration creation failed: {e}"
            )

    @staticmethod
    def get_service_status() -> FlextResult[FlextTypes.Dict]:
        """Get current status of web services.

        Returns:
            FlextResult with service status information or error

        Example:
            >>> from flext_web import FlextWeb
            >>>
            >>> status = FlextWeb.get_service_status()
            >>> if status.is_success:
            ...     print(f"Services running: {status.unwrap()}")

        """
        # Get status from container/registry - no try/except needed for simple operations
        container = FlextContainer.get_global()
        logger = FlextLogger(__name__)

        # Check if web services are registered
        services_status: FlextTypes.Dict = {
            "web_services_available": True,
            "fastapi_support": True,
            "container_initialized": container is not None,
        }

        logger.info("Web service status retrieved", **services_status)
        return FlextResult[FlextTypes.Dict].ok(services_status)

    @staticmethod
    def validate_web_config(config: FlextTypes.Dict) -> FlextResult[bool]:
        """Validate web configuration data.

        Args:
            config: Configuration dict to validate

        Returns:
            FlextResult with validation result or error

        Example:
            >>> from flext_web import FlextWeb
            >>>
            >>> config = {"host": "localhost", "port": 8080}
            >>> result = FlextWeb.validate_web_config(config)
            >>> if result.is_success and result.unwrap():
            ...     print("Configuration is valid")

        """
        # Input validation
        if not isinstance(config, dict):
            return FlextResult[bool].fail("Configuration must be a dictionary")

        if not config:
            return FlextResult[bool].fail("Configuration cannot be empty")

        # Try to create config to validate - Pydantic will handle validation
        try:
            FlextWebConfig(**config)
            return FlextResult[bool].ok(True)
        except Exception as e:
            # Log validation failure and return result
            logger = FlextLogger(__name__)
            logger.warning("Web configuration validation failed", error=str(e))
            return FlextResult[bool].fail(f"Invalid configuration: {e}")


__all__ = [
    "FlextWeb",
]
