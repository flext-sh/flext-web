"""Comprehensive test coverage for flext_web.utilities module.

This test module targets specific missing coverage areas identified in the coverage report.
Focus on real execution tests without mocks for maximum functional coverage.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from flext_core import FlextResult

from flext_web import FlextWebUtilities


class TestFlextWebUtilitiesAppId:
    """Test application ID generation and formatting utilities."""

    def test_generate_app_id(self) -> None:
        """Test generating unique app ID."""
        app_id = FlextWebUtilities.generate_app_id("Test App")

        assert app_id.startswith("app_test-app_")
        assert len(app_id.split("_")) == 3  # app, slugified-name, unique-id

    def test_generate_app_id_with_special_characters(self) -> None:
        """Test generating app ID with special characters."""
        app_id = FlextWebUtilities.generate_app_id("Test@App#123")

        assert app_id.startswith("app_test-app-123_")
        assert "_" in app_id

    def test_generate_app_id_empty_name(self) -> None:
        """Test generating app ID with empty name."""
        app_id = FlextWebUtilities.generate_app_id("")

        # Should still generate a valid ID even with empty name
        assert app_id.startswith("app_")
        assert len(app_id) > 4

    def test_format_app_id(self) -> None:
        """Test formatting application name to valid ID."""
        app_id = FlextWebUtilities.format_app_id("My Test App")

        assert app_id == "app_my-test-app"

    def test_format_app_id_with_special_chars(self) -> None:
        """Test formatting app ID with special characters."""
        app_id = FlextWebUtilities.format_app_id("App@#$%^&*()")

        assert app_id == "app_app"

    def test_format_app_id_empty_string(self) -> None:
        """Test formatting empty string to app ID."""
        app_id = FlextWebUtilities.format_app_id("")

        assert app_id == "app_default"

    def test_format_app_id_whitespace_only(self) -> None:
        """Test formatting whitespace-only string to app ID."""
        app_id = FlextWebUtilities.format_app_id("   ")

        assert app_id == "app_default"


class TestFlextWebUtilitiesValidation:
    """Test validation utility functions."""

    def test_validate_app_name_valid(self) -> None:
        """Test validating valid app names."""
        valid_names = ["test", "Test App", "my-app-123", "A"]

        for name in valid_names:
            assert FlextWebUtilities.validate_app_name(name) is True

    def test_validate_app_name_invalid(self) -> None:
        """Test validating invalid app names."""
        invalid_names = [None, "", "   ", "\t\n"]

        for name in invalid_names:
            assert FlextWebUtilities.validate_app_name(name) is False

    def test_validate_port_range_valid(self) -> None:
        """Test validating valid port numbers."""
        valid_ports = [80, 443, 8000, 8080, 3000, 9000, 65535]

        for port in valid_ports:
            assert FlextWebUtilities.validate_port_range(port) is True

    def test_validate_port_range_invalid(self) -> None:
        """Test validating invalid port numbers."""
        invalid_ports = [-1, 0, 65536, 70000, 999999]

        for port in invalid_ports:
            assert FlextWebUtilities.validate_port_range(port) is False

    def test_validate_url_valid(self) -> None:
        """Test validating valid URLs."""
        valid_urls = [
            "http://localhost:8080",
            "https://example.com",
            "https://internal.invalid/REDACTED",
            "https://subdomain.example.org/path",
            "ftp://files.example.com",
        ]

        for url in valid_urls:
            assert FlextWebUtilities.validate_url(url) is True

    def test_validate_url_invalid(self) -> None:
        """Test validating invalid URLs."""
        invalid_urls = [
            "",
            "not-a-url",
            "http://",
            "://example.com",
            "example.com",  # Missing scheme
            "http:///path",  # Missing netloc
        ]

        for url in invalid_urls:
            assert FlextWebUtilities.validate_url(url) is False

    def test_validate_url_exception_handling(self) -> None:
        """Test URL validation handles exceptions."""
        # Pass invalid string that might cause urlparse to raise exception
        assert FlextWebUtilities.validate_url("") is False

    def test_validate_host_format_valid_ipv4(self) -> None:
        """Test validating valid IPv4 addresses."""
        valid_ipv4 = [
            "192.168.1.1",
            "127.0.0.1",
            "10.0.0.1",
            "255.255.255.255",
            "0.0.0.0",
        ]

        for host in valid_ipv4:
            assert FlextWebUtilities.validate_host_format(host) is True

    def test_validate_host_format_valid_hostnames(self) -> None:
        """Test validating valid hostnames."""
        valid_hostnames = [
            "localhost",
            "example.com",
            "subdomain.example.org",
            "test-server",
            "internal.invalid",
            "::",  # IPv6 localhost
            "::1",  # IPv6 localhost
        ]

        for host in valid_hostnames:
            assert FlextWebUtilities.validate_host_format(host) is True

    def test_validate_host_format_invalid(self) -> None:
        """Test validating invalid host formats."""
        invalid_hosts = [
            "",
            "   ",
            "-invalid-host",  # Cannot start with dash
            "host-.com",  # Cannot end with dash
            "host..com",  # Double dots
            "a" * 70 + ".com",  # Too long segment
            "not a valid host name with spaces",  # Spaces not allowed
        ]

        for host in invalid_hosts:
            assert FlextWebUtilities.validate_host_format(host) is False

    def test_validate_host_format_empty_after_safe_string(self) -> None:
        """Test host validation when safe_string returns empty."""
        # Test with None (should be handled by safe_string)
        assert FlextWebUtilities.validate_host_format("") is False


class TestFlextWebUtilitiesDataSanitization:
    """Test data sanitization utilities."""

    def test_sanitize_request_data_basic(self) -> None:
        """Test basic request data sanitization."""
        data = {"name": "test app", "port": 8000, "host": "localhost"}

        sanitized = FlextWebUtilities.sanitize_request_data(data)

        assert sanitized["name"] == "test app"
        assert sanitized["port"] == 8000
        assert sanitized["host"] == "localhost"

    def test_sanitize_request_data_with_special_chars(self) -> None:
        """Test sanitizing data with special characters."""
        data = {
            "app@name": "test<script>alert('xss')</script>",
            "port": 8000,
            "desc": "Description with & special chars",
        }

        sanitized = FlextWebUtilities.sanitize_request_data(data)

        # Keys are passed through safe_string (minimal processing)
        assert "app@name" in sanitized  # Key preserved as-is
        # String values should be processed by safe_string
        assert isinstance(sanitized["app@name"], str)
        assert sanitized["port"] == 8000  # Non-string values preserved

    def test_sanitize_request_data_non_string_values(self) -> None:
        """Test sanitizing data with non-string values."""
        data = {
            "name": "test",
            "port": 8000,
            "enabled": True,
            "config": {"key": "value"},
            "tags": ["tag1", "tag2"],
        }

        sanitized = FlextWebUtilities.sanitize_request_data(data)

        # Non-string values should be preserved
        assert sanitized["port"] == 8000
        assert sanitized["enabled"] is True
        assert sanitized["config"] == {"key": "value"}
        assert sanitized["tags"] == ["tag1", "tag2"]

    def test_sanitize_request_data_empty(self) -> None:
        """Test sanitizing empty data."""
        data: FlextTypes.Core.Dict = {}

        sanitized = FlextWebUtilities.sanitize_request_data(data)

        assert sanitized == {}


class TestFlextWebUtilitiesResponseCreation:
    """Test response creation utilities."""

    def test_create_success_response(self) -> None:
        """Test creating success response."""
        response = FlextWebUtilities.create_success_response("Operation completed")

        assert response["success"] is True
        assert response["message"] == "Operation completed"
        assert response["data"] is None
        assert "timestamp" in response

    def test_create_success_response_with_data(self) -> None:
        """Test creating success response with data."""
        data = {"id": "123", "name": "test"}
        response = FlextWebUtilities.create_success_response(
            "Created successfully", data
        )

        assert response["success"] is True
        assert response["message"] == "Created successfully"
        assert response["data"] == data
        assert "timestamp" in response

    def test_create_error_response(self) -> None:
        """Test creating error response."""
        response = FlextWebUtilities.create_error_response("Something went wrong")

        assert response["success"] is False
        assert response["message"] == "Something went wrong"
        assert response["data"] is None
        assert response["status_code"] == 400
        assert "timestamp" in response

    def test_create_error_response_with_custom_status(self) -> None:
        """Test creating error response with custom status code."""
        response = FlextWebUtilities.create_error_response("Not found", 404)

        assert response["success"] is False
        assert response["message"] == "Not found"
        assert response["status_code"] == 404
        assert "timestamp" in response

    def test_create_api_response_success(self) -> None:
        """Test creating API response for success."""
        data = {"result": "ok"}
        response = FlextWebUtilities.create_api_response(
            "Success", success=True, data=data
        )

        assert response["success"] is True
        assert response["message"] == "Success"
        assert response["data"] == data
        assert "timestamp" in response

    def test_create_api_response_error(self) -> None:
        """Test creating API response for error."""
        response = FlextWebUtilities.create_api_response(
            "Failed", success=False, data=None
        )

        assert response["success"] is False
        assert response["message"] == "Failed"
        assert response["data"] is None
        assert "timestamp" in response

    def test_create_api_response_defaults(self) -> None:
        """Test creating API response with defaults."""
        response = FlextWebUtilities.create_api_response("Default response")

        assert response["success"] is True  # Default
        assert response["message"] == "Default response"
        assert response["data"] is None  # Default
        assert "timestamp" in response


class TestFlextWebUtilitiesFlextResultHandling:
    """Test FlextResult handling utilities."""

    def test_handle_flext_result_success(self) -> None:
        """Test handling successful FlextResult."""
        success_result = FlextResult[FlextTypes.Core.Headers].ok(
            {"id": "123", "name": "test"}
        )

        response = FlextWebUtilities.handle_flext_result(success_result)

        assert response["success"] is True
        assert response["message"] == "Operation successful"
        assert response["data"] == {"id": "123", "name": "test"}
        assert "timestamp" in response

    def test_handle_flext_result_failure(self) -> None:
        """Test handling failed FlextResult."""
        failure_result = FlextResult[str].fail("Validation error occurred")

        response = FlextWebUtilities.handle_flext_result(failure_result)

        assert response["success"] is False
        assert "Operation failed: Validation error occurred" in str(response["message"])
        assert response["data"] is None
        assert "timestamp" in response

    def test_handle_flext_result_with_none_value(self) -> None:
        """Test handling FlextResult with None value."""
        success_result = FlextResult[None].ok(None)

        response = FlextWebUtilities.handle_flext_result(success_result)

        assert response["success"] is True
        assert response["data"] is None


class TestFlextWebUtilitiesWebAppDataCreation:
    """Test web app data creation utility."""

    def test_create_web_app_data_valid(self) -> None:
        """Test creating valid web app data."""
        result = FlextWebUtilities.create_web_app_data("test-app", 8000, "localhost")

        assert result.is_success
        data = result.value
        assert data["name"] == "test-app"
        assert data["port"] == 8000
        assert data["host"] == "localhost"
        assert data["id"] == "app_test-app"
        assert "created_at" in data

    def test_create_web_app_data_defaults(self) -> None:
        """Test creating web app data with defaults."""
        result = FlextWebUtilities.create_web_app_data("my-app")

        assert result.is_success
        data = result.value
        assert data["name"] == "my-app"
        assert data["port"] == 8000  # Default
        assert data["host"] == "localhost"  # Default

    def test_create_web_app_data_invalid_name(self) -> None:
        """Test creating web app data with invalid name."""
        result = FlextWebUtilities.create_web_app_data("", 8000, "localhost")

        assert result.is_failure
        assert "Invalid app name" in str(result.error)

    def test_create_web_app_data_invalid_port(self) -> None:
        """Test creating web app data with invalid port."""
        result = FlextWebUtilities.create_web_app_data("test-app", -1, "localhost")

        assert result.is_failure
        assert "Invalid port" in str(result.error)

    def test_create_web_app_data_invalid_host(self) -> None:
        """Test creating web app data with invalid host."""
        result = FlextWebUtilities.create_web_app_data("test-app", 8000, "")

        assert result.is_failure
        assert "Invalid host" in str(result.error)

    def test_create_web_app_data_all_invalid(self) -> None:
        """Test creating web app data with all invalid parameters."""
        result = FlextWebUtilities.create_web_app_data("", -1, "")

        # Should fail on first validation (name)
        assert result.is_failure
        assert "Invalid app name" in str(result.error)


class TestFlextWebUtilitiesEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_generate_app_id_unicode_characters(self) -> None:
        """Test generating app ID with unicode characters."""
        app_id = FlextWebUtilities.generate_app_id("测试应用")

        # Should handle unicode gracefully
        assert app_id.startswith("app_")
        assert len(app_id) > 4

    def test_validate_host_format_edge_cases(self) -> None:
        """Test host format validation edge cases."""
        edge_cases = {
            "   localhost   ": True,  # Whitespace trimmed
            "LOCALHOST": True,  # Case insensitive for special hosts
            "0.0.0.0": True,  # Special IP
        }

        for host, expected in edge_cases.items():
            assert FlextWebUtilities.validate_host_format(host) == expected

    def test_sanitize_request_data_none_values(self) -> None:
        """Test sanitizing request data with None values."""
        data: FlextTypes.Core.Dict = {"name": None, "port": 8000, "description": None}

        sanitized = FlextWebUtilities.sanitize_request_data(data)

        # None values should be preserved
        assert sanitized["name"] is None
        assert sanitized["description"] is None
        assert sanitized["port"] == 8000
