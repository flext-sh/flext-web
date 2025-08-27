"""FlextWeb-specific utilities extending flext-core patterns.

This module provides web-specific utility functionality while following the
FLEXT architectural requirement of extending FlextUtilities from flext-core
rather than creating duplicate implementations.

MASSIVE EXPANSION: Uses all 15+ utility classes from flext-core plus web-specific extensions.
Single consolidated class following "one class per module" pattern.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse

from flext_core import FlextResult, FlextUtilities


class FlextWebUtilities(FlextUtilities):
    """Web-specific utilities extending FlextUtilities from flext-core.

    Following FLEXT architectural patterns - extends base FlextUtilities
    rather than duplicating functionality. Adds web-specific operations
    while inheriting all core utility functionality.

    Extends: FlextUtilities with 15+ utility classes from flext-core:
    - Generators: ID/timestamp generation
    - TextProcessor: Text cleaning/formatting
    - TimeUtils: Duration formatting
    - Performance: Function timing
    - Conversions: Type conversions
    - TypeGuards: Type checking
    - Formatters: Data formatting
    - ProcessingUtils: Processing operations
    - ResultUtils: Result processing
    - Factories: Object creation
    """

    # =========================================================================
    # WEB-SPECIFIC EXTENSIONS (using flext-core utilities where possible)
    # =========================================================================

    class WebGenerators:
        """Web-specific ID generation using flext-core Generators."""

        @staticmethod
        def generate_app_id(name: str) -> str:
            """Generate application ID with web_ prefix using core generators."""
            # Use core ID generation + web-specific formatting
            base_id = FlextUtilities.Generators.generate_id()
            clean_name = FlextUtilities.TextProcessor.slugify(name)
            return f"web_{clean_name}_{base_id.split('_')[1]}"

        @staticmethod
        def generate_session_token() -> str:
            """Generate web session token using core generators."""
            return FlextUtilities.Generators.generate_session_id()

        @staticmethod
        def generate_request_id() -> str:
            """Generate web request ID using core generators."""
            return FlextUtilities.Generators.generate_request_id()

        @staticmethod
        def generate_correlation_id() -> str:
            """Generate correlation ID for request tracing."""
            return FlextUtilities.Generators.generate_correlation_id()

    class WebFormatters:
        """Web-specific formatting operations using flext-core Formatters."""

        @staticmethod
        def format_app_id(name: str) -> str:
            """Format application name into consistent app_id format."""
            # Use core text processing for cleaning
            clean_name = FlextUtilities.TextProcessor.clean_text(name)
            slugified = FlextUtilities.TextProcessor.slugify(clean_name)
            return f"app_{slugified}"

        @staticmethod
        def format_response_message(operation: str, name: str, *, success: bool) -> str:
            """Format consistent API response messages."""
            # Use core text processing
            clean_operation = FlextUtilities.TextProcessor.clean_text(operation)
            clean_name = FlextUtilities.TextProcessor.clean_text(name)
            status = "successfully" if success else "failed"
            return f"Application '{clean_name}' {clean_operation} {status}"

        @staticmethod
        def format_url_safe(text: str) -> str:
            """Format text to be URL-safe using core text processing."""
            return FlextUtilities.TextProcessor.slugify(text)

        @staticmethod
        def format_duration(seconds: float) -> str:
            """Format duration using core time utilities."""
            return FlextUtilities.TimeUtils.format_duration(seconds)

        @staticmethod
        def mask_api_key(api_key: str) -> str:
            """Mask API key for logging using core text processing."""
            return FlextUtilities.TextProcessor.mask_sensitive(
                api_key, show_first=4, show_last=4
            )

    class WebValidators:
        """Web-specific validation operations using flext-core validators."""

        @staticmethod
        def validate_app_name(name: str | None) -> bool:
            """Validate application name follows web standards."""
            if not name or not isinstance(name, str):
                return False

            # Use core text processing for cleaning
            clean_name = FlextUtilities.TextProcessor.clean_text(name)
            min_name_length = 2
            if not clean_name or len(clean_name) < min_name_length:
                return False

            # Web-specific validation: allow letters, numbers, hyphens, underscores
            return re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", clean_name) is not None

        @staticmethod
        def validate_port_range(port: int) -> bool:
            """Validate port is in valid range for web services."""
            return FlextUtilities.MIN_PORT <= port <= FlextUtilities.MAX_PORT

        @staticmethod
        def validate_url(url: str) -> bool:
            """Validate URL format."""
            try:
                parsed = urlparse(url)
                return bool(parsed.scheme and parsed.netloc)
            except Exception:
                return False

        @staticmethod
        def validate_host_format(host: str) -> bool:
            """Validate host format (IP or hostname)."""
            if not host:
                return False

            # Check for localhost or IP patterns
            if host in {"localhost", "0.0.0.0", "127.0.0.1"}:  # noqa: S104
                return True

            # Basic hostname validation
            return re.match(r"^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$", host) is not None

    class WebConverters:
        """Web-specific conversion operations using flext-core Conversions."""

        @staticmethod
        def status_to_http_code(status: str) -> int:
            """Convert application status to appropriate HTTP status code."""
            status_map = {
                "CREATED": 201,
                "RUNNING": 200,
                "STOPPED": 200,
                "ERROR": 500,
                "STARTING": 202,
                "STOPPING": 202,
                "FAILED": 500,
            }
            return status_map.get(status.upper(), 400)

        @staticmethod
        def dict_to_query_string(params: dict[str, object]) -> str:
            """Convert dictionary to URL query string using core conversions."""
            if not params:
                return ""

            pairs = []
            for key, value in params.items():
                if value is not None:
                    # Use core type conversion
                    str_value = str(value)
                    pairs.append(f"{key}={str_value}")
            return "&".join(pairs)

        @staticmethod
        def bytes_to_human_readable(bytes_count: int) -> str:
            """Convert bytes to human readable format."""
            kb = 1024
            mb = kb * 1024
            gb = mb * 1024

            if bytes_count < kb:
                return f"{bytes_count} B"
            if bytes_count < mb:
                return f"{bytes_count / kb:.1f} KB"
            if bytes_count < gb:
                return f"{bytes_count / mb:.1f} MB"
            return f"{bytes_count / gb:.1f} GB"

    class WebProcessors:
        """Web-specific processing using flext-core ProcessingUtils."""

        @staticmethod
        def sanitize_request_data(data: dict[str, object]) -> dict[str, object]:
            """Sanitize request data using core processing."""
            sanitized: dict[str, object] = {}
            for key, value in data.items():
                if isinstance(value, str):
                    # Use core text processing for cleaning
                    sanitized[key] = FlextUtilities.TextProcessor.clean_text(value)
                else:
                    sanitized[key] = value
            return sanitized

        @staticmethod
        def extract_app_info_from_request(data: dict[str, object]) -> dict[str, str | int]:
            """Extract and validate app info from request data."""
            # Use core processing and validation
            sanitized = FlextWebUtilities.WebProcessors.sanitize_request_data(data)

            result: dict[str, str | int] = {}
            if "name" in sanitized:
                result["name"] = str(sanitized["name"])
            if "port" in sanitized:
                try:
                    port_obj = sanitized["port"]
                    if isinstance(port_obj, (int, str)):
                        port_value = int(port_obj)
                        result["port"] = port_value
                    else:
                        result["port"] = 8000  # Default port
                except (ValueError, TypeError):
                    result["port"] = 8000  # Default port
            if "host" in sanitized:
                result["host"] = str(sanitized["host"])

            return result

    class WebResultUtils:
        """Web-specific result processing using flext-core ResultUtils."""

        @staticmethod
        def create_api_response(
            message: str,
            *,
            success: bool,
            data: object = None,
            errors: dict[str, str] | None = None
        ) -> dict[str, object]:
            """Create standardized API response format."""
            response = {
                "success": success,
                "message": FlextUtilities.TextProcessor.clean_text(message),
                "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
            }

            if data is not None:
                response["data"] = data
            if errors:
                response["errors"] = errors

            return response

        @staticmethod
        def handle_flext_result(result: FlextResult[object]) -> dict[str, object]:
            """Convert FlextResult to API response format."""
            if result.success:
                return FlextWebUtilities.WebResultUtils.create_api_response(
                    message="Operation completed successfully",
                    success=True,
                    data=result.value
                )
            return FlextWebUtilities.WebResultUtils.create_api_response(
                message=result.error or "Operation failed",
                success=False,
                errors={"error": result.error} if result.error else None
            )

    class WebFactories:
        """Web-specific factories using flext-core factory patterns."""

        @staticmethod
        def create_app_config(name: str, port: int = 8000, host: str = "localhost") -> dict[str, str | int]:
            """Create application configuration using validation."""
            # Use core validation and web validation
            if not FlextWebUtilities.WebValidators.validate_app_name(name):
                msg = f"Invalid app name: {name}"
                raise ValueError(msg)
            if not FlextWebUtilities.WebValidators.validate_port_range(port):
                msg = f"Invalid port: {port}"
                raise ValueError(msg)
            if not FlextWebUtilities.WebValidators.validate_host_format(host):
                msg = f"Invalid host: {host}"
                raise ValueError(msg)

            return {
                "id": FlextWebUtilities.WebFormatters.format_app_id(name),
                "name": name,
                "port": port,
                "host": host,
                "created_at": FlextUtilities.Generators.generate_iso_timestamp(),
            }

        @staticmethod
        def create_error_response(error_message: str, status_code: int = 500) -> dict[str, object]:
            """Create standardized error response."""
            return FlextWebUtilities.WebResultUtils.create_api_response(
                message=error_message,
                success=False,
                errors={"status_code": str(status_code)}
            )
