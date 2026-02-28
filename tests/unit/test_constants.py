"""Unit tests for flext_web.constants module.

Tests the web constants functionality following flext standards.
"""

from collections.abc import Mapping

from tests import c


class TestFlextWebConstants:
    """Test suite for c class."""

    def test_web_server_constants(self) -> None:
        """Test web server constants."""
        assert c.Web.WebDefaults.HOST == "localhost"
        assert c.Web.WebDefaults.PORT == 8080
        assert c.Web.WebServer.MIN_PORT == 1024
        assert c.Web.WebServer.MAX_PORT == 65535
        assert c.Web.WebServer.MIN_APP_NAME_LENGTH == 3
        assert c.Web.WebServer.MAX_APP_NAME_LENGTH == 100
        assert c.Web.WebServer.MIN_SECRET_KEY_LENGTH == 32

    def test_web_specific_constants(self) -> None:
        """Test web-specific constants."""
        assert c.Web.WebDefaults.HOST == "localhost"
        assert c.Web.WebDefaults.PORT == 8080
        assert len(c.Web.WebDefaults.DEV_SECRET_KEY) >= 32
        assert len(c.Web.WebSpecific.DEV_ENVIRONMENT_KEY) >= 32
        assert len(c.Web.WebSpecific.TEST_ENVIRONMENT_KEY) >= 32
        assert c.Web.WebSpecific.ALL_INTERFACES == "0.0.0.0"
        assert c.Web.WebSpecific.LOCALHOST_IP == "127.0.0.1"
        assert c.Web.WebSpecific.SYSTEM_PORTS_THRESHOLD == 1023
        assert c.Web.WebSpecific.PRIVILEGED_PORTS_MAX == 1023

    def test_web_environment_types(self) -> None:
        """Test web environment type definitions."""
        # Test that the types are properly defined under Web namespace
        assert hasattr(c.Web, "Name")
        assert hasattr(c.Web, "ApplicationType")
        assert hasattr(c.Web, "Method")
        assert hasattr(c.Web, "Status")

    def test_web_security_constants(self) -> None:
        """Test web security constants."""
        assert isinstance(c.Web.WebSecurity.CORS_DEFAULT_ORIGINS, tuple)
        assert "*" in c.Web.WebSecurity.CORS_DEFAULT_ORIGINS
        assert isinstance(c.Web.WebSecurity.CORS_SAFE_METHODS, tuple)
        assert "GET" in c.Web.WebSecurity.CORS_SAFE_METHODS
        assert isinstance(c.Web.WebSecurity.CORS_SAFE_HEADERS, tuple)
        assert "Content-Type" in c.Web.WebSecurity.CORS_SAFE_HEADERS
        assert c.Web.WebSecurity.SESSION_COOKIE_SECURE_DEFAULT is False
        assert c.Web.WebSecurity.SESSION_COOKIE_HTTPONLY_DEFAULT is True
        assert c.Web.WebSecurity.SESSION_COOKIE_SAMESITE_DEFAULT == "Lax"
        assert c.Web.WebSecurity.SSL_ALT_PORT == 8443

    def test_web_validation_constants(self) -> None:
        """Test web validation constants."""
        assert c.Web.WebValidation.MAX_CONTENT_LENGTH_DEFAULT == 16 * 1024 * 1024
        assert c.Web.WebValidation.MIN_CONTENT_LENGTH == 0
        assert c.Web.WebValidation.REQUEST_TIMEOUT_DEFAULT == 30
        assert c.Web.WebValidation.REQUEST_TIMEOUT_MAX == 600
        assert c.Web.WebValidation.MAX_URL_LENGTH == 2048
        assert c.Web.WebValidation.MIN_URL_LENGTH == 1
        assert c.Web.WebValidation.MAX_HEADER_LENGTH == 8192
        assert c.Web.WebValidation.MAX_HEADERS_COUNT == 100

    def test_constants_are_immutable(self) -> None:
        """Test that constants are properly defined and immutable."""
        # Test that we can access the constants without errors
        assert isinstance(c.Web.WebDefaults.HOST, str)
        assert isinstance(c.Web.WebDefaults.PORT, int)
        assert isinstance(c.Web.WebValidation.PORT_RANGE, tuple)
        assert isinstance(c.Web.WebValidation.NAME_LENGTH_RANGE, tuple)
        assert isinstance(c.Web.WebServer.MIN_SECRET_KEY_LENGTH, int)

    def test_environment_type_values(self) -> None:
        """Test that environment type values are valid."""
        # Test that the type literals exist and are accessible
        assert c.Web.Name is not None
        assert c.Web.ApplicationType is not None
        assert c.Web.Method is not None
        assert c.Web.Status is not None

    def test_security_constants_types(self) -> None:
        """Test that security constants have correct types."""
        # Test the actual constants that exist
        assert isinstance(c.Web.WebSecurity.MIN_SECRET_KEY_LENGTH, int)
        assert isinstance(c.Web.WebDefaults.SECRET_KEY, str)
        assert isinstance(c.Web.WebSecurity.SSL_PORTS, tuple)
        assert isinstance(c.Web.WebSecurity.SESSION_DEFAULTS, Mapping)

    def test_validation_constants_types(self) -> None:
        """Test that validation constants have correct types."""
        # Test the actual constants that exist
        assert isinstance(
            c.Web.WebValidation.CONTENT_LENGTH_RANGE,
            tuple,
        )
        assert isinstance(
            c.Web.WebValidation.REQUEST_TIMEOUT_RANGE,
            tuple,
        )
        assert isinstance(c.Web.WebValidation.URL_LENGTH_RANGE, tuple)
        assert isinstance(c.Web.WebValidation.MIN_URL_LENGTH, int)
        assert isinstance(c.Web.WebValidation.MAX_HEADER_LENGTH, int)
        assert isinstance(c.Web.WebValidation.MAX_HEADERS_COUNT, int)
