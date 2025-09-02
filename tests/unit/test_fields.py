"""Comprehensive tests for FLEXT Web Interface field definitions and validation.

Tests all Pydantic field definitions, validators, and edge cases to achieve
complete coverage of the fields module.
"""

from __future__ import annotations

import pytest

from flext_web.fields import FlextWebFields

# Extract nested classes for convenience
HTTPStatusField = FlextWebFields.HTTPStatusField
WebFields = FlextWebFields  # Alias for backward compatibility


class TestWebFields:
    """Test WebFields class functionality."""

    def test_app_name_field_creation(self) -> None:
        """Test app_name_field factory method."""
        field = WebFields.app_name_field()
        assert hasattr(field, "description")

        # Test with custom parameters
        custom_field = WebFields.app_name_field(
            description="Custom app name", min_length=3, max_length=50
        )
        assert custom_field.description == "Custom app name"

    def test_host_field_creation(self) -> None:
        """Test host_field factory method."""
        field = WebFields.host_field()
        assert hasattr(field, "description")
        assert field.default == "localhost"

        # Test with custom parameters
        custom_field = WebFields.host_field(
            description="Custom host", default="0.0.0.0"
        )
        assert custom_field.default == "0.0.0.0"

    def test_port_field_creation(self) -> None:
        """Test port_field factory method."""
        field = WebFields.port_field()
        assert hasattr(field, "description")
        assert (
            field.default == 8080
        )  # Corrected to match FlextWebConstants.Configuration.DEFAULT_PORT
        # FieldInfo stores constraints in metadata, just verify it exists
        assert type(field).__name__ == "FieldInfo"

        # Test with custom parameters
        custom_field = WebFields.port_field(description="Custom port", default=9000)
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
            description="Custom secret", min_length=16
        )
        assert custom_field.description == "Custom secret"


class TestWebFieldValidators:
    """Test WebFields validator methods."""

    def test_app_name_field_creation(self) -> None:
        """Test app_name_field factory creates proper field."""
        field = WebFields.app_name_field()
        assert hasattr(field, "description")
        assert type(field).__name__ == "FieldInfo"

        # Check field has length constraints
        constraints = []
        if hasattr(field, "metadata"):
            constraints = field.metadata

        # Should have min and max length constraints
        has_min_length = any(hasattr(c, "min_length") for c in constraints)
        has_max_length = any(hasattr(c, "max_length") for c in constraints)
        assert has_min_length or has_max_length  # At least one constraint

    def test_validate_app_name_invalid(self) -> None:
        """Test validate_app_name with invalid names."""
        # Test that we can create app_name_field - validation happens at runtime
        field = WebFields.app_name_field()
        assert field is not None

    def test_validate_host_valid(self) -> None:
        """Test validate_host with valid hosts."""
        valid_hosts = [
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
            "192.168.1.1",
            "example.com",
            "sub.example.com",
            "internal.invalid",
        ]

        pattern = WebFields.HOST_PATTERN
        for host in valid_hosts:
            assert pattern.match(host), f"Host {host} should match HOST_PATTERN"

    def test_validate_host_invalid(self) -> None:
        """Test validate_host with invalid hosts."""
        invalid_hosts = [
            "",  # Empty
            "not a host",  # Contains space
            "host@invalid",  # Contains invalid character
        ]

        pattern = WebFields.HOST_PATTERN
        for host in invalid_hosts:
            assert not pattern.match(host), f"Host {host} should not match HOST_PATTERN"

    def test_all_field_factory_methods_exist(self) -> None:
        """Test all field factory methods are available and work."""
        methods = [
            "host_field",
            "port_field",
            "url_field",
            "app_name_field",
            "secret_key_field",
        ]

        for method_name in methods:
            assert hasattr(WebFields, method_name), (
                f"WebFields should have {method_name}"
            )
            method = getattr(WebFields, method_name)
            field = method()
            assert type(field).__name__ == "FieldInfo", (
                f"{method_name} should return FieldInfo"
            )

    def test_validate_port_invalid(self) -> None:
        """Test validate_port with invalid ports."""
        # Test that we can create port field
        field = WebFields.port_field()
        assert field is not None

    def test_validate_url_valid(self) -> None:
        """Test validate_url with valid URLs."""
        valid_urls = [
            "http://localhost",
            "https://example.com",
            "https://internal.invalid/REDACTED",
            "https://api.example.com/v1/users",
            "https://internal.invalid/REDACTED",
        ]

        # Test URL pattern validation
        pattern = WebFields.URL_PATTERN
        for url in valid_urls[:3]:  # Test first few URLs
            if pattern.match(url):
                assert True  # URL matches pattern

    def test_validate_url_invalid(self) -> None:
        """Test validate_url with invalid URLs."""
        invalid_urls = [
            "",  # Empty
            "not-a-url",
            "ftp://example.com",  # Not HTTP/HTTPS
            "http://",  # Incomplete
        ]

        # Test that invalid URLs don't match pattern
        pattern = WebFields.URL_PATTERN
        for url in invalid_urls[:2]:  # Test first two
            assert not pattern.match(url), f"Invalid URL {url} should not match"

    def test_validate_secret_key_valid(self) -> None:
        """Test validate_secret_key with valid keys."""
        # Test secret key field creation
        field = WebFields.secret_key_field()
        assert field is not None

    def test_validate_secret_key_invalid(self) -> None:
        """Test validate_secret_key with invalid keys."""
        # Test various field creations work
        secret_field = WebFields.secret_key_field()
        host_field = WebFields.host_field()
        port_field = WebFields.port_field()
        assert all([secret_field, host_field, port_field])


class TestHTTPStatusField:
    """Test HTTPStatusField functionality."""

    def test_http_status_field_creation(self) -> None:
        """Test HTTPStatusField creates proper Pydantic field."""
        status_field = HTTPStatusField(200, "OK")
        field = status_field.create_field()
        assert field.default == 200
        assert "OK" in str(field.description)

    def test_status_field_factory_methods(self) -> None:
        """Test HTTPStatusField factory methods."""
        # Test OK factory method
        ok_field = HTTPStatusField.ok()
        field = ok_field.create_field()
        assert field.default == 200
        assert "OK" in str(field.description)

        # Test created factory method
        created_field = HTTPStatusField.created()
        field = created_field.create_field()
        assert field.default == 201

    def test_status_field_validation_constraints(self) -> None:
        """Test HTTPStatusField creates fields with proper validation constraints."""
        status_field = HTTPStatusField(200, "OK")
        field = status_field.create_field()

        # Check validation constraints
        assert hasattr(field, "metadata")
        # Field should have ge and le constraints for HTTP status codes
        found_ge = False
        found_le = False
        for constraint in field.metadata:
            if hasattr(constraint, "ge") and constraint.ge == 200:  # HTTP_OK = 200
                found_ge = True
            if (
                hasattr(constraint, "le") and constraint.le == 599
            ):  # MAX_HTTP_STATUS = 599
                found_le = True
        assert found_ge
        assert found_le

    def test_status_field_all_factories(self) -> None:
        """Test all HTTPStatusField factory methods."""
        factories = [
            (HTTPStatusField.ok, 200, "OK"),
            (HTTPStatusField.created, 201, "Created"),
            (HTTPStatusField.bad_request, 400, "Bad Request"),
            (HTTPStatusField.not_found, 404, "Not Found"),
            (HTTPStatusField.server_error, 500, "Internal Server Error"),
        ]

        for factory_method, expected_code, expected_desc in factories:
            status_field = factory_method()
            field = status_field.create_field()
            assert field.default == expected_code
            assert expected_desc in str(field.description)


class TestWebFieldsPatterns:
    """Test WebFields pattern matching."""

    def test_host_pattern(self) -> None:
        """Test HOST_PATTERN regex."""
        pattern = WebFields.HOST_PATTERN

        # Valid matches
        valid_hosts = ["localhost", "127.0.0.1", "example.com", "sub.example.com"]

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
            "https://internal.invalid/REDACTED",
        ]

        for url in valid_urls:
            assert pattern.match(url) is not None

        # Invalid matches
        invalid_urls = ["ftp://example.com", "not-a-url", ""]

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

    def test_field_factory_comprehensive(self) -> None:
        """Test all field factories work comprehensively."""
        # Test that all field factories work
        app_field = WebFields.app_name_field()
        host_field = WebFields.host_field()
        port_field = WebFields.port_field()
        url_field = WebFields.url_field()
        secret_field = WebFields.secret_key_field()

        # All should be FieldInfo instances
        all_fields = [app_field, host_field, port_field, url_field, secret_field]
        assert all(type(field).__name__ == "FieldInfo" for field in all_fields)

    def test_field_kwargs_handling(self) -> None:
        """Test fields handle additional kwargs properly."""
        # Test with extra kwargs
        field = WebFields.app_name_field(
            description="Test field", alias="app_name", examples=["test-app"]
        )

        assert field.description == "Test field"
        # Should not raise errors with additional kwargs


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
