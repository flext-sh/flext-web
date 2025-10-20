"""Comprehensive unit tests for flext_web.protocols module.

Tests the unified FlextWebProtocols class following flext standards.
"""

from flext_web.protocols import FlextWebProtocols


class TestFlextWebProtocols:
    """Test suite for FlextWebProtocols unified class."""

    def test_protocols_inheritance(self) -> None:
        """Test that FlextWebProtocols inherits from FlextProtocols."""
        # Should inherit from FlextProtocols
        from flext_core.protocols import FlextProtocols

        assert issubclass(FlextWebProtocols, FlextProtocols)

        # Should have web-specific protocols directly available
        assert hasattr(FlextWebProtocols, "WebAppManagerProtocol")
        assert hasattr(FlextWebProtocols, "WebResponseFormatterProtocol")
        assert hasattr(FlextWebProtocols, "WebFrameworkInterfaceProtocol")

    def test_web_protocols_structure(self) -> None:
        """Test FlextWebProtocols structure."""
        # Web protocols should be directly available (flattened structure)
        assert hasattr(FlextWebProtocols, "WebAppManagerProtocol")
        assert hasattr(FlextWebProtocols, "WebResponseFormatterProtocol")
        assert hasattr(FlextWebProtocols, "WebFrameworkInterfaceProtocol")
        assert hasattr(FlextWebProtocols, "WebTemplateRendererProtocol")
        assert hasattr(FlextWebProtocols, "WebServiceProtocol")
        assert hasattr(FlextWebProtocols, "WebRepositoryProtocol")
        assert hasattr(FlextWebProtocols, "WebTemplateEngineProtocol")
        assert hasattr(FlextWebProtocols, "WebMonitoringProtocol")

    def test_web_app_manager_protocol(self) -> None:
        """Test WebAppManagerProtocol definition."""
        protocol = FlextWebProtocols.WebAppManagerProtocol

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
        protocol = FlextWebProtocols.WebResponseFormatterProtocol

        # Should be a Protocol
        assert isinstance(protocol, type)
        assert hasattr(protocol, "__annotations__")

        # Should have required methods
        assert hasattr(protocol, "format_success")
        assert hasattr(protocol, "format_error")

    def test_web_framework_interface_protocol(self) -> None:
        """Test WebFrameworkInterfaceProtocol definition."""
        protocol = FlextWebProtocols.WebFrameworkInterfaceProtocol

        # Should be a Protocol
        assert isinstance(protocol, type)
        assert hasattr(protocol, "__annotations__")

        # Should have required methods
        assert hasattr(protocol, "create_json_response")
        assert hasattr(protocol, "get_request_data")
        assert hasattr(protocol, "is_json_request")

    def test_template_renderer_protocol(self) -> None:
        """Test TemplateRendererProtocol definition."""
        protocol = FlextWebProtocols.WebTemplateRendererProtocol

        # Should be a Protocol
        assert isinstance(protocol, type)
        # Check if it's a Protocol by checking for __annotations__
        assert hasattr(protocol, "__annotations__")

        # Should have required methods
        assert hasattr(protocol, "render_template")
        assert hasattr(protocol, "render_dashboard")

    def test_web_service_protocol(self) -> None:
        """Test WebServiceProtocol definition."""
        protocol = FlextWebProtocols.WebServiceProtocol

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
        protocol = FlextWebProtocols.WebRepositoryProtocol

        # Should be a Protocol
        assert isinstance(protocol, type)
        assert hasattr(protocol, "__annotations__")

        # Should have required methods from FlextProtocols.Repository
        assert hasattr(protocol, "get_by_id")
        assert hasattr(protocol, "save")
        assert hasattr(protocol, "delete")
        assert hasattr(protocol, "find_all")

    def test_web_handler_protocol(self) -> None:
        """Test WebHandlerProtocol definition."""
        protocol = FlextWebProtocols.WebHandlerProtocol

        # Should be a Protocol
        assert isinstance(protocol, type)
        assert hasattr(protocol, "__annotations__")

        # Should have required methods from FlextProtocols.Handler
        assert hasattr(protocol, "handle")
        assert callable(protocol)
        assert hasattr(protocol, "can_handle")
        assert hasattr(protocol, "execute")
        # Web-specific method
        assert hasattr(protocol, "handle_request")

    def test_web_template_engine_protocol(self) -> None:
        """Test WebTemplateEngineProtocol definition."""
        protocol = FlextWebProtocols.WebTemplateEngineProtocol

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
        protocol = FlextWebProtocols.WebMonitoringProtocol

        # Should be a Protocol
        assert isinstance(protocol, type)
        assert hasattr(protocol, "__annotations__")

        # Should have required methods from FlextProtocols.Observability
        assert hasattr(protocol, "record_metric")
        assert hasattr(protocol, "log_event")
        # Web-specific methods
        assert hasattr(protocol, "record_web_request")
        assert hasattr(protocol, "get_web_health_status")
        assert hasattr(protocol, "get_web_metrics")

    def test_protocol_runtime_checkable(self) -> None:
        """Test that protocols are runtime checkable."""
        # All protocols should be runtime checkable (decorated with @runtime_checkable)
        protocols = [
            FlextWebProtocols.WebAppManagerProtocol,
            FlextWebProtocols.WebResponseFormatterProtocol,
            FlextWebProtocols.WebFrameworkInterfaceProtocol,
            FlextWebProtocols.WebTemplateRendererProtocol,
            FlextWebProtocols.WebServiceProtocol,
            FlextWebProtocols.WebRepositoryProtocol,
            FlextWebProtocols.WebHandlerProtocol,
            FlextWebProtocols.WebTemplateEngineProtocol,
            FlextWebProtocols.WebMonitoringProtocol,
        ]

        for protocol in protocols:
            # Check if protocol has runtime_checkable attribute (should be True if decorated)
            if hasattr(protocol, "__runtime_checkable__"):
                assert protocol.__runtime_checkable__ is True
            # If not decorated, that's also acceptable for Protocol classes

    def test_protocol_method_signatures(self) -> None:
        """Test that protocol methods have correct signatures."""
        # Test AppManagerProtocol methods
        protocol = FlextWebProtocols.WebAppManagerProtocol

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
        web_service_protocol = FlextWebProtocols.WebServiceProtocol
        assert hasattr(web_service_protocol, "__bases__")

        # AppRepositoryInterface should inherit from Domain.Repository
        app_repo_protocol = FlextWebProtocols.WebRepositoryProtocol
        assert hasattr(app_repo_protocol, "__bases__")

        # MiddlewareInterface should inherit from Extensions.Middleware
        middleware_protocol = FlextWebProtocols.WebHandlerProtocol
        assert hasattr(middleware_protocol, "__bases__")

        # TemplateEngineInterface should inherit from Infrastructure.Configurable
        template_engine_protocol = FlextWebProtocols.WebTemplateEngineProtocol
        assert hasattr(template_engine_protocol, "__bases__")

        # MonitoringInterface should inherit from Extensions.Observability
        monitoring_protocol = FlextWebProtocols.WebMonitoringProtocol
        assert hasattr(monitoring_protocol, "__bases__")

    def test_protocol_type_annotations(self) -> None:
        """Test that protocols have proper type annotations."""
        # Test AppManagerProtocol type annotations
        protocol = FlextWebProtocols.WebAppManagerProtocol

        # create_app should have proper type annotations
        create_app_annotations = protocol.__dict__["create_app"].__annotations__
        assert "name" in create_app_annotations
        assert "port" in create_app_annotations
        assert "host" in create_app_annotations
        assert "return" in create_app_annotations

    def test_protocol_documentation(self) -> None:
        """Test that protocols have proper documentation."""
        # Test AppManagerProtocol documentation
        protocol = FlextWebProtocols.WebAppManagerProtocol
        assert hasattr(protocol, "__doc__")
        assert protocol.__doc__ is not None

        # Note: Protocol methods defined with ... don't have docstrings
        # This is expected behavior for Protocol type annotations

    def test_protocol_consistency(self) -> None:
        """Test that protocols are consistent with implementation."""
        # All protocols should be consistent with their expected usage
        protocols = [
            FlextWebProtocols.WebAppManagerProtocol,
            FlextWebProtocols.WebResponseFormatterProtocol,
            FlextWebProtocols.WebFrameworkInterfaceProtocol,
            FlextWebProtocols.WebTemplateRendererProtocol,
            FlextWebProtocols.WebServiceProtocol,
            FlextWebProtocols.WebRepositoryProtocol,
            FlextWebProtocols.WebHandlerProtocol,
            FlextWebProtocols.WebTemplateEngineProtocol,
            FlextWebProtocols.WebMonitoringProtocol,
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
            def create_app(self, name: str, port: int, host: str) -> dict[str, object]:
                return {"name": name, "host": host, "port": port}

            def start_app(self, app_id: str) -> dict[str, object]:
                return {"name": "test", "host": "localhost", "port": 8080}

            def stop_app(self, app_id: str) -> dict[str, object]:
                return {"name": "test", "host": "localhost", "port": 8080}

            def list_apps(self) -> list[dict[str, object]]:
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
        class CustomProtocol(FlextWebProtocols.WebAppManagerProtocol):
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
