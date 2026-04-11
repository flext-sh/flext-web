"""Application factories for flext-web.

Provides the framework-facing creation and configuration of FastAPI/Flask apps
without duplicating runtime/service orchestration concerns from the public API.

Copyright (c) 2025 FLEXT Contributors. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json as _json
from collections.abc import Callable
from typing import override

import flask
from fastapi import FastAPI

from flext_core import r
from flext_web import FlextWebServiceBase, FlextWebSettings, c, m, t, u


class FlextWebApp(FlextWebServiceBase[bool]):
    """Generic web application coordinator using flext-core patterns and SOLID principles.

    Single Responsibility: Coordinates web application creation and configuration.
    Delegates specific framework operations to specialized factory classes.
    Uses flext-web config models for type-safe configuration management.
    Delegates to flext-core for logging, container management, and error handling.
    """

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
            default_config = m.Web.FastAPIAppConfig(
                title="FastAPI",
                version=c.Web.WebDefaults.VERSION_STRING,
                description=c.Web.WebApi.DEFAULT_DESCRIPTION,
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
            except (RuntimeError, OSError, TypeError, ValueError) as exc:
                error_msg = f"Failed to create FastAPI application: {exc}"
                return r[FastAPI].fail(error_msg)
            return r[FastAPI].ok(app)

    @staticmethod
    def _configure_fastapi_endpoints(
        app: FastAPI,
        config: m.Web.FastAPIAppConfig,
    ) -> FastAPI:
        """Configure FastAPI endpoints."""

        def health_check() -> t.Web.ResponseDict:
            return FlextWebApp.HealthHandler.create_handler()()

        def info_endpoint() -> t.Web.ResponseDict:
            return FlextWebApp.InfoHandler.create_handler(config)()

        app.add_api_route("/health", health_check, methods=["GET"])
        app.add_api_route("/info", info_endpoint, methods=["GET"])
        return app

    def create_fastapi_app(
        self,
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
        fastapi_config = (
            config
            if config is not None
            else m.Web.FastAPIAppConfig(
                title=self.settings.app_name,
                version=self.settings.version,
                description=c.Web.WebApi.DEFAULT_DESCRIPTION,
                docs_url=c.Web.WebApi.DOCS_URL,
                redoc_url=c.Web.WebApi.REDOC_URL,
                openapi_url=c.Web.WebApi.OPENAPI_URL,
            )
        )
        factory_payload = (
            factory_config
            if factory_config is not None
            else m.Web.FastAPIAppConfig(
                title=fastapi_config.title,
                version=fastapi_config.version,
                description=fastapi_config.description,
                docs_url=fastapi_config.docs_url,
                redoc_url=fastapi_config.redoc_url,
                openapi_url=fastapi_config.openapi_url,
            )
        )
        result = self.FastAPIFactory.create_instance(factory_payload).map(
            lambda app: self._configure_fastapi_endpoints(app, fastapi_config),
        )
        if result.success:
            self.logger.info(
                "FastAPI application created",
                title=fastapi_config.title,
                version=fastapi_config.version,
            )
        return result

    def create_flask_app(
        self, config: FlextWebSettings | None = None
    ) -> r[flask.Flask]:
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
        flask_config = config if config is not None else self.settings
        app = flask.Flask(flask_config.app_name)
        app.config["SECRET_KEY"] = flask_config.secret_key
        app.config["DEBUG"] = flask_config.debug
        app.config["TESTING"] = flask_config.testing

        def health_check() -> flask.Response:
            body: str = _json.dumps({
                "status": c.Web.WebResponse.STATUS_HEALTHY,
                "service": c.Web.WebService.SERVICE_NAME_FLASK,
                "timestamp": u.generate_iso_timestamp(),
            })
            response = flask.make_response(body, 200)
            response.content_type = "application/json"
            return response

        app.add_url_rule("/health", "health_check", health_check)

        self.logger.info("Flask application created", app_name=flask_config.app_name)
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

    def configure_fastapi_error_handlers(self, app: FastAPI) -> r[bool]:
        """Configure FastAPI error handlers (extensible for future needs).

        Args:
            app: FastAPI application instance

        Returns:
            r[bool]: Success contains True if error handlers configured,
                              failure contains error message

        """
        _ = app
        return r[bool].ok(value=True)

    def configure_fastapi_middleware(
        self,
        app: FastAPI,
        config: FlextWebSettings | None = None,
    ) -> r[bool]:
        """Configure FastAPI middleware (extensible for future needs).

        Args:
            app: FastAPI application instance
            config: Web configuration model

        Returns:
            r[bool]: Success contains True if middleware configured,
                              failure contains error message

        """
        _ = (app, config if config is not None else self.settings)
        return r[bool].ok(value=True)

    def configure_fastapi_routes(
        self,
        app: FastAPI,
        config: FlextWebSettings | None = None,
    ) -> r[bool]:
        """Configure FastAPI routes (extensible for future needs).

        Args:
            app: FastAPI application instance
            config: Web configuration model

        Returns:
            r[bool]: Success contains True if routes configured,
                              failure contains error message

        """
        _ = (app, config if config is not None else self.settings)
        return r[bool].ok(value=True)

    @override
    def validate_business_rules(self) -> r[bool]:
        """Validate business rules for web app service (s requirement).

        Returns:
            r[bool]: Success contains True if valid, failure with error message

        """
        return r[bool].ok(value=True)


__all__ = ["FlextWebApp"]
