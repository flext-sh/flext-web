"""Unit tests for flext_web.app."""

from __future__ import annotations

import json

from fastapi.testclient import TestClient
from flext_tests import tm

from flext_web import FlextWebSettings, web
from tests import c, m


class TestsFlextWebApp:
    """Tests for app-related operations through the public facade."""

    def test_create_fastapi_app_success(self) -> None:
        """The service creates FastAPI applications with explicit settings."""
        settings = m.Web.FastAPIAppConfig(
            title="Custom Test API",
            version="2.0.0",
            description=c.Web.API_DEFAULT_DESCRIPTION,
        )
        result = web.create_fastapi_app(settings)
        tm.ok(result)
        tm.that(result.value.title, eq="Custom Test API")
        tm.that(result.value.version, eq="2.0.0")

    def test_create_fastapi_app_registers_endpoints(self) -> None:
        """Health and info endpoints are registered on the created app."""
        settings = m.Web.FastAPIAppConfig(title="Test API", version="1.0.0")
        result = web.create_fastapi_app(settings)
        tm.ok(result)
        client = TestClient(result.value)
        health_response = client.get("/health")
        info_response = client.get("/info")
        tm.that(health_response.status_code, eq=200)
        tm.that(info_response.status_code, eq=200)
        tm.that(health_response.json(), has="status")
        tm.that(info_response.json(), has="title")

    def test_create_fastapi_app_uses_settings_defaults(self) -> None:
        """When no settings is passed, the service uses its typed settings."""
        result = web.create_fastapi_app()
        tm.ok(result)
        tm.that(result.value.title, eq=web.settings.app_name)

    def test_create_fastapi_app_allows_factory_overrides(self) -> None:
        """Factory overrides remain supported without API ceremony."""
        settings = m.Web.FastAPIAppConfig(title="Base API", version="1.0.0")
        factory_config = m.Web.FastAPIAppConfig(
            title="Override API",
            version="2.0.0",
            docs_url="/custom-docs",
            redoc_url="/custom-redoc",
            openapi_url="/custom-openapi.json",
        )
        result = web.create_fastapi_app(settings, factory_config)
        tm.ok(result)
        tm.that(result.value.title, eq="Override API")
        tm.that(result.value.openapi_url, eq="/custom-openapi.json")

    def test_create_flask_app_success(self) -> None:
        """The service creates Flask apps from typed settings."""
        settings = FlextWebSettings(
            app_name="flext-web-test",
            host="127.0.0.1",
            port=8123,
            debug=True,
            debug_mode=True,
            secret_key="flask-secret-key-32-characters!!",
        )
        result = web.create_flask_app(settings)
        tm.ok(result)
        tm.that(result.value.config["SECRET_KEY"], eq=settings.secret_key)

    def test_create_flask_app_health_route(self) -> None:
        """The Flask health endpoint returns JSON over the public HTTP interface."""
        result = web.create_flask_app()
        tm.ok(result)
        client = result.value.test_client()
        response = client.get("/health")
        payload = json.loads(response.get_data(as_text=True))
        tm.that(response.status_code, eq=200)
        tm.that(payload, has="status")

    def test_fastapi_configuration_hooks_return_success(self) -> None:
        """Framework-specific configure hooks stay explicit and separate."""
        fastapi_result = web.create_fastapi_app()
        tm.ok(fastapi_result)
        settings = web.settings.create_web_config().value
        tm.ok(web.configure_fastapi_error_handlers(fastapi_result.value))
        tm.ok(
            web.configure_fastapi_middleware(
                fastapi_result.value,
                settings,
            ),
        )
        tm.ok(web.configure_fastapi_routes(fastapi_result.value, settings))

    def test_validate_business_rules_success(self) -> None:
        """The app service validates successfully in the default state."""
        tm.ok(web.validate_business_rules())
