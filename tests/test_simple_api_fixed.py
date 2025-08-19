"""FLEXT Web Interface - REST API Integration Testing Suite.

Enterprise-grade test suite for REST API endpoints, HTTP request/response handling,
and service integration patterns. Ensures API follows enterprise standards with
proper error handling, validation, and response formatting.

Test Coverage:
    - REST API endpoint functionality and response validation
    - HTTP status code handling and error responses
    - JSON request/response serialization and validation
    - Application lifecycle management through API
    - Health check and monitoring endpoint validation

Integration:
    - Tests Flask integration with enterprise patterns
    - Validates FlextWebService API endpoint implementation
    - Ensures proper error handling and response formatting
    - Verifies CQRS handler integration through API layer

Author: FLEXT Development Team
Version: 0.9.0
Status: Enterprise API testing with comprehensive HTTP validation
"""

from __future__ import annotations

from flext_web import create_service
from flext_web.constants import FlextWebConstants

# Constants - Using refactored constants
HTTP_OK = FlextWebConstants.HTTP.OK
EXPECTED_TOTAL_PAGES = 8


class TestFlextWebService:
    """Enterprise REST API testing for FlextWebService functionality.

    Comprehensive test suite covering REST API endpoint implementation,
    HTTP request/response handling, and service integration patterns.
    Ensures API follows enterprise standards with proper validation.
    """

    def test_service_creation(self) -> None:
        """Test FlextWebService creation with proper initialization.

        Validates that service instance creates successfully with Flask
        application, route registration, and handler initialization.
        Tests fundamental service patterns used in enterprise deployment.
        """
        service = create_service()

        assert service.app is not None
        if service.apps != {}:
            msg: str = f"Expected {{}}, got {service.apps}"
            raise AssertionError(msg)
        assert service.handler is not None

    def test_health_check(self) -> None:
        """Test health check endpoint."""
        service = create_service()

        with service.app.test_client() as client:
            response = client.get("/health")

            if response.status_code != HTTP_OK:
                msg: str = f"Expected {200}, got {response.status_code}"
                raise AssertionError(msg)
            data = response.get_json()
            if not (data["success"]):
                msg: str = f"Expected True, got {data['success']}"
                raise AssertionError(msg)
            if "healthy" not in data["message"]:
                msg: str = f"Expected {'healthy'} in {data['message']}"
                raise AssertionError(msg)

    def test_list_apps_empty(self) -> None:
        """Test listing empty apps."""
        service = create_service()

        with service.app.test_client() as client:
            response = client.get("/api/v1/apps")

            if response.status_code != HTTP_OK:
                msg: str = f"Expected {200}, got {response.status_code}"
                raise AssertionError(msg)
            data = response.get_json()
            if not (data["success"]):
                msg: str = f"Expected True, got {data['success']}"
                raise AssertionError(msg)
            if data["data"]["apps"] != []:
                msg: str = f"Expected {[]}, got {data['data']['apps']}"
                raise AssertionError(msg)

    def test_create_app(self) -> None:
        """Test creating an app."""
        service = create_service()

        with service.app.test_client() as client:
            response = client.post(
                "/api/v1/apps",
                json={
                    "name": "TestApp",
                    "port": 8080,
                },
            )

            if response.status_code != HTTP_OK:
                msg: str = f"Expected {200}, got {response.status_code}"
                raise AssertionError(msg)
            data = response.get_json()
            if not (data["success"]):
                msg: str = f"Expected True, got {data['success']}"
                raise AssertionError(msg)
            if data["data"]["name"] != "TestApp":
                msg: str = f"Expected {'TestApp'}, got {data['data']['name']}"
                raise AssertionError(
                    msg,
                )
            assert data["data"]["port"] == 8080

    def test_create_app_missing_name(self) -> None:
        """Test creating app with missing name."""
        service = create_service()

        with service.app.test_client() as client:
            response = client.post(
                "/api/v1/apps",
                json={
                    "port": 8080,
                },
            )

            if response.status_code != 400:
                msg: str = f"Expected {400}, got {response.status_code}"
                raise AssertionError(msg)
            data = response.get_json()
            if data["success"]:
                msg: str = f"Expected False, got {data['success']}"
                raise AssertionError(msg)
            assert "App name is required" in data["message"]
