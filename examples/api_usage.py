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
from flext_core import FlextConstants

from flext_web.typings import FlextWebTypes

# Constants for HTTP status codes
HTTP_OK = FlextConstants.Web.HTTP_OK
DEFAULT_HOST = FlextConstants.Infrastructure.DEFAULT_HOST
DEFAULT_PORT = FlextConstants.Web.DEFAULT_DEVELOPMENT_PORT
BASE_URL = f"http://{DEFAULT_HOST}:{DEFAULT_PORT}"


def check_service_health() -> bool:
    """Check if the service is running and healthy.

    Uses the /health endpoint that returns standardized FlextResult format.

    Returns:
        True if service is healthy, False otherwise.

    """
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == HTTP_OK:
            health_data = cast("FlextWebTypes.HealthResponseDict", response.json())
            # Check the standardized response format
            return (
                health_data.get("success", False)
                and health_data.get("data", {}).get("status") == "healthy"
            )
        return False
    except requests.RequestException:
        return False


def create_application(
    name: str,
    port: int,
    host: str = "localhost",
) -> FlextWebTypes.AppDataDict | None:
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
            f"{BASE_URL}{FlextConstants.Endpoints.APPS_BASE}",
            json=request_data,
            timeout=5,
        )
        if response.status_code == HTTP_OK:
            result = cast("FlextWebTypes.ApiResponseDict", response.json())
            if result.get("success"):
                data = result.get("data")
                # Type guard: ensure we return AppDataDict
                if isinstance(data, dict) and "id" in data and "name" in data:
                    return cast("FlextWebTypes.AppDataDict", data)
                return None
        return None
    except requests.RequestException:
        return None


def start_application(app_id: str) -> FlextWebTypes.AppDataDict | None:
    """Start an application using FlextWebAppHandler.start().

    Args:
        app_id: Application ID (format: "app_{name}")

    Returns:
        Updated application data with RUNNING status or None if failed.

    """
    try:
        response = requests.post(
            f"{BASE_URL}{FlextConstants.Endpoints.APP_START.format(app_id=app_id)}",
            timeout=5,
        )
        if response.status_code == HTTP_OK:
            result = cast("FlextWebTypes.ApiResponseDict", response.json())
            if result.get("success"):
                data = result.get("data")
                # Type guard: ensure we return AppDataDict
                if isinstance(data, dict) and "id" in data and "name" in data:
                    return cast("FlextWebTypes.AppDataDict", data)
                return None
        return None
    except requests.RequestException:
        return None


def get_application_status(app_id: str) -> FlextWebTypes.AppDataDict | None:
    """Get application status using FlextWebApp entity.

    Args:
        app_id: Application ID (format: "app_{name}")

    Returns:
        Application data with current FlextWebAppStatus or None if failed.

    """
    try:
        response = requests.get(
            f"{BASE_URL}{FlextConstants.Endpoints.APP_DETAIL.format(app_id=app_id)}",
            timeout=5,
        )
        if response.status_code == HTTP_OK:
            result = cast("FlextWebTypes.ApiResponseDict", response.json())
            if result.get("success"):
                data = result.get("data")
                # Type guard: ensure we return AppDataDict
                if isinstance(data, dict) and "id" in data and "name" in data:
                    return cast("FlextWebTypes.AppDataDict", data)
                return None
        return None
    except requests.RequestException:
        return None


def stop_application(app_id: str) -> FlextWebTypes.AppDataDict | None:
    """Stop an application using FlextWebAppHandler.stop().

    Args:
        app_id: Application ID (format: "app_{name}")

    Returns:
        Updated application data with STOPPED status or None if failed.

    """
    try:
        response = requests.post(
            f"{BASE_URL}{FlextConstants.Endpoints.APP_STOP.format(app_id=app_id)}",
            timeout=5,
        )
        if response.status_code == HTTP_OK:
            result = cast("FlextWebTypes.ApiResponseDict", response.json())
            if result.get("success"):
                data = result.get("data")
                # Type guard: ensure we return AppDataDict
                if isinstance(data, dict) and "id" in data and "name" in data:
                    return cast("FlextWebTypes.AppDataDict", data)
                return None
        return None
    except requests.RequestException:
        return None


def list_applications() -> list[FlextWebTypes.AppDataDict]:
    """List all applications using FlextWebService.apps storage.

    Returns:
        List of FlextWebApp entities with current status information.

    """
    try:
        response = requests.get(
            f"{BASE_URL}{FlextConstants.Endpoints.APPS_BASE}", timeout=5
        )
        if response.status_code == HTTP_OK:
            result = cast("FlextWebTypes.AppListResponseDict", response.json())
            if result.get("success"):
                data = result.get("data")
                if data:
                    apps = data.get("apps", [])
                    # Type guard and display status with proper emoji indicators
                    validated_apps: list[FlextWebTypes.AppDataDict] = []
                    for app in apps:
                        if isinstance(app, dict) and "id" in app and "name" in app:
                            "🟢" if app.get("is_running") else "🔴"
                            validated_apps.append(app)
                    return validated_apps
        return []
    except requests.RequestException:
        return []


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
    start_result1 = start_application(app1["id"])
    start_result2 = start_application(app2["id"])

    if start_result1:
        pass
    if start_result2:
        pass

    # Check individual status with proper error handling
    for app_data in [app1, app2]:
        app_id: str = app_data["id"]
        status: FlextWebTypes.AppDataDict | None = get_application_status(app_id)
        if status:
            "🟢" if status.get("is_running") else "🔴"

    list_applications()

    # Stop applications
    stop_result1 = stop_application(app1["id"])
    stop_result2 = stop_application(app2["id"])

    if stop_result1:
        pass
    if stop_result2:
        pass

    list_applications()


if __name__ == "__main__":
    demo_application_lifecycle()
