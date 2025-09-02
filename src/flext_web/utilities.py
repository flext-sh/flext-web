"""FlextWeb-specific utilities extending flext-core patterns.

MASSIVE USAGE: This module MASSIVELY uses FlextUtilities from flext-core for ALL
generic functionality while providing ONLY web-domain-specific extensions.

Single consolidated class following "one class per module" pattern with
MASSIVE delegation to FlextUtilities from flext-core.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse

from flext_core import FlextResult
from flext_core.utilities import FlextUtilities


class FlextWebUtilities:
    """Web-specific utilities with MASSIVE FlextUtilities delegation.

    MASSIVELY uses FlextUtilities from flext-core for ALL generic operations:
    - Generators: ALL ID/timestamp generation → FlextUtilities.Generators
    - TextProcessor: ALL text operations → FlextUtilities.TextProcessor
    - TimeUtils: ALL time formatting → FlextUtilities.TimeUtils
    - Performance: ALL performance tracking → FlextUtilities.Performance

    Only provides web-domain-specific extensions where absolutely necessary.
    """

    # =========================================================================
    # MASSIVE FLEXT-CORE DELEGATION CLASSES
    # =========================================================================

    class WebGenerators:
        """Web-specific ID generation using MASSIVE FlextUtilities.Generators delegation."""

        @staticmethod
        def generate_app_id(name: str) -> str:
            """Generate application ID using MASSIVE FlextUtilities.Generators + TextProcessor."""
            # MASSIVE USAGE: FlextUtilities.Generators.generate_entity_id()
            base_id = FlextUtilities.Generators.generate_entity_id()
            # MASSIVE USAGE: FlextUtilities.TextProcessor.slugify()
            clean_name = FlextUtilities.TextProcessor.slugify(name)
            return f"app_{clean_name}_{base_id.split('_')[1]}"

        @staticmethod
        def generate_session_token() -> str:
            """Generate session token using MASSIVE FlextUtilities.Generators."""
            return FlextUtilities.Generators.generate_session_id()

        @staticmethod
        def generate_request_id() -> str:
            """Generate request ID using MASSIVE FlextUtilities.Generators."""
            return FlextUtilities.Generators.generate_request_id()

        @staticmethod
        def generate_correlation_id() -> str:
            """Generate correlation ID using MASSIVE FlextUtilities.Generators."""
            return FlextUtilities.Generators.generate_correlation_id()

    class WebFormatters:
        """Web-specific formatting using MASSIVE FlextUtilities.TextProcessor delegation."""

        @staticmethod
        def format_app_id(name: str) -> str:
            """Format application name to ID using MASSIVE FlextUtilities.TextProcessor."""
            # MASSIVE USAGE: FlextUtilities.TextProcessor.safe_string + slugify
            clean_name = FlextUtilities.TextProcessor.safe_string(name, "app").strip()
            slugified = FlextUtilities.TextProcessor.slugify(clean_name)
            return f"app_{slugified}" if slugified else "app_default"

        @staticmethod
        def format_response_message(operation: str, name: str, *, success: bool) -> str:
            """Format response messages using MASSIVE FlextUtilities.TextProcessor."""
            status = "successfully" if success else "failed to"
            # MASSIVE USAGE: FlextUtilities.TextProcessor.safe_string for ALL strings
            clean_operation = FlextUtilities.TextProcessor.safe_string(
                operation, "operation"
            )
            clean_name = FlextUtilities.TextProcessor.safe_string(name, "item")
            return f"Application '{clean_name}' {status} {clean_operation}"

        @staticmethod
        def format_url_safe(text: str) -> str:
            """Format text to URL-safe using MASSIVE FlextUtilities.TextProcessor.slugify."""
            return FlextUtilities.TextProcessor.slugify(text)

        @staticmethod
        def format_duration(seconds: float) -> str:
            """Format duration using MASSIVE FlextUtilities.TimeUtils.format_duration."""
            return FlextUtilities.TimeUtils.format_duration(seconds)

    class WebValidators:
        """Web-specific validation using MASSIVE FlextUtilities delegation."""

        @staticmethod
        def validate_app_name(name: str | None) -> bool:
            """Validate application name using MASSIVE FlextUtilities.TextProcessor."""
            if name is None:
                return False
            # MASSIVE USAGE: FlextUtilities.TextProcessor.safe_string for validation
            safe_name = FlextUtilities.TextProcessor.safe_string(name, "")
            return safe_name.strip() != "" and len(safe_name.strip()) >= 1

        @staticmethod
        def validate_port_range(port: int) -> bool:
            """Validate port using MASSIVE FlextUtilities constants."""
            # MASSIVE USAGE: FlextUtilities.MIN_PORT and MAX_PORT constants
            return FlextUtilities.MIN_PORT <= port <= FlextUtilities.MAX_PORT

        @staticmethod
        def validate_url(url: str) -> bool:
            """Validate basic URL format."""
            try:
                result = urlparse(url)
                return all([result.scheme, result.netloc])
            except Exception:
                return False

        @staticmethod
        def validate_host_format(host: str) -> bool:
            """Validate host format using MASSIVE FlextUtilities.TextProcessor."""
            # MASSIVE USAGE: FlextUtilities.TextProcessor.safe_string for safety
            safe_host = FlextUtilities.TextProcessor.safe_string(host, "")
            if not safe_host:
                return False

            safe_host = safe_host.strip()
            if not safe_host:
                return False

            # Basic validation for common patterns
            # IPv4 pattern
            ipv4_pattern = r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$"
            if re.match(ipv4_pattern, safe_host):
                return True

            # Hostname pattern (simplified)
            hostname_pattern = r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$"
            if re.match(hostname_pattern, safe_host):
                return True

            # localhost and similar
            return safe_host.lower() in {"localhost", "0.0.0.0", "::", "::1"}

    class WebProcessors:
        """Web-specific processing using MASSIVE FlextUtilities delegation."""

        @staticmethod
        def sanitize_request_data(data: dict[str, object]) -> dict[str, object]:
            """Sanitize request data using MASSIVE FlextUtilities.TextProcessor."""
            sanitized: dict[str, object] = {}
            for key, value in data.items():
                # MASSIVE USAGE: FlextUtilities.TextProcessor.safe_string for ALL conversions
                safe_key = FlextUtilities.TextProcessor.safe_string(key, "unknown")
                if isinstance(value, str):
                    safe_value = FlextUtilities.TextProcessor.safe_string(value, "")
                    sanitized[safe_key] = safe_value
                else:
                    sanitized[safe_key] = value
            return sanitized

        @staticmethod
        def extract_app_info_from_request(data: dict[str, object]) -> dict[str, object]:
            """Extract app info using MASSIVE FlextWebUtilities delegation."""
            # MASSIVE USAGE: FlextWebUtilities.WebProcessors.sanitize_request_data
            sanitized = FlextWebUtilities.WebProcessors.sanitize_request_data(data)

            return {
                "name": sanitized.get("name", ""),
                "port": sanitized.get("port", 8000),
                "host": sanitized.get("host", "localhost"),
            }

    class WebFactories:
        """Web-specific factories using MASSIVE FlextUtilities delegation."""

        @staticmethod
        def create_success_response(
            message: str, data: object = None
        ) -> dict[str, object]:
            """Create success response using MASSIVE FlextUtilities.Generators."""
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
            """Create error response using MASSIVE FlextUtilities.Generators."""
            return {
                "success": False,
                "message": message,
                "data": None,
                "status_code": status_code,
                "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
            }

    class WebResultUtils:
        """Web result utilities using MASSIVE FlextUtilities delegation."""

        @staticmethod
        def create_api_response(
            message: str, *, success: bool = True, data: object = None
        ) -> dict[str, object]:
            """Create API response using MASSIVE FlextUtilities.Generators."""
            return {
                "success": success,
                "message": message,
                "data": data,
                "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
            }

        @staticmethod
        def handle_flext_result(result: FlextResult[object]) -> dict[str, object]:
            """Handle FlextResult using MASSIVE FlextUtilities delegation."""
            if result.success:
                return FlextWebUtilities.WebResultUtils.create_api_response(
                    "Operation successful", success=True, data=result.value
                )
            return FlextWebUtilities.WebResultUtils.create_api_response(
                f"Operation failed: {result.error}", success=False, data=None
            )

    # =========================================================================
    # WEB-SPECIFIC APPLICATION CREATION (using MASSIVE delegation)
    # =========================================================================

    @classmethod
    def create_web_app_data(
        cls, name: str, port: int = 8000, host: str = "localhost"
    ) -> FlextResult[dict[str, object]]:
        """Create web app data using MASSIVE FlextUtilities validation and generation."""
        # MASSIVE USAGE: FlextWebUtilities.WebValidators for ALL validation
        if not FlextWebUtilities.WebValidators.validate_app_name(name):
            return FlextResult[dict[str, object]].fail(f"Invalid app name: {name}")
        if not FlextWebUtilities.WebValidators.validate_port_range(port):
            return FlextResult[dict[str, object]].fail(f"Invalid port: {port}")
        if not FlextWebUtilities.WebValidators.validate_host_format(host):
            return FlextResult[dict[str, object]].fail(f"Invalid host: {host}")

        # MASSIVE USAGE: FlextWebUtilities.WebFormatters + FlextUtilities.Generators
        app_data = {
            "id": FlextWebUtilities.WebFormatters.format_app_id(name),
            "name": name,
            "port": port,
            "host": host,
            "created_at": FlextUtilities.Generators.generate_iso_timestamp(),
        }

        return FlextResult[dict[str, object]].ok(app_data)

    class WebMetrics:
        """Web service metrics and observability using MASSIVE FlextObservability delegation."""

        @staticmethod
        def track_app_creation(name: str, duration: float) -> FlextResult[None]:
            """Track app creation metrics (placeholder implementation)."""
            try:
                # Placeholder: Actual FlextObservability integration would be here
                # For now, just validate input and return success
                _ = FlextUtilities.TextProcessor.safe_string(name, "unknown")
                _ = duration  # Use duration parameter
                # Log the metrics instead of recording to actual metrics system
                # This would be replaced with actual FlextObservability calls
                return FlextResult[None].ok(None)
            except Exception as e:
                return FlextResult[None].fail(f"Metrics tracking failed: {e}")

        @staticmethod
        def track_app_operation(
            operation: str, app_name: str, *, success: bool
        ) -> FlextResult[None]:
            """Track app operations (placeholder implementation)."""
            try:
                _ = "success" if success else "failure"  # Use success parameter
                _ = FlextUtilities.TextProcessor.safe_string(operation, "unknown")
                _ = FlextUtilities.TextProcessor.safe_string(app_name, "unknown")
                # Placeholder: Actual FlextObservability integration would be here
                return FlextResult[None].ok(None)
            except Exception as e:
                return FlextResult[None].fail(f"Operation metrics tracking failed: {e}")

        @staticmethod
        def create_health_check() -> FlextResult[dict[str, object]]:
            """Create health check (placeholder implementation)."""
            try:
                # Placeholder: Simple health check without FlextObservability
                health_data: dict[str, object] = {
                    "status": "healthy",
                    "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
                    "service": "flext-web",
                    "version": "0.9.0",
                }
                return FlextResult[dict[str, object]].ok(health_data)
            except Exception as e:
                return FlextResult[dict[str, object]].fail(f"Health check failed: {e}")


__all__ = [
    "FlextWebUtilities",
]
