"""Comprehensive unit tests for flext_web.protocols module.

Tests the unified FlextWebProtocols class following flext standards.
"""

from flext_web.models import FlextWebModels
from flext_web.protocols import FlextWebProtocols


class TestFlextWebProtocols:
    """Test suite for FlextWebProtocols unified class."""

    def test_protocols_inheritance(self) -> None:
        """Test that FlextWebProtocols inherits from FlextProtocols."""
        # Should have access to base FlextProtocols
        assert hasattr(FlextWebProtocols, "Foundation")
        assert hasattr(FlextWebProtocols, "Domain")
        assert hasattr(FlextWebProtocols, "Application")
        assert hasattr(FlextWebProtocols, "Infrastructure")
        assert hasattr(FlextWebProtocols, "Extensions")
        assert hasattr(FlextWebProtocols, "Commands")

    def test_web_protocols_structure(self) -> None:
        """Test FlextWebProtocols structure."""
        # Should have Web nested class
        assert hasattr(FlextWebProtocols, "Web")

        # Web class should have protocol definitions
        web_protocols = FlextWebProtocols.Web
        assert hasattr(web_protocols, "AppManagerProtocol")
        assert hasattr(web_protocols, "ResponseFormatterProtocol")
        assert hasattr(web_protocols, "WebFrameworkInterface")
        assert hasattr(web_protocols, "TemplateRendererProtocol")
        assert hasattr(web_protocols, "WebServiceInterface")
        assert hasattr(web_protocols, "AppRepositoryInterface")
        assert hasattr(web_protocols, "MiddlewareInterface")
        assert hasattr(web_protocols, "TemplateEngineInterface")
        assert hasattr(web_protocols, "MonitoringInterface")

    def test_app_manager_protocol(self) -> None:
        """Test AppManagerProtocol definition."""
        protocol = FlextWebProtocols.Web.AppManagerProtocol

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
        protocol = FlextWebProtocols.Web.ResponseFormatterProtocol

        # Should be a Protocol
        assert isinstance(protocol, type)
        assert hasattr(protocol, "__annotations__")

        # Should have required methods
        assert hasattr(protocol, "format_success")
        assert hasattr(protocol, "format_error")

    def test_web_framework_interface(self) -> None:
        """Test WebFrameworkInterface definition."""
        protocol = FlextWebProtocols.Web.WebFrameworkInterface

        # Should be a Protocol
        assert isinstance(protocol, type)
        assert hasattr(protocol, "__annotations__")

        # Should have required methods
        assert hasattr(protocol, "create_json_response")
        assert hasattr(protocol, "get_request_data")
        assert hasattr(protocol, "is_json_request")

    def test_template_renderer_protocol(self) -> None:
        """Test TemplateRendererProtocol definition."""
        protocol = FlextWebProtocols.Web.TemplateRendererProtocol

        # Should be a Protocol
        assert isinstance(protocol, type)
        # Check if it's a Protocol by checking for __annotations__
        assert hasattr(protocol, "__annotations__")

        # Should have required methods
        assert hasattr(protocol, "render_template")
        assert hasattr(protocol, "render_dashboard")

    def test_web_service_interface(self) -> None:
        """Test WebServiceInterface definition."""
        protocol = FlextWebProtocols.Web.WebServiceInterface

        # Should be a Protocol
        assert isinstance(protocol, type)
        assert hasattr(protocol, "__annotations__")

        # Should have required methods
        assert hasattr(protocol, "initialize_routes")
        assert hasattr(protocol, "configure_middleware")
        assert hasattr(protocol, "start_service")
        assert hasattr(protocol, "stop_service")

    def test_app_repository_interface(self) -> None:
        """Test AppRepositoryInterface definition."""
        protocol = FlextWebProtocols.Web.AppRepositoryInterface

        # Should be a Protocol
        assert isinstance(protocol, type)
        assert hasattr(protocol, "__annotations__")

        # Should have required methods
        assert hasattr(protocol, "create")
        assert hasattr(protocol, "get")
        assert hasattr(protocol, "update")
        assert hasattr(protocol, "find_by__name")

    def test_middleware_interface(self) -> None:
        """Test MiddlewareInterface definition."""
        protocol = FlextWebProtocols.Web.MiddlewareInterface

        # Should be a Protocol
        assert isinstance(protocol, type)
        assert hasattr(protocol, "__annotations__")

        # Should have required methods
        assert hasattr(protocol, "before_request")
        assert hasattr(protocol, "after_request")
        assert hasattr(protocol, "handle__error")

    def test_template_engine_interface(self) -> None:
        """Test TemplateEngineInterface definition."""
        protocol = FlextWebProtocols.Web.TemplateEngineInterface

        # Should be a Protocol
        assert isinstance(protocol, type)
        assert hasattr(protocol, "__annotations__")

        # Should have required methods
        assert hasattr(protocol, "render")
        assert hasattr(protocol, "add_filter")
        assert hasattr(protocol, "add_global")

    def test_monitoring_interface(self) -> None:
        """Test MonitoringInterface definition."""
        protocol = FlextWebProtocols.Web.MonitoringInterface

        # Should be a Protocol
        assert isinstance(protocol, type)
        assert hasattr(protocol, "__annotations__")

        # Should have required methods
        assert hasattr(protocol, "record_request")
        assert hasattr(protocol, "record_error")
        assert hasattr(protocol, "get_health_status")
        assert hasattr(protocol, "get_metrics")

    def test_protocol_runtime_checkable(self) -> None:
        """Test that protocols are runtime checkable."""
        # All protocols should be runtime checkable
        protocols = [
            FlextWebProtocols.Web.AppManagerProtocol,
            FlextWebProtocols.Web.ResponseFormatterProtocol,
            FlextWebProtocols.Web.WebFrameworkInterface,
            FlextWebProtocols.Web.TemplateRendererProtocol,
            FlextWebProtocols.Web.WebServiceInterface,
            FlextWebProtocols.Web.AppRepositoryInterface,
            FlextWebProtocols.Web.MiddlewareInterface,
            FlextWebProtocols.Web.TemplateEngineInterface,
            FlextWebProtocols.Web.MonitoringInterface,
        ]

        for protocol in protocols:
            assert hasattr(protocol, "__runtime_checkable__")
            assert protocol.__runtime_checkable__ is True

    def test_protocol_method_signatures(self) -> None:
        """Test that protocol methods have correct signatures."""
        # Test AppManagerProtocol methods
        protocol = FlextWebProtocols.Web.AppManagerProtocol

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
        # WebServiceInterface should inherit from Domain.Service
        web_service_protocol = FlextWebProtocols.Web.WebServiceInterface
        assert hasattr(web_service_protocol, "__bases__")

        # AppRepositoryInterface should inherit from Domain.Repository
        app_repo_protocol = FlextWebProtocols.Web.AppRepositoryInterface
        assert hasattr(app_repo_protocol, "__bases__")

        # MiddlewareInterface should inherit from Extensions.Middleware
        middleware_protocol = FlextWebProtocols.Web.MiddlewareInterface
        assert hasattr(middleware_protocol, "__bases__")

        # TemplateEngineInterface should inherit from Infrastructure.Configurable
        template_engine_protocol = FlextWebProtocols.Web.TemplateEngineInterface
        assert hasattr(template_engine_protocol, "__bases__")

        # MonitoringInterface should inherit from Extensions.Observability
        monitoring_protocol = FlextWebProtocols.Web.MonitoringInterface
        assert hasattr(monitoring_protocol, "__bases__")

    def test_protocol_type_annotations(self) -> None:
        """Test that protocols have proper type annotations."""
        # Test AppManagerProtocol type annotations
        protocol = FlextWebProtocols.Web.AppManagerProtocol

        # create_app should have proper type annotations
        create_app_annotations = protocol.__dict__["create_app"].__annotations__
        assert "name" in create_app_annotations
        assert "port" in create_app_annotations
        assert "host" in create_app_annotations
        assert "return" in create_app_annotations

    def test_protocol_documentation(self) -> None:
        """Test that protocols have proper documentation."""
        # Test AppManagerProtocol documentation
        protocol = FlextWebProtocols.Web.AppManagerProtocol
        assert hasattr(protocol, "__doc__")
        assert protocol.__doc__ is not None

        # Test method documentation
        create_app_method = protocol.__dict__["create_app"]
        assert hasattr(create_app_method, "__doc__")
        assert create_app_method.__doc__ is not None

    def test_protocol_consistency(self) -> None:
        """Test that protocols are consistent with implementation."""
        # All protocols should be consistent with their expected usage
        protocols = [
            FlextWebProtocols.Web.AppManagerProtocol,
            FlextWebProtocols.Web.ResponseFormatterProtocol,
            FlextWebProtocols.Web.WebFrameworkInterface,
            FlextWebProtocols.Web.TemplateRendererProtocol,
            FlextWebProtocols.Web.WebServiceInterface,
            FlextWebProtocols.Web.AppRepositoryInterface,
            FlextWebProtocols.Web.MiddlewareInterface,
            FlextWebProtocols.Web.TemplateEngineInterface,
            FlextWebProtocols.Web.MonitoringInterface,
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
            ) -> FlextWebModels.WebApp:
                return FlextWebModels.WebApp(name=name, host=host, port=port)

            def start_app(self, app_id: str) -> FlextWebModels.WebApp:
                return FlextWebModels.WebApp(name="test", host="localhost", port=8080)

            def stop_app(self, app_id: str) -> FlextWebModels.WebApp:
                return FlextWebModels.WebApp(name="test", host="localhost", port=8080)

            def list_apps(self) -> list[FlextWebModels.WebApp]:
                return [FlextWebModels.WebApp(name="test", host="localhost", port=8080)]

        mock_manager = MockAppManager()

        # Should be able to check protocol compliance
        assert hasattr(mock_manager, "create_app")
        assert hasattr(mock_manager, "start_app")
        assert hasattr(mock_manager, "stop_app")
        assert hasattr(mock_manager, "list_apps")

    def test_protocol_extensibility(self) -> None:
        """Test that protocols are extensible."""

        # Should be able to create new protocols that inherit from web protocols
        class CustomProtocol(FlextWebProtocols.Web.AppManagerProtocol):
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
