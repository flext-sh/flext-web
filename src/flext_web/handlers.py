"""FLEXT Web Handlers - Main Handler Coordination.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import MutableMapping, Sequence
from typing import ClassVar, override

from flext_core import FlextLogger, FlextService, r, u

from flext_web import c, m

__all__ = ["FlextWebHandlers"]

# Canonical model aliases for this module
SystemInfo = m.Web.SystemInfo
HealthStatus = m.Web.HealthStatus


class FlextWebHandlers(FlextService[bool]):
    """Consolidated web handler system extending flext-core patterns.

    This class serves as the single point of access for all web-specific
    handlers, command processors, and response formatters while extending
    FlextService from flext-core for proper architectural inheritance.

    All handler functionality is accessible through this single class following the
    "one class per module" architectural requirement.
    """

    SystemInfo: ClassVar[type[m.Web.SystemInfo]] = m.Web.SystemInfo
    HealthStatus: ClassVar[type[m.Web.HealthStatus]] = m.Web.HealthStatus

    class ApplicationHandler:
        """CQRS command handler for web application lifecycle management.

        Implements Command Query Responsibility Segregation (CQRS) patterns for
        web application operations using flext-core handler patterns. Provides
        validated, consistent handling of application lifecycle commands with
        complete error handling and business rule enforcement.

        Responsibilities:
          - Command validation and processing
          - Business rule enforcement via domain entities
          - Error handling and reporting
          - Application registry management

        """

        def __init__(self) -> None:
            """Initialize application handler."""
            super().__init__()
            self.logger = FlextLogger(__name__)
            self._apps_registry: MutableMapping[str, m.Web.Entity] = {}
            self.apps_registry = self._apps_registry
            self.logger.info("WebApp handler initialized")

        @staticmethod
        def _validate_create_inputs(name: str, port: int, host: str) -> r[str]:
            """Validate create inputs - consolidates all validations."""
            if len(name) < c.Web.WebServer.MIN_APP_NAME_LENGTH:
                return r[str].fail(
                    f"Application name must be at least {c.Web.WebServer.MIN_APP_NAME_LENGTH} characters",
                )
            if name.isdigit():
                return r[str].fail("Application name cannot be numeric-only")
            if not host:
                return r[str].fail("Host cannot be empty")
            min_port = c.Web.WebValidation.PORT_RANGE[0]
            max_port = c.Web.WebValidation.PORT_RANGE[1]
            if port < min_port:
                return r[str].fail(f"Port must be at least {min_port}")
            if port > max_port:
                return r[str].fail(f"Port must be at most {max_port}")
            return r[str].ok("")

        def create(
            self,
            name: str,
            port: int = c.Web.WebDefaults.PORT,
            host: str = c.Web.WebDefaults.HOST,
        ) -> r[m.Web.Entity]:
            """Create new web application with validation."""
            self.logger.info("Create app command")
            validation_result = self._validate_create_inputs(name, port, host)
            if validation_result.is_failure:
                return r[m.Web.Entity].fail(validation_result.error)
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
            return app.validate_business_rules().flat_map(
                lambda _: self._register_app(app),
            )

        def create_app(
            self,
            name: str,
            port: int = c.Web.WebDefaults.PORT,
            host: str = c.Web.WebDefaults.HOST,
        ) -> r[m.Web.Entity]:
            """Create a new application - implements WebAppManager.

            This method delegates to the create method for protocol compliance.
            """
            return self.create(name, port, host)

        def list_apps(self) -> r[Sequence[m.Web.Entity]]:
            """List all applications - implements WebAppManager."""
            apps_list = list(self.apps_registry.values())
            return r[Sequence[m.Web.Entity]].ok(apps_list)

        def start_app(self, app_id: str) -> r[m.Web.Entity]:
            """Start an application - implements WebAppManager."""
            if app_id not in self.apps_registry:
                return r[m.Web.Entity].fail(f"Application {app_id} not found")
            app = self.apps_registry[app_id]
            return app.start().map(
                lambda updated_app: self._update_app_in_registry(app_id, updated_app),
            )

        def stop_app(self, app_id: str) -> r[m.Web.Entity]:
            """Stop an application - implements WebAppManager."""
            if app_id not in self.apps_registry:
                return r[m.Web.Entity].fail(f"Application {app_id} not found")
            app = self.apps_registry[app_id]
            return app.stop().map(
                lambda updated_app: self._update_app_in_registry(app_id, updated_app),
            )

        def _register_app(self, app: m.Web.Entity) -> r[m.Web.Entity]:
            """Register application in registry."""
            self.apps_registry[app.id] = app
            return r[m.Web.Entity].ok(app)

        def _update_app_in_registry(
            self,
            app_id: str,
            app: m.Web.Entity,
        ) -> m.Web.Entity:
            """Update application in registry."""
            self.apps_registry[app_id] = app
            return app

    @classmethod
    def handle_create_app(
        cls,
        name: str,
        port: int = c.Web.WebDefaults.PORT,
        host: str = c.Web.WebDefaults.HOST,
    ) -> r[m.Web.Entity]:
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
    def handle_start_app(cls, app: m.Web.Entity) -> r[m.Web.Entity]:
        """Handle application start requests.

        Args:
        app: Application to start

        Returns:
        r containing updated application or error

        """
        return app.start()

    @classmethod
    def handle_stop_app(cls, app: m.Web.Entity) -> r[m.Web.Entity]:
        """Handle application stop requests.

        Args:
        app: Application to stop

        Returns:
        r containing updated application or error

        """
        return app.stop()

    @classmethod
    def handle_system_info(cls) -> r[m.Web.SystemInfo]:
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
    def handle_health_check() -> r[m.Web.HealthStatus]:
        """Handle health check requests with system status.

        Returns:
        r containing health status information.

        """
        return r[m.Web.HealthStatus].ok(
            m.Web.HealthStatus(
                status=c.Web.WebResponse.STATUS_HEALTHY,
                service=c.Web.WebService.SERVICE_NAME,
                version="0.9.0",
                timestamp=u.generate_iso_timestamp(),
                components={
                    "web_service": c.Web.WebResponse.STATUS_OPERATIONAL,
                    "configuration": c.Web.WebMessages.CONFIG_LOADED,
                    "handlers": c.Web.WebMessages.HANDLERS_REGISTERED,
                },
            ),
        )

    @override
    def execute(self, **_kwargs: str | float | bool | None) -> r[bool]:
        """Execute web handler service (FlextService requirement).

        Returns:
            r[bool]: Success contains True if handlers are operational,
            failure contains error message

        """
        return r[bool].ok(value=True)

    @override
    def validate_business_rules(self) -> r[bool]:
        """Validate business rules for web handlers (FlextService requirement).

        Returns:
            r[bool]: Success contains True if valid, failure with error message

        """
        return r[bool].ok(value=True)
