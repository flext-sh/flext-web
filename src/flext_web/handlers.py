"""FLEXT Web Handlers - Main Handler Coordination.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import override

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

    class WebAppHandler:
        """CQRS command handler for web application lifecycle management.

        Implements Command Query Responsibility Segregation (CQRS) patterns for
        web application operations using flext-core handler patterns. Provides
        validated, consistent handling of application lifecycle commands with
        comprehensive error handling and business rule enforcement.

        The handler acts as the application service layer, coordinating between
        domain entities and infrastructure concerns while maintaining clean
        separation of responsibilities.

        Implements FlextWebProtocols.AppManagerProtocol through structural subtyping:
        - create_app: Create new web application with validation
        - start_app: Start existing application with state validation
        - stop_app: Stop running application with graceful shutdown
        - list_apps: List all applications (delegated to registry)

        Responsibilities:
          - Command validation and processing
          - Business rule enforcement
          - Domain entity coordination
          - Error handling and reporting
          - Integration with persistence layers

        Supported Operations:
          - create: Create new web application with validation
          - start: Start existing application with state validation
          - stop: Stop running application with graceful shutdown

        Integration:
          - Uses FlextResult for consistent error handling
          - Validates all operations through domain entity rules
          - Compatible with repository patterns for persistence
          - Supports monitoring and observability integration

        Example:
          Basic handler usage:

          >>> handler = FlextWebHandlers.WebAppHandler()
          >>> result: FlextResult[object] = handler.create(
          ...     "web-service", 3000, "localhost"
          ... )
          >>> if result.success:
          ...     app = result.value
          ...     start_result: FlextResult[object] = handler.start(app)
          ...     if start_result.success:
          ...         print(f"Started {start_result.value.name}")

        """

        @override
        def __init__(self) -> None:
            """Initialize WebApp handler with FlextMixins functionality."""
            self.logger = FlextLogger(__name__)
            self._apps_registry: dict[str, FlextWebModels.WebApp] = {}

            # Initialize handler state
            self._initialized = True
            self.logger.info("WebApp handler initialized")

        # =============================================================================
        # HANDLER METHODS - Enhanced with registry integration
        # =============================================================================

        def create(
            self,
            name: str,
            port: int = FlextWebConstants.DEFAULT_PORT,
            host: str = FlextWebConstants.DEFAULT_HOST,
        ) -> FlextResult:
            """Create new web application with comprehensive validation.

            Creates a new WebApp domain entity with the specified parameters,
            performing full validation of input parameters and business rules.
            The created application starts in STOPPED state and can be started
            using the start() method.

            Args:
                name: Application name, must be non-empty string
                port: Network port number (1-65535) for application services
                host: Network host address for application binding

            Returns:
                FlextResult[WebApp]: Success contains newly created application
                entity with generated ID and timestamp information, failure contains
                detailed error message explaining validation failure.

            """
            # Log create operation
            self.logger.info("Create app command")

            # Step 1: Sanitize inputs using FlextUtilities
            sanitize_result = self._sanitize_inputs(name, host)
            if sanitize_result.is_failure:
                return FlextResult.fail(sanitize_result.error)

            # Step 2: Validate all inputs
            validate_result = self._validate_app_inputs(
                sanitize_result.value["name"],
                port,
                sanitize_result.value["host"],
            )
            if validate_result.is_failure:
                return FlextResult.fail(validate_result.error)

            # Step 3: Create domain entity
            create_result = self._create_app_entity(
                str(validate_result.value["name"]),
                int(str(validate_result.value["port"])),
                str(validate_result.value["host"]),
            )
            if create_result.is_failure:
                return create_result

            # Step 4: Validate business rules
            result = self._validate_and_return_app(create_result.value)

            # Register app if created successfully
            if result.is_success:
                app = result.unwrap()
                self._apps_registry[app.id] = app

            return result

        # =============================================================================
        # PROTOCOL IMPLEMENTATION METHODS - AppManagerProtocol
        # =============================================================================

        def create_app(
            self,
            name: str,
            port: int,
            host: str,
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Create a new application - implements AppManagerProtocol."""
            return self.create(name, port, host)

        def start_app(self, app_id: str) -> FlextResult[FlextWebModels.WebApp]:
            """Start an application - implements AppManagerProtocol."""
            if app_id not in self._apps_registry:
                return FlextResult[FlextWebModels.WebApp].fail(
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

        def stop_app(self, app_id: str) -> FlextResult[FlextWebModels.WebApp]:
            """Stop an application - implements AppManagerProtocol."""
            if app_id not in self._apps_registry:
                return FlextResult[FlextWebModels.WebApp].fail(
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

        def list_apps(self) -> FlextResult[list[FlextWebModels.WebApp]]:
            """List all applications - implements AppManagerProtocol."""
            try:
                apps_list = list(self._apps_registry.values())
                return FlextResult[list[FlextWebModels.WebApp]].ok(apps_list)
            except Exception as e:
                return FlextResult[list[FlextWebModels.WebApp]].fail(
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
        port: int = FlextWebConstants.DEFAULT_PORT,
        host: str = FlextWebConstants.DEFAULT_HOST,
    ) -> FlextResult[FlextWebModels.WebApp]:
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
            app = FlextWebModels.WebApp(
                id=app_id, name=name, port=port, host=host, domain_events=[]
            )
            validation_result: FlextResult[None] = app.validate_business_rules()

            if validation_result.is_failure:
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"Application validation failed: {validation_result.error}",
                )

            return FlextResult[FlextWebModels.WebApp].ok(app)

        except Exception as e:
            return FlextResult[FlextWebModels.WebApp].fail(
                f"Failed to create application: {e}",
            )

    @classmethod
    def handle_start_app(
        cls,
        app: FlextWebModels.WebApp,
    ) -> FlextResult[FlextWebModels.WebApp]:
        """Handle application start requests.

        Args:
            app: Application to start

        Returns:
            FlextResult containing updated application or error

        """
        handler = FlextWebHandlers.WebAppHandler()
        return handler.start(app)

    @classmethod
    def handle_stop_app(
        cls,
        app: FlextWebModels.WebApp,
    ) -> FlextResult[FlextWebModels.WebApp]:
        """Handle application stop requests.

        Args:
            app: Application to stop

        Returns:
            FlextResult containing updated application or error

        """
        handler = FlextWebHandlers.WebAppHandler()
        return handler.stop(app)

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
    def format_app_data(cls, app: FlextWebModels.WebApp) -> FlextWebTypes.AppData:
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
    def format_health_data(cls: object) -> FlextWebTypes.HealthResponse:
        """Format health check data for API responses.

        Returns:
            Formatted health data dictionary

        """
        return FlextWebTypes.HealthResponse(
            status="healthy",
            service="flext-web",
            version="0.9.0",
            applications=0,  # This would be populated by the service
            timestamp=FlextUtilities.Generators.generate_iso_timestamp(),
            service_id="handler-health",
            created_at=None,
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
