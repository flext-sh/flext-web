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
from flext_core import FlextContainer, FlextLogger, FlextResult, FlextUtilities
from pydantic import BaseModel, Field

from flext_web.config import FlextWebConfig
from flext_web.constants import FlextWebConstants


class FlextWebApp:
    """Generic FastAPI application factory using flext-core patterns and SOLID principles.

    Single Responsibility: Only handles FastAPI application creation and configuration.
    Uses flext-web config models for type-safe configuration management.
    Delegates to flext-core for logging, container management, and error handling.
    """

    def __init__(self) -> None:
        """Initialize with flext-core container and logger."""
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)

    # =========================================================================
    # FASTAPI CONFIGURATION MODELS - Pydantic Integration
    # =========================================================================

    class FastAPIConfig(BaseModel):
        """Pydantic model for FastAPI application configuration."""

        title: str = Field(default="HTTP API", min_length=1, max_length=100)
        version: str = Field(default="1.0.0", pattern=r"^\d+\.\d+\.\d+$")
        description: str = Field(default="Generic HTTP API", max_length=500)
        docs_url: str | None = Field(default="/docs")
        redoc_url: str | None = Field(default="/redoc")
        openapi_url: str | None = Field(default="/openapi.json")
        root_path: str = Field(default="")

        @classmethod
        def from_web_config(cls, config: FlextWebConfig) -> FlextWebApp.FastAPIConfig:
            """Create FastAPI config from FlextWebConfig."""
            return cls(
                title=config.app_name,
                version=config.version,
                description=f"{config.app_name} - HTTP API Service",
            )

    # =========================================================================
    # FASTAPI APPLICATION FACTORY - Single Responsibility
    # =========================================================================

    @classmethod
    def create_fastapi_app(
        cls, config: FlextWebConfig | dict[str, Any] | None = None
    ) -> FlextResult[FastAPI]:
        """Create FastAPI app with flext-core integration and Pydantic validation.

        Single Responsibility: Creates and configures FastAPI application only.
        Uses Pydantic models for configuration validation and type safety.
        Delegates logging and error handling to flext-core patterns.

        Args:
            config: Configuration object (FlextWebConfig or compatible)

        Returns:
            FlextResult[FastAPI]: Success contains configured FastAPI app,
                                failure contains detailed error message

        """
        logger = FlextLogger(__name__)

        try:
            # Convert config to Pydantic model for validation
            if isinstance(config, FlextWebConfig):
                fastapi_config = cls.FastAPIConfig.from_web_config(config)
            elif isinstance(config, dict):
                # Handle dict config objects
                fastapi_config = cls.FastAPIConfig(
                    title=config.get(
                        "app_name", "HTTP API"
                    ),
                    version=config.get(
                        "version", "1.0.0"
                    ),
                    description=config.get("description", "Generic HTTP API"),
                )
            elif config is None:
                # Use default configuration
                fastapi_config = cls.FastAPIConfig()
            else:
                # Handle generic config objects with getattr
                fastapi_config = cls.FastAPIConfig(
                    title=getattr(
                        config,
                        "app_name",
                        FlextWebConstants.WebSpecific.DEFAULT_APP_NAME,
                    ),
                    version=getattr(
                        config, "version", FlextWebConstants.WebSpecific.DEFAULT_VERSION
                    ),
                    description=getattr(config, "description", "Generic HTTP API"),
                )

            # Create FastAPI application with validated config
            app = FastAPI(
                title=fastapi_config.title,
                version=fastapi_config.version,
                description=fastapi_config.description,
                docs_url=fastapi_config.docs_url,
                redoc_url=fastapi_config.redoc_url,
                openapi_url=fastapi_config.openapi_url,
                root_path=fastapi_config.root_path,
            )

            # Add health endpoint using flext-core patterns
            app.add_api_route(
                "/health",
                cls._create_health_handler(),
                methods=["GET"],
                tags=["Health"],
                summary="Service health check",
                description="Returns service health status and metadata",
            )

            # Add info endpoint for API metadata
            app.add_api_route(
                "/info",
                cls._create_info_handler(fastapi_config),
                methods=["GET"],
                tags=["Info"],
                summary="API information",
                description="Returns API metadata and configuration",
            )

            logger.info(
                f"FastAPI application '{fastapi_config.title}' v{fastapi_config.version} created"
            )
            return FlextResult.ok(app)

        except Exception as e:
            logger.exception("FastAPI creation failed")
            return FlextResult.fail(f"FastAPI creation failed: {e}")

    # =========================================================================
    # HEALTH AND INFO HANDLERS - Focused Responsibilities
    # =========================================================================

    @staticmethod
    def _create_health_handler() -> Callable[[], dict[str, Any]]:
        """Create health check handler function."""

        def health_check() -> dict[str, Any]:
            return {
                "status": "healthy",
                "service": "flext-web",
                "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
            }

        return health_check

    @staticmethod
    def _create_info_handler(config: FastAPIConfig) -> Callable[[], dict[str, Any]]:
        """Create API info handler function."""

        def api_info() -> dict[str, Any]:
            return {
                "title": config.title,
                "version": config.version,
                "description": config.description,
                "service": "flext-web",
                "docs_url": config.docs_url,
                "redoc_url": config.redoc_url,
            }

        return api_info

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
