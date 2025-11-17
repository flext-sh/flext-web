"""FLEXT Web Handlers - Main Handler Coordination.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import (
    FlextLogger,
    FlextResult,
    FlextService,
    FlextUtilities,
)

from flext_web.constants import FlextWebConstants
from flext_web.models import FlextWebModels
from flext_web.typings import FlextWebTypes


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
            self._apps_registry: dict[str, FlextWebModels.Application.Entity] = {}
            self.logger.info("WebApp handler initialized")

        def create(
            self,
            name: str,
            port: int = FlextWebConstants.WebDefaults.PORT,
            host: str = FlextWebConstants.WebDefaults.HOST,
        ) -> FlextResult[FlextWebModels.Application.Entity]:
            """Create new web application with validation."""
            self.logger.info("Create app command")

            # Validate inputs - fast fail, no fallbacks
            if not isinstance(name, str):
                return FlextResult[FlextWebModels.Application.Entity].fail(
                    "Application name must be a string"
                )
            if len(name) < FlextWebConstants.WebServer.MIN_APP_NAME_LENGTH:
                return FlextResult[FlextWebModels.Application.Entity].fail(
                    f"Application name must be at least {FlextWebConstants.WebServer.MIN_APP_NAME_LENGTH} characters"
                )

            if not isinstance(host, str):
                return FlextResult[FlextWebModels.Application.Entity].fail(
                    "Host must be a string"
                )
            if len(host) == 0:
                return FlextResult[FlextWebModels.Application.Entity].fail(
                    "Host cannot be empty"
                )

            if not isinstance(port, int):
                return FlextResult[FlextWebModels.Application.Entity].fail(
                    "Port must be an integer"
                )
            min_port = FlextWebConstants.WebValidation.PORT_RANGE[0]
            max_port = FlextWebConstants.WebValidation.PORT_RANGE[1]
            if port < min_port:
                return FlextResult[FlextWebModels.Application.Entity].fail(
                    f"Port must be at least {min_port}"
                )
            if port > max_port:
                return FlextResult[FlextWebModels.Application.Entity].fail(
                    f"Port must be at most {max_port}"
                )

            # Create domain entity
            app_id = FlextWebModels.Application.Entity.format_id_from_name(name)
            app = FlextWebModels.Application.Entity(
                id=app_id, name=name, port=port, host=host, domain_events=[]
            )

            # Validate business rules using monadic pattern
            return app.validate_business_rules().flat_map(
                lambda _: self._register_app(app)
            )

        def _register_app(
            self, app: FlextWebModels.Application.Entity
        ) -> FlextResult[FlextWebModels.Application.Entity]:
            """Register application in registry."""
            self._apps_registry[app.id] = app
            return FlextResult[FlextWebModels.Application.Entity].ok(app)

        # =============================================================================
        # PROTOCOL IMPLEMENTATION METHODS - WebAppManagerProtocol
        # =============================================================================

        def create_app(
            self,
            name: str,
            port: int = FlextWebConstants.WebDefaults.PORT,
            host: str = FlextWebConstants.WebDefaults.HOST,
        ) -> FlextResult[FlextWebModels.Application.Entity]:
            """Create a new application - implements WebAppManagerProtocol.

            This method delegates to the create method for protocol compliance.
            """
            return self.create(name, port, host)

        def start_app(
            self, app_id: str
        ) -> FlextResult[FlextWebModels.Application.Entity]:
            """Start an application - implements WebAppManagerProtocol."""
            if app_id not in self._apps_registry:
                return FlextResult[FlextWebModels.Application.Entity].fail(
                    f"Application {app_id} not found"
                )

            app = self._apps_registry[app_id]
            # Use entity's start method with monadic pattern and update registry
            return app.start().map(
                lambda updated_app: self._update_app_in_registry(app_id, updated_app)
            )

        def _update_app_in_registry(
            self,
            app_id: str,
            app: FlextWebModels.Application.Entity,
        ) -> FlextWebModels.Application.Entity:
            """Update application in registry."""
            self._apps_registry[app_id] = app
            return app

        def stop_app(
            self, app_id: str
        ) -> FlextResult[FlextWebModels.Application.Entity]:
            """Stop an application - implements WebAppManagerProtocol."""
            if app_id not in self._apps_registry:
                return FlextResult[FlextWebModels.Application.Entity].fail(
                    f"Application {app_id} not found"
                )

            app = self._apps_registry[app_id]
            # Use entity's stop method with monadic pattern and update registry
            return app.stop().map(
                lambda updated_app: self._update_app_in_registry(app_id, updated_app)
            )

        def list_apps(self) -> FlextResult[list[FlextWebModels.Application.Entity]]:
            """List all applications - implements WebAppManagerProtocol."""
            apps_list = list(self._apps_registry.values())
            return FlextResult[list[FlextWebModels.Application.Entity]].ok(apps_list)

    # =========================================================================
    # HEALTH AND SYSTEM HANDLERS
    # =========================================================================

    @staticmethod
    def handle_health_check() -> FlextResult[FlextWebTypes.Core.ResponseDict]:
        """Handle health check requests with system status.

        Returns:
        FlextResult containing health status information.

        """
        return FlextResult[FlextWebTypes.Core.ResponseDict].ok(
            {
                "status": FlextWebConstants.WebResponse.STATUS_HEALTHY,
                "service": FlextWebConstants.WebService.SERVICE_NAME,
                "version": "0.9.0",
                "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
                "components": {
                    "web_service": FlextWebConstants.WebResponse.STATUS_OPERATIONAL,
                    "configuration": "loaded",
                    "handlers": "registered",
                },
            },
        )

    @classmethod
    def handle_system_info(cls) -> FlextResult[FlextWebTypes.Core.ResponseDict]:
        """Handle system information requests.

        Returns:
        FlextResult containing detailed system information.

        """
        return FlextResult[FlextWebTypes.Core.ResponseDict].ok(
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
        port: int = FlextWebConstants.WebDefaults.PORT,
        host: str = FlextWebConstants.WebDefaults.HOST,
    ) -> FlextResult[FlextWebModels.Application.Entity]:
        """Handle application creation requests.

        Args:
        name: Application name
        port: Application port
        host: Application host

        Returns:
        FlextResult containing created application or error

        """
        app_id = FlextWebModels.Application.Entity.format_id_from_name(name)
        # Create app directly with typed parameters
        app = FlextWebModels.Application.Entity(
            id=app_id, name=name, port=port, host=host, domain_events=[]
        )
        # Use monadic pattern for validation
        return app.validate_business_rules().flat_map(
            lambda _: FlextResult[FlextWebModels.Application.Entity].ok(app)
        )

    @classmethod
    def handle_start_app(
        cls,
        app: FlextWebModels.Application.Entity,
    ) -> FlextResult[FlextWebModels.Application.Entity]:
        """Handle application start requests.

        Args:
        app: Application to start

        Returns:
        FlextResult containing updated application or error

        """
        # Validate application entity - fast fail
        if not isinstance(app, FlextWebModels.Application.Entity):
            return FlextResult[FlextWebModels.Application.Entity].fail(
                "Invalid application entity type"
            )

        # Use entity's start method with monadic pattern
        return app.start()

    @classmethod
    def handle_stop_app(
        cls,
        app: FlextWebModels.Application.Entity,
    ) -> FlextResult[FlextWebModels.Application.Entity]:
        """Handle application stop requests.

        Args:
        app: Application to stop

        Returns:
        FlextResult containing updated application or error

        """
        # Validate application entity - fast fail
        if not isinstance(app, FlextWebModels.Application.Entity):
            return FlextResult[FlextWebModels.Application.Entity].fail(
                "Invalid application entity type"
            )

        # Use entity's stop method with monadic pattern
        return app.stop()

    # =========================================================================
    # RESPONSE FORMATTING - Removed unnecessary helpers
    # =========================================================================
    # Removed create_response_handler, format_app_data, format_health_data
    # Use FlextWebModels.Service.AppResponse and HealthResponse directly where needed
    # No helpers needed - direct model instantiation is clearer and more maintainable

    # =========================================================================
    # ERROR HANDLING - Use FlextResult.fail() directly, no helpers needed
    # =========================================================================
    # Removed handle_validation_error and handle_processing_error helpers
    # Use FlextResult.fail() directly where needed for proper error handling

    # =========================================================================
    # HANDLER FACTORY METHODS - Removed unnecessary wrapper methods
    # =========================================================================

    # =========================================================================
    # FLEXTSERVICE REQUIRED METHODS
    # =========================================================================

    def execute(self) -> FlextResult[bool]:
        """Execute web handler service (FlextService requirement).

        Returns:
            FlextResult[bool]: Success contains True if handlers are operational,
            failure contains error message

        """
        # Return bool for FlextService compatibility
        return FlextResult[bool].ok(True)

    def validate_business_rules(self) -> FlextResult[bool]:
        """Validate business rules for web handlers (FlextService requirement).

        Returns:
            FlextResult[bool]: Success contains True if valid, failure with error message

        """
        return FlextResult[bool].ok(True)


__all__ = [
    "FlextWebHandlers",
]
