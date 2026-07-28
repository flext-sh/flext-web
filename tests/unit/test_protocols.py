"""Unit tests for the flext_web protocol surface.

Every test exercises the real protocol-backed runtime through the public `u.Web`
surface and asserts observable behavior. Facade-only assertions (is-a-type,
callable, __doc__, __annotations__), empty tests, local protocol-simulating
classes, and duplicates are intentionally absent: they validate structure, not
behavior, and are prohibited.
"""

from __future__ import annotations

import flask
from fastapi import FastAPI
from fastapi.routing import APIRoute

from flext_tests import tm
from tests import c, u


class TestsFlextWebProtocolsUnit:
    """Real-behavior tests for the web protocol runtime via `u.Web`."""

    @staticmethod
    def _reset_protocol_state() -> None:
        u.Web.apps_registry.clear()
        u.Web.framework_instances.clear()
        u.Web.app_runtimes.clear()
        u.Web.service_state.update({
            "routes_initialized": False,
            "middleware_configured": False,
            "service_running": False,
        })
        u.Web.template_config.clear()
        u.Web.template_filters.clear()
        u.Web.template_globals.clear()
        u.Web.web_metrics.update({
            "requests": 0,
            "errors": 0,
            "uptime": "0s",
            "avg_response_time_ms": 0,
        })

    @staticmethod
    def _assert_protocol_base_lifecycle() -> None:
        """Exercise protocol-base lifecycle with a real ephemeral port."""
        TestsFlextWebProtocolsUnit._reset_protocol_state()
        manager = u.Web.WebAppManager
        test_port = u.Web.Tests.TestPortManager.allocate_port()
        app_id: str | None = None
        try:
            created = manager.create_app("test", test_port, "localhost")
            tm.ok(created)
            app_id = str(created.value["id"])
            tm.that(["fastapi", "flask"], has=created.value["framework"])
            tm.that(["asgi", "wsgi"], has=created.value["interface"])
            started = manager.start_app(app_id)
            tm.ok(started)
            tm.that(started.value["status"], eq=c.Web.Status.RUNNING.value)
            listed = manager.list_apps()
            tm.ok(listed)
            tm.that(len(listed.value), eq=1)
            tm.that(listed.value[0]["id"], eq=app_id)
            stopped = manager.stop_app(app_id)
            tm.ok(stopped)
            tm.that(stopped.value["status"], eq=c.Web.Status.STOPPED.value)
        finally:
            if app_id is not None and app_id in u.Web.apps_registry:
                app_state = u.Web.apps_registry[app_id]
                if app_state.get("status") == c.Web.Status.RUNNING.value:
                    manager.stop_app(app_id)
            u.Web.Tests.TestPortManager.release_port(test_port)

    def test_app_manager_protocol_real_lifecycle_behavior(self) -> None:
        """App manager creates, starts, lists and stops a real app."""
        self._assert_protocol_base_lifecycle()

    def test_service_protocol_real_behavior(self) -> None:
        """Service rejects start before setup, then runs the real lifecycle."""
        self._reset_protocol_state()
        service = u.Web.WebService
        start_without_setup = service.start_service()
        tm.fail(start_without_setup)
        tm.ok(service.initialize_routes())
        tm.ok(service.configure_middleware())
        tm.ok(service.start_service())
        tm.ok(service.stop_service())

    def test_repository_protocol_real_behavior(self) -> None:
        """Repository returns apps matching real criteria."""
        self._reset_protocol_state()
        manager = u.Web.WebAppManager
        created = manager.create_app("repo-app", 8081, "127.0.0.1")
        tm.ok(created)
        repo = u.Web.WebRepository
        result = repo.find_by_criteria({"host": "127.0.0.1"})
        tm.ok(result)
        tm.that(len(result.value), eq=1)

    def test_handler_protocol_real_behavior(self) -> None:
        """Handler creates then lists apps via real request dispatch."""
        self._reset_protocol_state()
        handler = u.Web.WebHandler
        create_result = handler.handle_request({
            "action": "create",
            "name": "handler-app",
            "port": 8082,
            "host": "localhost",
        })
        tm.ok(create_result)
        list_result = handler.handle_request({"action": "list"})
        tm.ok(list_result)
        tm.that(list_result.value["count"], eq=1)

    def test_protocol_app_lifecycle_end_to_end(self) -> None:
        """Create, list, start, and stop transition through real app states."""
        self._reset_protocol_state()
        manager = u.Web.WebAppManager
        create_result = manager.create_app("lifecycle-app", 7070, "localhost")
        tm.ok(create_result)
        app_id = str(create_result.value["id"])
        list_result = manager.list_apps()
        tm.ok(list_result)
        tm.that(len(list_result.value), eq=1)
        tm.that(list_result.value[0]["status"], eq=c.Web.Status.STOPPED.value)
        start_result = manager.start_app(app_id)
        tm.ok(start_result)
        tm.that(start_result.value["status"], eq=c.Web.Status.RUNNING.value)
        stop_result = manager.stop_app(app_id)
        tm.ok(stop_result)
        tm.that(stop_result.value["status"], eq=c.Web.Status.STOPPED.value)

    def test_create_app_configures_protocol_health_route(self) -> None:
        """create_app registers the real /protocol/health endpoint."""
        self._reset_protocol_state()
        manager = u.Web.WebAppManager
        create_result = manager.create_app("route-app", 7171, "localhost")
        tm.ok(create_result)
        app_id = str(create_result.value["id"])
        framework = str(create_result.value["framework"])
        app_instance = u.Web.framework_instances[app_id]
        if framework == "fastapi" and isinstance(app_instance, FastAPI):
            paths = [
                route.path
                for route in app_instance.routes
                if isinstance(route, APIRoute)
            ]
            tm.that(paths, has="/protocol/health")
        elif isinstance(app_instance, flask.Flask):
            routes = [rule.rule for rule in app_instance.url_map.iter_rules()]
            tm.that(routes, has="/protocol/health")

    def test_start_stop_manage_runtime_registry(self) -> None:
        """Runtime metadata persists on start and is cleaned up on stop."""
        self._reset_protocol_state()
        manager = u.Web.WebAppManager
        created = manager.create_app("runtime-app", 7272, "localhost")
        tm.ok(created)
        app_id = str(created.value["id"])
        started = manager.start_app(app_id)
        tm.ok(started)
        tm.that(u.Web.app_runtimes, has=app_id)
        stopped = manager.stop_app(app_id)
        tm.ok(stopped)
        tm.that(app_id not in u.Web.app_runtimes, eq=True)
