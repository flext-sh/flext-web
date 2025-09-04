"""FLEXT Web Handlers - Consolidated handler system extending flext-core patterns.

This module implements the consolidated handler architecture following the
"one class per module" pattern, with FlextWebHandlers extending FlextHandlers
and containing all web-specific handler functionality as nested classes and methods.
"""

from __future__ import annotations

from flask import jsonify
from flask.typing import ResponseReturnValue
from flext_core import (
    FlextConstants,
    FlextHandlers,
    FlextLogger,
    FlextMixins,
    FlextResult,
    FlextUtilities,
)

from flext_web.models import FlextWebModels
from flext_web.typings import FlextWebTypes
from flext_web.utilities import FlextWebUtilities

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

        def __init__(self) -> None:
            """Initialize WebApp handler with FlextMixins functionality."""
            self.logger = FlextLogger(__name__)

            # Initialize FlextMixins features
            FlextMixins.create_timestamp_fields(self)
            FlextMixins.ensure_id(self)
            FlextMixins.initialize_validation(self)
            FlextMixins.initialize_state(self, "ready")

            FlextMixins.log_operation(
                self, "webapp_handler_initialized", handler_type="cqrs_command_handler"
            )

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
            # Log create operation
            FlextMixins.log_operation(
                self, "create_app_command", app_name=name, app_port=port, app_host=host
            )

            # MASSIVE USAGE: Railway-oriented programming with FlextResult composition
            return (
                # Step 1: Sanitize inputs using FlextUtilities
                self._sanitize_inputs(name, host)
                # Step 2: Validate all inputs (chained validation)
                .flat_map(
                    lambda inputs: self._validate_app_inputs(
                        inputs["name"], port, inputs["host"]
                    )
                )
                # Step 3: Create domain entity
                .flat_map(
                    lambda validated: self._create_app_entity(
                        validated["name"],
                        int(validated["port"]),
                        validated["host"],
                    )
                )
                # Step 4: Validate business rules
                .flat_map(self._validate_and_return_app)
            )

        def _sanitize_inputs(self, name: str, host: str) -> FlextResult[dict[str, str]]:
            """Sanitize inputs using MASSIVE FlextUtilities delegation."""
            try:
                safe_name = FlextUtilities.TextProcessor.safe_string(name, "")
                safe_host = FlextUtilities.TextProcessor.safe_string(host, "localhost")

                return FlextResult[dict[str, str]].ok({
                    "name": safe_name,
                    "host": safe_host,
                })
            except Exception as e:
                return FlextResult[dict[str, str]].fail(
                    f"Input sanitization failed: {e}"
                )

        def _validate_app_inputs(
            self, name: str, port: int, host: str
        ) -> FlextResult[dict[str, str]]:
            """Validate all app inputs using FlextWebUtilities."""
            # Direct validation without complex typing - simpler and clearer
            if not FlextWebUtilities.validate_app_name(name):
                return FlextResult[dict[str, str]].fail(
                    f"Invalid application name: '{FlextUtilities.TextProcessor.safe_string(name, 'invalid')}'"
                )

            if not FlextWebUtilities.validate_port_range(port):
                return FlextResult[dict[str, str]].fail(
                    f"Invalid port: {port}. Range: {FlextConstants.Web.MIN_PORT}-{FlextConstants.Web.MAX_PORT}"
                )

            if not FlextWebUtilities.validate_host_format(host):
                return FlextResult[dict[str, str]].fail(
                    f"Invalid host format: '{FlextUtilities.TextProcessor.safe_string(host, 'invalid')}'"
                )

            return FlextResult[dict[str, str]].ok({
                "name": name,
                "port": str(port),
                "host": host,
            })

        def _create_app_entity(
            self, name: str, port: int, host: str
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Create app entity using FlextWebUtilities for ID generation."""
            try:
                app_id = FlextWebUtilities.format_app_id(name)
                app = FlextWebModels.WebApp(id=app_id, name=name, port=port, host=host)
                return FlextResult[FlextWebModels.WebApp].ok(app)
            except Exception as e:
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"Entity creation failed: {e}"
                )

        def _validate_and_return_app(
            self, app: FlextWebModels.WebApp
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Validate business rules and return app using FlextResult."""
            validation = app.validate_business_rules()
            if not validation.success:
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"Domain validation failed: {validation.error}"
                )
            return FlextResult[FlextWebModels.WebApp].ok(app)

        def _execute_app_lifecycle_operation(
            self,
            app: FlextWebModels.WebApp,
            operation_name: str,
            domain_method: str,
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Template Method pattern for app lifecycle operations (start/stop).

            Eliminates 77 lines of duplication by extracting common pattern:
            1. Log operation start
            2. Validate domain rules
            3. Delegate to domain entity
            4. Log success if applicable
            5. Return result

            Args:
                app: WebApp entity to operate on
                operation_name: Operation name for logging ("start"/"stop")
                domain_method: Domain method name to call ("start"/"stop")

            Returns:
                FlextResult with updated app or error

            """
            # Step 1: Log operation start
            FlextMixins.log_operation(
                self,
                f"{operation_name}_app_command",
                app_name=app.name,
                current_status=app.status.value,
            )

            # Step 2: Validate domain rules before attempting state change
            validation = app.validate_business_rules()
            if not validation.success:
                FlextMixins.log_operation(
                    self,
                    f"{operation_name}_validation_failed",
                    app_name=app.name,
                    error=validation.error,
                )
                return FlextResult[FlextWebModels.WebApp].fail(
                    validation.error or "Validation failed"
                )

            # Step 3: Delegate to domain entity for state transition
            domain_method_func = getattr(app, domain_method)
            result: FlextResult[FlextWebModels.WebApp] = domain_method_func()

            # Step 4: Log success if applicable
            if result.is_success:
                FlextMixins.log_operation(
                    self, f"app_{operation_name}_success", app_name=app.name
                )

            return result

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
                ...     name="service",
                ...     status=FlextWebModels.WebAppStatus.STOPPED,
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
            return self._execute_app_lifecycle_operation(app, "start", "start")

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
                ...     name="service",
                ...     status=FlextWebModels.WebAppStatus.RUNNING,
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
            return self._execute_app_lifecycle_operation(app, "stop", "stop")

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
            self.logger = FlextLogger(__name__)

            # Initialize FlextMixins features
            FlextMixins.create_timestamp_fields(self)
            FlextMixins.ensure_id(self)
            FlextMixins.initialize_validation(self)
            FlextMixins.initialize_state(self, "initialized")

            FlextMixins.log_operation(
                self,
                "response_handler_initialized",
                success_status=success_status,
                error_status=error_status,
            )

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
            safe_message = FlextUtilities.TextProcessor.safe_string(message, "Success")

            response_data: FlextWebTypes.ResponseDataDict = {
                "success": True,
                "message": safe_message,
                "data": data,
                "errors": [],
                "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
            }

            return jsonify(response_data), status_code or self.success_status

        def create_error_response(
            self,
            message: str,
            status_code: int | None = None,
            errors: str | dict[str, object] | None = None,
        ) -> ResponseReturnValue:
            """Create error JSON response.

            Args:
                message: Error message
                status_code: Optional HTTP status code override
                errors: Optional detailed error information

            Returns:
                Flask JSON response with error format

            """
            safe_message = FlextUtilities.TextProcessor.safe_string(
                message, "Unknown error"
            )

            response_data: FlextWebTypes.ResponseDataDict = {
                "success": False,
                "message": safe_message,
                "data": None,
                "errors": errors
                if isinstance(errors, dict)
                else ([errors] if errors else []),
                "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
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
    def handle_health_check() -> FlextResult[dict[str, object]]:
        """Handle health check requests with system status.

        Returns:
            FlextResult containing health status information.

        """
        return FlextResult[dict[str, object]].ok({
            "status": "healthy",
            "service": "flext-web",
            "version": "0.9.0",
            "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
            "components": {
                "web_service": "operational",
                "configuration": "loaded",
                "handlers": "registered",
            },
        })

    @classmethod
    def handle_system_info(cls) -> FlextResult[dict[str, object]]:
        """Handle system information requests.

        Returns:
            FlextResult containing detailed system information.

        """
        return FlextResult[dict[str, object]].ok({
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
        })

    # =========================================================================
    # APPLICATION HANDLERS
    # =========================================================================

    @classmethod
    def handle_create_app(
        cls,
        name: str,
        port: int = 8000,
        host: str = "localhost",
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
            app = FlextWebModels.WebApp(id=app_id, name=name, port=port, host=host)
            validation_result = app.validate_business_rules()

            if not validation_result.success:
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"Application validation failed: {validation_result.error}"
                )

            return FlextResult[FlextWebModels.WebApp].ok(app)

        except Exception as e:
            return FlextResult[FlextWebModels.WebApp].fail(
                f"Failed to create application: {e}"
            )

    @classmethod
    def handle_start_app(
        cls, app: FlextWebModels.WebApp
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
        cls, app: FlextWebModels.WebApp
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
            status=app.status.value,
            is_running=bool(app.is_running),
        )

    @classmethod
    def format_health_data(cls) -> FlextWebTypes.HealthResponse:
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
    # HANDLER FACTORY METHODS
    # =========================================================================

    @classmethod
    def create_app_handler(cls) -> WebAppHandler:
        """Create web application handler instance.

        Returns:
            WebAppHandler for CQRS operations

        """
        return cls.WebAppHandler()


__all__ = [
    "FlextWebHandlers",
]
