"""FLEXT Web Domain Handlers - CQRS command handlers for application operations.

This module implements Command Query Responsibility Segregation (CQRS) patterns for
web application lifecycle management using flext-core handler patterns.

The handlers act as the application service layer, coordinating between domain entities
and infrastructure concerns while maintaining clean separation of responsibilities.

Key Components:
    - FlextWebAppHandler: CQRS command handler for web application lifecycle

Integration:
    - Built on flext-core FlextHandlers patterns
    - Uses FlextResult for railway-oriented programming
    - Integrates with domain entities for business logic
"""

from __future__ import annotations

from flext_core import FlextHandlers, FlextResult

from .entities import FlextWebApp


class FlextWebAppHandler(FlextHandlers.Handler[FlextWebApp, FlextWebApp]):
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

        >>> handler = FlextWebAppHandler()
        >>> result = handler.create("web-service", 3000, "localhost")
        >>> if result.success:
        ...     app = result.data
        ...     start_result = handler.start(app)
        ...     if start_result.success:
        ...         print(f"Started {start_result.data.name}")

    """

    def create(
        self,
        name: str,
        port: int = 8000,
        host: str = "localhost",
    ) -> FlextResult[FlextWebApp]:
        """Create new web application with comprehensive validation.

        Creates a new FlextWebApp domain entity with the specified parameters,
        performing full validation of input parameters and business rules.
        The created application starts in STOPPED state and can be started
        using the start() method.

        Args:
            name: Application name, must be non-empty string
            port: Network port number (1-65535) for application services
            host: Network host address for application binding

        Returns:
            FlextResult[FlextWebApp]: Success contains newly created application
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
            >>> handler = FlextWebAppHandler()
            >>> result = handler.create("web-api", 8080, "0.0.0.0")
            >>> if result.success:
            ...     app = result.data
            ...     print(f"Created: {app.name} [{app.id}] at {app.host}:{app.port}")
            ... else:
            ...     print(f"Creation failed: {result.error}")

        """
        try:
            # Create domain entity with generated ID
            app = FlextWebApp(id=f"app_{name}", name=name, port=port, host=host)

            # Validate domain rules before returning
            validation = app.validate_domain_rules()
            if not validation.success:
                return FlextResult.fail(validation.error or "Domain validation failed")

            return FlextResult.ok(app)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Application creation failed: {e}")

    def start(self, app: FlextWebApp) -> FlextResult[FlextWebApp]:
        """Start web application with validation and state management.

        Initiates the startup process for a web application, performing
        validation checks and state transitions according to business rules.
        The operation is atomic and maintains consistency of application state.

        Args:
            app: FlextWebApp entity to start, must be in valid state for starting

        Returns:
            FlextResult[FlextWebApp]: Success contains updated application entity
            with RUNNING status, failure contains error message explaining why
            the application cannot be started.

        Pre-conditions:
            - Application must be in STOPPED or ERROR state
            - Application configuration must pass validation
            - All domain rules must be satisfied

        Post-conditions:
            - Application status updated to RUNNING on success
            - Timestamp fields updated to reflect state change
            - Domain events triggered for monitoring integration

        Business Rules:
            - Applications already RUNNING cannot be started again
            - Applications in STARTING state cannot be started
            - State transitions must follow defined state machine
            - All validation rules must pass before state change

        Example:
            >>> handler = FlextWebAppHandler()
            >>> app = FlextWebApp(name="service", status=FlextWebAppStatus.STOPPED)
            >>> result = handler.start(app)
            >>> if result.success:
            ...     running_app = result.data
            ...     print(
            ...         f"Started: {running_app.name} is now {running_app.status.value}"
            ...     )
            ... else:
            ...     print(f"Start failed: {result.error}")

        """
        # Validate domain rules before attempting state change
        validation = app.validate_domain_rules()
        if not validation.success:
            return FlextResult.fail("App name is required")

        # Delegate to domain entity for state transition
        return app.start()

    def stop(self, app: FlextWebApp) -> FlextResult[FlextWebApp]:
        """Stop web application with graceful shutdown and validation.

        Initiates the shutdown process for a running web application, performing
        validation checks and state transitions according to business rules.
        The operation ensures graceful shutdown with proper cleanup.

        Args:
            app: FlextWebApp entity to stop, must be in valid state for stopping

        Returns:
            FlextResult[FlextWebApp]: Success contains updated application entity
            with STOPPED status, failure contains error message explaining why
            the application cannot be stopped.

        Pre-conditions:
            - Application must be in RUNNING or ERROR state
            - Application must exist and be valid
            - All domain rules must be satisfied

        Post-conditions:
            - Application status updated to STOPPED on success
            - Timestamp fields updated to reflect state change
            - Domain events triggered for monitoring integration
            - Resources properly released and cleaned up

        Business Rules:
            - Applications already STOPPED cannot be stopped again
            - Applications in STOPPING state cannot be stopped
            - State transitions must follow defined state machine
            - Graceful shutdown procedures must be followed

        Example:
            >>> handler = FlextWebAppHandler()
            >>> app = FlextWebApp(name="service", status=FlextWebAppStatus.RUNNING)
            >>> result = handler.stop(app)
            >>> if result.success:
            ...     stopped_app = result.data
            ...     print(
            ...         f"Stopped: {stopped_app.name} is now {stopped_app.status.value}"
            ...     )
            ... else:
            ...     print(f"Stop failed: {result.error}")

        """
        # Validate domain rules before attempting state change
        validation = app.validate_domain_rules()
        if not validation.success:
            return FlextResult.fail("App name is required")

        # Delegate to domain entity for state transition
        return app.stop()
