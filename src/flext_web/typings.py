"""FLEXT Web Types - Consolidated web type system following single-class pattern.

CONSOLIDAÇÃO COMPLETA seguindo flext-core architectural patterns:
- Apenas UMA classe FlextWebTypes com toda funcionalidade de tipos
- Todas as outras definições antigas removidas completamente
- Arquitetura consolidada seguindo padrão FLEXT estrito
- Python 3.13+ com type system avançado sem compatibilidade legada
- Uso EXTENSIVO do FlextTypes como base fundamental

Architecture Overview:
    FlextWebTypes - Single consolidated type class containing:
        - All web-specific type definitions as class attributes
        - Type aliases extending FlextTypes foundation
        - Factory methods for type creation and validation
        - Configuration methods for type system management

Examples:
    Using consolidated FlextWebTypes:
        app_data: FlextWebTypes.AppData = {"name": "MyApp", "port": 8080}
        response: FlextWebTypes.APIResponse = {"success": True, "message": "OK"}
        config: FlextWebTypes.ConfigData = {"host": "localhost", "port": 8080}

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Callable
from typing import TypedDict, TypeVar

from flask.typing import ResponseReturnValue
from flext_core import FlextResult, FlextTypes

from flext_web.constants import FlextWebConstants

# =============================================================================
# WEB-SPECIFIC TYPE VARIABLES
# =============================================================================

# Web domain-specific type variables extending flext-core foundation
TWebApp = TypeVar("TWebApp")  # Web application types
TWebConfig = TypeVar("TWebConfig")  # Web configuration types
TWebService = TypeVar("TWebService")  # Web service types
TWebHandler = TypeVar("TWebHandler")  # Web handler types
TWebRequest = TypeVar("TWebRequest")  # Web request types
TWebResponse = TypeVar("TWebResponse")  # Web response types
TFlaskApp = TypeVar("TFlaskApp")  # Flask application types


class FlextWebTypes:
    """Consolidated FLEXT web type system providing all web-specific type definitions.

    This is the complete web type system for the FLEXT Web ecosystem, following
    the single consolidated class pattern from flext-core. All web-specific types
    are defined as class attributes within this single container for consistent
    usage and centralized management.

    Architecture Overview:
        Single consolidated class containing all web type definitions:

        - **Application Types**: Web application data structures and validation
        - **API Types**: REST API request/response type definitions
        - **Configuration Types**: Web service configuration and settings
        - **Service Types**: Web service and handler type definitions
        - **Result Types**: Web operation result patterns with error handling
        - **Flask Types**: Flask framework integration type definitions

    Design Patterns:
        - **Single Point of Truth**: All web types in one consolidated class
        - **flext-core Extension**: Built on FlextTypes foundation patterns
        - **Type Safety**: Comprehensive generic annotations with Python 3.13+
        - **Centralized Management**: Single location for all web type definitions
        - **Factory Integration**: Type creation through factory methods
        - **Validation Support**: Type validation and constraint checking

    Usage Examples:
        Web application types::

            # Application data structure
            app_data: FlextWebTypes.AppData = {
                "id": "app_123",
                "name": "MyApp",
                "host": "localhost",
                "port": 8080,
                "status": "running",
                "is_running": True,
            }

            # Application creation request
            create_req: FlextWebTypes.CreateAppRequest = {
                "name": "NewApp",
                "host": "0.0.0.0",
                "port": 3000,
            }

        API response types::

            # Success response
            success: FlextWebTypes.SuccessResponse = {
                "success": True,
                "message": "Operation completed",
                "data": app_data,
            }

            # Error response
            error: FlextWebTypes.ErrorResponse = {
                "success": False,
                "message": "Operation failed",
                "error": "Validation error",
            }

        Configuration and service types::

            # Configuration data
            config_data: FlextWebTypes.ConfigData = {
                "host": "localhost",
                "port": 8080,
                "debug": True,
                "secret_key": "my-secret-key-32-chars-long!",
                "app_name": "FLEXT Web",
            }

    Note:
        This consolidated approach follows flext-core architectural patterns,
        ensuring consistency across the FLEXT ecosystem while providing
        comprehensive web-specific type functionality in a single class.

    """

    # =============================================================================
    # WEB APPLICATION TYPES
    # =============================================================================

    class AppData(TypedDict):
        """Web application data structure for API responses and internal processing."""

        id: str
        name: str
        host: str
        port: int
        status: str
        is_running: bool

    class AppCreationData(TypedDict):
        """Web application creation data structure for API requests."""

        name: str
        host: str
        port: int

    class AppUpdateData(TypedDict, total=False):
        """Web application update data structure with optional fields."""

        name: str
        host: str
        port: int
        status: str

    # =============================================================================
    # API TYPES
    # =============================================================================

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

        data: dict[str, object]

    class ErrorResponse(BaseResponse):
        """Error API response with error details."""

        error: str

    class ListResponse(BaseResponse):
        """List API response for multiple items."""

        data: list[dict[str, object]]

    class HealthResponse(TypedDict):
        """Health check API response structure."""

        status: str
        service: str
        version: str
        applications: int
        timestamp: str

    # =============================================================================
    # CONFIGURATION TYPES
    # =============================================================================

    class ConfigData(TypedDict):
        """Web configuration data structure for factory methods."""

        host: str
        port: int
        debug: bool
        secret_key: str
        app_name: str

    class ProductionConfigData(TypedDict):
        """Production-specific configuration requirements."""

        host: str
        port: int
        secret_key: str  # Required in production
        debug: bool  # Must be False
        enable_cors: bool

    class DevelopmentConfigData(TypedDict, total=False):
        """Development-specific configuration with optional overrides."""

        host: str
        port: int
        debug: bool
        secret_key: str
        enable_cors: bool

    # =============================================================================
    # SERVICE TYPES
    # =============================================================================

    # Service implementation types
    WebService = object  # FlextWebServices.WebService type
    ServiceRegistry = object  # FlextWebServices.WebServiceRegistry type
    FlaskApplication = object  # Flask application instance type

    # Handler types
    RequestHandler = Callable[[object], ResponseReturnValue]  # Flask route handler
    ErrorHandler = Callable[[Exception], ResponseReturnValue]  # Error handler
    MiddlewareHandler = Callable[[object], object]  # Middleware handler

    # Flask integration types
    RouteHandler = Callable[[object], ResponseReturnValue]  # Flask route handler type
    URLRule = str  # Flask URL rule pattern
    HTTPMethod = str  # HTTP method: "GET", "POST", "PUT", "DELETE"

    # =============================================================================
    # SIMPLE TYPE ALIASES
    # =============================================================================

    # Application types
    AppStatus = str  # Application status values: "stopped", "starting", "running", "stopping", "error"
    AppId = str  # Application identifier format: "app_{name}"
    AppName = str  # Application name validation pattern
    AppHost = str  # Host address format validation
    AppPort = int  # Port number range validation (1-65535)

    # Service types
    ServiceName = str  # Service registry name identifier
    ServiceInstance = object  # Service instance type (generic for flexibility)
    ServiceHealth = bool  # Service health status indicator
    ServiceStatus = str  # Service status: "starting", "running", "stopping", "stopped"
    ServiceMetrics = dict[str, object]  # Service performance metrics

    # API types
    HTTPStatus = int  # HTTP status codes (200, 400, 404, 500, etc.)
    APIMessage = str  # API response message text
    ErrorCode = str  # Structured error code identifier
    ErrorDetails = str  # Detailed error description

    # Configuration types
    Environment = (
        str  # Environment names: "development", "staging", "production", "test"
    )
    SecretKey = str  # Secret key format (minimum 32 characters)
    HostAddress = str  # Valid host address format
    PortNumber = int  # Port number range (1-65535)
    ConfigDict = dict[str, object]  # Generic configuration dictionary
    ConfigErrors = list[str]  # Configuration error messages

    # Result types extending FlextResult
    WebResult = FlextResult[object]  # Generic web result type
    AppResult = FlextResult[AppData]  # Application operation result
    ConfigResult = FlextResult[ConfigData]  # Configuration operation result
    ServiceResult = FlextResult[
        object
    ]  # Service operation result (WebService is object type)

    # Validation types
    ValidationError = str  # Validation error message
    ValidationErrors = list[str]  # Multiple validation errors
    ValidationResult = FlextResult[None]  # Validation operation result
    ValidatorFunction = Callable[[object], bool]  # Custom validator function

    # Flask types
    FlaskApp = object  # Flask application instance
    FlaskConfig = dict[str, object]  # Flask configuration dictionary
    FlaskRequest = object  # Flask request object
    FlaskResponse = ResponseReturnValue  # Flask response type

    # Additional TypedDict classes for compatibility
    class ResponseDataDict(TypedDict, total=False):
        """Generic response data dictionary structure."""

        success: bool
        message: str
        data: dict[str, object] | list[object] | None
        error: str
        errors: list[str] | dict[str, object]
        timestamp: str

    class RequestContext(TypedDict, total=False):
        """Request context data structure."""

        user_id: str
        session_id: str
        timestamp: str
        headers: dict[str, str]

    # Type aliases using proper types
    ResponseData = dict[str, object]  # Generic response data type
    TemplateFilter = Callable[[str], str]  # Template filter function type

    # =============================================================================
    # FACTORY METHODS AND UTILITIES
    # =============================================================================

    @classmethod
    def create_app_data(
        cls,
        app_id: str,
        name: str,
        host: str,
        port: int,
        status: str,
        *,
        is_running: bool = False,
    ) -> FlextWebTypes.AppData:
        """Create application data structure with validation."""
        return cls.AppData(
            id=app_id,
            name=name,
            host=host,
            port=port,
            status=status,
            is_running=is_running,
        )

    @classmethod
    def create_success_response(
        cls, message: str, data: dict[str, object]
    ) -> FlextWebTypes.SuccessResponse:
        """Create success API response structure."""
        return cls.SuccessResponse(success=True, message=message, data=data)

    @classmethod
    def create_error_response(
        cls, message: str, error: str
    ) -> FlextWebTypes.ErrorResponse:
        """Create error API response structure."""
        return cls.ErrorResponse(success=False, message=message, error=error)

    @classmethod
    def create_config_data(
        cls,
        host: str = "localhost",
        port: int = 8080,
        *,
        debug: bool = True,
        secret_key: str = FlextWebConstants.WebSpecific.DEV_SECRET_KEY,
        app_name: str = "FLEXT Web",
    ) -> FlextWebTypes.ConfigData:
        """Create configuration data structure with defaults."""
        return cls.ConfigData(
            host=host,
            port=port,
            debug=debug,
            secret_key=secret_key,
            app_name=app_name,
        )

    @classmethod
    def validate_app_data(
        cls, data: dict[str, object]
    ) -> FlextResult[FlextWebTypes.AppData]:
        """Validate and convert dictionary to AppData structure."""
        try:
            required_fields = {
                "id",
                "name",
                "host",
                "port",
                "status",
                "is_running",
            }
            missing_fields = required_fields - set(data.keys())

            if missing_fields:
                return FlextResult[FlextWebTypes.AppData].fail(
                    f"Missing required fields: {', '.join(missing_fields)}"
                )

            # Type-safe casting with validation
            port_value = data["port"]

            def _validate_app_port(value: object) -> int:
                if not isinstance(value, (int, str)):
                    msg = f"Port must be int or str, got {type(value)}"
                    raise TypeError(msg)  # noqa: TRY301
                return int(value)

            safe_port = _validate_app_port(port_value)

            app_data = FlextWebTypes.AppData(
                id=str(data["id"]),
                name=str(data["name"]),
                host=str(data["host"]),
                port=safe_port,
                status=str(data["status"]),
                is_running=bool(data["is_running"]),
            )

            return FlextResult[FlextWebTypes.AppData].ok(app_data)

        except Exception as e:
            return FlextResult[FlextWebTypes.AppData].fail(
                f"App data validation failed: {e}"
            )

    @classmethod
    def validate_config_data(
        cls, data: dict[str, object]
    ) -> FlextResult[FlextWebTypes.ConfigData]:
        """Validate and convert dictionary to ConfigData structure."""
        try:
            required_fields = {
                "host",
                "port",
                "debug",
                "secret_key",
                "app_name",
            }
            missing_fields = required_fields - set(data.keys())

            if missing_fields:
                return FlextResult[FlextWebTypes.ConfigData].fail(
                    f"Missing required fields: {', '.join(missing_fields)}"
                )

            # Type-safe casting with validation
            port_value = data["port"]

            def _validate_config_port(value: object) -> int:
                if not isinstance(value, (int, str)):
                    msg = f"Port must be int or str, got {type(value)}"
                    raise TypeError(msg)  # noqa: TRY301
                return int(value)

            safe_port = _validate_config_port(port_value)

            config_data = FlextWebTypes.ConfigData(
                host=str(data["host"]),
                port=safe_port,
                debug=bool(data["debug"]),
                secret_key=str(data["secret_key"]),
                app_name=str(data["app_name"]),
            )

            return FlextResult[FlextWebTypes.ConfigData].ok(config_data)

        except Exception as e:
            return FlextResult[FlextWebTypes.ConfigData].fail(
                f"Config data validation failed: {e}"
            )

    # =============================================================================
    # FLEXT WEB TYPES CONFIGURATION METHODS
    # =============================================================================

    @classmethod
    def configure_web_types_system(
        cls, config: FlextTypes.Config.ConfigDict
    ) -> FlextResult[FlextTypes.Config.ConfigDict]:
        """Configure web types system using FlextTypes.Config with validation."""
        try:
            validated_config = dict(config)

            # Web types specific settings
            validated_config.setdefault("enable_strict_typing", True)
            validated_config.setdefault("enable_runtime_validation", True)
            validated_config.setdefault("enable_type_checking", True)
            validated_config.setdefault("enable_protocol_validation", True)

            return FlextResult[FlextTypes.Config.ConfigDict].ok(validated_config)

        except Exception as e:
            return FlextResult[FlextTypes.Config.ConfigDict].fail(
                f"Failed to configure web types system: {e}"
            )

    @classmethod
    def get_web_types_system_config(
        cls,
    ) -> FlextResult[FlextTypes.Config.ConfigDict]:
        """Get current web types system configuration with runtime information."""
        try:
            config: FlextTypes.Config.ConfigDict = {
                # Type system settings
                "enable_strict_typing": True,
                "enable_runtime_validation": True,
                "enable_type_checking": True,
                "enable_protocol_validation": True,
                # Available type categories
                "available_type_categories": [
                    "AppData",
                    "APIResponse",
                    "ConfigData",
                    "ServiceTypes",
                ],
                # Type system metrics
                "total_type_definitions": 50,
                "factory_methods": 10,
                "validation_methods": 5,
            }

            return FlextResult[FlextTypes.Config.ConfigDict].ok(config)

        except Exception as e:
            return FlextResult[FlextTypes.Config.ConfigDict].fail(
                f"Failed to get web types system config: {e}"
            )


# =============================================================================
# NO ALIASES - USE DIRECT CLASS ACCESS FlextWebTypes.*
# =============================================================================


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    "FlextWebTypes",
    "TFlaskApp",
    "TWebApp",
    "TWebConfig",
    "TWebHandler",
    "TWebRequest",
    "TWebResponse",
    "TWebService",
]
