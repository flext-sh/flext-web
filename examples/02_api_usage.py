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

from typing import cast

import requests
from flext_core import FlextResult

from flext_web import FlextWebTypes


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
        if response.status_code == ExampleConstants.HTTP_OK:
            result = response.json()
            # Check the standardized response format
            if result.get("success", False):
                data = result.get("data")
                if isinstance(data, dict):
                    return data.get("status") == "healthy"
        return False
    except requests.RequestException:
        return False


def create_application(
    name: str,
    port: int,
    host: str = "localhost",
) -> FlextWebTypes.AppData | None:
    """Create a new application using WebHandlers.

    Args:
        name: Application name (must follow WebFields validation)
        port: Port number (1-65535 range)
        host: Host address (default: localhost)

    Returns:
        Application data from FlextWebApp model or None if failed.

    """
    request_data: dict[str, str | int] = {"name": name, "port": port, "host": host}

    try:
        response = requests.post(
            f"{ExampleConstants.BASE_URL}{ExampleConstants.APPS_BASE}",
            json=request_data,
            timeout=5,
        )
        if response.status_code == ExampleConstants.HTTP_OK:
            result = response.json()
            if result.get("success"):
                data = result.get("data")

                if isinstance(data, dict) and "id" in data and "name" in data:
                    return cast("FlextWebTypes.AppData", data)
                return None
        return None
    except requests.RequestException:
        return None


def _extract_apps_from_response(
    response_data: object,
    data_key: str,
) -> list[FlextWebTypes.AppData]:
    """Extract apps list from response data with proper type checking."""
    if not isinstance(response_data, dict):
        return []

    data_section = response_data.get("data")
    if not isinstance(data_section, dict):
        return []

    apps_list = data_section.get(data_key)
    if not isinstance(apps_list, list):
        return []

    return [
        cast("FlextWebTypes.AppData", app)
        for app in apps_list
        if isinstance(app, dict)
        and all(k in app and isinstance(app[k], str) for k in ["id", "name"])
    ]


def _execute_app_operation(
    method: str,
    endpoint: str,
    json_data: dict[str, object] | None = None,
) -> FlextWebTypes.AppData | None:
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

    # Use existing flext-core monadic chain
    result = (
        _make_http_request()
        .flat_map(
            lambda resp: FlextResult[dict[str, object]].ok(resp.json())
            if resp.status_code == ExampleConstants.HTTP_OK
            else FlextResult[dict[str, object]].fail("Invalid response"),
        )
        .flat_map(
            lambda json_data: FlextResult[FlextWebTypes.AppData].ok(
                cast("FlextWebTypes.AppData", json_data["data"]),
            )
            if all(
                [
                    json_data.get("success"),
                    isinstance(data := json_data.get("data"), dict),
                    data
                    and {"id", "name"}.issubset(
                        cast("dict[str, object]", data).keys(),
                    ),
                ],
            )
            else FlextResult[FlextWebTypes.AppData].fail("Invalid app data"),
        )
    )

    return result.value if result.is_success else None


def _execute_list_operation(
    endpoint: str,
    data_key: str,
) -> list[FlextWebTypes.AppData]:
    """Advanced Monad Composition using flext-core - eliminates 7 returns with Kleisli composition."""
    # Pure functional Kleisli composition using flext-core patterns
    return (
        FlextResult.safe_call(
            lambda: requests.get(f"{ExampleConstants.BASE_URL}{endpoint}", timeout=5),
        )
        .filter(
            lambda r: r.status_code == ExampleConstants.HTTP_OK,
            "HTTP request failed",
        )
        .flat_map(
            lambda r: FlextResult.safe_call(r.json)
            if hasattr(r, "json")
            else FlextResult[dict[str, object]].fail("Invalid response object"),
        )
        .map(lambda d: _extract_apps_from_response(d, data_key))
        .unwrap_or([])
    )


def start_application(app_id: str) -> FlextWebTypes.AppData | None:
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


def get_application_status(app_id: str) -> FlextWebTypes.AppData | None:
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


def stop_application(app_id: str) -> FlextWebTypes.AppData | None:
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


def list_applications() -> list[FlextWebTypes.AppData]:
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

    # Create applications with different configurations
    app1 = create_application("web-service", 3000)
    app2 = create_application("api-gateway", 4000, "127.0.0.1")

    if not app1 or not app2:
        return

    list_applications()

    # Start applications and check results
    start_result1 = start_application(str(app1["id"]))
    start_result2 = start_application(str(app2["id"]))

    if start_result1:
        print(f"✅ Application {app1['name']} started successfully")
    else:
        print(f"❌ Failed to start application {app1['name']}")

    if start_result2:
        print(f"✅ Application {app2['name']} started successfully")
    else:
        print(f"❌ Failed to start application {app2['name']}")

    # Check individual status with proper error handling
    for app_data in [app1, app2]:
        app_id: str = str(app_data["id"])
        status: FlextWebTypes.AppData | None = get_application_status(app_id)
        if status:
            "🟢" if status.get("is_running") else "🔴"

    list_applications()

    # Stop applications
    stop_result1 = stop_application(str(app1["id"]))
    stop_result2 = stop_application(str(app2["id"]))

    if stop_result1:
        print(f"✅ Application {app1['name']} stopped successfully")
    else:
        print(f"❌ Failed to stop application {app1['name']}")

    if stop_result2:
        print(f"✅ Application {app2['name']} stopped successfully")
    else:
        print(f"❌ Failed to stop application {app2['name']}")

    list_applications()


if __name__ == "__main__":
    demo_application_lifecycle()
