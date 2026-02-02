"""Generic HTTP App - FastAPI Application Factory with SOLID Principles.

Domain-agnostic FastAPI application factory using flext-core patterns and Pydantic models.
Follows SOLID principles with focused responsibilities and proper delegation.

Copyright (c) 2025 FLEXT Contributors. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TypedDict, override

from fastapi import FastAPI
from flask import Flask
from flext_core import (
    FlextLogger,
    FlextService,
    r,
)

from flext_web.constants import c
from flext_web.models import m
from flext_web.settings import FlextWebSettings
from flext_web.typings import t
from flext_web.utilities import u


class FlextWebApp(FlextService[bool]):
    """Generic web application coordinator using flext-core patterns and SOLID principles.

    Single Responsibility: Coordinates web application creation and configuration.
    Delegates specific framework operations to specialized factory classes.
    Uses flext-web config models for type-safe configuration management.
    Delegates to flext-core for logging, container management, and error handling.
    """

    class _FastAPIConfig(TypedDict, total=False):
        """FastAPI configuration dictionary."""

        title: str
        version: str
        description: str
        docs_url: str
        redoc_url: str
        openapi_url: str

    def __init__(self) -> None:
        """Initialize with flext-core container and logger."""
        super().__init__()

    @override
    def execute(self, **_kwargs: t.Types.GeneralValueType) -> r[bool]:
        """Execute the web application service.

        Main domain operation for the web application service.
        Creates and returns application metadata.

        Returns:
        r[bool]: Success contains True if app is ready,
        failure contains error message

        """
        self.logger.info("FlextWebApp service executed successfully")
        # Return bool for FlextService compatibility
        return r[bool].ok(True)

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
            config: FlextWebApp._FastAPIConfig | None = None,
        ) -> r[FastAPI]:
            """Create FastAPI application instance with validated configuration.

            Args:
            config: FastAPI configuration dictionary or None for defaults

            Returns:
            r[FastAPI]: Success contains configured FastAPI app,
            failure contains detailed error message

            """
            logger = FlextLogger(__name__)

            default_config = FlextWebApp._FastAPIConfig(
                title="FastAPI",
                version=c.Web.WebDefaults.VERSION_STRING,
                description="FlextWeb FastAPI Application",
                docs_url=c.Web.WebApi.DOCS_URL,
                redoc_url=c.Web.WebApi.REDOC_URL,
                openapi_url=c.Web.WebApi.OPENAPI_URL,
            )
            # Extract configuration values with defaults
            final_config = config if config is not None else default_config
            title: str = final_config.get("title", "FastAPI")
            version: str = final_config.get(
                "version",
                c.Web.WebDefaults.VERSION_STRING,
            )
            description: str = final_config.get(
                "description",
                "FlextWeb FastAPI Application",
            )
            docs_url: str = final_config.get("docs_url", c.Web.WebApi.DOCS_URL)
            redoc_url: str = final_config.get("redoc_url", c.Web.WebApi.REDOC_URL)
            openapi_url: str = final_config.get(
                "openapi_url",
                c.Web.WebApi.OPENAPI_URL,
            )

            # Use try/except for error handling with exception message
            try:
                app = FastAPI(
                    title=title,
                    version=version,
                    description=description,
                    docs_url=docs_url,
                    redoc_url=redoc_url,
                    openapi_url=openapi_url,
                )
            except Exception as e:
                error_msg = f"Failed to create FastAPI application: {e}"
                logger.exception(error_msg)
                return r[FastAPI].fail(error_msg)

            logger.info("FastAPI application '%s' v%s created", title, version)
            return r.ok(app)

    @classmethod
    def create_fastapi_app(
        cls,
        config: m.Web.FastAPIAppConfig | None = None,
        factory_config: FlextWebApp._FastAPIConfig | None = None,
    ) -> r[FastAPI]:
        """Create FastAPI app with flext-core integration and Pydantic validation.

        Single Responsibility: Creates and configures FastAPI application only.
        Uses Pydantic models for configuration validation and type safety.
        Delegates logging and error handling to flext-core patterns.

        Args:
        config: FastAPI configuration model or None for defaults
        factory_config: FastAPI factory configuration dictionary or None to use config

        Returns:
        r[FastAPI]: Success contains configured FastAPI app,
        failure contains detailed error message

        """
        fastapi_config = config if config is not None else m.Web.FastAPIAppConfig()

        factory_config_final = factory_config if factory_config is not None else None
        if factory_config_final is None:
            factory_config_new = FlextWebApp._FastAPIConfig(
                title=fastapi_config.title,
                version=fastapi_config.version,
                description=fastapi_config.description,
                docs_url=fastapi_config.docs_url,
                redoc_url=fastapi_config.redoc_url,
                openapi_url=fastapi_config.openapi_url,
            )
            factory_config_final = factory_config_new

        return cls.FastAPIFactory.create_instance(factory_config_final).map(
            lambda app: cls._configure_fastapi_endpoints(app, fastapi_config),
        )

    @classmethod
    def _configure_fastapi_endpoints(
        cls,
        app: FastAPI,
        config: m.Web.FastAPIAppConfig,
    ) -> FastAPI:
        """Configure FastAPI endpoints."""

        # Add health endpoint using flext-core patterns
        @app.get("/health")
        def health_check() -> t.WebCore.ResponseDict:
            # Handler returns ResponseDict directly
            return cls.HealthHandler.create_handler()()

        # Add info endpoint for API metadata
        @app.get("/info")
        def info_endpoint() -> t.WebCore.ResponseDict:
            return cls.InfoHandler.create_handler(config)()

        logger = FlextLogger(__name__)
        logger.info(f"FastAPI application '{config.title}' v{config.version} created")
        return app

    @classmethod
    def create_flask_app(
        cls,
        config: FlextWebSettings | None = None,
    ) -> r[Flask]:
        """Create Flask app with flext-core integration and configuration.

        Single Responsibility: Creates and configures Flask application only.
        Uses Pydantic models for configuration validation and type safety.
        Delegates logging and error handling to flext-core patterns.

        Args:
        config: Flask configuration model or None for defaults

        Returns:
        r[Flask]: Success contains configured Flask app,
        failure contains detailed error message

        """
        logger = FlextLogger(__name__)

        flask_config = config if config is not None else FlextWebSettings()

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
                "status": c.Web.WebResponse.STATUS_HEALTHY,
                "service": c.Web.WebService.SERVICE_NAME_FLASK,
                "timestamp": u.Generators.generate_iso_timestamp(),
            }

        logger.info(f"Flask application '{flask_config.app_name}' created")
        return r.ok(app)

    # =========================================================================
    # HEALTH AND INFO HANDLERS - Single Responsibility Principle
    # =========================================================================

    class HealthHandler:
        """Health check handler with single responsibility for system health monitoring."""

        @staticmethod
        def create_handler() -> Callable[[], t.WebCore.ResponseDict]:
            """Create FastAPI health check handler function."""

            def health_check() -> t.WebCore.ResponseDict:
                return {
                    "status": c.Web.WebResponse.STATUS_HEALTHY,
                    "service": c.Web.WebService.SERVICE_NAME,
                    "timestamp": u.Generators.generate_iso_timestamp(),
                }

            return health_check

    class InfoHandler:
        """Application info handler with single responsibility for metadata exposure."""

        @staticmethod
        def create_handler(
            config: m.Web.FastAPIAppConfig,
        ) -> Callable[[], t.WebCore.ResponseDict]:
            """Create FastAPI info handler function."""

            def info_handler() -> t.WebCore.ResponseDict:
                return {
                    "service": c.Web.WebService.SERVICE_NAME,
                    "title": config.title,
                    "version": config.version,
                    "description": config.description,
                    "debug": config.debug,
                    "timestamp": u.Generators.generate_iso_timestamp(),
                }

            return info_handler

    # =========================================================================
    # APPLICATION MANAGEMENT - SOLID Extension Points
    # =========================================================================

    @classmethod
    def configure_middleware(
        cls,
        app: FastAPI,
        config: FlextWebSettings,
    ) -> r[bool]:
        """Configure FastAPI middleware (extensible for future needs).

        Args:
            app: FastAPI application instance
            config: Web configuration model

        Returns:
            r[bool]: Success contains True if middleware configured,
                              failure contains error message

        """
        # Placeholder for middleware configuration
        # Can be extended with CORS, authentication, rate limiting, etc.
        _ = app, config  # Parameters reserved for future implementation
        return r[bool].ok(True)

    @classmethod
    def configure_routes(
        cls,
        app: FastAPI,
        config: FlextWebSettings,
    ) -> r[bool]:
        """Configure FastAPI routes (extensible for future needs).

        Args:
            app: FastAPI application instance
            config: Web configuration model

        Returns:
            r[bool]: Success contains True if routes configured,
                              failure contains error message

        """
        # Placeholder for route configuration
        # Can be extended with API routes, WebSocket routes, etc.
        _ = app, config  # Parameters reserved for future implementation
        return r[bool].ok(True)

    @classmethod
    def configure_error_handlers(cls, app: FastAPI) -> r[bool]:
        """Configure FastAPI error handlers (extensible for future needs).

        Args:
            app: FastAPI application instance

        Returns:
            r[bool]: Success contains True if error handlers configured,
                              failure contains error message

        """
        # Placeholder for error handler configuration
        # Can be extended with custom exception handlers
        _ = app  # Parameter reserved for future implementation
        return r[bool].ok(True)

    def validate_business_rules(self) -> r[bool]:
        """Validate business rules for web app service (FlextService requirement).

        Returns:
            r[bool]: Success contains True if valid, failure with error message

        """
        return r[bool].ok(True)


__all__ = [
    "FlextWebApp",
]
