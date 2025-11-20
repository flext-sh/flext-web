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
        """Test protocol implementation - REAL execution."""
        handler = FlextWebHandlers.ApplicationHandler()

        # Test WebAppManagerProtocol methods - REAL execution
        result = handler.create_app("test", 8080, "localhost")
        assert result.is_success

        result = handler.list_apps()
        assert result.is_success

    def test_application_handler_create_validation_errors(self) -> None:
        """Test ApplicationHandler.create with validation errors - REAL validation."""
        handler = FlextWebHandlers.ApplicationHandler()

        # Test invalid name type
        result = handler.create(123, 8080, "localhost")
        assert result.is_failure
        assert "must be a string" in result.error

        # Test name too short
        result = handler.create("ab", 8080, "localhost")
        assert result.is_failure
        assert "at least" in result.error

        # Test invalid host type
        result = handler.create("test-app", 8080, 123)
        assert result.is_failure
        assert "must be a string" in result.error

        # Test empty host
        result = handler.create("test-app", 8080, "")
        assert result.is_failure
        assert "cannot be empty" in result.error

        # Test invalid port type
        result = handler.create("test-app", "8080", "localhost")
        assert result.is_failure
        assert "must be an integer" in result.error

        # Test port too low
        result = handler.create("test-app", 0, "localhost")
        assert result.is_failure
        assert "at least" in result.error

        # Test port too high
        result = handler.create("test-app", 70000, "localhost")
        assert result.is_failure
        assert "at most" in result.error

    def test_application_handler_start_app_not_found(self) -> None:
        """Test ApplicationHandler.start_app with non-existent app - REAL validation."""
        handler = FlextWebHandlers.ApplicationHandler()

        result = handler.start_app("nonexistent-id")
        assert result.is_failure
        assert "not found" in result.error

    def test_application_handler_stop_app_not_found(self) -> None:
        """Test ApplicationHandler.stop_app with non-existent app - REAL validation."""
        handler = FlextWebHandlers.ApplicationHandler()

        result = handler.stop_app("nonexistent-id")
        assert result.is_failure
        assert "not found" in result.error

    def test_application_handler_start_stop_cycle(self) -> None:
        """Test ApplicationHandler start/stop cycle - REAL execution."""
        handler = FlextWebHandlers.ApplicationHandler()

        # Create app
        create_result = handler.create("test-app", 8080, "localhost")
        assert create_result.is_success
        app = create_result.unwrap()
        app_id = app.id

        # Start app
        start_result = handler.start_app(app_id)
        assert start_result.is_success
        started_app = start_result.unwrap()
        assert started_app.status == "running"

        # Stop app
        stop_result = handler.stop_app(app_id)
        assert stop_result.is_success
        stopped_app = stop_result.unwrap()
        assert stopped_app.status == "stopped"

    def test_handle_start_app_invalid_type(self) -> None:
        """Test handle_start_app with invalid entity type - REAL validation."""
        # Pass non-Entity object
        result = FlextWebHandlers.handle_start_app("not-an-entity")
        assert result.is_failure
        assert "Invalid application entity type" in result.error

    def test_handle_stop_app_invalid_type(self) -> None:
        """Test handle_stop_app with invalid entity type - REAL validation."""
        # Pass non-Entity object
        result = FlextWebHandlers.handle_stop_app("not-an-entity")
        assert result.is_failure
        assert "Invalid application entity type" in result.error

    def test_handlers_execute(self) -> None:
        """Test FlextWebHandlers.execute - REAL execution."""
        handlers = FlextWebHandlers()
        result = handlers.execute()
        assert result.is_success
        assert result.unwrap() is True

    def test_handlers_validate_business_rules(self) -> None:
        """Test FlextWebHandlers.validate_business_rules - REAL execution."""
        handlers = FlextWebHandlers()
        result = handlers.validate_business_rules()
        assert result.is_success
        assert result.unwrap() is True
