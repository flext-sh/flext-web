"""Unit tests for flext_web services facade class."""

from __future__ import annotations

from flext_tests import tm
from flext_web import FlextWebServices, FlextWebSettings, u


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
        settings = FlextWebSettings().clone(Web={"app_name": "direct-test"})
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
