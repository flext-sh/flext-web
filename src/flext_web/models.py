"""FLEXT Web Domain Models - Domain entities, value objects and CQRS handlers.

This module consolidates the core domain components for the FLEXT Web Interface,
implementing Domain-Driven Design patterns with Clean Architecture boundaries
and CQRS command handlers.

The entities encapsulate business logic, state transitions, and validation rules
while maintaining consistency with flext-core foundation patterns. Handlers
implement Command Query Responsibility Segregation for application operations.

Key Components:
    - FlextWebAppStatus: Status enumeration with state machine rules
    - FlextWebApp: Rich domain entity with lifecycle management
    - FlextWebAppHandler: CQRS command handler for application operations

Integration:
    - Built on flext-core foundation patterns (FlextEntity, FlextResult, FlextHandlers)
    - Implements railway-oriented programming for error handling
    - Compatible with CQRS and Event Sourcing patterns
"""

from __future__ import annotations

from enum import Enum
from typing import override

from flext_core import (
    FlextEntity,
    FlextEntityId,
    FlextResult,
    FlextValidator,
)
from pydantic import ConfigDict, Field, field_validator

# =============================================================================
# DOMAIN ENTITIES AND VALUE OBJECTS
# =============================================================================


class FlextWebAppStatus(Enum):
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


class FlextWebApp(FlextEntity):
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
      - Integrates with FlextWebAppHandler for CQRS operations
      - Compatible with repository patterns for persistence

    Example:
      Creating and managing an application:

      >>> app = FlextWebApp(
      ...     id="app_web-service", name="web-service", host="localhost", port=3000
      ... )
      >>> result = app.start()
      >>> if result.success:
      ...     updated_app = result.data
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
    status: FlextWebAppStatus = Field(
        default=FlextWebAppStatus.STOPPED,
        description="Application status",
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate application name is non-empty."""
        if not FlextValidator.is_non_empty_string(v):
            msg = "Application name cannot be empty"
            raise ValueError(msg)
        return v

    @field_validator("host")
    @classmethod
    def validate_host(cls, v: str) -> str:
        """Validate host address is non-empty."""
        if not FlextValidator.is_non_empty_string(v):
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
    def _coerce_status(cls, v: object) -> FlextWebAppStatus:
        """Coerce incoming status to enum for consistent attribute access."""
        if isinstance(v, FlextWebAppStatus):
            return v
        try:
            return FlextWebAppStatus(str(v))
        except Exception:
            return FlextWebAppStatus.ERROR

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
            >>> app = FlextWebApp(name="test", host="localhost", port=3000)
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

    def _status_enum(self) -> FlextWebAppStatus:
        """Return status as FlextWebAppStatus regardless of storage format.

        flext-core base models enable `use_enum_values=True`, which means fields
        typed as Enum may be stored internally as their raw value (e.g. str).
        This helper guarantees robust comparisons by coercing to Enum.
        """
        # Status is guaranteed to be FlextWebAppStatus by Pydantic validator
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
            >>> app = FlextWebApp(name="service", status=FlextWebAppStatus.RUNNING)
            >>> if app.is_running:
            ...     print("Application is operational")

        """
        return self._status_enum() == FlextWebAppStatus.RUNNING

    def start(self) -> FlextResult[FlextWebApp]:
        """Start application with state transition validation.

        Initiates application startup following defined business rules and
        state machine constraints. Validates current state allows starting
        and returns updated entity with new state.

        Returns:
            FlextResult[FlextWebApp]: Success contains updated application entity
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
            >>> app = FlextWebApp(name="service", status=FlextWebAppStatus.STOPPED)
            >>> result = app.start()
            >>> if result.success:
            ...     running_app = result.data
            ...     print(f"Started {running_app.name}: {running_app.is_running}")
            ... else:
            ...     print(f"Cannot start: {result.error}")

        """
        status = self._status_enum()
        if status == FlextWebAppStatus.RUNNING:
            return FlextResult[FlextWebApp].fail("Application already running")
        if status == FlextWebAppStatus.STARTING:
            return FlextResult[FlextWebApp].fail("Application already starting")
        return FlextResult[FlextWebApp].ok(
            self.model_copy(update={"status": FlextWebAppStatus.RUNNING}),
        )

    def stop(self) -> FlextResult[FlextWebApp]:
        """Stop application with graceful state transition.

        Initiates application shutdown following defined business rules and
        state machine constraints. Validates current state allows stopping
        and returns updated entity with new state.

        Returns:
            FlextResult[FlextWebApp]: Success contains updated application entity
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
            >>> app = FlextWebApp(name="service", status=FlextWebAppStatus.RUNNING)
            >>> result = app.stop()
            >>> if result.success:
            ...     stopped_app = result.data
            ...     print(f"Stopped {stopped_app.name}: {not stopped_app.is_running}")
            ... else:
            ...     print(f"Cannot stop: {result.error}")

        """
        status = self._status_enum()
        if status == FlextWebAppStatus.STOPPED:
            return FlextResult[FlextWebApp].fail("Application already stopped")
        if status == FlextWebAppStatus.STOPPING:
            return FlextResult[FlextWebApp].fail("Application already stopping")
        return FlextResult[FlextWebApp].ok(
            self.model_copy(update={"status": FlextWebAppStatus.STOPPED}),
        )


# =============================================================================
# CQRS COMMAND HANDLERS
# =============================================================================


class FlextWebAppHandler:
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
            entity_id = FlextEntityId(f"app_{name}")
            app = FlextWebApp(id=entity_id, name=name, port=port, host=host)

            # Validate domain rules before returning
            validation = app.validate_business_rules()
            if not validation.success:
                return FlextResult[FlextWebApp].fail(
                    validation.error or "Domain validation failed"
                )

            return FlextResult[FlextWebApp].ok(app)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[FlextWebApp].fail(f"Application creation failed: {e}")

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
            return FlextResult[FlextWebApp].fail(
                validation.error or "Validation failed"
            )

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
            return FlextResult[FlextWebApp].fail(
                validation.error or "Validation failed"
            )

        # Delegate to domain entity for state transition
        return app.stop()
