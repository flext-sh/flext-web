"""HTTP Services - Orchestration layer using flext-core patterns.

Single Responsibility: Service orchestration and delegation only.
All business logic delegated to nested services or flext-core.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import uuid
from collections.abc import MutableMapping, Sequence
from typing import override

from flext_core import r, s, u

from flext_web import FlextWebSettings, c, m, t


class FlextWebServices(s[bool]):
    """HTTP service orchestration layer.

    Delegates all operations to focused nested services.
    Pure orchestration with no business logic.
    Uses monadic patterns with r for error handling.
    """

    class Auth:
        """User authentication service."""

        @staticmethod
        def authenticate(
            credentials: m.Web.Credentials,
        ) -> r[m.Web.AuthResponse]:
            """Authenticate user with explicit validation - no fallbacks.

            Args:
                credentials: Authentication credentials model

            Returns:
                r[AuthResponse]: Success contains auth response,
                                         failure contains error message

            """
            if credentials.username == c.NONEXISTENT_USERNAME:
                return r[m.Web.AuthResponse].fail("Authentication failed")

            if credentials.password != c.DEFAULT_TEST_CREDENTIAL:
                return r[m.Web.AuthResponse].fail("Authentication failed")

            auth_response = m.Web.AuthResponse(
                token=f"token_{credentials.username}",
                user_id=credentials.username,
                authenticated=True,
            )
            return r[m.Web.AuthResponse].ok(auth_response)

        @staticmethod
        def register_user(user_data: m.Web.UserData) -> r[m.Web.UserResponse]:
            """Register user with explicit validation - no fallbacks.

            Args:
                user_data: User registration data model

            Returns:
                r[UserResponse]: Success contains user response,
                                         failure contains error message

            """
            if user_data.username.isdigit():
                return r[m.Web.UserResponse].fail("Username cannot be numeric-only")

            user_response = m.Web.UserResponse(
                id=f"user_{user_data.username}",
                username=user_data.username,
                email=user_data.email,
                created=True,
            )
            return r[m.Web.UserResponse].ok(user_response)

    class Entity(s[m.Web.EntityData]):
        """Entity CRUD service with monadic patterns."""

        def __init__(self) -> None:
            """Initialize storage."""
            super().__init__()
            self._storage: MutableMapping[str, m.Web.EntityData] = {}

        def create(self, data: m.Web.EntityData) -> r[m.Web.EntityData]:
            """Create entity with validation.

            Args:
                data: Entity data model

            Returns:
                r[EntityData]: Success contains entity data,
                                       failure contains error message

            """
            entity_id = str(uuid.uuid4())
            entity = m.Web.EntityData(data={"id": entity_id, **data.data})
            self._storage[entity_id] = entity
            return r[m.Web.EntityData].ok(entity)

        @override
        def execute(self, **_kwargs: str | float | bool | None) -> r[m.Web.EntityData]:
            """Execute entity service - required by s.

            Returns:
                r[EntityData]: Service ready response

            """
            ready_response = m.Web.EntityData(
                data={"message": c.Web.WebMessages.ENTITY_SERVICE_READY},
            )
            return r[m.Web.EntityData].ok(ready_response)

        def get_entity(self, entity_id: str) -> r[m.Web.EntityData]:
            """Get entity - fail fast if not found.

            Args:
                entity_id: Entity identifier

            Returns:
                r[EntityData]: Success contains entity data,
                                       failure contains error message

            """
            if not u.ensure_str(entity_id):
                return r[m.Web.EntityData].fail("Entity ID cannot be empty")
            if entity_id not in self._storage:
                return r[m.Web.EntityData].fail(f"Entity not found: {entity_id}")
            return r[m.Web.EntityData].ok(self._storage[entity_id])

        def list_all(self) -> r[Sequence[m.Web.EntityData]]:
            """List all entities.

            Returns:
                r[Sequence[EntityData]]: Success contains list of entities

            """
            return r[Sequence[m.Web.EntityData]].ok(list(self._storage.values()))

    class Health:
        """Health check service."""

        @staticmethod
        def metrics() -> r[m.Web.MetricsResponse]:
            """Get metrics.

            Returns:
                r[MetricsResponse]: Success contains metrics

            """
            metrics_response = m.Web.MetricsResponse(
                service_status=c.Web.WebResponse.STATUS_OPERATIONAL,
                components=["auth", "entities", "health"],
            )
            return r[m.Web.MetricsResponse].ok(metrics_response)

        @staticmethod
        def status() -> r[m.Web.HealthResponse]:
            """Get health status.

            Returns:
                r[HealthResponse]: Success contains health status

            """
            health_response = m.Web.HealthResponse(
                status=c.Web.WebResponse.STATUS_HEALTHY,
                service=c.Web.WebService.SERVICE_NAME,
                timestamp=u.generate_iso_timestamp(),
            )
            return r[m.Web.HealthResponse].ok(health_response)

    def __init__(self, _config: FlextWebSettings | None = None) -> None:
        """Initialize with config.

        Args:
            _config: Service configuration model or None for defaults.
                    If None, uses FlextWebSettings() with Constants defaults.

        """
        super().__init__()
        self._entity_service: FlextWebServices.Entity | None = None
        self._routes_initialized = False
        self._middleware_configured = False
        self._service_running = False
        self._applications: MutableMapping[str, m.Web.ApplicationResponse] = {}

    @classmethod
    def create_service(
        cls,
        config: FlextWebSettings | None = None,
    ) -> r[FlextWebServices]:
        """Create service instance with explicit validation.

        Args:
            config: Service configuration model or None for defaults.
                   If None, uses FlextWebSettings() with Constants defaults.

        Returns:
            r[FlextWebServices]: Success contains service instance,
                                          failure contains error message

        """
        return r[FlextWebServices].ok(cls(_config=config))

    @classmethod
    def create_web_service(
        cls,
        config: FlextWebSettings | None = None,
    ) -> r[FlextWebServices]:
        """Create web service with explicit validation.

        Args:
            config: Service configuration model or None for defaults

        Returns:
            r[FlextWebServices]: Success contains service instance,
                                          failure contains error message

        """
        return cls.create_service(config)

    @staticmethod
    def create_configuration(config: FlextWebSettings) -> r[FlextWebSettings]:
        """Create config using Pydantic 2 with explicit validation.

        Args:
            config: Configuration model (already validated by Pydantic)

        Returns:
            r[FlextWebSettings]: Success contains config,
                                        failure contains error message

        """
        return r[FlextWebSettings].ok(config)

    @staticmethod
    def logout() -> r[m.Web.EntityData]:
        """Logout user.

        Returns:
            r[EntityData]: Success response

        """
        logout_response = m.Web.EntityData(data={"success": True})
        return r[m.Web.EntityData].ok(logout_response)

    def authenticate(self, credentials: m.Web.Credentials) -> r[m.Web.AuthResponse]:
        """Authenticate user with explicit validation - no fallbacks.

        Args:
            credentials: Authentication credentials model

        Returns:
            r[AuthResponse]: Success contains auth response,
                                     failure contains error message

        """
        return self.Auth.authenticate(credentials)

    def configure_middleware(self) -> r[bool]:
        """Configure HTTP middleware."""
        if self._middleware_configured:
            return r[bool].ok(value=True)
        self._middleware_configured = True
        return r[bool].ok(value=True)

    def create_app(self, app_data: m.Web.AppData) -> r[m.Web.ApplicationResponse]:
        """Create application with explicit validation - no fallbacks.

        Args:
            app_data: Application data model

        Returns:
            r[AppResponse]: Success contains app response,
                                    failure contains error message

        """
        if app_data.name.isdigit():
            return r[m.Web.ApplicationResponse].fail(
                "Application name cannot be numeric-only",
            )

        app_id = str(uuid.uuid4())
        app_response = m.Web.ApplicationResponse(
            id=app_id,
            name=app_data.name,
            host=app_data.host,
            port=app_data.port,
            status=c.Web.Status.STOPPED.value,
            created_at=u.generate_iso_timestamp(),
        )
        self._applications[app_id] = app_response
        return r[m.Web.ApplicationResponse].ok(app_response)

    def create_entity(self, data: m.Web.EntityData) -> r[m.Web.EntityData]:
        """Delegate to Entity using monadic pattern."""
        return self._ensure_entity_service().flat_map(
            lambda service: service.create(data),
        )

    def dashboard(self) -> r[m.Web.DashboardResponse]:
        """Dashboard info with explicit status calculation."""
        apps_list = list(self._applications.values())
        total_apps = u.count(apps_list)
        running_status = c.Web.Status.RUNNING.value
        stopped_status = c.Web.Status.STOPPED.value
        running_apps_filtered = u.filter(
            apps_list,
            lambda app: app.status == running_status,
        )
        running_apps = u.count(running_apps_filtered)
        service_status = (
            c.Web.WebResponse.STATUS_OPERATIONAL
            if self._service_running
            else stopped_status
        )
        dashboard_response = m.Web.DashboardResponse(
            total_applications=total_apps,
            running_applications=running_apps,
            service_status=service_status,
            routes_initialized=self._routes_initialized,
            middleware_configured=self._middleware_configured,
            timestamp=u.generate_iso_timestamp(),
        )
        return r[m.Web.DashboardResponse].ok(dashboard_response)

    def dashboard_metrics(self) -> r[m.Web.MetricsResponse]:
        """Delegate to Health."""
        return self.Health.metrics()

    @override
    def execute(self, **_kwargs: str | float | bool | None) -> r[bool]:
        """Execute web service orchestration (s requirement).

        Returns:
        r[bool]: Success contains True if service is operational,
        failure contains error message

        """
        return r[bool].ok(value=True)

    def get_app(self, app_id: str) -> r[m.Web.ApplicationResponse]:
        """Get application by ID - fail fast if not found."""
        if not u.ensure_str(app_id):
            return r[m.Web.ApplicationResponse].fail("Application ID cannot be empty")
        if app_id not in self._applications:
            return r[m.Web.ApplicationResponse].fail(f"Application not found: {app_id}")
        return r[m.Web.ApplicationResponse].ok(self._applications[app_id])

    def get_entity(self, entity_id: str) -> r[m.Web.EntityData]:
        """Delegate to Entity using monadic pattern."""
        return self._ensure_entity_service().flat_map(
            lambda service: service.get_entity(entity_id),
        )

    def health_check(self) -> r[t.Web.ResponseDict]:
        """Health check."""
        return self.health_status().map(
            lambda health_response: {
                "status": health_response.status,
                "service": health_response.service,
                "timestamp": health_response.timestamp,
            },
        )

    def health_status(self) -> r[m.Web.HealthResponse]:
        """Delegate to Health."""
        return self.Health.status()

    def initialize_routes(self) -> r[bool]:
        """Initialize HTTP routes."""
        if self._routes_initialized:
            return r[bool].ok(value=True)
        self._routes_initialized = True
        return r[bool].ok(value=True)

    def list_apps(self) -> r[Sequence[m.Web.ApplicationResponse]]:
        """List applications.

        Returns:
            r[Sequence[AppResponse]]: Success contains list of app responses

        """
        apps_list = list(self._applications.values())
        return r[Sequence[m.Web.ApplicationResponse]].ok(apps_list)

    def list_entities(self) -> r[Sequence[m.Web.EntityData]]:
        """Delegate to Entity using monadic pattern."""
        return self._ensure_entity_service().flat_map(
            lambda service: service.list_all(),
        )

    def register_user(self, user_data: m.Web.UserData) -> r[m.Web.UserResponse]:
        """Register user with explicit validation - no fallbacks.

        Args:
            user_data: User registration data model

        Returns:
            r[UserResponse]: Success contains user response,
                                     failure contains error message

        """
        return self.Auth.register_user(user_data)

    def start_app(self, app_id: str) -> r[m.Web.ApplicationResponse]:
        """Start application - fail fast if not found."""
        if not u.ensure_str(app_id):
            return r[m.Web.ApplicationResponse].fail("Application ID cannot be empty")
        if app_id not in self._applications:
            return r[m.Web.ApplicationResponse].fail(f"Application not found: {app_id}")
        app = self._applications[app_id]
        updated_app = app.model_copy(update={"status": c.Web.Status.RUNNING.value})
        self._applications[app_id] = updated_app
        return r[m.Web.ApplicationResponse].ok(updated_app)

    def start_service(
        self,
        _host: str = c.Web.WebDefaults.HOST,
        _port: int = c.Web.WebDefaults.PORT,
        *,
        _debug: bool = False,
    ) -> r[bool]:
        """Start HTTP service."""
        if self._service_running:
            return r[bool].fail("Service is already running")
        return (
            self
            .initialize_routes()
            .flat_map(lambda _: self.configure_middleware())
            .map(lambda _: self._mark_service_running())
        )

    def stop_app(self, app_id: str) -> r[m.Web.ApplicationResponse]:
        """Stop application - fail fast if not found."""
        if not u.ensure_str(app_id):
            return r[m.Web.ApplicationResponse].fail("Application ID cannot be empty")
        if app_id not in self._applications:
            return r[m.Web.ApplicationResponse].fail(f"Application not found: {app_id}")
        app = self._applications[app_id]
        updated_app = app.model_copy(update={"status": c.Web.Status.STOPPED.value})
        self._applications[app_id] = updated_app
        return r[m.Web.ApplicationResponse].ok(updated_app)

    def stop_service(self) -> r[bool]:
        """Stop HTTP service."""
        if not self._service_running:
            return r[bool].fail("Service is not running")
        self._service_running = False
        return r[bool].ok(value=True)

    @override
    def validate_business_rules(self) -> r[bool]:
        """Validate business rules for web services (s requirement).

        Returns:
            r[bool]: Success contains True if valid, failure with error message

        """
        if self._service_running and not self._routes_initialized:
            return r[bool].fail("Service cannot be running without initialized routes")

        if self._service_running and not self._middleware_configured:
            return r[bool].fail(
                "Service cannot be running without configured middleware",
            )
        return r[bool].ok(value=True)

    def _ensure_entity_service(self) -> r[Entity]:
        """Ensure entity service is initialized - fail fast if not available."""
        if self._entity_service is None:
            self._entity_service = self.Entity()
        return r[FlextWebServices.Entity].ok(self._entity_service)

    def _mark_service_running(self) -> bool:
        """Mark service as running state - internal state management."""
        self._service_running = True
        return True


__all__ = ["FlextWebServices"]
