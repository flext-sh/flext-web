"""FLEXT Web Types - Consolidated web type system.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TypedDict, TypeVar

from flask.typing import ResponseReturnValue
from flext_core import FlextResult, FlextTypes

# Web domain-specific type variables
TWebApp = TypeVar("TWebApp")
TWebConfig = TypeVar("TWebConfig")
TWebService = TypeVar("TWebService")
TWebHandler = TypeVar("TWebHandler")
TWebRequest = TypeVar("TWebRequest")
TWebResponse = TypeVar("TWebResponse")
TFlaskApp = TypeVar("TFlaskApp")


class FlextWebTypes:
    """Consolidated FLEXT web type system."""

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

    # Service types
    WebService = object
    ServiceRegistry = object
    FlaskApplication = object

    # Handler types
    RequestHandler = Callable[[object], ResponseReturnValue]
    ErrorHandler = Callable[[Exception], ResponseReturnValue]
    MiddlewareHandler = Callable[[object], object]

    # Flask integration types
    RouteHandler = Callable[[object], ResponseReturnValue]
    URLRule = str
    HTTPMethod = str

    # Simple type aliases
    AppStatus = str
    AppId = str
    AppName = str
    AppHost = str
    AppPort = int

    ServiceName = str
    ServiceInstance = object
    ServiceHealth = bool
    ServiceStatus = str
    ServiceMetrics = dict[str, object]

    HTTPStatus = int
    APIMessage = str
    ErrorCode = str
    ErrorDetails = str

    Environment = str
    SecretKey = str
    HostAddress = str
    PortNumber = int
    ConfigDict = dict[str, object]
    ConfigErrors = list[str]

    # Result types
    WebResult = FlextResult[object]
    AppResult = FlextResult[AppData]
    ConfigResult = FlextResult[ConfigData]
    ServiceResult = FlextResult[object]

    # Validation types
    ValidationError = str
    ValidationErrors = list[str]
    ValidationResult = FlextResult[None]
    ValidatorFunction = Callable[[object], bool]

    # Flask types
    FlaskApp = object
    FlaskConfig = dict[str, object]
    FlaskRequest = object
    FlaskResponse = ResponseReturnValue

    # Additional TypedDict classes
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

    # Type aliases
    ResponseData = dict[str, object]
    TemplateFilter = Callable[[str], str]

    # Factory methods
    @classmethod
    def create_success_response(
        cls, message: str, data: dict[str, object]
    ) -> SuccessResponse:
        """Create success API response structure."""
        return cls.SuccessResponse(success=True, message=message, data=data)

    @classmethod
    def create_error_response(cls, message: str, error: str) -> ErrorResponse:
        """Create error API response structure."""
        return cls.ErrorResponse(success=False, message=message, error=error)

    # Configuration methods
    @classmethod
    def configure_web_types_system(
        cls, config: FlextTypes.Config.ConfigDict
    ) -> FlextResult[FlextTypes.Config.ConfigDict]:
        """Configure web types system."""
        try:
            validated_config = dict(config)
            validated_config.setdefault("enable_strict_typing", True)
            validated_config.setdefault("enable_runtime_validation", True)
            return FlextResult[FlextTypes.Config.ConfigDict].ok(validated_config)
        except Exception as e:
            return FlextResult[FlextTypes.Config.ConfigDict].fail(
                f"Failed to configure web types system: {e}"
            )

    @classmethod
    def get_web_types_system_config(
        cls,
    ) -> FlextResult[FlextTypes.Config.ConfigDict]:
        """Get current web types system configuration."""
        try:
            config: FlextTypes.Config.ConfigDict = {
                "enable_strict_typing": True,
                "enable_runtime_validation": True,
                "total_type_definitions": 50,
                "factory_methods": 2,
            }
            return FlextResult[FlextTypes.Config.ConfigDict].ok(config)
        except Exception as e:
            return FlextResult[FlextTypes.Config.ConfigDict].fail(
                f"Failed to get web types system config: {e}"
            )


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
