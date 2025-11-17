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

    def test_error_handling_with_flext_result(self) -> None:
        """Test error handling using FlextResult directly - no helpers."""
        from flext_core import FlextResult

        # Test that errors are handled using FlextResult.fail() directly
        error = ValueError("Invalid input")
        result = FlextResult[str].fail(f"Validation error: {error}")
        assert result.is_failure
        assert result.error is not None and "Validation error" in result.error

    def test_processing_error_with_flext_result(self) -> None:
        """Test processing error handling using FlextResult directly."""
        from flext_core import FlextResult

        # Test that errors are handled using FlextResult.fail() directly
        error = RuntimeError("Processing failed")
        result = FlextResult[str].fail(f"Operation failed: {error}")
        assert result.is_failure
        assert result.error is not None and "Operation failed" in result.error

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
