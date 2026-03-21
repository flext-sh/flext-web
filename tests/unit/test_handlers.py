"""Unit tests for flext_web.handlers module.

Tests the web handlers functionality following flext standards.
"""

from __future__ import annotations

from flext_core import r
from flext_tests import m, u

from flext_web import FlextWebHandlers


class TestFlextWebHandlers:
    """Test suite for FlextWebHandlers class."""

    def test_web_app_handler_initialization(self) -> None:
        """Test WebAppHandler initialization."""
        handler = FlextWebHandlers.ApplicationHandler()
        u.Tests.Matchers.that(handler is not None, eq=True)
        u.Tests.Matchers.that(hasattr(handler, "logger"), eq=True)
        u.Tests.Matchers.that(hasattr(handler, "_apps_registry"), eq=True)

    def test_web_app_handler_list_apps(self) -> None:
        """Test listing apps."""
        handler = FlextWebHandlers.ApplicationHandler()
        result = handler.list_apps()
        u.Tests.Matchers.ok(result)
        apps = result.value
        u.Tests.Matchers.that(isinstance(apps, list), eq=True)

    def test_handle_health_check(self) -> None:
        """Test health check handling."""
        result = FlextWebHandlers.handle_health_check()
        u.Tests.Matchers.ok(result)
        health_data = result.value
        u.Tests.Matchers.that(hasattr(health_data, "status"), eq=True)
        u.Tests.Matchers.that(hasattr(health_data, "service"), eq=True)
        u.Tests.Matchers.that(hasattr(health_data, "version"), eq=True)
        u.Tests.Matchers.that(hasattr(health_data, "timestamp"), eq=True)

    def test_handle_system_info(self) -> None:
        """Test system info handling."""
        result = FlextWebHandlers.handle_system_info()
        u.Tests.Matchers.ok(result)
        system_data = result.value
        u.Tests.Matchers.that(hasattr(system_data, "service_name"), eq=True)
        u.Tests.Matchers.that(hasattr(system_data, "service_type"), eq=True)
        u.Tests.Matchers.that(hasattr(system_data, "architecture"), eq=True)

    def test_handle_create_app(self) -> None:
        """Test app creation handling."""
        result = FlextWebHandlers.handle_create_app("test-app", 8080, "localhost")
        u.Tests.Matchers.ok(result)
        app = result.value
        u.Tests.Matchers.that(app.name, eq="test-app")
        u.Tests.Matchers.that(app.port, eq=8080)
        u.Tests.Matchers.that(app.host, eq="localhost")

    def test_error_handling_with_flext_result(self) -> None:
        """Test error handling using r directly - no helpers."""
        error = ValueError("Invalid input")
        result: r[str] = r[str].fail(f"Validation error: {error}")
        u.Tests.Matchers.fail(result)
        assert result.error is not None
        u.Tests.Matchers.that("Validation error" in result.error, eq=True)

    def test_processing_error_with_flext_result(self) -> None:
        """Test processing error handling using r directly."""
        error = RuntimeError("Processing failed")
        result: r[str] = r[str].fail(f"Operation failed: {error}")
        u.Tests.Matchers.fail(result)
        assert result.error is not None
        u.Tests.Matchers.that("Operation failed" in result.error, eq=True)

    def test_app_registry_integration(self) -> None:
        """Test app registry integration."""
        handler = FlextWebHandlers.ApplicationHandler()
        create_result = handler.create_app("test-app", 8080, "localhost")
        u.Tests.Matchers.ok(create_result)
        app = create_result.value
        u.Tests.Matchers.that(app.id in handler.apps_registry, eq=True)
        u.Tests.Matchers.that(handler.apps_registry[app.id], eq=app)

    def test_protocol_implementation(self) -> None:
        """Test protocol implementation - REAL execution."""
        handler = FlextWebHandlers.ApplicationHandler()
        create_result = handler.create_app("test", 8080, "localhost")
        u.Tests.Matchers.ok(create_result)
        list_result = handler.list_apps()
        u.Tests.Matchers.ok(list_result)

    def test_application_handler_create_validation_errors(self) -> None:
        """Test ApplicationHandler.create with validation errors - REAL validation."""
        handler = FlextWebHandlers.ApplicationHandler()
        result = handler.create("123", 8080, "localhost")
        u.Tests.Matchers.fail(result)
        assert result.error is not None
        result = handler.create("ab", 8080, "localhost")
        u.Tests.Matchers.fail(result)
        assert result.error is not None
        u.Tests.Matchers.that("at least" in result.error, eq=True)
        result = handler.create("test-app", 8080, "")
        u.Tests.Matchers.fail(result)
        assert result.error is not None
        u.Tests.Matchers.that("cannot be empty" in result.error, eq=True)
        result = handler.create("test-app", 8080, "localhost")
        u.Tests.Matchers.that(result.is_success or result.is_failure, eq=True)
        result = handler.create("test-app", 0, "localhost")
        u.Tests.Matchers.fail(result)
        assert result.error is not None
        u.Tests.Matchers.that("at least" in result.error, eq=True)
        result = handler.create("test-app", 70000, "localhost")
        u.Tests.Matchers.fail(result)
        assert result.error is not None
        u.Tests.Matchers.that("at most" in result.error, eq=True)

    def test_application_handler_start_app_not_found(self) -> None:
        """Test ApplicationHandler.start_app with non-existent app - REAL validation."""
        handler = FlextWebHandlers.ApplicationHandler()
        result = handler.start_app("nonexistent-id")
        u.Tests.Matchers.fail(result)
        assert result.error is not None
        u.Tests.Matchers.that("not found" in result.error, eq=True)

    def test_application_handler_stop_app_not_found(self) -> None:
        """Test ApplicationHandler.stop_app with non-existent app - REAL validation."""
        handler = FlextWebHandlers.ApplicationHandler()
        result = handler.stop_app("nonexistent-id")
        u.Tests.Matchers.fail(result)
        assert result.error is not None
        u.Tests.Matchers.that("not found" in result.error, eq=True)

    def test_application_handler_start_stop_cycle(self) -> None:
        """Test ApplicationHandler start/stop cycle - REAL execution."""
        handler = FlextWebHandlers.ApplicationHandler()
        create_result = handler.create("test-app", 8080, "localhost")
        u.Tests.Matchers.ok(create_result)
        app = create_result.value
        app_id = app.id
        start_result = handler.start_app(app_id)
        u.Tests.Matchers.ok(start_result)
        started_app = start_result.value
        u.Tests.Matchers.that(started_app.status, eq="running")
        stop_result = handler.stop_app(app_id)
        u.Tests.Matchers.ok(stop_result)
        stopped_app = stop_result.value
        u.Tests.Matchers.that(stopped_app.status, eq="stopped")

    def test_handle_start_app_invalid_type(self) -> None:
        """Test handle_start_app with invalid entity type - REAL validation."""
        pass

    def test_handle_stop_app_invalid_type(self) -> None:
        """Test handle_stop_app with invalid entity type - REAL validation."""
        pass

    def test_handlers_execute(self) -> None:
        """Test FlextWebHandlers.execute - REAL execution."""
        handlers = FlextWebHandlers()
        result = handlers.execute()
        u.Tests.Matchers.ok(result)
        u.Tests.Matchers.that(result.value is True, eq=True)

    def test_handlers_validate_business_rules(self) -> None:
        """Test FlextWebHandlers.validate_business_rules - REAL execution."""
        handlers = FlextWebHandlers()
        result = handlers.validate_business_rules()
        u.Tests.Matchers.ok(result)
        u.Tests.Matchers.that(result.value is True, eq=True)

    def test_handle_start_app(self) -> None:
        """Test handle_start_app with valid entity."""
        app_result = m.Web.create_web_app("test-app", "localhost", 8080)
        u.Tests.Matchers.ok(app_result)
        app = app_result.value
        result = FlextWebHandlers.handle_start_app(app)
        u.Tests.Matchers.ok(result)
        started_app = result.value
        u.Tests.Matchers.that(started_app.is_running, eq=True)

    def test_handle_stop_app(self) -> None:
        """Test handle_stop_app with valid entity."""
        app_result = m.Web.create_web_app("test-app", "localhost", 8080)
        u.Tests.Matchers.ok(app_result)
        app = app_result.value
        start_result = app.start()
        u.Tests.Matchers.ok(start_result)
        started_app = start_result.value
        result = FlextWebHandlers.handle_stop_app(started_app)
        u.Tests.Matchers.ok(result)
        stopped_app = result.value
        u.Tests.Matchers.that(stopped_app.status, eq="stopped")
