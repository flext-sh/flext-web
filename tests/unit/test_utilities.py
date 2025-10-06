"""Comprehensive unit tests for flext_web.utilities module.

Tests the unified FlextWebUtilities class following flext standards.
"""

from flext_web.utilities import FlextWebUtilities


class TestFlextWebUtilities:
    """Test suite for FlextWebUtilities unified class."""

    def test_utilities_inheritance(self) -> None:
        """Test that FlextWebUtilities inherits from FlextUtilities."""
        # Should have access to base FlextUtilities
        assert hasattr(FlextWebUtilities, "Generators")
        assert hasattr(FlextWebUtilities, "TextProcessor")
        assert hasattr(FlextWebUtilities, "Validators")

    def test_slugify_method(self) -> None:
        """Test _slugify method."""
        # Test basic slugification
        result = FlextWebUtilities._slugify("Test App Name")
        assert result == "test-app-name"

        # Test with special characters
        result = FlextWebUtilities._slugify("Test@App#Name!")
        assert result == "testappname"

        # Test with multiple spaces
        result = FlextWebUtilities._slugify("Test   App    Name")
        assert result == "test-app-name"

        # Test with leading/trailing spaces
        result = FlextWebUtilities._slugify("  Test App Name  ")
        assert result == "test-app-name"

    def test_generate_app_id(self) -> None:
        """Test generate_app_id method."""
        # Test app ID generation
        result = FlextWebUtilities.generate_app_id("Test App")
        assert result.startswith("app_")
        assert "test-app" in result

        # Test with special characters
        result = FlextWebUtilities.generate_app_id("Test@App#Name!")
        assert result.startswith("app_")
        assert "testappname" in result

    def test_format_app_id(self) -> None:
        """Test format_app_id method."""
        # Test app ID formatting
        result = FlextWebUtilities.format_app_id("Test App")
        assert result == "app_test-app"

        # Test with empty string
        result = FlextWebUtilities.format_app_id("")
        assert result == "app_default"

        # Test with special characters
        result = FlextWebUtilities.format_app_id("Test@App#Name!")
        assert result == "app_testappname"

    def test_validate_app_name(self) -> None:
        """Test validate_app_name method."""
        # Test valid app names
        assert FlextWebUtilities.validate_app_name("test-app") is True
        assert FlextWebUtilities.validate_app_name("my_service") is True
        assert FlextWebUtilities.validate_app_name("api-server") is True

        # Test invalid app names
        assert FlextWebUtilities.validate_app_name(None) is False
        assert FlextWebUtilities.validate_app_name("") is False
        assert FlextWebUtilities.validate_app_name("   ") is False

    def test_validate_port_range(self) -> None:
        """Test validate_port_range method."""
        # Test valid ports
        assert FlextWebUtilities.validate_port_range(1024) is True
        assert FlextWebUtilities.validate_port_range(3000) is True
        assert FlextWebUtilities.validate_port_range(8080) is True
        assert FlextWebUtilities.validate_port_range(65535) is True

        # Test invalid ports
        assert FlextWebUtilities.validate_port_range(0) is False
        assert FlextWebUtilities.validate_port_range(1023) is False
        assert FlextWebUtilities.validate_port_range(65536) is False

    def test_validate_url(self) -> None:
        """Test validate_url method."""
        # Test valid URLs
        assert FlextWebUtilities.validate_url("https://example.com") is True
        assert FlextWebUtilities.validate_url("http://localhost:8080") is True
        assert FlextWebUtilities.validate_url("https://api.example.com/v1") is True

        # Test invalid URLs
        assert FlextWebUtilities.validate_url("") is False
        assert FlextWebUtilities.validate_url("not-a-url") is False
        assert FlextWebUtilities.validate_url("ftp://example.com") is False
        assert FlextWebUtilities.validate_url("example.com") is False

    def test_validate_host_format(self) -> None:
        """Test validate_host_format method."""
        # Test valid hosts
        assert FlextWebUtilities.validate_host_format("localhost") is True
        assert FlextWebUtilities.validate_host_format("127.0.0.1") is True
        assert FlextWebUtilities.validate_host_format("0.0.0.0") is True
        assert FlextWebUtilities.validate_host_format("example.com") is True
        assert FlextWebUtilities.validate_host_format("api.example.com") is True

        # Test invalid hosts
        assert FlextWebUtilities.validate_host_format("") is False
        assert FlextWebUtilities.validate_host_format("   ") is False
        assert FlextWebUtilities.validate_host_format("invalid@host") is False

    def test_sanitize_request_data(self) -> None:
        """Test sanitize_request_data method."""
        # Test with valid data
        data = {"key": "value", "number": 123, "boolean": True}
        result = FlextWebUtilities.sanitize_request_data(data)

        assert isinstance(result, dict)
        assert result["key"] == "value"
        assert result["number"] == 123
        assert result["boolean"] is True

        # Test with string data
        data = {"key": "  value  ", "name": "Test@Name#!"}
        result = FlextWebUtilities.sanitize_request_data(data)

        assert result["key"] == "value"
        assert result["name"] == "TestName"

    def test_create_success_response(self) -> None:
        """Test create_success_response method."""
        # Test with message only
        result = FlextWebUtilities.create_success_response("Operation successful")

        assert isinstance(result, dict)
        assert result["success"] == "True"
        assert result["message"] == "Operation successful"
        assert result["data"] is None
        assert "timestamp" in result

        # Test with data
        result = FlextWebUtilities.create_success_response(
            "Operation successful", {"key": "value"}
        )

        assert result["success"] == "True"
        assert result["message"] == "Operation successful"
        assert result["data"] == {"key": "value"}

    def test_create_error_response(self) -> None:
        """Test create_error_response method."""
        # Test with message only
        result = FlextWebUtilities.create_error_response("Operation failed")

        assert isinstance(result, dict)
        assert result["success"] == "False"
        assert result["message"] == "Operation failed"
        assert result["data"] is None
        assert result["status_code"] == 400
        assert "timestamp" in result

        # Test with custom status code
        result = FlextWebUtilities.create_error_response("Operation failed", 500)

        assert result["success"] == "False"
        assert result["message"] == "Operation failed"
        assert result["status_code"] == 500

    def test_create_api_response(self) -> None:
        """Test create_api_response method."""
        # Test success response
        result = FlextWebUtilities.create_api_response(
            "Success", success=True, data={"key": "value"}
        )

        assert isinstance(result, dict)
        assert result["success"] is True
        assert result["message"] == "Success"
        assert result["data"] == {"key": "value"}
        assert "timestamp" in result

        # Test error response
        result = FlextWebUtilities.create_api_response(
            "Error", success=False, data=None
        )

        assert result["success"] is False
        assert result["message"] == "Error"
        assert result["data"] is None

    def test_handle_flext_result(self) -> None:
        """Test handle_flext_result method."""
        from flext_core import FlextResult

        # Test with success result
        success_result = FlextResult[str].ok("Success data")
        result = FlextWebUtilities.handle_flext_result(success_result)

        assert isinstance(result, dict)
        assert result["success"] is True
        assert result["message"] == "Operation successful"
        assert result["data"] == "Success data"

        # Test with failure result
        failure_result = FlextResult[str].fail("Error message")
        result = FlextWebUtilities.handle_flext_result(failure_result)

        assert isinstance(result, dict)
        assert result["success"] is False
        assert result["message"] == "Operation failed: Error message"
        assert result["data"] is None

    def test_create_web_app_data_success(self) -> None:
        """Test create_web_app_data method with success."""
        result = FlextWebUtilities.create_web_app_data("test-app", 8080, "localhost")

        assert result.is_success
        app_data = result.value
        assert isinstance(app_data, dict)
        assert app_data["name"] == "test-app"
        assert app_data["host"] == "localhost"
        assert app_data["port"] == 8080
        assert "id" in app_data
        assert "created_at" in app_data

    def test_create_web_app_data_validation_error(self) -> None:
        """Test create_web_app_data method with validation error."""
        # Test with invalid name
        result = FlextWebUtilities.create_web_app_data("", 8080, "localhost")

        assert result.is_failure
        assert "Invalid app name" in result.error

    def test_create_web_app_data_invalid_port(self) -> None:
        """Test create_web_app_data method with invalid port."""
        # Test with invalid port
        result = FlextWebUtilities.create_web_app_data("test-app", 0, "localhost")

        assert result.is_failure
        assert "Invalid port" in result.error

    def test_create_web_app_data_invalid_host(self) -> None:
        """Test create_web_app_data method with invalid host."""
        # Test with invalid host
        result = FlextWebUtilities.create_web_app_data("test-app", 8080, "")

        assert result.is_failure
        assert "Invalid host" in result.error

    def test_utilities_integration_patterns(self) -> None:
        """Test FlextWebUtilities integration patterns."""
        # All methods should return appropriate types
        methods_to_test = [
            lambda: FlextWebUtilities.validate_app_name("test"),
            lambda: FlextWebUtilities.validate_port_range(8080),
            lambda: FlextWebUtilities.validate_url("https://example.com"),
            lambda: FlextWebUtilities.validate_host_format("localhost"),
        ]

        for method in methods_to_test:
            result = method()
            assert isinstance(result, bool)

    def test_utilities_error_handling(self) -> None:
        """Test FlextWebUtilities error handling."""
        # Test with None inputs
        assert FlextWebUtilities.validate_app_name(None) is False
        assert FlextWebUtilities.validate_url(None) is False
        assert FlextWebUtilities.validate_host_format(None) is False

    def test_utilities_logging_integration(self) -> None:
        """Test FlextWebUtilities logging integration."""
        # Should have access to FlextUtilities logging
        assert hasattr(FlextWebUtilities, "Generators")
        assert hasattr(FlextWebUtilities.Generators, "generate_iso_timestamp")

    def test_utilities_type_consistency(self) -> None:
        """Test FlextWebUtilities type consistency."""
        # All methods should return consistent types
        assert isinstance(FlextWebUtilities.format_app_id("test"), str)
        assert isinstance(FlextWebUtilities.generate_app_id("test"), str)
        assert isinstance(FlextWebUtilities.validate_app_name("test"), bool)
        assert isinstance(FlextWebUtilities.validate_port_range(8080), bool)
        assert isinstance(FlextWebUtilities.validate_url("https://example.com"), bool)
        assert isinstance(FlextWebUtilities.validate_host_format("localhost"), bool)

    def test_utilities_edge_cases(self) -> None:
        """Test FlextWebUtilities edge cases."""
        # Test empty string handling
        assert FlextWebUtilities.validate_app_name("") is False
        assert FlextWebUtilities.format_app_id("") == "app_default"

        # Test whitespace handling
        assert FlextWebUtilities.validate_app_name("   ") is False
        assert FlextWebUtilities.format_app_id("   ") == "app_default"

        # Test special character handling
        result = FlextWebUtilities.format_app_id("Test@App#Name!")
        assert result == "app_testappname"

    def test_utilities_performance(self) -> None:
        """Test FlextWebUtilities performance."""
        # Test that methods complete quickly
        import time

        start_time = time.time()
        for _ in range(100):
            FlextWebUtilities.validate_app_name("test-app")
        end_time = time.time()

        # Should complete quickly (less than 1 second for 100 iterations)
        assert end_time - start_time < 1.0

    def test_utilities_consistency(self) -> None:
        """Test FlextWebUtilities consistency."""
        # Test that same inputs produce same outputs
        result1 = FlextWebUtilities.format_app_id("Test App")
        result2 = FlextWebUtilities.format_app_id("Test App")
        assert result1 == result2

        # Test that different inputs produce different outputs
        result1 = FlextWebUtilities.format_app_id("Test App")
        result2 = FlextWebUtilities.format_app_id("Different App")
        assert result1 != result2
