"""Unit tests for flext_web.handlers module.

Tests the web handlers functionality following flext standards.
"""

from flext_core import FlextConstants, FlextResult

from flext_web.handlers import FlextWebHandlers
from flext_web.models import FlextWebModels
from flext_web.typings import FlextWebTypes


class TestFlextWebHandlers:
    """Test suite for FlextWebHandlers class."""

    def test_web_app_handler_initialization(self) -> None:
        """Test WebAppHandler initialization."""
        handler = FlextWebHandlers.WebAppHandler()
        assert handler is not None
        assert hasattr(handler, "logger")
        assert hasattr(handler, "_apps_registry")

    def test_web_response_handler_initialization(self) -> None:
        """Test WebResponseHandler initialization."""
        handler = FlextWebHandlers.WebResponseHandler()
        assert handler is not None
        assert hasattr(handler, "success_status")
        assert hasattr(handler, "error_status")
        assert handler.success_status == FlextConstants.Http.HTTP_OK

    def test_web_response_handler_with_custom_status(self) -> None:
        """Test WebResponseHandler with custom status codes."""
        handler = FlextWebHandlers.WebResponseHandler(
            success_status=201, error_status=400
        )
        assert handler.success_status == 201
        assert handler.error_status == 400

    def test_web_app_handler_create_app_success(self) -> None:
        """Test successful app creation."""
        handler = FlextWebHandlers.WebAppHandler()
        result = handler.create_app("test-app", 8080, "localhost")
        assert result.is_success
        app = result.unwrap()
        assert app.name == "test-app"
        assert app.port == 8080
        assert app.host == "localhost"

    def test_web_app_handler_create_app_with_defaults(self) -> None:
        """Test app creation with default values."""
        handler = FlextWebHandlers.WebAppHandler()
        result = handler.create_app("test-app")
        assert result.is_success
        app = result.unwrap()
        assert app.name == "test-app"
        # Should use default port and host

    def test_web_app_handler_start_app_success(self) -> None:
        """Test successful app start."""
        handler = FlextWebHandlers.WebAppHandler()
        # First create an app
        create_result = handler.create_app("test-app", 8080, "localhost")
        assert create_result.is_success
        app = create_result.unwrap()

        # Then start it
        start_result = handler.start(app)
        assert start_result.is_success
        started_app = start_result.unwrap()
        assert started_app.status == FlextWebModels.WebAppStatus.RUNNING

    def test_web_app_handler_stop_app_success(self) -> None:
        """Test successful app stop."""
        handler = FlextWebHandlers.WebAppHandler()
        # First create and start an app
        create_result = handler.create_app("test-app", 8080, "localhost")
        assert create_result.is_success
        app = create_result.unwrap()

        start_result = handler.start(app)
        assert start_result.is_success
        running_app = start_result.unwrap()

        # Then stop it
        stop_result = handler.stop(running_app)
        assert stop_result.is_success
        stopped_app = stop_result.unwrap()
        assert stopped_app.status == FlextWebModels.WebAppStatus.STOPPED

    def test_web_app_handler_list_apps(self) -> None:
        """Test listing apps."""
        handler = FlextWebHandlers.WebAppHandler()
        result = handler.list_apps()
        assert result.is_success
        apps = result.unwrap()
        assert isinstance(apps, list)

    def test_web_response_handler_format_success(self) -> None:
        """Test success response formatting."""
        handler = FlextWebHandlers.WebResponseHandler()
        data = {"message": "Success", "data": {"id": 1}}
        response = handler.format_success(data, "Operation completed", 200)
        assert response is not None
        # Response should be a tuple (jsonify result, status_code)
        assert len(response) == 2

    def test_web_response_handler_format_error(self) -> None:
        """Test error response formatting."""
        handler = FlextWebHandlers.WebResponseHandler()
        response = handler.format_error("Operation failed", 500, "Internal error")
        assert response is not None
        # Response should be a tuple (jsonify result, status_code)
        assert len(response) == 2

    def test_web_response_handler_create_success_response(self) -> None:
        """Test success response creation."""
        handler = FlextWebHandlers.WebResponseHandler()
        data = {"result": "success"}
        response = handler.create_success_response(data, "Success", 200)
        assert response is not None

    def test_web_response_handler_create_error_response(self) -> None:
        """Test error response creation."""
        handler = FlextWebHandlers.WebResponseHandler()
        response = handler.create_error_response("Error occurred", 400, "Bad request")
        assert response is not None

    def test_web_response_handler_handle_result_success(self) -> None:
        """Test handling successful result."""
        handler = FlextWebHandlers.WebResponseHandler()
        result = FlextResult[str].ok("Success data")
        response = handler.handle_result(result, "Operation successful")
        assert response is not None

    def test_web_response_handler_handle_result_failure(self) -> None:
        """Test handling failed result."""
        handler = FlextWebHandlers.WebResponseHandler()
        result = FlextResult[str].fail("Error message")
        response = handler.handle_result(result, "Operation failed")
        assert response is not None

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

    def test_handle_start_app(self) -> None:
        """Test app start handling."""
        app = FlextWebModels.WebApp(
            id="test-id", name="test-app", host="localhost", port=8080
        )
        result = FlextWebHandlers.handle_start_app(app)
        assert result.is_success

    def test_handle_stop_app(self) -> None:
        """Test app stop handling."""
        app = FlextWebModels.WebApp(
            id="test-id",
            name="test-app",
            host="localhost",
            port=8080,
            status=FlextWebModels.WebAppStatus.RUNNING,
        )
        result = FlextWebHandlers.handle_stop_app(app)
        assert result.is_success

    def test_create_response_handler(self) -> None:
        """Test response handler creation."""
        handler = FlextWebHandlers.create_response_handler(201, 400)
        assert handler is not None
        assert handler.success_status == 201
        assert handler.error_status == 400

    def test_format_app_data(self) -> None:
        """Test app data formatting."""
        app = FlextWebModels.WebApp(
            id="test-id", name="test-app", host="localhost", port=8080
        )
        app_data = FlextWebHandlers.format_app_data(app)
        assert isinstance(app_data, FlextWebTypes.AppData)
        assert app_data["id"] == "test-id"
        assert app_data["name"] == "test-app"

    def test_format_health_data(self) -> None:
        """Test health data formatting."""
        health_data = FlextWebHandlers.format_health_data()
        assert isinstance(health_data, FlextWebTypes.HealthResponse)
        assert "status" in health_data
        assert "service" in health_data

    def test_handle_validation_error(self) -> None:
        """Test validation error handling."""
        error = ValueError("Invalid input")
        result = FlextWebHandlers.handle_validation_error(error, "test context")
        assert result.is_failure
        assert "Validation error" in result.error

    def test_handle_processing_error(self) -> None:
        """Test processing error handling."""
        error = RuntimeError("Processing failed")
        result = FlextWebHandlers.handle_processing_error(error, "test operation")
        assert result.is_failure
        assert "Processing failed" in result.error

    def test_app_registry_integration(self) -> None:
        """Test app registry integration."""
        handler = FlextWebHandlers.WebAppHandler()

        # Create an app
        create_result = handler.create_app("test-app", 8080, "localhost")
        assert create_result.is_success
        app = create_result.unwrap()

        # App should be in registry
        assert app.id in handler._apps_registry
        assert handler._apps_registry[app.id] == app

    def test_protocol_implementation(self) -> None:
        """Test protocol implementation."""
        handler = FlextWebHandlers.WebAppHandler()

        # Test AppManagerProtocol methods
        result = handler.create_app("test", 8080, "localhost")
        assert result.is_success

        result = handler.list_apps()
        assert result.is_success

        # Test ResponseFormatterProtocol methods
        response_handler = FlextWebHandlers.WebResponseHandler()
        data = {"test": "data"}
        response = response_handler.format_success(data)
        assert response is not None
