"""FLEXT Web Handlers - Consolidated handler system extending flext-core patterns.

This module implements the consolidated handler architecture following the
"one class per module" pattern, with FlextWebHandlers extending FlextHandlers
and containing all web-specific handler functionality as nested classes and methods.
"""

from __future__ import annotations

from flask import jsonify
from flask.typing import ResponseReturnValue
from flext_core import FlextEntityId, FlextHandlers, FlextResult

from flext_web.models import FlextWebApp, FlextWebModels
from flext_web.typings import FlextWebTypes

# =============================================================================
# CONSOLIDATED HANDLERS CLASS
# =============================================================================


class FlextWebHandlers(FlextHandlers):
    """Consolidated web handler system extending flext-core patterns.

    This class serves as the single point of access for all web-specific
    handlers, command processors, and response formatters while extending
    FlextHandlers from flext-core for proper architectural inheritance.

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
          >>> result = handler.create("web-service", 3000, "localhost")
          >>> if result.success:
          ...     app = result.value
          ...     start_result = handler.start(app)
          ...     if start_result.success:
          ...         print(f"Started {start_result.value.name}")

        """

        def create(
            self,
            name: str,
            port: int = 8000,
            host: str = "localhost",
        ) -> FlextResult[FlextWebModels.WebApp]:
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

            Business Rules:
                - Application name must be non-empty string
                - Port must be within valid range (1-65535)
                - Host must be non-empty string
                - Application ID is automatically generated as "app_{name}"

            Side Effects:
                - Creates new domain entity with timestamp information
                - Assigns unique identifier for application tracking
                - Initializes application in STOPPED state

            Example:
                >>> handler = FlextWebHandlers.WebAppHandler()
                >>> result = handler.create("web-api", 8080, "0.0.0.0")
                >>> if result.success:
                ...     app = result.value
                ...     print(
                ...         f"Created: {app.name} [{app.id}] at {app.host}:{app.port}"
                ...     )
                ... else:
                ...     print(f"Creation failed: {result.error}")

            """
            try:
                # Create domain entity with generated ID
                entity_id = FlextEntityId(f"app_{name}")
                app = FlextWebModels.WebApp(
                    id=entity_id, name=name, port=port, host=host
                )

                # Validate domain rules before returning
                validation = app.validate_business_rules()
                if not validation.success:
                    return FlextResult["FlextWebModels.WebApp"].fail(
                        validation.error or "Domain validation failed"
                    )

                return FlextResult["FlextWebModels.WebApp"].ok(app)
            except (RuntimeError, ValueError, TypeError) as e:
                return FlextResult["FlextWebModels.WebApp"].fail(
                    f"Application creation failed: {e}"
                )

        def start(
            self, app: FlextWebModels.WebApp
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Start web application with validation and state management.

            Initiates the startup process for a web application, performing
            validation checks and state transitions according to business rules.
            The operation is atomic and maintains consistency of application state.

            Args:
                app: WebApp entity to start, must be in valid state for starting

            Returns:
                FlextResult[WebApp]: Success contains updated application entity
                with RUNNING status, failure contains error message explaining why
                the application cannot be started.

            Pre-conditions:
                - Application must be in STOPPED or ERROR state
                - Application configuration must pass validation
                - All domain rules must be satisfied

            Post-conditions:
                - Application status updated to RUNNING on success
                - Domain events triggered for monitoring integration

            Business Rules:
                - Applications already RUNNING cannot be started again
                - Applications in STARTING state cannot be started
                - State transitions must follow defined state machine
                - All validation rules must pass before state change

            Example:
                >>> handler = FlextWebHandlers.WebAppHandler()
                >>> app = FlextWebModels.WebApp(
                ...     name="service", status=FlextWebModels.WebAppStatus.STOPPED
                ... )
                >>> result = handler.start(app)
                >>> if result.success:
                ...     running_app = result.value
                ...     print(
                ...         f"Started: {running_app.name} is now {running_app.status.value}"
                ...     )
                ... else:
                ...     print(f"Start failed: {result.error}")

            """
            # Validate domain rules before attempting state change
            validation = app.validate_domain_rules()
            if not validation.success:
                return FlextResult["FlextWebModels.WebApp"].fail(
                    validation.error or "Validation failed"
                )

            # Delegate to domain entity for state transition
            return app.start()

        def stop(
            self, app: FlextWebModels.WebApp
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Stop web application with graceful shutdown and validation.

            Initiates the shutdown process for a running web application, performing
            validation checks and state transitions according to business rules.
            The operation ensures graceful shutdown with proper cleanup.

            Args:
                app: WebApp entity to stop, must be in valid state for stopping

            Returns:
                FlextResult[WebApp]: Success contains updated application entity
                with STOPPED status, failure contains error message explaining why
                the application cannot be stopped.

            Pre-conditions:
                - Application must be in RUNNING or ERROR state
                - Application must exist and be valid
                - All domain rules must be satisfied

            Post-conditions:
                - Application status updated to STOPPED on success
                - Domain events triggered for monitoring integration
                - Resources properly released and cleaned up

            Business Rules:
                - Applications already STOPPED cannot be stopped again
                - Applications in STOPPING state cannot be stopped
                - State transitions must follow defined state machine
                - Graceful shutdown procedures must be followed

            Example:
                >>> handler = FlextWebHandlers.WebAppHandler()
                >>> app = FlextWebModels.WebApp(
                ...     name="service", status=FlextWebModels.WebAppStatus.RUNNING
                ... )
                >>> result = handler.stop(app)
                >>> if result.success:
                ...     stopped_app = result.value
                ...     print(
                ...         f"Stopped: {stopped_app.name} is now {stopped_app.status.value}"
                ...     )
                ... else:
                ...     print(f"Stop failed: {result.error}")

            """
            # Validate domain rules before attempting state change
            validation = app.validate_domain_rules()
            if not validation.success:
                return FlextResult["FlextWebModels.WebApp"].fail(
                    validation.error or "Validation failed"
                )

            # Delegate to domain entity for state transition
            return app.stop()

    class WebResponseHandler:
        """Specialized response handler for Flask integration and JSON formatting.

        Provides consistent response formatting across all web endpoints with
        proper error handling, status codes, and structured response data.
        """

        def __init__(self, success_status: int = 200, error_status: int = 500) -> None:
            """Initialize response handler with default status codes.

            Args:
                success_status: Default HTTP status for successful responses
                error_status: Default HTTP status for error responses

            """
            self.success_status = success_status
            self.error_status = error_status

        def create_success_response(
            self,
            data: dict[str, object] | list[object] | None = None,
            message: str = "Success",
            status_code: int | None = None,
        ) -> ResponseReturnValue:
            """Create successful JSON response.

            Args:
                data: Response data
                message: Success message
                status_code: Optional HTTP status code override

            Returns:
                Flask JSON response with success format

            """
            response_data: FlextWebTypes.ResponseDataDict = {
                "success": True,
                "message": message,
                "data": data,
                "errors": None,
            }

            return jsonify(response_data), status_code or self.success_status

        def create_error_response(
            self,
            message: str,
            status_code: int | None = None,
            errors: FlextWebTypes.ErrorDetails = None,
        ) -> ResponseReturnValue:
            """Create error JSON response.

            Args:
                message: Error message
                status_code: Optional HTTP status code override
                errors: Optional detailed error information

            Returns:
                Flask JSON response with error format

            """
            response_data: FlextWebTypes.ResponseDataDict = {
                "success": False,
                "message": message,
                "data": None,
                "errors": errors,
            }

            return jsonify(response_data), status_code or self.error_status

        def handle_result(
            self,
            result: FlextResult[object],
            success_message: str = "Operation completed",
            error_message: str = "Operation failed",
        ) -> ResponseReturnValue:
            """Handle FlextResult and convert to appropriate response.

            Args:
                result: FlextResult to process
                success_message: Message for successful results
                error_message: Message for failed results

            Returns:
                Flask JSON response based on result status

            """
            if result.success:
                return self.create_success_response(
                    data=result.value
                    if isinstance(result.value, (dict, list))
                    else {"value": result.value},
                    message=success_message,
                )
            return self.create_error_response(
                message=f"{error_message}: {result.error}",
                status_code=400,  # Bad request for business logic errors
            )

    # =========================================================================
    # HEALTH AND SYSTEM HANDLERS
    # =========================================================================

    @staticmethod
    def handle_health_check() -> FlextResult[dict[str, FlextWebTypes.ResponseData]]:
        """Handle health check requests with system status.

        Returns:
            FlextResult containing health status information.

        """
        return FlextResult[dict[str, FlextWebTypes.ResponseData]].ok(
            {
                "status": "healthy",
                "service": "flext-web",
                "version": "0.9.0",
                "timestamp": "2025-01-XX",
                "components": {
                    "web_service": "operational",
                    "configuration": "loaded",
                    "handlers": "registered",
                },
            }
        )

    @classmethod
    def handle_system_info(cls) -> FlextResult[dict[str, FlextWebTypes.ResponseData]]:
        """Handle system information requests.

        Returns:
            FlextResult containing detailed system information.

        """
        return FlextResult[dict[str, FlextWebTypes.ResponseData]].ok(
            {
                "service_name": "FLEXT Web Interface",
                "service_type": "web_api",
                "architecture": "flask_clean_architecture",
                "patterns": ["CQRS", "Clean Architecture", "Domain-Driven Design"],
                "integrations": ["flext-core", "pydantic", "flask"],
                "capabilities": [
                    "application_management",
                    "health_monitoring",
                    "api_endpoints",
                    "web_dashboard",
                ],
            }
        )

    # =========================================================================
    # APPLICATION HANDLERS
    # =========================================================================

    @classmethod
    def handle_create_app(
        cls,
        name: str,
        port: int = 8000,
        host: str = "localhost",
        **kwargs: object,
    ) -> FlextResult[FlextWebApp]:
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
            # Generate ID for the app
            entity_id = FlextEntityId(f"app_{name}")
            app_data = {"id": entity_id, "name": name, "port": port, "host": host, **kwargs}
            app = FlextWebApp(**app_data)  # type: ignore[arg-type]
            validation_result = app.validate_domain_rules()

            if not validation_result.success:
                return FlextResult[FlextWebApp].fail(
                    f"Application validation failed: {validation_result.error}"
                )

            return FlextResult[FlextWebApp].ok(app)

        except Exception as e:
            return FlextResult[FlextWebApp].fail(f"Failed to create application: {e}")

    @classmethod
    def handle_start_app(cls, app: FlextWebApp) -> FlextResult[FlextWebApp]:
        """Handle application start requests.

        Args:
            app: Application to start

        Returns:
            FlextResult containing updated application or error

        """
        handler = FlextWebAppHandler()
        return handler.start(app)

    @classmethod
    def handle_stop_app(cls, app: FlextWebApp) -> FlextResult[FlextWebApp]:
        """Handle application stop requests.

        Args:
            app: Application to stop

        Returns:
            FlextResult containing updated application or error

        """
        handler = FlextWebAppHandler()
        return handler.stop(app)

    # =========================================================================
    # RESPONSE FORMATTING HELPERS
    # =========================================================================

    @classmethod
    def create_response_handler(
        cls,
        success_status: int = 200,
        error_status: int = 500,
    ) -> WebResponseHandler:
        """Create response handler instance.

        Args:
            success_status: Default success HTTP status
            error_status: Default error HTTP status

        Returns:
            Configured WebResponseHandler instance

        """
        return cls.WebResponseHandler(success_status, error_status)

    @classmethod
    def format_app_data(cls, app: FlextWebApp) -> FlextWebTypes.AppDataDict:
        """Format application data for API responses.

        Args:
            app: Application to format

        Returns:
            Formatted application data dictionary

        """
        return FlextWebTypes.AppDataDict(
            name=app.name,
            host=app.host,
            port=app.port,
            status=app.status_value,
            id=str(app.id),
        )

    @classmethod
    def format_health_data(cls) -> FlextWebTypes.HealthDataDict:
        """Format health check data for API responses.

        Returns:
            Formatted health data dictionary

        """
        return FlextWebTypes.HealthDataDict(
            status="healthy",
            service="flext-web",
            version="0.9.0",
            apps_count=0,  # This would be populated by the service
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
    # HANDLER FACTORY METHODS
    # =========================================================================

    @classmethod
    def create_app_handler(cls) -> WebAppHandler:
        """Create web application handler instance.

        Returns:
            WebAppHandler for CQRS operations

        """
        return cls.WebAppHandler()


# =============================================================================
# BACKWARD COMPATIBILITY ALIASES
# =============================================================================

# Legacy aliases for existing code compatibility
WebHandlers = FlextWebHandlers
WebAppHandler = FlextWebHandlers.WebAppHandler
WebResponseHandler = FlextWebHandlers.WebResponseHandler
FlextWebAppHandler = FlextWebHandlers.WebAppHandler


__all__ = [
    "FlextWebAppHandler",
    "FlextWebHandlers",
    # Legacy compatibility exports
    "WebAppHandler",
    "WebHandlers",
    "WebResponseHandler",
]
