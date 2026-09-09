"""Unit tests for flext_web health service."""

from __future__ import annotations

from flext_tests import tm

from flext_web import FlextWebHealth, u
from tests import c


class TestsFlextWebHealth:
    """Test suite for FlextWebHealth."""

    def setup_method(self) -> None:
        """Reset shared protocol runtime state."""
        u.Web.service_state.update({
            "routes_initialized": False,
            "middleware_configured": False,
            "service_running": False,
        })
        u.Web.web_metrics.clear()

    def test_execute_returns_success(self) -> None:
        """Health service execute returns success."""
        health = FlextWebHealth()
        result = health.execute()
        tm.ok(result)
        tm.that(result.value is True, eq=True)

    def test_metrics_when_stopped(self) -> None:
        """Metrics reflect stopped service state."""
        health = FlextWebHealth()
        result = health.metrics()
        tm.ok(result)
        tm.that(result.value.service_status, eq=c.Web.Status.STOPPED.value)
        tm.that(result.value.components, has="requests")

    def test_metrics_when_operational(self) -> None:
        """Metrics reflect operational service state."""
        u.Web.service_state["service_running"] = True
        u.Web.web_metrics.update({"requests": 5, "errors": 1})
        health = FlextWebHealth()
        result = health.metrics()
        tm.ok(result)
        tm.that(result.value.service_status, eq=c.Web.ResponseStatus.OPERATIONAL.value)
        tm.that(result.value.components, has="requests")
        tm.that(result.value.components, has="errors")

    def test_status_when_stopped(self) -> None:
        """Health status reflects stopped state when service is not running."""
        health = FlextWebHealth()
        result = health.status()
        tm.ok(result)
        tm.that(result.value.status, eq=c.Web.Status.STOPPED.value)
        tm.that(result.value.service, eq=c.Web.SERVICE_NAME)

    def test_status_when_running(self) -> None:
        """Health status reflects healthy state when service is running."""
        u.Web.service_state["service_running"] = True
        health = FlextWebHealth()
        result = health.status()
        tm.ok(result)
        tm.that(result.value.status, eq=c.Web.ResponseStatus.HEALTHY.value)
        tm.that(result.value.service, eq=c.Web.SERVICE_NAME)

    def test_status_incomplete_payload_fails(self) -> None:
        """Health status fails when monitoring payload is incomplete."""
        original = u.Web.WebMonitoring.web_health_status
        u.Web.WebMonitoring.web_health_status = lambda: {"service": "flext-web"}
        try:
            health = FlextWebHealth()
            result = health.status()
            tm.fail(result)
            tm.that(result.error, none=False)
        finally:
            u.Web.WebMonitoring.web_health_status = original

    def test_validate_business_rules(self) -> None:
        """Health service business rules validate cleanly."""
        health = FlextWebHealth()
        result = health.validate_business_rules()
        tm.ok(result)
        tm.that(result.value is True, eq=True)
