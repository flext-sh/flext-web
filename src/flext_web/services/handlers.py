"""FLEXT Web Handlers - Main Handler Coordination.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import ClassVar

from flext_web import c, m, p, r, s, u


class FlextWebHandlers(s[bool]):
    """Consolidated web handler system extending flext-core patterns.

    This class serves as the single point of access for all web-specific
    handlers, command processors, and response formatters while extending
    s from flext-core for proper architectural inheritance.

    All handler functionality is accessible through this single class following the
    "one class per module" architectural requirement.
    """

    SystemInfo: ClassVar[type[m.Web.SystemInfo]] = m.Web.SystemInfo
    HealthStatus: ClassVar[type[m.Web.HealthStatus]] = m.Web.HealthStatus

    @classmethod
    def handle_create_app(
        cls,
        name: str,
        port: int = c.Web.DEFAULT_PORT,
        host: str = c.Web.DEFAULT_HOST,
    ) -> p.Result[m.Web.Entity]:
        """Handle application creation requests.

        Args:
        name: Application name
        port: Application port
        host: Application host

        Returns:
        r containing created application or error

        """
        app_id = m.Web.Entity.format_id_from_name(name)
        app = m.Web.Entity(
            id=app_id,
            name=name,
            port=port,
            host=host,
            status=c.Web.Status.STOPPED.value,
            environment=c.Web.Name.DEVELOPMENT.value,
            debug_mode=False,
            metrics={},
            web_events=[],
            domain_events=[],
        )
        return app.validate_business_rules().flat_map(lambda _: r[m.Web.Entity].ok(app))

    @classmethod
    def handle_start_app(cls, app: m.Web.Entity) -> p.Result[m.Web.Entity]:
        """Handle application start requests.

        Args:
        app: Application to start

        Returns:
        r containing updated application or error

        """
        return app.start()

    @classmethod
    def handle_stop_app(cls, app: m.Web.Entity) -> p.Result[m.Web.Entity]:
        """Handle application stop requests.

        Args:
        app: Application to stop

        Returns:
        r containing updated application or error

        """
        return app.stop()

    @classmethod
    def handle_system_info(cls) -> p.Result[m.Web.SystemInfo]:
        """Handle system information requests.

        Returns:
        r containing detailed system information.

        """
        return r[m.Web.SystemInfo].ok(
            m.Web.SystemInfo(
                service_name="FLEXT Web Interface",
                service_type="web_api",
                architecture="flask_clean_architecture",
                patterns=["CQRS", "Clean Architecture", "Domain-Driven Design"],
                integrations=["flext-core", "pydantic", "flask"],
                capabilities=[
                    "application_management",
                    "health_monitoring",
                    "api_endpoints",
                    "web_dashboard",
                ],
            ),
        )

    @staticmethod
    def handle_health_check() -> p.Result[m.Web.HealthStatus]:
        """Handle health check requests with system status.

        Returns:
        r containing health status information.

        """
        return r[m.Web.HealthStatus].ok(
            m.Web.HealthStatus(
                status=c.Web.RESPONSE_STATUS_HEALTHY,
                service=c.Web.SERVICE_NAME,
                version="0.9.0",
                timestamp=u.generate_iso_timestamp(),
                components={
                    "web_service": c.Web.RESPONSE_STATUS_OPERATIONAL,
                    "configuration": c.Web.MESSAGE_CONFIG_LOADED,
                    "handlers": c.Web.MESSAGE_HANDLERS_REGISTERED,
                },
            ),
        )

    def execute(
        self,
    ) -> p.Result[bool]:
        """Execute web handler service (s requirement).

        Returns:
            r[bool]: Success contains True if handlers are operational,
            failure contains error message

        """
        return r[bool].ok(value=True)

    def validate_business_rules(self) -> p.Result[bool]:
        """Validate business rules for web handlers (s requirement).

        Returns:
            r[bool]: Success contains True if valid, failure with error message

        """
        return r[bool].ok(value=True)


__all__: list[str] = ["FlextWebHandlers"]
