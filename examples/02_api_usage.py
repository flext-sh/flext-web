"""FLEXT Web Interface - API Usage Example.

Demonstrates how to interact with the FLEXT Web Interface REST API
for application lifecycle management using the refactored architecture.

This example shows:
- Health check against the running web service
- Application lifecycle management
- Error handling with r patterns
- Usage of new type aliases for better type safety
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import requests
from flext_core import r

from flext_web import t


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
        result: Mapping[str, t.ContainerValue] = response.json()
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
    """Create a new application through the web API.

    Args:
        name: Application name (must follow service validation)
        port: Port number (1-65535 range)
        host: Host address (default: localhost)

    Returns:
        Application data validated into `t.AppData`.

    Raises:
        ValueError: If application creation fails.

    """
    request_data: Mapping[str, str | int] = {"name": name, "port": port, "host": host}

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
    ) -> r[Mapping[str, t.ContainerValue]]:
        """Parse JSON response."""
        try:
            json_data: Mapping[str, t.ContainerValue] = response.json()
            return r[t.ContainerValueMapping].ok(json_data)
        except Exception as e:
            return r[t.ContainerValueMapping].fail(f"JSON parse failed: {e}")

    result = _make_request()
    if result.is_success and result.value.status_code != ExampleConstants.HTTP_OK:
        msg = "HTTP request failed"
        raise ValueError(msg)
    parsed_result = result.flat_map(_parse_json)
    if parsed_result.is_failure:
        raise ValueError(parsed_result.error or "Parse failed")
    json_data: Mapping[str, t.ContainerValue] = parsed_result.value
    if (
        json_data.get("success")
        and isinstance((data := json_data.get("data")), dict)
        and ("id" in data)
        and ("name" in data)
    ):
        return t.AppData.model_validate(json_data["data"])
    msg = "Invalid application data"
    raise ValueError(msg)


def _extract_apps_from_response(
    response_data: Mapping[str, t.ContainerValue] | t.ContainerValue,
    data_key: str,
) -> Sequence[t.AppData]:
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
                result_list.append(t.AppData.model_validate(app_item))
        except (ValueError, TypeError):
            continue
    return result_list


def _execute_app_operation(
    method: str,
    endpoint: str,
    json_data: Mapping[str, t.ContainerValue] | None = None,
) -> t.AppData:
    """Execute application operation using existing flext-core Railway-oriented programming.

    Reduces from 9 returns to single monadic chain using r from flext-core.
    Leverages existing framework instead of recreating functionality.
    """

    def _make_http_request() -> r[requests.Response]:
        """Make HTTP request using r for error handling."""
        try:
            request_func = getattr(requests, method.lower())
            kwargs: dict[str, t.ContainerValue] = {
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
    ) -> r[Mapping[str, t.ContainerValue]]:
        """Parse JSON from response."""
        try:
            json_data: Mapping[str, t.ContainerValue] = response.json()
            return r[t.ContainerValueMapping].ok(json_data)
        except Exception as e:
            return r[t.ContainerValueMapping].fail(f"JSON parse failed: {e}")

    result = (
        _make_http_request()
        .flat_map(_parse_json_response)
        .flat_map(
            lambda json_data: (
                r[t.AppData].ok(t.AppData.model_validate(json_data["data"]))
                if "success" in json_data
                and json_data["success"] is True
                and ("data" in json_data)
                and isinstance((data := json_data["data"]), dict)
                and ("id" in data)
                and ("name" in data)
                else r[t.AppData].fail("Invalid app data")
            ),
        )
    )
    if result.is_failure:
        error_msg = f"Operation failed: {result.error}"
        raise ValueError(error_msg)
    return result.value


def _execute_list_operation(endpoint: str, data_key: str) -> Sequence[t.AppData]:
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
    ) -> r[Mapping[str, t.ContainerValue]]:
        """Parse JSON from response."""
        try:
            json_data: Mapping[str, t.ContainerValue] = response.json()
            return r[t.ContainerValueMapping].ok(json_data)
        except Exception as e:
            return r[t.ContainerValueMapping].fail(f"JSON parse failed: {e}")

    result = _make_get_request()
    if result.is_success and result.value.status_code != ExampleConstants.HTTP_OK:
        msg = "HTTP request failed"
        raise ValueError(msg)
    parsed_result = result.flat_map(_parse_response_json)
    if parsed_result.is_failure:
        raise ValueError(parsed_result.error or "Parse failed")
    response_dict: Mapping[str, t.ContainerValue] = parsed_result.value
    apps_list: Sequence[t.AppData] = _extract_apps_from_response(
        response_dict,
        data_key,
    )
    return apps_list


def start_application(app_id: str) -> t.AppData:
    """Start an application through the web API.

    Args:
        app_id: Application ID.

    Returns:
        Updated application data validated into `t.AppData`.

    """
    return _execute_app_operation(
        method="POST",
        endpoint=ExampleConstants.APP_START.format(app_id=app_id),
    )


def get_application_status(app_id: str) -> t.AppData:
    """Get application status through the web API.

    Args:
        app_id: Application ID.

    Returns:
        Application data validated into `t.AppData`.

    """
    return _execute_app_operation(
        method="GET",
        endpoint=ExampleConstants.APP_DETAIL.format(app_id=app_id),
    )


def stop_application(app_id: str) -> t.AppData:
    """Stop an application through the web API.

    Args:
        app_id: Application ID.

    Returns:
        Updated application data validated into `t.AppData`.

    """
    return _execute_app_operation(
        method="POST",
        endpoint=ExampleConstants.APP_STOP.format(app_id=app_id),
    )


def list_applications() -> Sequence[t.AppData]:
    """List all applications available through the web API.

    Returns:
        List of validated `t.AppData` payloads.

    """
    return _execute_list_operation(endpoint=ExampleConstants.APPS_BASE, data_key="apps")


def demo_application_lifecycle() -> None:
    """Demonstrate complete lifecycle usage through the public REST API.

    Shows the full workflow:
    1. Health check over HTTP
    2. Application creation through REST endpoints
    3. Lifecycle management through REST endpoints
    4. Response validation into `t.AppData`
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
