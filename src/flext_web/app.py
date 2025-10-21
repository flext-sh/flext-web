"""Generic HTTP App - FastAPI Application Factory with SOLID Principles.

Domain-agnostic FastAPI application factory using flext-core patterns and Pydantic models.
Follows SOLID principles with focused responsibilities and proper delegation.

Copyright (c) 2025 FLEXT Contributors. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from fastapi import FastAPI
from flask import Flask
from flext_core import (
    FlextContainer,
    FlextLogger,
    FlextResult,
    FlextService,
    FlextUtilities,
)

from flext_web.config import FlextWebConfig
from flext_web.models import FlextWebModels


class FlextWebApp(FlextService[dict[str, object]]):
    """Generic web application coordinator using flext-core patterns and SOLID principles.

    Single Responsibility: Coordinates web application creation and configuration.
    Delegates specific framework operations to specialized factory classes.
    Uses flext-web config models for type-safe configuration management.
    Delegates to flext-core for logging, container management, and error handling.
    """

    def __init__(self) -> None:
        """Initialize with flext-core container and logger."""
        super().__init__()
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)

    def execute(self) -> FlextResult[dict[str, object]]:
        """Execute the web application service.

        Main domain operation for the web application service.
        Creates and returns application metadata.

        Returns:
        FlextResult[dict[str, object]]: Success contains app metadata,
        failure contains error message

        """
        try:
            app_info: dict[str, object] = {
                "service": "flext-web-app",
                "type": "fastapi_application_factory",
                "capabilities": [
                    "configure_middleware",
                    "configure_routes",
                    "create_fastapi_app",
                ],
                "status": "initialized",
                "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
            }

            self._logger.info("FlextWebApp service executed successfully")
            return FlextResult.ok(app_info)

        except Exception as e:
            self._logger.exception("FlextWebApp service execution failed")
            return FlextResult.fail(f"Service execution failed: {e}")

    # =========================================================================
    # FASTAPI APPLICATION FACTORY - Single Responsibility
    # =========================================================================

    class FastAPIFactory:
        """FastAPI application factory with flext-core integration.

        Single Responsibility: Creates FastAPI applications with proper configuration.
        Uses Pydantic models for validation and flext-core patterns for error handling.
        """

        @staticmethod
        def create_instance(
            title: str = "FastAPI",
            version: str = "1.0.0",
            description: str = "FlextWeb FastAPI Application",
            docs_url: str | None = "/docs",
            redoc_url: str | None = "/redoc",
            openapi_url: str | None = "/openapi.json",
        ) -> FlextResult[FastAPI]:
            """Create FastAPI application instance with validated configuration.

            Args:
            title: Application title
            version: Application version
            description: Application description
            docs_url: Swagger UI docs URL
            redoc_url: ReDoc URL
            openapi_url: OpenAPI schema URL

            Returns:
            FlextResult[FastAPI]: Success contains configured FastAPI app,
            failure contains detailed error message

            """
            logger = FlextLogger(__name__)

            try:
                # Validate FastAPI is available
                if FastAPI is None:
                    return FlextResult.fail("FastAPI is required but not available")

                # Create FastAPI application
                app = FastAPI(
                    title=title,
                    version=version,
                    description=description,
                    docs_url=docs_url,
                    redoc_url=redoc_url,
                    openapi_url=openapi_url,
                )

                logger.info(f"FastAPI application '{title}' v{version} created")
                return FlextResult.ok(app)

            except Exception as e:
                logger.exception("FastAPI creation failed")
                return FlextResult.fail(f"Failed to create FastAPI application: {e}")

    @classmethod
    def create_fastapi_app(
        cls,
        config: FlextWebModels.FastAPI.FastAPIAppConfig
        | FlextWebConfig
        | dict[str, Any]
        | None = None,
        title: str | None = None,
        docs_url: str | None = None,
        redoc_url: str | None = None,
        openapi_url: str | None = None,
    ) -> FlextResult[FastAPI]:
        """Create FastAPI app with flext-core integration and Pydantic validation.

        Single Responsibility: Creates and configures FastAPI application only.
        Uses Pydantic models for configuration validation and type safety.
        Delegates logging and error handling to flext-core patterns.

        Args:
        config: FastAPI configuration object, dict, or None for defaults
        title: Application title (overrides config.title)
        docs_url: Swagger UI docs URL
        redoc_url: ReDoc URL
        openapi_url: OpenAPI schema URL

        Returns:
        FlextResult[FastAPI]: Success contains configured FastAPI app,
        failure contains detailed error message

        """
        logger = FlextLogger(__name__)

        try:
            # Convert config to Pydantic model for validation
            if config is None:
                fastapi_config = FlextWebModels.FastAPI.FastAPIAppConfig()
            elif isinstance(config, FlextWebModels.FastAPI.FastAPIAppConfig):
                fastapi_config = config
            elif isinstance(config, FlextWebConfig):
                # Convert FlextWebConfig to FastAPIAppConfig
                fastapi_config = FlextWebModels.FastAPI.FastAPIAppConfig(
                    title=config.app_name,
                    version=config.version,
                    description=f"Web service for {config.app_name}",
                    debug=config.debug_mode,
                    testing=config.testing,
                    docs_url="/docs" if config.debug_mode else None,
                    redoc_url="/redoc" if config.debug_mode else None,
                    openapi_url="/openapi.json" if config.debug_mode else None,
                )
            else:
                try:
                    fastapi_config = (
                        FlextWebModels.FastAPI.FastAPIAppConfig.model_validate(config)
                    )
                except Exception as validation_error:
                    return FlextResult.fail(
                        f"FastAPI configuration validation failed: {validation_error}"
                    )

            # Use factory to create FastAPI application with custom parameters
            factory_result = cls.FastAPIFactory.create_instance(
                title=title or fastapi_config.title,
                version=fastapi_config.version,
                description=fastapi_config.description,
                docs_url=docs_url or fastapi_config.docs_url,
                redoc_url=redoc_url or fastapi_config.redoc_url,
                openapi_url=openapi_url or fastapi_config.openapi_url,
            )

            if factory_result.is_failure:
                return factory_result

            app = factory_result.value

            # Add health endpoint using flext-core patterns
            @app.get("/health")
            def health_check() -> dict[str, str]:
                return cls.HealthHandler.create_handler()()

            # Add info endpoint for API metadata
            @app.get("/info")
            def info_endpoint() -> dict[str, str]:
                return cls.InfoHandler.create_handler(fastapi_config)()

            logger.info(
                f"FastAPI application '{fastapi_config.title}' v{fastapi_config.version} created"
            )
            return FlextResult.ok(app)

        except Exception as e:
            logger.exception("FastAPI creation failed")
            return FlextResult.fail(f"FastAPI creation failed: {e}")

    @classmethod
    def create_flask_app(
        cls,
        config: FlextWebConfig | dict[str, Any] | None = None,
    ) -> FlextResult[Flask]:
        """Create Flask app with flext-core integration and configuration.

        Single Responsibility: Creates and configures Flask application only.
        Uses Pydantic models for configuration validation and type safety.
        Delegates logging and error handling to flext-core patterns.

        Args:
        config: Flask configuration object or dict

        Returns:
        FlextResult[Flask]: Success contains configured Flask app,
        failure contains detailed error message


        """
        logger = FlextLogger(__name__)

        try:
            # Handle configuration - support both Pydantic model and dict
            if isinstance(config, dict):
                flask_config = FlextWebConfig.model_validate(config)
            elif isinstance(config, FlextWebConfig):
                flask_config = config
            else:
                # Use default configuration
                flask_config = FlextWebConfig()

            # Create Flask application
            app = Flask(flask_config.app_name)

            # Configure Flask app
            app.config["SECRET_KEY"] = flask_config.secret_key
            app.config["DEBUG"] = flask_config.debug
            app.config["TESTING"] = flask_config.testing

            # Add basic health route
            @app.route("/health")
            def health_check() -> dict[str, str]:
                return {
                    "status": "healthy",
                    "service": "flext-web-flask",
                    "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
                }

            logger.info(f"Flask application '{flask_config.app_name}' created")
            return FlextResult.ok(app)

        except Exception as e:
            logger.exception("Flask creation failed")
            return FlextResult.fail(f"Flask creation failed: {e}")

    # =========================================================================
    # HEALTH AND INFO HANDLERS - Single Responsibility Principle
    # =========================================================================

    class HealthHandler:
        """Health check handler with single responsibility for system health monitoring."""

        @staticmethod
        def create_handler() -> Callable[[], dict[str, str]]:
            """Create FastAPI health check handler function."""

            def health_check() -> dict[str, str]:
                return {
                    "status": "healthy",
                    "service": "flext-web",
                    "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
                }

            return health_check

    class InfoHandler:
        """Application info handler with single responsibility for metadata exposure."""

        @staticmethod
        def create_handler(
            config: FlextWebModels.FastAPI.FastAPIAppConfig,
        ) -> Callable[[], dict[str, Any]]:
            """Create FastAPI info handler function."""

            def info_handler() -> dict[str, Any]:
                return {
                    "service": "flext-web",
                    "title": config.title,
                    "version": config.version,
                    "description": config.description,
                    "debug": config.debug,
                    "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
                }

            return info_handler

    # =========================================================================
    # APPLICATION MANAGEMENT - SOLID Extension Points
    # =========================================================================

    @classmethod
    def configure_middleware(cls, app: FastAPI, config: FlextWebConfig) -> None:
        """Configure FastAPI middleware (extensible for future needs)."""
        # Placeholder for middleware configuration
        # Can be extended with CORS, authentication, rate limiting, etc.

    @classmethod
    def configure_routes(cls, app: FastAPI, config: FlextWebConfig) -> None:
        """Configure FastAPI routes (extensible for future needs)."""
        # Placeholder for route configuration
        # Can be extended with API routes, WebSocket routes, etc.

    @classmethod
    def configure_error_handlers(cls, app: FastAPI) -> None:
        """Configure FastAPI error handlers (extensible for future needs)."""
        # Placeholder for error handler configuration
        # Can be extended with custom exception handlers


__all__ = ["FlextWebApp"]
