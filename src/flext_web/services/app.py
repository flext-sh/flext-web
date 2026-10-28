"""Application factories for flext-web.

Provides the framework-facing creation and configuration of the FastAPI app
without duplicating runtime/service orchestration concerns from the public API.

Copyright (c) 2025 FLEXT Contributors. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from typing import TYPE_CHECKING, override

from fastapi import FastAPI

from flext_web import c, m, p, r, s, t, u

if TYPE_CHECKING:
    from collections.abc import Callable


class FlextWebApp(s):
    """Generic web application coordinator using flext-core patterns.

    Follows SOLID principles.
    Single Responsibility: Coordinates web application creation and configuration.
    Delegates specific framework operations to specialized factory classes.
    Uses flext-web settings models for type-safe configuration management.
    Delegates to flext-core for logging, container management, and error handling.
    """

    @override
    def execute(self) -> p.Result[bool]:
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
            settings: m.Web.FastAPIAppConfig | None = None,
        ) -> p.Result[FastAPI]:
            """Create FastAPI application instance with validated configuration.

            Args:
            settings: FastAPI configuration dictionary or None for defaults

            Returns:
            r[FastAPI]: Success contains configured FastAPI app,
            failure contains detailed error message

            """
            default_config = m.Web.FastAPIAppConfig(
                title="FastAPI",
                description=c.Web.API_DEFAULT_DESCRIPTION,
                docs_url=c.Web.API_DOCS_URL,
                redoc_url=c.Web.API_REDOC_URL,
                openapi_url=c.Web.API_OPENAPI_URL,
            )
            final_config = settings if settings is not None else default_config
            title: str = final_config.title or "FastAPI"
            version: str = final_config.version
            description: str = (
                final_config.description or "FlextWeb FastAPI Application"
            )
            docs_url: str = final_config.docs_url or c.Web.API_DOCS_URL
            redoc_url: str = final_config.redoc_url or c.Web.API_REDOC_URL
            openapi_url: str = final_config.openapi_url or c.Web.API_OPENAPI_URL
            try:
                app = FastAPI(
                    title=title,
                    version=version,
                    description=description,
                    docs_url=docs_url,
                    redoc_url=redoc_url,
                    openapi_url=openapi_url,
                )
            except c.EXC_OS_RUNTIME_TYPE as exc:
                error_msg = f"Failed to create FastAPI application: {exc}"
                return r[FastAPI].fail(error_msg)
            return r[FastAPI].ok(app)

    @staticmethod
    def _configure_fastapi_endpoints(
        app: FastAPI,
        settings: m.Web.FastAPIAppConfig,
    ) -> FastAPI:
        """Configure FastAPI endpoints.

        Returns:
            The resulting ``FastAPI``.

        """

        def health_check() -> t.Web.FastApiEndpointPayload:
            """Serve the health endpoint payload.

            Returns:
                The health payload with status, service name, and timestamp.

            """
            return FlextWebApp.HealthHandler.create_handler()()

        def info_endpoint() -> t.Web.FastApiEndpointPayload:
            """Serve the info endpoint payload.

            Returns:
                The info payload with service metadata from the settings.

            """
            return FlextWebApp.InfoHandler.create_handler(settings)()

        app.add_api_route("/health", health_check, methods=["GET"])
        app.add_api_route("/info", info_endpoint, methods=["GET"])
        return app

    def create_fastapi_app(
        self,
        settings: m.Web.FastAPIAppConfig | None = None,
        factory_config: m.Web.FastAPIAppConfig | None = None,
    ) -> p.Result[FastAPI]:
        """Create FastAPI app with flext-core integration and Pydantic validation.

        Single Responsibility: Creates and configures FastAPI application only.
        Uses Pydantic models for configuration validation and type safety.
        Delegates logging and error handling to flext-core patterns.

        Args:
        settings: FastAPI configuration model or None for defaults
        factory_config: FastAPI factory configuration dictionary or None to use settings

        Returns:
        r[FastAPI]: Success contains configured FastAPI app,
        failure contains detailed error message

        """
        fastapi_config = settings or m.Web.FastAPIAppConfig(
            title=self.settings.Web.app_name,
            version=self.settings.Web.version,
            description=c.Web.API_DEFAULT_DESCRIPTION,
            docs_url=c.Web.API_DOCS_URL,
            redoc_url=c.Web.API_REDOC_URL,
            openapi_url=c.Web.API_OPENAPI_URL,
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

    class HealthHandler:
        """Health check handler with single responsibility.

        Monitors system health.
        """

        @staticmethod
        def create_handler() -> Callable[
            [],
            t.Web.FastApiEndpointPayload,
        ]:
            """Create FastAPI health check handler function.

            Returns:
                The resulting ``Callable[[], t.Web.FastApiEndpointPayload]``.

            """

            def health_check() -> t.Web.FastApiEndpointPayload:
                """Build the health endpoint payload.

                Returns:
                    The payload with healthy status, service name, and
                    timestamp.

                """
                return {
                    "status": c.Web.ResponseStatus.HEALTHY.value,
                    "service": c.Web.SERVICE_NAME,
                    "timestamp": u.generate_iso_timestamp(),
                }

            return health_check

    class InfoHandler:
        """Application info handler with single responsibility for metadata exposure."""

        @staticmethod
        def create_handler(
            settings: m.Web.FastAPIAppConfig,
        ) -> Callable[[], t.Web.FastApiEndpointPayload]:
            """Create FastAPI info handler function.

            Returns:
                The resulting ``Callable[[], t.Web.FastApiEndpointPayload]``.

            """

            def info_handler() -> t.Web.FastApiEndpointPayload:
                """Build the info endpoint payload.

                Returns:
                    The payload with service metadata from the settings.

                """
                return {
                    "service": c.Web.SERVICE_NAME,
                    "title": settings.title,
                    "version": settings.version,
                    "description": settings.description,
                    "debug": settings.debug,
                    "timestamp": u.generate_iso_timestamp(),
                }

            return info_handler


__all__: list[str] = ["FlextWebApp"]
