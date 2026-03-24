"""Generic HTTP App - FastAPI Application Factory with SOLID Principles.

Domain-agnostic FastAPI application factory using flext-core patterns and Pydantic models.
Follows SOLID principles with focused responsibilities and proper delegation.

Copyright (c) 2025 FLEXT Contributors. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable
from typing import override

import flask
from fastapi import FastAPI
from flext_core import FlextLogger, FlextService, r

from flext_web import FlextWebSettings, c, m, t, u


class FlextWebApp(FlextService[bool]):
    """Generic web application coordinator using flext-core patterns and SOLID principles.

    Single Responsibility: Coordinates web application creation and configuration.
    Delegates specific framework operations to specialized factory classes.
    Uses flext-web config models for type-safe configuration management.
    Delegates to flext-core for logging, container management, and error handling.
    """

    def __init__(self) -> None:
        """Initialize with flext-core container and logger."""
        super().__init__()

    @override
    def execute(self, **_kwargs: str | float | bool | None) -> r[bool]:
        """Execute the web application service.

        Main domain operation for the web application service.
        Creates and returns application metadata.

        Returns:
        r[bool]: Success contains True if app is ready,
        failure contains error message

        """
        self.logger.info("FlextWebApp service executed successfully")
        return r[bool].ok(value=True)

    class FastAPIFactory:
        """FastAPI application factory with flext-core integration.

        Single Responsibility: Creates FastAPI applications with proper configuration.
        Uses Pydantic models for validation and flext-core patterns for error handling.
        """

        @staticmethod
        def create_instance(
            config: m.Web.FastAPIAppConfig | None = None,
        ) -> r[FastAPI]:
            """Create FastAPI application instance with validated configuration.

            Args:
            config: FastAPI configuration dictionary or None for defaults

            Returns:
            r[FastAPI]: Success contains configured FastAPI app,
            failure contains detailed error message

            """
            logger = FlextLogger(__name__)
            default_config = m.Web.FastAPIAppConfig(
                title="FastAPI",
                version=c.Web.WebDefaults.VERSION_STRING,
                description="FlextWeb FastAPI Application",
                docs_url=c.Web.WebApi.DOCS_URL,
                redoc_url=c.Web.WebApi.REDOC_URL,
                openapi_url=c.Web.WebApi.OPENAPI_URL,
            )
            final_config = config if config is not None else default_config
            title: str = final_config.title or "FastAPI"
            version: str = final_config.version or c.Web.WebDefaults.VERSION_STRING
            description: str = (
                final_config.description or "FlextWeb FastAPI Application"
            )
            docs_url: str = final_config.docs_url or c.Web.WebApi.DOCS_URL
            redoc_url: str = final_config.redoc_url or c.Web.WebApi.REDOC_URL
            openapi_url: str = final_config.openapi_url or c.Web.WebApi.OPENAPI_URL
            try:
                app = FastAPI(
                    title=title,
                    version=version,
                    description=description,
                    docs_url=docs_url,
                    redoc_url=redoc_url,
                    openapi_url=openapi_url,
                )
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                RuntimeError,
                ImportError,
            ) as e:
                error_msg = f"Failed to create FastAPI application: {e}"
                logger.exception(error_msg)
                return r[FastAPI].fail(error_msg)
            logger.info("FastAPI application '%s' v%s created", title, version)
            return r[FastAPI].ok(app)

    @classmethod
    def _configure_fastapi_endpoints(
        cls,
        app: FastAPI,
        config: m.Web.FastAPIAppConfig,
    ) -> FastAPI:
        """Configure FastAPI endpoints."""

        def health_check() -> t.Web.ResponseDict:
            return cls.HealthHandler.create_handler()()

        def info_endpoint() -> t.Web.ResponseDict:
            return cls.InfoHandler.create_handler(config)()

        app.add_api_route("/health", health_check, methods=["GET"])
        app.add_api_route("/info", info_endpoint, methods=["GET"])

        logger = FlextLogger(__name__)
        logger.info(f"FastAPI application '{config.title}' v{config.version} created")
        return app

    @classmethod
    def create_fastapi_app(
        cls,
        config: m.Web.FastAPIAppConfig | None = None,
        factory_config: m.Web.FastAPIAppConfig | None = None,
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
            factory_config_new = m.Web.FastAPIAppConfig(
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
    def create_flask_app(cls, config: FlextWebSettings | None = None) -> r[flask.Flask]:
        """Create Flask app with flext-core integration and configuration.

        Single Responsibility: Creates and configures Flask application only.
        Uses Pydantic models for configuration validation and type safety.
        Delegates logging and error handling to flext-core patterns.

        Args:
        config: Flask configuration model or None for defaults

        Returns:
        r[flask.Flask]: Success contains configured Flask app,
        failure contains detailed error message

        """
        logger = FlextLogger(__name__)
        flask_config = config if config is not None else FlextWebSettings()
        app = flask.Flask(flask_config.app_name)
        app.config["SECRET_KEY"] = flask_config.secret_key
        app.config["DEBUG"] = flask_config.debug
        app.config["TESTING"] = flask_config.testing

        def health_check() -> flask.Response:
            import json as _json  # noqa: PLC0415

            body: str = _json.dumps({
                "status": c.Web.WebResponse.STATUS_HEALTHY,
                "service": c.Web.WebService.SERVICE_NAME_FLASK,
                "timestamp": u.generate_iso_timestamp(),
            })
            response = flask.make_response(body, 200)
            response.content_type = "application/json"
            return response

        app.add_url_rule("/health", "health_check", health_check)

        logger.info(f"Flask application '{flask_config.app_name}' created")
        return r[flask.Flask].ok(app)

    class HealthHandler:
        """Health check handler with single responsibility for system health monitoring."""

        @staticmethod
        def create_handler() -> Callable[[], t.Web.ResponseDict]:
            """Create FastAPI health check handler function."""

            def health_check() -> t.Web.ResponseDict:
                return {
                    "status": c.Web.WebResponse.STATUS_HEALTHY,
                    "service": c.Web.WebService.SERVICE_NAME,
                    "timestamp": u.generate_iso_timestamp(),
                }

            return health_check

    class InfoHandler:
        """Application info handler with single responsibility for metadata exposure."""

        @staticmethod
        def create_handler(
            config: m.Web.FastAPIAppConfig,
        ) -> Callable[[], t.Web.ResponseDict]:
            """Create FastAPI info handler function."""

            def info_handler() -> t.Web.ResponseDict:
                return {
                    "service": c.Web.WebService.SERVICE_NAME,
                    "title": config.title,
                    "version": config.version,
                    "description": config.description,
                    "debug": config.debug,
                    "timestamp": u.generate_iso_timestamp(),
                }

            return info_handler

    @classmethod
    def configure_error_handlers(cls, app: FastAPI) -> r[bool]:
        """Configure FastAPI error handlers (extensible for future needs).

        Args:
            app: FastAPI application instance

        Returns:
            r[bool]: Success contains True if error handlers configured,
                              failure contains error message

        """
        _ = app
        return r[bool].ok(value=True)

    @classmethod
    def configure_middleware(cls, app: FastAPI, config: FlextWebSettings) -> r[bool]:
        """Configure FastAPI middleware (extensible for future needs).

        Args:
            app: FastAPI application instance
            config: Web configuration model

        Returns:
            r[bool]: Success contains True if middleware configured,
                              failure contains error message

        """
        _ = (app, config)
        return r[bool].ok(value=True)

    @classmethod
    def configure_routes(cls, app: FastAPI, config: FlextWebSettings) -> r[bool]:
        """Configure FastAPI routes (extensible for future needs).

        Args:
            app: FastAPI application instance
            config: Web configuration model

        Returns:
            r[bool]: Success contains True if routes configured,
                              failure contains error message

        """
        _ = (app, config)
        return r[bool].ok(value=True)

    @override
    def validate_business_rules(self) -> r[bool]:
        """Validate business rules for web app service (FlextService requirement).

        Returns:
            r[bool]: Success contains True if valid, failure with error message

        """
        return r[bool].ok(value=True)


__all__ = ["FlextWebApp"]
