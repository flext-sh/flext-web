"""Canonical facade usage for flext-web application lifecycle operations.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence

from flext_web import m, p, r, web


class FlextWebExamples:
    """FlextWeb example facade for the application lifecycle demonstration."""

    @staticmethod
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

    @staticmethod
    def check_service_health() -> p.Result[m.Web.HealthResponse]:
        """Return structured health information through the public facade."""
        health_result: p.Result[m.Web.HealthResponse] = web.health_status()
        return health_result

    @staticmethod
    def create_application(
        name: str,
        port: int,
        host: str = "127.0.0.1",
    ) -> p.Result[m.Web.ApplicationResponse]:
        """Create an application through the canonical `web` facade.

        Returns:
            The resulting ``p.Result[m.Web.ApplicationResponse]``.
        """
        create_result: p.Result[m.Web.ApplicationResponse] = web.create_app(
            m.Web.AppData(name=name, host=host, port=port),
        )
        return create_result

    @staticmethod
    def start_application(app_id: str) -> p.Result[m.Web.ApplicationResponse]:
        """Start an application through the canonical `web` facade.

        Returns:
            The resulting ``p.Result[m.Web.ApplicationResponse]``.
        """
        start_result: p.Result[m.Web.ApplicationResponse] = web.start_app(app_id)
        return start_result

    @staticmethod
    def fetch_application_status(
        app_id: str,
    ) -> p.Result[m.Web.ApplicationResponse]:
        """Load a single application projection through the canonical `web` facade.

        Returns:
            The resulting ``p.Result[m.Web.ApplicationResponse]``.
        """
        fetch_result: p.Result[m.Web.ApplicationResponse] = web.fetch_app(app_id)
        return fetch_result

    @staticmethod
    def stop_application(app_id: str) -> p.Result[m.Web.ApplicationResponse]:
        """Stop an application through the canonical `web` facade.

        Returns:
            The resulting ``p.Result[m.Web.ApplicationResponse]``.
        """
        stop_result: p.Result[m.Web.ApplicationResponse] = web.stop_app(app_id)
        return stop_result

    @staticmethod
    def list_applications() -> p.Result[Sequence[m.Web.ApplicationResponse]]:
        """List application projections through the canonical `web` facade.

        Returns:
            The resulting ``p.Result[Sequence[m.Web.ApplicationResponse]]``.
        """
        list_result: p.Result[Sequence[m.Web.ApplicationResponse]] = web.list_apps()
        return list_result

    def demo_application_lifecycle(
        self,
    ) -> p.Result[Sequence[m.Web.ApplicationResponse]]:
        """Demonstrate the canonical public lifecycle flow for flext-web.

        Returns:
            The resulting ``p.Result[Sequence[m.Web.ApplicationResponse]]``.
        """
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
                lambda created: r.traverse(created, lambda app: web.fetch_app(app.id)),
            )
        )

    @staticmethod
    def _start_all(
        created: Sequence[m.Web.ApplicationResponse],
    ) -> p.Result[Sequence[m.Web.ApplicationResponse]]:
        """Start every created application, preserving the created projection.

        Returns:
            The resulting ``p.Result[Sequence[m.Web.ApplicationResponse]]``.
        """
        return r.traverse(created, lambda app: web.start_app(app.id)).map(
            lambda _: created,
        )

    @staticmethod
    def _stop_all(
        created: Sequence[m.Web.ApplicationResponse],
    ) -> p.Result[Sequence[m.Web.ApplicationResponse]]:
        """Stop every created application, preserving the created projection.

        Returns:
            The resulting ``p.Result[Sequence[m.Web.ApplicationResponse]]``.
        """
        return r.traverse(created, lambda app: web.stop_app(app.id)).map(
            lambda _: created,
        )

    def main(self) -> None:
        """Run the facade lifecycle demonstration."""
        _ = self.demo_application_lifecycle()


if __name__ == "__main__":
    FlextWebExamples().main()

__all__: list[str] = ["FlextWebExamples"]
