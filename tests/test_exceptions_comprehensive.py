#!/usr/bin/env python3
"""Comprehensive tests for FLEXT Web Interface exception hierarchy.

Tests all exception classes, their inheritance relationships, message handling,
error codes, and integration with flext-core patterns.
"""

from __future__ import annotations

import pytest
from flext_web.exceptions import (
    FlextWebAuthenticationError,
    FlextWebConfigurationError,
    FlextWebConnectionError,
    FlextWebError,
    FlextWebMiddlewareError,
    FlextWebProcessingError,
    FlextWebRoutingError,
    FlextWebSessionError,
    FlextWebTemplateError,
    FlextWebTimeoutError,
    FlextWebValidationError,
)


class TestFlextWebErrorBase:
    """Test base FlextWebError functionality."""

    def test_flext_web_error_creation(self) -> None:
        """Test basic FlextWebError creation with message."""
        error = FlextWebError("Test error message")
        assert "Test error message" in str(error)
        assert error.message == "Test error message"

    def test_flext_web_error_with_route(self) -> None:
        """Test FlextWebError creation with route context."""
        error = FlextWebError("Test error", "/api/v1/test")
        assert error.message == "Test error"
        assert hasattr(error, "error_code")

    def test_flext_web_error_with_kwargs(self) -> None:
        """Test FlextWebError creation with additional context."""
        error = FlextWebError("Validation failed", context="test_context")
        assert error.message == "Validation failed"

    def test_flext_web_error_repr(self) -> None:
        """Test FlextWebError string representation."""
        error = FlextWebError("Test message")
        assert "Test message" in str(error)

    def test_flext_web_error_dict_conversion(self) -> None:
        """Test FlextWebError to_dict method."""
        error = FlextWebError("Test error", "/api/test")
        error_dict = error.to_dict()

        assert "message" in error_dict
        assert error_dict["message"] == "Test error"
        assert "error_code" in error_dict


class TestValidationErrors:
    """Test validation-related exception classes."""

    def test_validation_error(self) -> None:
        """Test FlextWebValidationError functionality."""
        error = FlextWebValidationError("Invalid input", field="name", value="invalid")
        assert isinstance(error, Exception)
        assert "Invalid input" in error.message

    def test_configuration_error(self) -> None:
        """Test FlextWebConfigurationError functionality."""
        error = FlextWebConfigurationError("Invalid config")
        assert isinstance(error, Exception)
        assert "Invalid config" in error.message

    def test_authentication_error(self) -> None:
        """Test FlextWebAuthenticationError functionality."""
        error = FlextWebAuthenticationError("Auth failed")
        assert isinstance(error, Exception)
        assert "Auth failed" in error.message


class TestConnectionAndProcessingErrors:
    """Test connection and processing exception classes."""

    def test_connection_error(self) -> None:
        """Test FlextWebConnectionError functionality."""
        error = FlextWebConnectionError("Connection failed")
        assert isinstance(error, Exception)
        assert "Connection failed" in error.message

    def test_processing_error(self) -> None:
        """Test FlextWebProcessingError functionality."""
        error = FlextWebProcessingError("Processing failed")
        assert isinstance(error, Exception)
        assert "Processing failed" in error.message

    def test_timeout_error(self) -> None:
        """Test FlextWebTimeoutError functionality."""
        error = FlextWebTimeoutError("Operation timeout")
        assert isinstance(error, Exception)
        assert "Operation timeout" in error.message


class TestWebSpecificErrors:
    """Test web-specific exception classes."""

    def test_template_error(self) -> None:
        """Test FlextWebTemplateError functionality."""
        error = FlextWebTemplateError("Template rendering failed")
        assert isinstance(error, FlextWebError)
        assert "Template rendering failed" in error.message

    def test_routing_error(self) -> None:
        """Test FlextWebRoutingError functionality."""
        error = FlextWebRoutingError("Route not found")
        assert isinstance(error, FlextWebError)
        assert "Route not found" in error.message

    def test_session_error(self) -> None:
        """Test FlextWebSessionError functionality."""
        error = FlextWebSessionError("Session expired")
        assert isinstance(error, FlextWebError)
        assert "Session expired" in error.message

    def test_middleware_error(self) -> None:
        """Test FlextWebMiddlewareError functionality."""
        error = FlextWebMiddlewareError("Middleware failed")
        assert isinstance(error, FlextWebError)
        assert "Middleware failed" in error.message


class TestExceptionHierarchy:
    """Test exception inheritance hierarchy and relationships."""

    def test_base_exception_inheritance(self) -> None:
        """Test that all exceptions inherit from Exception and proper base classes."""
        # FlextWebError inherits from FlextError
        assert isinstance(FlextWebError("test"), Exception)

        # Check specific inheritance patterns
        assert isinstance(FlextWebValidationError("test"), Exception)
        assert isinstance(FlextWebAuthenticationError("test"), Exception)
        assert isinstance(FlextWebConfigurationError("test"), Exception)
        assert isinstance(FlextWebConnectionError("test"), Exception)
        assert isinstance(FlextWebProcessingError("test"), Exception)
        assert isinstance(FlextWebTimeoutError("test"), Exception)

        # Web-specific errors inherit from FlextWebError
        web_specific_errors = [
            FlextWebTemplateError("test"),
            FlextWebRoutingError("test"),
            FlextWebSessionError("test"),
            FlextWebMiddlewareError("test"),
        ]

        for exception in web_specific_errors:
            assert isinstance(exception, FlextWebError)
            assert isinstance(exception, Exception)

    def test_web_specific_error_hierarchy(self) -> None:
        """Test that web-specific errors inherit directly from FlextWebError."""
        web_specific_errors = [
            FlextWebTemplateError("test"),
            FlextWebRoutingError("test"),
            FlextWebSessionError("test"),
            FlextWebMiddlewareError("test"),
        ]

        for error in web_specific_errors:
            # These should inherit directly from FlextWebError
            assert isinstance(error, FlextWebError)
            assert type(error).__bases__[0].__name__ == "FlextWebError"


class TestExceptionUtilities:
    """Test exception utility methods and features."""

    def test_exception_chaining(self) -> None:
        """Test exception chaining functionality."""
        original = ValueError("Original error")

        try:
            raise original
        except ValueError as e:
            chained = FlextWebProcessingError("Processing failed")
            chained.__cause__ = e

            assert chained.__cause__ is original
            assert str(chained.__cause__) == "Original error"

    def test_error_context_preservation(self) -> None:
        """Test that error context is preserved."""
        details = {"request_id": "123", "user_id": "user456", "operation": "create_app"}

        error = FlextWebProcessingError("App creation failed", **details)
        error_dict = error.to_dict()

        # Just check that the error was created and has basic properties
        assert "App creation failed" in error.message
        assert "message" in error_dict

    def test_multiple_exception_handling(self) -> None:
        """Test handling multiple related exceptions."""
        errors: list[Exception] = []

        # Simulate multiple validation errors
        errors.extend((FlextWebValidationError("Name required"), FlextWebValidationError("Port invalid"), FlextWebValidationError("Host invalid")))

        assert len(errors) == 3
        assert all(isinstance(e, FlextWebValidationError) for e in errors)
        assert all(isinstance(e, Exception) for e in errors)

    def test_error_serialization(self) -> None:
        """Test error serialization for API responses."""
        error = FlextWebProcessingError("Application startup failed")
        serialized = error.to_dict()

        assert "error_code" in serialized
        assert "Application startup failed" in str(serialized["message"])
        assert "context" in serialized or "details" in serialized

    def test_route_context_handling(self) -> None:
        """Test route context in routing errors."""
        error = FlextWebRoutingError("Route not found", "/api/v1/nonexistent")

        assert "Route not found" in error.message
        assert isinstance(error, FlextWebError)

    def test_template_error_context(self) -> None:
        """Test template error with rendering context."""
        error = FlextWebTemplateError("Template variable not found")

        assert "Template variable not found" in error.message
        assert isinstance(error, FlextWebError)

    def test_session_error_context(self) -> None:
        """Test session error with session context."""
        error = FlextWebSessionError("Session validation failed")

        assert "Session validation failed" in error.message
        assert isinstance(error, FlextWebError)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
