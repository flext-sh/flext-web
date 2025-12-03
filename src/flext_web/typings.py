"""FLEXT Web Types - Domain-specific web type definitions using Pydantic models.

This module provides web-specific type definitions using FlextWebModels.
Uses Pydantic 2 models instead of dict types for better type safety and validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TypedDict

from flext_core import FlextResult, t

from flext_web.constants import FlextWebConstants
from flext_web.models import FlextWebModels

# Import aliases for simplified usage
u = FlextUtilities
t = t
c = FlextWebConstants
m = FlextWebModels

HttpMethod = FlextWebConstants.Http.Method


class _WebRequestConfig(TypedDict, total=False):
    """Web request configuration dictionary."""

    url: str
    method: FlextWebConstants.Literals.HttpMethodLiteral | str
    headers: dict[str, str] | None
    body: str | dict[str, str] | None
    timeout: float
    query_params: dict[str, object] | None
    client_ip: str
    user_agent: str


class _WebResponseConfig(TypedDict, total=False):
    """Web response configuration dictionary."""

    status_code: int
    request_id: str
    headers: dict[str, str] | None
    body: str | dict[str, str] | None
    elapsed_time: float
    content_type: FlextWebConstants.Literals.ContentTypeLiteral | str
    content_length: int
    processing_time_ms: float


class _ApplicationConfig(TypedDict, total=False):
    """Application configuration dictionary."""

    name: str
    host: str
    port: int
    status: FlextWebConstants.Literals.ApplicationStatusLiteral | str
    environment: str
    debug_mode: bool
    version: int


class FlextWebTypes(t):
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
    # ApplicationStatus - use constants instead (StrEnum from constants)
    ApplicationStatus = FlextWebConstants.WebEnvironment.Status

    # Application data types - use Pydantic model instead of dict
    AppData: type = FlextWebModels.Service.AppResponse

    # Health response type - use Pydantic model instead of dict
    HealthResponse: type = FlextWebModels.Service.HealthResponse

    # =========================================================================
    # TYPE ALIASES - Using Pydantic models and Protocols
    # =========================================================================

    # Core data types - use Protocols and specific types
    class Core:
        """Core type aliases for request/response data."""

        ConfigValue: type = str | int | bool | list[str]
        RequestDict: type = dict[
            str, str | int | bool | list[str] | dict[str, str | int | bool]
        ]
        ResponseDict: type = dict[
            str, str | int | bool | list[str] | dict[str, str | int | bool]
        ]

    # Core response types - use Pydantic models
    SuccessResponse = FlextWebModels.Service.ServiceResponse
    BaseResponse = FlextWebModels.Service.ServiceResponse
    ErrorResponse = FlextWebModels.Service.ServiceResponse

    # ResponseDict wrapper for FlextService - use TypeAlias for registration compatibility
    # FlextService registration requires TypeAlias, not direct assignment
    class Data:
        """Data type definitions for FlextService compatibility."""

        WebResponseDict: type = dict[
            str, str | int | bool | list[str] | dict[str, str | int | bool]
        ]

    # Configuration types - use Pydantic model
    WebConfigDict = FlextWebModels.Application.EntityConfig
    AppConfigDict = FlextWebModels.Application.EntityConfig

    # =========================================================================
    # FACTORY METHODS - Create instances of Pydantic models
    # =========================================================================

    @classmethod
    def create_http_request(
        cls,
        url: str,
        method: FlextWebConstants.Literals.HttpMethodLiteral | str = (
            FlextWebConstants.Http.Method.GET
        ),
        headers: dict[str, str] | None = None,
        body: str | dict[str, str] | None = None,
        timeout: float = FlextWebConstants.Http.DEFAULT_TIMEOUT_SECONDS,
    ) -> FlextResult[FlextWebModels.Http.Request]:
        """Create HTTP request model instance with proper validation.

        Args:
            url: Request URL
            method: HTTP method (must be valid from constants)
            headers: Request headers (validated, no fallback)
            body: Request body
            timeout: Request timeout in seconds

        Returns:
            FlextResult[Http.Request]: Success contains request model,
                                     failure contains validation error

        """
        # Validate method against constants - fast fail, no fallback
        valid_methods = set(FlextWebConstants.Http.METHODS)
        method_upper = method.upper()
        if method_upper not in valid_methods:
            return FlextResult[FlextWebModels.Http.Request].fail(
                f"Invalid HTTP method: {method}. Must be one of: {valid_methods}"
            )

        # Validate headers - no fallback, use Pydantic default_factory
        if headers is not None and not isinstance(headers, dict):
            return FlextResult[FlextWebModels.Http.Request].fail(
                "Headers must be a dictionary or None"
            )

        try:
            # Validate method is valid Literal value - fast fail
            valid_methods_set = set(FlextWebConstants.Http.METHODS)
            if method_upper not in valid_methods_set:
                return FlextResult[
                    FlextWebModels.Http.Request
                ].fail(  # pragma: no cover
                    f"Invalid HTTP method: {method_upper}"
                )
            # Type narrowing: use match/case for type safety
            # Pydantic will validate at runtime, this ensures type checker understands
            match method_upper:
                case "GET" | "POST" | "PUT" | "DELETE" | "PATCH" | "HEAD" | "OPTIONS":
                    # Use empty dict if None - headers field requires dict
                    request_headers = headers if headers is not None else {}
                    request = FlextWebModels.Http.Request(
                        url=url,
                        method=method_upper,  # Type narrowed by match/case
                        headers=request_headers,
                        body=body,
                        timeout=timeout,
                    )
                    return FlextResult[FlextWebModels.Http.Request].ok(request)
                case _:  # pragma: no cover
                    return FlextResult[FlextWebModels.Http.Request].fail(
                        f"Invalid HTTP method: {method_upper}"
                    )
        except Exception as e:
            return FlextResult[FlextWebModels.Http.Request].fail(
                f"Failed to create HTTP request: {e}"
            )

    @classmethod
    def create_http_response(
        cls,
        status_code: int,
        headers: dict[str, str] | None = None,
        body: str | dict[str, str] | None = None,
        elapsed_time: float | None = None,
    ) -> FlextResult[FlextWebModels.Http.Response]:
        """Create HTTP response model instance with proper validation.

        Args:
            status_code: HTTP status code
            headers: Response headers (validated, no fallback)
            body: Response body
            elapsed_time: Response processing time

        Returns:
            FlextResult[Http.Response]: Success contains response model,
                                      failure contains validation error

        """
        # Validate headers - no fallback, use Pydantic default_factory
        if headers is not None and not isinstance(headers, dict):
            return FlextResult[FlextWebModels.Http.Response].fail(
                "Headers must be a dictionary or None"
            )

        try:
            # Use empty dict if None - headers field requires dict
            response_headers = headers if headers is not None else {}
            response = FlextWebModels.Http.Response(
                status_code=status_code,
                headers=response_headers,
                body=body,
                elapsed_time=elapsed_time,
            )
            return FlextResult[FlextWebModels.Http.Response].ok(response)
        except Exception as e:
            return FlextResult[FlextWebModels.Http.Response].fail(
                f"Failed to create HTTP response: {e}"
            )

    @classmethod
    def create_web_request(
        cls, config: _WebRequestConfig
    ) -> FlextResult[FlextWebModels.Web.Request]:
        """Create web request model instance with proper validation.

        Args:
            config: Web request configuration dictionary

        Returns:
            FlextResult[Web.Request]: Success contains request model,
                                     failure contains validation error

        """
        # Extract values with defaults
        url = config.get("url", "")
        method = config.get("method", FlextWebConstants.Http.Method.GET)
        headers = config.get("headers")
        body = config.get("body")
        timeout = config.get("timeout", FlextWebConstants.Http.DEFAULT_TIMEOUT_SECONDS)
        query_params = config.get("query_params")
        client_ip = config.get("client_ip", "")
        user_agent = config.get("user_agent", "")

        # Validate using uturns
        validations = [
            (url, "URL is required"),
            (
                isinstance(headers, dict) if headers is not None else True,
                "Headers must be a dictionary or None",
            ),
            (
                isinstance(query_params, dict) if query_params is not None else True,
                "Query params must be a dictionary or None",
            ),
        ]

        failed = u.find(validations, lambda v: not v[0])
        if failed:
            error_msg = (
                str(failed[1]) if isinstance(failed[1], str) else "Validation failed"
            )
            return FlextResult[FlextWebModels.Web.Request].fail(error_msg)

        # Validate method
        valid_methods = set(FlextWebConstants.Http.METHODS)
        method_upper = str(method).upper()
        if method_upper not in valid_methods:
            return FlextResult[FlextWebModels.Web.Request].fail(
                f"Invalid HTTP method: {method}. Must be one of: {valid_methods}"
            )

        try:
            # Type narrowing: use match/case for type safety
            match method_upper:
                case "GET" | "POST" | "PUT" | "DELETE" | "PATCH" | "HEAD" | "OPTIONS":
                    request = FlextWebModels.Web.Request(
                        url=url,
                        method=method_upper,
                        headers=headers if headers is not None else {},
                        body=body,
                        timeout=timeout,
                        query_params=query_params if query_params is not None else {},
                        client_ip=client_ip,
                        user_agent=user_agent,
                    )
                    return FlextResult[FlextWebModels.Web.Request].ok(request)
                case _:  # pragma: no cover
                    return FlextResult[FlextWebModels.Web.Request].fail(
                        f"Invalid HTTP method: {method_upper}"
                    )
        except Exception as e:
            return FlextResult[FlextWebModels.Web.Request].fail(
                f"Failed to create web request: {e}"
            )

    @classmethod
    def create_web_response(
        cls, config: _WebResponseConfig
    ) -> FlextResult[FlextWebModels.Web.Response]:
        """Create web response model instance with proper validation.

        Args:
            config: Web response configuration dictionary

        Returns:
            FlextResult[Web.Response]: Success contains response model,
                                      failure contains validation error

        """
        # Extract values with defaults
        status_code = config.get("status_code", 200)
        request_id = config.get("request_id", "")
        headers = config.get("headers")
        body = config.get("body")
        elapsed_time = config.get("elapsed_time", 0.0)
        content_type = config.get(
            "content_type", FlextWebConstants.Http.CONTENT_TYPE_JSON
        )
        content_length = config.get("content_length", 0)
        processing_time_ms = config.get("processing_time_ms", 0.0)

        # Validate headers
        if headers is not None and not isinstance(headers, dict):
            return FlextResult[FlextWebModels.Web.Response].fail(
                "Headers must be a dictionary or None"
            )

        try:
            response = FlextWebModels.Web.Response(
                status_code=status_code,
                request_id=request_id,
                headers=headers if headers is not None else {},
                body=body,
                elapsed_time=elapsed_time,
                content_type=content_type,
                content_length=content_length,
                processing_time_ms=processing_time_ms,
            )
            return FlextResult[FlextWebModels.Web.Response].ok(response)
        except Exception as e:
            return FlextResult[FlextWebModels.Web.Response].fail(
                f"Failed to create web response: {e}"
            )

    @classmethod
    def create_application(
        cls, config: _ApplicationConfig
    ) -> FlextResult[FlextWebModels.Application.Entity]:
        """Create application model instance.

        Args:
            config: Application configuration dictionary

        Returns:
            FlextResult[Application.Entity]: Success contains application entity,
                                            failure contains error message

        """
        # Extract values with defaults
        name = config.get("name", "")
        host = config.get("host", "localhost")
        port = config.get("port", 8080)
        status = config.get(
            "status", FlextWebConstants.WebEnvironment.Status.STOPPED.value
        )
        environment = config.get(
            "environment", FlextWebConstants.WebEnvironment.Name.DEVELOPMENT.value
        )
        debug_mode = config.get("debug_mode", FlextWebConstants.WebDefaults.DEBUG_MODE)
        version = config.get("version", FlextWebConstants.WebDefaults.VERSION_INT)

        try:
            entity = FlextWebModels.Application.Entity(
                name=name,
                host=host,
                port=port,
                status=status,
                environment=environment,
                debug_mode=debug_mode,
                version=version,
                domain_events=[],
            )
            return FlextResult[FlextWebModels.Application.Entity].ok(entity)
        except Exception as e:
            return FlextResult[FlextWebModels.Application.Entity].fail(
                f"Failed to create application: {e}"
            )

    # =========================================================================
    # TYPE SYSTEM CONFIGURATION
    # =========================================================================

    class TypesConfig:
        """Configuration model for web types system."""

        def __init__(
            self,
            *,
            use_pydantic_models: bool = True,
            enable_runtime_validation: bool = True,
            models_available: list[str] | None = None,
        ) -> None:
            """Initialize types configuration."""
            self.use_pydantic_models = use_pydantic_models
            self.enable_runtime_validation = enable_runtime_validation
            self.models_available = (
                [
                    "Http.Message",
                    "Http.Request",
                    "Http.Response",
                    "Web.Request",
                    "Web.Response",
                    "Application.Entity",
                ]
                if models_available is None
                else models_available
            )

    @classmethod
    def configure_web_types_system(
        cls,
        *,
        use_pydantic_models: bool = True,
        enable_runtime_validation: bool = True,
        models_available: list[str] | None = None,
    ) -> FlextResult[FlextWebTypes.TypesConfig]:
        """Configure web types system to use Pydantic models.

        Args:
            use_pydantic_models: Enable Pydantic model usage
            enable_runtime_validation: Enable runtime validation
            models_available: List of available model names

        Returns:
            FlextResult[TypesConfig]: Configuration result

        """
        try:
            config = cls.TypesConfig(
                use_pydantic_models=use_pydantic_models,
                enable_runtime_validation=enable_runtime_validation,
                models_available=(
                    [
                        "Http.Message",
                        "Http.Request",
                        "Http.Response",
                        "Web.Request",
                        "Web.Response",
                        "Application.Entity",
                    ]
                    if models_available is None
                    else models_available
                ),
            )
            return FlextResult[FlextWebTypes.TypesConfig].ok(config)
        except Exception as e:  # pragma: no cover
            return FlextResult[FlextWebTypes.TypesConfig].fail(
                f"Failed to configure web types system: {e}",
            )

    @classmethod
    def get_web_types_system_config(
        cls,
    ) -> FlextResult[FlextWebTypes.TypesConfig]:
        """Get current web types system configuration.

        Returns:
            FlextResult[TypesConfig]: Current configuration

        """
        try:
            config = cls.TypesConfig()
            return FlextResult[FlextWebTypes.TypesConfig].ok(config)
        except Exception as e:  # pragma: no cover
            return FlextResult[FlextWebTypes.TypesConfig].fail(
                f"Failed to get web types system config: {e}",
            )

    # =========================================================================
    # WEB PROJECT TYPES - Domain-specific project types extending t
    # =========================================================================

    class Project(t):
        """Web-specific project types extending t.

        Adds web application-specific project types while inheriting
        generic types from t. Follows domain separation principle:
        Web domain owns web application-specific types.
        """

        # Web-specific project configurations - use Pydantic models
        WebProjectConfig = FlextWebModels.Application.EntityConfig
        ApplicationConfig = FlextWebModels.Application.EntityConfig
        WebServerConfig = FlextWebModels.Application.EntityConfig
        WebPipelineConfig = FlextWebModels.Application.EntityConfig


__all__ = [
    "FlextWebTypes",
]
