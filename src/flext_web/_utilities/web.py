"""Web runtime utilities for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, ClassVar

from flext_cli import u

from flext_core import r
from flext_web import c, t

if TYPE_CHECKING:
    from collections.abc import Callable

    from flext_web import p


class FlextWebUtilitiesWeb:
    """Web runtime registries and protocol-backing utilities."""

    service_state: ClassVar[t.MutableMappingKV[str, bool]] = {
        "routes_initialized": False,
        "middleware_configured": False,
        "service_running": False,
    }
    apps_registry: ClassVar[t.MutableMappingKV[str, t.Web.ResponseDict]] = {}
    app_runtimes: ClassVar[t.MutableMappingKV[str, t.Web.ResponseDict]] = {}
    framework_instances: ClassVar[
        t.MutableMappingKV[str, p.Web.FastApiLikeApp | p.Web.FlaskLikeApp]
    ] = {}
    template_config: ClassVar[t.MutableMappingKV[str, t.JsonValue]] = {}
    template_filters: ClassVar[t.MutableMappingKV[str, Callable[[str], str]]] = {}
    template_globals: ClassVar[t.MutableMappingKV[str, t.JsonValue]] = {}
    web_metrics: ClassVar[t.MutableMappingKV[str, t.Scalar]] = {}

    @staticmethod
    def protocol(*, ssl_enabled: bool) -> str:
        """Return the wire protocol selected by the TLS flag."""
        selected: str = (
            c.Web.DEFAULT_HTTPS_PROTOCOL if ssl_enabled else c.Web.DEFAULT_HTTP_PROTOCOL
        )
        return selected

    @staticmethod
    def base_url(*, host: str, port: int, ssl_enabled: bool) -> str:
        """Return the base URL for the given host, port, and TLS flag."""
        scheme = FlextWebUtilitiesWeb.protocol(ssl_enabled=ssl_enabled)
        return f"{scheme}://{host}:{port}"

    class WebService:
        """Protocol-backed service lifecycle state owner."""

        @classmethod
        def configure_middleware(cls) -> p.Result[bool]:
            """Mark middleware as configured in the shared runtime state."""
            FlextWebUtilitiesWeb.service_state["middleware_configured"] = True
            return r[bool].ok(True)

        @classmethod
        def initialize_routes(cls) -> p.Result[bool]:
            """Mark routes as initialized in the shared runtime state."""
            FlextWebUtilitiesWeb.service_state["routes_initialized"] = True
            return r[bool].ok(True)

        @classmethod
        def start_service(cls) -> p.Result[bool]:
            """Mark the service as running in the shared runtime state."""
            FlextWebUtilitiesWeb.service_state["service_running"] = True
            return r[bool].ok(True)

        @classmethod
        def stop_service(cls) -> p.Result[bool]:
            """Mark the service as stopped in the shared runtime state."""
            FlextWebUtilitiesWeb.service_state["service_running"] = False
            return r[bool].ok(True)

    class WebAppManager:
        """Application registry lifecycle owner."""

        @classmethod
        def create_app(
            cls, name: str, port: int, host: str
        ) -> p.Result[t.Web.ResponseDict]:
            """Register a stopped application and return its payload."""
            registry = FlextWebUtilitiesWeb.apps_registry
            app_id = u.format_app_id(name)
            if app_id in registry:
                app_id = f"{app_id}-{len(registry) + 1}"
            payload: t.Web.ResponseDict = {
                "id": app_id,
                "name": name,
                "host": host,
                "port": port,
                "status": c.Web.Status.STOPPED.value,
                "created_at": u.generate_iso_timestamp(),
            }
            registry[app_id] = payload
            return r[t.Web.ResponseDict].ok(payload)

        @classmethod
        def start_app(cls, app_id: str) -> p.Result[t.Web.ResponseDict]:
            """Start a registered application and return its payload."""
            payload_result = FlextWebUtilitiesWeb.WebRepository.fetch_by_id(app_id)
            if payload_result.failure:
                return r[t.Web.ResponseDict].fail(payload_result.error)
            payload = payload_result.value
            payload["status"] = c.Web.Status.RUNNING.value
            FlextWebUtilitiesWeb.apps_registry[app_id] = payload
            return r[t.Web.ResponseDict].ok(payload)

        @classmethod
        def stop_app(cls, app_id: str) -> p.Result[t.Web.ResponseDict]:
            """Stop a registered application and return its payload."""
            payload_result = FlextWebUtilitiesWeb.WebRepository.fetch_by_id(app_id)
            if payload_result.failure:
                return r[t.Web.ResponseDict].fail(payload_result.error)
            payload = payload_result.value
            payload["status"] = c.Web.Status.STOPPED.value
            FlextWebUtilitiesWeb.apps_registry[app_id] = payload
            return r[t.Web.ResponseDict].ok(payload)

        @classmethod
        def list_apps(cls) -> p.Result[Sequence[t.Web.ResponseDict]]:
            """Return every registered application payload."""
            return r[Sequence[t.Web.ResponseDict]].ok(
                list(FlextWebUtilitiesWeb.apps_registry.values())
            )

    class WebRepository:
        """Application registry persistence owner."""

        @classmethod
        def fetch_by_id(cls, entity_id: str) -> p.Result[t.Web.ResponseDict]:
            """Return the registered payload or fail with a not-found error."""
            payload = FlextWebUtilitiesWeb.apps_registry.get(entity_id)
            if payload is None:
                return r[t.Web.ResponseDict].fail(
                    f"Application '{entity_id}' not found"
                )
            return r[t.Web.ResponseDict].ok(payload)

        @classmethod
        def save(cls, entity: t.Web.ResponseDict) -> p.Result[t.Web.ResponseDict]:
            """Persist an application payload under its identifier."""
            entity_id = entity.get("id")
            if not isinstance(entity_id, str) or not entity_id:
                return r[t.Web.ResponseDict].fail("Application id is required")
            FlextWebUtilitiesWeb.apps_registry[entity_id] = entity
            return r[t.Web.ResponseDict].ok(entity)

        @classmethod
        def delete(cls, entity_id: str) -> p.Result[bool]:
            """Remove an application payload by identifier."""
            return r[bool].ok(
                FlextWebUtilitiesWeb.apps_registry.pop(entity_id, None) is not None
            )

        @classmethod
        def find_all(cls) -> p.Result[Sequence[t.Web.ResponseDict]]:
            """Return every registered application payload."""
            return FlextWebUtilitiesWeb.WebAppManager.list_apps()

        @classmethod
        def find_by_criteria(
            cls, criteria: t.Web.RequestDict
        ) -> p.Result[Sequence[t.Web.ResponseDict]]:
            """Return payloads matching every requested criterion."""
            matched = [
                payload
                for payload in FlextWebUtilitiesWeb.apps_registry.values()
                if all(payload.get(key) == value for key, value in criteria.items())
            ]
            return r[Sequence[t.Web.ResponseDict]].ok(matched)

    class WebMonitoring:
        """Web health and metrics projection owner."""

        @staticmethod
        def web_health_status() -> t.Web.ResponseDict:
            """Return the service health payload from runtime state."""
            running = FlextWebUtilitiesWeb.service_state["service_running"]
            status_value = (
                c.Web.ResponseStatus.OPERATIONAL.value
                if running
                else c.Web.Status.STOPPED.value
            )
            return {"status": status_value, "service": c.Web.SERVICE_NAME}

        @staticmethod
        def web_metrics() -> t.Web.ResponseDict:
            """Return a snapshot of the recorded web metrics."""
            snapshot: t.Web.ResponseDict = {}
            for metric_name, metric_value in FlextWebUtilitiesWeb.web_metrics.items():
                snapshot[metric_name] = metric_value
            return snapshot

        @staticmethod
        def record_web_request(
            request: t.Web.RequestDict, response_time: float
        ) -> None:
            """Record one request observation in the shared metrics registry."""
            metrics = FlextWebUtilitiesWeb.web_metrics
            current = metrics.get("requests")
            requests = current if isinstance(current, int) else 0
            metrics["requests"] = requests + 1
            metrics["last_response_time"] = response_time
            _ = request


__all__: list[str] = ["FlextWebUtilitiesWeb"]
