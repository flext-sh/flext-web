"""Tests for web interface functionality."""

from __future__ import annotations

from flext_web.api import create_app


class TestWebInterface:
    """Test web interface functionality."""

    def test_create_app_factory(self) -> None:
        """Test create_app factory function."""
        app = create_app()

        assert app is not None
        assert app.name == "flext_web.api"

    def test_dashboard_route(self) -> None:
        """Test dashboard route."""
        app = create_app()

        with app.test_client() as client:
            response = client.get("/")

            assert response.status_code == 200
            assert b"FLEXT Web Dashboard" in response.data
            assert b"Clean Architecture" in response.data
