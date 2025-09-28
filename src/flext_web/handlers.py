"""FLEXT Web Handlers.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flask import jsonify
from flask.typing import ResponseReturnValue

from flext_core import (
    FlextLogger,
    FlextProcessors,
    FlextResult,
    FlextTypes,
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
            start_result = self.start(app)

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
            stop_result = self.stop(app)

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

        # =============================================================================
        # EXISTING HANDLER METHODS - Enhanced with registry integration
        # =============================================================================

        def create(
            self,
            name: str,
            port: int = FlextWebConstants.Web.DEFAULT_PORT,
            host: str = FlextWebConstants.Web.DEFAULT_HOST,
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

            """
            # Log create operation
            self.logger.info("Create app command")

            # MASSIVE USAGE: Railway-oriented programming with FlextResult composition
            result = (
                # Step 1: Sanitize inputs using FlextUtilities
                self._sanitize_inputs(name, host)
                # Step 2: Validate all inputs (chained validation)
                .flat_map(
                    lambda inputs: self._validate_app_inputs(
                        inputs["name"],
                        port,
                        inputs["host"],
                    ),
                )
                # Step 3: Create domain entity
                .flat_map(
                    lambda validated: self._create_app_entity(
                        validated["name"],
                        int(validated["port"]),
                        validated["host"],
                    ),
                )
                # Step 4: Validate business rules
                .flat_map(self._validate_and_return_app)
            )

            # Register app if created successfully
            if result.is_success:
                app = result.unwrap()
                self._apps_registry[app.id] = app

            return result

        def _sanitize_inputs(
            self,
            name: str,
            host: str,
        ) -> FlextResult[FlextTypes.Core.Headers]:
            """Sanitize inputs using MASSIVE FlextUtilities delegation."""
            try:
                safe_name = FlextUtilities.TextProcessor.safe_string(name)
                safe_host = FlextUtilities.TextProcessor.safe_string(host)

                return FlextResult[FlextTypes.Core.Headers].ok(
                    {
                        "name": safe_name,
                        "host": safe_host,
                    },
                )
            except Exception as e:
                return FlextResult[FlextTypes.Core.Headers].fail(
                    f"Input sanitization failed: {e}",
                )

        def _validate_app_inputs(
            self,
            name: str,
            port: int,
            host: str,
        ) -> FlextResult[FlextTypes.Core.Headers]:
            """Validate all app inputs - simplified to rely on Pydantic model validation."""
            return FlextResult[FlextTypes.Core.Headers].ok(
                {
                    "name": name,
                    "port": str(port),
                    "host": host,
                },
            )

        def _create_app_entity(
            self,
            name: str,
            port: int,
            host: str,
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Create app entity using FlextWebUtilities for ID generation."""
            try:
                app_id = FlextWebUtilities.format_app_id(name)
                app = FlextWebModels.WebApp(
                    id=app_id, name=name, port=port, host=host, domain_events=[]
                )
                return FlextResult[FlextWebModels.WebApp].ok(app)
            except Exception as e:
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"Entity creation failed: {e}",
                )

        def _validate_and_return_app(
            self,
            app: FlextWebModels.WebApp,
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Validate business rules and return app using FlextResult."""
            validation = app.validate_business_rules()
            if validation.is_failure:
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"Domain validation failed: {validation.error}",
                )
            return FlextResult[FlextWebModels.WebApp].ok(app)

        def _execute_app_lifecycle_operation(
            self,
            app: FlextWebModels.WebApp,
            operation_name: str,
            domain_method: str,
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Template Method pattern for app lifecycle operations (start/stop).

            Args:
                app: WebApp entity to operate on
                operation_name: Operation name for logging ("start"/"stop")
                domain_method: Domain method name to call ("start"/"stop")

            Returns:
                FlextResult with updated app or error

            """
            # Step 1: Log operation start
            self.logger.info(f"{operation_name}_app_command")

            # Step 2: Validate domain rules before attempting state change
            validation = app.validate_business_rules()
            if validation.is_failure:
                self.logger.warning(f"{operation_name}_validation_failed")
                return FlextResult[FlextWebModels.WebApp].fail(
                    validation.error or "Validation failed",
                )

            # Step 3: Delegate to domain entity for state transition
            domain_method_func = getattr(app, domain_method)
            result: FlextResult[FlextWebModels.WebApp] = domain_method_func()

            # Step 4: Log success if applicable and update registry
            if result.is_success:
                self.logger.info(f"app_{operation_name}_success")
                updated_app = result.unwrap()
                self._apps_registry[app.id] = updated_app

            return result

        def start(
            self,
            app: FlextWebModels.WebApp,
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
                >>> result: FlextResult[object] = handler.start(app)
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
            self,
            app: FlextWebModels.WebApp,
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
                >>> result: FlextResult[object] = handler.stop(app)
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

        Implements FlextWebProtocols.ResponseFormatterProtocol through structural subtyping:
        - format_success: Format success responses with data
        - format_error: Format error responses with details
        """

        @override
        def __init__(
            self,
            success_status: int = FlextWebConstants.Web.HTTP_OK,
            error_status: int = FlextWebConstants.Web.HTTP_INTERNAL_ERROR,
        ) -> None:
            """Initialize response handler with default status codes.

            Args:
                success_status: Default HTTP status for successful responses
                error_status: Default HTTP status for error responses

            """
            self.success_status = success_status
            self.error_status = error_status
            self.logger = FlextLogger(__name__)

            # Initialize response handler state
            self._initialized = True
            self.logger.info("Response handler initialized")

        # =============================================================================
        # PROTOCOL IMPLEMENTATION METHODS - ResponseFormatterProtocol
        # =============================================================================

        def format_success(
            self,
            data: FlextTypes.Core.Dict,
            message: str = "Success",
            status_code: int = 200,
        ) -> FlextWebTypes.Core.WebResponse:
            """Format success response - implements ResponseFormatterProtocol."""
            safe_message = FlextUtilities.TextProcessor.safe_string(message)

            response_data = {
                "success": True,
                "message": safe_message,
                "data": data,
                "status_code": status_code,
                "errors": [],  # Flask-specific field
            }

            return jsonify(response_data), status_code

        def format_error(
            self,
            message: str,
            status_code: int = 500,
            details: str | None = None,
        ) -> FlextWebTypes.Core.WebResponse:
            """Format error response - implements ResponseFormatterProtocol."""
            safe_message = FlextUtilities.TextProcessor.safe_string(
                message or "Unknown error",
            )

            response_data = {
                "success": False,
                "message": safe_message,
                "status_code": status_code,
                "errors": ([details] if details else []),
            }

            if details:
                response_data["details"] = details

            return jsonify(response_data), status_code

        # =============================================================================
        # EXISTING METHODS - Updated to use protocol methods
        # =============================================================================

        def create_success_response(
            self,
            data: FlextTypes.Core.Dict | FlextTypes.Core.List | None = None,
            message: str = "Success",
            status_code: int | None = None,
        ) -> ResponseReturnValue:
            """Create successful JSON response using protocol method.

            Args:
                data: Response data
                message: Success message
                status_code: Optional HTTP status code override

            Returns:
                Flask JSON response with success format

            """
            # Convert data to dict if needed for protocol compliance
            if data is None:
                formatted_data = {}
            elif isinstance(data, list):
                formatted_data = {"items": data}
            else:
                formatted_data = data

            return self.format_success(
                data=formatted_data,
                message=message,
                status_code=status_code or self.success_status,
            )

        def create_error_response(
            self,
            message: str,
            status_code: int | None = None,
            errors: str | FlextTypes.Core.Dict | None = None,
        ) -> ResponseReturnValue:
            """Create error JSON response using protocol method.

            Args:
                message: Error message
                status_code: Optional HTTP status code override
                errors: Optional detailed error information

            Returns:
                Flask JSON response with error format

            """
            details = None
            if errors:
                if isinstance(errors, str):
                    details = errors
                elif isinstance(errors, dict):
                    details = str(errors)

            return self.format_error(
                message=message,
                status_code=status_code or self.error_status,
                details=details,
            )

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
            if result.is_success:
                result_data = result.value
                if isinstance(result_data, (dict, list)):
                    data = (
                        result_data
                        if isinstance(result_data, dict)
                        else {"items": result_data}
                    )
                else:
                    data = {"value": result_data}

                return self.format_success(data=data, message=success_message)

            return self.format_error(
                message=f"{error_message}: {result.error}",
                status_code=FlextWebConstants.Web.HTTP_BAD_REQUEST,  # Bad request for business logic errors
            )

    # =========================================================================
    # HEALTH AND SYSTEM HANDLERS
    # =========================================================================

    @staticmethod
    def handle_health_check() -> FlextResult[FlextTypes.Core.Dict]:
        """Handle health check requests with system status.

        Returns:
            FlextResult containing health status information.

        """
        return FlextResult[FlextTypes.Core.Dict].ok(
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
    def handle_system_info(cls: object) -> FlextResult[FlextTypes.Core.Dict]:
        """Handle system information requests.

        Returns:
            FlextResult containing detailed system information.

        """
        return FlextResult[FlextTypes.Core.Dict].ok(
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
        port: int = FlextWebConstants.Web.DEFAULT_PORT,
        host: str = FlextWebConstants.Web.DEFAULT_HOST,
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
        success_status: int = FlextWebConstants.Web.HTTP_OK,
        error_status: int = FlextWebConstants.Web.HTTP_INTERNAL_ERROR,
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
