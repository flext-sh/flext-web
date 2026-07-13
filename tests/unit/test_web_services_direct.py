"""Unit tests for flext_web services facade class."""

from __future__ import annotations

from collections.abc import Sequence
from unittest.mock import patch

from flext_tests import tm

from flext_cli import r
from flext_web import FlextWebServices, FlextWebSettings, c, m, p, t, u


class TestsFlextWebServicesDirect:
    """Test suite for FlextWebServices methods."""

    def setup_method(self) -> None:
        """Reset shared protocol runtime state."""
        FlextWebSettings.reset_for_testing()
        u.Web.apps_registry.clear()
        u.Web.framework_instances.clear()
        u.Web.app_runtimes.clear()
        u.Web.service_state.update({
            "routes_initialized": False,
            "middleware_configured": False,
            "service_running": False,
        })
        u.Web.web_metrics.clear()

    def test_create_service_with_settings(self) -> None:
        """create_service accepts settings overrides."""
        settings = FlextWebSettings(Web={"app_name": "direct-test"})
        result = FlextWebServices.create_service(settings)
        tm.ok(result)
        tm.that(result.value.settings.Web.app_name, eq="direct-test")

    def test_create_service_without_settings(self) -> None:
        """create_service works without settings."""
        result = FlextWebServices.create_service()
        tm.ok(result)

    def test_dashboard_metrics(self) -> None:
        """dashboard_metrics delegates to health service."""
        service = FlextWebServices()
        result = service.dashboard_metrics()
        tm.ok(result)
        tm.that(result.value.service_status, none=False)

    def test_execute(self) -> None:
        """Service facade execute validates business rules."""
        service = FlextWebServices()
        result = service.execute()
        tm.ok(result)
        tm.that(result.value is True, eq=True)

    def test_api_capabilities(self) -> None:
        """Capabilities expose the public facade surface."""
        service = FlextWebServices()
        result = service.api_capabilities()
        tm.ok(result)
        tm.that(result.value, has="application_management")

    def test_fetch_app_invalid_id(self) -> None:
        """fetch_app fails for empty identifier."""
        service = FlextWebServices()
        result = service.fetch_app("")
        tm.fail(result)
        tm.that(result.error, none=False)

    def test_fetch_app_not_found(self) -> None:
        """fetch_app fails for unknown identifier."""
        service = FlextWebServices()
        result = service.fetch_app("unknown-id")
        tm.fail(result)
        tm.that(result.error, none=False)

    def test_health_check(self) -> None:
        """health_check returns a simple payload."""
        service = FlextWebServices()
        result = service.health_check()
        tm.ok(result)
        tm.that(result.value, has="status")
        tm.that(result.value, has="service")

    def test_initialize_routes(self) -> None:
        """initialize_routes configures protocol state."""
        service = FlextWebServices()
        result = service.initialize_routes()
        tm.ok(result)
        tm.that(u.Web.service_state["routes_initialized"] is True, eq=True)

    def test_validate_business_rules_invalid_state(self) -> None:
        """validate_business_rules detects inconsistent running state."""
        service = FlextWebServices()
        u.Web.service_state.update({
            "service_running": True,
            "routes_initialized": False,
            "middleware_configured": True,
        })
        result = service.validate_business_rules()
        tm.fail(result)
        tm.that(result.error, none=False)

    def test_stop_service_with_no_apps(self) -> None:
        """stop_service succeeds when no apps are running."""
        service = FlextWebServices()
        u.Web.service_state["service_running"] = True
        result = service.stop_service()
        tm.ok(result)
        tm.that(u.Web.service_state["service_running"], eq=False)

    def test_get_or_create_runtime_application_creates(self) -> None:
        """Runtime application is created when missing."""
        service = FlextWebServices()
        result = service._get_or_create_runtime_application("localhost", 8080)
        tm.ok(result)
        tm.that(result.value.name, eq=service.settings.Web.app_name)

    def test_get_or_create_runtime_application_returns_existing(self) -> None:
        """Existing runtime application is returned when matched."""
        service = FlextWebServices()
        first = service._get_or_create_runtime_application("localhost", 8080)
        tm.ok(first)
        second = service._get_or_create_runtime_application("localhost", 8080)
        tm.ok(second)
        tm.that(second.value.id, eq=first.value.id)

    def test_validate_business_rules_missing_middleware(self) -> None:
        """validate_business_rules detects running without middleware."""
        service = FlextWebServices()
        u.Web.service_state.update({
            "service_running": True,
            "routes_initialized": True,
            "middleware_configured": False,
        })
        result = service.validate_business_rules()
        tm.fail(result)
        tm.that(result.error, none=False)

    def test_application_response_from_payload_invalid(self) -> None:
        """Invalid payload fails application response projection."""
        service = FlextWebServices()
        result = service._application_response_from_payload({
            "id": "test",
            "name": "test",
            "host": "localhost",
            "port": "not-an-int",
            "status": "stopped",
        })
        tm.fail(result)
        tm.that(result.error, none=False)

    def test_application_responses_from_payloads_invalid(self) -> None:
        """Invalid payload in sequence fails projection."""
        service = FlextWebServices()
        result = service._application_responses_from_payloads([
            {
                "id": "test",
                "name": "test",
                "host": "localhost",
                "port": 8080,
                "status": "stopped",
            },
            {
                "id": "bad",
                "name": "bad",
                "host": "localhost",
                "port": "x",
                "status": "stopped",
            },
        ])
        tm.fail(result)
        tm.that(result.error, none=False)

    def test_start_service_get_or_create_failure(self) -> None:
        """start_service fails when runtime application cannot be created."""
        service = FlextWebServices()
        original = service._get_or_create_runtime_application
        service._get_or_create_runtime_application = lambda host, port: r[
            m.Web.ApplicationResponse
        ].fail("forced failure")
        try:
            result = service.start_service(host="localhost", port=8080)
            tm.fail(result)
            tm.that(result.error, none=False)
        finally:
            service._get_or_create_runtime_application = original

    def test_stop_service_list_apps_failure(self) -> None:
        """stop_service fails when list_apps fails."""
        service = FlextWebServices()
        original = u.Web.WebAppManager.list_apps

        def _failing_list_apps() -> p.Result[Sequence[t.Web.ResponseDict]]:
            return r[Sequence[t.Web.ResponseDict]].fail("forced failure")

        u.Web.WebAppManager.list_apps = _failing_list_apps
        try:
            result = service.stop_service()
            tm.fail(result)
            tm.that(result.error, none=False)
        finally:
            u.Web.WebAppManager.list_apps = original

    def test_start_service_initialize_routes_failure(self) -> None:
        """start_service fails when initialize_routes fails."""
        service = FlextWebServices()
        with patch.object(
            FlextWebServices,
            "initialize_routes",
            return_value=r[bool].fail("routes failed"),
        ):
            result = service.start_service(host="localhost", port=8080)
            tm.fail(result)
            tm.that(result.error, none=False)

    def test_start_service_configure_middleware_failure(self) -> None:
        """start_service fails when configure_middleware fails."""
        service = FlextWebServices()
        with patch.object(
            FlextWebServices,
            "configure_middleware",
            return_value=r[bool].fail("middleware failed"),
        ):
            result = service.start_service(host="localhost", port=8080)
            tm.fail(result)
            tm.that(result.error, none=False)

    def test_start_service_start_app_failure(self) -> None:
        """start_service fails when start_app fails."""
        service = FlextWebServices()
        with patch.object(
            FlextWebServices,
            "start_app",
            return_value=r[m.Web.ApplicationResponse].fail("start failed"),
        ):
            result = service.start_service(host="localhost", port=8080)
            tm.fail(result)
            tm.that(result.error, none=False)

    def test_stop_service_stop_app_failure(self) -> None:
        """stop_service fails when stopping a running app fails."""
        service = FlextWebServices()
        create_result = service.create_app(
            m.Web.AppData(name="running-app", host="localhost", port=8080)
        )
        tm.ok(create_result)
        app_id = create_result.value.id
        u.Web.apps_registry[app_id]["status"] = c.Web.Status.RUNNING.value
        with patch.object(
            FlextWebServices,
            "stop_app",
            return_value=r[m.Web.ApplicationResponse].fail("stop failed"),
        ):
            result = service.stop_service()
            tm.fail(result)
            tm.that(result.error, none=False)

    def test_get_or_create_runtime_application_list_apps_failure(self) -> None:
        """_get_or_create_runtime_application fails when list_apps fails."""
        service = FlextWebServices()
        with patch.object(
            FlextWebServices,
            "list_apps",
            return_value=r[Sequence[m.Web.ApplicationResponse]].fail("list failed"),
        ):
            result = service._get_or_create_runtime_application("localhost", 8080)
            tm.fail(result)
            tm.that(result.error, none=False)
