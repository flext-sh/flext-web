"""Tests for API functionality."""

from __future__ import annotations

from flext_web.api import WebAPI


class TestWebAPI:
    """Test WebAPI functionality."""

    def test_api_creation(self) -> None:
        """Test API creation."""
        api = WebAPI()

        assert api.app is not None
        assert api._apps == {}
        assert api._handler is not None

    def test_health_check(self) -> None:
        """Test health check endpoint."""
        api = WebAPI()

        with api.app.test_client() as client:
            response = client.get("/health")

            assert response.status_code == 200
            data = response.get_json()
            assert data["success"] is True
            assert "healthy" in data["message"]

    def test_list_apps_empty(self) -> None:
        """Test listing empty apps."""
        api = WebAPI()

        with api.app.test_client() as client:
            response = client.get("/api/v1/apps")

            assert response.status_code == 200
            data = response.get_json()
            assert data["success"] is True
            assert data["data"]["apps"] == []

    def test_create_app(self) -> None:
        """Test creating an app."""
        api = WebAPI()

        with api.app.test_client() as client:
            response = client.post("/api/v1/apps", json={
                "name": "TestApp",
                "port": 8080
            })

            assert response.status_code == 200
            data = response.get_json()
            assert data["success"] is True
            assert data["data"]["name"] == "TestApp"
            assert data["data"]["port"] == 8080

    def test_create_app_missing_name(self) -> None:
        """Test creating app with missing name."""
        api = WebAPI()

        with api.app.test_client() as client:
            response = client.post("/api/v1/apps", json={
                "port": 8080
            })

            assert response.status_code == 400
            data = response.get_json()
            assert data["success"] is False
            assert "App name is required" in data["message"]
