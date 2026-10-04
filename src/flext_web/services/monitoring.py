"""Monitoring surface of the flext-web service facade.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web import FlextWebHealth, FlextWebSettings, c, m, p, r, s, t, u


class FlextWebMonitoring(s):
    """Health, capability and status surface shared by the web services."""

    _health_service: FlextWebHealth | None = u.PrivateAttr(default_factory=lambda: None)

    @staticmethod
    def api_capabilities() -> p.Result[t.Web.ResponseDict]:
        """Expose the canonical capabilities of the public web facade.

        Returns:
            The resulting ``p.Result[t.Web.ResponseDict]``.
        """
        return r[t.Web.ResponseDict].ok({
            "application_management": ["create_app", "fetch_app", "list_apps"],
            "framework_management": ["create_fastapi_app", "create_flask_app"],
            "service_management": ["start_service", "stop_service"],
            "configuration_management": ["settings", "create_service"],
            "monitoring": ["health_check", "health_status", "dashboard"],
        })

    def dashboard_metrics(self) -> p.Result[m.Web.MetricsResponse]:
        """Return health metrics for the dashboard."""
        return self._health().metrics()

    def health_check(self) -> p.Result[t.Web.ResponseDict]:
        """Return a simple health payload for external consumers."""
        return self.health_status().map(
            lambda health_response: {
                "status": health_response.status,
                "service": health_response.service,
                "timestamp": health_response.timestamp,
            },
        )

    def health_status(self) -> p.Result[m.Web.HealthResponse]:
        """Return structured health status."""
        return self._health().status()

    def service_status(self) -> p.Result[m.Web.ServiceResponse]:
        """Return service status using protocol runtime state and settings."""
        return r[m.Web.ServiceResponse].ok(
            m.Web.ServiceResponse(
                service=c.Web.SERVICE_NAME_API,
                capabilities=[
                    "http_services_available",
                    "fastapi_support",
                    "flask_support",
                    "settings_namespace_registered",
                ],
                status=self._service_status_label(),
                settings=True,
            ),
        )

    @staticmethod
    def _service_status_label() -> str:
        """Return the canonical service status label from runtime state."""
        state = u.Web.service_state
        service_running: bool = state["service_running"]
        if service_running:
            operational_label: str = c.Web.ResponseStatus.OPERATIONAL.value
            return operational_label
        stopped_label: str = c.Web.Status.STOPPED.value
        return stopped_label

    def _health(self) -> FlextWebHealth:
        """Return the lazily created health service."""
        if self._health_service is None:
            self._health_service = FlextWebHealth.with_settings(
                self._runtime_settings_clone(),
            )
        return self._health_service

    def _runtime_settings_clone(self) -> FlextWebSettings:
        """Return a clone of the bound runtime settings for child services."""
        return FlextWebSettings.model_validate(self.settings.clone())


__all__: list[str] = ["FlextWebMonitoring"]
