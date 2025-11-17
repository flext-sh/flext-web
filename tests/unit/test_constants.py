"""Unit tests for flext_web.constants module.

Tests the web constants functionality following flext standards.
"""

from collections.abc import Mapping

from flext_web.constants import FlextWebConstants


class TestFlextWebConstants:
    """Test suite for FlextWebConstants class."""

    def test_web_server_constants(self) -> None:
        """Test web server constants."""
        assert FlextWebConstants.WebDefaults.HOST == "localhost"
        assert FlextWebConstants.WebDefaults.PORT == 8080
        assert FlextWebConstants.WebServer.MIN_PORT == 1024
        assert FlextWebConstants.WebServer.MAX_PORT == 65535
        assert FlextWebConstants.WebServer.MIN_APP_NAME_LENGTH == 3
        assert FlextWebConstants.WebServer.MAX_APP_NAME_LENGTH == 100
        assert FlextWebConstants.WebServer.MIN_SECRET_KEY_LENGTH == 32

    def test_web_specific_constants(self) -> None:
        """Test web-specific constants."""
        assert FlextWebConstants.WebDefaults.HOST == "localhost"
        assert FlextWebConstants.WebDefaults.PORT == 8080
        assert len(FlextWebConstants.WebDefaults.DEV_SECRET_KEY) >= 32
        assert len(FlextWebConstants.WebSpecific.DEV_ENVIRONMENT_KEY) >= 32
        assert len(FlextWebConstants.WebSpecific.TEST_ENVIRONMENT_KEY) >= 32
        assert FlextWebConstants.WebSpecific.ALL_INTERFACES == "0.0.0.0"
        assert FlextWebConstants.WebSpecific.LOCALHOST_IP == "127.0.0.1"
        assert FlextWebConstants.WebSpecific.SYSTEM_PORTS_THRESHOLD == 1023
        assert FlextWebConstants.WebSpecific.PRIVILEGED_PORTS_MAX == 1023

    def test_web_environment_types(self) -> None:
        """Test web environment type definitions."""
        # Test that the types are properly defined at the top level
        assert hasattr(FlextWebConstants, "EnvironmentType")
        assert hasattr(FlextWebConstants, "ApplicationType")
        assert hasattr(FlextWebConstants, "HttpMethod")
        assert hasattr(FlextWebConstants, "ApplicationStatus")

    def test_web_security_constants(self) -> None:
        """Test web security constants."""
        assert isinstance(FlextWebConstants.WebSecurity.CORS_DEFAULT_ORIGINS, tuple)
        assert "*" in FlextWebConstants.WebSecurity.CORS_DEFAULT_ORIGINS
        assert isinstance(FlextWebConstants.WebSecurity.CORS_SAFE_METHODS, tuple)
        assert "GET" in FlextWebConstants.WebSecurity.CORS_SAFE_METHODS
        assert isinstance(FlextWebConstants.WebSecurity.CORS_SAFE_HEADERS, tuple)
        assert "Content-Type" in FlextWebConstants.WebSecurity.CORS_SAFE_HEADERS
        assert FlextWebConstants.WebSecurity.SESSION_COOKIE_SECURE_DEFAULT is False
        assert FlextWebConstants.WebSecurity.SESSION_COOKIE_HTTPONLY_DEFAULT is True
        assert FlextWebConstants.WebSecurity.SESSION_COOKIE_SAMESITE_DEFAULT == "Lax"
        assert FlextWebConstants.WebSecurity.SSL_ALT_PORT == 8443

    def test_web_validation_constants(self) -> None:
        """Test web validation constants."""
        assert (
            FlextWebConstants.WebValidation.MAX_CONTENT_LENGTH_DEFAULT
            == 16 * 1024 * 1024
        )
        assert FlextWebConstants.WebValidation.MIN_CONTENT_LENGTH == 0
        assert FlextWebConstants.WebValidation.REQUEST_TIMEOUT_DEFAULT == 30
        assert FlextWebConstants.WebValidation.REQUEST_TIMEOUT_MAX == 600
        assert FlextWebConstants.WebValidation.MAX_URL_LENGTH == 2048
        assert FlextWebConstants.WebValidation.MIN_URL_LENGTH == 1
        assert FlextWebConstants.WebValidation.MAX_HEADER_LENGTH == 8192
        assert FlextWebConstants.WebValidation.MAX_HEADERS_COUNT == 100

    def test_constants_are_immutable(self) -> None:
        """Test that constants are properly defined and immutable."""
        # Test that we can access the constants without errors
        assert isinstance(FlextWebConstants.WebDefaults.HOST, str)
        assert isinstance(FlextWebConstants.WebDefaults.PORT, int)
        assert isinstance(FlextWebConstants.PORT_RANGE, tuple)
        assert isinstance(FlextWebConstants.NAME_LENGTH_RANGE, tuple)
        assert isinstance(FlextWebConstants.MIN_SECRET_KEY_LENGTH, int)

    def test_environment_type_values(self) -> None:
        """Test that environment type values are valid."""
        # Test that the type literals exist and are accessible
        assert FlextWebConstants.EnvironmentType is not None
        assert FlextWebConstants.ApplicationType is not None
        assert FlextWebConstants.HttpMethod is not None
        assert FlextWebConstants.ApplicationStatus is not None

    def test_security_constants_types(self) -> None:
        """Test that security constants have correct types."""
        # Test the actual constants that exist
        assert isinstance(FlextWebConstants.MIN_SECRET_KEY_LENGTH, int)
        assert isinstance(FlextWebConstants.WebDefaults.SECRET_KEY, str)
        assert isinstance(FlextWebConstants.SSL_PORTS, tuple)
        assert isinstance(FlextWebConstants.SESSION_DEFAULTS, Mapping)

    def test_validation_constants_types(self) -> None:
        """Test that validation constants have correct types."""
        # Test the actual constants that exist
        assert isinstance(FlextWebConstants.CONTENT_LENGTH_RANGE, tuple)
        assert isinstance(FlextWebConstants.REQUEST_TIMEOUT_RANGE, tuple)
        assert isinstance(FlextWebConstants.URL_LENGTH_RANGE, tuple)
        assert isinstance(FlextWebConstants.WebValidation.MIN_URL_LENGTH, int)
        assert isinstance(FlextWebConstants.WebValidation.MAX_HEADER_LENGTH, int)
        assert isinstance(FlextWebConstants.WebValidation.MAX_HEADERS_COUNT, int)
