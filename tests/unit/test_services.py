"""Unit tests for the public service surface exposed by `web`.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web import p, web
from tests import m, tm
from tests.fixtures import TestsFlextWebAuthFixture


class TestsFlextWebService:
    """Tests for the canonical web service layer through `web`."""

    @staticmethod
    def test_authenticate_success() -> None:
        """Authentication succeeds for the canonical test credentials."""
        credentials = TestsFlextWebAuthFixture().credentials
        result = web.authenticate(credentials)
        tm.ok(result)
        tm.that(result.value.user_id, eq=credentials.username)

    @staticmethod
    def test_authenticate_failure() -> None:
        """Authentication fails for invalid credentials."""
        canonical = TestsFlextWebAuthFixture()
        credentials = canonical.credentials.model_copy(
            update={"username": canonical.rejected_username},
        )
        result = web.authenticate(credentials)
        tm.fail(result)
        tm.that(result.error, has="authenticate")

    @staticmethod
    def test_register_user_success() -> None:
        """User registration succeeds for valid input."""
        credentials = TestsFlextWebAuthFixture().credentials
        result = web.register_user(
            m.Web.UserData(
                username="newuser",
                email="newuser@example.com",
                password=credentials.password,
            ),
        )
        tm.ok(result)
        tm.that(result.value.created, eq=True)

    @staticmethod
    def test_register_user_rejects_numeric_username() -> None:
        """Numeric-only usernames are rejected."""
        credentials = TestsFlextWebAuthFixture().credentials
        result = web.register_user(
            m.Web.UserData(
                username="12345",
                email="numeric@example.com",
                password=credentials.password,
            ),
        )
        tm.fail(result)

    @staticmethod
    def test_create_get_list_app_cycle() -> None:
        """Applications are created through protocol-backed runtime state."""
        create_result = web.create_app(
            m.Web.AppData(name="test-app", host="127.0.0.1", port=8182),
        )
        tm.ok(create_result)
        app = create_result.value
        get_result = web.fetch_app(app.id)
        list_result = web.list_apps()
        tm.ok(get_result)
        tm.ok(list_result)
        tm.that(get_result.value.id, eq=app.id)
        tm.that(
            any(listed_app.id == app.id for listed_app in list_result.value),
            eq=True,
        )

    @staticmethod
    def test_start_and_stop_app_cycle() -> None:
        """Applications transition through running and stopped states."""
        create_result = web.create_app(
            m.Web.AppData(name="runtime-app", host="127.0.0.1", port=8183),
        )
        tm.ok(create_result)
        app_id = create_result.value.id
        start_result = web.start_app(app_id)
        tm.ok(start_result)
        tm.that(start_result.value.status, eq="running")
        stop_result = web.stop_app(app_id)
        tm.ok(stop_result)
        tm.that(stop_result.value.status, eq="stopped")

    @staticmethod
    def test_entity_crud_cycle() -> None:
        """Generic entity CRUD remains available on the canonical service."""
        create_result = web.create_entity(m.Web.EntityData(data={"key": "value"}))
        tm.ok(create_result)
        entity_id = str(create_result.value.data["id"])
        get_result = web.fetch_entity(entity_id)
        list_result = web.list_entities()
        tm.ok(get_result)
        tm.ok(list_result)
        tm.that(get_result.value.data["key"], eq="value")
        tm.that(list_result.value, length=1)

    @staticmethod
    def test_health_dashboard_and_capabilities() -> None:
        """Health, dashboard and capability projections stay coherent."""
        tm.ok(web.initialize_routes())
        tm.ok(web.configure_middleware())
        health_result = web.health_status()
        dashboard_result = web.dashboard()
        capabilities_result = web.api_capabilities()
        tm.ok(health_result)
        tm.ok(dashboard_result)
        tm.ok(capabilities_result)
        tm.that(health_result.value.service, eq="flext-web")
        tm.that(dashboard_result.value.routes_initialized, eq=True)
        tm.that(capabilities_result.value, has="framework_management")

    @staticmethod
    def test_start_and_stop_service() -> None:
        """Service start bootstraps a runtime application and stop tears it down."""
        start_result = web.start_service(host="127.0.0.1", port=8184)
        tm.ok(start_result)
        status_result = web.service_status()
        tm.ok(status_result)
        tm.that(status_result.value.status, eq="operational")
        apps_result = web.list_apps()
        tm.ok(apps_result)
        tm.that(any(app.status == "running" for app in apps_result.value), eq=True)
        stop_result = web.stop_service()
        tm.ok(stop_result)
        stopped_status = web.service_status()
        tm.ok(stopped_status)
        tm.that(stopped_status.value.status, eq="stopped")

    @staticmethod
    def test_get_service_status() -> None:
        """Structured service status is exposed by the service layer itself."""
        result = web.service_status()
        tm.ok(result)
        tm.that(result.value.service, eq="flext-web-api")
        tm.that(result.value.capabilities, has="flask_support")

    @staticmethod
    def _is_service_rules(candidate: p.Base) -> bool:
        """Report structural conformance without a type-narrowed argument.

        Returns:
            The resulting ``bool``.
        """
        return isinstance(candidate, p.Web.WebServiceRules)

    def test_web_satisfies_its_own_service_rules_protocol(self) -> None:
        """The real composed facade structurally satisfies its own protocol."""
        tm.that(self._is_service_rules(web), eq=True)
        result = web.validate_business_rules()
        tm.ok(result)
        tm.that(result.value, eq=True)
