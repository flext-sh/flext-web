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

from collections import UserDict
from dataclasses import dataclass
from typing import Literal

from flext_core import FlextResult, FlextTypes

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
    # CORE WEB TYPES - Commonly used type aliases extending FlextTypes
    # =========================================================================

    class Core(FlextTypes):
        """Core Web types extending FlextTypes.

        Replaces generic FlextTypes.Dict with semantic web types.
        """

        type WebResponse = (
            tuple[object, int]
            | tuple[str, int]
            | tuple[str, int, FlextTypes.StringDict]
            | str
        )
        type JsonResponse = FlextTypes.JsonValue

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
        type ExtendedConfigDict = dict[str, FlextTypes.ConfigValue | FlextTypes.Dict]
        type WebConfigDict = FlextTypes.Dict
        type AppConfigDict = FlextTypes.Dict
        type ServiceConfigDict = FlextTypes.Dict
        type ServerConfigDict = FlextTypes.Dict

        # Data processing types
        type DataDict = FlextTypes.Dict
        type RequestDict = FlextTypes.Dict
        type ResponseDict = FlextTypes.Dict
        type ValidationDict = FlextTypes.Dict
        type RoutingDict = FlextTypes.Dict

        # Template and structured response types
        type TemplateDict = dict[str, str | FlextTypes.Dict]
        type EndpointDict = FlextTypes.Dict
        type MiddlewareDict = FlextTypes.Dict
        type SecurityDict = FlextTypes.Dict

        # Operation and context types
        type OperationDict = FlextTypes.Dict
        type ContextDict = FlextTypes.Dict
        type SettingsDict = FlextTypes.Dict
        type MetricsDict = FlextTypes.Dict

    # =========================================================================
    # WEB APPLICATION TYPES - Complex web application types
    # =========================================================================

    class Application:
        """Web application complex types."""

        type ApplicationConfiguration = dict[
            str, FlextTypes.ConfigValue | FlextTypes.Dict
        ]
        type ApplicationMetadata = dict[
            str, str | int | bool | dict[str, FlextTypes.JsonValue]
        ]
        type ApplicationLifecycle = dict[str, str | bool | FlextTypes.Dict]
        type ApplicationSecurity = dict[
            str, bool | str | FlextTypes.StringList | dict[str, FlextTypes.ConfigValue]
        ]
        type ApplicationMiddleware = list[dict[str, FlextTypes.JsonValue]]
        type ApplicationRouting = dict[
            str, FlextTypes.StringList | dict[str, FlextTypes.JsonValue]
        ]

    # =========================================================================
    # HTTP REQUEST/RESPONSE TYPES - Complex HTTP handling types
    # =========================================================================

    class RequestResponse:
        """HTTP request and response complex types."""

        type RequestConfiguration = dict[str, FlextTypes.JsonValue | FlextTypes.Dict]
        type RequestHeaders = dict[str, str | FlextTypes.StringList]
        type RequestParameters = dict[
            str, FlextTypes.JsonValue | list[FlextTypes.JsonValue]
        ]
        type RequestBody = dict[str, FlextTypes.JsonValue] | str | bytes
        type ResponseConfiguration = dict[str, FlextTypes.JsonValue | FlextTypes.Dict]
        type ResponseHeaders = dict[str, str | FlextTypes.StringList]
        type ResponseBody = dict[str, FlextTypes.JsonValue] | str | bytes

    # =========================================================================
    # WEB SERVICE TYPES - Complex web service types
    # =========================================================================

    class WebService:
        """Web service complex types."""

        type ServiceConfiguration = dict[str, FlextTypes.ConfigValue | FlextTypes.Dict]
        type ServiceRegistration = dict[
            str, str | bool | dict[str, FlextTypes.JsonValue]
        ]
        type ServiceDiscovery = dict[
            str, FlextTypes.StringList | dict[str, FlextTypes.JsonValue]
        ]
        type ServiceHealth = dict[str, bool | int | str | FlextTypes.Dict]
        type ServiceMetrics = dict[str, int | float | dict[str, FlextTypes.JsonValue]]
        type ServiceDeployment = dict[str, str | dict[str, FlextTypes.ConfigValue]]

    # =========================================================================
    # WEB SECURITY TYPES - Complex security types
    # =========================================================================

    class Security:
        """Web security complex types."""

        type SecurityConfiguration = dict[
            str, bool | str | FlextTypes.StringList | dict[str, FlextTypes.ConfigValue]
        ]
        type AuthenticationConfig = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type AuthorizationPolicy = dict[
            str, FlextTypes.StringList | dict[str, bool | object]
        ]
        type CorsConfiguration = dict[
            str, bool | FlextTypes.StringList | FlextTypes.StringDict
        ]
        type CsrfProtection = dict[str, bool | str | dict[str, FlextTypes.ConfigValue]]
        type SecurityHeaders = dict[str, str | bool | FlextTypes.StringDict]

    # =========================================================================
    # API ENDPOINT TYPES - Complex API management types
    # =========================================================================

    class ApiEndpoint:
        """API endpoint complex types."""

        type EndpointConfiguration = dict[
            str, str | bool | FlextTypes.StringList | dict[str, FlextTypes.JsonValue]
        ]
        type EndpointValidation = dict[
            str, bool | FlextTypes.StringList | FlextTypes.Dict
        ]
        type EndpointDocumentation = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type RouteConfiguration = dict[
            str, str | FlextTypes.StringList | FlextTypes.Dict
        ]
        type ApiVersioning = dict[str, str | int | dict[str, FlextTypes.ConfigValue]]
        type RateLimiting = dict[str, int | dict[str, FlextTypes.JsonValue]]

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
            """Initialize dict with dataclass fields."""
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
        headers: FlextTypes.StringDict
        query_params: FlextTypes.StringDict
        body: str | bytes | None = None
        client_ip: str | None = None

    # =========================================================================
    # WEB PROJECT TYPES - Domain-specific project types extending FlextTypes
    # =========================================================================

    class Project(FlextTypes.Project):
        """Web-specific project types extending FlextTypes.Project.

        Adds web-specific project types while inheriting generic types from FlextTypes.
        Follows domain separation principle: Web domain owns web-specific types.
        """

        # Web-specific project types extending the generic ones
        type WebProjectType = Literal[
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
        type WebProjectConfig = dict[str, FlextTypes.ConfigValue | object]
        type FlaskProjectConfig = dict[str, str | int | bool | FlextTypes.StringList]
        type ApiProjectConfig = dict[str, bool | str | FlextTypes.Dict]
        type SecurityProjectConfig = dict[str, FlextTypes.ConfigValue | object]

    # Configuration methods
    @classmethod
    def configure_web_types_system(
        cls,
        config: FlextTypes.Dict,
    ) -> FlextResult[FlextTypes.Dict]:
        """Configure web types system.

        Returns:
            FlextResult[FlextTypes.Dict]: Configuration result.

        """
        try:
            validated_config: FlextTypes.Dict = dict(config)
            validated_config.setdefault("enable_strict_typing", True)
            validated_config.setdefault("enable_runtime_validation", True)
            return FlextResult[FlextTypes.Dict].ok(validated_config)
        except Exception as e:
            return FlextResult[FlextTypes.Dict].fail(
                f"Failed to configure web types system: {e}",
            )

    @classmethod
    def get_web_types_system_config(
        cls,
    ) -> FlextResult[FlextTypes.Dict]:
        """Get current web types system configuration."""
        try:
            config: FlextTypes.Dict = {
                "enable_strict_typing": "True",
                "enable_runtime_validation": "True",
                "total_type_definitions": 50,
                "factory_methods": 2,
            }
            return FlextResult[FlextTypes.Dict].ok(config)
        except Exception as e:
            return FlextResult[FlextTypes.Dict].fail(
                f"Failed to get web types system config: {e}",
            )

    @classmethod
    def create_app_data(
        cls,
        **kwargs: object,
    ) -> FlextTypes.Dict:
        """Create app data dictionary."""
        return dict(kwargs)

    @classmethod
    def create_config_data(cls) -> FlextTypes.Dict:
        """Create config data dictionary."""
        return {}

    @classmethod
    def create_request_context(
        cls,
        method: str = "GET",
        path: str = "/",
        headers: FlextTypes.StringDict | None = None,
        data: FlextTypes.Dict | None = None,
    ) -> FlextTypes.Dict:
        """Create request context dictionary."""
        return {
            "method": method,
            "path": path,
            "headers": headers or {},
            "data": data or {},
        }

    @classmethod
    def validate_app_data(cls, data: FlextTypes.Dict) -> FlextResult[FlextTypes.Dict]:
        """Validate app data."""
        if not isinstance(data, dict):
            return FlextResult[FlextTypes.Dict].fail("App data must be a dictionary")
        return FlextResult[FlextTypes.Dict].ok(data)

    @classmethod
    def validate_config_data(
        cls, data: FlextTypes.Dict | str
    ) -> FlextResult[FlextTypes.Dict]:
        """Validate config data."""
        if isinstance(data, str):
            return FlextResult[FlextTypes.Dict].fail("Config data must be a dictionary")
        return FlextResult[FlextTypes.Dict].ok(data)


# =============================================================================
# PUBLIC API EXPORTS - Web TypeVars and types
# =============================================================================


__all__ = [
    "FlextWebTypes",
]
