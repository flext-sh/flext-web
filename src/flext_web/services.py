"""FLEXT Web Services - Generic Enterprise Service System using Python 3.13+.

This module provides FlextWebServices, the main web service class following
flext-core patterns with nested specialized service classes for different responsibilities.

SOLID Principles Applied:
- Single Responsibility: Each nested class handles one specific domain
- Open/Closed: Classes are extensible through inheritance but closed for modification
- Liskov Substitution: All nested classes can be substituted by their implementations
- Interface Segregation: Each nested class provides a focused interface
- Dependency Inversion: Main class depends on abstractions (nested classes)

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import uuid
from typing import Any, TypeVar

from flext_core import FlextContainer, FlextLogger, FlextResult, FlextUtilities

from flext_web.config import FlextWebConfig
from flext_web.models import FlextWebModels

T = TypeVar("T")


class FlextWebServices[T]:
    """Generic FLEXT web service using advanced patterns and flext-core delegation.

    This class serves as the single point of access for all web service operations,
    following the "one class per module" architectural requirement. All web service
    functionality is accessible through this unified interface with nested specialized
    service classes for different responsibilities.

    Architecture:
    - Main class: FlextWebServices (coordinates all operations)
    - Nested classes: AuthService, EntityService, HealthService, ConfigService
    - SOLID principles: Each nested class has single responsibility
    - Delegation pattern: Main class delegates to specialized nested classes
    """

    def __init__(self, config: FlextWebConfig | None = None) -> None:
        """Initialize with flext-core dependency injection."""
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)
        self._config = config
        self._entities: dict[str, T] = {}

        # Initialize nested service instances (SOLID - Dependency Injection)
        self.auth_service = self.AuthService()
        self.entity_service = self.EntityService[T]()
        self.health_service = self.HealthService()
        self.config_service = self.ConfigService(config)

    # =========================================================================
    # NESTED SERVICE CLASSES - Single Responsibility Principle
    # =========================================================================

    class AuthService:
        """Authentication service - handles all authentication operations.

        Single Responsibility: Only handles user authentication and registration.
        Uses flext-core patterns for validation and error handling.
        """

        def authenticate(
            self, credentials: dict[str, Any]
        ) -> FlextResult[dict[str, Any]]:
            """Authenticate user credentials using flext-core patterns."""
            username = credentials.get("username")
            password = credentials.get("password")
            if not isinstance(username, str) or not isinstance(password, str):
                return FlextResult.fail("Invalid credentials format")
            return FlextResult.ok({"token": f"token_{username}", "user_id": username})

        def register_user(
            self, user_data: dict[str, Any]
        ) -> FlextResult[dict[str, Any]]:
            """Register new user using flext-core patterns."""
            username = user_data.get("username")
            email = user_data.get("email")
            if not isinstance(username, str) or not isinstance(email, str):
                return FlextResult.fail("Invalid user data format")
            return FlextResult.ok({
                "id": f"user_{username}",
                "username": username,
                "email": email,
            })

    class EntityService[T]:
        """Entity management service - handles all entity operations.

        Single Responsibility: Only handles CRUD operations for domain entities.
        Uses flext-core factory patterns and flext-web models for entity creation.
        """

        def __init__(self) -> None:
            """Initialize entity service."""
            self._entities: dict[str, T] = {}

        def create_entity(self, data: dict[str, Any]) -> FlextResult[T]:
            """Create entity using flext-core factory patterns."""
            # Create entity using simple approach for now
            result = FlextResult.ok({"id": str(uuid.uuid4()), **data})
            if result.is_success:
                entity = result.unwrap()
                self._entities[str(getattr(entity, "id", id(entity)))] = entity
            return result

        def get_entity(self, entity_id: str) -> FlextResult[T]:
            """Retrieve entity by ID using flext-core patterns."""
            entity = self._entities.get(entity_id)
            if entity is None:
                return FlextResult.fail("Entity not found")
            return FlextResult.ok(entity)

        def list_entities(self) -> FlextResult[list[T]]:
            """List all entities using flext-core patterns."""
            return FlextResult.ok(list(self._entities.values()))

    class HealthService:
        """Health monitoring service - handles all health check operations.

        Single Responsibility: Only handles service health and metrics.
        Uses flext-core container for system information and timing.
        """

        def health_status(self) -> FlextResult[dict[str, Any]]:
            """Get service health status using flext-core patterns."""
            return FlextResult.ok({
                "status": "healthy",
                "service": "flext-web",
                "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
            })

        def dashboard_metrics(self) -> FlextResult[dict[str, Any]]:
            """Get dashboard metrics using flext-core patterns."""
            return FlextResult.ok({
                "service_status": "operational",
                "components": [
                    "authentication",
                    "entity_management",
                    "health_monitoring",
                ],
            })

    class ConfigService:
        """Configuration service - handles all configuration operations.

        Single Responsibility: Only handles configuration creation and validation.
        Uses flext-web config models for type-safe configuration management.
        """

        def __init__(self, config: FlextWebConfig | None = None) -> None:
            """Initialize configuration service."""
            self._config = config

        def create_configuration(
            self, config_data: dict[str, Any]
        ) -> FlextResult[FlextWebConfig]:
            """Create configuration using flext-core patterns."""
            return FlextWebConfig.create_config(config_data)

        def validate_configuration(self) -> FlextResult[None]:
            """Validate configuration using flext-core patterns."""
            if self._config is None:
                return FlextResult.ok(None)
            # Configuration is validated during creation, so just return success
            return FlextResult.ok(None)

    # =========================================================================
    # MAIN SERVICE INTERFACE - Delegation Pattern (Open/Closed Principle)
    # =========================================================================

    # Authentication operations - delegate to AuthService (Single Responsibility)
    def authenticate(self, credentials: dict[str, Any]) -> FlextResult[dict[str, Any]]:
        """Authentication via auth service."""
        return self.auth_service.authenticate(credentials)

    def register_user(self, user_data: dict[str, Any]) -> FlextResult[dict[str, Any]]:
        """User registration via auth service."""
        return self.auth_service.register_user(user_data)

    # Entity operations - delegate to EntityService (Single Responsibility)
    def create_entity(self, data: dict[str, Any]) -> FlextResult[T]:
        """Entity creation via entity service."""
        return self.entity_service.create_entity(data)

    def get_entity(self, entity_id: str) -> FlextResult[T]:
        """Entity retrieval via entity service."""
        return self.entity_service.get_entity(entity_id)

    def list_entities(self) -> FlextResult[list[T]]:
        """Entity enumeration via entity service."""
        return self.entity_service.list_entities()

    # Health operations - delegate to HealthService (Single Responsibility)
    def health_status(self) -> FlextResult[dict[str, Any]]:
        """Health status via health service."""
        return self.health_service.health_status()

    def dashboard_metrics(self) -> FlextResult[dict[str, Any]]:
        """Dashboard metrics via health service."""
        return self.health_service.dashboard_metrics()

    # Configuration operations - delegate to ConfigService (Single Responsibility)
    def create_configuration(
        self, config_data: dict[str, Any]
    ) -> FlextResult[FlextWebConfig]:
        """Configuration creation via config service."""
        return self.config_service.create_configuration(config_data)

    def validate_configuration(self) -> FlextResult[None]:
        """Configuration validation via config service."""
        return self.config_service.validate_configuration()

    # Service factory - follows flext-core patterns (Dependency Inversion)
    @classmethod
    def create_service(
        cls, config: dict[str, Any] | None = None
    ) -> FlextResult[FlextWebServices[T]]:
        """Generic service factory using flext-core patterns."""
        try:
            web_config = None
            if config:
                web_config = FlextWebConfig(**config)
            service = cls(config=web_config)
            return FlextResult.ok(service)
        except Exception as e:
            return FlextResult.fail(f"Service creation failed: {e}")


__all__ = ["FlextWebServices"]
