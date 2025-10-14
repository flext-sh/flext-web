"""FlextWeb-specific utilities extending flext-core patterns.

Minimal implementation providing ONLY web-domain-specific utilities not available
in flext-core. Delegates all generic operations to FlextCore.Utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import re
from typing import TypeVar

from flext_core import FlextCore
from pydantic import ValidationError

from flext_web.constants import FlextWebConstants
from flext_web.models import FlextWebModels
from flext_web.typings import FlextWebTypes

T = TypeVar("T")


class FlextWebUtilities(FlextCore.Utilities):
    """Web-specific utilities delegating to flext-core.

    Inherits from FlextCore.Utilities to avoid duplication and ensure consistency.
    Provides only web-domain-specific functionality not available in FlextCore.Utilities.
    All generic operations delegate to FlextCore.Utilities from flext-core.
    """

    @staticmethod
    def _slugify(text: str) -> str:
        """Convert text to URL-safe slug format."""
        # Convert to lowercase and replace spaces/special chars with hyphens
        slug = re.sub(r"[^\w\s-]", "", text.lower())
        slug = re.sub(r"[-\s]+", "-", slug)
        return slug.strip("-")

    @staticmethod
    def generate_app_id(name: str) -> str:
        """Generate web application ID using flext-core utilities."""
        clean_name = FlextWebUtilities._slugify(name)
        base_id = FlextCore.Utilities.Generators.generate_entity_id()
        # Handle different base_id formats
        if "_" in base_id:
            return f"app_{clean_name}_{base_id.split('_')[1]}"
        return f"app_{clean_name}_{base_id}"

    @staticmethod
    def format_app_id(name: str) -> str:
        """Format application name to valid ID.

        Returns:
            str: Description of return value.

        """
        clean_name = FlextCore.Utilities.TextProcessor.safe_string(name).strip()
        slugified = FlextWebUtilities._slugify(clean_name)
        return f"app_{slugified}" if slugified else "app_default"

    @staticmethod
    def sanitize_request_data(
        data: FlextWebTypes.Core.RequestDict,
    ) -> FlextWebTypes.Core.RequestDict:
        """Sanitize web request data.

        Returns:
            FlextWebTypes.Core.RequestDict: Sanitized request data dictionary.

        """
        sanitized: FlextWebTypes.Core.RequestDict = {}
        for key, value in data.items():
            safe_key = FlextCore.Utilities.TextProcessor.safe_string(key)
            if isinstance(value, str):
                # More aggressive sanitization for string values
                safe_value = FlextCore.Utilities.TextProcessor.safe_string(value)
                # Remove special characters that could be problematic
                safe_value = re.sub(r"[^\w\s\-]", "", safe_value).strip()
                sanitized[safe_key] = safe_value
            else:
                sanitized[safe_key] = value
        return sanitized

    @staticmethod
    def create_success_response(
        message: str,
        data: object = None,
    ) -> FlextWebTypes.Core.ResponseDict:
        """Create success response structure.

        Returns:
            FlextWebTypes.Core.ResponseDict: Success response data dictionary.

        """
        return {
            "success": "True",
            "message": message,
            "data": data,
            "timestamp": FlextCore.Utilities.Generators.generate_iso_timestamp(),
        }

    @staticmethod
    def create_error_response(
        message: str,
        status_code: int = 400,
    ) -> FlextWebTypes.Core.ResponseDict:
        """Create error response structure.

        Returns:
            FlextWebTypes.Core.ResponseDict: Error response data dictionary.

        """
        return {
            "success": "False",
            "message": message,
            "data": None,
            "status_code": status_code,
            "timestamp": FlextCore.Utilities.Generators.generate_iso_timestamp(),
        }

    @staticmethod
    def create_api_response(
        message: str,
        *,
        success: bool = True,
        data: object = None,
    ) -> FlextWebTypes.Core.ResponseDict:
        """Create API response structure.

        Returns:
            FlextWebTypes.Core.ResponseDict: API response data dictionary.

        """
        return {
            "success": success,
            "message": message,
            "data": data,
            "timestamp": FlextCore.Utilities.Generators.generate_iso_timestamp(),
        }

    @staticmethod
    def handle_flext_result(
        result: FlextCore.Result[object],
    ) -> FlextWebTypes.Core.ResponseDict:
        """Convert FlextCore.Result to API response.

        Returns:
            FlextWebTypes.Core.ResponseDict: API response data dictionary.

        """
        if result.is_success:
            return FlextWebUtilities.create_api_response(
                "Operation successful",
                success=True,
                data=result.value,
            )
        return FlextWebUtilities.create_api_response(
            f"Operation failed: {result.error}",
            success=False,
            data=None,
        )

    @classmethod
    def create_web_app_data(
        cls,
        name: str,
        port: int = FlextWebConstants.WebServer.DEFAULT_PORT,
        host: str = FlextWebConstants.WebServer.DEFAULT_HOST,
    ) -> FlextCore.Result[FlextWebTypes.Core.ResponseDict]:
        """Create web application data with Pydantic validation.

        Returns:
            FlextCore.Result[FlextWebTypes.Core.ResponseDict]: Web application data result.

        """
        # Import at runtime to avoid circular imports

        try:
            # Let Pydantic handle all validation through field validators
            app = FlextWebModels.WebApp(
                id=cls.format_app_id(name),
                name=name,
                port=port,
                host=host,
            )

            app_data: FlextWebTypes.Core.ResponseDict = {
                "id": app.id,
                "name": app.name,
                "port": app.port,
                "host": app.host,
                "created_at": FlextCore.Utilities.Generators.generate_iso_timestamp(),
            }

            return FlextCore.Result[FlextWebTypes.Core.ResponseDict].ok(app_data)
        except ValidationError as e:
            # Extract meaningful error messages for compatibility
            error_msg = ""
            for error in e.errors():
                field = str(error["loc"][0]) if error["loc"] else "unknown"
                if "name" in field:
                    error_msg = f"Invalid app name: {name}"
                elif "port" in field:
                    error_msg = f"Invalid port: {port}"
                elif "host" in field:
                    error_msg = f"Invalid host: {host}"
                else:
                    error_msg = f"Validation error: {error['msg']}"
                break  # Use first error
            return FlextCore.Result[FlextWebTypes.Core.ResponseDict].fail(error_msg)
        except ValueError as e:
            return FlextCore.Result[FlextWebTypes.Core.ResponseDict].fail(str(e))


__all__ = [
    "FlextWebUtilities",
]
