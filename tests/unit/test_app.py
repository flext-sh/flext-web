"""Unit tests for flext_web.app.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web import web
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
    def test_validate_business_rules_success() -> None:
        """The app service validates successfully in the default state."""
        tm.ok(web.validate_business_rules())
