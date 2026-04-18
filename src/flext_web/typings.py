"""FLEXT Web Types - Domain-specific web type definitions using Pydantic models.

This module provides web-specific type definitions using m.
Uses Pydantic 2 models instead of dict types for better type safety and validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated

from flext_core import p, r, t
from flext_web import c, m, u


class FlextWebTypes(t):
    """Web-specific type definitions using m.

    Uses Pydantic 2 models from m for type safety.
    Provides type aliases and factory methods for web operations.
    Follows single unified class per module pattern.
    """

    class Web:
        """Web core type aliases for request/response data.

        Provides organized access to all Web types for other FLEXT projects.
        Usage: Other projects can reference `t.Web.Http.*`, `t.Web.Project.*`, etc.
        This enables consistent namespace patterns for cross-project type access.
        """

        ConfigValue = t.Scalar | t.StrSequence

        class ApplicationConfig(m.Web.EntityConfig):
            """Application configuration with web-specific defaults."""

            name: Annotated[
                str,
                u.Field(description="App name"),
            ] = c.Web.WebDefaults.APP_NAME
            status: Annotated[
                str,
                u.Field(description="App status"),
            ] = c.Web.Status.STOPPED.value
            environment: Annotated[
                str,
                u.Field(description="Environment"),
            ] = c.Web.Name.DEVELOPMENT.value
            debug_mode: Annotated[
                bool,
                u.Field(description="Debug"),
            ] = c.Web.WebDefaults.DEBUG_MODE
            version: Annotated[
                int,
                u.Field(description="Version"),
            ] = c.Web.WebDefaults.VERSION_INT

        class RequestConfig(m.Web.AppRequest):
            """Web request configuration extending AppRequest."""

        class ResponseConfig(m.Web.AppResponse):
            """Web response configuration extending AppResponse."""

        type RequestDict = dict[
            str,
            t.Scalar | t.StrSequence | Mapping[str, t.Scalar],
        ]
        type ResponseDict = dict[
            str,
            t.Scalar | t.StrSequence | Mapping[str, t.Scalar],
        ]

    class Types:
        """Type system aliases for flext-web Removed redundant aliases."""

    class WebConfigDict(m.Web.EntityConfig):
        """Web configuration dictionary model - inherits from m.Web.EntityConfig."""

    class AppConfigDict(m.Web.EntityConfig):
        """Application configuration dictionary model - inherits from m.Web.EntityConfig."""

    @classmethod
    def create_application(
        cls,
        settings: FlextWebTypes.Web.ApplicationConfig,
    ) -> p.Result[m.Web.Entity]:
        """Create application model instance.

        Args:
            settings: Application configuration model

        Returns:
            r[Web.Entity]: Success contains application entity,
                                            failure contains error message

        """
        name: str = settings.name or ""
        host: str = settings.host or "localhost"
        port: int = settings.port or 8080
        status: str = settings.status or c.Web.Status.STOPPED.value
        environment: str = settings.environment or c.Web.Name.DEVELOPMENT.value
        debug_mode: bool = settings.debug_mode
        version: int = settings.version

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
        headers: t.StrMapping | None = None,
        body: str | Mapping[str, t.Scalar] | None = None,
        timeout: float = c.Web.Http.DEFAULT_TIMEOUT_SECONDS,
    ) -> p.Result[m.Web.Request]:
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
        method_validated = u.guard(method_upper, str, return_value=True)
        if (
            not isinstance(method_validated, str)
            or method_validated not in valid_methods
        ):
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
        headers: t.StrMapping | None = None,
        body: str | Mapping[str, t.Scalar] | None = None,
        elapsed_time: float | None = None,
    ) -> p.Result[m.Web.Response]:
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
        settings: FlextWebTypes.Web.RequestConfig,
    ) -> p.Result[m.Web.AppRequest]:
        """Create web request model instance with proper validation.

        Args:
            settings: Web request configuration model

        Returns:
            r[Web.AppRequest]: Success contains request model,
                                        failure contains validation error

        """
        url: str = settings.url or ""
        method: str = settings.method or c.Web.Method.GET
        headers = settings.headers
        body = settings.body
        timeout: float = settings.timeout or c.Web.Http.DEFAULT_TIMEOUT_SECONDS
        query_params = settings.query_params
        client_ip: str = settings.client_ip or ""
        user_agent: str = settings.user_agent or ""
        if not url or not url.strip():
            return r[m.Web.AppRequest].fail("URL is required")
        url_validated = url.strip()
        headers_validated: t.StrMapping = headers or {}
        query_params_validated: Mapping[str, t.Scalar] = query_params or {}
        method_upper = method.upper()
        valid_methods = set(c.Web.Http.METHODS)
        method_validated = u.guard(method_upper, str, return_value=True)
        if (
            not isinstance(method_validated, str)
            or method_validated not in valid_methods
        ):
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
        settings: FlextWebTypes.Web.ResponseConfig,
    ) -> p.Result[m.Web.AppResponse]:
        """Create web response model instance with proper validation.

        Args:
            settings: Web response configuration model

        Returns:
            r[Web.AppResponse]: Success contains response model,
                                         failure contains validation error

        """
        status_code: int = settings.status_code or 200
        request_id: str = settings.request_id or ""
        headers = settings.headers
        body = settings.body
        elapsed_time: float = settings.elapsed_time or 0.0
        content_type: str = settings.content_type or c.Web.Http.CONTENT_TYPE_JSON
        content_length: int = settings.content_length or 0
        processing_time_ms: float = settings.processing_time_ms or 0.0
        headers_validated: t.StrMapping = headers or {}

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
            models_available: t.StrSequence | None = None,
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
        models_available: t.StrSequence | None = None,
    ) -> p.Result[FlextWebTypes.TypesConfig]:
        """Configure web types system to use Pydantic models.

        Args:
            use_pydantic_models: Enable Pydantic model usage
            enable_runtime_validation: Enable runtime validation
            models_available: List of available model names

        Returns:
            r[TypesConfig]: Configuration result

        """
        try:
            settings = cls.TypesConfig(
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
            return r[FlextWebTypes.TypesConfig].ok(settings)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as exc:
            return r[FlextWebTypes.TypesConfig].fail(
                f"Failed to configure web types system: {exc}",
            )

    @classmethod
    def web_types_system_config(cls) -> p.Result[FlextWebTypes.TypesConfig]:
        """Get current web types system configuration.

        Returns:
            r[TypesConfig]: Current configuration

        """
        try:
            settings = cls.TypesConfig()
            return r[FlextWebTypes.TypesConfig].ok(settings)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as exc:
            return r[FlextWebTypes.TypesConfig].fail(
                f"Failed to get web types system settings: {exc}",
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

__all__: list[str] = [
    "FlextWebTypes",
    "t",
]
