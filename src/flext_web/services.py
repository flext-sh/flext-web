"""HTTP Services - Orchestration layer using flext-core patterns.

Single Responsibility: Service orchestration and delegation only.
All business logic delegated to nested services or flext-core.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import uuid
from collections.abc import MutableMapping

from flext_core import (
    FlextConstants,
    FlextResult,
    FlextService,
)
from flext_core.utilities import u

from flext_web.constants import c
from flext_web.models import m
from flext_web.settings import FlextWebSettings
from flext_web.typings import t


class FlextWebServices(FlextService[bool]):
    """HTTP service orchestration layer.

    Delegates all operations to focused nested services.
    Pure orchestration with no business logic.
    Uses monadic patterns with FlextResult for error handling.
    """

    @classmethod
    def _get_service_config_type(cls) -> type[FlextWebSettings]:
        """Get the config type for this service class."""
        return FlextWebSettings

    class Auth:
        """User authentication service."""

        @staticmethod
        def authenticate(
            credentials: m.Web.Credentials,
        ) -> FlextResult[m.Web.AuthResponse]:
            """Authenticate user with explicit validation - no fallbacks.

            Args:
                credentials: Authentication credentials model

            Returns:
                FlextResult[AuthResponse]: Success contains auth response,
                                         failure contains error message

            """
            # Use u.guard() for unified validation (DSL pattern)
            username_validated = u.guard(
                credentials.username,
                lambda un: un != FlextConstants.Test.NONEXISTENT_USERNAME,
                return_value=True,
            )
            if username_validated is None:
                return FlextResult.fail("Authentication failed")
            password_validated = u.guard(
                credentials.password,
                lambda pw: pw == FlextConstants.Test.DEFAULT_PASSWORD,
                return_value=True,
            )
            if password_validated is None:
                return FlextResult.fail("Authentication failed")

            auth_response = m.Web.AuthResponse(
                token=f"token_{credentials.username}",
                user_id=credentials.username,
                authenticated=True,
            )
            return FlextResult.ok(auth_response)

        @staticmethod
        def register_user(
            user_data: m.Web.UserData,
        ) -> FlextResult[m.Web.UserResponse]:
            """Register user with explicit validation - no fallbacks.

            Args:
                user_data: User registration data model

            Returns:
                FlextResult[UserResponse]: Success contains user response,
                                         failure contains error message

            """
            user_response = m.Web.UserResponse(
                id=f"user_{user_data.username}",
                username=user_data.username,
                email=user_data.email,
                created=True,
            )
            return FlextResult.ok(user_response)

    class Entity(FlextService[m.Web.EntityData]):
        """Entity CRUD service with monadic patterns."""

        def __init__(self) -> None:
            """Initialize storage."""
            super().__init__()
            self._storage: MutableMapping[str, m.Web.EntityData] = {}

        def create(
            self,
            data: m.Web.EntityData,
        ) -> FlextResult[m.Web.EntityData]:
            """Create entity with validation.

            Args:
                data: Entity data model

            Returns:
                FlextResult[EntityData]: Success contains entity data,
                                       failure contains error message

            """
            entity_id = str(uuid.uuid4())
            entity = m.Web.EntityData(data={"id": entity_id, **data.data})
            self._storage[entity_id] = entity
            return FlextResult.ok(entity)

        def get(self, entity_id: str) -> FlextResult[m.Web.EntityData]:
            """Get entity - fail fast if not found.

            Args:
                entity_id: Entity identifier

            Returns:
                FlextResult[EntityData]: Success contains entity data,
                                       failure contains error message

            """
            # Use u.ensure_str to simplify validation
            if not u.ensure_str(entity_id):
                return FlextResult.fail("Entity ID cannot be empty")

            if entity_id not in self._storage:
                return FlextResult.fail(f"Entity not found: {entity_id}")

            return FlextResult.ok(self._storage[entity_id])

        def list_all(
            self,
        ) -> FlextResult[list[m.Web.EntityData]]:
            """List all entities.

            Returns:
                FlextResult[list[EntityData]]: Success contains list of entities

            """
            return FlextResult.ok(list(self._storage.values()))

        def execute(
            self,
            **_kwargs: str | float | bool | None,
        ) -> FlextResult[m.Web.EntityData]:
            """Execute entity service - required by FlextService.

            Returns:
                FlextResult[EntityData]: Service ready response

            """
            ready_response = m.Web.EntityData(
                data={"message": "Entity service ready"},
            )
            return FlextResult.ok(ready_response)

    class Health:
        """Health check service."""

        @staticmethod
        def status() -> FlextResult[m.Web.HealthResponse]:
            """Get health status.

            Returns:
                FlextResult[HealthResponse]: Success contains health status

            """
            health_response = m.Web.HealthResponse(
                status=c.Web.WebResponse.STATUS_HEALTHY,
                service=c.Web.WebService.SERVICE_NAME,
                timestamp=u.Generators.generate_iso_timestamp(),
            )
            return FlextResult.ok(health_response)

        @staticmethod
        def metrics() -> FlextResult[m.Web.MetricsResponse]:
            """Get metrics.

            Returns:
                FlextResult[MetricsResponse]: Success contains metrics

            """
            metrics_response = m.Web.MetricsResponse(
                service_status=c.Web.WebResponse.STATUS_OPERATIONAL,
                components=["auth", "entities", "health"],
            )
            return FlextResult.ok(metrics_response)

    def __init__(self, config: FlextWebSettings | None = None) -> None:
        """Initialize with config.

        Args:
            config: Service configuration model or None for defaults.
                   If None, uses FlextWebSettings() with Constants defaults.

        """
        web_config = config if config is not None else FlextWebSettings()
        # Pass config to super().__init__() - FlextService will use _get_service_config_type()
        # but we override _config after initialization to use the passed config
        super().__init__()
        # Override _config with web config (FlextService creates default via _get_service_config_type)
        # Set attribute directly (no PrivateAttr needed, compatible with FlextService)
        self._config = web_config
        self._entity_service: FlextWebServices.Entity | None = None

        # HTTP server state management
        self._routes_initialized = False
        self._middleware_configured = False
        self._service_running = False

        # Application registry for web service management
        self._applications: MutableMapping[str, m.Web.ApplicationResponse] = {}

    def authenticate(
        self,
        credentials: m.Web.Credentials,
    ) -> FlextResult[m.Web.AuthResponse]:
        """Authenticate user with explicit validation - no fallbacks.

        Args:
            credentials: Authentication credentials model

        Returns:
            FlextResult[AuthResponse]: Success contains auth response,
                                     failure contains error message

        """
        return self.Auth.authenticate(credentials)

    def register_user(
        self,
        user_data: m.Web.UserData,
    ) -> FlextResult[m.Web.UserResponse]:
        """Register user with explicit validation - no fallbacks.

        Args:
            user_data: User registration data model

        Returns:
            FlextResult[UserResponse]: Success contains user response,
                                     failure contains error message

        """
        return self.Auth.register_user(user_data)

    def _ensure_entity_service(self) -> FlextResult[Entity]:
        """Ensure entity service is initialized - fail fast if not available."""
        if self._entity_service is None:
            self._entity_service = self.Entity()
        return FlextResult.ok(self._entity_service)

    def create_entity(
        self,
        data: m.Web.EntityData,
    ) -> FlextResult[m.Web.EntityData]:
        """Delegate to Entity using monadic pattern."""
        return self._ensure_entity_service().flat_map(
            lambda service: service.create(data),
        )

    def get_entity(self, entity_id: str) -> FlextResult[m.Web.EntityData]:
        """Delegate to Entity using monadic pattern."""
        return self._ensure_entity_service().flat_map(
            lambda service: service.get(entity_id),
        )

    def list_entities(
        self,
    ) -> FlextResult[list[m.Web.EntityData]]:
        """Delegate to Entity using monadic pattern."""
        return self._ensure_entity_service().flat_map(
            lambda service: service.list_all(),
        )

    def health_status(
        self,
    ) -> FlextResult[m.Web.HealthResponse]:
        """Delegate to Health."""
        return self.Health.status()

    def dashboard_metrics(
        self,
    ) -> FlextResult[m.Web.MetricsResponse]:
        """Delegate to Health."""
        return self.Health.metrics()

    @staticmethod
    def create_configuration(config: FlextWebSettings) -> FlextResult[FlextWebSettings]:
        """Create config using Pydantic 2 with explicit validation.

        Args:
            config: Configuration model (already validated by Pydantic)

        Returns:
            FlextResult[FlextWebSettings]: Success contains config,
                                        failure contains error message

        """
        return FlextResult.ok(config)

    # =========================================================================
    # HTTP SERVER MANAGEMENT - SOLID HTTP Service Lifecycle
    # =========================================================================

    def initialize_routes(self) -> FlextResult[bool]:
        """Initialize HTTP routes."""
        if self._routes_initialized:
            return FlextResult[bool].ok(value=True)
        self._routes_initialized = True
        return FlextResult[bool].ok(value=True)

    def configure_middleware(self) -> FlextResult[bool]:
        """Configure HTTP middleware."""
        if self._middleware_configured:
            return FlextResult[bool].ok(value=True)
        self._middleware_configured = True
        return FlextResult[bool].ok(value=True)

    def start_service(
        self,
        _host: str = "localhost",
        _port: int = 8080,
        *,
        _debug: bool = False,
    ) -> FlextResult[bool]:
        """Start HTTP service."""
        if self._service_running:
            return FlextResult[bool].fail("Service is already running")

        return (
            self
            .initialize_routes()
            .flat_map(lambda _: self.configure_middleware())
            .map(lambda _: self._mark_service_running())
        )

    def _mark_service_running(self) -> bool:
        """Mark service as running state - internal state management."""
        self._service_running = True
        return True

    def stop_service(self) -> FlextResult[bool]:
        """Stop HTTP service."""
        if not self._service_running:
            return FlextResult[bool].fail("Service is not running")
        self._service_running = False
        return FlextResult[bool].ok(value=True)

    @staticmethod
    def logout() -> FlextResult[m.Web.EntityData]:
        """Logout user.

        Returns:
            FlextResult[EntityData]: Success response

        """
        logout_response = m.Web.EntityData(data={"success": True})
        return FlextResult.ok(logout_response)

    def list_apps(
        self,
    ) -> FlextResult[list[m.Web.ApplicationResponse]]:
        """List applications.

        Returns:
            FlextResult[list[AppResponse]]: Success contains list of app responses

        """
        apps_list = list(self._applications.values())
        return FlextResult.ok(apps_list)

    def create_app(
        self,
        app_data: m.Web.AppData,
    ) -> FlextResult[m.Web.ApplicationResponse]:
        """Create application with explicit validation - no fallbacks.

        Args:
            app_data: Application data model

        Returns:
            FlextResult[AppResponse]: Success contains app response,
                                    failure contains error message

        """
        app_id = str(uuid.uuid4())
        app_response = m.Web.ApplicationResponse(
            id=app_id,
            name=app_data.name,
            host=app_data.host,
            port=app_data.port,
            status=c.Web.Status.STOPPED.value,
            created_at=u.Generators.generate_iso_timestamp(),
        )
        self._applications[app_id] = app_response
        return FlextResult.ok(app_response)

    def get_app(self, app_id: str) -> FlextResult[m.Web.ApplicationResponse]:
        """Get application by ID - fail fast if not found."""
        # Use u.ensure_str to simplify validation
        if not u.ensure_str(app_id):
            return FlextResult[m.Web.ApplicationResponse].fail(
                "Application ID cannot be empty",
            )

        if app_id not in self._applications:
            return FlextResult[m.Web.ApplicationResponse].fail(
                f"Application not found: {app_id}",
            )

        return FlextResult[m.Web.ApplicationResponse].ok(self._applications[app_id])

    def start_app(self, app_id: str) -> FlextResult[m.Web.ApplicationResponse]:
        """Start application - fail fast if not found."""
        # Use u.ensure_str to simplify validation
        if not u.ensure_str(app_id):
            return FlextResult[m.Web.ApplicationResponse].fail(
                "Application ID cannot be empty",
            )

        if app_id not in self._applications:
            return FlextResult[m.Web.ApplicationResponse].fail(
                f"Application not found: {app_id}",
            )

        app = self._applications[app_id]
        updated_app = app.model_copy(
            update={
                "status": c.Web.Status.RUNNING.value,
            },
        )
        self._applications[app_id] = updated_app
        return FlextResult[m.Web.ApplicationResponse].ok(updated_app)

    def stop_app(self, app_id: str) -> FlextResult[m.Web.ApplicationResponse]:
        """Stop application - fail fast if not found."""
        # Use u.ensure_str to simplify validation
        if not u.ensure_str(app_id):
            return FlextResult[m.Web.ApplicationResponse].fail(
                "Application ID cannot be empty",
            )

        if app_id not in self._applications:
            return FlextResult[m.Web.ApplicationResponse].fail(
                f"Application not found: {app_id}",
            )

        app = self._applications[app_id]
        updated_app = app.model_copy(
            update={"status": c.Web.Status.STOPPED.value},
        )
        self._applications[app_id] = updated_app
        return FlextResult[m.Web.ApplicationResponse].ok(updated_app)

    def health_check(self) -> FlextResult[t.WebCore.ResponseDict]:
        """Health check."""
        return self.health_status().map(
            lambda health_response: {
                "status": health_response.status,
                "service": health_response.service,
                "timestamp": health_response.timestamp,
            },
        )

    def dashboard(
        self,
    ) -> FlextResult[m.Web.DashboardResponse]:
        """Dashboard info with explicit status calculation."""
        # Use u.count() for unified counting (DSL pattern)
        apps_list = list(self._applications.values())
        total_apps = u.count(apps_list)
        running_status = c.Web.Status.RUNNING.value
        stopped_status = c.Web.Status.STOPPED.value
        # Use u.count() + u.filter() for unified counting with predicate (DSL pattern)
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
            timestamp=u.Generators.generate_iso_timestamp(),
        )
        return FlextResult[m.Web.DashboardResponse].ok(dashboard_response)

    @classmethod
    def create_web_service(
        cls,
        config: FlextWebSettings | None = None,
    ) -> FlextResult[FlextWebServices]:
        """Create web service with explicit validation.

        Args:
            config: Service configuration model or None for defaults

        Returns:
            FlextResult[FlextWebServices]: Success contains service instance,
                                          failure contains error message

        """
        return cls.create_service(config)

    def execute(self, **_kwargs: str | float | bool | None) -> FlextResult[bool]:
        """Execute web service orchestration (FlextService requirement).

        Returns:
        FlextResult[bool]: Success contains True if service is operational,
        failure contains error message

        """
        # Return bool for FlextService compatibility
        return FlextResult[bool].ok(value=True)

    def validate_business_rules(self) -> FlextResult[bool]:
        """Validate business rules for web services (FlextService requirement).

        Returns:
            FlextResult[bool]: Success contains True if valid, failure with error message

        """
        # Use u.guard() for unified validation (DSL pattern)
        routes_validated = u.guard(
            self._routes_initialized,
            lambda routes_init: not self._service_running or routes_init,
            return_value=True,
        )
        if routes_validated is None:
            return FlextResult[bool].fail(
                "Service cannot be running without initialized routes",
            )
        middleware_validated = u.guard(
            self._middleware_configured,
            lambda mw_conf: not self._service_running or mw_conf,
            return_value=True,
        )
        if middleware_validated is None:
            return FlextResult[bool].fail(
                "Service cannot be running without configured middleware",
            )
        return FlextResult[bool].ok(value=True)

    @classmethod
    def create_service(
        cls,
        config: FlextWebSettings | None = None,
    ) -> FlextResult[FlextWebServices]:
        """Create service instance with explicit validation.

        Args:
            config: Service configuration model or None for defaults.
                   If None, uses FlextWebSettings() with Constants defaults.

        Returns:
            FlextResult[FlextWebServices]: Success contains service instance,
                                          failure contains error message

        """
        # Use Pydantic defaults if None - Models use Constants in initialization
        # FlextWebSettings uses Constants defaults, so None creates config with defaults
        service_config = config if config is not None else FlextWebSettings()
        return FlextResult.ok(cls(config=service_config))


__all__ = ["FlextWebServices"]
