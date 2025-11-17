"""FLEXT Web Types - Domain-specific web type definitions using Pydantic models.

This module provides web-specific type definitions using FlextWebModels.
Uses Pydantic 2 models instead of dict types for better type safety and validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Any, Protocol, TypeAlias, runtime_checkable

from flext_core import FlextResult, FlextTypes

from flext_web.constants import FlextWebConstants
from flext_web.models import FlextWebModels

# Type aliases - import from constants for centralized definition
HttpMethodLiteral = FlextWebConstants.HttpMethodLiteral
HttpMethod = FlextWebConstants.Http.Method
EnvironmentNameLiteral = FlextWebConstants.EnvironmentNameLiteral
ApplicationStatusLiteral = FlextWebConstants.ApplicationStatusLiteral
ApplicationTypeLiteral = FlextWebConstants.ApplicationTypeLiteral


@runtime_checkable
class ConfigValueProtocol(Protocol):
    """Protocol for configuration values."""

    def __str__(self) -> str: ...
    def __int__(self) -> int: ...
    def __bool__(self) -> bool: ...


@runtime_checkable
class ResponseDataProtocol(Protocol):
    """Protocol for response data structures."""

    def get(
        self, key: str, default: str | None = None
    ) -> str | int | bool | list[str] | None: ...


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
    # ApplicationStatus - use constants instead (StrEnum from constants)
    ApplicationStatus = FlextWebConstants.WebEnvironment.Status

    # Application data types - use Pydantic model instead of dict
    AppData: TypeAlias = FlextWebModels.Service.AppResponse

    # Health response type - use Pydantic model instead of dict
    HealthResponse: TypeAlias = FlextWebModels.Service.HealthResponse

    # =========================================================================
    # TYPE ALIASES - Using Pydantic models and Protocols
    # =========================================================================

    # Core data types - use Protocols and specific types
    class Core:
        """Core type aliases for request/response data."""

        ConfigValue: TypeAlias = str | int | bool | list[str]
        RequestDict: TypeAlias = dict[
            str, str | int | bool | list[str] | dict[str, str | int | bool]
        ]
        ResponseDict: TypeAlias = dict[
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

        WebResponseDict: TypeAlias = dict[
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
        method: str = FlextWebConstants.Http.Method.GET,
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
                return FlextResult[FlextWebModels.Http.Request].fail(
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
                case _:
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
        cls,
        url: str,
        method: str = FlextWebConstants.Http.Method.GET,
        headers: dict[str, str] | None = None,
        body: str | dict[str, str] | None = None,
        timeout: float = FlextWebConstants.Http.DEFAULT_TIMEOUT_SECONDS,
        query_params: dict[str, Any] | None = None,
        client_ip: str = "",
        user_agent: str = "",
    ) -> FlextResult[FlextWebModels.Web.Request]:
        """Create web request model instance with proper validation.

        Args:
            url: Request URL
            method: HTTP method (must be valid from constants)
            headers: Request headers (validated, no fallback)
            body: Request body
            timeout: Request timeout in seconds
            query_params: Query parameters (validated, no fallback)
            client_ip: Client IP address
            user_agent: User agent string

        Returns:
            FlextResult[Web.Request]: Success contains request model,
                                     failure contains validation error

        """
        # Validate method against constants - fast fail, no fallback
        valid_methods = set(FlextWebConstants.Http.METHODS)
        method_upper = method.upper()
        if method_upper not in valid_methods:
            return FlextResult[FlextWebModels.Web.Request].fail(
                f"Invalid HTTP method: {method}. Must be one of: {valid_methods}"
            )

        # Validate headers - no fallback
        if headers is not None and not isinstance(headers, dict):
            return FlextResult[FlextWebModels.Web.Request].fail(
                "Headers must be a dictionary or None"
            )

        # Validate query_params - no fallback
        if query_params is not None and not isinstance(query_params, dict):
            return FlextResult[FlextWebModels.Web.Request].fail(
                "Query params must be a dictionary or None"
            )

        try:
            # Validate method is valid Literal value - fast fail
            valid_methods_set = set(FlextWebConstants.Http.METHODS)
            if method_upper not in valid_methods_set:
                return FlextResult[FlextWebModels.Web.Request].fail(
                    f"Invalid HTTP method: {method_upper}"
                )
            # Type narrowing: use match/case for type safety
            # Pydantic will validate at runtime, this ensures type checker understands
            match method_upper:
                case "GET" | "POST" | "PUT" | "DELETE" | "PATCH" | "HEAD" | "OPTIONS":
                    # Use defaults if None - fields require specific types
                    request_headers = headers if headers is not None else {}
                    request_query_params = (
                        query_params if query_params is not None else {}
                    )
                    request = FlextWebModels.Web.Request(
                        url=url,
                        method=method_upper,  # Type narrowed by match/case
                        headers=request_headers,
                        body=body,
                        timeout=timeout,
                        query_params=request_query_params,
                        client_ip=client_ip,
                        user_agent=user_agent,
                    )
                    return FlextResult[FlextWebModels.Web.Request].ok(request)
                case _:
                    return FlextResult[FlextWebModels.Web.Request].fail(
                        f"Invalid HTTP method: {method_upper}"
                    )
        except Exception as e:
            return FlextResult[FlextWebModels.Web.Request].fail(
                f"Failed to create web request: {e}"
            )

    @classmethod
    def create_web_response(
        cls,
        status_code: int,
        request_id: str,
        headers: dict[str, str] | None = None,
        body: str | dict[str, str] | None = None,
        elapsed_time: float = 0.0,
        content_type: str = FlextWebConstants.Http.CONTENT_TYPE_JSON,
        content_length: int = 0,
        processing_time_ms: float = 0.0,
    ) -> FlextResult[FlextWebModels.Web.Response]:
        """Create web response model instance with proper validation.

        Args:
            status_code: HTTP status code
            request_id: Associated request identifier
            headers: Response headers (validated, no fallback)
            body: Response body
            elapsed_time: Response processing time
            content_type: Response content type
            content_length: Response content length
            processing_time_ms: Processing time in milliseconds

        Returns:
            FlextResult[Web.Response]: Success contains response model,
                                      failure contains validation error

        """
        # Validate headers - no fallback
        if headers is not None and not isinstance(headers, dict):
            return FlextResult[FlextWebModels.Web.Response].fail(
                "Headers must be a dictionary or None"
            )

        try:
            # Use defaults if None - fields require specific types
            response_headers = headers if headers is not None else {}
            response = FlextWebModels.Web.Response(
                status_code=status_code,
                request_id=request_id,
                headers=response_headers,
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
        cls,
        name: str,
        host: str = "localhost",
        port: int = 8080,
        status: str = FlextWebConstants.WebEnvironment.Status.STOPPED.value,
        environment: str = FlextWebConstants.WebEnvironment.Name.DEVELOPMENT.value,
        *,
        debug_mode: bool = FlextWebConstants.WebDefaults.DEBUG_MODE,
        version: int = FlextWebConstants.WebDefaults.VERSION_INT,
    ) -> FlextResult[FlextWebModels.Application.Entity]:
        """Create application model instance."""
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
        except Exception as e:
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
        except Exception as e:
            return FlextResult[FlextWebTypes.TypesConfig].fail(
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

        # Web-specific project configurations - use Pydantic models
        WebProjectConfig = FlextWebModels.Application.EntityConfig
        ApplicationConfig = FlextWebModels.Application.EntityConfig
        WebServerConfig = FlextWebModels.Application.EntityConfig
        WebPipelineConfig = FlextWebModels.Application.EntityConfig


__all__ = [
    "FlextWebTypes",
]
