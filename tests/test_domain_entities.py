"""Tests for FlextWeb domain entities."""

from __future__ import annotations

from flext_web.api import WebApp, WebAppHandler


class TestWebApp:
    """Test WebApp entity."""

    def test_webapp_creation(self) -> None:
        """Test WebApp creation."""
        app = WebApp(id="test_app", name="TestApp", port=8080)

        assert app.id == "test_app"
        assert app.name == "TestApp"
        assert app.port == 8080
        assert app.host == "localhost"
        assert not app.is_running

    def test_webapp_validation(self) -> None:
        """Test WebApp validation."""
        app = WebApp(id="test_app", name="TestApp", port=8080)
        result = app.validate_domain_rules()

        assert result.is_success

    def test_webapp_invalid_port(self) -> None:
        """Test WebApp with invalid port."""
        import pytest
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            WebApp(id="test_app", name="TestApp", port=99999)

    def test_webapp_empty_name(self) -> None:
        """Test WebApp with empty name."""
        app = WebApp(id="test_app", name="", port=8080)
        result = app.validate_domain_rules()

        assert not result.is_success
        assert "App name is required" in result.error

    def test_webapp_start(self) -> None:
        """Test WebApp start."""
        app = WebApp(id="test_app", name="TestApp", port=8080)
        result = app.start()

        assert result.is_success
        started_app = result.data
        assert started_app is not None
        assert started_app.is_running

    def test_webapp_stop(self) -> None:
        """Test WebApp stop."""
        app = WebApp(id="test_app", name="TestApp", port=8080, is_running=True)
        result = app.stop()

        assert result.is_success
        stopped_app = result.data
        assert stopped_app is not None
        assert not stopped_app.is_running


class TestWebAppHandler:
    """Test WebAppHandler."""

    def test_handler_create(self) -> None:
        """Test handler create."""
        handler = WebAppHandler()
        result = handler.handle_create("TestApp", port=8080)

        assert result.is_success
        app = result.data
        assert app is not None
        assert app.name == "TestApp"
        assert app.port == 8080

    def test_handler_start(self) -> None:
        """Test handler start."""
        handler = WebAppHandler()
        app = WebApp(id="test_app", name="TestApp", port=8080)

        result = handler.handle_start(app)

        assert result.is_success
        started_app = result.data
        assert started_app is not None
        assert started_app.is_running

    def test_handler_stop(self) -> None:
        """Test handler stop."""
        handler = WebAppHandler()
        app = WebApp(id="test_app", name="TestApp", port=8080, is_running=True)

        result = handler.handle_stop(app)

        assert result.is_success
        stopped_app = result.data
        assert stopped_app is not None
        assert not stopped_app.is_running
