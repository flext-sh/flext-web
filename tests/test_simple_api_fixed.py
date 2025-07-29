"""Tests for API functionality."""

from __future__ import annotations

from flext_web.api import WebAPI


# Constants
HTTP_OK = 200
EXPECTED_TOTAL_PAGES = 8

class TestWebAPI:
    """Test WebAPI functionality."""

    def test_api_creation(self) -> None:
        """Test API creation."""
        api = WebAPI()

        assert api.app is not None
        if api._apps != {}:
            raise AssertionError(f"Expected {{}}, got {api._apps}")
        assert api._handler is not None

    def test_health_check(self) -> None:
        """Test health check endpoint."""
        api = WebAPI()

        with api.app.test_client() as client:
            response = client.get("/health")

            if response.status_code != HTTP_OK:

                raise AssertionError(f"Expected {200}, got {response.status_code}")
            data = response.get_json()
            if not (data["success"]):
                raise AssertionError(f"Expected True, got {data["success"]}")
            if "healthy" not in data["message"]:
                raise AssertionError(f"Expected {"healthy"} in {data["message"]}")

    def test_list_apps_empty(self) -> None:
        """Test listing empty apps."""
        api = WebAPI()

        with api.app.test_client() as client:
            response = client.get("/api/v1/apps")

            if response.status_code != HTTP_OK:

                raise AssertionError(f"Expected {200}, got {response.status_code}")
            data = response.get_json()
            if not (data["success"]):
                raise AssertionError(f"Expected True, got {data["success"]}")
            if data["data"]["apps"] != []:
                raise AssertionError(f"Expected {[]}, got {data["data"]["apps"]}")

    def test_create_app(self) -> None:
        """Test creating an app."""
        api = WebAPI()

        with api.app.test_client() as client:
            response = client.post("/api/v1/apps", json={
                "name": "TestApp",
                "port": 8080,
            })

            if response.status_code != HTTP_OK:

                raise AssertionError(f"Expected {200}, got {response.status_code}")
            data = response.get_json()
            if not (data["success"]):
                raise AssertionError(f"Expected True, got {data["success"]}")
            if data["data"]["name"] != "TestApp":
                raise AssertionError(f"Expected {"TestApp"}, got {data["data"]["name"]}")
            assert data["data"]["port"] == 8080

    def test_create_app_missing_name(self) -> None:
        """Test creating app with missing name."""
        api = WebAPI()

        with api.app.test_client() as client:
            response = client.post("/api/v1/apps", json={
                "port": 8080,
            })

            if response.status_code != 400:

                raise AssertionError(f"Expected {400}, got {response.status_code}")
            data = response.get_json()
            if data["success"]:
                raise AssertionError(f"Expected False, got {data["success"]}")\ n            assert "App name is required" in data["message"]
