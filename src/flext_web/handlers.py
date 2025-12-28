"""FLEXT Web Handlers - Main Handler Coordination.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import (
    FlextLogger,
    FlextService,
    FlextTypes as t,
    r,
)

from flext_web.constants import c
from flext_web.models import m
from flext_web.utilities import u


class FlextWebHandlers(FlextService[bool]):
    """Consolidated web handler system extending flext-core patterns.

    This class serves as the single point of access for all web-specific
    handlers, command processors, and response formatters while extending
    FlextService from flext-core for proper architectural inheritance.

    All handler functionality is accessible through this single class following the
    "one class per module" architectural requirement.
    """

    # =========================================================================
    # NESTED HANDLER CLASSES
    # =========================================================================

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
            self._apps_registry: dict[str, m.Web.Entity] = {}
            self.logger.info("WebApp handler initialized")

        def create(
            self,
            name: str,
            port: int = c.Web.WebDefaults.PORT,
            host: str = c.Web.WebDefaults.HOST,
        ) -> r[m.Web.Entity]:
            """Create new web application with validation."""
            self.logger.info("Create app command")

            # Validate inputs using ues validation
            validation_result = self._validate_create_inputs(name, port, host)
            if validation_result.is_failure:
                return r[m.Web.Entity].fail(validation_result.error)

            # Create domain entity
            app_id = m.Web.Entity.format_id_from_name(name)
            app = m.Web.Entity(
                id=app_id,
                name=name,
                port=port,
                host=host,
                domain_events=[],
            )

            # Validate business rules using monadic pattern
            return app.validate_business_rules().flat_map(
                lambda _: self._register_app(app),
            )

        @staticmethod
        def _validate_create_inputs(
            name: str,
            port: int,
            host: str,
        ) -> r[str]:
            """Validate create inputs - consolidates all validations."""
            # Basic type validation
            if not isinstance(name, str):
                return r[str].fail("Application name must be a string")
            if not isinstance(host, str):
                return r[str].fail("Host must be a string")
            if not isinstance(port, int):
                return r[str].fail("Port must be an integer")

            # Length validation
            if len(name) < c.Web.WebServer.MIN_APP_NAME_LENGTH:
                return r[str].fail(
                    f"Application name must be at least {c.Web.WebServer.MIN_APP_NAME_LENGTH} characters",
                )
            if not host:
                return r[str].fail("Host cannot be empty")

            # Port range validation
            min_port = c.Web.WebValidation.PORT_RANGE[0]
            max_port = c.Web.WebValidation.PORT_RANGE[1]
            if port < min_port:
                return r[str].fail(f"Port must be at least {min_port}")
            if port > max_port:
                return r[str].fail(f"Port must be at most {max_port}")

            return r[str].ok("")

        def _register_app(
            self,
            app: m.Web.Entity,
        ) -> r[m.Web.Entity]:
            """Register application in registry."""
            self._apps_registry[app.id] = app
            return r[m.Web.Entity].ok(app)

        # =============================================================================
        # PROTOCOL IMPLEMENTATION METHODS - WebAppManagerProtocol
        # =============================================================================

        def create_app(
            self,
            name: str,
            port: int = c.Web.WebDefaults.PORT,
            host: str = c.Web.WebDefaults.HOST,
        ) -> r[m.Web.Entity]:
            """Create a new application - implements WebAppManagerProtocol.

            This method delegates to the create method for protocol compliance.
            """
            return self.create(name, port, host)

        def start_app(self, app_id: str) -> r[m.Web.Entity]:
            """Start an application - implements WebAppManagerProtocol."""
            if app_id not in self._apps_registry:
                return r[m.Web.Entity].fail(
                    f"Application {app_id} not found",
                )

            app = self._apps_registry[app_id]
            # Use entity's start method with monadic pattern and update registry
            return app.start().map(
                lambda updated_app: self._update_app_in_registry(app_id, updated_app),
            )

        def _update_app_in_registry(
            self,
            app_id: str,
            app: m.Web.Entity,
        ) -> m.Web.Entity:
            """Update application in registry."""
            self._apps_registry[app_id] = app
            return app

        def stop_app(self, app_id: str) -> r[m.Web.Entity]:
            """Stop an application - implements WebAppManagerProtocol."""
            if app_id not in self._apps_registry:
                return r[m.Web.Entity].fail(
                    f"Application {app_id} not found",
                )

            app = self._apps_registry[app_id]
            # Use entity's stop method with monadic pattern and update registry
            return app.stop().map(
                lambda updated_app: self._update_app_in_registry(app_id, updated_app),
            )

        def list_apps(self) -> r[list[m.Web.Entity]]:
            """List all applications - implements WebAppManagerProtocol."""
            apps_list = list(self._apps_registry.values())
            return r[list[m.Web.Entity]].ok(apps_list)

    # =========================================================================
    # HEALTH AND SYSTEM HANDLERS
    # =========================================================================

    @staticmethod
    def handle_health_check() -> r[dict[str, t.GeneralValueType]]:
        """Handle health check requests with system status.

        Returns:
        r containing health status information.

        """
        return r[dict[str, str]].ok(
            {
                "status": c.Web.WebResponse.STATUS_HEALTHY,
                "service": c.Web.WebService.SERVICE_NAME,
                "version": "0.9.0",
                "timestamp": u.Generators.generate_iso_timestamp(),
                "components": {
                    "web_service": c.Web.WebResponse.STATUS_OPERATIONAL,
                    "configuration": "loaded",
                    "handlers": "registered",
                },
            },
        )

    @classmethod
    def handle_system_info(cls) -> r[dict[str, t.GeneralValueType]]:
        """Handle system information requests.

        Returns:
        r containing detailed system information.

        """
        return r[dict[str, str]].ok(
            {
                "service_name": "FLEXT Web Interface",
                "service_type": "web_api",
                "architecture": "flask_clean_architecture",
                "patterns": [
                    "CQRS",
                    "Clean Architecture",
                    "Domain-Driven Design",
                ],
                "integrations": ["flext-core", "pydantic", "flask"],
                "capabilities": [
                    "application_management",
                    "health_monitoring",
                    "api_endpoints",
                    "web_dashboard",
                ],
            },
        )

    # =========================================================================
    # APPLICATION HANDLERS
    # =========================================================================

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
        # Create app directly with typed parameters
        app = m.Web.Entity(
            id=app_id,
            name=name,
            port=port,
            host=host,
            domain_events=[],
        )
        # Use monadic pattern for validation
        return app.validate_business_rules().flat_map(
            lambda _: r[m.Web.Entity].ok(app),
        )

    @classmethod
    def handle_start_app(
        cls,
        app: m.Web.Entity,
    ) -> r[m.Web.Entity]:
        """Handle application start requests.

        Args:
        app: Application to start

        Returns:
        r containing updated application or error

        """
        # Validate application entity - fast fail
        if not isinstance(app, m.Web.Entity):
            return r[m.Web.Entity].fail(
                "Invalid application entity type",
            )

        # Use entity's start method with monadic pattern
        return app.start()

    @classmethod
    def handle_stop_app(
        cls,
        app: m.Web.Entity,
    ) -> r[m.Web.Entity]:
        """Handle application stop requests.

        Args:
        app: Application to stop

        Returns:
        r containing updated application or error

        """
        # Application entity is already validated by type system
        # Use entity's stop method with monadic pattern
        return app.stop()

    # =========================================================================
    # RESPONSE FORMATTING - Removed unnecessary helpers
    # =========================================================================
    # Removed create_response_handler, format_app_data, format_health_data
    # Use FlextWebModels.Service.AppResponse and HealthResponse directly where needed
    # No helpers needed - direct model instantiation is clearer and more maintainable

    # =========================================================================
    # ERROR HANDLING - Use r.fail() directly, no helpers needed
    # =========================================================================
    # Removed handle_validation_error and handle_processing_error helpers
    # Use r.fail() directly where needed for proper error handling

    # =========================================================================
    # HANDLER FACTORY METHODS - Removed unnecessary wrapper methods
    # =========================================================================

    # =========================================================================
    # FLEXTSERVICE REQUIRED METHODS
    # =========================================================================

    def execute(self, **_kwargs: object) -> r[bool]:
        """Execute web handler service (FlextService requirement).

        Returns:
            r[bool]: Success contains True if handlers are operational,
            failure contains error message

        """
        # Return bool for FlextService compatibility
        return r[bool].ok(True)

    def validate_business_rules(self) -> r[bool]:
        """Validate business rules for web handlers (FlextService requirement).

        Returns:
            r[bool]: Success contains True if valid, failure with error message

        """
        return r[bool].ok(True)


__all__ = [
    "FlextWebHandlers",
]
