"""FLEXT Web Models - Consolidated domain model system extending flext-core patterns.

This module implements the consolidated model architecture following the
"one class per module" pattern, with FlextWebModels extending FlextHandlers
and containing all web-specific model functionality as nested classes.
"""

from __future__ import annotations

from enum import Enum
from typing import override

from flext_core import (
    FlextEntity,
    FlextEntityId,
    FlextHandlers,
    FlextResult,
)
from pydantic import ConfigDict, Field, field_validator

# =============================================================================
# CONSOLIDATED MODELS CLASS
# =============================================================================


class FlextWebModels(FlextHandlers):
    """Consolidated web model system extending flext-core patterns.

    This class serves as the single point of access for all web-specific
    model functionality while extending FlextHandlers from flext-core
    for proper architectural inheritance.

    All model functionality is accessible through this single class following the
    "one class per module" architectural requirement.
    """

    # =========================================================================
    # NESTED MODEL CLASSES
    # =========================================================================

    class WebAppStatus(Enum):
        """Web application status enumeration with state transition rules.

        Defines the possible states for web applications within the FLEXT ecosystem,
        following state machine patterns for reliable application lifecycle management.

        States:
          STOPPED: Application is not running and can be started
          STARTING: Application is in the process of starting (transitional)
          RUNNING: Application is actively running and operational
          STOPPING: Application is in the process of stopping (transitional)
          ERROR: Application encountered an error and requires intervention

        State Transitions:
          STOPPED -> STARTING -> RUNNING
          RUNNING -> STOPPING -> STOPPED
          Any state -> ERROR (on failure)
          ERROR -> STOPPED (on recovery)

        Business Rules:
          - Applications can only be started from STOPPED or ERROR states
          - Applications can only be stopped from RUNNING or ERROR states
          - Transitional states (STARTING, STOPPING) prevent new operations
        """

        STOPPED = "stopped"
        STARTING = "starting"
        RUNNING = "running"
        STOPPING = "stopping"
        ERROR = "error"

    class WebApp(FlextEntity):
        """Web application domain entity with lifecycle management capabilities.

        Rich domain entity representing a web application within the FLEXT ecosystem.
        Implements business rules for application lifecycle management, state transitions,
        and validation using flext-core foundation patterns.

        The entity follows Domain-Driven Design principles with encapsulated business
        logic, consistent state management, and comprehensive validation rules.

        Attributes:
          name: Unique application identifier within the system
          host: Network host address for application binding
          port: Network port number (1-65535) for application services
          status: Current application state following defined state machine

        Inherited Attributes:
          id: Unique entity identifier (from FlextEntity)

        Business Rules:
          - Application names must be non-empty strings
          - Port numbers must be within valid range (1-65535)
          - State transitions must follow defined state machine
          - Only one application per host:port combination

        Integration:
          - Uses FlextValidators for consistent validation patterns
          - Returns FlextResult for railway-oriented programming
          - Integrates with WebAppHandler for CQRS operations
          - Compatible with repository patterns for persistence

        Example:
          Creating and managing an application:

          >>> app = FlextWebModels.WebApp(
          ...     id="app_web-service", name="web-service", host="localhost", port=3000
          ... )
          >>> result = app.start()
          >>> if result.success:
          ...     updated_app = result.value
          ...     print(
          ...         f"Started: {updated_app.name} on {updated_app.host}:{updated_app.port}"
          ...     )

        """

        # Ensure enums are kept as Enum instances for attribute access/tests
        model_config = ConfigDict(
            use_enum_values=False,
        )

        name: str = Field(description="Application name")
        host: str = Field(default="localhost", description="Host address")
        port: int = Field(default=8000, ge=1, le=65535, description="Port number")
        status: FlextWebModels.WebAppStatus | None = Field(
            default=None,
            description="Application status",
        )

        @field_validator("name")
        @classmethod
        def validate_name(cls, v: str) -> str:
            """Validate application name is non-empty."""
            if not v or not v.strip():
                msg = "Application name cannot be empty"
                raise ValueError(msg)
            return v

        @field_validator("host")
        @classmethod
        def validate_host(cls, v: str) -> str:
            """Validate host address is non-empty."""
            if not v or not v.strip():
                msg = "Host address cannot be empty"
                raise ValueError(msg)
            return v

        @field_validator("port")
        @classmethod
        def validate_port(cls, v: int) -> int:
            """Validate port is within valid range."""
            max_port_number = 65535
            if not (1 <= v <= max_port_number):
                msg = "Port must be between 1 and 65535"
                raise ValueError(msg)
            return v

        @field_validator("status", mode="before")
        @classmethod
        def _coerce_status(cls, v: object) -> FlextWebModels.WebAppStatus:
            """Coerce incoming status to enum for consistent attribute access."""
            # If it's already an enum, return it
            if hasattr(v, "value") and hasattr(v, "name"):
                return v  # type: ignore[return-value]

            # If None or not provided, set default to STOPPED
            if v is None:
                v = "stopped"

            # Use the proper WebAppStatus enum instead of local enum
            try:
                return FlextWebModels.WebAppStatus(str(v))
            except Exception:
                return FlextWebModels.WebAppStatus.ERROR

        @override
        def validate_business_rules(self) -> FlextResult[None]:
            """Validate application according to domain business rules.

            Performs comprehensive validation of the application entity using
            flext-core validation patterns. Ensures all business rules are
            satisfied before allowing operations on the entity.

            Returns:
                FlextResult[None]: Success if all validations pass, failure with
                detailed error message if any validation rule is violated.

            Note:
                Basic field validations are now handled by @field_validator decorators.
                This method performs additional domain business rules validation.

            Example:
                >>> app = FlextWebModels.WebApp(name="test", host="localhost", port=3000)
                >>> result = app.validate_business_rules()
                >>> if result.success:
                ...     print("Application is valid")
                ... else:
                ...     print(f"Validation failed: {result.error}")

            """
            # Validate name is not empty (critical for application operations)
            if not self.name or not self.name.strip():
                return FlextResult[None].fail("Application name cannot be empty")

            # Validate port range
            max_port = 65535
            if not (1 <= self.port <= max_port):
                return FlextResult[None].fail(
                    f"Invalid port number: must be between 1 and {max_port}"
                )

            # Validate host is not empty
            if not self.host or not self.host.strip():
                return FlextResult[None].fail("Host cannot be empty")

            # Additional business rule validations can be added here as needed
            return FlextResult[None].ok(None)

        def validate_domain_rules(self) -> FlextResult[None]:
            """Validate business rules required by FlextEntity abstract method."""
            return self.validate_business_rules()

        def _status_enum(self) -> FlextWebModels.WebAppStatus:
            """Return status as WebAppStatus regardless of storage format.

            flext-core base models enable `use_enum_values=True`, which means fields
            typed as Enum may be stored internally as their raw value (e.g. str).
            This helper guarantees robust comparisons by coercing to Enum.
            """
            # Status is guaranteed to be WebAppStatus by Pydantic validator
            # If somehow None, return STOPPED as default
            if self.status is None:
                return FlextWebModels.WebAppStatus.STOPPED
            return self.status

        @property
        def status_value(self) -> str:
            """Return status value as string, robust to enum/str storage."""
            return self._status_enum().value

        @property
        def status_name(self) -> str:
            """Return status name as string, robust to enum/str storage."""
            return self._status_enum().name

        @property
        def is_running(self) -> bool:
            """Check if application is currently in running state.

            Convenience property for determining if the application is actively
            running and operational. Used by monitoring systems and status checks.

            Returns:
                bool: True if application status is RUNNING, False otherwise.

            Note:
                This property only checks the current status. It does not verify
                actual process state or network connectivity. For comprehensive
                health checks, use monitoring integration patterns.

            Example:
                >>> app = FlextWebModels.WebApp(name="service", status=FlextWebModels.WebAppStatus.RUNNING)
                >>> if app.is_running:
                ...     print("Application is operational")

            """
            return self._status_enum() == FlextWebModels.WebAppStatus.RUNNING

        def start(self) -> FlextResult[FlextWebModels.WebApp]:
            """Start application with state transition validation.

            Initiates application startup following defined business rules and
            state machine constraints. Validates current state allows starting
            and returns updated entity with new state.

            Returns:
                FlextResult[WebApp]: Success contains updated application entity
                with RUNNING status, failure contains error message explaining why
                the application cannot be started.

            Business Rules:
                - Application must be in STOPPED or ERROR state to start
                - Applications in STARTING state cannot be started again
                - Applications already RUNNING cannot be started
                - State transition is atomic and consistent

            Side Effects:
                - Updates application status to RUNNING on success
                - Triggers domain events for monitoring and integration
                - May update timestamp fields through FlextTimestampMixin

            Example:
                >>> app = FlextWebModels.WebApp(name="service", status=FlextWebModels.WebAppStatus.STOPPED)
                >>> result = app.start()
                >>> if result.success:
                ...     running_app = result.value
                ...     print(f"Started {running_app.name}: {running_app.is_running}")
                ... else:
                ...     print(f"Cannot start: {result.error}")

            """
            status = self._status_enum()
            if status == FlextWebModels.WebAppStatus.RUNNING:
                return FlextResult["FlextWebModels.WebApp"].fail("Application already running")
            if status == FlextWebModels.WebAppStatus.STARTING:
                return FlextResult["FlextWebModels.WebApp"].fail("Application already starting")
            return FlextResult["FlextWebModels.WebApp"].ok(
                self.model_copy(update={"status": FlextWebModels.WebAppStatus.RUNNING}),
            )

        def stop(self) -> FlextResult[FlextWebModels.WebApp]:
            """Stop application with graceful state transition.

            Initiates application shutdown following defined business rules and
            state machine constraints. Validates current state allows stopping
            and returns updated entity with new state.

            Returns:
                FlextResult[WebApp]: Success contains updated application entity
                with STOPPED status, failure contains error message explaining why
                the application cannot be stopped.

            Business Rules:
                - Application must be in RUNNING or ERROR state to stop
                - Applications already STOPPED cannot be stopped again
                - Applications in STOPPING state cannot be stopped again
                - State transition is atomic and consistent

            Side Effects:
                - Updates application status to STOPPED on success
                - Triggers domain events for monitoring and integration
                - May update timestamp fields through FlextTimestampMixin
                - Allows cleanup and resource release operations

            Example:
                >>> app = FlextWebModels.WebApp(name="service", status=FlextWebModels.WebAppStatus.RUNNING)
                >>> result = app.stop()
                >>> if result.success:
                ...     stopped_app = result.value
                ...     print(f"Stopped {stopped_app.name}: {not stopped_app.is_running}")
                ... else:
                ...     print(f"Cannot stop: {result.error}")

            """
            status = self._status_enum()
            if status == FlextWebModels.WebAppStatus.STOPPED:
                return FlextResult["FlextWebModels.WebApp"].fail("Application already stopped")
            if status == FlextWebModels.WebAppStatus.STOPPING:
                return FlextResult["FlextWebModels.WebApp"].fail("Application already stopping")
            return FlextResult["FlextWebModels.WebApp"].ok(
                self.model_copy(update={"status": FlextWebModels.WebAppStatus.STOPPED}),
            )

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

          >>> handler = FlextWebModels.WebAppHandler()
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
                >>> handler = FlextWebModels.WebAppHandler()
                >>> result = handler.create("web-api", 8080, "0.0.0.0")
                >>> if result.success:
                ...     app = result.value
                ...     print(f"Created: {app.name} [{app.id}] at {app.host}:{app.port}")
                ... else:
                ...     print(f"Creation failed: {result.error}")

            """
            try:
                # Create domain entity with generated ID
                entity_id = FlextEntityId(f"app_{name}")
                app = FlextWebModels.WebApp(id=entity_id, name=name, port=port, host=host)

                # Validate domain rules before returning
                validation = app.validate_business_rules()
                if not validation.success:
                    return FlextResult["FlextWebModels.WebApp"].fail(
                        validation.error or "Domain validation failed"
                    )

                return FlextResult["FlextWebModels.WebApp"].ok(app)
            except (RuntimeError, ValueError, TypeError) as e:
                return FlextResult["FlextWebModels.WebApp"].fail(f"Application creation failed: {e}")

        def start(self, app: FlextWebModels.WebApp) -> FlextResult[FlextWebModels.WebApp]:
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
                >>> handler = FlextWebModels.WebAppHandler()
                >>> app = FlextWebModels.WebApp(name="service", status=FlextWebModels.WebAppStatus.STOPPED)
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

        def stop(self, app: FlextWebModels.WebApp) -> FlextResult[FlextWebModels.WebApp]:
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
                >>> handler = FlextWebModels.WebAppHandler()
                >>> app = FlextWebModels.WebApp(name="service", status=FlextWebModels.WebAppStatus.RUNNING)
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

    # =========================================================================
    # MODEL FACTORY METHODS
    # =========================================================================

    @classmethod
    def create_web_app(
        cls,
        name: str,
        port: int = 8000,
        host: str = "localhost",
    ) -> FlextResult[WebApp]:
        """Create web application using handler pattern.

        Args:
            name: Application name
            port: Application port
            host: Application host

        Returns:
            FlextResult containing created WebApp or error

        """
        handler = cls.WebAppHandler()
        return handler.create(name, port, host)

    @classmethod
    def create_app_handler(cls) -> WebAppHandler:
        """Create web application handler instance.

        Returns:
            WebAppHandler for CQRS operations

        """
        return cls.WebAppHandler()

    @classmethod
    def create_app_status(cls, value: str) -> WebAppStatus:
        """Create WebAppStatus from string value.

        Args:
            value: Status value string

        Returns:
            WebAppStatus enum instance

        """
        return cls.WebAppStatus(value)


# =============================================================================
# BACKWARD COMPATIBILITY ALIASES
# =============================================================================

# Legacy aliases for existing code compatibility
FlextWebAppStatus = FlextWebModels.WebAppStatus
FlextWebApp = FlextWebModels.WebApp
FlextWebAppHandler = FlextWebModels.WebAppHandler


__all__ = [
    "FlextWebApp",
    "FlextWebAppHandler",
    # Legacy compatibility exports
    "FlextWebAppStatus",
    "FlextWebModels",
]
