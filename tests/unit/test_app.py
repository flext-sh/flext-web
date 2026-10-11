"""Unit tests for flext_web.app.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import u as cli_u

from flext_web import FlextWebSettings, web
from tests import tm


class TestsFlextWebApp:
    """Tests for app-related operations through the public facade."""

    @staticmethod
    def test_create_fastapi_app_uses_settings_defaults() -> None:
        """When no settings is passed, the service uses its typed settings."""
        result = web.create_fastapi_app()
        tm.ok(result)
        tm.that(result.value.title, eq=web.settings.Web.app_name)

    @staticmethod
    def test_create_flask_app_success() -> None:
        """The service creates Flask apps from typed settings."""
        settings = FlextWebSettings().clone(
            Web={
                "app_name": "flext-web-test",
                "host": "127.0.0.1",
                "port": 8123,
                "secret_key": "f" + "0" * 40,
            },
            debug=True,
        )
        result = web.create_flask_app(settings)
        tm.ok(result)
        tm.that(result.value.config["SECRET_KEY"], eq=settings.Web.secret_key)

    @staticmethod
    def test_create_flask_app_health_route() -> None:
        """The Flask health endpoint returns JSON over the public HTTP interface."""
        result = web.create_flask_app()
        tm.ok(result)
        client = result.value.test_client()
        response = client.get("/health")
        body: str = response.get_data(as_text=True)
        payload = cli_u.Cli.json_loads(body).unwrap()
        tm.that(response.status_code, eq=200)
        tm.that(payload, has="status")

    @staticmethod
    def test_validate_business_rules_success() -> None:
        """The app service validates successfully in the default state."""
        tm.ok(web.validate_business_rules())
