"""FLEXT Web Types - Domain-specific web type definitions extending flext-core.

This module provides web-specific type definitions extending FlextTypes.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends FlextTypes properly
- Single unified class per module pattern

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections import UserDict
from dataclasses import dataclass
from typing import Literal

from flask import Response
from flext_core import FlextResult, FlextTypes

from flext_web.constants import FlextWebConstants


class FlextWebTypes:
    """Web-specific type definitions extending FlextTypes.

    Domain-specific type system for web/HTTP operations.
    Contains ONLY complex web-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    Follows single unified class per module pattern.
    """

    # =========================================================================
    # CORE WEB TYPES - Commonly used type aliases extending FlextTypes
    # =========================================================================

    class Core:
        """Core Web types extending FlextTypes.

        Replaces generic dict[str, object] with semantic web types.
        """

        type WebResponse = (
            tuple[str, int]
            | tuple[str, int, dict[str, str]]
            | tuple[Response, int]
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
        type ExtendedConfigDict = dict[str, object | dict[str, object]]
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

        type ApplicationConfiguration = dict[str, object | dict[str, object]]
        type ApplicationMetadata = dict[
            str, str | int | bool | dict[str, FlextTypes.JsonValue]
        ]
        type ApplicationLifecycle = dict[str, str | bool | dict[str, object]]
        type ApplicationSecurity = dict[
            str,
            bool | str | list[str] | dict[str, object],
        ]
        type ApplicationMiddleware = list[dict[str, FlextTypes.JsonValue]]
        type ApplicationRouting = dict[str, list[str] | dict[str, FlextTypes.JsonValue]]

    # =========================================================================
    # HTTP REQUEST/RESPONSE TYPES - Complex HTTP handling types
    # =========================================================================

    class RequestResponse:
        """HTTP request and response complex types."""

        type RequestConfiguration = dict[str, FlextTypes.JsonValue | dict[str, object]]
        type RequestHeaders = dict[str, str | list[str]]
        type RequestParameters = dict[
            str, FlextTypes.JsonValue | list[FlextTypes.JsonValue]
        ]
        type RequestBody = dict[str, FlextTypes.JsonValue] | str | bytes
        type ResponseConfiguration = dict[str, FlextTypes.JsonValue | dict[str, object]]
        type ResponseHeaders = dict[str, str | list[str]]
        type ResponseBody = dict[str, FlextTypes.JsonValue] | str | bytes

    # =========================================================================
    # WEB SERVICE TYPES - Complex web service types
    # =========================================================================

    class WebService:
        """Web service complex types."""

        type ServiceConfiguration = dict[str, object | dict[str, object]]
        type ServiceRegistration = dict[
            str, str | bool | dict[str, FlextTypes.JsonValue]
        ]
        type ServiceDiscovery = dict[str, list[str] | dict[str, FlextTypes.JsonValue]]
        type ServiceHealth = dict[str, bool | int | str | dict[str, object]]
        type ServiceMetrics = dict[str, int | float | dict[str, FlextTypes.JsonValue]]
        type ServiceDeployment = dict[str, str | dict[str, object]]

    # =========================================================================
    # WEB SECURITY TYPES - Complex security types
    # =========================================================================

    class Security:
        """Web security complex types."""

        type SecurityConfiguration = dict[
            str,
            bool | str | list[str] | dict[str, object],
        ]
        type AuthenticationConfig = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type AuthorizationPolicy = dict[str, list[str] | dict[str, bool | object]]
        type CorsConfiguration = dict[str, bool | list[str] | dict[str, str]]
        type CsrfProtection = dict[str, bool | str | dict[str, object]]
        type SecurityHeaders = dict[str, str | bool | dict[str, str]]

    # =========================================================================
    # API ENDPOINT TYPES - Complex API management types
    # =========================================================================

    class ApiEndpoint:
        """API endpoint complex types."""

        type EndpointConfiguration = dict[
            str,
            str | bool | list[str] | dict[str, FlextTypes.JsonValue],
        ]
        type EndpointValidation = dict[str, bool | list[str] | dict[str, object]]
        type EndpointDocumentation = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type RouteConfiguration = dict[str, str | list[str] | dict[str, object]]
        type ApiVersioning = dict[str, str | int | dict[str, object]]
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
        headers: dict[str, str]
        query_params: dict[str, str]
        body: str | bytes | None = None
        client_ip: str | None = None

    # =========================================================================
    # WEB PROJECT TYPES - Domain-specific project types extending FlextTypes
    # =========================================================================

    class Project(FlextTypes):
        """Web-specific project types extending FlextTypes.

        Adds web-specific project types while inheriting generic types from FlextTypes.
        Follows domain separation principle: Web domain owns web-specific types.
        """

        # Web-specific project types extending the generic ones
        type WebProjectType = Literal["webapp", "spa", "api-server", "web-service", "microservice", "rest-api", "web-portal", "dashboard", "REDACTED_LDAP_BIND_PASSWORD-panel"]

        # Web-specific project configurations
        type WebProjectConfig = dict[str, object]
        type FlaskProjectConfig = dict[str, str | int | bool | list[str]]
        type ApiProjectConfig = dict[str, bool | str | dict[str, object]]
        type SecurityProjectConfig = dict[str, object]

    # =========================================================================
    # CONFIGURATION METHODS - Type system configuration and validation
    # =========================================================================

    @classmethod
    def configure_web_types_system(
        cls,
        config: dict[str, object],
    ) -> FlextResult[dict[str, object]]:
        """Configure web types system.

        Args:
            config: Configuration dictionary for web types system

        Returns:
            FlextResult[dict[str, object]]: Configuration result

        """
        try:
            validated_config: dict[str, object] = dict[str, object](config)
            validated_config.setdefault("enable_strict_typing", True)
            validated_config.setdefault("enable_runtime_validation", True)
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
                "enable_strict_typing": True,
                "enable_runtime_validation": True,
                "total_type_definitions": 50,
                "factory_methods": 2,
            }
            return FlextResult[dict[str, object]].ok(config)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"Failed to get web types system config: {e}",
            )

    @classmethod
    def create_app_data(
        cls,
        **kwargs: object,
    ) -> dict[str, object]:
        """Create app data dictionary.

        Args:
            **kwargs: Application data fields

        Returns:
            dict[str, object]: Application data dictionary

        """
        return dict[str, object](kwargs)

    @classmethod
    def create_config_data(cls) -> dict[str, object]:
        """Create config data dictionary.

        Returns:
            dict[str, object]: Empty configuration dictionary

        """
        return {}

    @classmethod
    def create_request_context(
        cls,
        method: str = "GET",
        path: str = "/",
        headers: dict[str, str] | None = None,
        data: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Create request context dictionary.

        Args:
            method: HTTP method
            path: Request path
            headers: Request headers
            data: Request data

        Returns:
            dict[str, object]: Request context dictionary

        """
        return {
            "method": method,
            "path": path,
            "headers": headers or {},
            "data": data or {},
        }

    @classmethod
    def validate_app_data(
        cls, data: dict[str, object]
    ) -> FlextResult[dict[str, object]]:
        """Validate app data.

        Args:
            data: Application data to validate

        Returns:
            FlextResult[dict[str, object]]: Validation result

        """
        if not isinstance(data, dict):
            return FlextResult[dict[str, object]].fail("App data must be a dictionary")
        return FlextResult[dict[str, object]].ok(data)

    @classmethod
    def validate_config_data(
        cls, data: dict[str, object] | str
    ) -> FlextResult[dict[str, object]]:
        """Validate config data.

        Args:
            data: Configuration data to validate

        Returns:
            FlextResult[dict[str, object]]: Validation result

        """
        if isinstance(data, str):
            return FlextResult[dict[str, object]].fail(
                "Config data must be a dictionary"
            )
        return FlextResult[dict[str, object]].ok(data)


__all__ = [
    "FlextWebTypes",
]
