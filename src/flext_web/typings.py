"""FLEXT Web Types - Domain-specific web type definitions extending flext-core.

This module provides web-specific type definitions extending FlextCore.Types.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends FlextCore.Types properly
- Single unified class per module pattern

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections import UserDict
from dataclasses import dataclass

from flask import Response
from flext_core import FlextCore

from flext_web.constants import FlextWebConstants


class FlextWebTypes:
    """Web-specific type definitions extending FlextCore.Types.

    Domain-specific type system for web/HTTP operations.
    Contains ONLY complex web-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    Follows single unified class per module pattern.
    """

    # =========================================================================
    # CORE WEB TYPES - Commonly used type aliases extending FlextCore.Types
    # =========================================================================

    class Core:
        """Core Web types extending FlextCore.Types.

        Replaces generic FlextCore.Types.Dict with semantic web types.
        """

        type WebResponse = (
            tuple[str, int]
            | tuple[str, int, FlextCore.Types.StringDict]
            | tuple[Response, int]
            | str
        )
        type JsonResponse = FlextCore.Types.JsonValue

        # Response type definitions (class attributes for runtime access)
        SuccessResponse = dict
        BaseResponse = dict
        ErrorResponse = dict
        ResponseDataDict = dict
        ConfigData = dict
        ProductionConfigData = dict
        DevelopmentConfigData = dict
        StatusInfo = dict
        AppData = dict
        RequestContext = dict

        # Configuration and settings types (extends flext-core ConfigDict)
        type ExtendedConfigDict = dict[
            str, FlextCore.Types.ConfigValue | FlextCore.Types.Dict
        ]
        type WebConfigDict = FlextCore.Types.Dict
        type AppConfigDict = FlextCore.Types.Dict
        type ServiceConfigDict = FlextCore.Types.Dict
        type ServerConfigDict = FlextCore.Types.Dict

        # Data processing types
        type DataDict = FlextCore.Types.Dict
        type RequestDict = FlextCore.Types.Dict
        type ResponseDict = FlextCore.Types.Dict
        type ValidationDict = FlextCore.Types.Dict
        type RoutingDict = FlextCore.Types.Dict

        # Template and structured response types
        type TemplateDict = dict[str, str | FlextCore.Types.Dict]
        type EndpointDict = FlextCore.Types.Dict
        type MiddlewareDict = FlextCore.Types.Dict
        type SecurityDict = FlextCore.Types.Dict

        # Operation and context types
        type OperationDict = FlextCore.Types.Dict
        type ContextDict = FlextCore.Types.Dict
        type SettingsDict = FlextCore.Types.Dict
        type MetricsDict = FlextCore.Types.Dict

    # =========================================================================
    # WEB APPLICATION TYPES - Complex web application types
    # =========================================================================

    class Application:
        """Web application complex types."""

        type ApplicationConfiguration = dict[
            str, FlextCore.Types.ConfigValue | FlextCore.Types.Dict
        ]
        type ApplicationMetadata = dict[
            str, str | int | bool | dict[str, FlextCore.Types.JsonValue]
        ]
        type ApplicationLifecycle = dict[str, str | bool | FlextCore.Types.Dict]
        type ApplicationSecurity = dict[
            str,
            bool
            | str
            | FlextCore.Types.StringList
            | dict[str, FlextCore.Types.ConfigValue],
        ]
        type ApplicationMiddleware = list[dict[str, FlextCore.Types.JsonValue]]
        type ApplicationRouting = dict[
            str, FlextCore.Types.StringList | dict[str, FlextCore.Types.JsonValue]
        ]

    # =========================================================================
    # HTTP REQUEST/RESPONSE TYPES - Complex HTTP handling types
    # =========================================================================

    class RequestResponse:
        """HTTP request and response complex types."""

        type RequestConfiguration = dict[
            str, FlextCore.Types.JsonValue | FlextCore.Types.Dict
        ]
        type RequestHeaders = dict[str, str | FlextCore.Types.StringList]
        type RequestParameters = dict[
            str, FlextCore.Types.JsonValue | list[FlextCore.Types.JsonValue]
        ]
        type RequestBody = dict[str, FlextCore.Types.JsonValue] | str | bytes
        type ResponseConfiguration = dict[
            str, FlextCore.Types.JsonValue | FlextCore.Types.Dict
        ]
        type ResponseHeaders = dict[str, str | FlextCore.Types.StringList]
        type ResponseBody = dict[str, FlextCore.Types.JsonValue] | str | bytes

    # =========================================================================
    # WEB SERVICE TYPES - Complex web service types
    # =========================================================================

    class WebService:
        """Web service complex types."""

        type ServiceConfiguration = dict[
            str, FlextCore.Types.ConfigValue | FlextCore.Types.Dict
        ]
        type ServiceRegistration = dict[
            str, str | bool | dict[str, FlextCore.Types.JsonValue]
        ]
        type ServiceDiscovery = dict[
            str, FlextCore.Types.StringList | dict[str, FlextCore.Types.JsonValue]
        ]
        type ServiceHealth = dict[str, bool | int | str | FlextCore.Types.Dict]
        type ServiceMetrics = dict[
            str, int | float | dict[str, FlextCore.Types.JsonValue]
        ]
        type ServiceDeployment = dict[str, str | dict[str, FlextCore.Types.ConfigValue]]

    # =========================================================================
    # WEB SECURITY TYPES - Complex security types
    # =========================================================================

    class Security:
        """Web security complex types."""

        type SecurityConfiguration = dict[
            str,
            bool
            | str
            | FlextCore.Types.StringList
            | dict[str, FlextCore.Types.ConfigValue],
        ]
        type AuthenticationConfig = dict[
            str, str | dict[str, FlextCore.Types.JsonValue]
        ]
        type AuthorizationPolicy = dict[
            str, FlextCore.Types.StringList | dict[str, bool | object]
        ]
        type CorsConfiguration = dict[
            str, bool | FlextCore.Types.StringList | FlextCore.Types.StringDict
        ]
        type CsrfProtection = dict[
            str, bool | str | dict[str, FlextCore.Types.ConfigValue]
        ]
        type SecurityHeaders = dict[str, str | bool | FlextCore.Types.StringDict]

    # =========================================================================
    # API ENDPOINT TYPES - Complex API management types
    # =========================================================================

    class ApiEndpoint:
        """API endpoint complex types."""

        type EndpointConfiguration = dict[
            str,
            str
            | bool
            | FlextCore.Types.StringList
            | dict[str, FlextCore.Types.JsonValue],
        ]
        type EndpointValidation = dict[
            str, bool | FlextCore.Types.StringList | FlextCore.Types.Dict
        ]
        type EndpointDocumentation = dict[
            str, str | dict[str, FlextCore.Types.JsonValue]
        ]
        type RouteConfiguration = dict[
            str, str | FlextCore.Types.StringList | FlextCore.Types.Dict
        ]
        type ApiVersioning = dict[
            str, str | int | dict[str, FlextCore.Types.ConfigValue]
        ]
        type RateLimiting = dict[str, int | dict[str, FlextCore.Types.JsonValue]]

    # =========================================================================
    # WEB DATA STRUCTURES - Dataclasses for web operations
    # =========================================================================

    @dataclass
    class AppData(UserDict[str, object]):
        """Application data structure for API responses."""

        id: str
        name: str
        host: str
        port: int
        status: str
        is_running: bool

        def __post_init__(self) -> None:
            """Initialize dict[str, object] with dataclass fields."""
            super().__init__(
                id=self.id,
                name=self.name,
                host=self.host,
                port=self.port,
                status=self.status,
                is_running=self.is_running,
            )

        created_at: str | None = None
        updated_at: str | None = None
        description: str | None = None
        environment: str | None = None
        debug_mode: bool | None = None

    @dataclass
    class HealthResponse:
        """Health check response structure."""

        status: str
        service: str
        version: str
        applications: int
        timestamp: str
        service_id: str
        created_at: str | None = None

    @dataclass
    class RequestContext:
        """Request context for middleware processing."""

        method: str
        path: str
        headers: FlextCore.Types.StringDict
        query_params: FlextCore.Types.StringDict
        body: str | bytes | None = None
        client_ip: str | None = None

    # =========================================================================
    # WEB PROJECT TYPES - Domain-specific project types extending FlextCore.Types
    # =========================================================================

    class Project(FlextCore.Types.Project):
        """Web-specific project types extending FlextCore.Types.Project.

        Adds web-specific project types while inheriting generic types from FlextCore.Types.
        Follows domain separation principle: Web domain owns web-specific types.
        """

        # Web-specific project types extending the generic ones
        type WebProjectType = FlextWebConstants.WebEnvironment.WebAppType

        # Web-specific project configurations
        type WebProjectConfig = dict[str, FlextCore.Types.ConfigValue | object]
        type FlaskProjectConfig = dict[
            str, str | int | bool | FlextCore.Types.StringList
        ]
        type ApiProjectConfig = dict[str, bool | str | FlextCore.Types.Dict]
        type SecurityProjectConfig = dict[str, FlextCore.Types.ConfigValue | object]

    # =========================================================================
    # CONFIGURATION METHODS - Type system configuration and validation
    # =========================================================================

    @classmethod
    def configure_web_types_system(
        cls,
        config: FlextCore.Types.Dict,
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Configure web types system.

        Args:
            config: Configuration dictionary for web types system

        Returns:
            FlextCore.Result[FlextCore.Types.Dict]: Configuration result

        """
        try:
            validated_config: FlextCore.Types.Dict = dict[str, object](config)
            validated_config.setdefault("enable_strict_typing", True)
            validated_config.setdefault("enable_runtime_validation", True)
            return FlextCore.Result[FlextCore.Types.Dict].ok(validated_config)
        except Exception as e:
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                f"Failed to configure web types system: {e}",
            )

    @classmethod
    def get_web_types_system_config(
        cls,
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Get current web types system configuration.

        Returns:
            FlextCore.Result[FlextCore.Types.Dict]: Current configuration

        """
        try:
            config: FlextCore.Types.Dict = {
                "enable_strict_typing": True,
                "enable_runtime_validation": True,
                "total_type_definitions": 50,
                "factory_methods": 2,
            }
            return FlextCore.Result[FlextCore.Types.Dict].ok(config)
        except Exception as e:
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                f"Failed to get web types system config: {e}",
            )

    @classmethod
    def create_app_data(
        cls,
        **kwargs: object,
    ) -> FlextCore.Types.Dict:
        """Create app data dictionary.

        Args:
            **kwargs: Application data fields

        Returns:
            FlextCore.Types.Dict: Application data dictionary

        """
        return dict[str, object](kwargs)

    @classmethod
    def create_config_data(cls) -> FlextCore.Types.Dict:
        """Create config data dictionary.

        Returns:
            FlextCore.Types.Dict: Empty configuration dictionary

        """
        return {}

    @classmethod
    def create_request_context(
        cls,
        method: str = "GET",
        path: str = "/",
        headers: FlextCore.Types.StringDict | None = None,
        data: FlextCore.Types.Dict | None = None,
    ) -> FlextCore.Types.Dict:
        """Create request context dictionary.

        Args:
            method: HTTP method
            path: Request path
            headers: Request headers
            data: Request data

        Returns:
            FlextCore.Types.Dict: Request context dictionary

        """
        return {
            "method": method,
            "path": path,
            "headers": headers or {},
            "data": data or {},
        }

    @classmethod
    def validate_app_data(
        cls, data: FlextCore.Types.Dict
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Validate app data.

        Args:
            data: Application data to validate

        Returns:
            FlextCore.Result[FlextCore.Types.Dict]: Validation result

        """
        if not isinstance(data, dict):
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                "App data must be a dictionary"
            )
        return FlextCore.Result[FlextCore.Types.Dict].ok(data)

    @classmethod
    def validate_config_data(
        cls, data: FlextCore.Types.Dict | str
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Validate config data.

        Args:
            data: Configuration data to validate

        Returns:
            FlextCore.Result[FlextCore.Types.Dict]: Validation result

        """
        if isinstance(data, str):
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                "Config data must be a dictionary"
            )
        return FlextCore.Result[FlextCore.Types.Dict].ok(data)


__all__ = [
    "FlextWebTypes",
]
