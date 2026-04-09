"""Unit tests for the canonical flext-web facade."""

from __future__ import annotations

from flext_tests import tm

from flext_web import web
from tests import m


class TestFlextWebApi:
    """Tests for the public `web` facade and its class interface."""

    def setup_method(self) -> None:
        """Stop any running public runtime before each test."""
        apps_result = web.list_apps()
        if apps_result.is_success:
            for app in apps_result.value:
                if app.status == "running":
                    _ = web.stop_app(app.id)
        status_result = web.get_service_status()
        if status_result.is_success and status_result.value.status == "operational":
            _ = web.stop_service()

    def test_create_fastapi_app_success(self) -> None:
        """The facade creates FastAPI applications directly."""
        result = web.create_fastapi_app()
        tm.ok(result)

    def test_create_fastapi_app_with_config(self) -> None:
        """The facade respects explicit FastAPI configuration."""
        config = m.Web.FastAPIAppConfig(title="Test API", version="1.0.0")
        result = web.create_fastapi_app(config)
        tm.ok(result)
        tm.that(result.value.title, eq="Test API")
        tm.that(result.value.version, eq="1.0.0")

    def test_settings_factory_success(self) -> None:
        """Validated settings can be built through the settings class."""
        result = web.settings.create_web_config(
            host="localhost",
            port=8080,
            debug=True,
        )
        tm.ok(result)
        tm.that(result.value.host, eq="localhost")
        tm.that(result.value.port, eq=8080)
        tm.that(result.value.debug_mode, eq=True)

    def test_settings_factory_rejects_invalid_values(self) -> None:
        """Invalid settings fail without xfail wrappers."""
        invalid_port = web.settings.create_web_config(
            host="localhost",
            port=-1,
            debug=True,
        )
        tm.fail(invalid_port)
        invalid_host = web.settings.create_web_config(host="", port=8080)
        tm.fail(invalid_host)

    def test_validate_settings_success(self) -> None:
        """Settings validation returns a successful r for valid input."""
        config = web.settings.model_copy(
            update={
                "host": "localhost",
                "port": 8080,
                "debug": True,
                "debug_mode": True,
                "secret_key": "test-secret-key-32-characters!!!",
            },
        )
        result = web.settings.validate_settings(config)
        tm.ok(result)
        tm.that(result.value, eq=True)

    def test_get_service_status(self) -> None:
        """The facade exposes structured service status."""
        result = web.get_service_status()
        tm.ok(result)
        status = result.value
        tm.that(status, is_=m.Web.ServiceResponse)
        tm.that(status.service, eq="flext-web-api")
        tm.that(status.capabilities, has="settings_namespace_registered")

    def test_get_api_capabilities(self) -> None:
        """The facade reports its canonical public capabilities."""
        result = web.get_api_capabilities()
        tm.ok(result)
        capabilities = result.value
        tm.that(capabilities, has="application_management")
        tm.that(capabilities, has="framework_management")
        tm.that(capabilities, has="service_management")

    def test_settings_property_uses_registered_namespace(self) -> None:
        """The facade exposes typed settings through `web.settings`."""
