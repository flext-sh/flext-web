"""Tests for web interface functionality."""

from __future__ import annotations

from flext_web.api import create_app

# Constants
HTTP_OK = 200


class TestWebInterface:
    """Test web interface functionality."""

    def test_create_app_factory(self) -> None:
        """Test create_app factory function."""
        app = create_app()

        assert app is not None
        if app.name != "flext_web.api":
            msg = f"Expected {"flext_web.api"}, got {app.name}"
            raise AssertionError(msg)

    def test_dashboard_route(self) -> None:
        """Test dashboard route."""
        app = create_app()

        with app.test_client() as client:
            response = client.get("/")

            if response.status_code != HTTP_OK:

                msg = f"Expected {200}, got {response.status_code}"
                raise AssertionError(msg)
            if b"FLEXT Web Dashboard" not in response.data:
                msg = f"Expected {b"FLEXT Web Dashboard"} in {response.data}"
                raise AssertionError(msg)
            assert b"Clean Architecture" in response.data
