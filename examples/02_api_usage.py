"""Canonical facade usage for flext-web application lifecycle operations."""

from __future__ import annotations

from collections.abc import Sequence

from flext_web import m, p, r, web


class FlextWebExamples:
    """FlextWeb example facade for the application lifecycle demonstration."""

    def _allocate_demo_port(self, *reserved_ports: int) -> int:
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

    def check_service_health(self) -> p.Result[m.Web.HealthResponse]:
        """Return structured health information through the public facade."""
        health_result: p.Result[m.Web.HealthResponse] = web.health_status()
        return health_result

    def create_application(
        self, name: str, port: int, host: str = "127.0.0.1"
    ) -> p.Result[m.Web.ApplicationResponse]:
        """Create an application through the canonical `web` facade."""
        create_result: p.Result[m.Web.ApplicationResponse] = web.create_app(
            m.Web.AppData(name=name, host=host, port=port)
        )
        return create_result

    def start_application(self, app_id: str) -> p.Result[m.Web.ApplicationResponse]:
        """Start an application through the canonical `web` facade."""
        start_result: p.Result[m.Web.ApplicationResponse] = web.start_app(app_id)
        return start_result

    def fetch_application_status(
        self, app_id: str
    ) -> p.Result[m.Web.ApplicationResponse]:
        """Load a single application projection through the canonical `web` facade."""
        fetch_result: p.Result[m.Web.ApplicationResponse] = web.fetch_app(app_id)
        return fetch_result

    def stop_application(self, app_id: str) -> p.Result[m.Web.ApplicationResponse]:
        """Stop an application through the canonical `web` facade."""
        stop_result: p.Result[m.Web.ApplicationResponse] = web.stop_app(app_id)
        return stop_result

    def list_applications(self) -> p.Result[Sequence[m.Web.ApplicationResponse]]:
        """List application projections through the canonical `web` facade."""
        list_result: p.Result[Sequence[m.Web.ApplicationResponse]] = web.list_apps()
        return list_result

    def demo_application_lifecycle(
        self,
    ) -> p.Result[Sequence[m.Web.ApplicationResponse]]:
        """Demonstrate the canonical public lifecycle flow for flext-web."""
        first_port = self._allocate_demo_port()
        second_port = self._allocate_demo_port(first_port)
        app_data: tuple[m.Web.AppData, ...] = (
            m.Web.AppData(name="web-service", host="127.0.0.1", port=first_port),
            m.Web.AppData(name="api-gateway", host="127.0.0.1", port=second_port),
        )
        return (
            r
            .traverse(app_data, web.create_app)
            .flat_map(self._start_all)
            .flat_map(lambda created: web.list_apps().map(lambda _: created))
            .flat_map(self._stop_all)
            .flat_map(
                lambda created: r.traverse(created, lambda app: web.fetch_app(app.id))
            )
        )

    @staticmethod
    def _start_all(
        created: Sequence[m.Web.ApplicationResponse],
    ) -> p.Result[Sequence[m.Web.ApplicationResponse]]:
        """Start every created application, preserving the created projection."""
        return r.traverse(created, lambda app: web.start_app(app.id)).map(
            lambda _: created
        )

    @staticmethod
    def _stop_all(
        created: Sequence[m.Web.ApplicationResponse],
    ) -> p.Result[Sequence[m.Web.ApplicationResponse]]:
        """Stop every created application, preserving the created projection."""
        return r.traverse(created, lambda app: web.stop_app(app.id)).map(
            lambda _: created
        )

    def main(self) -> None:
        """Run the facade lifecycle demonstration."""
        _ = self.demo_application_lifecycle()


__all__: list[str] = ["FlextWebExamples"]

if __name__ == "__main__":
    FlextWebExamples().main()
