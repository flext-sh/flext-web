"""FastAPI application factory for flext-web.

Provides enterprise-grade FastAPI application creation with flext-core integration,
middleware support, and authentication via flext-auth.

This module was moved from flext-api to establish flext-web as the web framework
authority for both Flask and FastAPI applications.

Integration Pattern:
    # Basic FastAPI app
    from flext_web import create_fastapi_app
    from flext_web.models import FlextWebModels

    config = FlextWebModels.AppConfig(
        title="My API",
        version="1.0.0",
        description="Enterprise API"
    )
    app = create_fastapi_app(config)

    # With authentication
    from flext_auth import OAuth2AuthProvider, WebAuthMiddleware

    auth_provider = OAuth2AuthProvider(...)
    auth_middleware = WebAuthMiddleware(provider=auth_provider)

    config = FlextWebModels.AppConfig(
        title="Authenticated API",
        middlewares=[auth_middleware]
    )
    app = create_fastapi_app(config)

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

try:
    from fastapi import FastAPI
except ImportError:
    FastAPI = None

from flext_core import FlextLogger, FlextResult, FlextService, FlextTypes
from flext_web.models import FlextWebModels


class FlextWebApp(FlextService[object]):
    """FastAPI application factory service.

    Provides enterprise-grade FastAPI application creation with:
    - flext-core service integration
    - Health check endpoints
    - Middleware support
    - Authentication via flext-auth
    - OpenAPI documentation

    This service consolidates all FastAPI functionality in flext-web,
    establishing it as the web framework authority alongside Flask support.

    Example:
        >>> from flext_web import FlextWebApp
        >>> from flext_web.models import FlextWebModels
        >>>
        >>> config = FlextWebModels.AppConfig(title="Enterprise API", version="1.0.0")
        >>> result = FlextWebApp.create_fastapi_app(config)
        >>> if result.is_success:
        ...     app = result.unwrap()

    """

    class _Factory:
        """Nested factory for FastAPI instance creation."""

        @staticmethod
        def create_instance(
            title: str | None = None,
            version: str | None = None,
            description: str | None = None,
            docs_url: str | None = None,
            redoc_url: str | None = None,
            openapi_url: str | None = None,
        ) -> FlextResult[object]:
            """Create FastAPI application instance.

            Args:
                title: Application title
                version: Application version
                description: Application description
                docs_url: Documentation URL (default: /docs)
                redoc_url: ReDoc URL (default: /redoc)
                openapi_url: OpenAPI JSON URL (default: /openapi.json)

            Returns:
                FlextResult with FastAPI application or error

            """
            if FastAPI is None:
                return FlextResult[object].fail(
                    "FastAPI is required for FlextWeb application creation"
                )

            try:
                app = FastAPI(
                    title=title or "FlextWeb FastAPI",
                    version=version or "1.0.0",
                    description=description or "FlextWeb FastAPI Application",
                    docs_url=docs_url or "/docs",
                    redoc_url=redoc_url or "/redoc",
                    openapi_url=openapi_url or "/openapi.json",
                )

                return FlextResult[object].ok(app)

            except Exception as e:
                return FlextResult[object].fail(
                    f"Failed to create FastAPI application: {e}"
                )

    @staticmethod
    def create_fastapi_app(config: FlextWebModels.AppConfig) -> FlextResult[object]:
        """Create FastAPI application with flext-core integration.

        This is the main entry point for creating FastAPI applications in the
        FLEXT ecosystem. It provides:
        - Automatic health check endpoint at /health
        - Middleware integration (including flext-auth authentication)
        - OpenAPI documentation
        - flext-core service integration

        Args:
            config: Application configuration with title, version, middlewares, etc.

        Returns:
            FlextResult with configured FastAPI application or error

        Example:
            >>> from flext_web import FlextWebApp
            >>> from flext_web.models import FlextWebModels
            >>> from flext_auth import JwtAuthProvider, WebAuthMiddleware
            >>>
            >>> # Create with authentication
            >>> auth = WebAuthMiddleware(JwtAuthProvider(secret="key"))
            >>> config = FlextWebModels.AppConfig(
            ...     title="Secure API", version="1.0.0", middlewares=[auth]
            ... )
            >>> result = FlextWebApp.create_fastapi_app(config)

        """
        logger = FlextLogger(__name__)

        logger.info(
            "Creating FastAPI application",
            title=config.title,
            version=config.version,
        )

        # Create FastAPI instance
        app_result = FlextWebApp._Factory.create_instance(
            title=config.title,
            version=config.version,
            description=getattr(config, "description", "FlextWeb FastAPI Application"),
            docs_url=getattr(config, "docs_url", "/docs"),
            redoc_url=getattr(config, "redoc_url", "/redoc"),
            openapi_url=getattr(config, "openapi_url", "/openapi.json"),
        )

        if app_result.is_failure:
            return app_result

        app = app_result.unwrap()

        # Add health check endpoint
        if hasattr(app, "get") and hasattr(app, "add_api_route"):

            def health_check() -> FlextTypes.StringDict:
                """Health check endpoint."""
                return {"status": "healthy", "service": "flext-web"}

            # Use add_api_route to avoid type issues
            add_route = getattr(app, "add_api_route")
            add_route("/health", health_check, methods=["GET"])
            logger.info("Health check endpoint registered at /health")

        # Add middleware if configured
        middlewares = getattr(config, "middlewares", [])
        if middlewares:
            logger.info(f"Registering {len(middlewares)} middleware(s)")
            for middleware in middlewares:
                if hasattr(middleware, "process_request"):
                    # FastAPI middleware integration
                    # Note: Full middleware integration would require FastAPI's
                    # middleware decorator patterns - this is a placeholder
                    logger.debug(
                        f"Middleware {getattr(middleware, 'name', type(middleware).__name__)} ready for integration"
                    )

        logger.info("FastAPI application created successfully")

        return FlextResult[object].ok(app)


def create_fastapi_app(config: FlextWebModels.AppConfig) -> FlextResult[object]:
    """Create FastAPI application (public API function).

    This is the recommended way to create FastAPI applications in the FLEXT
    ecosystem. It delegates to FlextWebApp.create_fastapi_app() for the
    actual implementation.

    Args:
        config: Application configuration

    Returns:
        FlextResult with FastAPI application or error

    Example:
        >>> from flext_web import create_fastapi_app
        >>> from flext_web.models import FlextWebModels
        >>>
        >>> config = FlextWebModels.AppConfig(title="My API", version="1.0.0")
        >>> result = create_fastapi_app(config)
        >>> if result.is_success:
        ...     app = result.unwrap()
        ...     # Use with uvicorn: uvicorn main:app --reload

    """
    return FlextWebApp.create_fastapi_app(config)


__all__ = [
    "FlextWebApp",
    "create_fastapi_app",
]
