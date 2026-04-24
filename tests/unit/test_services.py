"""Unit tests for the public service surface exposed by `web`."""

from __future__ import annotations

from flext_tests import tm

from flext_web import web
from tests import m


class TestFlextWebService:
    """Tests for the canonical web service layer through `web`."""

    def setup_method(self) -> None:
        """Stop any running service before each test."""
        apps_result = web.list_apps()
        if apps_result.success:
            for app in apps_result.value:
                if app.status == "running":
                    _ = web.stop_app(app.id)
        status_result = web.service_status()
        if status_result.success and status_result.value.status == "operational":
            _ = web.stop_service()

    def test_authenticate_success(self) -> None:
        """Authentication succeeds for the canonical test credentials."""
        credentials = m.Web.Credentials(
            username="testuser",
            password="test_password",
        )
        result = web.authenticate(credentials)
        tm.ok(result)
        tm.that(result.value.user_id, eq="testuser")

    def test_authenticate_failure(self) -> None:
        """Authentication fails for invalid credentials."""
        credentials = m.Web.Credentials(
            username="nonexistent",
            password="wrong-password",
        )
        result = web.authenticate(credentials)
        tm.fail(result)
        tm.that(result.error, has="Authentication failed")

    def test_register_user_success(self) -> None:
        """User registration succeeds for valid input."""
        result = web.register_user(
            m.Web.UserData(
                username="newuser",
                email="newuser@example.com",
                password="password123",
            ),
        )
        tm.ok(result)
        tm.that(result.value.created, eq=True)

    def test_register_user_rejects_numeric_username(self) -> None:
        """Numeric-only usernames are rejected."""
        result = web.register_user(
            m.Web.UserData(
                username="12345",
                email="numeric@example.com",
                password="password123",
            ),
        )
        tm.fail(result)

    def test_create_get_list_app_cycle(self) -> None:
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

    def test_start_and_stop_app_cycle(self) -> None:
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

    def test_entity_crud_cycle(self) -> None:
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

    def test_health_dashboard_and_capabilities(self) -> None:
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

    def test_start_and_stop_service(self) -> None:
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

    def test_get_service_status(self) -> None:
        """Structured service status is exposed by the service layer itself."""
        result = web.service_status()
        tm.ok(result)
        tm.that(result.value.service, eq="flext-web-api")
        tm.that(result.value.capabilities, has="flask_support")
