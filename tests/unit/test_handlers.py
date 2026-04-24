"""Unit tests for public behavior backed by web handlers."""

from __future__ import annotations

from flext_tests import tm

from flext_web import web
from tests import m, u


class TestsFlextWebHandlers:
    """Tests for handler-backed behavior exposed through `web`."""

    _allocated_ports: list[int]

    def setup_method(self) -> None:
        """Reset the public runtime to a stopped state before each test."""
        self._allocated_ports: list[int] = []
        apps_result = web.list_apps()
        if apps_result.success:
            for app in apps_result.value:
                if app.status == "running":
                    _ = web.stop_app(app.id)
        status_result = web.service_status()
        if status_result.success and status_result.value.status == "operational":
            _ = web.stop_service()

    def teardown_method(self) -> None:
        """Release ports reserved for each test method."""
        for port in self._allocated_ports:
            u.Web.Tests.TestPortManager.release_port(port)

    def _next_port(self) -> int:
        """Reserve and return a unique port for the current test."""
        port = u.Web.Tests.TestPortManager.allocate_port()
        self._allocated_ports.append(port)
        return port

    def test_list_apps_uses_public_registry(self) -> None:
        """Applications are listed through the public facade."""
        create_result = web.create_app(
            m.Web.AppData(
                name="test-app",
                host="localhost",
                port=self._next_port(),
            ),
        )
        tm.ok(create_result)
        result = web.list_apps()
        tm.ok(result)
        tm.that(result.value, is_=list)
        tm.that(any(app.name == "test-app" for app in result.value), eq=True)

    def test_health_check_projection(self) -> None:
        """Health state is exposed through the public facade."""
        result = web.health_status()
        tm.ok(result)

    def test_service_status_projection(self) -> None:
        """Service metadata is exposed through the public facade."""
        result = web.service_status()
        tm.ok(result)

    def test_create_app_through_public_facade(self) -> None:
        """Application creation goes through the public facade."""
        port = self._next_port()
        result = web.create_app(
            m.Web.AppData(name="test-app", host="localhost", port=port),
        )
        tm.ok(result)
        app = result.value
        tm.that(app.name, eq="test-app")
        tm.that(app.port, eq=port)
        tm.that(app.host, eq="localhost")

    def test_app_registry_integration(self) -> None:
        """Created applications remain visible through the public registry."""
        create_result = web.create_app(
            m.Web.AppData(
                name="test-app",
                host="localhost",
                port=self._next_port(),
            ),
        )
        tm.ok(create_result)
        app = create_result.value
        list_result = web.list_apps()
        tm.ok(list_result)
        tm.that(
            any(listed_app.id == app.id for listed_app in list_result.value), eq=True
        )

    def test_protocol_implementation(self) -> None:
        """Public app lifecycle operations remain coherent."""
        create_result = web.create_app(
            m.Web.AppData(name="test", host="localhost", port=self._next_port()),
        )
        tm.ok(create_result)
        list_result = web.list_apps()
        tm.ok(list_result)

    def test_public_identifier_validation_errors(self) -> None:
        """Invalid public identifiers fail before runtime mutation."""
        start_result = web.start_app("")
        tm.fail(start_result)
        stop_result = web.stop_app("")
        tm.fail(stop_result)

    def test_application_handler_start_app_not_found(self) -> None:
        """Starting an unknown app fails through the public API."""
        result = web.start_app("nonexistent-id")
        tm.fail(result)
        assert result.error is not None
        tm.that(result.error, has="not found")

    def test_application_handler_stop_app_not_found(self) -> None:
        """Stopping an unknown app fails through the public API."""
        result = web.stop_app("nonexistent-id")
        tm.fail(result)
        assert result.error is not None
        tm.that(result.error, has="not found")

    def test_application_handler_start_stop_cycle(self) -> None:
        """Apps can be started and stopped through the public API."""
        create_result = web.create_app(
            m.Web.AppData(
                name="test-app",
                host="localhost",
                port=self._next_port(),
            ),
        )
        tm.ok(create_result)
        app_id = create_result.value.id
        start_result = web.start_app(app_id)
        tm.ok(start_result)
        tm.that(start_result.value.status, eq="running")
        stop_result = web.stop_app(app_id)
        tm.ok(stop_result)
        tm.that(stop_result.value.status, eq="stopped")

    def test_handle_start_app_invalid_type(self) -> None:
        """App lifecycle public API rejects unknown app identifiers."""
        result = web.start_app("")
        tm.fail(result)

    def test_handle_stop_app_invalid_type(self) -> None:
        """App lifecycle public API rejects empty app identifiers."""
        result = web.stop_app("")
        tm.fail(result)

    def test_handlers_execute(self) -> None:
        """The public facade remains executable."""
        result = web.execute()
        tm.ok(result)
        tm.that(result.value is True, eq=True)

    def test_handlers_validate_business_rules(self) -> None:
        """Business-rule validation is exposed through the public facade."""
        result = web.validate_business_rules()
        tm.ok(result)
        tm.that(result.value is True, eq=True)

    def test_handle_start_app(self) -> None:
        """Starting a created app works through the public facade."""
        app_result = web.create_app(
            m.Web.AppData(
                name="test-app",
                host="localhost",
                port=self._next_port(),
            ),
        )
        tm.ok(app_result)
        result = web.start_app(app_result.value.id)
        tm.ok(result)
        tm.that(result.value.status, eq="running")

    def test_handle_stop_app(self) -> None:
        """Stopping a running app works through the public facade."""
        app_result = web.create_app(
            m.Web.AppData(
                name="test-app",
                host="localhost",
                port=self._next_port(),
            ),
        )
        tm.ok(app_result)
        start_result = web.start_app(app_result.value.id)
        tm.ok(start_result)
        result = web.stop_app(start_result.value.id)
        tm.ok(result)
        tm.that(result.value.status, eq="stopped")
