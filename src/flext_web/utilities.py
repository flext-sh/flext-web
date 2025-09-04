"""FlextWeb-specific utilities extending flext-core patterns.

Minimal implementation providing ONLY web-domain-specific utilities not available
in flext-core. Delegates all generic operations to FlextUtilities.
"""

from __future__ import annotations

import re
from typing import TypeVar
from urllib.parse import urlparse

from flext_core import FlextConstants, FlextResult, FlextUtilities

T = TypeVar("T")


class FlextWebUtilities:
    """Web-specific utilities delegating to flext-core.

    Provides only web-domain-specific functionality not available in FlextUtilities.
    All generic operations delegate to FlextUtilities from flext-core.
    """

    @staticmethod
    def generate_app_id(name: str) -> str:
        """Generate web application ID using flext-core utilities."""
        clean_name = FlextUtilities.TextProcessor.slugify(name)
        base_id = FlextUtilities.Generators.generate_entity_id()
        return f"app_{clean_name}_{base_id.split('_')[1]}"

    @staticmethod
    def format_app_id(name: str) -> str:
        """Format application name to valid ID."""
        clean_name = FlextUtilities.TextProcessor.safe_string(name, "app").strip()
        slugified = FlextUtilities.TextProcessor.slugify(clean_name)
        return f"app_{slugified}" if slugified else "app_default"

    @staticmethod
    def validate_app_name(name: str | None) -> bool:
        """Validate application name format."""
        if name is None:
            return False
        safe_name = FlextUtilities.TextProcessor.safe_string(name, "")
        return safe_name.strip() != "" and len(safe_name.strip()) >= 1

    @staticmethod
    def validate_port_range(port: int) -> bool:
        """Validate port number range."""
        return FlextConstants.Web.MIN_PORT <= port <= FlextConstants.Web.MAX_PORT

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    @staticmethod
    def validate_host_format(host: str) -> bool:
        """Validate host address format."""
        safe_host = FlextUtilities.TextProcessor.safe_string(host, "")
        if not safe_host:
            return False

        safe_host = safe_host.strip()
        if not safe_host:
            return False

        # IPv4 pattern
        ipv4_pattern = (
            r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$"
        )
        if re.match(ipv4_pattern, safe_host):
            return True

        # Hostname pattern
        hostname_pattern = r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$"
        if re.match(hostname_pattern, safe_host):
            return True

        return safe_host.lower() in {"localhost", "0.0.0.0", "::", "::1"}  # nosec B104  # noqa: S104

    @staticmethod
    def sanitize_request_data(data: dict[str, object]) -> dict[str, object]:
        """Sanitize web request data."""
        sanitized: dict[str, object] = {}
        for key, value in data.items():
            safe_key = FlextUtilities.TextProcessor.safe_string(key, "unknown")
            if isinstance(value, str):
                safe_value = FlextUtilities.TextProcessor.safe_string(value, "")
                sanitized[safe_key] = safe_value
            else:
                sanitized[safe_key] = value
        return sanitized

    @staticmethod
    def create_success_response(message: str, data: object = None) -> dict[str, object]:
        """Create success response structure."""
        return {
            "success": True,
            "message": message,
            "data": data,
            "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
        }

    @staticmethod
    def create_error_response(
        message: str, status_code: int = 400
    ) -> dict[str, object]:
        """Create error response structure."""
        return {
            "success": False,
            "message": message,
            "data": None,
            "status_code": status_code,
            "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
        }

    @staticmethod
    def create_api_response(
        message: str, *, success: bool = True, data: object = None
    ) -> dict[str, object]:
        """Create API response structure."""
        return {
            "success": success,
            "message": message,
            "data": data,
            "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
        }

    @staticmethod
    def handle_flext_result(result: FlextResult[T]) -> dict[str, object]:
        """Convert FlextResult to API response."""
        if result.success:
            return FlextWebUtilities.create_api_response(
                "Operation successful", success=True, data=result.value
            )
        return FlextWebUtilities.create_api_response(
            f"Operation failed: {result.error}", success=False, data=None
        )

    @classmethod
    def create_web_app_data(
        cls, name: str, port: int = 8000, host: str = "localhost"
    ) -> FlextResult[dict[str, object]]:
        """Create web application data with validation."""
        if not cls.validate_app_name(name):
            return FlextResult[dict[str, object]].fail(f"Invalid app name: {name}")
        if not cls.validate_port_range(port):
            return FlextResult[dict[str, object]].fail(f"Invalid port: {port}")
        if not cls.validate_host_format(host):
            return FlextResult[dict[str, object]].fail(f"Invalid host: {host}")

        app_data = {
            "id": cls.format_app_id(name),
            "name": name,
            "port": port,
            "host": host,
            "created_at": FlextUtilities.Generators.generate_iso_timestamp(),
        }

        return FlextResult[dict[str, object]].ok(app_data)


__all__ = [
    "FlextWebUtilities",
]
