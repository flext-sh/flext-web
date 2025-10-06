"""Unit tests for flext_web.exceptions module.

Tests the web exceptions functionality following flext standards.
"""

from flext_web.exceptions import FlextWebExceptions


class TestFlextWebExceptions:
    """Test suite for FlextWebExceptions class."""

    def test_web_error_initialization(self) -> None:
        """Test WebError initialization."""
        error = FlextWebExceptions.WebError("Test error message")
        assert str(error) == "Test error message"
        assert error.error_code == "WEB_ERROR"

    def test_web_error_with_route(self) -> None:
        """Test WebError initialization with route."""
        error = FlextWebExceptions.WebError("Test error message", route="/api/test")
        assert str(error) == "Test error message"
        assert error.error_code == "WEB_ERROR"

    def test_web_error_with_context(self) -> None:
        """Test WebError initialization with context."""
        error = FlextWebExceptions.WebError(
            "Test error message", context={"key": "value"}, correlation_id="test-123"
        )
        assert str(error) == "Test error message"
        assert error.error_code == "WEB_ERROR"

    def test_web_validation_error_initialization(self) -> None:
        """Test WebValidationError initialization."""
        error = FlextWebExceptions.WebValidationError("Validation failed")
        assert "Validation failed" in str(error)
        assert error.error_code == "WEB_VALIDATION_ERROR"

    def test_web_validation_error_with_field(self) -> None:
        """Test WebValidationError with field information."""
        error = FlextWebExceptions.WebValidationError(
            "Invalid value", field="email", value="invalid-email"
        )
        assert "Invalid value" in str(error)
        assert "field: email" in str(error)
        assert "[value: invalid-email]" in str(error)

    def test_web_configuration_error_initialization(self) -> None:
        """Test WebConfigurationError initialization."""
        error = FlextWebExceptions.WebConfigurationError("Config error")
        assert str(error) == "Config error"
        assert error.error_code == "WEB_CONFIG_ERROR"

    def test_web_connection_error_initialization(self) -> None:
        """Test WebConnectionError initialization."""
        error = FlextWebExceptions.WebConnectionError("Connection failed")
        assert str(error) == "Connection failed"
        assert error.error_code == "WEB_CONNECTION_ERROR"

    def test_web_processing_error_initialization(self) -> None:
        """Test WebProcessingError initialization."""
        error = FlextWebExceptions.WebProcessingError("Processing failed")
        assert str(error) == "Processing failed"
        assert error.error_code == "WEB_PROCESSING_ERROR"

    def test_web_authentication_error_initialization(self) -> None:
        """Test WebAuthenticationError initialization."""
        error = FlextWebExceptions.WebAuthenticationError("Auth failed")
        assert str(error) == "Auth failed"
        assert error.error_code == "WEB_AUTH_ERROR"

    def test_web_timeout_error_initialization(self) -> None:
        """Test WebTimeoutError initialization."""
        error = FlextWebExceptions.WebTimeoutError("Timeout occurred")
        assert str(error) == "Timeout occurred"
        assert error.error_code == "WEB_TIMEOUT_ERROR"

    def test_web_template_error_initialization(self) -> None:
        """Test WebTemplateError initialization."""
        error = FlextWebExceptions.WebTemplateError("Template error")
        assert str(error) == "Template error"
        assert error.error_code == "WEB_TEMPLATE_ERROR"

    def test_web_template_error_with_template_name(self) -> None:
        """Test WebTemplateError with template name."""
        error = FlextWebExceptions.WebTemplateError(
            "Template not found", template_name="index.html"
        )
        assert "Template not found" in str(error)
        assert error.template_name == "index.html"

    def test_web_routing_error_initialization(self) -> None:
        """Test WebRoutingError initialization."""
        error = FlextWebExceptions.WebRoutingError("Routing error")
        assert str(error) == "Routing error"
        assert error.error_code == "WEB_ROUTING_ERROR"

    def test_web_routing_error_with_endpoint(self) -> None:
        """Test WebRoutingError with endpoint information."""
        error = FlextWebExceptions.WebRoutingError(
            "Route not found", endpoint="/api/test", method="GET"
        )
        assert "Route not found" in str(error)
        assert error.endpoint == "/api/test"
        assert error.method == "GET"

    def test_web_session_error_initialization(self) -> None:
        """Test WebSessionError initialization."""
        error = FlextWebExceptions.WebSessionError("Session error")
        assert str(error) == "Session error"
        assert error.error_code == "WEB_SESSION_ERROR"

    def test_web_session_error_with_session_id(self) -> None:
        """Test WebSessionError with session ID."""
        error = FlextWebExceptions.WebSessionError(
            "Session expired", session_id="sess-123"
        )
        assert "Session expired" in str(error)
        assert error.session_id == "sess-123"

    def test_web_middleware_error_initialization(self) -> None:
        """Test WebMiddlewareError initialization."""
        error = FlextWebExceptions.WebMiddlewareError("Middleware error")
        assert str(error) == "Middleware error"
        assert error.error_code == "WEB_MIDDLEWARE_ERROR"

    def test_web_middleware_error_with_middleware_name(self) -> None:
        """Test WebMiddlewareError with middleware name."""
        error = FlextWebExceptions.WebMiddlewareError(
            "Middleware failed", middleware_name="auth_middleware"
        )
        assert "Middleware failed" in str(error)

    def test_exception_inheritance(self) -> None:
        """Test that all exceptions inherit from the base WebError."""
        error_classes = [
            FlextWebExceptions.WebValidationError,
            FlextWebExceptions.WebConfigurationError,
            FlextWebExceptions.WebConnectionError,
            FlextWebExceptions.WebProcessingError,
            FlextWebExceptions.WebAuthenticationError,
            FlextWebExceptions.WebTimeoutError,
            FlextWebExceptions.WebTemplateError,
            FlextWebExceptions.WebRoutingError,
            FlextWebExceptions.WebSessionError,
            FlextWebExceptions.WebMiddlewareError,
        ]

        for error_class in error_classes:
            error = error_class("Test message")
            assert isinstance(error, FlextWebExceptions.WebError)

    def test_error_codes_are_unique(self) -> None:
        """Test that all error codes are unique."""
        error_classes = [
            FlextWebExceptions.WebError,
            FlextWebExceptions.WebValidationError,
            FlextWebExceptions.WebConfigurationError,
            FlextWebExceptions.WebConnectionError,
            FlextWebExceptions.WebProcessingError,
            FlextWebExceptions.WebAuthenticationError,
            FlextWebExceptions.WebTimeoutError,
            FlextWebExceptions.WebTemplateError,
            FlextWebExceptions.WebRoutingError,
            FlextWebExceptions.WebSessionError,
            FlextWebExceptions.WebMiddlewareError,
        ]

        error_codes = []
        for error_class in error_classes:
            error = error_class("Test message")
            error_codes.append(error.error_code)

        # All error codes should be unique
        assert len(error_codes) == len(set(error_codes))

    def test_error_context_handling(self) -> None:
        """Test error context handling."""
        error = FlextWebExceptions.WebError(
            "Test error",
            context={"user_id": "123", "action": "create"},
            correlation_id="corr-456",
        )
        assert error.correlation_id == "corr-456"
        # Context should be stored in the error
        assert hasattr(error, "context")
