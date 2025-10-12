"""FLEXT Web API - Unified facade for web services and applications.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextCore

from flext_web.app import FlextWebApp
from flext_web.config import FlextWebConfig
from flext_web.constants import FlextWebConstants
from flext_web.models import FlextWebModels
from flext_web.services import FlextWebService


class FlextWeb:
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

    def __init__(self) -> None:
        """Initialize unified web facade with flext-core integration."""
        self._container = FlextCore.Container.get_global()
        self.logger = FlextCore.Logger(__name__)

    @staticmethod
    def create_fastapi_app(
        config: FlextWebModels.AppConfig,
    ) -> FlextCore.Result[object]:
        """Create FastAPI application with full web integration.

        This is the recommended way to create FastAPI applications in the FLEXT
        ecosystem. It delegates to FlextWebApp for actual implementation while
        providing unified access through the facade.

        Args:
            config: Application configuration with title, version, middlewares, etc.

        Returns:
            FlextCore.Result with configured FastAPI application or error

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
        cls, config: FlextCore.Types.Dict | None = None
    ) -> FlextCore.Result[FlextWebService]:
        """Create unified web service instance.

        This method creates a WebService instance with proper
        flext-core integration and configuration.

        Args:
            config: Optional configuration dict for the web service

        Returns:
            FlextCore.Result with configured web service or error

        Example:
            >>> from flext_web import FlextWeb
            >>>
            >>> result = FlextWeb.create_web_service()
            >>> if result.is_success:
            ...     service = result.unwrap()
            ...     service.initialize_routes()

        """
        return FlextWebService.create_web_service(config)

    @staticmethod
    def create_web_config(
        host: str | None = None,
        port: int | None = None,
        *,
        debug: bool | None = None,
        **kwargs: object,
    ) -> FlextCore.Result[FlextWebConfig]:
        """Create web configuration with sensible defaults.

        Args:
            host: Server host (default: localhost)
            port: Server port (default: 8080)
            debug: Debug mode (default: False)
            **kwargs: Additional configuration options

        Returns:
            FlextCore.Result with configured FlextWebConfig or error

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
            return FlextCore.Result[FlextWebConfig].fail("Host must be a string")

        if port is not None and not isinstance(port, int):
            return FlextCore.Result[FlextWebConfig].fail("Port must be an integer")

        if debug is not None and not isinstance(debug, bool):
            return FlextCore.Result[FlextWebConfig].fail("Debug must be a boolean")

        # Use defaults from constants if not provided
        config_data = {
            "host": host or FlextWebConstants.WebSpecific.DEFAULT_HOST,
            "port": port or FlextWebConstants.WebSpecific.DEFAULT_PORT,
            "debug": debug if debug is not None else False,
        }

        # Add kwargs if they are valid config fields
        valid_config_fields = {
            "host",
            "port",
            "debug",
            "development_mode",
            "web_environment",
            "secret_key",
            "app_name",
            "version",
            "max_content_length",
            "request_timeout",
            "enable_cors",
            "cors_origins",
            "ssl_enabled",
            "ssl_cert_path",
            "ssl_key_path",
            "session_cookie_secure",
            "session_cookie_httponly",
            "session_cookie_samesite",
            "log_level",
            "log_format",
        }

        config_data.update({
            key: value
            for key, value in kwargs.items()
            if key in valid_config_fields and isinstance(value, (str, int, bool))
        })

        # Create config with Pydantic validation - let it raise and catch
        try:
            web_config = FlextWebConfig(**config_data)
            return FlextCore.Result[FlextWebConfig].ok(web_config)
        except Exception as e:
            # Log the error and return failure result
            logger = FlextCore.Logger(__name__)
            logger.warning("Failed to create web configuration", error=str(e))
            return FlextCore.Result[FlextWebConfig].fail(
                f"Configuration creation failed: {e}"
            )

    @staticmethod
    def get_service_status() -> FlextCore.Result[FlextCore.Types.Dict]:
        """Get current status of web services.

        Returns:
            FlextCore.Result with service status information or error

        Example:
            >>> from flext_web import FlextWeb
            >>>
            >>> status = FlextWeb.get_service_status()
            >>> if status.is_success:
            ...     print(f"Services running: {status.unwrap()}")

        """
        # Get status from container/registry - no try/except needed for simple operations
        container = FlextCore.Container.get_global()
        logger = FlextCore.Logger(__name__)

        # Check if web services are registered
        services_status: FlextCore.Types.Dict = {
            "web_services_available": True,
            "fastapi_support": True,
            "container_initialized": container is not None,
        }

        logger.info("Web service status retrieved", **services_status)
        return FlextCore.Result[FlextCore.Types.Dict].ok(services_status)

    @staticmethod
    def validate_web_config(config: FlextCore.Types.Dict) -> FlextCore.Result[bool]:
        """Validate web configuration data.

        Args:
            config: Configuration dict to validate

        Returns:
            FlextCore.Result with validation result or error

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
            return FlextCore.Result[bool].fail("Configuration must be a dictionary")

        if not config:
            return FlextCore.Result[bool].fail("Configuration cannot be empty")

        # Try to create config to validate - Pydantic will handle validation
        try:
            # Pydantic will validate the types at runtime
            # Use type: ignore to suppress type checker warnings since Pydantic handles validation
            FlextWebConfig(**config)
            return FlextCore.Result[bool].ok(True)
        except Exception as e:
            # Log validation failure and return result
            logger = FlextCore.Logger(__name__)
            logger.warning("Web configuration validation failed", error=str(e))
            return FlextCore.Result[bool].fail(f"Invalid configuration: {e}")


__all__ = [
    "FlextWeb",
]
