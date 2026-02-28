"""FLEXT Web Types - Domain-specific web type definitions using Pydantic models.

This module provides web-specific type definitions using m.
Uses Pydantic 2 models instead of dict types for better type safety and validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Literal

from flext_core import (
    FlextResult,
    FlextTypes,
    u,
)
from pydantic import BaseModel, ConfigDict, Field

from flext_web import c, m

HttpMethod = c.Web.Method


class _WebRequestConfig(BaseModel):
    """Web request configuration model."""

    model_config = ConfigDict(frozen=False, extra="forbid")

    url: str = Field(default="")
    method: str = Field(default="GET")
    headers: dict[str, str] | None = Field(default=None)
    body: str | dict[str, FlextTypes.ConfigMapValue] | None = Field(default=None)
    timeout: float = Field(default=30.0)
    query_params: dict[str, FlextTypes.ConfigMapValue] | None = Field(default=None)
    client_ip: str = Field(default="")
    user_agent: str = Field(default="")


class _WebResponseConfig(BaseModel):
    """Web response configuration model."""

    model_config = ConfigDict(frozen=False, extra="forbid")

    status_code: int = Field(default=200)
    request_id: str = Field(default="")
    headers: dict[str, str] | None = Field(default=None)
    body: str | dict[str, FlextTypes.ConfigMapValue] | None = Field(default=None)
    elapsed_time: float = Field(default=0.0)
    content_type: str = Field(default="application/json")
    content_length: int = Field(default=0)
    processing_time_ms: float = Field(default=0.0)


class _ApplicationConfig(BaseModel):
    """Application configuration model."""

    model_config = ConfigDict(frozen=False, extra="forbid")

    name: str = Field(default="")
    host: str = Field(default="localhost")
    port: int = Field(default=8080)
    status: str = Field(default="stopped")
    environment: str = Field(default="development")
    debug_mode: bool = Field(default=False)
    version: int = Field(default=1)


class FlextWebTypes(FlextTypes):
    """Web-specific type definitions using m.

    Uses Pydantic 2 models from m for type safety.
    Provides type aliases and factory methods for web operations.
    Follows single unified class per module pattern.
    """

    # =========================================================================
    # PYDANTIC MODEL CLASSES - Use inheritance instead of aliases
    # =========================================================================

    # HTTP protocol models - proper inheritance from m
    class HttpMessage(m.Web.Message):
        """HTTP message model - inherits from m.Web.Message."""

    class HttpRequest(m.Web.Request):
        """HTTP request model - inherits from m.Web.Request."""

    class HttpResponse(m.Web.Response):
        """HTTP response model - inherits from m.Web.Response."""

    # Web-specific models - reference existing models
    WebRequest = m.Web.AppRequest
    """Web request model - references m.Web.AppRequest."""

    WebResponse = m.Web.AppResponse
    """Web response model - references m.Web.AppResponse."""

    # Application models - proper inheritance from m
    class ApplicationEntity(m.Web.Entity):
        """Application entity model - inherits from m.Web.Entity."""

    # ApplicationStatus - StrEnum cannot be inherited (Python limitation)
    ApplicationStatus = c.Web.Status

    # Application data types - proper inheritance from m
    class AppData(m.Web.ApplicationResponse):
        """Application data model - inherits from m.Web.ApplicationResponse."""

    # Health response type - proper inheritance from m
    HealthResponse = m.Web.HealthResponse
    """Health response model - references m.Web.HealthResponse."""

    # =========================================================================
    # TYPE ALIASES - Using Pydantic models and Protocols
    # =========================================================================

    # Core data types - use Protocols and specific types
    class Web:
        """Web core type aliases for request/response data.

        Provides organized access to all Web types for other FLEXT projects.
        Usage: Other projects can reference `t.Web.Http.*`, `t.Web.Project.*`, etc.
        This enables consistent namespace patterns for cross-project type access.
        """

        ConfigValue = str | int | bool | list[str]
        RequestDict = dict[
            str,
            str | int | bool | list[str] | dict[str, str | int | bool],
        ]
        ResponseDict = dict[
            str,
            str | int | bool | list[str] | dict[str, str | int | bool],
        ]

        # ============================================================================
        # LITERAL TYPE DEFINITIONS
        # ============================================================================
        # These Literal types provide compile-time safety for string literals
        # All Literal[] definitions belong in typings.py under the t.* namespace

        # HTTP method literal - references Http.Method StrEnum members
        HttpMethodLiteral = Literal[
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "PATCH",
            "HEAD",
            "OPTIONS",
        ]

        # Environment name literal - references WebEnvironment.Name StrEnum members
        EnvironmentNameLiteral = Literal[
            "development",
            "staging",
            "production",
            "testing",
        ]

        # Application status literal - references WebEnvironment.Status StrEnum members
        ApplicationStatusLiteral = Literal[
            "stopped",
            "starting",
            "running",
            "stopping",
            "error",
            "maintenance",
            "deploying",
        ]

        # Application type literal - references WebEnvironment.ApplicationType StrEnum members
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

        # Response status literal - uses string literals matching WebResponse constants
        ResponseStatusLiteral = Literal[
            "success",
            "error",
            "operational",
            "healthy",
        ]

        # Protocol literal - uses string literals matching WebDefaults constants
        ProtocolLiteral = Literal[
            "http",
            "https",
        ]

        # Content type literal - uses string literals matching Http constants
        ContentTypeLiteral = Literal[
            "application/json",
            "text/plain",
            "text/html",
        ]

        # Session cookie SameSite literal - standard HTTP cookie attribute values
        SameSiteLiteral = Literal["Lax", "Strict", "None"]

    class WebCore:
        """Compatibility namespace for request/response dict aliases."""

        RequestDict = dict[
            str,
            str | int | bool | list[str] | dict[str, str | int | bool],
        ]
        ResponseDict = dict[
            str,
            str | int | bool | list[str] | dict[str, str | int | bool],
        ]

    class Types:
        """Type system aliases for flext-web."""

        ConfigMapValue = FlextTypes.ConfigMapValue
        """Config map value type - references FlextTypes.ConfigMapValue."""

    # Core response types - proper inheritance from m
    SuccessResponse = m.Web.ServiceResponse
    """Success response model - references m.Web.ServiceResponse."""

    BaseResponse = m.Web.ServiceResponse
    """Base response model - references m.Web.ServiceResponse."""

    ErrorResponse = m.Web.ServiceResponse
    """Error response model - references m.Web.ServiceResponse."""

    # ResponseDict wrapper for FlextService - use PEP 695 type keyword
    class Data:
        """Data type definitions for FlextService compatibility."""

        type WebResponseDict = dict[
            str,
            str | int | bool | list[str] | dict[str, str | int | bool],
        ]

    # Configuration types - proper inheritance from m
    class WebConfigDict(m.Web.EntityConfig):
        """Web configuration dictionary model - inherits from m.Web.EntityConfig."""

    class AppConfigDict(m.Web.EntityConfig):
        """Application configuration dictionary model - inherits from m.Web.EntityConfig."""

    # =========================================================================
    # FACTORY METHODS - Create instances of Pydantic models
    # =========================================================================

    @classmethod
    def create_http_request(
        cls,
        url: str,
        method: str = c.Web.Method.GET,
        headers: dict[str, str] | None = None,
        body: str | dict[str, FlextTypes.ConfigMapValue] | None = None,
        timeout: float = c.Web.Http.DEFAULT_TIMEOUT_SECONDS,
    ) -> FlextResult[m.Web.Request]:
        """Create HTTP request model instance with proper validation.

        Args:
            url: Request URL
            method: HTTP method (must be valid from constants)
            headers: Request headers (validated, no fallback)
            body: Request body
            timeout: Request timeout in seconds

        Returns:
            FlextResult[Web.Request]: Success contains request model,
                                     failure contains validation error

        """
        # Use # Direct validation instead for unified method validation (DSL pattern)
        method_upper = method.upper()
        valid_methods = set(c.Web.Http.METHODS)

        def _validate_method(m: FlextTypes.GeneralValueType) -> bool:
            return isinstance(m, str) and m in valid_methods

        method_validated = u.guard(
            method_upper,
            _validate_method,
            return_value=True,
        )
        if method_validated is None:
            return FlextResult[m.Web.Request].fail(
                f"Invalid HTTP method: {method}. Must be one of: {valid_methods}",
            )

        # Use # Direct validation instead for unified headers validation (DSL pattern)
        # Validate headers - must be dict or None
        headers_validated = headers or {}

        # Use u.try_() for unified error handling (DSL pattern)
        def create_request() -> m.Web.Request:
            """Create request model."""
            return m.Web.Request(
                url=url,
                method=method_upper,
                headers=headers_validated or {},
                body=body,
                timeout=timeout,
            )

        # Use u.try_() with custom exception handling for better error messages
        try:
            request = create_request()
            return FlextResult[m.Web.Request].ok(request)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as exc:
            # Use u.err() pattern for unified error extraction (DSL pattern)
            error_msg = f"Failed to create HTTP request: {exc}"
            return FlextResult[m.Web.Request].fail(error_msg)

    @classmethod
    def create_http_response(
        cls,
        status_code: int,
        headers: dict[str, str] | None = None,
        body: str | dict[str, FlextTypes.ConfigMapValue] | None = None,
        elapsed_time: float | None = None,
    ) -> FlextResult[m.Web.Response]:
        """Create HTTP response model instance with proper validation.

        Args:
            status_code: HTTP status code
            headers: Response headers (validated, no fallback)
            body: Response body
            elapsed_time: Response processing time

        Returns:
            FlextResult[Web.Response]: Success contains response model,
                                      failure contains validation error

        """
        # Use # Direct validation instead for unified headers validation (DSL pattern)
        # Validate headers - must be dict or None
        headers_validated = headers or {}

        # Use u.try_() for unified error handling (DSL pattern)
        def create_response() -> m.Web.Response:
            """Create response model."""
            return m.Web.Response(
                status_code=status_code,
                headers=headers_validated or {},
                body=body,
                elapsed_time=elapsed_time,
            )

        # Use u.try_() with custom exception handling for better error messages
        try:
            response = create_response()
            return FlextResult[m.Web.Response].ok(response)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as exc:
            # Use u.err() pattern for unified error extraction (DSL pattern)
            return FlextResult[m.Web.Response].fail(
                f"Failed to create HTTP response: {exc}",
            )

    @classmethod
    def create_web_request(
        cls,
        config: _WebRequestConfig,
    ) -> FlextResult[m.Web.AppRequest]:
        """Create web request model instance with proper validation.

        Args:
            config: Web request configuration model

        Returns:
            FlextResult[Web.AppRequest]: Success contains request model,
                                        failure contains validation error

        """
        # Direct model access with defaults
        url: str = config.url or ""
        method: str = config.method or c.Web.Method.GET
        headers = config.headers
        body = config.body
        timeout: float = config.timeout or c.Web.Http.DEFAULT_TIMEOUT_SECONDS
        query_params = config.query_params
        client_ip: str = config.client_ip or ""
        user_agent: str = config.user_agent or ""

        # Validate URL - must be non-empty string
        if not url or not url.strip():
            return FlextResult[m.Web.AppRequest].fail("URL is required")
        url_validated = url.strip()

        # Use # Direct validation instead for headers and query_params validation (DSL pattern)
        # Validate headers - must be dict or None
        headers_validated: dict[str, str] = headers or {}
        # Validate query_params - must be dict or None
        query_params_validated: dict[str, FlextTypes.ConfigMapValue] = query_params or {}

        # Use # Direct validation instead for method validation (DSL pattern)
        method_upper = method.upper()
        valid_methods = set(c.Web.Http.METHODS)

        def _validate_method(m: FlextTypes.GeneralValueType) -> bool:
            return isinstance(m, str) and m in valid_methods

        method_validated = u.guard(
            method_upper,
            _validate_method,
            return_value=True,
        )
        if method_validated is None:
            return FlextResult[m.Web.AppRequest].fail(
                f"Invalid HTTP method: {method}. Must be one of: {valid_methods}",
            )

        # Use u.try_() for unified error handling (DSL pattern)
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

        # Use u.try_() with custom exception handling for better error messages
        try:
            request = create_request()
            return FlextResult[m.Web.AppRequest].ok(request)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as exc:
            # Use u.err() pattern for unified error extraction (DSL pattern)
            return FlextResult[m.Web.AppRequest].fail(
                f"Failed to create web request: {exc}",
            )

    @classmethod
    def create_web_response(
        cls,
        config: _WebResponseConfig,
    ) -> FlextResult[m.Web.AppResponse]:
        """Create web response model instance with proper validation.

        Args:
            config: Web response configuration model

        Returns:
            FlextResult[Web.AppResponse]: Success contains response model,
                                         failure contains validation error

        """
        # Direct model access with defaults
        status_code: int = config.status_code or 200
        request_id: str = config.request_id or ""
        headers = config.headers
        body = config.body
        elapsed_time: float = config.elapsed_time or 0.0
        content_type: str = config.content_type or c.Web.Http.CONTENT_TYPE_JSON
        content_length: int = config.content_length or 0
        processing_time_ms: float = config.processing_time_ms or 0.0

        # Use # Direct validation instead for unified headers validation (DSL pattern)
        # Validate headers - must be dict or None
        headers_validated: dict[str, str] = headers or {}

        # Use u.try_() for unified error handling (DSL pattern)
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

        # Use u.try_() with custom exception handling for better error messages
        try:
            response = create_response()
            return FlextResult[m.Web.AppResponse].ok(response)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as exc:
            # Use u.err() pattern for unified error extraction (DSL pattern)
            return FlextResult[m.Web.AppResponse].fail(
                f"Failed to create web response: {exc}",
            )

    @classmethod
    def create_application(
        cls,
        config: _ApplicationConfig,
    ) -> FlextResult[m.Web.Entity]:
        """Create application model instance.

        Args:
            config: Application configuration model

        Returns:
            FlextResult[Web.Entity]: Success contains application entity,
                                            failure contains error message

        """
        # Direct model access with defaults
        name: str = config.name or ""
        host: str = config.host or "localhost"
        port: int = config.port or 8080
        status: str = config.status or c.Web.Status.STOPPED.value
        environment: str = config.environment or c.Web.Name.DEVELOPMENT.value
        debug_mode: bool = config.debug_mode
        version: int = config.version

        # Use u.try_() for unified error handling (DSL pattern)
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

        # Use u.try_() with custom exception handling for better error messages
        try:
            entity = create_entity()
            return FlextResult[m.Web.Entity].ok(entity)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as exc:
            # Use u.err() pattern for unified error extraction (DSL pattern)
            return FlextResult[m.Web.Entity].fail(
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
                        "Web.Message",
                        "Web.Request",
                        "Web.Response",
                        "Web.Request",
                        "Web.Response",
                        "Web.Entity",
                    ]
                    if models_available is None
                    else models_available
                ),
            )
            return FlextResult[FlextWebTypes.TypesConfig].ok(config)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
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
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            return FlextResult[FlextWebTypes.TypesConfig].fail(
                f"Failed to get web types system config: {e}",
            )

    # =========================================================================
    # WEB PROJECT TYPES - Domain-specific project types extending t
    # =========================================================================

    class Project:
        """Web-specific project types.

        Adds web application-specific project types.
        Follows domain separation principle:
        Web domain owns web application-specific types.
        """

        # Web-specific project configurations - proper inheritance from m
        class WebProjectConfig(m.Web.EntityConfig):
            """Web project configuration model - inherits from m.Web.EntityConfig."""

        class ApplicationConfig(m.Web.EntityConfig):
            """Application configuration model - inherits from m.Web.EntityConfig."""

        class WebServerConfig(m.Web.EntityConfig):
            """Web server configuration model - inherits from m.Web.EntityConfig."""

        class WebPipelineConfig(m.Web.EntityConfig):
            """Web pipeline configuration model - inherits from m.Web.EntityConfig."""


# Alias for simplified usage
t = FlextWebTypes

# Namespace composition via class inheritance
# Web namespace provides access to nested classes through inheritance
# Access patterns:
# - t.Web.* for Web-specific types
# - t.Project.* for project types
# - t.Core.* for core types (inherited from parent)


__all__ = [
    "FlextWebTypes",
    "t",
]
