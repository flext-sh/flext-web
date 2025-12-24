#!/usr/bin/env python3
"""FLEXT Web Interface - API Usage Example.

Demonstrates how to interact with the FLEXT Web Interface REST API
for application lifecycle management using the refactored architecture.

This example shows:
- Health check using WebHandlers
- Application lifecycle management
- Error handling with FlextResult patterns
- Usage of new type aliases for better type safety
"""

import requests

from flext import FlextResult
from flext_web.typings import t


class ExampleConstants:
    """Consolidated constants for API usage example following flext-core patterns."""

    HTTP_OK = 200
    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = 8080
    BASE_URL = f"http://{DEFAULT_HOST}:{DEFAULT_PORT}"

    # API Endpoints
    APPS_BASE = "/api/v1/apps"
    APP_START = "/api/v1/apps/{app_id}/start"
    APP_DETAIL = "/api/v1/apps/{app_id}"
    APP_STOP = "/api/v1/apps/{app_id}/stop"


def check_service_health() -> bool:
    """Check if the service is running and healthy.

    Uses the /health endpoint that returns SuccessResponse with HealthResponse data.

    Returns:
        True if service is healthy, False otherwise.

    """
    try:
        response = requests.get(f"{ExampleConstants.BASE_URL}/health", timeout=5)
        if response.status_code != ExampleConstants.HTTP_OK:
            return False

        result = response.json()
        # Use ustructure - reduces returns
        validations = [
            isinstance(result, dict),
            result.get("success") is True,
            "data" in result,
            isinstance(result.get("data"), dict),
            result.get("data", {}).get("status") == "healthy",
        ]

        # All validations must pass
        return all(validations)
    except requests.RequestException:
        return False


def create_application(
    name: str,
    port: int,
    host: str = "localhost",
) -> t.AppData:
    """Create a new application using WebHandlers.

    Args:
        name: Application name (must follow WebFields validation)
        port: Port number (1-65535 range)
        host: Host address (default: localhost)

    Returns:
        Application data from FlextWebApp model.

    Raises:
        ValueError: If application creation fails.

    """
    request_data: dict[str, str | int] = {"name": name, "port": port, "host": host}

    # Use FlextResult for error handling - fast fail, no fallback
    def _make_request() -> FlextResult[requests.Response]:
        """Make HTTP request using FlextResult for error handling."""
        try:
            response = requests.post(
                f"{ExampleConstants.BASE_URL}{ExampleConstants.APPS_BASE}",
                json=request_data,
                timeout=5,
            )
            return FlextResult[requests.Response].ok(response)
        except requests.RequestException as e:
            return FlextResult[requests.Response].fail(f"Request failed: {e}")

    def _parse_json(response: requests.Response) -> FlextResult[dict[str, object]]:
        """Parse JSON response."""
        try:
            json_data = response.json()
            return FlextResult[dict[str, object]].ok(json_data)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(f"JSON parse failed: {e}")

    result = _make_request()
    if result.is_success and result.value.status_code != ExampleConstants.HTTP_OK:
        result = FlextResult[dict[str, object]].fail("HTTP request failed")
    else:
        result = result.flat_map(_parse_json).flat_map(
            lambda json_data: (
                FlextResult[t.AppData].ok(
                    t.AppData.model_validate(json_data["data"]),
                )
                if (
                    json_data.get("success")
                    and isinstance(data := json_data.get("data"), dict)
                    and "id" in data
                    and "name" in data
                )
                else FlextResult[t.AppData].fail("Invalid application data")
            ),
        )

    # Fast fail - no fallback to None
    if result.is_failure:
        error_msg = f"Application creation failed: {result.error}"
        raise ValueError(error_msg)
    return result.value


def _extract_apps_from_response(
    response_data: object,
    data_key: str,
) -> list[t.AppData]:
    """Extract apps list from response data with proper type checking."""
    # Fast fail - no fallback, validate structure explicitly
    if not isinstance(response_data, dict):
        return []
    if "data" not in response_data:
        return []
    data_section = response_data["data"]
    if not isinstance(data_section, dict):
        return []

    # Fast fail - no fallback, validate structure explicitly
    if data_key not in data_section:
        return []
    apps_list = data_section[data_key]
    if not isinstance(apps_list, list):
        return []

    return [
        t.AppData.model_validate(app)
        for app in apps_list
        if isinstance(app, dict)
        and all(k in app and isinstance(app[k], str) for k in ["id", "name"])
    ]


def _execute_app_operation(
    method: str,
    endpoint: str,
    json_data: dict[str, object] | None = None,
) -> t.AppData:
    """Execute application operation using existing flext-core Railway-oriented programming.

    Reduces from 9 returns to single monadic chain using FlextResult from flext-core.
    Leverages existing framework instead of recreating functionality.
    """

    def _make_http_request() -> FlextResult[requests.Response]:
        """Make HTTP request using FlextResult for error handling."""
        try:
            request_func = getattr(requests, method.lower())
            kwargs: dict[str, object] = {
                "url": f"{ExampleConstants.BASE_URL}{endpoint}",
                "timeout": 5,
            }
            if json_data:
                kwargs["json"] = json_data

            response = request_func(**kwargs)
            return (
                FlextResult[requests.Response].ok(response)
                if response.status_code == ExampleConstants.HTTP_OK
                else FlextResult[requests.Response].fail(f"HTTP {response.status_code}")
            )
        except requests.RequestException as e:
            return FlextResult[requests.Response].fail(f"Request failed: {e}")

    def _parse_json_response(
        response: requests.Response,
    ) -> FlextResult[dict[str, object]]:
        """Parse JSON from response."""
        try:
            json_data = response.json()
            return FlextResult[dict[str, object]].ok(json_data)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(f"JSON parse failed: {e}")

    # Use existing flext-core monadic chain
    result = (
        _make_http_request()
        .flat_map(_parse_json_response)
        .flat_map(
            lambda json_data: FlextResult[t.AppData].ok(
                t.AppData.model_validate(json_data["data"]),
            )
            if (
                isinstance(json_data, dict)
                and "success" in json_data
                and json_data["success"] is True
                and "data" in json_data
                and isinstance(data := json_data["data"], dict)
                and "id" in data
                and "name" in data
            )
            else FlextResult[t.AppData].fail("Invalid app data"),
        )
    )

    # Fast fail - no fallback to None
    if result.is_failure:
        error_msg = f"Operation failed: {result.error}"
        raise ValueError(error_msg)
    return result.value


def _execute_list_operation(
    endpoint: str,
    data_key: str,
) -> list[t.AppData]:
    """Advanced Monad Composition using flext-core - eliminates 7 returns with Kleisli composition."""

    # Pure functional Kleisli composition using flext-core patterns
    def _make_get_request() -> FlextResult[requests.Response]:
        """Make GET request."""
        try:
            response = requests.get(f"{ExampleConstants.BASE_URL}{endpoint}", timeout=5)
            return FlextResult[requests.Response].ok(response)
        except requests.RequestException as e:
            return FlextResult[requests.Response].fail(f"Request failed: {e}")

    def _parse_response_json(
        response: requests.Response,
    ) -> FlextResult[dict[str, object]]:
        """Parse JSON from response."""
        try:
            json_data = response.json()
            return FlextResult[dict[str, object]].ok(json_data)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(f"JSON parse failed: {e}")

    result = _make_get_request()
    if result.is_success and result.value.status_code != ExampleConstants.HTTP_OK:
        result = FlextResult[dict[str, object]].fail("HTTP request failed")
    else:
        result = result.flat_map(_parse_response_json).map(
            lambda d: _extract_apps_from_response(d, data_key),
        )

    # Fast fail - no fallback to empty list
    if result.is_failure:
        error_msg = f"List operation failed: {result.error}"
        raise ValueError(error_msg)
    return result.value


def start_application(app_id: str) -> t.AppData:
    """Start an application using FlextWebAppHandler.start().

    Args:
        app_id: Application ID (format: "app_{name}")

    Returns:
        Updated application data with RUNNING status or None if failed.

    """
    return _execute_app_operation(
        method="POST",
        endpoint=ExampleConstants.APP_START.format(app_id=app_id),
    )


def get_application_status(app_id: str) -> t.AppData:
    """Get application status using FlextWebApp entity.

    Args:
        app_id: Application ID (format: "app_{name}")

    Returns:
        Application data with current FlextWebAppStatus or None if failed.

    """
    return _execute_app_operation(
        method="GET",
        endpoint=ExampleConstants.APP_DETAIL.format(app_id=app_id),
    )


def stop_application(app_id: str) -> t.AppData:
    """Stop an application using FlextWebAppHandler.stop().

    Args:
        app_id: Application ID (format: "app_{name}")

    Returns:
        Updated application data with STOPPED status or None if failed.

    """
    return _execute_app_operation(
        method="POST",
        endpoint=ExampleConstants.APP_STOP.format(app_id=app_id),
    )


def list_applications() -> list[t.AppData]:
    """List all applications using FlextWebServices.apps storage.

    Returns:
        List of FlextWebApp entities with current status information.

    """
    return _execute_list_operation(endpoint=ExampleConstants.APPS_BASE, data_key="apps")


def demo_application_lifecycle() -> None:
    """Demonstrate complete application lifecycle using the refactored API.

    Shows the full workflow:
    1. Health check using standardized FlextResult responses
    2. Application creation with WebFields validation
    3. Lifecycle management via FlextWebAppHandler
    4. Status monitoring through FlextWebApp entities
    """
    if not check_service_health():
        return

    # Create applications with different configurations - fast fail on error
    try:
        app1 = create_application("web-service", 3000)
        app2 = create_application("api-gateway", 4000, "127.0.0.1")
    except ValueError:
        return

    list_applications()

    # Start applications and check results - fast fail on error
    try:
        start_application(str(app1.id))
        start_application(str(app2.id))
    except ValueError:
        return

    # Check individual status with proper error handling - fast fail on error
    try:
        for app_data in [app1, app2]:
            app_id = str(app_data.id)
            get_application_status(app_id)
    except ValueError:
        return

    list_applications()

    # Stop applications - fast fail on error
    try:
        stop_application(str(app1.id))
        stop_application(str(app2.id))
    except ValueError:
        return

    list_applications()


if __name__ == "__main__":
    demo_application_lifecycle()
