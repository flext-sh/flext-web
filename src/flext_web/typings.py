"""FLEXT Web Types - Domain-specific web type definitions using Pydantic models.

This module provides web-specific type definitions using FlextWebModels.
Uses Pydantic 2 models instead of dict types for better type safety and validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TypeAlias, TypedDict, cast

from flext_core import FlextResult, FlextUtilities, t

from flext_web.constants import FlextWebConstants
from flext_web.models import FlextWebModels

# Import aliases for simplified usage (DSL pattern)
u = FlextUtilities
c = FlextWebConstants
m = FlextWebModels

HttpMethod = FlextWebConstants.Http.Method


class _WebRequestConfig(TypedDict, total=False):
    """Web request configuration dictionary."""

    url: str
    method: str
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
    content_type: str
    content_length: int
    processing_time_ms: float


class _ApplicationConfig(TypedDict, total=False):
    """Application configuration dictionary."""

    name: str
    host: str
    port: int
    status: str
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
    # PYDANTIC MODEL CLASSES - Use inheritance instead of aliases
    # =========================================================================

    # HTTP protocol models - proper inheritance from FlextWebModels
    class HttpMessage(FlextWebModels.Http.Message):
        """HTTP message model - inherits from FlextWebModels.Http.Message."""

    class HttpRequest(FlextWebModels.Http.Request):
        """HTTP request model - inherits from FlextWebModels.Http.Request."""

    class HttpResponse(FlextWebModels.Http.Response):
        """HTTP response model - inherits from FlextWebModels.Http.Response."""

    # Web-specific models - proper inheritance from FlextWebModels
    class WebRequest(FlextWebModels.Web.Request):
        """Web request model - inherits from FlextWebModels.Web.Request."""

    class WebResponse(FlextWebModels.Web.Response):
        """Web response model - inherits from FlextWebModels.Web.Response."""

    # Application models - proper inheritance from FlextWebModels
    class ApplicationEntity(FlextWebModels.Application.Entity):
        """Application entity model - inherits from FlextWebModels.Application.Entity."""

    # ApplicationStatus - StrEnum cannot be inherited (Python limitation)
    ApplicationStatus = FlextWebConstants.WebEnvironment.Status

    # Application data types - proper inheritance from FlextWebModels
    class AppData(FlextWebModels.Service.AppResponse):
        """Application data model - inherits from FlextWebModels.Service.AppResponse."""

    # Health response type - proper inheritance from FlextWebModels
    class HealthResponse(FlextWebModels.Service.HealthResponse):
        """Health response model - inherits from FlextWebModels.Service.HealthResponse."""

    # =========================================================================
    # TYPE ALIASES - Using Pydantic models and Protocols
    # =========================================================================

    # Core data types - use Protocols and specific types
    class Core:
        """Core type aliases for request/response data."""

        ConfigValue: TypeAlias = str | int | bool | list[str]
        RequestDict: TypeAlias = dict[
            str,
            str | int | bool | list[str] | dict[str, str | int | bool],
        ]
        ResponseDict: TypeAlias = dict[
            str,
            str | int | bool | list[str] | dict[str, str | int | bool],
        ]

    # Core response types - proper inheritance from FlextWebModels
    class SuccessResponse(FlextWebModels.Service.ServiceResponse):
        """Success response model - inherits from FlextWebModels.Service.ServiceResponse."""

    class BaseResponse(FlextWebModels.Service.ServiceResponse):
        """Base response model - inherits from FlextWebModels.Service.ServiceResponse."""

    class ErrorResponse(FlextWebModels.Service.ServiceResponse):
        """Error response model - inherits from FlextWebModels.Service.ServiceResponse."""

    # ResponseDict wrapper for FlextService - use TypeAlias for registration compatibility
    # FlextService registration requires TypeAlias, not direct assignment
    class Data:
        """Data type definitions for FlextService compatibility."""

        WebResponseDict: TypeAlias = dict[
            str,
            str | int | bool | list[str] | dict[str, str | int | bool],
        ]

    # Configuration types - proper inheritance from FlextWebModels
    class WebConfigDict(FlextWebModels.Application.EntityConfig):
        """Web configuration dictionary model - inherits from FlextWebModels.Application.EntityConfig."""

    class AppConfigDict(FlextWebModels.Application.EntityConfig):
        """Application configuration dictionary model - inherits from FlextWebModels.Application.EntityConfig."""

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
        # Use u.guard() for unified method validation (DSL pattern)
        method_upper = method.upper()
        valid_methods = set(FlextWebConstants.Http.METHODS)
        method_validated = u.guard(
            method_upper,
            lambda m: m in valid_methods,
            error_message=f"Invalid HTTP method: {method}. Must be one of: {valid_methods}",
            return_value=True,
        )
        if method_validated is None:
            return FlextResult[FlextWebModels.Http.Request].fail(
                f"Invalid HTTP method: {method}. Must be one of: {valid_methods}",
            )

        # Use u.guard() for unified headers validation (DSL pattern)
        # Validate headers - must be dict or None
        if headers is not None and not isinstance(headers, dict):
            return FlextResult[FlextWebModels.Http.Request].fail(
                "Headers must be a dictionary or None",
            )
        headers_validated = headers if isinstance(headers, dict) else {}

        # Use u.try_() for unified error handling (DSL pattern)
        def create_request() -> FlextWebModels.Http.Request:
            """Create request model."""
            # Cast body to match model type (dict[str, object] | str | None)
            body_typed: str | dict[str, object] | None = (
                cast("dict[str, object]", body) if isinstance(body, dict) else body
            )
            return FlextWebModels.Http.Request(
                url=url,
                method=method_upper,
                headers=headers_validated or {},
                body=body_typed,
                timeout=timeout,
            )

        # Use u.try_() with custom exception handling for better error messages
        try:
            request = create_request()
            return FlextResult[FlextWebModels.Http.Request].ok(request)
        except Exception as exc:
            # Use u.err() pattern for unified error extraction (DSL pattern)
            error_msg = f"Failed to create HTTP request: {exc}"
            return FlextResult[FlextWebModels.Http.Request].fail(error_msg)

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
        # Use u.guard() for unified headers validation (DSL pattern)
        # Validate headers - must be dict or None
        if headers is not None and not isinstance(headers, dict):
            return FlextResult[FlextWebModels.Http.Response].fail(
                "Headers must be a dictionary or None",
            )
        headers_validated = headers if isinstance(headers, dict) else {}

        # Use u.try_() for unified error handling (DSL pattern)
        def create_response() -> FlextWebModels.Http.Response:
            """Create response model."""
            # Cast body to match model type (dict[str, object] | str | None)
            body_typed: str | dict[str, object] | None = (
                cast("dict[str, object]", body) if isinstance(body, dict) else body
            )
            return FlextWebModels.Http.Response(
                status_code=status_code,
                headers=headers_validated or {},
                body=body_typed,
                elapsed_time=elapsed_time,
            )

        # Use u.try_() with custom exception handling for better error messages
        try:
            response = create_response()
            return FlextResult[FlextWebModels.Http.Response].ok(response)
        except Exception as exc:
            # Use u.err() pattern for unified error extraction (DSL pattern)
            return FlextResult[FlextWebModels.Http.Response].fail(
                f"Failed to create HTTP response: {exc}",
            )

    @classmethod
    def create_web_request(
        cls,
        config: _WebRequestConfig,
    ) -> FlextResult[FlextWebModels.Web.Request]:
        """Create web request model instance with proper validation.

        Args:
            config: Web request configuration dictionary

        Returns:
            FlextResult[Web.Request]: Success contains request model,
                                     failure contains validation error

        """
        # Use u.get() for unified extraction with defaults (DSL pattern)
        url = u.get(config, "url", default="")
        method = u.get(config, "method", default=FlextWebConstants.Http.Method.GET)
        headers = u.get(config, "headers")
        body = u.get(config, "body")
        timeout = u.get(
            config,
            "timeout",
            default=FlextWebConstants.Http.DEFAULT_TIMEOUT_SECONDS,
        )
        query_params = u.get(config, "query_params")
        client_ip = u.get(config, "client_ip", default="")
        user_agent = u.get(config, "user_agent", default="")

        # Use u.guard() for unified validation (DSL pattern)
        url_validated = u.guard(url, str, "non_empty", return_value=True)
        if not url_validated:
            return FlextResult[FlextWebModels.Web.Request].fail("URL is required")

        # Use u.guard() for headers and query_params validation (DSL pattern)
        # Validate headers - must be dict or None
        if headers is not None and not isinstance(headers, dict):
            return FlextResult[FlextWebModels.Web.Request].fail(
                "Headers must be a dictionary or None",
            )
        headers_validated = headers if isinstance(headers, dict) else {}
        # Validate query_params - must be dict or None
        if query_params is not None and not isinstance(query_params, dict):
            return FlextResult[FlextWebModels.Web.Request].fail(
                "Query params must be a dictionary or None",
            )
        query_params_validated = query_params if isinstance(query_params, dict) else {}

        # Use u.guard() for method validation (DSL pattern)
        method_upper = str(method).upper()
        valid_methods = set(FlextWebConstants.Http.METHODS)
        method_validated = u.guard(
            method_upper,
            lambda m: m in valid_methods,
            error_message=f"Invalid HTTP method: {method}. Must be one of: {valid_methods}",
            return_value=True,
        )
        if method_validated is None:
            return FlextResult[FlextWebModels.Web.Request].fail(
                f"Invalid HTTP method: {method}. Must be one of: {valid_methods}",
            )

        # Use u.try_() for unified error handling (DSL pattern)
        def create_request() -> FlextWebModels.Web.Request:
            """Create request model."""
            return FlextWebModels.Web.Request(
                url=url_validated,
                method=method_upper,
                headers=headers_validated or {},
                body=body,
                timeout=timeout,
                query_params=query_params_validated or {},
                client_ip=client_ip,
                user_agent=user_agent,
            )

        # Use u.try_() with custom exception handling for better error messages
        try:
            request = create_request()
            return FlextResult[FlextWebModels.Web.Request].ok(request)
        except Exception as exc:
            # Use u.err() pattern for unified error extraction (DSL pattern)
            return FlextResult[FlextWebModels.Web.Request].fail(
                f"Failed to create web request: {exc}",
            )

    @classmethod
    def create_web_response(
        cls,
        config: _WebResponseConfig,
    ) -> FlextResult[FlextWebModels.Web.Response]:
        """Create web response model instance with proper validation.

        Args:
            config: Web response configuration dictionary

        Returns:
            FlextResult[Web.Response]: Success contains response model,
                                      failure contains validation error

        """
        # Use u.get() for unified extraction with defaults (DSL pattern)
        status_code = u.get(config, "status_code", default=200)
        request_id = u.get(config, "request_id", default="")
        headers = u.get(config, "headers")
        body = u.get(config, "body")
        elapsed_time = u.get(config, "elapsed_time", default=0.0)
        content_type = u.get(
            config,
            "content_type",
            default=FlextWebConstants.Http.CONTENT_TYPE_JSON,
        )
        content_length = u.get(config, "content_length", default=0)
        processing_time_ms = u.get(config, "processing_time_ms", default=0.0)

        # Use u.guard() for unified headers validation (DSL pattern)
        # Validate headers - must be dict or None
        if headers is not None and not isinstance(headers, dict):
            return FlextResult[FlextWebModels.Web.Response].fail(
                "Headers must be a dictionary or None",
            )
        headers_validated = headers if isinstance(headers, dict) else {}

        # Use u.try_() for unified error handling (DSL pattern)
        def create_response() -> FlextWebModels.Web.Response:
            """Create response model."""
            return FlextWebModels.Web.Response(
                status_code=status_code,
                request_id=request_id,
                headers=headers_validated or {},
                body=body,
                elapsed_time=elapsed_time,
                content_type=content_type,
                content_length=content_length,
                processing_time_ms=processing_time_ms,
            )

        # Use u.try_() with custom exception handling for better error messages
        try:
            response = create_response()
            return FlextResult[FlextWebModels.Web.Response].ok(response)
        except Exception as exc:
            # Use u.err() pattern for unified error extraction (DSL pattern)
            return FlextResult[FlextWebModels.Web.Response].fail(
                f"Failed to create web response: {exc}",
            )

    @classmethod
    def create_application(
        cls,
        config: _ApplicationConfig,
    ) -> FlextResult[FlextWebModels.Application.Entity]:
        """Create application model instance.

        Args:
            config: Application configuration dictionary

        Returns:
            FlextResult[Application.Entity]: Success contains application entity,
                                            failure contains error message

        """
        # Use u.get() for unified extraction with defaults (DSL pattern)
        name = u.get(config, "name", default="")
        host = u.get(config, "host", default="localhost")
        port_raw = u.get(config, "port", default=8080)
        port = port_raw if isinstance(port_raw, int) else 8080
        status = u.get(
            config,
            "status",
            default=FlextWebConstants.WebEnvironment.Status.STOPPED.value,
        )
        environment = u.get(
            config,
            "environment",
            default=FlextWebConstants.WebEnvironment.Name.DEVELOPMENT.value,
        )
        debug_mode_raw = u.get(
            config,
            "debug_mode",
            default=FlextWebConstants.WebDefaults.DEBUG_MODE,
        )
        debug_mode = (
            debug_mode_raw
            if isinstance(debug_mode_raw, bool)
            else FlextWebConstants.WebDefaults.DEBUG_MODE
        )
        version_raw = u.get(
            config,
            "version",
            default=FlextWebConstants.WebDefaults.VERSION_INT,
        )
        version = (
            version_raw
            if isinstance(version_raw, int)
            else FlextWebConstants.WebDefaults.VERSION_INT
        )

        # Use u.try_() for unified error handling (DSL pattern)
        def create_entity() -> FlextWebModels.Application.Entity:
            """Create application entity."""
            return FlextWebModels.Application.Entity(
                name=name,
                host=host,
                port=port,
                status=status,
                environment=environment,
                debug_mode=debug_mode,
                version=version,
                domain_events=[],
            )

        # Use u.try_() with custom exception handling for better error messages
        try:
            entity = create_entity()
            return FlextResult[FlextWebModels.Application.Entity].ok(entity)
        except Exception as exc:
            # Use u.err() pattern for unified error extraction (DSL pattern)
            return FlextResult[FlextWebModels.Application.Entity].fail(
                f"Failed to create application: {exc}",
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

        # Web-specific project configurations - proper inheritance from FlextWebModels
        class WebProjectConfig(FlextWebModels.Application.EntityConfig):
            """Web project configuration model - inherits from FlextWebModels.Application.EntityConfig."""

        class ApplicationConfig(FlextWebModels.Application.EntityConfig):
            """Application configuration model - inherits from FlextWebModels.Application.EntityConfig."""

        class WebServerConfig(FlextWebModels.Application.EntityConfig):
            """Web server configuration model - inherits from FlextWebModels.Application.EntityConfig."""

        class WebPipelineConfig(FlextWebModels.Application.EntityConfig):
            """Web pipeline configuration model - inherits from FlextWebModels.Application.EntityConfig."""


__all__ = [
    "FlextWebTypes",
]
