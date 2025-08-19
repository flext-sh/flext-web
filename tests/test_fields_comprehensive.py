"""Comprehensive tests for FLEXT Web Interface field definitions and validation.

Tests all Pydantic field definitions, validators, and edge cases to achieve
complete coverage of the fields module.
"""

from __future__ import annotations

import pytest

from flext_web.fields import (
    HTTPStatusField,
    WebFields,
)


class TestWebFields:
    """Test WebFields class functionality."""

    def test_app_name_field_creation(self) -> None:
        """Test app_name_field factory method."""
        field = WebFields.app_name_field()
        assert hasattr(field, "description")

        # Test with custom parameters
        custom_field = WebFields.app_name_field(
            description="Custom app name",
            min_length=3,
            max_length=50
        )
        assert custom_field.description == "Custom app name"

    def test_host_field_creation(self) -> None:
        """Test host_field factory method."""
        field = WebFields.host_field()
        assert hasattr(field, "description")
        assert field.default == "localhost"

        # Test with custom parameters
        custom_field = WebFields.host_field(
            description="Custom host",
            default="0.0.0.0"
        )
        assert custom_field.default == "0.0.0.0"

    def test_port_field_creation(self) -> None:
        """Test port_field factory method."""
        field = WebFields.port_field()
        assert hasattr(field, "description")
        assert field.default == 8000
        # FieldInfo stores constraints in metadata, just verify it exists
        assert type(field).__name__ == "FieldInfo"

        # Test with custom parameters
        custom_field = WebFields.port_field(
            description="Custom port",
            default=9000
        )
        assert custom_field.default == 9000

    def test_url_field_creation(self) -> None:
        """Test url_field factory method."""
        field = WebFields.url_field()
        assert hasattr(field, "description")

        # Test with custom description
        custom_field = WebFields.url_field(description="Custom URL")
        assert custom_field.description == "Custom URL"

    def test_secret_key_field_creation(self) -> None:
        """Test secret_key_field factory method."""
        field = WebFields.secret_key_field()
        assert hasattr(field, "description")
        # FieldInfo stores constraints in metadata, just verify it exists
        assert type(field).__name__ == "FieldInfo"

        # Test with custom parameters
        custom_field = WebFields.secret_key_field(
            description="Custom secret",
            min_length=16
        )
        assert custom_field.description == "Custom secret"


class TestWebFieldValidators:
    """Test WebFields validator methods."""

    def test_validate_app_name_valid(self) -> None:
        """Test validate_app_name with valid names."""
        valid_names = [
            "test-app",
            "web_service",
            "MyApp123",
            "app1",
            "a",
            "test-app-123_name"
        ]

        for name in valid_names:
            result = WebFields.validate_app_name(name)
            assert result == name

    def test_validate_app_name_invalid(self) -> None:
        """Test validate_app_name with invalid names."""
        invalid_names = [
            "",  # Empty
            "-app",  # Starts with hyphen
            "app-",  # Ends with hyphen
            "_app",  # Starts with underscore
            "app_",  # Ends with underscore
            "app name",  # Contains space
            "app@name",  # Contains invalid character
            "a" * 256,  # Too long
        ]

        for name in invalid_names:
            with pytest.raises(ValueError):
                WebFields.validate_app_name(name)

    def test_validate_host_valid(self) -> None:
        """Test validate_host with valid hosts."""
        valid_hosts = [
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
            "192.168.1.1",
            "example.com",
            "sub.example.com",
            "internal.invalid"
        ]

        for host in valid_hosts:
            result = WebFields.validate_host(host)
            assert result == host

    def test_validate_host_invalid(self) -> None:
        """Test validate_host with invalid hosts."""
        invalid_hosts = [
            "",  # Empty
            "not a host",  # Contains space
            "host@invalid",  # Contains invalid character
        ]

        for host in invalid_hosts:
            with pytest.raises(ValueError):
                WebFields.validate_host(host)

    def test_validate_port_valid(self) -> None:
        """Test validate_port with valid ports."""
        valid_ports = [1, 80, 443, 8080, 8443, 65535]

        for port in valid_ports:
            result = WebFields.validate_port(port)
            assert result == port

    def test_validate_port_invalid(self) -> None:
        """Test validate_port with invalid ports."""
        invalid_ports = [0, -1, 65536, 100000]

        for port in invalid_ports:
            with pytest.raises(ValueError):
                WebFields.validate_port(port)

    def test_validate_url_valid(self) -> None:
        """Test validate_url with valid URLs."""
        valid_urls = [
            "http://localhost",
            "https://example.com",
            "https://internal.invalid/REDACTED",
            "https://api.example.com/v1/users",
            "https://internal.invalid/REDACTED"
        ]

        for url in valid_urls:
            result = WebFields.validate_url(url)
            assert result == url

    def test_validate_url_invalid(self) -> None:
        """Test validate_url with invalid URLs."""
        invalid_urls = [
            "",  # Empty
            "not-a-url",
            "ftp://example.com",  # Not HTTP/HTTPS
            "http://",  # Incomplete
        ]

        for url in invalid_urls:
            with pytest.raises(ValueError):
                WebFields.validate_url(url)

    def test_validate_secret_key_valid(self) -> None:
        """Test validate_secret_key with valid keys."""
        valid_keys = [
            "a" * 32,  # Minimum length
            "super-secret-key-for-testing-123456",
            "x" * 100,  # Long key
        ]

        for key in valid_keys:
            result = WebFields.validate_secret_key(key)
            assert result == key

    def test_validate_secret_key_invalid(self) -> None:
        """Test validate_secret_key with invalid keys."""
        invalid_keys = [
            "",  # Empty
            "short",  # Too short
            "development-secret-change-in-production",  # Default key
        ]

        for key in invalid_keys:
            with pytest.raises(ValueError):
                WebFields.validate_secret_key(key)


class TestHTTPStatusField:
    """Test HTTPStatusField functionality."""

    def test_http_status_field_validators(self) -> None:
        """Test HTTPStatusField validators are present."""
        validators = HTTPStatusField.__get_validators__()
        validator_list = list(validators)
        assert len(validator_list) > 0

    def test_validate_status_valid(self) -> None:
        """Test HTTPStatusField.validate with valid status codes."""
        valid_codes = [100, 200, 201, 404, 500, 599]

        for code in valid_codes:
            result = HTTPStatusField.validate(code)
            assert result == code

    def test_validate_status_invalid_type(self) -> None:
        """Test HTTPStatusField.validate with invalid types."""
        invalid_values = ["200", 200.5, None, [200]]

        for value in invalid_values:
            with pytest.raises((TypeError, ValueError)):
                HTTPStatusField.validate(value)

    def test_validate_status_invalid_range(self) -> None:
        """Test HTTPStatusField.validate with invalid ranges."""
        invalid_codes = [0, 99, 600, 1000]

        for code in invalid_codes:
            with pytest.raises(ValueError):
                HTTPStatusField.validate(code)

    def test_modify_schema(self) -> None:
        """Test HTTPStatusField schema modification."""
        schema = {}
        HTTPStatusField.__modify_schema__(schema)

        assert "type" in schema
        assert schema["type"] == "integer"
        assert "minimum" in schema
        assert "maximum" in schema
        assert "description" in schema


class TestWebFieldsPatterns:
    """Test WebFields pattern matching."""

    def test_host_pattern(self) -> None:
        """Test HOST_PATTERN regex."""
        pattern = WebFields.HOST_PATTERN

        # Valid matches
        valid_hosts = [
            "localhost",
            "127.0.0.1",
            "example.com",
            "sub.example.com"
        ]

        for host in valid_hosts:
            assert pattern.match(host) is not None

        # Invalid matches
        invalid_hosts = [
            "not a host",  # Contains space
            "",  # Empty string
        ]

        for host in invalid_hosts:
            assert pattern.match(host) is None

    def test_url_pattern(self) -> None:
        """Test URL_PATTERN regex."""
        pattern = WebFields.URL_PATTERN

        # Valid matches
        valid_urls = [
            "http://localhost",
            "https://example.com",
            "https://internal.invalid/REDACTED"
        ]

        for url in valid_urls:
            assert pattern.match(url) is not None

        # Invalid matches
        invalid_urls = [
            "ftp://example.com",
            "not-a-url",
            ""
        ]

        for url in invalid_urls:
            assert pattern.match(url) is None


class TestFieldIntegration:
    """Test field integration and edge cases."""

    def test_field_factory_consistency(self) -> None:
        """Test field factories return consistent objects."""
        field1 = WebFields.app_name_field()
        field2 = WebFields.app_name_field()

        # Should have same properties
        assert field1.description == field2.description
        # Both should be FieldInfo objects
        assert type(field1).__name__ == "FieldInfo"
        assert type(field2).__name__ == "FieldInfo"

    def test_validator_error_messages(self) -> None:
        """Test validator error messages are meaningful."""
        with pytest.raises(ValueError, match="Application name cannot be empty"):
            WebFields.validate_app_name("")

        with pytest.raises(ValueError, match="Host address cannot be empty"):
            WebFields.validate_host("")

        with pytest.raises(ValueError, match="Port must be between"):
            WebFields.validate_port(0)

        with pytest.raises(ValueError, match="URL cannot be empty"):
            WebFields.validate_url("")

        with pytest.raises(ValueError, match="Secret key cannot be empty"):
            WebFields.validate_secret_key("")

    def test_field_kwargs_handling(self) -> None:
        """Test fields handle additional kwargs properly."""
        # Test with extra kwargs
        field = WebFields.app_name_field(
            description="Test field",
            alias="app_name",
            examples=["test-app"]
        )

        assert field.description == "Test field"
        # Should not raise errors with additional kwargs


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
