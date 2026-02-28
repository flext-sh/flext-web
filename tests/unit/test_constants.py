"""Unit tests for flext_web.constants module.

Tests the web constants functionality following flext standards.
"""

from collections.abc import Mapping

from flext_web import FlextWebConstants


class TestFlextWebConstants:
    """Test suite for FlextWebConstants class."""

    def test_web_server_constants(self) -> None:
        """Test web server constants."""
        assert FlextWebConstants.Web.WebDefaults.HOST == "localhost"
        assert FlextWebConstants.Web.WebDefaults.PORT == 8080
        assert FlextWebConstants.Web.WebServer.MIN_PORT == 1024
        assert FlextWebConstants.Web.WebServer.MAX_PORT == 65535
        assert FlextWebConstants.Web.WebServer.MIN_APP_NAME_LENGTH == 3
        assert FlextWebConstants.Web.WebServer.MAX_APP_NAME_LENGTH == 100
        assert FlextWebConstants.Web.WebServer.MIN_SECRET_KEY_LENGTH == 32

    def test_web_specific_constants(self) -> None:
        """Test web-specific constants."""
        assert FlextWebConstants.Web.WebDefaults.HOST == "localhost"
        assert FlextWebConstants.Web.WebDefaults.PORT == 8080
        assert len(FlextWebConstants.Web.WebDefaults.DEV_SECRET_KEY) >= 32
        assert len(FlextWebConstants.Web.WebSpecific.DEV_ENVIRONMENT_KEY) >= 32
        assert len(FlextWebConstants.Web.WebSpecific.TEST_ENVIRONMENT_KEY) >= 32
        assert FlextWebConstants.Web.WebSpecific.ALL_INTERFACES == "0.0.0.0"
        assert FlextWebConstants.Web.WebSpecific.LOCALHOST_IP == "127.0.0.1"
        assert FlextWebConstants.Web.WebSpecific.SYSTEM_PORTS_THRESHOLD == 1023
        assert FlextWebConstants.Web.WebSpecific.PRIVILEGED_PORTS_MAX == 1023

    def test_web_environment_types(self) -> None:
        """Test web environment type definitions."""
        # Test that the types are properly defined under Web namespace
        assert hasattr(FlextWebConstants.Web, "Name")
        assert hasattr(FlextWebConstants.Web, "ApplicationType")
        assert hasattr(FlextWebConstants.Web, "Method")
        assert hasattr(FlextWebConstants.Web, "Status")

    def test_web_security_constants(self) -> None:
        """Test web security constants."""
        assert isinstance(FlextWebConstants.Web.WebSecurity.CORS_DEFAULT_ORIGINS, tuple)
        assert "*" in FlextWebConstants.Web.WebSecurity.CORS_DEFAULT_ORIGINS
        assert isinstance(FlextWebConstants.Web.WebSecurity.CORS_SAFE_METHODS, tuple)
        assert "GET" in FlextWebConstants.Web.WebSecurity.CORS_SAFE_METHODS
        assert isinstance(FlextWebConstants.Web.WebSecurity.CORS_SAFE_HEADERS, tuple)
        assert "Content-Type" in FlextWebConstants.Web.WebSecurity.CORS_SAFE_HEADERS
        assert FlextWebConstants.Web.WebSecurity.SESSION_COOKIE_SECURE_DEFAULT is False
        assert FlextWebConstants.Web.WebSecurity.SESSION_COOKIE_HTTPONLY_DEFAULT is True
        assert (
            FlextWebConstants.Web.WebSecurity.SESSION_COOKIE_SAMESITE_DEFAULT == "Lax"
        )
        assert FlextWebConstants.Web.WebSecurity.SSL_ALT_PORT == 8443

    def test_web_validation_constants(self) -> None:
        """Test web validation constants."""
        assert (
            FlextWebConstants.Web.WebValidation.MAX_CONTENT_LENGTH_DEFAULT
            == 16 * 1024 * 1024
        )
        assert FlextWebConstants.Web.WebValidation.MIN_CONTENT_LENGTH == 0
        assert FlextWebConstants.Web.WebValidation.REQUEST_TIMEOUT_DEFAULT == 30
        assert FlextWebConstants.Web.WebValidation.REQUEST_TIMEOUT_MAX == 600
        assert FlextWebConstants.Web.WebValidation.MAX_URL_LENGTH == 2048
        assert FlextWebConstants.Web.WebValidation.MIN_URL_LENGTH == 1
        assert FlextWebConstants.Web.WebValidation.MAX_HEADER_LENGTH == 8192
        assert FlextWebConstants.Web.WebValidation.MAX_HEADERS_COUNT == 100

    def test_constants_are_immutable(self) -> None:
        """Test that constants are properly defined and immutable."""
        # Test that we can access the constants without errors
        assert isinstance(FlextWebConstants.Web.WebDefaults.HOST, str)
        assert isinstance(FlextWebConstants.Web.WebDefaults.PORT, int)
        assert isinstance(FlextWebConstants.Web.WebValidation.PORT_RANGE, tuple)
        assert isinstance(FlextWebConstants.Web.WebValidation.NAME_LENGTH_RANGE, tuple)
        assert isinstance(FlextWebConstants.Web.WebServer.MIN_SECRET_KEY_LENGTH, int)

    def test_environment_type_values(self) -> None:
        """Test that environment type values are valid."""
        # Test that the type literals exist and are accessible
        assert FlextWebConstants.Web.Name is not None
        assert FlextWebConstants.Web.ApplicationType is not None
        assert FlextWebConstants.Web.Method is not None
        assert FlextWebConstants.Web.Status is not None

    def test_security_constants_types(self) -> None:
        """Test that security constants have correct types."""
        # Test the actual constants that exist
        assert isinstance(FlextWebConstants.Web.WebSecurity.MIN_SECRET_KEY_LENGTH, int)
        assert isinstance(FlextWebConstants.Web.WebDefaults.SECRET_KEY, str)
        assert isinstance(FlextWebConstants.Web.WebSecurity.SSL_PORTS, tuple)
        assert isinstance(FlextWebConstants.Web.WebSecurity.SESSION_DEFAULTS, Mapping)

    def test_validation_constants_types(self) -> None:
        """Test that validation constants have correct types."""
        # Test the actual constants that exist
        assert isinstance(
            FlextWebConstants.Web.WebValidation.CONTENT_LENGTH_RANGE, tuple
        )
        assert isinstance(
            FlextWebConstants.Web.WebValidation.REQUEST_TIMEOUT_RANGE, tuple
        )
        assert isinstance(FlextWebConstants.Web.WebValidation.URL_LENGTH_RANGE, tuple)
        assert isinstance(FlextWebConstants.Web.WebValidation.MIN_URL_LENGTH, int)
        assert isinstance(FlextWebConstants.Web.WebValidation.MAX_HEADER_LENGTH, int)
        assert isinstance(FlextWebConstants.Web.WebValidation.MAX_HEADERS_COUNT, int)
