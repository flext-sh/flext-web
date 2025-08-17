#!/usr/bin/env python3
"""FLEXT Web Interface - API Usage Example.

Demonstrates how to interact with the FLEXT Web Interface REST API
for application lifecycle management.
"""

import requests
from flext_core import FlextConstants

# Constants for HTTP status codes
HTTP_OK = 200
BASE_URL = f"http://{FlextConstants.Platform.DEFAULT_HOST}:{FlextConstants.Platform.FLEXCORE_PORT}"


def check_service_health() -> bool | None:
    """Check if the service is running and healthy."""
    try:
      response = requests.get(f"{BASE_URL}/health", timeout=5)
      if response.status_code == HTTP_OK:
          response.json()
          return True
      return False
    except requests.RequestException:
      return False


def create_application(
    name: str,
    port: int,
    host: str = "localhost",
) -> dict[str, object] | None | bool:
    """Create a new application."""
    data = {"name": name, "port": port, "host": host}

    try:
      response = requests.post(f"{BASE_URL}/api/v1/apps", json=data, timeout=5)
      if response.status_code == HTTP_OK:
          return response.json()["data"]
      response.json()
      return None
    except requests.RequestException:
      return None


def start_application(app_id: str) -> dict[str, object] | None | bool:
    """Start an application."""
    try:
      response = requests.post(f"{BASE_URL}/api/v1/apps/{app_id}/start", timeout=5)
      if response.status_code == HTTP_OK:
          return response.json()["data"]
      response.json()
      return None
    except requests.RequestException:
      return None


def get_application_status(app_id: str) -> dict[str, object] | None | bool:
    """Get application status."""
    try:
      response = requests.get(f"{BASE_URL}/api/v1/apps/{app_id}", timeout=5)
      if response.status_code == HTTP_OK:
          return response.json()["data"]
      return None
    except requests.RequestException:
      return None


def stop_application(app_id: str) -> dict[str, object] | None | bool:
    """Stop an application."""
    try:
      response = requests.post(f"{BASE_URL}/api/v1/apps/{app_id}/stop", timeout=5)
      if response.status_code == HTTP_OK:
          return response.json()["data"]
      response.json()
      return None
    except requests.RequestException:
      return None


def list_applications() -> list[dict[str, object]]:
    """List all applications."""
    try:
      response = requests.get(f"{BASE_URL}/api/v1/apps", timeout=5)
      if response.status_code == HTTP_OK:
          data = response.json()["data"]
          apps = data["apps"]
          for app in apps:
              "🟢" if app["is_running"] else "🔴"
          return apps
      response.json()
      return []
    except requests.RequestException:
      return []


def demo_application_lifecycle() -> None:
    """Demonstrate complete application lifecycle."""
    # Check service health
    if not check_service_health():
      return

    # Create applications
    app1 = create_application("web-service", 3000)
    app2 = create_application("api-gateway", 4000, "127.0.0.1")

    if not app1 or not app2:
      return

    # List applications
    list_applications()

    # Start applications
    start_application(app1["id"])
    start_application(app2["id"])

    # Check status
    for app_id in [app1["id"], app2["id"]]:
      status = get_application_status(app_id)
      if status:
          "🟢" if status["is_running"] else "🔴"

    # List applications again
    list_applications()

    # Stop applications
    stop_application(app1["id"])
    stop_application(app2["id"])

    # Final status
    list_applications()


if __name__ == "__main__":
    demo_application_lifecycle()
