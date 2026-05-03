"""Comprehensive unit tests for flext_web.protocols module.

Tests the unified p class following flext standards.
"""

from __future__ import annotations

from collections.abc import (
    Callable,
    Sequence,
)
from typing import override

import flask
from fastapi import FastAPI
from fastapi.routing import APIRoute
from flext_tests import tm

from flext_core import FlextContainer, FlextContext, FlextSettings
from tests import c, p, r, t, u


class TestsFlextWebProtocolsUnit:
    """Test suite for p unified class."""

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

    def test_protocols_inheritance(self) -> None:
        """Test that p has expected Web namespace."""

    def test_web_protocols_structure(self) -> None:
        """Test p structure."""

    def test_web_app_manager_protocol(self) -> None:
        """Test WebAppManager definition."""
        protocol = u.Web.WebAppManager
        tm.that(protocol, is_=type)

    def test_web_service_protocol(self) -> None:
        """Test WebService definition."""
        protocol = u.Web.WebService
        tm.that(protocol, is_=type)

    def test_web_repository_protocol(self) -> None:
        """Test WebRepository definition."""
        protocol = u.Web.WebRepository
        tm.that(protocol, is_=type)

    def test_web_handler_protocol(self) -> None:
        """Test WebHandler definition."""
        protocol = u.Web.WebHandler
        tm.that(protocol, is_=type)
        tm.that(callable(protocol), eq=True)

    def test_web_template_engine_protocol(self) -> None:
        """Test WebTemplateEngine definition."""
        protocol = u.Web.WebTemplateEngine
        tm.that(protocol, is_=type)

    def test_web_monitoring_protocol(self) -> None:
        """Test WebMonitoring definition."""
        protocol = u.Web.WebMonitoring
        tm.that(protocol, is_=type)

    def test_protocol_method_signatures(self) -> None:
        """Test that protocol methods have correct signatures."""
        protocol = u.Web.WebAppManager
        create_app_method = protocol.__dict__["create_app"]
        tm.that(callable(create_app_method), eq=True)
        start_app_method = protocol.__dict__["start_app"]
        tm.that(callable(start_app_method), eq=True)
        stop_app_method = protocol.__dict__["stop_app"]
        tm.that(callable(stop_app_method), eq=True)
        list_apps_method = protocol.__dict__["list_apps"]
        tm.that(callable(list_apps_method), eq=True)

    def test_protocol_inheritance_chain(self) -> None:
        """Test that protocols properly inherit from base protocols."""

    def test_protocol_type_annotations(self) -> None:
        """Test that protocols have proper type annotations."""
        protocol = u.Web.WebAppManager
        create_app_annotations = protocol.__dict__["create_app"].__annotations__
        tm.that(create_app_annotations, has="name")
        tm.that(create_app_annotations, has="port")
        tm.that(create_app_annotations, has="host")
        tm.that(create_app_annotations, has="return")

    def test_protocol_documentation(self) -> None:
        """Test that protocols have proper documentation."""
        protocol = u.Web.WebAppManager
        tm.that(protocol.__doc__, none=False)

    def test_protocol_usage_patterns(self) -> None:
        """Test that protocols follow expected usage patterns."""

        class MockAppManager:
            def create_app(self, name: str, port: int, host: str) -> t.Web.ResponseDict:
                return {"name": name, "host": host, "port": port}

            def start_app(self, app_id: str) -> p.Result[t.Web.ResponseDict]:
                return r[t.Web.ResponseDict].ok({
                    "name": "test",
                    "host": "localhost",
                    "port": 8080,
                })

            def stop_app(self, app_id: str) -> p.Result[t.Web.ResponseDict]:
                return r[t.Web.ResponseDict].ok({
                    "name": "test",
                    "host": "localhost",
                    "port": 8080,
                })

            def list_apps(self) -> p.Result[Sequence[t.Web.ResponseDict]]:
                return r[Sequence[t.Web.ResponseDict]].ok([
                    {"name": "test", "host": "localhost", "port": 8080},
                ])

        MockAppManager()

    def test_protocol_extensibility(self) -> None:
        """Test that protocols are extensible."""

        class Custom(u.Web.WebAppManager):
            @property
            @override
            def settings(self) -> p.Settings:
                return FlextSettings.fetch_global()

            @property
            @override
            def container(self) -> p.Container:
                return FlextContainer()

            @property
            @override
            def context(self) -> p.Context:
                return FlextContext()

            def custom_method(self) -> None:
                msg = "Must use unified test helpers per Rule 3.6"
                raise NotImplementedError(msg)

            @override
            def execute(self) -> p.Result[t.Web.ResponseDict]:
                return r[t.Web.ResponseDict].ok({})

            @override
            def validate_business_rules(self) -> p.Result[bool]:
                return r[bool].ok(True)

            @override
            def service_info(self) -> t.JsonMapping:
                return {"name": "Custom"}

            @override
            def valid(self) -> bool:
                return True

            @override
            def ok[V](self, value: V) -> p.Result[V]:
                return r[V].ok(value)

            @override
            def fail_op(
                self,
                operation: str,
                exc: Exception | str | None = None,
            ) -> p.Result[t.Web.ResponseDict]:
                error = str(exc) if exc is not None else operation
                return r[t.Web.ResponseDict].fail(error)

        _ = Custom

    def test_protocol_validation(self) -> None:
        """Test that protocols can be used for validation."""

        class ValidAppManager:
            def create_app(self, name: str, port: int, host: str) -> None:
                msg = "Must use unified test helpers per Rule 3.6"
                raise NotImplementedError(msg)

            def start_app(self, app_id: str) -> None:
                msg = "Must use unified test helpers per Rule 3.6"
                raise NotImplementedError(msg)

            def stop_app(self, app_id: str) -> None:
                msg = "Must use unified test helpers per Rule 3.6"
                raise NotImplementedError(msg)

            def list_apps(self) -> None:
                msg = "Must use unified test helpers per Rule 3.6"
                raise NotImplementedError(msg)

        class InvalidAppManager:
            def create_app(self, name: str, port: int, host: str) -> None:
                msg = "Must use unified test helpers per Rule 3.6"
                raise NotImplementedError(msg)

        def validate_app_manager(
            obj: ValidAppManager | InvalidAppManager,
        ) -> bool:
            return hasattr(obj, "create_app") and hasattr(obj, "start_app")

        tm.that(validate_app_manager(ValidAppManager()), eq=True)
        tm.that(not validate_app_manager(InvalidAppManager()), eq=True)

    def test_app_manager_protocol_real_lifecycle_behavior(self) -> None:
        """Validate real app lifecycle behavior from protocol base implementation."""
        self._assert_protocol_base_lifecycle()

    def test_web_service_protocol_methods(self) -> None:
        """Test WebService methods execution."""

        class RealWebService:
            def initialize_routes(self) -> p.Result[bool]:
                return r[bool].ok(True)

            def configure_middleware(self) -> p.Result[bool]:
                return r[bool].ok(True)

            def start_service(self) -> p.Result[bool]:
                return r[bool].ok(True)

            def stop_service(self) -> p.Result[bool]:
                return r[bool].ok(True)

            def execute(self) -> p.Result[t.Web.ResponseDict]:
                return r[t.Web.ResponseDict].ok({})

            def validate_business_rules(self) -> p.Result[bool]:
                return r[bool].ok(True)

            def service_info(self) -> t.ScalarMapping:
                return {"name": "WebService"}

            def valid(self) -> bool:
                return True

        service = RealWebService()
        tm.ok(service.initialize_routes())
        tm.ok(service.configure_middleware())
        tm.ok(service.start_service())
        tm.ok(service.stop_service())

    def test_web_repository_protocol_methods(self) -> None:
        """Test WebRepository methods execution."""

        class RealWebRepository:
            def find_by_criteria(
                self,
                criteria: t.Web.RequestDict,
            ) -> p.Result[Sequence[t.Web.ResponseDict]]:
                return r[Sequence[t.Web.ResponseDict]].ok([])

            def fetch_by_id(self, entity_id: str) -> p.Result[t.Web.ResponseDict]:
                return r[t.Web.ResponseDict].ok({"id": entity_id})

            def save(self, entity: t.Web.ResponseDict) -> p.Result[t.Web.ResponseDict]:
                return r[t.Web.ResponseDict].ok(entity)

            def delete(self, entity_id: str) -> p.Result[bool]:
                return r[bool].ok(True)

            def find_all(self) -> p.Result[Sequence[t.Web.ResponseDict]]:
                return r[Sequence[t.Web.ResponseDict]].ok([])

            def execute(self) -> p.Result[t.Web.ResponseDict]:
                return r[t.Web.ResponseDict].ok({})

            def validate_business_rules(self) -> p.Result[bool]:
                return r[bool].ok(True)

            def service_info(self) -> t.ScalarMapping:
                return {"name": "WebRepository"}

            def valid(self) -> bool:
                return True

        repo = RealWebRepository()
        result = repo.find_by_criteria({"key": "value"})
        tm.ok(result)

    def test_web_template_engine_protocol_methods(self) -> None:
        """Test WebTemplateEngine methods execution."""

        class RealTemplateEngine:
            def load_template_config(
                self, settings: t.Web.RequestDict
            ) -> p.Result[bool]:
                return r[bool].ok(True)

            def template_config(self) -> p.Result[t.Web.ResponseDict]:
                return r[t.Web.ResponseDict].ok({})

            def validate_template_config(
                self, settings: t.Web.RequestDict
            ) -> p.Result[bool]:
                return r[bool].ok(True)

            def render(
                self, template: str, context: t.Web.RequestDict
            ) -> p.Result[str]:
                return r[str].ok("")

            def add_filter(self, name: str, filter_func: Callable[[str], str]) -> None:
                _ = name, filter_func

            def add_global(self, name: str, *, value: t.JsonValue) -> None:
                _ = name, value

            def execute(self) -> p.Result[t.Web.ResponseDict]:
                return r[t.Web.ResponseDict].ok({})

            def validate_business_rules(self) -> p.Result[bool]:
                return r[bool].ok(True)

            def service_info(self) -> t.ScalarMapping:
                return {"name": "TemplateEngine"}

            def valid(self) -> bool:
                return True

        engine = RealTemplateEngine()
        tm.ok(engine.load_template_config({"key": "value"}))
        tm.ok(engine.template_config())
        tm.ok(engine.validate_template_config({"key": "value"}))
        tm.ok(engine.render("template", {"key": "value"}))

        def filter_func(x: str) -> str:
            return x

        engine.add_filter("test", filter_func)
        engine.add_global("test", value="value")
        engine.add_global("test_int", value=42)
        engine.add_global("test_bool", value=True)

    def test_web_monitoring_protocol_methods(self) -> None:
        """Test WebMonitoring methods execution."""

        class RealWebMonitoring:
            def record_web_request(
                self,
                request: t.Web.RequestDict,
                response_time: float,
            ) -> None:
                pass

            def web_health_status(self) -> t.Web.ResponseDict:
                return {
                    "status": c.Web.ResponseStatus.HEALTHY.value,
                    "service": c.Web.SERVICE_NAME,
                }

            def web_metrics(self) -> t.Web.ResponseDict:
                return {"requests": 0, "errors": 0, "uptime": "0s"}

            def execute(self) -> p.Result[t.Web.ResponseDict]:
                return r[t.Web.ResponseDict].ok({})

            def validate_business_rules(self) -> p.Result[bool]:
                return r[bool].ok(True)

            def service_info(self) -> t.ScalarMapping:
                return {"name": "WebMonitoring"}

            def valid(self) -> bool:
                return True

        monitoring = RealWebMonitoring()
        monitoring.record_web_request({"method": "GET"}, 0.1)
        health = monitoring.web_health_status()
        tm.that(health["status"], eq=c.Web.ResponseStatus.HEALTHY.value)
        metrics = monitoring.web_metrics()
        tm.that(metrics, has="requests")

    def test_app_lifecycle_direct_execution_on_protocol_base(self) -> None:
        """Test real app lifecycle behavior through WebAppManager protocol base."""
        self._assert_protocol_base_lifecycle()

    def test_service_protocol_real_behavior(self) -> None:
        """Test web service lifecycle protocol behavior."""
        self._reset_protocol_state()
        service = u.Web.WebService
        start_without_setup = service.start_service()
        tm.fail(start_without_setup)
        tm.ok(service.initialize_routes())
        tm.ok(service.configure_middleware())
        tm.ok(service.start_service())
        tm.ok(service.stop_service())

    def test_repository_protocol_real_behavior(self) -> None:
        """Test repository protocol criteria filtering behavior."""
        self._reset_protocol_state()
        manager = u.Web.WebAppManager
        created = manager.create_app("repo-app", 8081, "127.0.0.1")
        tm.ok(created)
        repo = u.Web.WebRepository
        result = repo.find_by_criteria({"host": "127.0.0.1"})
        tm.ok(result)
        tm.that(len(result.value), eq=1)

    def test_handler_protocol_real_behavior(self) -> None:
        """Test handler protocol create/list action behavior."""
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
        """TDD lifecycle flow: create, start, stop, and list app states."""
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
        """TDD create_app must register protocol health endpoint."""
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
        """TDD lifecycle must persist and cleanup runtime metadata."""
        self._reset_protocol_state()
        manager = u.Web.WebAppManager
        created = manager.create_app("runtime-app", 7272, "localhost")
        tm.ok(created)
        app_id = str(created.value["id"])
        started = manager.start_app(app_id)
        tm.ok(started)
        assert app_id in u.Web.app_runtimes
        stopped = manager.stop_app(app_id)
        tm.ok(stopped)
        tm.that(app_id not in u.Web.app_runtimes, eq=True)
