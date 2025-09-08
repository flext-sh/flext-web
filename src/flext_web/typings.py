"""Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from flext_core import FlextTypes

"""FLEXT Web Types - Consolidated web type system.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""


import os
from typing import TypedDict, TypeVar

from flext_core import FlextResult

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
        secret_key: str = os.getenv(
            "FLEXT_WEB_SECRET_KEY", "dev-key-unsafe-change-in-prod"
        ),
        app_name: str = "FLEXT Web",
    ) -> ConfigData:
        """Create config data structure with defaults."""
        return cls.ConfigData(
            host=host, port=port, debug=debug, secret_key=secret_key, app_name=app_name
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
            method=method, path=path, headers=headers or {}, data=data or {}
        )

    @classmethod
    def validate_config_data(
        cls, data: object
    ) -> FlextResult[FlextWebTypes.ConfigData]:
        """Validate configuration data structure."""
        try:
            if not isinstance(data, dict):
                return FlextResult[FlextWebTypes.ConfigData].fail(
                    "Data must be a dictionary"
                )

            required_fields = ["host", "port", "debug", "secret_key", "app_name"]
            for field in required_fields:
                if field not in data:
                    return FlextResult[FlextWebTypes.ConfigData].fail(
                        f"Required field '{field}' is missing"
                    )

            # Type validations
            if not isinstance(data["host"], str):
                return FlextResult[FlextWebTypes.ConfigData].fail(
                    "Field 'host' must be a string"
                )
            if not isinstance(data["port"], int):
                return FlextResult[FlextWebTypes.ConfigData].fail(
                    "Field 'port' must be an integer"
                )
            if not isinstance(data["debug"], bool):
                return FlextResult[FlextWebTypes.ConfigData].fail(
                    "Field 'debug' must be a boolean"
                )
            if not isinstance(data["secret_key"], str):
                return FlextResult[FlextWebTypes.ConfigData].fail(
                    "Field 'secret_key' must be a string"
                )
            if not isinstance(data["app_name"], str):
                return FlextResult[FlextWebTypes.ConfigData].fail(
                    "Field 'app_name' must be a string"
                )

            config_data = cls.ConfigData(
                host=data["host"],
                port=data["port"],
                debug=data["debug"],
                secret_key=data["secret_key"],
                app_name=data["app_name"],
            )
            return FlextResult[FlextWebTypes.ConfigData].ok(config_data)

        except Exception as e:
            return FlextResult[FlextWebTypes.ConfigData].fail(
                f"Configuration validation error: {e}"
            )

    @classmethod
    def validate_app_data(cls, data: object) -> FlextResult[FlextWebTypes.AppData]:
        """Validate app data structure."""
        try:
            if not isinstance(data, dict):
                return FlextResult[FlextWebTypes.AppData].fail(
                    "Data must be a dictionary"
                )

            required_fields = ["id", "name", "host", "port", "status", "is_running"]
            for field in required_fields:
                if field not in data:
                    return FlextResult[FlextWebTypes.AppData].fail(
                        f"Required field '{field}' is missing"
                    )

            # Type validations
            if not isinstance(data["id"], str):
                return FlextResult[FlextWebTypes.AppData].fail(
                    "Field 'id' must be a string"
                )
            if not isinstance(data["name"], str):
                return FlextResult[FlextWebTypes.AppData].fail(
                    "Field 'name' must be a string"
                )
            if not isinstance(data["host"], str):
                return FlextResult[FlextWebTypes.AppData].fail(
                    "Field 'host' must be a string"
                )
            if not isinstance(data["port"], int):
                return FlextResult[FlextWebTypes.AppData].fail(
                    "Field 'port' must be an integer"
                )
            if not isinstance(data["status"], str):
                return FlextResult[FlextWebTypes.AppData].fail(
                    "Field 'status' must be a string"
                )
            if not isinstance(data["is_running"], bool):
                return FlextResult[FlextWebTypes.AppData].fail(
                    "Field 'is_running' must be a boolean"
                )

            app_data = cls.AppData(
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
        cls, config: FlextTypes.Core.Dict
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Configure web types system.

        Returns:
            FlextResult[FlextWebTypes.AppData]:: Description of return value.

        """
        try:
            validated_config = dict(config)
            validated_config.setdefault("enable_strict_typing", True)
            validated_config.setdefault("enable_runtime_validation", True)
            return FlextResult[FlextTypes.Core.Dict].ok(validated_config)
        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Failed to configure web types system: {e}"
            )

    @classmethod
    def get_web_types_system_config(
        cls,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Get current web types system configuration."""
        try:
            config: FlextTypes.Core.Dict = {
                "enable_strict_typing": True,
                "enable_runtime_validation": True,
                "total_type_definitions": 50,
                "factory_methods": 2,
            }
            return FlextResult[FlextTypes.Core.Dict].ok(config)
        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Failed to get web types system config: {e}"
            )


__all__ = [
    "FlextTypes",
    "FlextWebTypes",
    "TFlaskApp",
    "TWebApp",
    "TWebConfig",
    "TWebHandler",
    "TWebRequest",
    "TWebResponse",
    "TWebService",
]
