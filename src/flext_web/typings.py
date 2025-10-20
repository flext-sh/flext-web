"""FLEXT Web Types - Domain-specific web type definitions using Pydantic models.

This module provides web-specific type definitions using FlextWebModels.
Uses Pydantic 2 models instead of dict types for better type safety and validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Any

from flext_core import FlextResult, FlextTypes

from flext_web.models import FlextWebModels


class FlextWebTypes(FlextTypes):
    """Web-specific type definitions using FlextWebModels.

    Uses Pydantic 2 models from FlextWebModels for type safety.
    Provides type aliases and factory methods for web operations.
    Follows single unified class per module pattern.
    """

    # =========================================================================
    # PYDANTIC MODEL TYPE ALIASES - Use models instead of dict types
    # =========================================================================

    # HTTP protocol models
    HttpMessage = FlextWebModels.Http.Message
    HttpRequest = FlextWebModels.Http.Request
    HttpResponse = FlextWebModels.Http.Response

    # Web-specific models
    WebRequest = FlextWebModels.Web.Request
    WebResponse = FlextWebModels.Web.Response

    # Application models
    ApplicationEntity = FlextWebModels.Application.Entity
    ApplicationStatus = FlextWebModels.Application.EntityStatus

    # Application data types
    AppData = dict[str, object]

    # Health response type
    HealthResponse = dict[str, str]

    # =========================================================================
    # TYPE ALIASES FOR BACKWARD COMPATIBILITY
    # =========================================================================

    # Core data types
    class Core:
        """Core type aliases for request/response data."""

        ConfigValue = str | int | bool | list[str] | dict[str, object]
        RequestDict = dict[str, object]
        ResponseDict = dict[str, object]

    # Core response types (using Pydantic models where possible)
    SuccessResponse = dict[str, object]
    BaseResponse = dict[str, object]
    ErrorResponse = dict[str, object]

    # Configuration types (should use FlextWebConfig from config.py)
    WebConfigDict = dict[str, object]
    AppConfigDict = dict[str, object]

    # =========================================================================
    # FACTORY METHODS - Create instances of Pydantic models
    # =========================================================================

    @classmethod
    def create_http_request(
        cls, url: str, method: str = "GET", **kwargs: Any
    ) -> FlextWebModels.Http.Request:
        """Create HTTP request model instance."""
        # Validate method parameter
        valid_methods = {"GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"}
        if method.upper() not in valid_methods:
            method = "GET"  # Default to GET for invalid methods

        return FlextWebModels.Http.Request(url=url, method=method.upper(), **kwargs)

    @classmethod
    def create_http_response(
        cls, status_code: int, **kwargs: Any
    ) -> FlextWebModels.Http.Response:
        """Create HTTP response model instance."""
        return FlextWebModels.Http.Response(status_code=status_code, **kwargs)

    @classmethod
    def create_web_request(
        cls, url: str, method: str = "GET", **kwargs: Any
    ) -> FlextWebModels.Web.Request:
        """Create web request model instance."""
        # Validate method parameter
        valid_methods = {"GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"}
        if method.upper() not in valid_methods:
            method = "GET"  # Default to GET for invalid methods

        return FlextWebModels.Web.Request(url=url, method=method.upper(), **kwargs)

    @classmethod
    def create_web_response(
        cls, status_code: int, request_id: str, **kwargs: Any
    ) -> FlextWebModels.Web.Response:
        """Create web response model instance."""
        return FlextWebModels.Web.Response(
            status_code=status_code, request_id=request_id, **kwargs
        )

    @classmethod
    def create_application(
        cls, name: str, host: str = "localhost", port: int = 8080, **kwargs: Any
    ) -> FlextWebModels.Application.Entity:
        """Create application model instance."""
        return FlextWebModels.Application.Entity(
            name=name, host=host, port=port, **kwargs
        )

    # =========================================================================
    # TYPE SYSTEM CONFIGURATION
    # =========================================================================

    @classmethod
    def configure_web_types_system(
        cls,
        config: dict[str, object],
    ) -> FlextResult[dict[str, object]]:
        """Configure web types system to use Pydantic models.

        Args:
            config: Configuration dictionary for web types system

        Returns:
            FlextResult[dict[str, object]]: Configuration result

        """
        try:
            # Validate config keys - only allow known configuration keys
            allowed_keys = {
                "use_pydantic_models",
                "enable_runtime_validation",
                "models_available",
            }
            invalid_keys = set(config.keys()) - allowed_keys
            if invalid_keys:
                return FlextResult[dict[str, object]].fail(
                    f"Invalid configuration keys: {invalid_keys}"
                )

            validated_config: dict[str, object] = dict(config)
            validated_config.setdefault("use_pydantic_models", True)
            validated_config.setdefault("enable_runtime_validation", True)
            validated_config.setdefault(
                "models_available",
                [
                    "Http.Message",
                    "Http.Request",
                    "Http.Response",
                    "Web.Request",
                    "Web.Response",
                    "Application.Entity",
                ],
            )
            return FlextResult[dict[str, object]].ok(validated_config)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"Failed to configure web types system: {e}",
            )

    @classmethod
    def get_web_types_system_config(
        cls,
    ) -> FlextResult[dict[str, object]]:
        """Get current web types system configuration.

        Returns:
            FlextResult[dict[str, object]]: Current configuration

        """
        try:
            config: dict[str, object] = {
                "use_pydantic_models": True,
                "enable_runtime_validation": True,
                "total_model_classes": 6,
                "factory_methods": 5,
            }
            return FlextResult[dict[str, object]].ok(config)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"Failed to get web types system config: {e}",
            )

    # =========================================================================
    # WEB PROJECT TYPES - Domain-specific project types extending FlextTypes
    # =========================================================================

    class Project(FlextTypes):
        """Web-specific project types extending FlextTypes.

        Adds web application-specific project types while inheriting
        generic types from FlextTypes. Follows domain separation principle:
        Web domain owns web application-specific types.
        """

        # Web-specific project configurations
        type WebProjectConfig = dict[str, FlextWebTypes.Core.ConfigValue | object]
        type ApplicationConfig = dict[str, str | int | bool | list[str]]
        type WebServerConfig = dict[str, bool | str | dict[str, object]]
        type WebPipelineConfig = dict[str, FlextWebTypes.Core.ConfigValue | object]


__all__ = [
    "FlextWebTypes",
]
