"""Canonical facade usage for flext-web application lifecycle operations."""

from __future__ import annotations

from collections.abc import (
    Sequence,
)

from flext_core import p, r
from flext_web import m, web


def _allocate_demo_port(*reserved_ports: int) -> int:
    """Return a deterministic demo port without reusing reserved ports."""
    apps_result = web.list_apps()
    used_ports: set[int] = (
        {app.port for app in apps_result.value} if apps_result.success else set()
    )
    used_ports.update(reserved_ports)
    candidate = 18080
    while candidate in used_ports:
        candidate += 1
    return candidate


def check_service_health() -> p.Result[m.Web.HealthResponse]:
    """Return structured health information through the public facade."""
    health_result: p.Result[m.Web.HealthResponse] = web.health_status()
    return health_result


def create_application(
    name: str,
    port: int,
    host: str = "127.0.0.1",
) -> p.Result[m.Web.ApplicationResponse]:
    """Create an application through the canonical `web` facade."""
    create_result: p.Result[m.Web.ApplicationResponse] = web.create_app(
        m.Web.AppData(name=name, host=host, port=port)
    )
    return create_result


def start_application(app_id: str) -> p.Result[m.Web.ApplicationResponse]:
    """Start an application through the canonical `web` facade."""
    start_result: p.Result[m.Web.ApplicationResponse] = web.start_app(app_id)
    return start_result


def fetch_application_status(app_id: str) -> p.Result[m.Web.ApplicationResponse]:
    """Load a single application projection through the canonical `web` facade."""
    fetch_result: p.Result[m.Web.ApplicationResponse] = web.fetch_app(app_id)
    return fetch_result


def stop_application(app_id: str) -> p.Result[m.Web.ApplicationResponse]:
    """Stop an application through the canonical `web` facade."""
    stop_result: p.Result[m.Web.ApplicationResponse] = web.stop_app(app_id)
    return stop_result


def list_applications() -> p.Result[Sequence[m.Web.ApplicationResponse]]:
    """List application projections through the canonical `web` facade."""
    list_result: p.Result[Sequence[m.Web.ApplicationResponse]] = web.list_apps()
    return list_result


def demo_application_lifecycle() -> p.Result[Sequence[m.Web.ApplicationResponse]]:
    """Demonstrate the canonical public lifecycle flow for flext-web."""
    created_apps: list[m.Web.ApplicationResponse] = []
    first_port = _allocate_demo_port()
    second_port = _allocate_demo_port(first_port)

    for app_data in (
        m.Web.AppData(name="web-service", host="127.0.0.1", port=first_port),
        m.Web.AppData(name="api-gateway", host="127.0.0.1", port=second_port),
    ):
        created_result = web.create_app(app_data)
        if created_result.failure:
            return r[Sequence[m.Web.ApplicationResponse]].fail(created_result.error)
        created_apps.append(created_result.value)

    for created_app in created_apps:
        started_result = web.start_app(created_app.id)
        if started_result.failure:
            return r[Sequence[m.Web.ApplicationResponse]].fail(started_result.error)

    listed_running_apps = web.list_apps()
    if listed_running_apps.failure:
        return r[Sequence[m.Web.ApplicationResponse]].fail(listed_running_apps.error)

    for created_app in created_apps:
        stopped_result = web.stop_app(created_app.id)
        if stopped_result.failure:
            return r[Sequence[m.Web.ApplicationResponse]].fail(stopped_result.error)

    final_apps: list[m.Web.ApplicationResponse] = []
    for created_app in created_apps:
        current_result = web.fetch_app(created_app.id)
        if current_result.failure:
            return r[Sequence[m.Web.ApplicationResponse]].fail(current_result.error)
        final_apps.append(current_result.value)
    return r[Sequence[m.Web.ApplicationResponse]].ok(final_apps)


def main() -> None:
    """Run the facade lifecycle demonstration."""
    _ = demo_application_lifecycle()


if __name__ == "__main__":
    main()
