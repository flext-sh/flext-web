"""Health and metrics services for flext-web."""

from __future__ import annotations

from flext_web import (
    c,
    m,
    p,
    r,
    s,
    u,
)


class FlextWebHealth(s[bool]):
    """Health and metrics access backed by protocol runtime state."""

    def execute(
        self,
    ) -> p.Result[bool]:
        """Execute the health namespace service."""
        return r[bool].ok(True)

    def metrics(self) -> p.Result[m.Web.MetricsResponse]:
        """Return metrics projected from the protocol runtime registry."""
        metrics = p.Web.WebMonitoring.web_metrics()
        state = p.Web.service_state
        service_status = (
            c.Web.RESPONSE_STATUS_OPERATIONAL
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

    def status(self) -> p.Result[m.Web.HealthResponse]:
        """Return health status from the protocol runtime registry."""
        payload = p.Web.WebMonitoring.web_health_status()
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

    def validate_business_rules(self) -> p.Result[bool]:
        """Validate health namespace invariants."""
        return r[bool].ok(True)


__all__: list[str] = ["FlextWebHealth"]
