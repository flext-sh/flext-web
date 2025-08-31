"""Comprehensive tests for FLEXT Web Interface handler classes.

Tests all handler functionality including WebHandlers base class,
WebResponseHandler, and integration patterns to achieve complete coverage.
"""

from __future__ import annotations

from collections.abc import Generator

import pytest
from flask import Flask

from flext_web.handlers import FlextWebHandlers
from flext_web.models import FlextWebModels
from flext_web.typings import FlextWebTypes

# Extract nested classes for convenience
WebHandlers = FlextWebHandlers  # Alias for backward compatibility
WebResponseHandler = FlextWebHandlers.WebResponseHandler
FlextWebModels.WebApp = FlextWebModels.WebApp
FlextWebModels.WebAppStatus = FlextWebModels.WebAppStatus
ErrorDetails = FlextWebTypes.ErrorDetails


class TestWebHandlers:
    """Test WebHandlers base class functionality."""

    def test_web_handlers_creation(self) -> None:
        """Test WebHandlers can be created."""
        handlers = WebHandlers()
        assert isinstance(handlers, WebHandlers)

    def test_web_handlers_inheritance(self) -> None:
        """Test WebHandlers inherits from FlextHandlers."""
        handlers = WebHandlers()

        # Should inherit basic handler functionality
        assert hasattr(handlers, "__class__")
        assert "WebHandlers" in str(type(handlers))

    def test_handle_health_check(self) -> None:
        """Test health check handler."""
        result = WebHandlers.handle_health_check()
        assert result.success is True
        assert result.value is not None
        assert result.value["status"] == "healthy"
        assert result.value["service"] == "flext-web"

    def test_handle_app_creation(self) -> None:
        """Test app creation handler."""
        result = WebHandlers.handle_create_app("test-app", 8080, "localhost")
        assert result.success is True
        assert result.value is not None
        assert result.value.name == "test-app"
        assert result.value.port == 8080
        assert result.value.host == "localhost"

    def test_handle_app_start(self) -> None:
        """Test app start handler."""
        # Create an app first
        app = FlextWebModels.WebApp(
            id="app_test-app",
            name="test-app",
            host="localhost",
            port=8080,
            status=FlextWebModels.WebAppStatus.STOPPED,
        )
        result = WebHandlers.handle_start_app(app)
        assert result.success is True
        assert result.value.status == FlextWebModels.WebAppStatus.RUNNING

    def test_handle_app_stop(self) -> None:
        """Test app stop handler."""
        # Create a running app first
        app = FlextWebModels.WebApp(
            id="app_test-app",
            name="test-app",
            host="localhost",
            port=8080,
            status=FlextWebModels.WebAppStatus.RUNNING,
        )
        result = WebHandlers.handle_stop_app(app)
        assert result.success is True
        assert result.value.status == FlextWebModels.WebAppStatus.STOPPED


class TestWebResponseHandler:
    """Test WebResponseHandler functionality."""

    @pytest.fixture(autouse=True)
    def setup_flask_context(self) -> Generator[None]:
        """Setup Flask app context for all tests."""
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()
        yield
        self.app_context.pop()

    def test_response_handler_creation(self) -> None:
        """Test WebResponseHandler can be created."""
        handler = WebResponseHandler()
        assert isinstance(handler, WebResponseHandler)

    def test_create_success_response(self) -> None:
        """Test creating successful JSON responses."""
        handler = WebResponseHandler()
        response = handler.create_success_response(
            data={"id": "123"}, message="Operation successful"
        )

        # Flask response object - check status code and data
        flask_response, status_code = response  # type: ignore[misc]
        assert status_code == 200
        data = flask_response.get_json()
        assert isinstance(data, dict)
        assert data["success"] is True
        assert data["message"] == "Operation successful"
        assert data["data"] == {"id": "123"}

    def test_create_success_response_without_data(self) -> None:
        """Test creating successful response without data."""
        handler = WebResponseHandler()
        response = handler.create_success_response(message="Success")

        flask_response, status_code = response  # type: ignore[misc]
        assert status_code == 200
        data = flask_response.get_json()
        assert isinstance(data, dict)
        assert data["success"] is True
        assert data["message"] == "Success"
        assert data["data"] is None

    def test_create_error_response(self) -> None:
        """Test creating error JSON responses."""
        handler = WebResponseHandler()
        response = handler.create_error_response(
            message="Something went wrong", status_code=400
        )

        flask_response, status_code = response  # type: ignore[misc]
        assert status_code == 400
        data = flask_response.get_json()
        assert isinstance(data, dict)
        assert data["success"] is False
        assert data["message"] == "Something went wrong"

    def test_create_error_response_with_details(self) -> None:
        """Test creating error response with additional details."""
        error_details: ErrorDetails = {"code": "VALIDATION_ERROR", "field": "name"}
        handler = WebResponseHandler()
        response = handler.create_error_response(
            message="Validation failed", status_code=422, errors=error_details
        )

        flask_response, status_code = response  # type: ignore[misc]
        assert status_code == 422
        data = flask_response.get_json()
        assert isinstance(data, dict)
        assert data["success"] is False
        assert data["message"] == "Validation failed"
        assert data["errors"] == error_details

    def test_create_json_response_direct(self) -> None:
        """Test creating JSON response directly."""
        # Note: create_json_response doesn't exist in current implementation
        # This test should be updated or removed
        handler = WebResponseHandler()
        response = handler.create_success_response(
            data={"test": "value"}, message="Test message", status_code=201
        )

        flask_response, status_code = response  # type: ignore[misc]
        assert status_code == 201
        data = flask_response.get_json()
        assert isinstance(data, dict)
        assert data["success"] is True
        assert data["message"] == "Test message"
        assert data["data"] == {"test": "value"}

    def test_response_structure_consistency(self) -> None:
        """Test response structure is consistent across methods."""
        handler = WebResponseHandler()
        success_response = handler.create_success_response(
            data={"test": True}, message="Success"
        )
        error_details: ErrorDetails = {"code": "TEST"}
        error_response = handler.create_error_response(
            message="Error", status_code=400, errors=error_details
        )

        # Extract response and status code from tuple
        success_resp, _success_status = success_response  # type: ignore[misc]
        error_resp, _error_status = error_response  # type: ignore[misc]

        success_data = success_resp.get_json()
        error_data = error_resp.get_json()

        # Both responses should be dicts
        assert isinstance(success_data, dict)
        assert isinstance(error_data, dict)

        # Both should have success and message fields
        assert "success" in success_data
        assert "message" in success_data
        assert "data" in success_data
        assert "success" in error_data
        assert "message" in error_data
        assert "data" in error_data

        # Success should be boolean in both
        assert isinstance(success_data["success"], bool)
        assert isinstance(error_data["success"], bool)

    def test_response_data_types(self) -> None:
        """Test response handles different data types."""
        data_types = [
            None,
            "",
            "string",
            123,
            [],
            {},
            {"nested": {"data": "value"}},
            [1, 2, 3],
        ]

        for data in data_types:
            handler = WebResponseHandler()
            response = handler.create_success_response(data=data, message="Test")
            flask_response, _status = response  # type: ignore[misc]
            response_data = flask_response.get_json()
            assert response_data["data"] == data
            assert response_data["success"] is True

    def test_error_response_defaults(self) -> None:
        """Test error response default values."""
        handler = WebResponseHandler()
        response = handler.create_error_response(message="Error message")

        # Should default to status code 500
        flask_response, status_code = response  # type: ignore[misc]
        assert status_code == 500
        data = flask_response.get_json()
        assert data["success"] is False
        assert data["message"] == "Error message"

    def test_success_response_defaults(self) -> None:
        """Test success response default values."""
        handler = WebResponseHandler()
        response = handler.create_success_response(message="Success message")

        # Should default to status code 200
        # Response is a tuple (response, status_code)
        response_obj, status_code = response  # type: ignore[misc]
        assert status_code == 200
        data = response_obj.get_json()
        assert data["success"] is True
        assert data["message"] == "Success message"
        assert data["data"] is None


class TestHandlerIntegration:
    """Test handler integration patterns."""

    def test_web_handlers_static_methods(self) -> None:
        """Test WebHandlers static methods work independently."""
        # Should be able to call without instantiation
        health_result = WebHandlers.handle_health_check()
        assert health_result.success is True

        app_result = WebHandlers.handle_create_app("integration-test")
        assert app_result.success is True

    def test_response_handler_static_methods(self) -> None:
        """Test WebResponseHandler static methods work independently."""
        app = Flask(__name__)
        with app.app_context():
            # Create handler instance
            handler = WebResponseHandler()
            response = handler.create_success_response("Test")
            _response_obj, status_code = response  # type: ignore[misc]
            assert status_code == 200

    def test_handlers_work_with_domain_models(self) -> None:
        """Test handlers integrate properly with domain models."""
        # Create app via handler
        create_result = WebHandlers.handle_create_app("domain-test", 9000)
        assert create_result.success is True

        app = create_result.value
        assert isinstance(app, FlextWebModels.WebApp)

        # Start app via handler
        start_result = WebHandlers.handle_start_app(app)
        assert start_result.success is True
        assert start_result.value.status == FlextWebModels.WebAppStatus.RUNNING

    def test_error_handling_patterns(self) -> None:
        """Test handlers handle errors properly."""
        # Try to start an already running app
        app = FlextWebModels.WebApp(
            id="app_error-test",
            name="error-test",
            status=FlextWebModels.WebAppStatus.RUNNING,
        )
        result = WebHandlers.handle_start_app(app)
        assert result.success is False
        assert result.error
        assert "already running" in result.error

    def test_handler_composition(self) -> None:
        """Test handlers can be composed together."""
        # Create, start, then stop an app
        create_result = WebHandlers.handle_create_app("compose-test")
        assert create_result.success is True

        start_result = WebHandlers.handle_start_app(create_result.value)
        assert start_result.success is True

        stop_result = WebHandlers.handle_stop_app(start_result.value)
        assert stop_result.success is True
        assert stop_result.value.status == FlextWebModels.WebAppStatus.STOPPED


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
