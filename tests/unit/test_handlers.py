"""Unit tests for flext_web.handlers module.

Tests the web handlers functionality following flext standards.
"""

from flext_web.handlers import FlextWebHandlers


class TestFlextWebHandlers:
    """Test suite for FlextWebHandlers class."""

    def test_web_app_handler_initialization(self) -> None:
        """Test WebAppHandler initialization."""
        handler = FlextWebHandlers.ApplicationHandler()
        assert handler is not None
        assert hasattr(handler, "logger")
        assert hasattr(handler, "_apps_registry")

    def test_web_app_handler_list_apps(self) -> None:
        """Test listing apps."""
        handler = FlextWebHandlers.ApplicationHandler()
        result = handler.list_apps()
        assert result.is_success
        apps = result.unwrap()
        assert isinstance(apps, list)

    def test_handle_health_check(self) -> None:
        """Test health check handling."""
        result = FlextWebHandlers.handle_health_check()
        assert result.is_success
        health_data = result.unwrap()
        assert "status" in health_data
        assert "service" in health_data
        assert "version" in health_data
        assert "timestamp" in health_data

    def test_handle_system_info(self) -> None:
        """Test system info handling."""
        result = FlextWebHandlers.handle_system_info()
        assert result.is_success
        system_data = result.unwrap()
        assert "service_name" in system_data
        assert "service_type" in system_data
        assert "architecture" in system_data

    def test_handle_create_app(self) -> None:
        """Test app creation handling."""
        result = FlextWebHandlers.handle_create_app("test-app", 8080, "localhost")
        assert result.is_success
        app = result.unwrap()
        assert app.name == "test-app"
        assert app.port == 8080
        assert app.host == "localhost"

    def test_handle_validation_error(self) -> None:
        """Test validation error handling."""
        error = ValueError("Invalid input")
        result = FlextWebHandlers.handle_validation_error(error, "test context")
        assert result.is_failure
        assert result.error is not None and "Test Context error" in result.error

    def test_handle_processing_error(self) -> None:
        """Test processing error handling."""
        error = RuntimeError("Processing failed")
        result = FlextWebHandlers.handle_processing_error(error, "test operation")
        assert result.is_failure
        assert result.error is not None and "Test Operation failed" in result.error

    def test_app_registry_integration(self) -> None:
        """Test app registry integration."""
        handler = FlextWebHandlers.ApplicationHandler()

        # Create an app
        create_result = handler.create_app("test-app", 8080, "localhost")
        assert create_result.is_success
        app = create_result.unwrap()

        # App should be in registry
        assert app.id in handler._apps_registry
        assert handler._apps_registry[app.id] == app

    def test_protocol_implementation(self) -> None:
        """Test protocol implementation."""
        handler = FlextWebHandlers.ApplicationHandler()

        # Test WebAppManagerProtocol methods
        result = handler.create_app("test", 8080, "localhost")
        assert result.is_success

        result = handler.list_apps()
        assert result.is_success
