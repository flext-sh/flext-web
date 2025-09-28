"""FLEXT Web Types - Domain-specific web type definitions.

This module provides web-specific type definitions extending FlextTypes.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends FlextTypes properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings
from typing import Literal, TypedDict

from flext_core import FlextResult, FlextTypes, FlextUtilities

# =============================================================================
# WEB-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for web operations
# =============================================================================


class FlextWebTypes(FlextTypes):
    """Web-specific type definitions extending FlextTypes.

    Domain-specific type system for web/HTTP operations.
    Contains ONLY complex web-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # =========================================================================
    # CORE WEB TYPES - Commonly used type aliases extending FlextTypes.Core
    # =========================================================================

    class Core(FlextTypes.Core):
        """Core Web types extending FlextTypes.Core.

        Replaces generic dict[str, object] with semantic web types.
        """

        type WebResponse = tuple[str, int] | tuple[str, int, dict[str, str]] | str
        type JsonResponse = FlextTypes.Core.JsonObject

        # Configuration and settings types
        type ConfigDict = dict[str, FlextTypes.Core.ConfigValue | dict[str, object]]
        type WebConfigDict = dict[str, object]
        type AppConfigDict = dict[str, object]
        type ServiceConfigDict = dict[str, object]
        type ServerConfigDict = dict[str, object]

        # Data processing types
        type DataDict = dict[str, object]
        type RequestDict = dict[str, object]
        type ResponseDict = dict[str, object]
        type ValidationDict = dict[str, object]
        type RoutingDict = dict[str, object]

        # Template and structured response types
        type TemplateDict = dict[str, str | dict[str, object]]
        type EndpointDict = dict[str, object]
        type MiddlewareDict = dict[str, object]
        type SecurityDict = dict[str, object]

        # Operation and context types
        type OperationDict = dict[str, object]
        type ContextDict = dict[str, object]
        type SettingsDict = dict[str, object]
        type MetricsDict = dict[str, object]

    # =========================================================================
    # WEB APPLICATION TYPES - Complex web application types
    # =========================================================================

    class Application:
        """Web application complex types."""

        type ApplicationConfiguration = dict[
            str, FlextTypes.Core.ConfigValue | dict[str, object]
        ]
        type ApplicationMetadata = dict[
            str, str | int | bool | dict[str, FlextTypes.Core.JsonValue]
        ]
        type ApplicationLifecycle = dict[str, str | bool | dict[str, object]]
        type ApplicationSecurity = dict[
            str, bool | str | list[str] | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type ApplicationMiddleware = list[dict[str, FlextTypes.Core.JsonValue]]
        type ApplicationRouting = dict[
            str, list[str] | dict[str, FlextTypes.Core.JsonValue]
        ]

    # =========================================================================
    # HTTP REQUEST/RESPONSE TYPES - Complex HTTP handling types
    # =========================================================================

    class RequestResponse:
        """HTTP request and response complex types."""

        type RequestConfiguration = dict[
            str, FlextTypes.Core.JsonValue | dict[str, object]
        ]
        type RequestHeaders = dict[str, str | list[str]]
        type RequestParameters = dict[
            str, FlextTypes.Core.JsonValue | list[FlextTypes.Core.JsonValue]
        ]
        type RequestBody = dict[str, FlextTypes.Core.JsonValue] | str | bytes
        type ResponseConfiguration = dict[
            str, FlextTypes.Core.JsonValue | dict[str, object]
        ]
        type ResponseHeaders = dict[str, str | list[str]]
        type ResponseBody = dict[str, FlextTypes.Core.JsonValue] | str | bytes

    # =========================================================================
    # WEB SERVICE TYPES - Complex web service types
    # =========================================================================

    class WebService:
        """Web service complex types."""

        type ServiceConfiguration = dict[
            str, FlextTypes.Core.ConfigValue | dict[str, object]
        ]
        type ServiceRegistration = dict[
            str, str | bool | dict[str, FlextTypes.Core.JsonValue]
        ]
        type ServiceDiscovery = dict[
            str, list[str] | dict[str, FlextTypes.Core.JsonValue]
        ]
        type ServiceHealth = dict[str, bool | int | str | dict[str, object]]
        type ServiceMetrics = dict[
            str, int | float | dict[str, FlextTypes.Core.JsonValue]
        ]
        type ServiceDeployment = dict[str, str | dict[str, FlextTypes.Core.ConfigValue]]

    # =========================================================================
    # WEB SECURITY TYPES - Complex security types
    # =========================================================================

    class Security:
        """Web security complex types."""

        type SecurityConfiguration = dict[
            str, bool | str | list[str] | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type AuthenticationConfig = dict[
            str, str | dict[str, FlextTypes.Core.JsonValue]
        ]
        type AuthorizationPolicy = dict[str, list[str] | dict[str, bool | object]]
        type CorsConfiguration = dict[str, bool | list[str] | dict[str, str]]
        type CsrfProtection = dict[
            str, bool | str | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type SecurityHeaders = dict[str, str | bool | dict[str, str]]

    # =========================================================================
    # API ENDPOINT TYPES - Complex API management types
    # =========================================================================

    class ApiEndpoint:
        """API endpoint complex types."""

        type EndpointConfiguration = dict[
            str, str | bool | list[str] | dict[str, FlextTypes.Core.JsonValue]
        ]
        type EndpointValidation = dict[str, bool | list[str] | dict[str, object]]
        type EndpointDocumentation = dict[
            str, str | dict[str, FlextTypes.Core.JsonValue]
        ]
        type RouteConfiguration = dict[str, str | list[str] | dict[str, object]]
        type ApiVersioning = dict[
            str, str | int | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type RateLimiting = dict[str, int | dict[str, FlextTypes.Core.JsonValue]]

    # =========================================================================
    # WEB PROJECT TYPES - Domain-specific project types extending FlextTypes
    # =========================================================================

    class Project(FlextTypes.Project):
        """Web-specific project types extending FlextTypes.Project.

        Adds web-specific project types while inheriting generic types from FlextTypes.
        Follows domain separation principle: Web domain owns web-specific types.
        """

        # Web-specific project types extending the generic ones
        type ProjectType = Literal[
            # Generic types inherited from FlextTypes.Project
            "library",
            "application",
            "service",
            # Web-specific types
            "webapp",
            "spa",
            "api-server",
            "web-service",
            "microservice",
            "rest-api",
            "web-portal",
            "dashboard",
            "REDACTED_LDAP_BIND_PASSWORD-panel",
        ]

        # Web-specific project configurations
        type WebProjectConfig = dict[str, FlextTypes.Core.ConfigValue | object]
        type FlaskProjectConfig = dict[str, str | int | bool | list[str]]
        type ApiProjectConfig = dict[str, bool | str | dict[str, object]]
        type SecurityProjectConfig = dict[str, FlextTypes.Core.ConfigValue | object]

    # =========================================================================
    # LEGACY TYPEDDICT CLASSES - Preserved for compatibility
    # =========================================================================

    # Application types
    class AppData(TypedDict):
        """Web application data structure."""

        id: str
        name: str
        host: str
        port: int
        status: str
        is_running: bool

    class AppCreationData(TypedDict):
        """Web application creation data structure."""

        name: str
        host: str
        port: int

    class AppUpdateData(TypedDict, total=False):
        """Web application update data structure with optional fields."""

        name: str
        host: str
        port: int
        status: str

    # API types
    class CreateAppRequest(TypedDict):
        """Create application API request structure."""

        name: str
        host: str
        port: int

    class UpdateAppRequest(TypedDict, total=False):
        """Update application API request structure with optional fields."""

        name: str
        host: str
        port: int

    class BaseResponse(TypedDict):
        """Base API response structure for all endpoints."""

        success: bool
        message: str

    class SuccessResponse(BaseResponse):
        """Successful API response with data payload."""

        data: FlextTypes.Core.Dict

    class ErrorResponse(BaseResponse):
        """Error API response with error details."""

        error: str

    class ListResponse(BaseResponse):
        """List API response for multiple items."""

        data: list[FlextTypes.Core.Dict]

    class HealthResponse(TypedDict):
        """Health check API response structure."""

        status: str
        service: str
        version: str
        applications: int
        timestamp: str
        service_id: str
        created_at: object

    # Configuration types
    class ConfigData(TypedDict):
        """Web configuration data structure."""

        host: str
        port: int
        debug: bool
        secret_key: str
        app_name: str

    class ProductionConfigData(TypedDict):
        """Production-specific configuration requirements."""

        host: str
        port: int
        secret_key: str
        debug: bool
        enable_cors: bool

    class DevelopmentConfigData(TypedDict, total=False):
        """Development-specific configuration with optional overrides."""

        host: str
        port: int
        debug: bool
        secret_key: str
        enable_cors: bool

    # Additional TypedDict classes
    class ResponseDataDict(TypedDict, total=False):
        """Generic response data dictionary structure."""

        success: bool
        message: str
        data: FlextTypes.Core.Dict | FlextTypes.Core.List | None
        error: str
        errors: FlextTypes.Core.StringList | FlextTypes.Core.Dict
        timestamp: str

    class RequestContext(TypedDict, total=False):
        """Request context data structure."""

        method: str
        path: str
        headers: FlextTypes.Core.Headers
        data: FlextTypes.Core.Dict
        user_id: str
        session_id: str
        timestamp: str

    class StatusInfo(TypedDict):
        """Status information structure."""

        code: int
        message: str
        details: str

    # Factory methods
    @classmethod
    def create_app_data(
        cls,
        app_id: str,
        name: str,
        host: str,
        port: int,
        status: str,
        *,
        is_running: bool,
    ) -> AppData:
        """Create app data structure."""
        return cls.AppData(
            id=app_id,
            name=name,
            host=host,
            port=port,
            status=status,
            is_running=is_running,
        )

    @classmethod
    def create_config_data(
        cls,
        host: str = "localhost",
        port: int = 8080,
        *,
        debug: bool = True,
        secret_key: str | None = None,
        app_name: str = "FLEXT Web",
    ) -> ConfigData:
        """Create config data structure with defaults.

        DEPRECATED: Use FlextWebConfig.get_global_instance() instead.
        This method will be removed in a future version.
        """
        warnings.warn(
            "create_config_data is deprecated. "
            "Use FlextWebConfig.get_global_instance() with Pydantic 2 Settings instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        # Use environment-aware config or fallback
        if secret_key is None:
            # Generate secure default secret key using FlextUtilities
            secret_key = f"flext_web_{FlextUtilities.Generators.generate_entity_id()}"

        return cls.ConfigData(
            host=host,
            port=port,
            debug=debug,
            secret_key=secret_key,
            app_name=app_name,
        )

    @classmethod
    def create_request_context(
        cls,
        method: str = "GET",
        path: str = "/",
        headers: FlextTypes.Core.Headers | None = None,
        data: FlextTypes.Core.Dict | None = None,
    ) -> RequestContext:
        """Create request context structure."""
        return cls.RequestContext(
            method=method,
            path=path,
            headers=headers or {},
            data=data or {},
        )

    @classmethod
    def validate_config_data(
        cls,
        data: object,
    ) -> FlextResult[ConfigData]:
        """Validate configuration data structure."""
        try:
            if not isinstance(data, dict):
                return FlextResult[FlextWebTypes.ConfigData].fail(
                    "Data must be a dictionary",
                )

            required_fields = ["host", "port", "debug", "secret_key", "app_name"]
            for field in required_fields:
                if field not in data:
                    return FlextResult[FlextWebTypes.ConfigData].fail(
                        f"Required field '{field}' is missing",
                    )

            if not isinstance(data["host"], str):
                return FlextResult[FlextWebTypes.ConfigData].fail(
                    "Field 'host' must be a string",
                )
            if not isinstance(data["port"], int):
                return FlextResult[FlextWebTypes.ConfigData].fail(
                    "Field 'port' must be an integer",
                )
            if not isinstance(data["debug"], bool):
                return FlextResult[FlextWebTypes.ConfigData].fail(
                    "Field 'debug' must be a boolean",
                )
            if not isinstance(data["secret_key"], str):
                return FlextResult[FlextWebTypes.ConfigData].fail(
                    "Field 'secret_key' must be a string",
                )
            if not isinstance(data["app_name"], str):
                return FlextResult[FlextWebTypes.ConfigData].fail(
                    "Field 'app_name' must be a string",
                )

            config_data = FlextWebTypes.ConfigData(
                host=data["host"],
                port=data["port"],
                debug=data["debug"],
                secret_key=data["secret_key"],
                app_name=data["app_name"],
            )
            return FlextResult[FlextWebTypes.ConfigData].ok(config_data)

        except Exception as e:
            return FlextResult[FlextWebTypes.ConfigData].fail(
                f"Configuration validation error: {e}",
            )

    @classmethod
    def validate_app_data(cls, data: object) -> FlextResult[AppData]:
        """Validate app data structure."""
        try:
            if not isinstance(data, dict):
                return FlextResult[FlextWebTypes.AppData].fail(
                    "Data must be a dictionary",
                )

            required_fields = ["id", "name", "host", "port", "status", "is_running"]
            for field in required_fields:
                if field not in data:
                    return FlextResult[FlextWebTypes.AppData].fail(
                        f"Required field '{field}' is missing",
                    )

            if not isinstance(data["id"], str):
                return FlextResult[FlextWebTypes.AppData].fail(
                    "Field 'id' must be a string",
                )
            if not isinstance(data["name"], str):
                return FlextResult[FlextWebTypes.AppData].fail(
                    "Field 'name' must be a string",
                )
            if not isinstance(data["host"], str):
                return FlextResult[FlextWebTypes.AppData].fail(
                    "Field 'host' must be a string",
                )
            if not isinstance(data["port"], int):
                return FlextResult[FlextWebTypes.AppData].fail(
                    "Field 'port' must be an integer",
                )
            if not isinstance(data["status"], str):
                return FlextResult[FlextWebTypes.AppData].fail(
                    "Field 'status' must be a string",
                )
            if not isinstance(data["is_running"], bool):
                return FlextResult[FlextWebTypes.AppData].fail(
                    "Field 'is_running' must be a boolean",
                )

            app_data = FlextWebTypes.AppData(
                id=data["id"],
                name=data["name"],
                host=data["host"],
                port=data["port"],
                status=data["status"],
                is_running=data["is_running"],
            )
            return FlextResult[FlextWebTypes.AppData].ok(app_data)

        except Exception as e:
            return FlextResult[FlextWebTypes.AppData].fail(f"Validation error: {e}")

    # Configuration methods
    @classmethod
    def configure_web_types_system(
        cls,
        config: FlextTypes.Core.Dict,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Configure web types system.

        Returns:
            FlextResult[FlextTypes.Core.Dict]: Configuration result.

        """
        try:
            validated_config: dict[str, object] = dict(config)
            validated_config.setdefault("enable_strict_typing", True)
            validated_config.setdefault("enable_runtime_validation", True)
            return FlextResult[FlextTypes.Core.Dict].ok(validated_config)
        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Failed to configure web types system: {e}",
            )

    @classmethod
    def get_web_types_system_config(
        cls,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Get current web types system configuration."""
        try:
            config: FlextTypes.Core.Dict = {
                "enable_strict_typing": "True",
                "enable_runtime_validation": "True",
                "total_type_definitions": 50,
                "factory_methods": 2,
            }
            return FlextResult[FlextTypes.Core.Dict].ok(config)
        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Failed to get web types system config: {e}",
            )


# =============================================================================
# PUBLIC API EXPORTS - Web TypeVars and types
# =============================================================================

__all__ = [
    "FlextWebTypes",
]
