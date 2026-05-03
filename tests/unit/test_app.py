"""Unit tests for flext_web.app."""

from __future__ import annotations

import json

from flext_tests import tm

from flext_web import FlextWebSettings, web


class TestsFlextWebApp:
    """Tests for app-related operations through the public facade."""

    def test_create_fastapi_app_uses_settings_defaults(self) -> None:
        """When no settings is passed, the service uses its typed settings."""
        result = web.create_fastapi_app()
        tm.ok(result)
        tm.that(result.value.title, eq=web.settings.app_name)

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
