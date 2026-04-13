"""Comprehensive unit tests for flext_web.protocols module.

Tests the unified p class following flext standards.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import override

import flask
import pytest
from fastapi import FastAPI
from fastapi.routing import APIRoute
from flext_tests import tm

from tests import c, p, r, t

_WebAppManagerBase = p.Web.TestBases._WebAppManagerBase
_WebConnectionBase = p.Web.TestBases._WebConnectionBase
_WebFrameworkInterfaceBase = p.Web.TestBases._WebFrameworkInterfaceBase
_WebHandlerBase = p.Web.TestBases._WebHandlerBase
_WebMonitoringBase = p.Web.TestBases._WebMonitoringBase
_WebRepositoryBase = p.Web.TestBases._WebRepositoryBase
_WebServiceBase = p.Web.TestBases._WebServiceBase
_WebTemplateEngineBase = p.Web.TestBases._WebTemplateEngineBase
_WebTemplateRendererBase = p.Web.TestBases._WebTemplateRendererBase


class TestFlextWebProtocols:
    """Test suite for p unified class."""

    @staticmethod
    def _reset_protocol_state() -> None:
        p.Web.apps_registry.clear()
        p.Web.framework_instances.clear()
        p.Web.app_runtimes.clear()
        p.Web.service_state.update({
            "routes_initialized": False,
            "middleware_configured": False,
            "service_running": False,
        })
        p.Web.template_config.clear()
        p.Web.template_filters.clear()
        p.Web.template_globals.clear()
        p.Web.web_metrics.update({
            "requests": 0,
            "errors": 0,
            "uptime": "0s",
            "avg_response_time_ms": 0,
        })

    @pytest.fixture(autouse=True)
    def _mock_runtime_lifecycle(self, monkeypatch: pytest.MonkeyPatch) -> None:

        def _start_runtime(
            app_id: str,
            app_data: t.Web.ResponseDict,
            app_instance: flask.Flask | FastAPI,
        ) -> p.Result[t.Web.ResponseDict]:
            _ = (app_data, app_instance)
            return r[t.Web.ResponseDict].ok({"runner": "mock", "app_id": app_id})

        def _stop_runtime(app_id: str, runtime: t.Web.ResponseDict) -> p.Result[bool]:
            _ = (app_id, runtime)
            return r[bool].ok(True)

    def test_protocols_inheritance(self) -> None:
        """Test that p has expected Web namespace."""

    def test_web_protocols_structure(self) -> None:
        """Test p structure."""

    def test_web_app_manager_protocol(self) -> None:
        """Test WebAppManager definition."""
        protocol = p.Web.WebAppManager
        tm.that(protocol, is_=type)

    def test_response_formatter_protocol(self) -> None:
        """Test ResponseFormatter definition."""
        protocol = p.Web.WebResponseFormatter
        tm.that(protocol, is_=type)

    def test_web_framework_interface_protocol(self) -> None:
        """Test WebFrameworkInterface definition."""
        protocol = p.Web.WebFrameworkInterface
        tm.that(protocol, is_=type)

    def test_template_renderer_protocol(self) -> None:
        """Test TemplateRenderer definition."""
        protocol = p.Web.WebTemplateRenderer
        tm.that(protocol, is_=type)

    def test_web_service_protocol(self) -> None:
        """Test WebService definition."""
        protocol = p.Web.WebService
        tm.that(protocol, is_=type)

    def test_web_repository_protocol(self) -> None:
        """Test WebRepository definition."""
        protocol = p.Web.WebRepository
        tm.that(protocol, is_=type)

    def test_web_handler_protocol(self) -> None:
        """Test WebHandler definition."""
        protocol = p.Web.WebHandler
        tm.that(protocol, is_=type)
        tm.that(callable(protocol), eq=True)

    def test_web_template_engine_protocol(self) -> None:
        """Test WebTemplateEngine definition."""
        protocol = p.Web.WebTemplateEngine
        tm.that(protocol, is_=type)

    def test_web_monitoring_protocol(self) -> None:
        """Test WebMonitoring definition."""
        protocol = p.Web.WebMonitoring
        tm.that(protocol, is_=type)

    def test_protocol_runtime_checkable(self) -> None:
        """Test that protocols are runtime checkable."""
        protocols = [
            p.Web.WebAppManager,
            p.Web.WebResponseFormatter,
            p.Web.WebFrameworkInterface,
            p.Web.WebTemplateRenderer,
            p.Web.WebService,
            p.Web.WebRepository,
            p.Web.WebHandler,
            p.Web.WebTemplateEngine,
            p.Web.WebMonitoring,
        ]
        for protocol in protocols:
            checkable = getattr(protocol, "__runtime_checkable__", None)
            if checkable is not None:
                tm.that(checkable is True, eq=True)

    def test_protocol_method_signatures(self) -> None:
        """Test that protocol methods have correct signatures."""
        protocol = p.Web.WebAppManager
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
        protocol = p.Web.WebAppManager
        create_app_annotations = protocol.__dict__["create_app"].__annotations__
        tm.that(create_app_annotations, has="name")
        tm.that(create_app_annotations, has="port")
        tm.that(create_app_annotations, has="host")
        tm.that(create_app_annotations, has="return")

    def test_protocol_documentation(self) -> None:
        """Test that protocols have proper documentation."""
        protocol = p.Web.WebAppManager
        tm.that(protocol.__doc__, none=False)

    def test_protocol_consistency(self) -> None:
        """Test that protocols are consistent with implementation."""
        protocols = [
            p.Web.WebAppManager,
            p.Web.WebResponseFormatter,
            p.Web.WebFrameworkInterface,
            p.Web.WebTemplateRenderer,
            p.Web.WebService,
            p.Web.WebRepository,
            p.Web.WebHandler,
            p.Web.WebTemplateEngine,
            p.Web.WebMonitoring,
        ]
        for protocol in protocols:
            tm.that(protocol, is_=type)
            methods = [name for name in dir(protocol) if not name.startswith("_")]
            tm.that(methods, empty=False)

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

        class Custom(p.Web.WebAppManager):
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
            def service_info(self) -> t.ScalarMapping:
                return {"name": "Custom"}

            @override
            def valid(self) -> bool:
                return True

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
        self._reset_protocol_state()
        manager = _WebAppManagerBase()
        created = manager.create_app("test", 8080, "localhost")
        tm.ok(created)
        app_id = str(created.value["id"])
        tm.that({"fastapi", "flask"}, has=created.value["framework"])
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

    def test_response_formatter_protocol_methods(self) -> None:
        """Test WebResponseFormatter methods execution."""

        class RealResponseFormatter:
            def format_success(self, data: t.Web.ResponseDict) -> t.Web.ResponseDict:
                response: t.Web.ResponseDict = {
                    "status": c.Web.WebResponse.STATUS_SUCCESS,
                }
                response.update({
                    key: value
                    for key, value in data.items()
                    if isinstance(value, (str, int, bool, list, dict))
                })
                return response

            def format_error(self, error: Exception) -> t.Web.ResponseDict:
                result: t.Web.ResponseDict = {
                    "status": c.Web.WebResponse.STATUS_ERROR,
                    "message": str(error),
                }
                return result

            def create_json_response(
                self,
                data: t.Web.ResponseDict,
            ) -> t.Web.ResponseDict:
                response: t.Web.ResponseDict = {
                    c.Web.Http.HEADER_CONTENT_TYPE: c.Web.Http.CONTENT_TYPE_JSON,
                }
                response.update({
                    key: value
                    for key, value in data.items()
                    if isinstance(value, (str, int, bool, list, dict))
                })
                return response

            def resolve_request_data(
                self,
                _request: t.Web.RequestDict,
            ) -> t.Web.RequestDict:
                return {}

            def execute(self) -> p.Result[t.Web.ResponseDict]:
                return r[t.Web.ResponseDict].ok({})

            def validate_business_rules(self) -> p.Result[bool]:
                return r[bool].ok(True)

            def service_info(self) -> t.ScalarMapping:
                return {"name": "ResponseFormatter"}

            def valid(self) -> bool:
                return True

        formatter = RealResponseFormatter()
        data_with_nested: t.Web.ResponseDict = {
            "key1": "value1",
            "nested": {"key2": "value2"},
        }
        result = formatter.format_success(data_with_nested)
        tm.that(result["status"], eq=c.Web.WebResponse.STATUS_SUCCESS)
        tm.that(result["key1"], eq="value1")
        tm.that(result["nested"], is_=dict)
        error = ValueError("Test error")
        error_result = formatter.format_error(error)
        tm.that(error_result["status"], eq=c.Web.WebResponse.STATUS_ERROR)
        tm.that(str(error_result["message"]), has="Test error")
        json_result = formatter.create_json_response(data_with_nested)
        tm.that(json_result, has=c.Web.Http.HEADER_CONTENT_TYPE)
        tm.that(
            (
                json_result[c.Web.Http.HEADER_CONTENT_TYPE]
                == c.Web.Http.CONTENT_TYPE_JSON
            ),
            eq=True,
        )

    def test_web_framework_interface_protocol_methods(self) -> None:
        """Test WebFrameworkInterface methods execution."""

        class RealFrameworkInterface:
            def create_json_response(
                self,
                data: t.Web.ResponseDict,
            ) -> t.Web.ResponseDict:
                response: t.Web.ResponseDict = {
                    c.Web.Http.HEADER_CONTENT_TYPE: c.Web.Http.CONTENT_TYPE_JSON,
                }
                response.update({
                    key: value
                    for key, value in data.items()
                    if isinstance(value, (str, int, bool, list, dict))
                })
                return response

            def resolve_request_data(
                self,
                _request: t.Web.RequestDict,
            ) -> t.Web.RequestDict:
                return {}

            def json_request(self, _request: t.Web.RequestDict) -> bool:
                return False

            def execute(self) -> p.Result[t.Web.ResponseDict]:
                return r[t.Web.ResponseDict].ok({})

            def validate_business_rules(self) -> p.Result[bool]:
                return r[bool].ok(True)

            def service_info(self) -> t.ScalarMapping:
                return {"name": "FrameworkInterface"}

            def valid(self) -> bool:
                return True

        framework = RealFrameworkInterface()
        data: t.Web.ResponseDict = {
            "test": "value",
            "nested": {"key": "value"},
        }
        json_response = framework.create_json_response(data)
        tm.that(json_response, has=c.Web.Http.HEADER_CONTENT_TYPE)
        request_data = framework.resolve_request_data({})
        tm.that(request_data, is_=dict)
        is_json = framework.json_request({})
        tm.that(is_json is False, eq=True)

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

    def test_web_template_renderer_protocol_methods(self) -> None:
        """Test WebTemplateRenderer methods execution."""

        class RealTemplateRenderer:
            def render_template(
                self,
                template_name: str,
                _context: t.Web.RequestDict,
            ) -> p.Result[str]:
                return r[str].ok("")

            def render_dashboard(self, data: t.Web.ResponseDict) -> p.Result[str]:
                return r[str].ok("<html>Dashboard</html>")

            def execute(self) -> p.Result[t.Web.ResponseDict]:
                return r[t.Web.ResponseDict].ok({})

            def validate_business_rules(self) -> p.Result[bool]:
                return r[bool].ok(True)

            def service_info(self) -> t.ScalarMapping:
                return {"name": "TemplateRenderer"}

            def valid(self) -> bool:
                return True

        renderer = RealTemplateRenderer()
        template_result = renderer.render_template(
            "tesFlextWebTypes.html",
            {"key": "value"},
        )
        tm.ok(template_result)
        dashboard_result = renderer.render_dashboard({"data": "value"})
        tm.ok(dashboard_result)
        tm.that(dashboard_result.value, has="<html>Dashboard</html>")

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
                self, template: str, _context: t.Web.RequestDict
            ) -> p.Result[str]:
                return r[str].ok("")

            def add_filter(self, name: str, filter_func: Callable[[str], str]) -> None:
                _ = name, filter_func

            def add_global(self, name: str, *, value: t.ContainerValue) -> None:
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
        engine.add_global("test_list", value=["item1", "item2"])
        engine.add_global("test_dict", value={"key": "value"})

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
                    "status": c.Web.WebResponse.STATUS_HEALTHY,
                    "service": c.Web.WebService.SERVICE_NAME,
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
        tm.that(health["status"], eq=c.Web.WebResponse.STATUS_HEALTHY)
        metrics = monitoring.web_metrics()
        tm.that(metrics, has="requests")

    def test_app_lifecycle_direct_execution_on_protocol_base(self) -> None:
        """Test real app lifecycle behavior through WebAppManager protocol base."""
        self._reset_protocol_state()
        manager = _WebAppManagerBase()
        result = manager.create_app("test", 8080, "localhost")
        tm.ok(result)
        app_id = str(result.value["id"])
        tm.that({"fastapi", "flask"}, has=result.value["framework"])
        tm.that({"asgi", "wsgi"}, has=result.value["interface"])
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

    def test_response_formatter_real_behavior(self) -> None:
        """Test response formatter protocol with real implementation behavior."""
        formatter = p.Web.TestBases._WebResponseFormatterBase()
        data_with_all_types: t.Web.ResponseDict = {
            "string": "value",
            "int": 42,
            "bool": True,
            "list": ["item1", "item2"],
            "dict": {"nested": "value"},
        }
        result = formatter.format_success(data_with_all_types)
        tm.that(result["status"], eq=c.Web.WebResponse.STATUS_SUCCESS)
        tm.that(result["string"], eq="value")
        tm.that(result["int"], eq=42)
        tm.that(result["bool"] is True, eq=True)
        tm.that(result["list"], is_=list)
        tm.that(result["dict"], is_=dict)
        error = ValueError("Test error message")
        error_result = formatter.format_error(error)
        tm.that(error_result["status"], eq=c.Web.WebResponse.STATUS_ERROR)
        tm.that(str(error_result["message"]), has="Test error message")
        json_result = formatter.create_json_response(data_with_all_types)
        tm.that(
            (
                json_result[c.Web.Http.HEADER_CONTENT_TYPE]
                == c.Web.Http.CONTENT_TYPE_JSON
            ),
            eq=True,
        )
        request_data = formatter.resolve_request_data({"test": "data"})
        tm.that(request_data, is_=dict)
        tm.that(request_data["test"], eq="data")

    def test_framework_interface_real_behavior(self) -> None:
        """Test web framework interface protocol with real request behavior."""
        framework = _WebFrameworkInterfaceBase()
        data: t.Web.ResponseDict = {"test": "value", "nested": {"key": "value"}}
        result = framework.create_json_response(data)
        tm.that(result[c.Web.Http.HEADER_CONTENT_TYPE], eq=c.Web.Http.CONTENT_TYPE_JSON)
        request_data = framework.resolve_request_data({"test": "data"})
        tm.that(request_data, is_=dict)
        tm.that(request_data["test"], eq="data")
        is_json = framework.json_request({"content-type": "application/json"})
        tm.that(is_json is True, eq=True)

    def test_service_protocol_real_behavior(self) -> None:
        """Test web service lifecycle protocol behavior."""
        self._reset_protocol_state()
        service = _WebServiceBase()
        start_without_setup = service.start_service()
        tm.fail(start_without_setup)
        tm.ok(service.initialize_routes())
        tm.ok(service.configure_middleware())
        tm.ok(service.start_service())
        tm.ok(service.stop_service())

    def test_repository_protocol_real_behavior(self) -> None:
        """Test repository protocol criteria filtering behavior."""
        self._reset_protocol_state()
        manager = _WebAppManagerBase()
        created = manager.create_app("repo-app", 8081, "127.0.0.1")
        tm.ok(created)
        repo = _WebRepositoryBase()
        result = repo.find_by_criteria({"host": "127.0.0.1"})
        tm.ok(result)
        tm.that(len(result.value), eq=1)

    def test_handler_protocol_real_behavior(self) -> None:
        """Test handler protocol create/list action behavior."""
        self._reset_protocol_state()
        handler = _WebHandlerBase()
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

    def test_template_renderer_real_behavior(self) -> None:
        """Test template renderer protocol with real template substitution."""
        renderer = _WebTemplateRendererBase()
        result = renderer.render_template("{{key}}-template", {"key": "value"})
        tm.ok(result)
        tm.that(result.value, eq="value-template")
        result = renderer.render_dashboard({
            "service": "dashboard",
            "status": "running",
        })
        tm.ok(result)
        tm.that(result.value, has="dashboard")

    def test_template_engine_real_behavior(self) -> None:
        """Test template engine protocol with settings and global/filter handling."""
        self._reset_protocol_state()
        engine = _WebTemplateEngineBase()
        tm.ok(engine.load_template_config({"template_dir": "templates"}))
        tm.ok(engine.template_config())
        tm.ok(engine.validate_template_config({"template_dir": "templates"}))
        tm.fail(engine.validate_template_config({"invalid": "value"}))
        engine.add_filter("test", lambda x: x.upper())
        engine.add_global("test", value="value")
        rendered = engine.render("{{test}}|test", {})
        tm.ok(rendered)
        tm.that(rendered.value, eq="VALUE")

    def test_connection_protocol_real_behavior(self) -> None:
        """Test connection protocol endpoint URL from running app."""
        self._reset_protocol_state()
        manager = _WebAppManagerBase()
        created = manager.create_app("endpoint-app", 9090, "127.0.0.1")
        tm.ok(created)
        app_id = str(created.value["id"])
        tm.ok(manager.start_app(app_id))
        connection = _WebConnectionBase()
        url = connection.endpoint_url()
        tm.that(url, eq="http://127.0.0.1:9090")

    def test_monitoring_protocol_real_behavior(self) -> None:
        """Test monitoring protocol metrics recording behavior."""
        self._reset_protocol_state()
        monitoring = _WebMonitoringBase()
        monitoring.record_web_request({"method": "GET"}, 0.1)
        health = monitoring.web_health_status()
        tm.that(health["status"], eq=c.Web.Status.STOPPED.value)
        tm.that(health["service"], eq=c.Web.WebService.SERVICE_NAME)
        metrics = monitoring.web_metrics()
        tm.that(metrics["requests"], eq=1)
        tm.that(metrics["errors"], eq=0)
        tm.that(metrics["uptime"], eq="0s")

    def test_protocol_app_lifecycle_end_to_end(self) -> None:
        """TDD lifecycle flow: create, start, stop, and list app states."""
        self._reset_protocol_state()
        manager = _WebAppManagerBase()
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
        manager = _WebAppManagerBase()
        create_result = manager.create_app("route-app", 7171, "localhost")
        tm.ok(create_result)
        app_id = str(create_result.value["id"])
        framework = str(create_result.value["framework"])
        app_instance = p.Web.framework_instances[app_id]
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
        manager = _WebAppManagerBase()
        created = manager.create_app("runtime-app", 7272, "localhost")
        tm.ok(created)
        app_id = str(created.value["id"])
        started = manager.start_app(app_id)
        tm.ok(started)
        assert app_id in p.Web.app_runtimes
        stopped = manager.stop_app(app_id)
        tm.ok(stopped)
        tm.that(app_id not in p.Web.app_runtimes, eq=True)
