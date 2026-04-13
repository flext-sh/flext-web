"""Canonical web service facade for flext-web."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Self, override

from pydantic import PrivateAttr

from flext_web import (
    FlextWebAuth,
    FlextWebEntities,
    FlextWebHealth,
    FlextWebServiceBase,
    FlextWebSettings,
    c,
    m,
    p,
    r,
    t,
    u,
)


class FlextWebServices(FlextWebServiceBase[bool]):
    """Public service layer backed by protocol runtime state."""

    _auth_service: FlextWebAuth | None = PrivateAttr(default=None)
    _entity_service: FlextWebEntities | None = PrivateAttr(default=None)
    _health_service: FlextWebHealth | None = PrivateAttr(default=None)

    @classmethod
    def create_service(
        cls,
        settings: FlextWebSettings | None = None,
    ) -> p.Result[Self]:
        """Create a service instance using optional settings overrides."""
        overrides = settings.model_dump() if settings is not None else None
        instance = cls(settings_overrides=overrides) if overrides is not None else cls()
        return r[Self](value=instance, success=True)

    def authenticate(
        self, credentials: m.Web.Credentials
    ) -> p.Result[m.Web.AuthResponse]:
        """Delegate authentication to the canonical auth service."""
        return self._auth().authenticate(credentials)

    def configure_middleware(self) -> p.Result[bool]:
        """Configure protocol-backed middleware state."""
        return p.Web.WebService.configure_middleware()

    def create_app(
        self, app_data: m.Web.AppData
    ) -> p.Result[m.Web.ApplicationResponse]:
        """Create an application through the protocol runtime registry."""
        return p.create_app(
            name=app_data.name,
            port=app_data.port,
            host=app_data.host,
        ).flat_map(self._application_response_from_payload)

    def create_entity(self, data: m.Web.EntityData) -> p.Result[m.Web.EntityData]:
        """Create a generic entity through the entity service."""
        return self._entities().create(data)

    def dashboard(self) -> p.Result[m.Web.DashboardResponse]:
        """Return dashboard data projected from the protocol runtime state."""
        state = p.Web.service_state
        return self.list_apps().map(
            lambda apps: m.Web.DashboardResponse(
                total_applications=len(apps),
                running_applications=sum(
                    1 for app in apps if app.status == c.Web.Status.RUNNING.value
                ),
                service_status=(
                    c.Web.WebResponse.STATUS_OPERATIONAL
                    if state["service_running"]
                    else c.Web.Status.STOPPED.value
                ),
                routes_initialized=state["routes_initialized"],
                middleware_configured=state["middleware_configured"],
                timestamp=u.generate_iso_timestamp(),
            ),
        )

    def dashboard_metrics(self) -> p.Result[m.Web.MetricsResponse]:
        """Return health metrics for the dashboard."""
        return self._health().metrics()

    @override
    def execute(self, **_kwargs: str | float | bool | None) -> p.Result[bool]:
        """Execute the web service facade."""
        return self.validate_business_rules()

    def api_capabilities(self) -> p.Result[t.Web.ResponseDict]:
        """Expose the canonical capabilities of the public web facade."""
        return r[t.Web.ResponseDict].ok({
            "application_management": ["create_app", "fetch_app", "list_apps"],
            "framework_management": ["create_fastapi_app", "create_flask_app"],
            "service_management": ["start_service", "stop_service"],
            "configuration_management": ["settings", "create_service"],
            "monitoring": ["health_check", "health_status", "dashboard"],
        })

    def fetch_app(self, app_id: str) -> p.Result[m.Web.ApplicationResponse]:
        """Return a registered application by identifier."""
        if not u.to_str(app_id):
            return r[m.Web.ApplicationResponse].fail("Application ID cannot be empty")
        return p.Web.WebRepository.fetch_by_id(app_id).flat_map(
            self._application_response_from_payload,
        )

    def fetch_entity(self, entity_id: str) -> p.Result[m.Web.EntityData]:
        """Return a generic entity by identifier."""
        return self._entities().fetch_entity(entity_id)

    def service_status(self) -> p.Result[m.Web.ServiceResponse]:
        """Return service status using protocol runtime state and settings."""
        state = p.Web.service_state
        return r[m.Web.ServiceResponse].ok(
            m.Web.ServiceResponse(
                service=c.Web.WebService.SERVICE_NAME_API,
                capabilities=[
                    "http_services_available",
                    "fastapi_support",
                    "flask_support",
                    "settings_namespace_registered",
                ],
                status=(
                    c.Web.WebResponse.STATUS_OPERATIONAL
                    if state["service_running"]
                    else c.Web.Status.STOPPED.value
                ),
                settings=True,
            ),
        )

    def health_check(self) -> p.Result[t.Web.ResponseDict]:
        """Return a simple health payload for external consumers."""
        return self.health_status().map(
            lambda health_response: {
                "status": health_response.status,
                "service": health_response.service,
                "timestamp": health_response.timestamp,
            },
        )

    def health_status(self) -> p.Result[m.Web.HealthResponse]:
        """Return structured health status."""
        return self._health().status()

    def initialize_routes(self) -> p.Result[bool]:
        """Initialize protocol-backed routes state."""
        return p.Web.WebService.initialize_routes()

    def list_apps(self) -> p.Result[Sequence[m.Web.ApplicationResponse]]:
        """List all registered applications."""
        return p.list_apps().flat_map(
            self._application_responses_from_payloads,
        )

    def list_entities(self) -> p.Result[Sequence[m.Web.EntityData]]:
        """List all generic entities."""
        return self._entities().list_all()

    def register_user(self, user_data: m.Web.UserData) -> p.Result[m.Web.UserResponse]:
        """Delegate registration to the canonical auth service."""
        return self._auth().register_user(user_data)

    def start_app(self, app_id: str) -> p.Result[m.Web.ApplicationResponse]:
        """Start a registered application and project its payload into a model."""
        if not u.to_str(app_id):
            return r[m.Web.ApplicationResponse].fail("Application ID cannot be empty")
        return p.start_app(app_id).flat_map(
            self._application_response_from_payload,
        )

    def start_service(
        self,
        host: str | None = None,
        port: int | None = None,
        *,
        debug: bool | None = None,
    ) -> p.Result[bool]:
        """Start the service and ensure a runtime application exists."""
        _ = debug
        init_result = self.initialize_routes()
        if init_result.failure:
            return init_result
        middleware_result = self.configure_middleware()
        if middleware_result.failure:
            return middleware_result
        app_result = self._get_or_create_runtime_application(host=host, port=port)
        if app_result.failure:
            return r[bool].fail(app_result.error)
        running_app = self.start_app(app_result.value.id)
        if running_app.failure:
            return r[bool].fail(running_app.error)
        return p.Web.WebService.start_service()

    def stop_app(self, app_id: str) -> p.Result[m.Web.ApplicationResponse]:
        """Stop a registered application and project its payload into a model."""
        if not u.to_str(app_id):
            return r[m.Web.ApplicationResponse].fail("Application ID cannot be empty")
        return p.stop_app(app_id).flat_map(
            self._application_response_from_payload,
        )

    def stop_service(self) -> p.Result[bool]:
        """Stop the service and all running applications."""
        apps_result = self.list_apps()
        if apps_result.failure:
            return r[bool].fail(apps_result.error)
        for app in apps_result.value:
            if app.status == c.Web.Status.RUNNING.value:
                stop_result = self.stop_app(app.id)
                if stop_result.failure:
                    return r[bool].fail(stop_result.error)
        return p.Web.WebService.stop_service()

    @override
    def validate_business_rules(self) -> p.Result[bool]:
        """Validate protocol-backed service state invariants."""
        state = p.Web.service_state
        if state["service_running"] and not state["routes_initialized"]:
            return r[bool].fail("Service cannot be running without initialized routes")
        if state["service_running"] and not state["middleware_configured"]:
            return r[bool].fail(
                "Service cannot be running without configured middleware",
            )
        return r[bool].ok(True)

    def _application_response_from_payload(
        self,
        payload: t.Web.ResponseDict,
    ) -> p.Result[m.Web.ApplicationResponse]:
        """Project a protocol payload into the canonical application response model."""
        name = payload.get("name")
        host = payload.get("host")
        port = payload.get("port")
        app_id = payload.get("id")
        status = payload.get("status")
        created_at_raw = payload.get("created_at")
        if not isinstance(name, str):
            return r[m.Web.ApplicationResponse].fail(
                "Application payload is missing name",
            )
        if not isinstance(host, str):
            return r[m.Web.ApplicationResponse].fail(
                "Application payload is missing host",
            )
        if not isinstance(app_id, str):
            return r[m.Web.ApplicationResponse].fail(
                "Application payload is missing id",
            )
        if not isinstance(status, str):
            return r[m.Web.ApplicationResponse].fail(
                "Application payload is missing status",
            )
        if not isinstance(port, int):
            return r[m.Web.ApplicationResponse].fail(
                "Application payload is missing port",
            )
        created_at = (
            created_at_raw
            if isinstance(created_at_raw, str)
            else u.generate_iso_timestamp()
        )
        return r[m.Web.ApplicationResponse].ok(
            m.Web.ApplicationResponse(
                id=app_id,
                name=name,
                host=host,
                port=port,
                status=status,
                created_at=created_at,
            ),
        )

    def _application_responses_from_payloads(
        self,
        payloads: Sequence[t.Web.ResponseDict],
    ) -> p.Result[Sequence[m.Web.ApplicationResponse]]:
        """Project a sequence of payloads into response models."""
        responses: list[m.Web.ApplicationResponse] = []
        for payload in payloads:
            response_result = self._application_response_from_payload(payload)
            if response_result.failure:
                return r[Sequence[m.Web.ApplicationResponse]].fail(
                    response_result.error,
                )
            responses.append(response_result.value)
        return r[Sequence[m.Web.ApplicationResponse]].ok(responses)

    def _auth(self) -> FlextWebAuth:
        """Return the lazily created auth service."""
        if self._auth_service is None:
            self._auth_service = FlextWebAuth(
                settings_overrides=self.settings.model_dump()
            )
        return self._auth_service

    def _entities(self) -> FlextWebEntities:
        """Return the lazily created entity service."""
        if self._entity_service is None:
            self._entity_service = FlextWebEntities(
                settings_overrides=self.settings.model_dump(),
            )
        return self._entity_service

    def _get_or_create_runtime_application(
        self,
        host: str | None,
        port: int | None,
    ) -> p.Result[m.Web.ApplicationResponse]:
        """Return the configured runtime application, creating it when needed."""
        target_name = self.settings.app_name
        target_host = host if host is not None else self.settings.host
        target_port = port if port is not None else self.settings.port
        apps_result = self.list_apps()
        if apps_result.failure:
            return r[m.Web.ApplicationResponse].fail(apps_result.error)
        for app in apps_result.value:
            if (
                app.name == target_name
                and app.host == target_host
                and app.port == target_port
            ):
                return r[m.Web.ApplicationResponse].ok(app)
        return self.create_app(
            m.Web.AppData(
                name=target_name,
                host=target_host,
                port=target_port,
            ),
        )

    def _health(self) -> FlextWebHealth:
        """Return the lazily created health service."""
        if self._health_service is None:
            self._health_service = FlextWebHealth(
                settings_overrides=self.settings.model_dump(),
            )
        return self._health_service


__all__: list[str] = ["FlextWebServices"]
