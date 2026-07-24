"""Unit tests for the canonical flext-web facade."""

from __future__ import annotations

import pytest

from flext_tests import tm
from flext_web import c, web
from tests import m


class TestsFlextWebApi:
    """Tests for the public `web` facade and its class interface."""

    def setup_method(self) -> None:
        """Stop any running public runtime before each test."""
        apps_result = web.list_apps()
        if apps_result.success:
            for app in apps_result.value:
                if app.status == "running":
                    _ = web.stop_app(app.id)
        status_result = web.service_status()
        if status_result.success and status_result.value.status == "operational":
            _ = web.stop_service()

    def test_create_fastapi_app_success(self) -> None:
        """The facade creates FastAPI applications directly."""
        result = web.create_fastapi_app()
        tm.ok(result)

    def test_settings_factory_success(self) -> None:
        """Validated settings can be built through the settings class."""
        settings = web.settings.clone(
            Web={"host": "localhost", "port": 8080}, debug=True
        )
        tm.that(settings.Web.host, eq="localhost")
        tm.that(settings.Web.port, eq=8080)
        tm.that(settings.debug, eq=True)

    def test_settings_factory_rejects_invalid_values(self) -> None:
        """Invalid settings fail validation without xfail wrappers."""
        with pytest.raises(c.ValidationError):
            _ = web.settings.clone(Web={"host": "localhost", "port": -1}, debug=True)
        with pytest.raises(c.ValidationError):
            _ = web.settings.clone(Web={"host": "", "port": 8080})

    def test_validate_settings_success(self) -> None:
        """Settings validation succeeds for a valid namespaced instance."""
        settings = web.settings.clone(
            Web={
                "host": "localhost",
                "port": 8080,
                "secret_key": "test-secret-key-32-characters!!!",
            },
            debug=True,
        )
        validated = type(settings).model_validate(settings.model_dump())
        tm.that(validated.Web.host, eq="localhost")

    def test_get_service_status(self) -> None:
        """The facade exposes structured service status."""
        result = web.service_status()
        tm.ok(result)
        status = result.value
        tm.that(status, is_=m.Web.ServiceResponse)
        tm.that(status.service, eq="flext-web-api")
        tm.that(status.capabilities, has="settings_namespace_registered")

    def test_get_api_capabilities(self) -> None:
        """The facade reports its canonical public capabilities."""
        result = web.api_capabilities()
        tm.ok(result)
        capabilities = result.value
        tm.that(capabilities, has="application_management")
        tm.that(capabilities, has="framework_management")
        tm.that(capabilities, has="service_management")

    def test_settings_property_uses_registered_namespace(self) -> None:
        """The facade exposes typed settings through `web.settings`."""
