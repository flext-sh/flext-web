"""FLEXT Web Types - Domain-specific web type definitions using Pydantic models.

This module provides web-specific type definitions using m.
Uses Pydantic 2 models instead of dict types for better type safety and validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Annotated, Literal

from flext_core import FlextTypes, r, u
from pydantic import Field

from flext_web import c, m


class _ApplicationConfig(m.Web.EntityConfig):
    name: Annotated[
        str,
        Field(default=c.Web.WebDefaults.APP_NAME, description="App name"),
    ]
    status: Annotated[
        str,
        Field(default=c.Web.Status.STOPPED.value, description="App status"),
    ]
    environment: Annotated[
        str,
        Field(
            default=c.Web.Name.DEVELOPMENT.value,
            description="Environment",
        ),
    ]
    debug_mode: Annotated[
        bool,
        Field(default=c.Web.WebDefaults.DEBUG_MODE, description="Debug"),
    ]
    version: Annotated[
        int,
        Field(default=c.Web.WebDefaults.VERSION_INT, description="Version"),
    ]


class _WebRequestConfig(m.Web.AppRequest):
    pass


class _WebResponseConfig(m.Web.AppResponse):
    pass


class FlextWebTypes(FlextTypes):
    """Web-specific type definitions using m.

    Uses Pydantic 2 models from m for type safety.
    Provides type aliases and factory methods for web operations.
    Follows single unified class per module pattern.
    """

    class HttpMessage(m.Web.Message):
        """HTTP message model - inherits from m.Web.Message."""

    class HttpRequest(m.Web.Request):
        """HTTP request model - inherits from m.Web.Request."""

    class HttpResponse(m.Web.Response):
        """HTTP response model - inherits from m.Web.Response."""

    WebRequest = m.Web.AppRequest
    "Web request model - references m.Web.AppRequest."
    WebResponse = m.Web.AppResponse
    "Web response model - references m.Web.AppResponse."

    class ApplicationEntity(m.Web.Entity):
        """Application entity model - inherits from m.Web.Entity."""

    ApplicationStatus = c.Web.Status

    class AppData(m.Web.ApplicationResponse):
        """Application data model - inherits from m.Web.ApplicationResponse."""

    HealthResponse = m.Web.HealthResponse
    "Health response model - references m.Web.HealthResponse."

    class Web:
        """Web core type aliases for request/response data.

        Provides organized access to all Web types for other FLEXT projects.
        Usage: Other projects can reference `t.Web.Http.*`, `t.Web.Project.*`, etc.
        This enables consistent namespace patterns for cross-project type access.
        """

        ConfigValue = str | int | bool | Sequence[str]
        type RequestDict = dict[
            str, str | int | bool | Sequence[str] | Mapping[str, str | int | bool]
        ]
        type ResponseDict = dict[
            str, str | int | bool | Sequence[str] | Mapping[str, str | int | bool]
        ]
        HttpMethodLiteral = Literal[
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "PATCH",
            "HEAD",
            "OPTIONS",
        ]
        EnvironmentNameLiteral = Literal[
            "development",
            "staging",
            "production",
            "testing",
        ]
        ApplicationStatusLiteral = Literal[
            "stopped",
            "starting",
            "running",
            "stopping",
            "error",
            "maintenance",
            "deploying",
        ]
        ApplicationTypeLiteral = Literal[
            "application",
            "service",
            "api",
            "microservice",
            "webapp",
            "spa",
            "dashboard",
            "REDACTED_LDAP_BIND_PASSWORD_panel",
        ]
        ResponseStatusLiteral = Literal["success", "error", "operational", "healthy"]
        ProtocolLiteral = Literal["http", "https"]
        ContentTypeLiteral = Literal["application/json", "text/plain", "text/html"]
        SameSiteLiteral = Literal["Lax", "Strict", "None"]

    class WebCore:
        """Compatibility namespace for request/response dict aliases."""

        type RequestDict = dict[
            str, str | int | bool | Sequence[str] | Mapping[str, str | int | bool]
        ]
        type ResponseDict = dict[
            str, str | int | bool | Sequence[str] | Mapping[str, str | int | bool]
        ]

    class Types:
        """Type system aliases for flext-web Removed redundant aliases."""

    SuccessResponse = m.Web.ServiceResponse
    "Success response model - references m.Web.ServiceResponse."
    BaseResponse = m.Web.ServiceResponse
    "Base response model - references m.Web.ServiceResponse."
    ErrorResponse = m.Web.ServiceResponse
    "Error response model - references m.Web.ServiceResponse."

    class Data:
        """Data type definitions for FlextService compatibility."""

        type ResponseDict = dict[
            str, str | int | bool | Sequence[str] | Mapping[str, str | int | bool]
        ]

    class WebConfigDict(m.Web.EntityConfig):
        """Web configuration dictionary model - inherits from m.Web.EntityConfig."""

    class AppConfigDict(m.Web.EntityConfig):
        """Application configuration dictionary model - inherits from m.Web.EntityConfig."""

    @classmethod
    def create_application(
        cls,
        config: _ApplicationConfig,
    ) -> r[m.Web.Entity]:
        """Create application model instance.

        Args:
            config: Application configuration model

        Returns:
            r[Web.Entity]: Success contains application entity,
                                            failure contains error message

        """
        name: str = config.name or ""
        host: str = config.host or "localhost"
        port: int = config.port or 8080
        status: str = config.status or c.Web.Status.STOPPED.value
        environment: str = config.environment or c.Web.Name.DEVELOPMENT.value
        debug_mode: bool = config.debug_mode
        version: int = config.version

        def create_entity() -> m.Web.Entity:
            """Create application entity."""
            return m.Web.Entity(
                name=name,
                host=host,
                port=port,
                status=status,
                environment=environment,
                debug_mode=debug_mode,
                version=version,
                domain_events=[],
            )

        try:
            entity = create_entity()
            return r[m.Web.Entity].ok(entity)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as exc:
            return r[m.Web.Entity].fail(f"Failed to create application: {exc}")

    @classmethod
    def create_http_request(
        cls,
        url: str,
        method: str = c.Web.Method.GET,
        headers: Mapping[str, str] | None = None,
        body: str | Mapping[str, FlextTypes.Scalar] | None = None,
        timeout: float = c.Web.Http.DEFAULT_TIMEOUT_SECONDS,
    ) -> r[m.Web.Request]:
        """Create HTTP request model instance with proper validation.

        Args:
            url: Request URL
            method: HTTP method (must be valid from constants)
            headers: Request headers (validated, no fallback)
            body: Request body
            timeout: Request timeout in seconds

        Returns:
            r[Web.Request]: Success contains request model,
                                     failure contains validation error

        """
        method_upper = method.upper()
        valid_methods = set(c.Web.Http.METHODS)

        def _validate_method(m: str) -> bool:
            return isinstance(m, str) and m in valid_methods

        method_validated = u.guard(method_upper, _validate_method, return_value=True)
        if method_validated is None:
            return r[m.Web.Request].fail(
                f"Invalid HTTP method: {method}. Must be one of: {valid_methods}",
            )
        headers_validated = headers or {}

        def create_request() -> m.Web.Request:
            """Create request model."""
            return m.Web.Request(
                url=url,
                method=method_upper,
                headers=headers_validated or {},
                body=body,
                timeout=timeout,
            )

        try:
            request = create_request()
            return r[m.Web.Request].ok(request)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as exc:
            error_msg = f"Failed to create HTTP request: {exc}"
            return r[m.Web.Request].fail(error_msg)

    @classmethod
    def create_http_response(
        cls,
        status_code: int,
        headers: Mapping[str, str] | None = None,
        body: str | Mapping[str, FlextTypes.Scalar] | None = None,
        elapsed_time: float | None = None,
    ) -> r[m.Web.Response]:
        """Create HTTP response model instance with proper validation.

        Args:
            status_code: HTTP status code
            headers: Response headers (validated, no fallback)
            body: Response body
            elapsed_time: Response processing time

        Returns:
            r[Web.Response]: Success contains response model,
                                      failure contains validation error

        """
        headers_validated = headers or {}

        def create_response() -> m.Web.Response:
            """Create response model."""
            return m.Web.Response(
                status_code=status_code,
                headers=headers_validated or {},
                body=body,
                elapsed_time=elapsed_time,
            )

        try:
            response = create_response()
            return r[m.Web.Response].ok(response)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as exc:
            return r[m.Web.Response].fail(f"Failed to create HTTP response: {exc}")

    @classmethod
    def create_web_request(
        cls,
        config: _WebRequestConfig,
    ) -> r[m.Web.AppRequest]:
        """Create web request model instance with proper validation.

        Args:
            config: Web request configuration model

        Returns:
            r[Web.AppRequest]: Success contains request model,
                                        failure contains validation error

        """
        url: str = config.url or ""
        method: str = config.method or c.Web.Method.GET
        headers = config.headers
        body = config.body
        timeout: float = config.timeout or c.Web.Http.DEFAULT_TIMEOUT_SECONDS
        query_params = config.query_params
        client_ip: str = config.client_ip or ""
        user_agent: str = config.user_agent or ""
        if not url or not url.strip():
            return r[m.Web.AppRequest].fail("URL is required")
        url_validated = url.strip()
        headers_validated: Mapping[str, str] = headers or {}
        query_params_validated: Mapping[str, FlextTypes.Scalar] = query_params or {}
        method_upper = method.upper()
        valid_methods = set(c.Web.Http.METHODS)

        def _validate_method(m: str) -> bool:
            return isinstance(m, str) and m in valid_methods

        method_validated = u.guard(method_upper, _validate_method, return_value=True)
        if method_validated is None:
            return r[m.Web.AppRequest].fail(
                f"Invalid HTTP method: {method}. Must be one of: {valid_methods}",
            )

        def create_request() -> m.Web.AppRequest:
            """Create request model."""
            return m.Web.AppRequest(
                url=url_validated,
                method=method_upper,
                headers=headers_validated,
                body=body,
                timeout=timeout or c.Web.Http.DEFAULT_TIMEOUT_SECONDS,
                query_params=query_params_validated,
                client_ip=client_ip,
                user_agent=user_agent,
            )

        try:
            request = create_request()
            return r[m.Web.AppRequest].ok(request)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as exc:
            return r[m.Web.AppRequest].fail(f"Failed to create web request: {exc}")

    @classmethod
    def create_web_response(
        cls,
        config: _WebResponseConfig,
    ) -> r[m.Web.AppResponse]:
        """Create web response model instance with proper validation.

        Args:
            config: Web response configuration model

        Returns:
            r[Web.AppResponse]: Success contains response model,
                                         failure contains validation error

        """
        status_code: int = config.status_code or 200
        request_id: str = config.request_id or ""
        headers = config.headers
        body = config.body
        elapsed_time: float = config.elapsed_time or 0.0
        content_type: str = config.content_type or c.Web.Http.CONTENT_TYPE_JSON
        content_length: int = config.content_length or 0
        processing_time_ms: float = config.processing_time_ms or 0.0
        headers_validated: Mapping[str, str] = headers or {}

        def create_response() -> m.Web.AppResponse:
            """Create response model."""
            return m.Web.AppResponse(
                status_code=status_code or 200,
                request_id=request_id,
                headers=headers_validated,
                body=body,
                elapsed_time=elapsed_time or 0.0,
                content_type=content_type,
                content_length=content_length or 0,
                processing_time_ms=processing_time_ms or 0.0,
            )

        try:
            response = create_response()
            return r[m.Web.AppResponse].ok(response)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as exc:
            return r[m.Web.AppResponse].fail(f"Failed to create web response: {exc}")

    class TypesConfig:
        """Configuration model for web types system."""

        def __init__(
            self,
            *,
            use_pydantic_models: bool = True,
            enable_runtime_validation: bool = True,
            models_available: Sequence[str] | None = None,
        ) -> None:
            """Initialize types configuration."""
            super().__init__()
            self.use_pydantic_models = use_pydantic_models
            self.enable_runtime_validation = enable_runtime_validation
            self.models_available = (
                [
                    "Web.Message",
                    "Web.Request",
                    "Web.Response",
                    "Web.Request",
                    "Web.Response",
                    "Web.Entity",
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
        models_available: Sequence[str] | None = None,
    ) -> r[FlextWebTypes.TypesConfig]:
        """Configure web types system to use Pydantic models.

        Args:
            use_pydantic_models: Enable Pydantic model usage
            enable_runtime_validation: Enable runtime validation
            models_available: List of available model names

        Returns:
            r[TypesConfig]: Configuration result

        """
        try:
            config = cls.TypesConfig(
                use_pydantic_models=use_pydantic_models,
                enable_runtime_validation=enable_runtime_validation,
                models_available=[
                    "Web.Message",
                    "Web.Request",
                    "Web.Response",
                    "Web.Request",
                    "Web.Response",
                    "Web.Entity",
                ]
                if models_available is None
                else models_available,
            )
            return r[FlextWebTypes.TypesConfig].ok(config)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            return r[FlextWebTypes.TypesConfig].fail(
                f"Failed to configure web types system: {e}",
            )

    @classmethod
    def get_web_types_system_config(cls) -> r[FlextWebTypes.TypesConfig]:
        """Get current web types system configuration.

        Returns:
            r[TypesConfig]: Current configuration

        """
        try:
            config = cls.TypesConfig()
            return r[FlextWebTypes.TypesConfig].ok(config)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            return r[FlextWebTypes.TypesConfig].fail(
                f"Failed to get web types system config: {e}",
            )

    class Project:
        """Web-specific project types.

        Adds web application-specific project types.
        Follows domain separation principle:
        Web domain owns web application-specific types.
        """

        class WebProjectConfig(m.Web.EntityConfig):
            """Web project configuration model - inherits from m.Web.EntityConfig."""

        class ApplicationConfig(m.Web.EntityConfig):
            """Application configuration model - inherits from m.Web.EntityConfig."""

        class WebServerConfig(m.Web.EntityConfig):
            """Web server configuration model - inherits from m.Web.EntityConfig."""

        class WebPipelineConfig(m.Web.EntityConfig):
            """Web pipeline configuration model - inherits from m.Web.EntityConfig."""


t = FlextWebTypes

__all__ = [
    "FlextWebTypes",
    "_ApplicationConfig",
    "_WebRequestConfig",
    "_WebResponseConfig",
    "t",
]
