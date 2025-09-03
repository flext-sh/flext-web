"""FLEXT Web Models - Consolidated web model system with enterprise patterns.

CONSOLIDAÇÃO COMPLETA seguindo flext-core architectural patterns:
- Apenas UMA classe FlextWebModels com toda funcionalidade
- Todas as outras classes antigas removidas completamente
- Arquitetura hierárquica seguindo padrão FLEXT estrito
- Python 3.13+ com Pydantic avançado sem compatibilidade legada

Architecture Overview:
    FlextWebModels - Single consolidated class containing:
        - Nested classes for web-specific models (WebApp, WebAppStatus, etc.)
        - Factory methods for creating instances with validation
        - Configuration methods for web system setup
        - Utility methods for web operations and management

Examples:
    Using consolidated FlextWebModels:
        app = FlextWebModels.WebApp(id="web_123", name="MyApp", port=8080)
        handler = FlextWebModels.WebAppHandler()
        config = FlextWebModels.create_web_app_config({"host": "0.0.0.0"})

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import uuid
from enum import Enum

from flext_core import (
    FlextConstants,
    FlextModels,
    FlextResult,
    FlextTypes,
)
from flext_core.loggings import FlextLogger
from pydantic import ConfigDict, Field, field_validator

# Import local constants and types for DIRECT usage - NO ALIASES - PRIORITIZING LOCAL LIBRARY
from flext_web.typings import FlextWebTypes


class FlextWebModels:
    """Consolidated FLEXT web model system providing all domain modeling functionality.

    This is the complete web model system for the FLEXT Web ecosystem, providing a unified
    approach to domain modeling using FlextModels as foundation and extending with
    web-specific patterns. All web model types are organized as nested classes within
    this single container for consistent configuration and easy access.

    Architecture Overview:
        The system is organized following Domain-Driven Design and flext-core patterns:

        - **Base Configuration**: Common configuration extending FlextModels
        - **Domain Models**: Web application entities with state management
        - **Status Management**: Application lifecycle status with state transitions
        - **Validation Models**: Input/output validation for web operations
        - **Factory Methods**: Safe creation methods returning FlextResult
        - **Configuration Methods**: Web system configuration with environment support

    Design Patterns:
        - **Single Point of Truth**: All web models defined in one location
        - **Type Safety**: Comprehensive generic type annotations and validation
        - **Railway Programming**: Factory methods return FlextResult for error handling
        - **Domain-Driven Design**: Clear separation of web domain concerns
        - **State Machine**: Application lifecycle with defined transitions
        - **CQRS**: Command handlers separate from domain entities
        - **flext-core Integration**: Built on FlextModels foundation

    Usage Examples:
        Web application management::

            # Create application with factory method
            app_result = FlextWebModels.create_web_app({
                "id": "app_123",
                "name": "MyWebApp",
                "host": "localhost",
                "port": 8080,
            })

            # Use CQRS handler
            handler = FlextWebModels.WebAppHandler()
            start_result = handler.start_app("app_123")

        Configuration management::

            # Create web system configuration
            config_result = FlextWebModels.create_web_system_config({
                "environment": "production",
                "max_apps": 50,
                "default_host": "0.0.0.0",
            })

    Note:
        This consolidated approach follows flext-core architectural patterns,
        ensuring consistency across the FLEXT ecosystem while providing
        web-specific domain functionality.

    """

    # =============================================================================
    # BASE MODEL CONFIGURATION EXTENDING FLEXTMODELS
    # =============================================================================

    class BaseWebConfig(FlextModels.Value):
        """Base configuration class for all FLEXT Web models extending flext-core patterns.

        Extends FlextModels with web-specific validation and serialization
        optimizations while maintaining full compatibility with flext-core ecosystem.
        """

        # Base configuration for web models
        model_config = ConfigDict(
            str_strip_whitespace=True,
            validate_assignment=True,
            use_enum_values=False,  # Keep enums as objects for web operations
            extra="forbid",
            frozen=False,
        )

    # =============================================================================
    # DOMAIN MODEL CLASSES
    # =============================================================================

    class WebAppStatus(Enum):
        """Web application status enumeration with state machine patterns.

        Defines the complete application lifecycle states within the FLEXT Web ecosystem,
        following state machine patterns for reliable application management and monitoring.

        States:
            - STOPPED: Application is not running and ready to start
            - STARTING: Transitional state during application startup
            - RUNNING: Application is actively running and operational
            - STOPPING: Transitional state during application shutdown
            - ERROR: Application encountered an error requiring intervention

        State Transitions:
            - STOPPED -> STARTING -> RUNNING (normal startup)
            - RUNNING -> STOPPING -> STOPPED (normal shutdown)
            - object state -> ERROR (on failure)
            - ERROR -> STOPPED (on recovery)

        Business Rules:
            - Applications can only start from STOPPED or ERROR states
            - Applications can only stop from RUNNING or ERROR states
            - Transitional states prevent new operations until completion
        """

        STOPPED = "stopped"
        STARTING = "starting"
        RUNNING = "running"
        STOPPING = "stopping"
        ERROR = "error"

    class WebApp(FlextModels.Entity):
        """Web application domain entity with lifecycle management and state machine.

        Rich domain entity representing a web application within the FLEXT Web ecosystem.
        Implements complete business rules for application lifecycle, state transitions,
        and validation using flext-core foundation patterns with railway-oriented programming.

        The entity follows Domain-Driven Design principles with encapsulated business
        logic, consistent state management, comprehensive validation, and state machine patterns.

        Attributes:
            name: Unique application identifier within the system
            host: Network host address for application binding
            port: Network port number (1-65535) for application services
            status: Current application state following state machine rules

        Inherited Attributes (from FlextModels):
            id: Unique entity identifier
            version: Entity version for optimistic locking
            created_at: Creation timestamp
            updated_at: Last modification timestamp
            domain_events: Collection of domain events

        Business Rules:
            - Application names must be non-empty and unique
            - Port numbers must be within valid range (1-65535)
            - Host addresses must be valid network addresses
            - State transitions must follow defined state machine
            - Applications must validate before state changes

        Integration:
            - Built on FlextModels foundation
            - Uses FlextResult for railway-oriented programming
            - Integrates with WebAppHandler for CQRS operations
            - Compatible with FlextServices patterns for processing

        """

        # Web application fields
        name: str = Field(..., min_length=1, description="Application name")
        host: str = Field(default="localhost", description="Host address")
        port: int = Field(
            default=8080,
            ge=FlextConstants.Web.MIN_PORT,
            le=FlextConstants.Web.MAX_PORT,
            description="Port number",
        )
        status: FlextWebModels.WebAppStatus = Field(
            default_factory=lambda: FlextWebModels.WebAppStatus.STOPPED,
            description="Application status",
        )

        @field_validator("status")
        @classmethod
        def validate_status(
            cls, v: FlextWebModels.WebAppStatus | str
        ) -> FlextWebModels.WebAppStatus:
            """Validate and normalize status field to enum."""
            if isinstance(v, str):
                try:
                    return FlextWebModels.WebAppStatus(v)
                except ValueError:
                    cls._raise_invalid_status_error(v)
            # Type assertion after isinstance check
            return v  # type: ignore[return-value]

        def __str__(self) -> str:
            """Custom string representation focusing on key identifiers."""
            return f"WebApp(name='{self.name}', endpoint='{self.host}:{self.port}', status={self.status.value})"

        def __repr__(self) -> str:
            """Custom repr representation with class name and key fields."""
            return f"WebApp(id='{self.id}', name='{self.name}', host:port='{self.host}:{self.port}', status='{self.status.value}')"

        @classmethod
        def _raise_invalid_status_error(cls, value: str) -> None:
            """Helper method to raise status validation error."""
            msg = f"Invalid status value: {value}. Must be one of {list(FlextWebModels.WebAppStatus)}"
            raise ValueError(msg)

        @field_validator("name")
        @classmethod
        def validate_name(cls, v: str) -> str:
            """Validate application name with comprehensive rules."""
            if not v or not v.strip():
                cls._raise_empty_name_error()

            name = v.strip()

            # Check reserved names
            reserved_names = {"REDACTED_LDAP_BIND_PASSWORD", "root", "api", "system"}
            if name.lower() in reserved_names:
                cls._raise_reserved_name_error(name)

            # Check for potentially dangerous characters (XSS prevention)
            dangerous_chars = ["<", ">", "&", '"', "'", "script", "javascript"]
            name_lower = name.lower()
            for dangerous in dangerous_chars:
                if dangerous in name_lower:
                    cls._raise_dangerous_name_error(name)

            return name

        @classmethod
        def _raise_empty_name_error(cls) -> None:
            """Helper method to raise empty name error."""
            msg = "Application name cannot be empty"
            raise ValueError(msg)

        @classmethod
        def _raise_reserved_name_error(cls, name: str) -> None:
            """Helper method to raise reserved name error."""
            msg = f"Application name '{name}' is reserved"
            raise ValueError(msg)

        @classmethod
        def _raise_dangerous_name_error(cls, name: str) -> None:
            """Helper method to raise dangerous name error."""
            msg = f"Application name contains potentially dangerous characters: {name}"
            raise ValueError(msg)

        @field_validator("host")
        @classmethod
        def validate_host(cls, v: str) -> str:
            """Validate host address format."""
            if not v or not v.strip():
                cls._raise_empty_host_error()

            host = v.strip()

            # Basic IP address validation for IPv4
            if host.replace(".", "").isdigit():  # Looks like an IP
                parts = host.split(".")
                if len(parts) == 4:  # noqa: PLR2004
                    try:
                        for part in parts:
                            octet = int(part)
                            if octet < 0 or octet > 255:  # noqa: PLR2004
                                cls._raise_invalid_host_format_error(host)
                    except ValueError:
                        cls._raise_invalid_host_format_error(host)
                elif "." in host:  # Has dots but not 4 parts - invalid IP
                    cls._raise_invalid_host_format_error(host)

            return host

        @classmethod
        def _raise_empty_host_error(cls) -> None:
            """Helper method to raise empty host error."""
            msg = "Host address cannot be empty"
            raise ValueError(msg)

        @classmethod
        def _raise_invalid_host_format_error(cls, host: str) -> None:
            """Helper method to raise invalid host format error."""
            msg = f"Invalid host address format: {host}"
            raise ValueError(msg)

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate web application business rules with comprehensive checks."""
            try:
                # Name validation
                if not self.name or not self.name.strip():
                    return FlextResult[None].fail("Application name is required")

                # Port validation
                min_port = FlextConstants.Web.MIN_PORT
                max_port = FlextConstants.Web.MAX_PORT
                if not (min_port <= self.port <= max_port):
                    return FlextResult[None].fail(
                        f"Port must be between {min_port} and {max_port}"
                    )

                # Host validation
                if not self.host or not self.host.strip():
                    return FlextResult[None].fail("Host address is required")

                # Status is validated by Pydantic field definition

                return FlextResult[None].ok(None)

            except Exception as e:
                return FlextResult[None].fail(f"Business rule validation failed: {e}")

        @property
        def is_running(self) -> bool:
            """Check if application is currently running."""
            return self.status == FlextWebModels.WebAppStatus.RUNNING

        @property
        def can_start(self) -> bool:
            """Check if application can be started."""
            return self.status in {
                FlextWebModels.WebAppStatus.STOPPED,
                FlextWebModels.WebAppStatus.ERROR,
            }

        @property
        def can_stop(self) -> bool:
            """Check if application can be stopped."""
            return self.status in {
                FlextWebModels.WebAppStatus.RUNNING,
                FlextWebModels.WebAppStatus.ERROR,
            }

        def start(self) -> FlextResult[FlextWebModels.WebApp]:
            """Start application with state machine validation."""
            if not self.can_start:
                if self.status == FlextWebModels.WebAppStatus.RUNNING:
                    return FlextResult[FlextWebModels.WebApp].fail(
                        "Application is already running"
                    )
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"Application cannot start from {self.status} state"
                )

            try:
                updated_app = self.model_copy(
                    update={
                        "status": FlextWebModels.WebAppStatus.RUNNING,
                        "version": self.version + 1,
                    }
                )
                return FlextResult[FlextWebModels.WebApp].ok(updated_app)
            except Exception as e:
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"Application start failed: {e}"
                )

        def stop(self) -> FlextResult[FlextWebModels.WebApp]:
            """Stop application with state machine validation."""
            if not self.can_stop:
                if self.status == FlextWebModels.WebAppStatus.STOPPED:
                    return FlextResult[FlextWebModels.WebApp].fail(
                        "Application is already stopped"
                    )
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"Application cannot stop from {self.status} state"
                )

            try:
                updated_app = self.model_copy(
                    update={
                        "status": FlextWebModels.WebAppStatus.STOPPED,
                        "version": self.version + 1,
                    }
                )
                return FlextResult[FlextWebModels.WebApp].ok(updated_app)
            except Exception as e:
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"Application stop failed: {e}"
                )

    # =============================================================================
    # DIRECT TYPE USAGE - NO ALIASES - PRIORITIZING LOCAL LIBRARY
    # =============================================================================
    # All types will be used directly as FlextWebTypes.SpecificType throughout the code

    @classmethod
    def _raise_invalid_port_type_error(cls, value: object) -> None:
        """Helper method to raise port type validation error."""
        msg = f"Port must be int or str, got {type(value)}"
        raise TypeError(msg)


    class WebAppHandler:
        """CQRS command handler for web application operations.

        Implements Command-Query Responsibility Segregation patterns for web application
        management, providing stateless command processing with comprehensive validation
        and error handling through FlextResult patterns.

        Command Operations:
            - create: Create new web application
            - start: Start existing application
            - stop: Stop running application
            - update: Update application configuration
            - delete: Remove application

        Integration:
            - Uses FlextResult for railway-oriented programming
            - Integrates with FlextWebModels.WebApp domain entity
            - Compatible with FlextServices for orchestration
            - Supports event sourcing through domain events
        """

        def create(
            self, name: str, port: int, host: str
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Create new web application with validation."""
            app_id = f"app_{name.lower().replace(' ', '_')}"

            # Log the creation attempt using centralized logger
            logger = FlextLogger(__name__)
            logger.info(f"Creating web application: {name} on {host}:{port}")

            # Create application instance with Pydantic validation error handling
            try:
                app = FlextWebModels.WebApp(
                    id=app_id,
                    name=name,
                    host=host,
                    port=port,
                    status=FlextWebModels.WebAppStatus.STOPPED,
                )
            except Exception as e:
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"App validation failed: {e}"
                )

            # Validate business rules using railway-oriented programming
            validation_result = app.validate_business_rules()
            if validation_result.is_failure:
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"App creation failed: {validation_result.error or 'Validation failed'}"
                )

            return FlextResult[FlextWebModels.WebApp].ok(app)

        def start_app(
            self, app: FlextWebModels.WebApp
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Start web application with state validation."""
            return app.start()

        def stop_app(
            self, app: FlextWebModels.WebApp
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Stop web application with state validation."""
            return app.stop()

    # =============================================================================
    # FACTORY METHODS AND UTILITIES
    # =============================================================================

    @classmethod
    def create_web_app(
        cls,
        data: FlextWebTypes.AppData,
    ) -> FlextResult[FlextWebModels.WebApp]:
        """Create web application instance with comprehensive validation."""
        try:
            # Ensure required fields with defaults
            app_data = dict(data)

            if "id" not in app_data:
                app_data.get("name", "unknown")
                app_data["id"] = f"app_{uuid.uuid4().hex[:8]}"

            if "status" not in app_data:
                app_data["status"] = FlextWebModels.WebAppStatus.STOPPED

            # Create application instance with type-safe parameters
            port_value = app_data["port"]

            def _validate_port(value: object) -> int:
                if not isinstance(value, (int, str)):
                    FlextWebModels._raise_invalid_port_type_error(value)
                # Type assertion after isinstance check
                return int(value)  # type: ignore[arg-type,no-any-return,call-overload]

            safe_port = _validate_port(port_value)

            # Let Pydantic model handle status conversion via field validator
            app = FlextWebModels.WebApp(
                id=str(app_data["id"]),
                name=str(app_data["name"]),
                host=str(app_data["host"]),
                port=safe_port,
                status=app_data["status"],  # type: ignore[arg-type]  # Pydantic handles conversion
            )

            # Validate business rules
            validation_result = app.validate_business_rules()
            if validation_result.is_failure:
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"Application validation failed: {validation_result.error}"
                )

            return FlextResult[FlextWebModels.WebApp].ok(app)

        except Exception as e:
            return FlextResult[FlextWebModels.WebApp].fail(
                f"Application creation failed: {e}"
            )

    @classmethod
    def create_web_app_handler(
        cls,
    ) -> FlextResult[FlextWebModels.WebAppHandler]:
        """Create web application handler instance."""
        try:
            handler = FlextWebModels.WebAppHandler()
            return FlextResult[FlextWebModels.WebAppHandler].ok(handler)
        except Exception as e:
            return FlextResult[FlextWebModels.WebAppHandler].fail(
                f"Handler creation failed: {e}"
            )

    @classmethod
    def create_web_system_config(
        cls, config: FlextWebTypes.ConfigData | str
    ) -> FlextResult[FlextWebTypes.ConfigData]:
        """Create web system configuration with environment validation."""
        try:
            # Handle both dict config and string environment
            if isinstance(config, str):
                environment = config
                config_dict: dict[str, object] = {"environment": environment}
            else:
                # config is FlextWebTypes.ConfigData, access fields directly
                config_dict = {
                    "host": config.get("host", "localhost"),
                    "port": config.get("port", 8080),
                    "debug": config.get("debug", True),
                    "secret_key": config.get("secret_key", "dev-secret"),
                    "app_name": config.get("app_name", "FLEXT Web"),
                    "environment": config.get("environment", "development")
                    if "environment" in config
                    else "development",
                }

            # Default configuration
            web_config = {
                "environment": config_dict.get("environment", "development"),
                "max_applications": config_dict.get("max_applications", 10),
                "default_host": config_dict.get("default_host", "localhost"),
                "port_range_start": config_dict.get("port_range_start", 8000),
                "port_range_end": config_dict.get("port_range_end", 9000),
                "enable_auto_start": config_dict.get("enable_auto_start", False),
                "enable_health_checks": config_dict.get("enable_health_checks", True),
            }

            # Validate environment
            valid_environments = [
                "development",
                "staging",
                "production",
                "test",
            ]
            if web_config["environment"] not in valid_environments:
                return FlextResult[FlextWebTypes.ConfigData].fail(
                    f"Invalid environment. Must be one of: {valid_environments}"
                )

            # Convert dict to typed ConfigData with safe casting
            default_port = web_config.get("default_port", 8080)
            port_value = (
                int(default_port) if isinstance(default_port, (int, str)) else 8080
            )

            config_data = FlextWebTypes.ConfigData(
                host=str(web_config["default_host"]),
                port=port_value,
                debug=bool(web_config.get("debug", True)),
                secret_key=str(
                    web_config.get(
                        "secret_key", "dev-key-change-in-production-32chars!"
                    )
                ),
                app_name=str(web_config.get("app_name", "FLEXT Web")),
            )
            return FlextResult[FlextWebTypes.ConfigData].ok(config_data)

        except Exception as e:
            return FlextResult[FlextWebTypes.ConfigData].fail(
                f"Config creation failed: {e}"
            )

    @classmethod
    def validate_app_data(
        cls, data: dict[str, object]
    ) -> FlextResult[dict[str, object]]:
        """Validate application data before creation."""
        try:
            # Required fields validation
            required_fields = {"name", "host", "port"}
            missing_fields = required_fields - set(data.keys())

            if missing_fields:
                return FlextResult[dict[str, object]].fail(
                    f"Missing required fields: {', '.join(missing_fields)}"
                )

            # Type validation
            if not isinstance(data.get("name"), str):
                return FlextResult[dict[str, object]].fail("Name must be a string")

            port = data.get("port")
            min_port = FlextConstants.Web.MIN_PORT
            max_port = FlextConstants.Web.MAX_PORT
            if not isinstance(port, int) or not (min_port <= port <= max_port):
                return FlextResult[dict[str, object]].fail(
                    f"Port must be an integer between {min_port} and {max_port}"
                )

            return FlextResult[dict[str, object]].ok(data)

        except Exception as e:
            return FlextResult[dict[str, object]].fail(f"Data validation failed: {e}")

    # =============================================================================
    # FLEXT WEB MODELS CONFIGURATION METHODS
    # =============================================================================

    @classmethod
    def configure_web_models_system(
        cls, config: FlextTypes.Config.ConfigDict
    ) -> FlextResult[FlextTypes.Config.ConfigDict]:
        """Configure web models system using FlextTypes.Config with validation."""
        try:
            validated_config = dict(config)

            # Validate environment using FlextConstants
            if "environment" in config:
                env_value = config["environment"]
                valid_environments = [
                    e.value for e in FlextConstants.Config.ConfigEnvironment
                ]
                if env_value not in valid_environments:
                    return FlextResult[FlextTypes.Config.ConfigDict].fail(
                        f"Invalid environment '{env_value}'. Valid options: {valid_environments}"
                    )
            else:
                validated_config["environment"] = (
                    FlextConstants.Config.ConfigEnvironment.DEVELOPMENT.value
                )

            # Web models specific settings
            validated_config.setdefault("enable_strict_validation", True)
            validated_config.setdefault("enable_state_machine", True)
            validated_config.setdefault("max_applications", 50)
            validated_config.setdefault("enable_domain_events", True)

            return FlextResult[FlextTypes.Config.ConfigDict].ok(validated_config)

        except Exception as e:
            return FlextResult[FlextTypes.Config.ConfigDict].fail(
                f"Failed to configure web models system: {e}"
            )

    @classmethod
    def get_web_models_system_config(
        cls,
    ) -> FlextResult[FlextTypes.Config.ConfigDict]:
        """Get current web models system configuration with runtime information."""
        try:
            config: FlextTypes.Config.ConfigDict = {
                # Environment configuration
                "environment": FlextConstants.Config.ConfigEnvironment.DEVELOPMENT.value,
                "log_level": FlextConstants.Config.LogLevel.INFO.value,
                # Web models specific settings
                "enable_strict_validation": True,
                "enable_state_machine": True,
                "max_applications": 50,
                "enable_domain_events": True,
                # Available model types
                "available_models": [
                    "WebApp",
                    "WebAppStatus",
                    "WebAppHandler",
                ],
                "available_factories": [
                    "create_web_app",
                    "create_web_app_handler",
                    "create_web_system_config",
                ],
                # Runtime metrics
                "active_applications": 0,
                "total_state_transitions": 0,
                "validation_success_rate": 100.0,
            }

            return FlextResult[FlextTypes.Config.ConfigDict].ok(config)

        except Exception as e:
            return FlextResult[FlextTypes.Config.ConfigDict].fail(
                f"Failed to get web models system config: {e}"
            )


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    "FlextWebModels",
]
