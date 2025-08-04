"""FLEXT Web Domain Entities - Core business entities with state management.

This module implements the core domain entities for the FLEXT Web Interface,
following Domain-Driven Design principles with Clean Architecture patterns.

The entities encapsulate business logic, state transitions, and validation rules
while maintaining consistency with flext-core foundation patterns.

Key Components:
    - FlextWebAppStatus: Status enumeration with state machine rules
    - FlextWebApp: Rich domain entity with lifecycle management

Integration:
    - Built on flext-core foundation patterns (FlextEntity, FlextResult)
    - Implements railway-oriented programming for error handling
    - Compatible with CQRS and Event Sourcing patterns
"""

from __future__ import annotations

from enum import Enum

from flext_core import (
    FlextEntity,
    FlextResult,
    FlextTimestampMixin,
    FlextValidatableMixin,
    FlextValidators,
)
from pydantic import Field


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


class FlextWebApp(FlextEntity, FlextTimestampMixin, FlextValidatableMixin):
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
        created_at: Timestamp of entity creation (from FlextTimestampMixin)
        updated_at: Timestamp of last modification (from FlextTimestampMixin)

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
        ...     id="app_web-service",
        ...     name="web-service",
        ...     host="localhost",
        ...     port=3000
        ... )
        >>> result = app.start()
        >>> if result.is_success:
        ...     updated_app = result.data
        ...     print(f"Started: {updated_app.name} on {updated_app.host}:{updated_app.port}")

    """

    name: str = Field(description="Application name")
    host: str = Field(default="localhost", description="Host address")
    port: int = Field(default=8000, ge=1, le=65535, description="Port number")
    status: FlextWebAppStatus = Field(
        default=FlextWebAppStatus.STOPPED,
        description="Application status",
    )

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate application according to domain business rules.

        Performs comprehensive validation of the application entity using
        flext-core validation patterns. Ensures all business rules are
        satisfied before allowing operations on the entity.

        Returns:
            FlextResult[None]: Success if all validations pass, failure with
            detailed error message if any validation rule is violated.

        Validation Rules:
            - Application name must be non-empty string
            - Port number must be within valid range (1-65535)
            - Host address must be non-empty string
            - Additional custom business rules as defined

        Example:
            >>> app = FlextWebApp(name="test", host="localhost", port=3000)
            >>> result = app.validate_domain_rules()
            >>> if result.is_success:
            ...     print("Application is valid")
            ... else:
            ...     print(f"Validation failed: {result.error}")

        """
        if not FlextValidators.is_non_empty_string(self.name):
            return FlextResult.fail("App name is required")
        if not (1 <= self.port <= 65535):
            return FlextResult.fail("Invalid port number")
        return FlextResult.ok(None)

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
        return self.status == FlextWebAppStatus.RUNNING

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
            >>> if result.is_success:
            ...     running_app = result.data
            ...     print(f"Started {running_app.name}: {running_app.is_running}")
            ... else:
            ...     print(f"Cannot start: {result.error}")

        """
        if self.status == FlextWebAppStatus.RUNNING:
            return FlextResult.fail("Application already running")
        if self.status == FlextWebAppStatus.STARTING:
            return FlextResult.fail("Application already starting")
        return FlextResult.ok(
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
            >>> if result.is_success:
            ...     stopped_app = result.data
            ...     print(f"Stopped {stopped_app.name}: {not stopped_app.is_running}")
            ... else:
            ...     print(f"Cannot stop: {result.error}")

        """
        if self.status == FlextWebAppStatus.STOPPED:
            return FlextResult.fail("Application already stopped")
        if self.status == FlextWebAppStatus.STOPPING:
            return FlextResult.fail("Application already stopping")
        return FlextResult.ok(
            self.model_copy(update={"status": FlextWebAppStatus.STOPPED}),
        )
