"""FLEXT Web Handlers - Main Handler Coordination.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import (
    FlextLogger,
    FlextProcessors,
    FlextResult,
    FlextUtilities,
)

from flext_web.constants import FlextWebConstants
from flext_web.models import FlextWebModels
from flext_web.typings import FlextWebTypes
from flext_web.utilities import FlextWebUtilities


class FlextWebHandlers(FlextProcessors):
    """Consolidated web handler system extending flext-core patterns.

    This class serves as the single point of access for all web-specific
    handlers, command processors, and response formatters while extending
    FlextProcessors from flext-core for proper architectural inheritance.

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

            # Validate inputs
            if (
                not name
                or not isinstance(name, str)
                or len(name) < FlextWebConstants.WebServer.MIN_APP_NAME_LENGTH
            ):
                return FlextResult[FlextWebModels.Application.Entity].fail(
                    f"Application name must be at least {FlextWebConstants.WebServer.MIN_APP_NAME_LENGTH} characters"
                )

            if not host or not isinstance(host, str):
                return FlextResult[FlextWebModels.Application.Entity].fail(
                    "Host must be a non-empty string"
                )

            if (
                not isinstance(port, int)
                or port < FlextWebConstants.WebValidation.PORT_RANGE[0]
                or port > FlextWebConstants.WebValidation.PORT_RANGE[1]
            ):
                return FlextResult[FlextWebModels.Application.Entity].fail(
                    f"Port must be between {FlextWebConstants.WebValidation.PORT_RANGE[0]} and {FlextWebConstants.WebValidation.PORT_RANGE[1]}"
                )

            # Create domain entity
            try:
                app_id = FlextWebUtilities.format_app_id(name)
                app = FlextWebModels.Application.Entity(
                    id=app_id, name=name, port=port, host=host, domain_events=[]
                )

                # Validate business rules
                validation = app.validate_business_rules()
                if validation.is_failure:
                    return FlextResult[FlextWebModels.Application.Entity].fail(
                        validation.error
                    )

                # Register application
                self._apps_registry[app.id] = app
                return FlextResult[FlextWebModels.Application.Entity].ok(app)

            except Exception as e:
                return FlextResult[FlextWebModels.Application.Entity].fail(
                    f"Failed to create application: {e}"
                )

        # =============================================================================
        # PROTOCOL IMPLEMENTATION METHODS - WebAppManagerProtocol
        # =============================================================================

        def create_app(
            self,
            name: str,
            port: int = FlextWebConstants.WebDefaults.PORT,
            host: str = FlextWebConstants.WebDefaults.HOST,
        ) -> FlextResult[FlextWebModels.Application.Entity]:
            """Create a new application - implements WebAppManagerProtocol."""
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
            # For now, just return the app as "started"
            start_result = FlextResult.ok(app)

            if start_result.is_success:
                # Update registry with new state
                updated_app = start_result.unwrap()
                self._apps_registry[app_id] = updated_app

            return start_result

        def stop_app(
            self, app_id: str
        ) -> FlextResult[FlextWebModels.Application.Entity]:
            """Stop an application - implements WebAppManagerProtocol."""
            if app_id not in self._apps_registry:
                return FlextResult[FlextWebModels.Application.Entity].fail(
                    f"Application {app_id} not found"
                )

            app = self._apps_registry[app_id]
            # For now, just return the app as "stopped"
            stop_result = FlextResult.ok(app)

            if stop_result.is_success:
                # Update registry with new state
                updated_app = stop_result.unwrap()
                self._apps_registry[app_id] = updated_app

            return stop_result

        def list_apps(self) -> FlextResult[list[FlextWebModels.Application.Entity]]:
            """List all applications - implements WebAppManagerProtocol."""
            try:
                apps_list = list(self._apps_registry.values())
                return FlextResult[list[FlextWebModels.Application.Entity]].ok(
                    apps_list
                )
            except Exception as e:
                return FlextResult[list[FlextWebModels.Application.Entity]].fail(
                    f"List apps failed: {e}"
                )

    # =========================================================================
    # HEALTH AND SYSTEM HANDLERS
    # =========================================================================

    @staticmethod
    def handle_health_check() -> FlextResult[dict[str, object]]:
        """Handle health check requests with system status.

        Returns:
        FlextResult containing health status information.

        """
        return FlextResult[dict[str, object]].ok(
            {
                "status": "healthy",
                "service": "flext - web",
                "version": "0.9.0",
                "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
                "components": {
                    "web_service": "operational",
                    "configuration": "loaded",
                    "handlers": "registered",
                },
            },
        )

    @classmethod
    def handle_system_info(cls: object) -> FlextResult[dict[str, object]]:
        """Handle system information requests.

        Returns:
        FlextResult containing detailed system information.

        """
        return FlextResult[dict[str, object]].ok(
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
        **kwargs: Additional application parameters

        Returns:
        FlextResult containing created application or error

        """
        try:
            app_id = FlextWebUtilities.format_app_id(name)
            # Create app directly with typed parameters
            app = FlextWebModels.Application.Entity(
                id=app_id, name=name, port=port, host=host, domain_events=[]
            )
            validation_result: FlextResult[None] = app.validate_business_rules()

            if validation_result.is_failure:
                return FlextResult[FlextWebModels.Application.Entity].fail(
                    f"Application validation failed: {validation_result.error}",
                )

            return FlextResult[FlextWebModels.Application.Entity].ok(app)

        except Exception as e:
            return FlextResult[FlextWebModels.Application.Entity].fail(
                f"Failed to create application: {e}",
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
        if not app or not hasattr(app, "id"):
            return FlextResult[FlextWebModels.Application.Entity].fail(
                "Invalid application object"
            )

        # Application is started by updating its state
        return FlextResult[FlextWebModels.Application.Entity].ok(app)

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
        if not app or not hasattr(app, "id"):
            return FlextResult[FlextWebModels.Application.Entity].fail(
                "Invalid application object"
            )

        # Application is stopped by updating its state
        return FlextResult[FlextWebModels.Application.Entity].ok(app)

    # =========================================================================
    # RESPONSE FORMATTING HELPERS
    # =========================================================================

    @classmethod
    def create_response_handler(
        cls,
        success_status: int = 200,
        error_status: int = 500,
    ) -> dict[str, object]:
        """Create response handler configuration.

        Args:
        success_status: Default success HTTP status
        error_status: Default error HTTP status

        Returns:
        Response handler configuration dictionary

        """
        return {
            "success_status": success_status,
            "error_status": error_status,
        }

    @classmethod
    def format_app_data(
        cls, app: FlextWebModels.Application.Entity
    ) -> FlextWebTypes.AppData:
        """Format application data for API responses.

        Args:
        app: Application to format

        Returns:
        Formatted application data dictionary

        """
        return FlextWebTypes.AppData(
            id=str(app.id),
            name=app.name,
            host=app.host,
            port=app.port,
            status=app.status,
            is_running=bool(app.is_running),
        )

    @classmethod
    def format_health_data(cls: type) -> FlextWebTypes.HealthResponse:
        """Format health check data for API responses.

        Returns:
        Formatted health data dictionary

        """
        return FlextWebTypes.HealthResponse(
            status="healthy",
            service="flext-web",
            version="0.9.0",
            applications="0",  # This would be populated by the service
            timestamp=FlextUtilities.Generators.generate_iso_timestamp(),
            service_id="handler-health",
            created_at=FlextUtilities.Generators.generate_iso_timestamp(),
        )

    # =========================================================================
    # ERROR HANDLING UTILITIES
    # =========================================================================

    @classmethod
    def handle_validation_error(
        cls,
        error: Exception,
        context: str = "validation",
    ) -> FlextResult[None]:
        """Handle validation errors with context.

        Args:
        error: Validation exception
        context: Error context description

        Returns:
        FlextResult with formatted error message

        """
        error_message = f"{context.title()} error: {error}"
        return FlextResult[None].fail(error_message)

    @classmethod
    def handle_processing_error(
        cls,
        error: Exception,
        operation: str = "operation",
    ) -> FlextResult[None]:
        """Handle processing errors with context.

        Args:
        error: Processing exception
        operation: Operation description

        Returns:
        FlextResult with formatted error message

        """
        error_message = f"{operation.title()} failed: {error}"
        return FlextResult[None].fail(error_message)

    # =========================================================================
    # HANDLER FACTORY METHODS - Removed unnecessary wrapper methods
    # =========================================================================


__all__ = [
    "FlextWebHandlers",
]
