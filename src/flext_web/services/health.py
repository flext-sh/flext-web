"""Health and metrics services for flext-web.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_web import c, m, p, r, s, u


class FlextWebHealth(s):
    """Health and metrics access backed by protocol runtime state."""

    @override
    def execute(self) -> p.Result[bool]:
        """Execute the health namespace service.

        Returns:
            The resulting ``p.Result[bool]``.
        """
        return r[bool].ok(value=True)

    @staticmethod
    def dashboard_metrics() -> p.Result[m.Web.MetricsResponse]:
        """Return metrics projected from the protocol runtime registry."""
        metrics = u.Web.WebMonitoring.web_metrics()
        components = list(metrics.keys()) or [
            "requests",
            "errors",
            "avg_response_time_ms",
        ]
        return r[m.Web.MetricsResponse].ok(
            m.Web.MetricsResponse(
                service_status=FlextWebHealth.service_status_label(),
                components=components,
            ),
        )

    @staticmethod
    def health_status() -> p.Result[m.Web.HealthResponse]:
        """Return health status from the protocol runtime registry."""
        payload = u.Web.WebMonitoring.web_health_status()
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

    @staticmethod
    def service_status_label() -> str:
        """Return the canonical service status label from runtime state."""
        if u.Web.service_state["service_running"]:
            operational_label: str = c.Web.ResponseStatus.OPERATIONAL.value
            return operational_label
        stopped_label: str = c.Web.Status.STOPPED.value
        return stopped_label


__all__: list[str] = ["FlextWebHealth"]
