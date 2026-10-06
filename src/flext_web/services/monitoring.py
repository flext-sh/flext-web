"""Monitoring surface of the flext-web service facade.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web import FlextWebHealth, c, m, p, r, t


class FlextWebMonitoring(FlextWebHealth):
    """Health, capability and status surface shared by the web services."""

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

    def health_check(self) -> p.Result[t.Web.ResponseDict]:
        """Return a simple health payload for external consumers."""
        return self.health_status().map(
            lambda health_response: {
                "status": health_response.status,
                "service": health_response.service,
                "timestamp": health_response.timestamp,
            },
        )

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
                status=self.service_status_label(),
                settings=True,
            ),
        )


__all__: list[str] = ["FlextWebMonitoring"]
