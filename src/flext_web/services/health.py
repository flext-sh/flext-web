"""Health and metrics services for flext-web."""

from __future__ import annotations

from typing import override

from flext_core import r
from flext_web import (
    FlextWebProtocols,
    FlextWebServiceBase,
    c,
    m,
    u,
)


class FlextWebHealth(FlextWebServiceBase[bool]):
    """Health and metrics access backed by protocol runtime state."""

    @override
    def execute(self, **_kwargs: str | float | bool | None) -> r[bool]:
        """Execute the health namespace service."""
        return r[bool].ok(True)

    def metrics(self) -> r[m.Web.MetricsResponse]:
        """Return metrics projected from the protocol runtime registry."""
        metrics = FlextWebProtocols.Web.WebMonitoring.get_web_metrics()
        state = FlextWebProtocols.Web.service_state
        service_status = (
            c.Web.WebResponse.STATUS_OPERATIONAL
            if state["service_running"]
            else c.Web.Status.STOPPED.value
        )
        components = list(metrics.keys()) or [
            "requests",
            "errors",
            "avg_response_time_ms",
        ]
        return r[m.Web.MetricsResponse].ok(
            m.Web.MetricsResponse(
                service_status=service_status,
                components=components,
            ),
        )

    def status(self) -> r[m.Web.HealthResponse]:
        """Return health status from the protocol runtime registry."""
        payload = FlextWebProtocols.Web.WebMonitoring.get_web_health_status()
        service_value = payload.get("service")
        status_value = payload.get("status")
        if not isinstance(service_value, str) or not isinstance(status_value, str):
            return r[m.Web.HealthResponse].fail(
                "Health monitoring payload is incomplete",
            )
        return r[m.Web.HealthResponse].ok(
            m.Web.HealthResponse(
                status=status_value,
                service=service_value,
                timestamp=u.generate_iso_timestamp(),
            ),
        )

    @override
    def validate_business_rules(self) -> r[bool]:
        """Validate health namespace invariants."""
        return r[bool].ok(True)


__all__ = ["FlextWebHealth"]
