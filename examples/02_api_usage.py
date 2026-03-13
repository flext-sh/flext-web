"""FLEXT Web Interface - API Usage Example.

Demonstrates how to interact with the FLEXT Web Interface REST API
for application lifecycle management using the refactored architecture.

This example shows:
- Health check using WebHandlers
- Application lifecycle management
- Error handling with r patterns
- Usage of new type aliases for better type safety
"""

from __future__ import annotations

import requests
from flext_core import r

from flext_web import t
from flext_web.protocols import ResponseDict


class ExampleConstants:
    """Consolidated constants for API usage example following flext-core patterns."""

    HTTP_OK = 200
    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = 8080
    BASE_URL = f"http://{DEFAULT_HOST}:{DEFAULT_PORT}"
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
        result: dict[str, object] = response.json()
        success_value = result.get("success")
        data_value = result.get("data")
        if not isinstance(data_value, dict):
            return False
        status_value = data_value.get("status")
        return (
            success_value is True and "data" in result and (status_value == "healthy")
        )
    except (requests.RequestException, ValueError):
        return False


def create_application(name: str, port: int, host: str = "localhost") -> t.AppData:
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

    def _make_request() -> r[requests.Response]:
        """Make HTTP request using r for error handling."""
        try:
            response = requests.post(
                f"{ExampleConstants.BASE_URL}{ExampleConstants.APPS_BASE}",
                json=request_data,
                timeout=5,
            )
            return r[requests.Response].ok(response)
        except requests.RequestException as e:
            return r[requests.Response].fail(f"Request failed: {e}")

    def _parse_json(
        response: requests.Response,
    ) -> r[dict[str, object]]:
        """Parse JSON response."""
        try:
            json_data: dict[str, object] = response.json()
            return r[object].ok(json_data)
        except Exception as e:
            return r[object].fail(f"JSON parse failed: {e}")

    result = _make_request()
    if result.is_success and result.value.status_code != ExampleConstants.HTTP_OK:
        msg = "HTTP request failed"
        raise ValueError(msg)
    parsed_result = result.flat_map(_parse_json)
    if parsed_result.is_failure:
        raise ValueError(parsed_result.error or "Parse failed")
    json_data: dict[str, object] = parsed_result.value
    if (
        json_data.get("success")
        and isinstance((data := json_data.get("data")), dict)
        and ("id" in data)
        and ("name" in data)
    ):
        app_obj: t.AppData = t.AppData(json_data["data"])
        return app_obj
    msg = "Invalid application data"
    raise ValueError(msg)


def _extract_apps_from_response(
    response_data: ResponseDict | object, data_key: str
) -> list[t.AppData]:
    """Extract apps list from response data with proper type checking."""
    if not isinstance(response_data, dict):
        return []
    data_section = response_data.get("data")
    if not isinstance(data_section, dict):
        return []
    apps_section = data_section.get(data_key)
    if not isinstance(apps_section, list):
        return []
    result_list: list[t.AppData] = []
    for app_item in apps_section:
        try:
            if isinstance(app_item, dict):
                result_list.append(t.AppData(app_item))
        except Exception:
            continue
    return result_list


def _execute_app_operation(
    method: str, endpoint: str, json_data: dict[str, object] | None = None
) -> t.AppData:
    """Execute application operation using existing flext-core Railway-oriented programming.

    Reduces from 9 returns to single monadic chain using r from flext-core.
    Leverages existing framework instead of recreating functionality.
    """

    def _make_http_request() -> r[requests.Response]:
        """Make HTTP request using r for error handling."""
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
                r[requests.Response].ok(response)
                if response.status_code == ExampleConstants.HTTP_OK
                else r[requests.Response].fail(f"HTTP {response.status_code}")
            )
        except requests.RequestException as e:
            return r[requests.Response].fail(f"Request failed: {e}")

    def _parse_json_response(
        response: requests.Response,
    ) -> r[dict[str, object]]:
        """Parse JSON from response."""
        try:
            json_data: dict[str, object] = response.json()
            return r[object].ok(json_data)
        except Exception as e:
            return r[object].fail(f"JSON parse failed: {e}")

    result = (
        _make_http_request()
        .flat_map(_parse_json_response)
        .flat_map(
            lambda json_data: (
                r[t.AppData].ok(t.AppData(json_data["data"]))
                if "success" in json_data
                and json_data["success"] is True
                and ("data" in json_data)
                and isinstance((data := json_data["data"]), dict)
                and ("id" in data)
                and ("name" in data)
                else r[t.AppData].fail("Invalid app data")
            )
        )
    )
    if result.is_failure:
        error_msg = f"Operation failed: {result.error}"
        raise ValueError(error_msg)
    return result.value


def _execute_list_operation(endpoint: str, data_key: str) -> list[t.AppData]:
    """Advanced Monad Composition using flext-core - eliminates 7 returns with Kleisli composition."""

    def _make_get_request() -> r[requests.Response]:
        """Make GET request."""
        try:
            response = requests.get(f"{ExampleConstants.BASE_URL}{endpoint}", timeout=5)
            return r[requests.Response].ok(response)
        except requests.RequestException as e:
            return r[requests.Response].fail(f"Request failed: {e}")

    def _parse_response_json(
        response: requests.Response,
    ) -> r[dict[str, object]]:
        """Parse JSON from response."""
        try:
            json_data: dict[str, object] = response.json()
            return r[object].ok(json_data)
        except Exception as e:
            return r[object].fail(f"JSON parse failed: {e}")

    result = _make_get_request()
    if result.is_success and result.value.status_code != ExampleConstants.HTTP_OK:
        msg = "HTTP request failed"
        raise ValueError(msg)
    parsed_result = result.flat_map(_parse_response_json)
    if parsed_result.is_failure:
        raise ValueError(parsed_result.error or "Parse failed")
    response_dict: dict[str, object] = parsed_result.value
    apps_list: list[t.AppData] = _extract_apps_from_response(response_dict, data_key)
    return apps_list


def start_application(app_id: str) -> t.AppData:
    """Start an application using FlextWebAppHandler.start().

    Args:
        app_id: Application ID (format: "app_{name}")

    Returns:
        Updated application data with RUNNING status or None if failed.

    """
    return _execute_app_operation(
        method="POST", endpoint=ExampleConstants.APP_START.format(app_id=app_id)
    )


def get_application_status(app_id: str) -> t.AppData:
    """Get application status using FlextWebApp entity.

    Args:
        app_id: Application ID (format: "app_{name}")

    Returns:
        Application data with current FlextWebAppStatus or None if failed.

    """
    return _execute_app_operation(
        method="GET", endpoint=ExampleConstants.APP_DETAIL.format(app_id=app_id)
    )


def stop_application(app_id: str) -> t.AppData:
    """Stop an application using FlextWebAppHandler.stop().

    Args:
        app_id: Application ID (format: "app_{name}")

    Returns:
        Updated application data with STOPPED status or None if failed.

    """
    return _execute_app_operation(
        method="POST", endpoint=ExampleConstants.APP_STOP.format(app_id=app_id)
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
    1. Health check using standardized r responses
    2. Application creation with WebFields validation
    3. Lifecycle management via FlextWebAppHandler
    4. Status monitoring through FlextWebApp entities
    """
    if not check_service_health():
        return
    try:
        app1 = create_application("web-service", 3000)
        app2 = create_application("api-gateway", 4000, "127.0.0.1")
    except ValueError:
        return
    _ = list_applications()
    try:
        _ = start_application(str(app1.id))
        _ = start_application(str(app2.id))
    except ValueError:
        return
    try:
        for app_data in [app1, app2]:
            app_id = str(app_data.id)
            _ = get_application_status(app_id)
    except ValueError:
        return
    _ = list_applications()
    try:
        _ = stop_application(str(app1.id))
        _ = stop_application(str(app2.id))
    except ValueError:
        return
    _ = list_applications()


if __name__ == "__main__":
    demo_application_lifecycle()
