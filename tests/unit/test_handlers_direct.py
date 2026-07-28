"""Unit tests for flext_web handlers class."""

from __future__ import annotations

from flext_tests import tm
from flext_web import FlextWebHandlers, c, m


class TestsFlextWebHandlersDirect:
    """Test suite for FlextWebHandlers methods."""

    def test_handle_create_app_success(self) -> None:
        """Handler creates a valid application entity."""
        result = FlextWebHandlers.handle_create_app(
            name="handler-app", port=8080, host="localhost"
        )
        tm.ok(result)
        tm.that(result.value.name, eq="handler-app")
        tm.that(result.value.status, eq=c.Web.Status.STOPPED.value)

    def test_handle_start_app_success(self) -> None:
        """Handler starts a stopped application."""
        app = m.Web.Entity(
            id="test-id",
            name="test-app",
            host="localhost",
            port=8080,
            status=c.Web.Status.STOPPED.value,
        )
        result = FlextWebHandlers.handle_start_app(app)
        tm.ok(result)
        tm.that(result.value.status, eq=c.Web.Status.RUNNING.value)

    def test_handle_stop_app_success(self) -> None:
        """Handler stops a running application."""
        app = m.Web.Entity(
            id="test-id",
            name="test-app",
            host="localhost",
            port=8080,
            status=c.Web.Status.RUNNING.value,
        )
        result = FlextWebHandlers.handle_stop_app(app)
        tm.ok(result)
        tm.that(result.value.status, eq=c.Web.Status.STOPPED.value)

    def test_handle_system_info(self) -> None:
        """Handler returns system information."""
        result = FlextWebHandlers.handle_system_info()
        tm.ok(result)
        tm.that(result.value.service_name, eq="FLEXT Web Interface")
        tm.that(result.value.capabilities, has="application_management")

    def test_handle_health_check(self) -> None:
        """Handler returns health status."""
        result = FlextWebHandlers.handle_health_check()
        tm.ok(result)
        tm.that(result.value.status, eq=c.Web.ResponseStatus.HEALTHY.value)
        tm.that(result.value.service, eq=c.Web.SERVICE_NAME)

    def test_execute(self) -> None:
        """Handlers execute returns success."""
        handlers = FlextWebHandlers()
        result = handlers.execute()
        tm.ok(result)
        tm.that(result.value is True, eq=True)

    def test_validate_business_rules(self) -> None:
        """Handlers validate business rules cleanly."""
        handlers = FlextWebHandlers()
        result = handlers.validate_business_rules()
        tm.ok(result)
        tm.that(result.value is True, eq=True)
