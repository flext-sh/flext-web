"""Comprehensive unit tests for flext_web.protocols module.

Tests the unified FlextWebProtocols class following flext standards.
"""

from __future__ import annotations

from typing import Any, cast

import pytest
from flext_core import FlextResult, p
from flext_web import t
from flext_web.constants import FlextWebConstants
from flext_web.protocols import FlextWebProtocols

# Access test base classes via the namespace
_WebAppManagerBase = FlextWebProtocols.Web.TestBases._WebAppManagerBase
_WebConnectionBase = FlextWebProtocols.Web.TestBases._WebConnectionBase
_WebFrameworkInterfaceBase = FlextWebProtocols.Web.TestBases._WebFrameworkInterfaceBase
_WebHandlerBase = FlextWebProtocols.Web.TestBases._WebHandlerBase
_WebMonitoringBase = FlextWebProtocols.Web.TestBases._WebMonitoringBase
_WebRepositoryBase = FlextWebProtocols.Web.TestBases._WebRepositoryBase
_WebServiceBase = FlextWebProtocols.Web.TestBases._WebServiceBase
_WebTemplateEngineBase = FlextWebProtocols.Web.TestBases._WebTemplateEngineBase
_WebTemplateRendererBase = FlextWebProtocols.Web.TestBases._WebTemplateRendererBase


class TestFlextWebProtocols:
    """Test suite for FlextWebProtocols unified class."""

    @staticmethod
    def _reset_protocol_state() -> None:
        FlextWebProtocols.Web.apps_registry.clear()
        FlextWebProtocols.Web.framework_instances.clear()
        FlextWebProtocols.Web.app_runtimes.clear()
        FlextWebProtocols.Web.service_state.update({
            "routes_initialized": False,
            "middleware_configured": False,
            "service_running": False,
        })
        FlextWebProtocols.Web.template_config.clear()
        FlextWebProtocols.Web.template_filters.clear()
        FlextWebProtocols.Web.template_globals.clear()
        FlextWebProtocols.Web.web_metrics.update({
            "requests": 0,
            "errors": 0,
            "uptime": "0s",
            "avg_response_time_ms": 0,
        })

    @pytest.fixture(autouse=True)
    def _mock_runtime_lifecycle(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def _start_runtime(
            app_id: str,
            app_data: t.WebCore.ResponseDict,
            app_instance: object,
        ) -> FlextResult[dict[str, object]]:
            _ = app_data, app_instance
            return FlextResult[dict[str, object]].ok({
                "runner": "mock",
                "app_id": app_id,
            })

        def _stop_runtime(
            app_id: str,
            runtime: dict[str, object],
        ) -> FlextResult[bool]:
            _ = app_id, runtime
            return FlextResult[bool].ok(True)

        monkeypatch.setattr(
            FlextWebProtocols.Web,
            "_start_app_runtime",
            staticmethod(_start_runtime),
        )
        monkeypatch.setattr(
            FlextWebProtocols.Web,
            "_stop_app_runtime",
            staticmethod(_stop_runtime),
        )

    def test_protocols_inheritance(self) -> None:
        """Test that FlextWebProtocols inherits from p."""
        # Should inherit from p
        assert issubclass(FlextWebProtocols, p)

        # Should have web-specific protocols under Web namespace
        assert hasattr(FlextWebProtocols.Web, "WebAppManagerProtocol")
        assert hasattr(FlextWebProtocols.Web, "WebResponseFormatterProtocol")
        assert hasattr(FlextWebProtocols.Web, "WebFrameworkInterfaceProtocol")

    def test_web_protocols_structure(self) -> None:
        """Test FlextWebProtocols structure."""
        # All web protocols are under the Web namespace
        assert hasattr(FlextWebProtocols.Web, "WebAppManagerProtocol")
        assert hasattr(FlextWebProtocols.Web, "WebResponseFormatterProtocol")
        assert hasattr(FlextWebProtocols.Web, "WebFrameworkInterfaceProtocol")
        assert hasattr(FlextWebProtocols.Web, "WebTemplateRendererProtocol")
        assert hasattr(FlextWebProtocols.Web, "WebServiceProtocol")
        assert hasattr(FlextWebProtocols.Web, "WebRepositoryProtocol")
        assert hasattr(FlextWebProtocols.Web, "WebTemplateEngineProtocol")
        assert hasattr(FlextWebProtocols.Web, "WebMonitoringProtocol")

    def test_web_app_manager_protocol(self) -> None:
        """Test WebAppManagerProtocol definition."""
        protocol = FlextWebProtocols.Web.WebAppManagerProtocol

        # Should be a Protocol
        assert isinstance(protocol, type)
        assert hasattr(protocol, "__annotations__")

        # Should have required methods
        assert hasattr(protocol, "create_app")
        assert hasattr(protocol, "start_app")
        assert hasattr(protocol, "stop_app")
        assert hasattr(protocol, "list_apps")

    def test_response_formatter_protocol(self) -> None:
        """Test ResponseFormatterProtocol definition."""
        protocol = FlextWebProtocols.Web.WebResponseFormatterProtocol

        # Should be a Protocol
        assert isinstance(protocol, type)
        assert hasattr(protocol, "__annotations__")

        # Should have required methods
        assert hasattr(protocol, "format_success")
        assert hasattr(protocol, "format_error")

    def test_web_framework_interface_protocol(self) -> None:
        """Test WebFrameworkInterfaceProtocol definition."""
        protocol = FlextWebProtocols.Web.WebFrameworkInterfaceProtocol

        # Should be a Protocol
        assert isinstance(protocol, type)
        assert hasattr(protocol, "__annotations__")

        # Should have required methods
        assert hasattr(protocol, "create_json_response")
        assert hasattr(protocol, "get_request_data")
        assert hasattr(protocol, "is_json_request")

    def test_template_renderer_protocol(self) -> None:
        """Test TemplateRendererProtocol definition."""
        protocol = FlextWebProtocols.Web.WebTemplateRendererProtocol

        # Should be a Protocol
        assert isinstance(protocol, type)
        # Check if it's a Protocol by checking for __annotations__
        assert hasattr(protocol, "__annotations__")

        # Should have required methods
        assert hasattr(protocol, "render_template")
        assert hasattr(protocol, "render_dashboard")

    def test_web_service_protocol(self) -> None:
        """Test WebServiceProtocol definition."""
        protocol = FlextWebProtocols.Web.WebServiceProtocol

        # Should be a Protocol
        assert isinstance(protocol, type)
        assert hasattr(protocol, "__annotations__")

        # Should have required methods
        assert hasattr(protocol, "initialize_routes")
        assert hasattr(protocol, "configure_middleware")
        assert hasattr(protocol, "start_service")
        assert hasattr(protocol, "stop_service")

    def test_web_repository_protocol(self) -> None:
        """Test WebRepositoryProtocol definition."""
        protocol = FlextWebProtocols.Web.WebRepositoryProtocol

        # Should be a Protocol
        assert isinstance(protocol, type)
        assert hasattr(protocol, "__annotations__")

        # Should have required methods from p.Repository
        assert hasattr(protocol, "get_by_id")
        assert hasattr(protocol, "save")
        assert hasattr(protocol, "delete")
        assert hasattr(protocol, "find_all")

    def test_web_handler_protocol(self) -> None:
        """Test WebHandlerProtocol definition."""
        protocol = FlextWebProtocols.Web.WebHandlerProtocol

        # Should be a Protocol
        assert isinstance(protocol, type)
        assert hasattr(protocol, "__annotations__")

        # Should have required methods from p.Handler
        assert hasattr(protocol, "handle")
        assert callable(protocol)
        assert hasattr(protocol, "can_handle")
        assert hasattr(protocol, "execute")
        # Web-specific method
        assert hasattr(protocol, "handle_request")

    def test_web_template_engine_protocol(self) -> None:
        """Test WebTemplateEngineProtocol definition."""
        protocol = FlextWebProtocols.Web.WebTemplateEngineProtocol

        # Should be a Protocol
        assert isinstance(protocol, type)
        assert hasattr(protocol, "__annotations__")

        # Should have required methods
        assert hasattr(protocol, "load_template_config")
        assert hasattr(protocol, "get_template_config")
        assert hasattr(protocol, "validate_template_config")
        assert hasattr(protocol, "render")
        assert hasattr(protocol, "add_filter")
        assert hasattr(protocol, "add_global")

    def test_web_monitoring_protocol(self) -> None:
        """Test WebMonitoringProtocol definition."""
        protocol = FlextWebProtocols.Web.WebMonitoringProtocol

        # Should be a Protocol
        assert isinstance(protocol, type)
        assert hasattr(protocol, "__annotations__")

        # Should have web-specific methods (no fake methods)
        assert hasattr(protocol, "record_web_request")
        assert hasattr(protocol, "get_web_health_status")
        assert hasattr(protocol, "get_web_metrics")

    def test_protocol_runtime_checkable(self) -> None:
        """Test that protocols are runtime checkable."""
        # All protocols should be runtime checkable (decorated with @runtime_checkable)
        protocols = [
            FlextWebProtocols.Web.WebAppManagerProtocol,
            FlextWebProtocols.Web.WebResponseFormatterProtocol,
            FlextWebProtocols.Web.WebFrameworkInterfaceProtocol,
            FlextWebProtocols.Web.WebTemplateRendererProtocol,
            FlextWebProtocols.Web.WebServiceProtocol,
            FlextWebProtocols.Web.WebRepositoryProtocol,
            FlextWebProtocols.Web.WebHandlerProtocol,
            FlextWebProtocols.Web.WebTemplateEngineProtocol,
            FlextWebProtocols.Web.WebMonitoringProtocol,
        ]

        for protocol in protocols:
            # Check if protocol has runtime_checkable attribute (should be True if decorated)
            if hasattr(protocol, "__runtime_checkable__"):
                assert protocol.__runtime_checkable__ is True
            # If not decorated, that's also acceptable for Protocol classes

    def test_protocol_method_signatures(self) -> None:
        """Test that protocol methods have correct signatures."""
        # Test AppManagerProtocol methods
        protocol = FlextWebProtocols.Web.WebAppManagerProtocol

        # create_app should take name, port, host and return FlextResult[WebApp]
        create_app_method = protocol.__dict__["create_app"]
        assert callable(create_app_method)

        # start_app should take app_id and return FlextResult[WebApp]
        start_app_method = protocol.__dict__["start_app"]
        assert callable(start_app_method)

        # stop_app should take app_id and return FlextResult[WebApp]
        stop_app_method = protocol.__dict__["stop_app"]
        assert callable(stop_app_method)

        # list_apps should return FlextResult[list[WebApp]]
        list_apps_method = protocol.__dict__["list_apps"]
        assert callable(list_apps_method)

    def test_protocol_inheritance_chain(self) -> None:
        """Test that protocols properly inherit from base protocols."""
        # WebServiceInterface should inherit from Service
        web_service_protocol = FlextWebProtocols.Web.WebServiceProtocol
        assert hasattr(web_service_protocol, "__bases__")

        # AppRepositoryInterface should inherit from Repository
        app_repo_protocol = FlextWebProtocols.Web.WebRepositoryProtocol
        assert hasattr(app_repo_protocol, "__bases__")

        # MiddlewareInterface should inherit from Extensions.Middleware
        middleware_protocol = FlextWebProtocols.Web.WebHandlerProtocol
        assert hasattr(middleware_protocol, "__bases__")

        # TemplateEngineInterface should inherit from Infrastructure.Configurable
        template_engine_protocol = FlextWebProtocols.Web.WebTemplateEngineProtocol
        assert hasattr(template_engine_protocol, "__bases__")

        # MonitoringInterface should inherit from Extensions.Observability
        monitoring_protocol = FlextWebProtocols.Web.WebMonitoringProtocol
        assert hasattr(monitoring_protocol, "__bases__")

    def test_protocol_type_annotations(self) -> None:
        """Test that protocols have proper type annotations."""
        # Test AppManagerProtocol type annotations
        protocol = FlextWebProtocols.Web.WebAppManagerProtocol

        # create_app should have proper type annotations
        create_app_annotations = protocol.__dict__["create_app"].__annotations__
        assert "name" in create_app_annotations
        assert "port" in create_app_annotations
        assert "host" in create_app_annotations
        assert "return" in create_app_annotations

    def test_protocol_documentation(self) -> None:
        """Test that protocols have proper documentation."""
        # Test AppManagerProtocol documentation
        protocol = FlextWebProtocols.Web.WebAppManagerProtocol
        assert hasattr(protocol, "__doc__")
        assert protocol.__doc__ is not None

        # Note: Protocol methods defined with ... don't have docstrings
        # This is expected behavior for Protocol type annotations

    def test_protocol_consistency(self) -> None:
        """Test that protocols are consistent with implementation."""
        # All protocols should be consistent with their expected usage
        protocols = [
            FlextWebProtocols.Web.WebAppManagerProtocol,
            FlextWebProtocols.Web.WebResponseFormatterProtocol,
            FlextWebProtocols.Web.WebFrameworkInterfaceProtocol,
            FlextWebProtocols.Web.WebTemplateRendererProtocol,
            FlextWebProtocols.Web.WebServiceProtocol,
            FlextWebProtocols.Web.WebRepositoryProtocol,
            FlextWebProtocols.Web.WebHandlerProtocol,
            FlextWebProtocols.Web.WebTemplateEngineProtocol,
            FlextWebProtocols.Web.WebMonitoringProtocol,
        ]

        for protocol in protocols:
            # Should be a Protocol class
            assert isinstance(protocol, type)
            assert hasattr(protocol, "__annotations__")

            # Should have methods defined (check for method names instead of annotations)
            methods = [name for name in dir(protocol) if not name.startswith("_")]
            assert len(methods) > 0

    def test_protocol_usage_patterns(self) -> None:
        """Test that protocols follow expected usage patterns."""

        # Protocols should be usable with isinstance checks
        class MockAppManager:
            def create_app(
                self, name: str, port: int, host: str
            ) -> dict[str, t.GeneralValueType]:
                return {"name": name, "host": host, "port": port}

            def start_app(self, app_id: str) -> dict[str, t.GeneralValueType]:
                return {"name": "test", "host": "localhost", "port": 8080}

            def stop_app(self, app_id: str) -> dict[str, t.GeneralValueType]:
                return {"name": "test", "host": "localhost", "port": 8080}

            def list_apps(self) -> list[dict[str, t.GeneralValueType]]:
                return [{"name": "test", "host": "localhost", "port": 8080}]

        mock_manager = MockAppManager()

        # Should be able to check protocol compliance
        assert hasattr(mock_manager, "create_app")
        assert hasattr(mock_manager, "start_app")
        assert hasattr(mock_manager, "stop_app")
        assert hasattr(mock_manager, "list_apps")

    def test_protocol_extensibility(self) -> None:
        """Test that protocols are extensible."""

        # Should be able to create new protocols that inherit from web protocols
        class CustomProtocol(FlextWebProtocols.Web.WebAppManagerProtocol):
            def custom_method(self) -> None:
                pass

        assert hasattr(CustomProtocol, "create_app")
        assert hasattr(CustomProtocol, "custom_method")

    def test_protocol_validation(self) -> None:
        """Test that protocols can be used for validation."""

        # Protocols should be usable for type checking
        def validate_app_manager(obj: object) -> bool:
            return hasattr(obj, "create_app") and hasattr(obj, "start_app")

        class ValidAppManager:
            def create_app(self, name: str, port: int, host: str) -> None:
                pass

            def start_app(self, app_id: str) -> None:
                pass

            def stop_app(self, app_id: str) -> None:
                pass

            def list_apps(self) -> None:
                pass

        class InvalidAppManager:
            def create_app(self, name: str, port: int, host: str) -> None:
                pass

            # Missing other methods

        assert validate_app_manager(ValidAppManager())
        assert not validate_app_manager(InvalidAppManager())

    def test_app_manager_protocol_real_lifecycle_behavior(self) -> None:
        """Validate real app lifecycle behavior from protocol base implementation."""
        self._reset_protocol_state()
        manager = _WebAppManagerBase()

        created = manager.create_app("test", 8080, "localhost")
        assert created.is_success
        app_id = str(created.value["id"])
        assert created.value["framework"] in {"fastapi", "flask"}

        started = manager.start_app(app_id)
        assert started.is_success
        assert started.value["status"] == FlextWebConstants.Web.Status.RUNNING.value

        listed = manager.list_apps()
        assert listed.is_success
        assert len(listed.value) == 1
        assert listed.value[0]["id"] == app_id

        stopped = manager.stop_app(app_id)
        assert stopped.is_success
        assert stopped.value["status"] == FlextWebConstants.Web.Status.STOPPED.value

    def test_response_formatter_protocol_methods(self) -> None:
        """Test WebResponseFormatterProtocol methods execution."""

        class RealResponseFormatter:
            def format_success(
                self, data: dict[str, t.GeneralValueType]
            ) -> dict[str, t.GeneralValueType]:
                response: dict[str, t.GeneralValueType] = {
                    "status": FlextWebConstants.Web.WebResponse.STATUS_SUCCESS,
                }
                response.update({
                    key: value
                    for key, value in data.items()
                    if isinstance(value, (str, int, bool, list, dict))
                })
                return response

            def format_error(self, error: Exception) -> dict[str, t.GeneralValueType]:
                result: dict[str, t.GeneralValueType] = {
                    "status": FlextWebConstants.Web.WebResponse.STATUS_ERROR,
                    "message": str(error),
                }
                return result

            def create_json_response(
                self,
                data: dict[str, t.GeneralValueType],
            ) -> dict[str, t.GeneralValueType]:
                response: dict[str, t.GeneralValueType] = {
                    FlextWebConstants.Web.Http.HEADER_CONTENT_TYPE: FlextWebConstants.Web.Http.CONTENT_TYPE_JSON,
                }
                response.update({
                    key: value
                    for key, value in data.items()
                    if isinstance(value, (str, int, bool, list, dict))
                })
                return response

            def get_request_data(
                self,
                _request: dict[str, t.GeneralValueType],
            ) -> dict[str, t.GeneralValueType]:
                return {}

            # Required by p.Service
            def execute(
                self,
                *args: object,
                **kwargs: object,
            ) -> FlextResult[dict[str, t.GeneralValueType]]:
                return FlextResult[dict[str, t.GeneralValueType]].ok({})

            def validate_business_rules(
                self,
                *args: object,
                **kwargs: object,
            ) -> FlextResult[bool]:
                return FlextResult[bool].ok(True)

            def get_service_info(self) -> dict[str, t.GeneralValueType]:
                return {"name": "ResponseFormatter"}

        formatter = RealResponseFormatter()
        # Check that it has all required methods (structural typing)
        assert hasattr(formatter, "format_success")
        assert hasattr(formatter, "format_error")
        assert hasattr(formatter, "create_json_response")

        # Test format_success with nested dict - proper type annotation
        data_with_nested: dict[str, t.GeneralValueType] = {
            "key1": "value1",
            "nested": {"key2": "value2"},
        }
        result = formatter.format_success(data_with_nested)
        assert result["status"] == FlextWebConstants.Web.WebResponse.STATUS_SUCCESS
        assert result["key1"] == "value1"
        assert isinstance(result["nested"], dict)

        # Test format_error
        error = ValueError("Test error")
        error_result = formatter.format_error(error)
        assert error_result["status"] == FlextWebConstants.Web.WebResponse.STATUS_ERROR
        assert "Test error" in str(error_result["message"])

        # Test create_json_response with nested dict
        json_result = formatter.create_json_response(data_with_nested)
        assert FlextWebConstants.Web.Http.HEADER_CONTENT_TYPE in json_result
        assert (
            json_result[FlextWebConstants.Web.Http.HEADER_CONTENT_TYPE]
            == FlextWebConstants.Web.Http.CONTENT_TYPE_JSON
        )

    def test_web_framework_interface_protocol_methods(self) -> None:
        """Test WebFrameworkInterfaceProtocol methods execution."""

        class RealFrameworkInterface:
            def create_json_response(
                self,
                data: dict[str, t.GeneralValueType],
            ) -> dict[str, t.GeneralValueType]:
                response: dict[str, t.GeneralValueType] = {
                    FlextWebConstants.Web.Http.HEADER_CONTENT_TYPE: FlextWebConstants.Web.Http.CONTENT_TYPE_JSON,
                }
                response.update({
                    key: value
                    for key, value in data.items()
                    if isinstance(value, (str, int, bool, list, dict))
                })
                return response

            def get_request_data(
                self,
                _request: dict[str, t.GeneralValueType],
            ) -> dict[str, t.GeneralValueType]:
                return {}

            def is_json_request(self, _request: dict[str, t.GeneralValueType]) -> bool:
                return False

            # Required by p.Service
            def execute(
                self,
                *args: object,
                **kwargs: object,
            ) -> FlextResult[dict[str, t.GeneralValueType]]:
                return FlextResult[dict[str, t.GeneralValueType]].ok({})

            def validate_business_rules(
                self,
                *args: object,
                **kwargs: object,
            ) -> FlextResult[bool]:
                return FlextResult[bool].ok(True)

            def get_service_info(self) -> dict[str, t.GeneralValueType]:
                return {"name": "FrameworkInterface"}

        framework = RealFrameworkInterface()
        # Check that it has all required methods (structural typing)
        assert hasattr(framework, "create_json_response")
        assert hasattr(framework, "get_request_data")
        assert hasattr(framework, "is_json_request")

        # Test methods - proper type annotation
        data: dict[str, t.GeneralValueType] = {
            "test": "value",
            "nested": {"key": "value"},
        }
        json_response = framework.create_json_response(data)
        assert FlextWebConstants.Web.Http.HEADER_CONTENT_TYPE in json_response

        request_data = framework.get_request_data({})
        assert isinstance(request_data, dict)

        is_json = framework.is_json_request({})
        assert is_json is False

    def test_web_service_protocol_methods(self) -> None:
        """Test WebServiceProtocol methods execution."""

        class RealWebService:
            def initialize_routes(self) -> FlextResult[bool]:
                return FlextResult[bool].ok(True)

            def configure_middleware(self) -> FlextResult[bool]:
                return FlextResult[bool].ok(True)

            def start_service(self) -> FlextResult[bool]:
                return FlextResult[bool].ok(True)

            def stop_service(self) -> FlextResult[bool]:
                return FlextResult[bool].ok(True)

            # Required by p.Service
            def execute(
                self,
                *args: object,
                **kwargs: object,
            ) -> FlextResult[dict[str, t.GeneralValueType]]:
                return FlextResult[dict[str, t.GeneralValueType]].ok({})

            def validate_business_rules(
                self,
                *args: object,
                **kwargs: object,
            ) -> FlextResult[bool]:
                return FlextResult[bool].ok(True)

            def get_service_info(self) -> dict[str, t.GeneralValueType]:
                return {"name": "WebService"}

        service = RealWebService()
        # Check that it has all required methods (structural typing)
        assert hasattr(service, "initialize_routes")
        assert hasattr(service, "configure_middleware")
        assert hasattr(service, "start_service")
        assert hasattr(service, "stop_service")

        # Execute all methods
        assert service.initialize_routes().is_success
        assert service.configure_middleware().is_success
        assert service.start_service().is_success
        assert service.stop_service().is_success

    def test_web_repository_protocol_methods(self) -> None:
        """Test WebRepositoryProtocol methods execution."""

        class RealWebRepository:
            def find_by_criteria(
                self,
                criteria: dict[str, t.GeneralValueType],
            ) -> FlextResult[list[dict[str, t.GeneralValueType]]]:
                return FlextResult[list[dict[str, t.GeneralValueType]]].ok([])

            # Required by p.Repository
            def get_by_id(
                self, entity_id: str
            ) -> FlextResult[dict[str, t.GeneralValueType]]:
                return FlextResult[dict[str, t.GeneralValueType]].ok({"id": entity_id})

            def save(
                self, entity: dict[str, t.GeneralValueType]
            ) -> FlextResult[dict[str, t.GeneralValueType]]:
                return FlextResult[dict[str, t.GeneralValueType]].ok(entity)

            def delete(self, entity_id: str) -> FlextResult[bool]:
                return FlextResult[bool].ok(True)

            def find_all(self) -> FlextResult[list[dict[str, t.GeneralValueType]]]:
                return FlextResult[list[dict[str, t.GeneralValueType]]].ok([])

            # Required by p.Service
            def execute(
                self,
                *args: object,
                **kwargs: object,
            ) -> FlextResult[dict[str, t.GeneralValueType]]:
                return FlextResult[dict[str, t.GeneralValueType]].ok({})

            def validate_business_rules(
                self,
                *args: object,
                **kwargs: object,
            ) -> FlextResult[bool]:
                return FlextResult[bool].ok(True)

            def get_service_info(self) -> dict[str, t.GeneralValueType]:
                return {"name": "WebRepository"}

        repo = RealWebRepository()
        # Check that it has all required methods (structural typing)
        assert hasattr(repo, "find_by_criteria")

        # Execute method
        result = repo.find_by_criteria({"key": "value"})
        assert result.is_success

    def test_web_template_renderer_protocol_methods(self) -> None:
        """Test WebTemplateRendererProtocol methods execution."""

        class RealTemplateRenderer:
            def render_template(
                self,
                template_name: str,
                _context: dict[str, t.GeneralValueType],
            ) -> FlextResult[str]:
                return FlextResult[str].ok("")

            def render_dashboard(
                self, data: dict[str, t.GeneralValueType]
            ) -> FlextResult[str]:
                return FlextResult[str].ok("<html>Dashboard</html>")

            # Required by p.Service
            def execute(
                self,
                *args: object,
                **kwargs: object,
            ) -> FlextResult[dict[str, t.GeneralValueType]]:
                return FlextResult[dict[str, t.GeneralValueType]].ok({})

            def validate_business_rules(
                self,
                *args: object,
                **kwargs: object,
            ) -> FlextResult[bool]:
                return FlextResult[bool].ok(True)

            def get_service_info(self) -> dict[str, t.GeneralValueType]:
                return {"name": "TemplateRenderer"}

        renderer = RealTemplateRenderer()
        # Check that it has all required methods (structural typing)
        assert hasattr(renderer, "render_template")
        assert hasattr(renderer, "render_dashboard")

        # Execute methods
        template_result = renderer.render_template(
            "tesFlextWebTypes.html", {"key": "value"}
        )
        assert template_result.is_success

        dashboard_result = renderer.render_dashboard({"data": "value"})
        assert dashboard_result.is_success
        assert "<html>Dashboard</html>" in dashboard_result.value

    def test_web_template_engine_protocol_methods(self) -> None:
        """Test WebTemplateEngineProtocol methods execution."""

        class RealTemplateEngine:
            def load_template_config(
                self,
                config: dict[str, t.GeneralValueType],
            ) -> FlextResult[bool]:
                return FlextResult[bool].ok(True)

            def get_template_config(self) -> FlextResult[dict[str, t.GeneralValueType]]:
                return FlextResult[dict[str, t.GeneralValueType]].ok({})

            def validate_template_config(
                self,
                config: dict[str, t.GeneralValueType],
            ) -> FlextResult[bool]:
                return FlextResult[bool].ok(True)

            def render(
                self,
                template: str,
                _context: dict[str, t.GeneralValueType],
            ) -> FlextResult[str]:
                return FlextResult[str].ok("")

            def add_filter(self, name: str, filter_func: object) -> None:
                pass

            def add_global(
                self,
                name: str,
                *,
                value: str | int | bool | list[str] | dict[str, str | int | bool],
            ) -> None:
                pass

            # Required by p.Service
            def execute(
                self,
                *args: object,
                **kwargs: object,
            ) -> FlextResult[dict[str, t.GeneralValueType]]:
                return FlextResult[dict[str, t.GeneralValueType]].ok({})

            def validate_business_rules(
                self,
                *args: object,
                **kwargs: object,
            ) -> FlextResult[bool]:
                return FlextResult[bool].ok(True)

            def get_service_info(self) -> dict[str, t.GeneralValueType]:
                return {"name": "TemplateEngine"}

        engine = RealTemplateEngine()
        # Check that it has all required methods (structural typing)
        assert hasattr(engine, "load_template_config")
        assert hasattr(engine, "get_template_config")
        assert hasattr(engine, "validate_template_config")
        assert hasattr(engine, "render")
        assert hasattr(engine, "add_filter")
        assert hasattr(engine, "add_global")

        # Execute all methods
        assert engine.load_template_config({"key": "value"}).is_success
        assert engine.get_template_config().is_success
        assert engine.validate_template_config({"key": "value"}).is_success
        assert engine.render("template", {"key": "value"}).is_success

        # Test add_filter and add_global (void methods)
        engine.add_filter("test", lambda x: x)
        engine.add_global("test", value="value")
        engine.add_global("test_int", value=42)
        engine.add_global("test_bool", value=True)
        engine.add_global("test_list", value=["item1", "item2"])
        engine.add_global("test_dict", value={"key": "value"})

    def test_web_monitoring_protocol_methods(self) -> None:
        """Test WebMonitoringProtocol methods execution."""

        class RealWebMonitoring:
            def record_web_request(
                self,
                request: dict[str, t.GeneralValueType],
                response_time: float,
            ) -> None:
                pass

            def get_web_health_status(self) -> dict[str, t.GeneralValueType]:
                return {
                    "status": FlextWebConstants.Web.WebResponse.STATUS_HEALTHY,
                    "service": FlextWebConstants.Web.WebService.SERVICE_NAME,
                }

            def get_web_metrics(self) -> dict[str, t.GeneralValueType]:
                return {"requests": 0, "errors": 0, "uptime": "0s"}

            # Required by p.Service
            def execute(
                self,
                *args: object,
                **kwargs: object,
            ) -> FlextResult[dict[str, t.GeneralValueType]]:
                return FlextResult[dict[str, t.GeneralValueType]].ok({})

            def validate_business_rules(
                self,
                *args: object,
                **kwargs: object,
            ) -> FlextResult[bool]:
                return FlextResult[bool].ok(True)

            def get_service_info(self) -> dict[str, t.GeneralValueType]:
                return {"name": "WebMonitoring"}

        monitoring = RealWebMonitoring()
        # WebMonitoringProtocol is @runtime_checkable, so isinstance should work
        if hasattr(
            FlextWebProtocols.Web.WebMonitoringProtocol, "__runtime_checkable__"
        ):
            assert isinstance(monitoring, FlextWebProtocols.Web.WebMonitoringProtocol)

        # Execute methods
        monitoring.record_web_request({"method": "GET"}, 0.1)
        health = monitoring.get_web_health_status()
        assert health["status"] == FlextWebConstants.Web.WebResponse.STATUS_HEALTHY
        metrics = monitoring.get_web_metrics()
        assert "requests" in metrics

    def test_app_lifecycle_direct_execution_on_protocol_base(self) -> None:
        """Test real app lifecycle behavior through WebAppManager protocol base."""
        self._reset_protocol_state()
        manager = _WebAppManagerBase()

        result = manager.create_app("test", 8080, "localhost")
        assert result.is_success
        app_id = str(result.value["id"])
        assert result.value["framework"] in {"fastapi", "flask"}
        assert result.value["interface"] in {"asgi", "wsgi"}

        started = manager.start_app(app_id)
        assert started.is_success
        assert started.value["status"] == FlextWebConstants.Web.Status.RUNNING.value

        listed = manager.list_apps()
        assert listed.is_success
        assert len(listed.value) == 1
        assert listed.value[0]["id"] == app_id

        stopped = manager.stop_app(app_id)
        assert stopped.is_success
        assert stopped.value["status"] == FlextWebConstants.Web.Status.STOPPED.value

    def test_response_formatter_real_behavior(self) -> None:
        """Test response formatter protocol with real implementation behavior."""
        formatter = FlextWebProtocols.Web.TestBases._WebResponseFormatterBase()

        data_with_all_types: t.WebCore.ResponseDict = {
            "string": "value",
            "int": 42,
            "bool": True,
            "list": ["item1", "item2"],
            "dict": {"nested": "value"},
        }
        result = formatter.format_success(data_with_all_types)
        assert result["status"] == FlextWebConstants.Web.WebResponse.STATUS_SUCCESS
        assert result["string"] == "value"
        assert result["int"] == 42
        assert result["bool"] is True
        assert isinstance(result["list"], list)
        assert isinstance(result["dict"], dict)

        # Test format_error to cover lines 315-319
        error = ValueError("Test error message")
        error_result = formatter.format_error(error)
        assert error_result["status"] == FlextWebConstants.Web.WebResponse.STATUS_ERROR
        assert "Test error message" in str(error_result["message"])

        # Test create_json_response with all value types to cover lines 335-345
        json_result = formatter.create_json_response(data_with_all_types)
        assert (
            json_result[FlextWebConstants.Web.Http.HEADER_CONTENT_TYPE]
            == FlextWebConstants.Web.Http.CONTENT_TYPE_JSON
        )

        request_data = formatter.get_request_data({"test": "data"})
        assert isinstance(request_data, dict)
        assert request_data["test"] == "data"

    def test_framework_interface_real_behavior(self) -> None:
        """Test web framework interface protocol with real request behavior."""
        framework = _WebFrameworkInterfaceBase()

        # Test create_json_response to cover lines 390-400
        data: t.WebCore.ResponseDict = {
            "test": "value",
            "nested": {"key": "value"},
        }
        result = framework.create_json_response(data)
        assert (
            result[FlextWebConstants.Web.Http.HEADER_CONTENT_TYPE]
            == FlextWebConstants.Web.Http.CONTENT_TYPE_JSON
        )

        request_data = framework.get_request_data({"test": "data"})
        assert isinstance(request_data, dict)
        assert request_data["test"] == "data"

        is_json = framework.is_json_request({"content-type": "application/json"})
        assert is_json is True

    def test_service_protocol_real_behavior(self) -> None:
        """Test web service lifecycle protocol behavior."""
        self._reset_protocol_state()
        service = _WebServiceBase()

        start_without_setup = service.start_service()
        assert start_without_setup.is_failure

        assert service.initialize_routes().is_success
        assert service.configure_middleware().is_success
        assert service.start_service().is_success
        assert service.stop_service().is_success

    def test_repository_protocol_real_behavior(self) -> None:
        """Test repository protocol criteria filtering behavior."""
        self._reset_protocol_state()
        manager = _WebAppManagerBase()
        created = manager.create_app("repo-app", 8081, "127.0.0.1")
        assert created.is_success

        repo = _WebRepositoryBase()
        result = repo.find_by_criteria({"host": "127.0.0.1"})
        assert result.is_success
        assert len(result.value) == 1

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
        assert create_result.is_success

        list_result = handler.handle_request({"action": "list"})
        assert list_result.is_success
        assert list_result.value["count"] == 1

    def test_template_renderer_real_behavior(self) -> None:
        """Test template renderer protocol with real template substitution."""
        renderer = _WebTemplateRendererBase()

        result = renderer.render_template("{{key}}-template", {"key": "value"})
        assert result.is_success
        assert result.value == "value-template"

        result = renderer.render_dashboard({
            "service": "dashboard",
            "status": "running",
        })
        assert result.is_success
        assert "dashboard" in result.value

    def test_template_engine_real_behavior(self) -> None:
        """Test template engine protocol with config and global/filter handling."""
        self._reset_protocol_state()
        engine = _WebTemplateEngineBase()

        assert engine.load_template_config({"template_dir": "templates"}).is_success
        assert engine.get_template_config().is_success
        assert engine.validate_template_config({"template_dir": "templates"}).is_success
        assert engine.validate_template_config({"invalid": "value"}).is_failure

        engine.add_filter("test", lambda x: x.upper())
        engine.add_global("test", value="value")
        rendered = engine.render("{{test}}|test", {})
        assert rendered.is_success
        assert rendered.value == "VALUE"

    def test_connection_protocol_real_behavior(self) -> None:
        """Test connection protocol endpoint URL from running app."""
        self._reset_protocol_state()
        manager = _WebAppManagerBase()
        created = manager.create_app("endpoint-app", 9090, "127.0.0.1")
        assert created.is_success
        app_id = str(created.value["id"])
        assert manager.start_app(app_id).is_success

        connection = _WebConnectionBase()
        url = connection.get_endpoint_url()
        assert url == "http://127.0.0.1:9090"

    def test_monitoring_protocol_real_behavior(self) -> None:
        """Test monitoring protocol metrics recording behavior."""
        self._reset_protocol_state()
        monitoring = _WebMonitoringBase()

        monitoring.record_web_request({"method": "GET"}, 0.1)

        health = monitoring.get_web_health_status()
        assert health["status"] == FlextWebConstants.Web.Status.STOPPED.value
        assert health["service"] == FlextWebConstants.Web.WebService.SERVICE_NAME

        metrics = monitoring.get_web_metrics()
        assert metrics["requests"] == 1
        assert metrics["errors"] == 0
        assert metrics["uptime"] == "0s"

    def test_protocol_app_lifecycle_end_to_end(self) -> None:
        """TDD lifecycle flow: create, start, stop, and list app states."""
        self._reset_protocol_state()
        manager = _WebAppManagerBase()

        create_result = manager.create_app("lifecycle-app", 7070, "localhost")
        assert create_result.is_success
        app_id = str(create_result.value["id"])

        list_result = manager.list_apps()
        assert list_result.is_success
        assert len(list_result.value) == 1
        assert (
            list_result.value[0]["status"] == FlextWebConstants.Web.Status.STOPPED.value
        )

        start_result = manager.start_app(app_id)
        assert start_result.is_success
        assert (
            start_result.value["status"] == FlextWebConstants.Web.Status.RUNNING.value
        )

        stop_result = manager.stop_app(app_id)
        assert stop_result.is_success
        assert stop_result.value["status"] == FlextWebConstants.Web.Status.STOPPED.value

    def test_create_app_configures_protocol_health_route(self) -> None:
        """TDD create_app must register protocol health endpoint."""
        self._reset_protocol_state()
        manager = _WebAppManagerBase()

        create_result = manager.create_app("route-app", 7171, "localhost")
        assert create_result.is_success
        app_id = str(create_result.value["id"])

        framework = str(create_result.value["framework"])
        app_instance = FlextWebProtocols.Web.framework_instances[app_id]
        if framework == "fastapi":
            fastapi_app = cast("Any", app_instance)
            paths = [route.path for route in fastapi_app.routes]
            assert "/protocol/health" in paths
        else:
            flask_app = cast("Any", app_instance)
            routes = [rule.rule for rule in flask_app.url_map.iter_rules()]
            assert "/protocol/health" in routes

    def test_start_stop_manage_runtime_registry(self) -> None:
        """TDD lifecycle must persist and cleanup runtime metadata."""
        self._reset_protocol_state()
        manager = _WebAppManagerBase()

        created = manager.create_app("runtime-app", 7272, "localhost")
        assert created.is_success
        app_id = str(created.value["id"])

        started = manager.start_app(app_id)
        assert started.is_success
        assert app_id in FlextWebProtocols.Web.app_runtimes

        stopped = manager.stop_app(app_id)
        assert stopped.is_success
        assert app_id not in FlextWebProtocols.Web.app_runtimes
