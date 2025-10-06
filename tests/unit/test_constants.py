"""Unit tests for flext_web.constants module.

Tests the web constants functionality following flext standards.
"""

from flext_web.constants import FlextWebConstants


class TestFlextWebConstants:
    """Test suite for FlextWebConstants class."""

    def test_web_server_constants(self) -> None:
        """Test web server constants."""
        assert FlextWebConstants.WebServer.DEFAULT_HOST == "localhost"
        assert FlextWebConstants.WebServer.DEFAULT_PORT == 8080
        assert FlextWebConstants.WebServer.MIN_PORT == 1024
        assert FlextWebConstants.WebServer.MAX_PORT == 65535
        assert FlextWebConstants.WebServer.MIN_APP_NAME_LENGTH == 3
        assert FlextWebConstants.WebServer.MAX_APP_NAME_LENGTH == 100
        assert FlextWebConstants.WebServer.MIN_SECRET_KEY_LENGTH == 32

    def test_web_specific_constants(self) -> None:
        """Test web-specific constants."""
        assert FlextWebConstants.WebSpecific.DEFAULT_HOST == "localhost"
        assert FlextWebConstants.WebSpecific.DEFAULT_PORT == 8080
        assert len(FlextWebConstants.WebSpecific.DEV_SECRET_KEY) >= 32
        assert len(FlextWebConstants.WebSpecific.DEV_ENVIRONMENT_KEY) >= 32
        assert len(FlextWebConstants.WebSpecific.TEST_ENVIRONMENT_KEY) >= 32
        assert FlextWebConstants.WebSpecific.ALL_INTERFACES == "0.0.0.0"
        assert FlextWebConstants.WebSpecific.LOCALHOST_IP == "127.0.0.1"
        assert FlextWebConstants.WebSpecific.SYSTEM_PORTS_THRESHOLD == 1023
        assert FlextWebConstants.WebSpecific.PRIVILEGED_PORTS_MAX == 1023

    def test_web_environment_types(self) -> None:
        """Test web environment type definitions."""
        # Test that the types are properly defined
        assert hasattr(FlextWebConstants.WebEnvironment, "EnvironmentType")
        assert hasattr(FlextWebConstants.WebEnvironment, "WebAppType")
        assert hasattr(FlextWebConstants.WebEnvironment, "HttpMethod")
        assert hasattr(FlextWebConstants.WebEnvironment, "WebStatus")

    def test_web_security_constants(self) -> None:
        """Test web security constants."""
        assert isinstance(FlextWebConstants.WebSecurity.CORS_DEFAULT_ORIGINS, list)
        assert "*" in FlextWebConstants.WebSecurity.CORS_DEFAULT_ORIGINS
        assert isinstance(FlextWebConstants.WebSecurity.CORS_SAFE_METHODS, list)
        assert "GET" in FlextWebConstants.WebSecurity.CORS_SAFE_METHODS
        assert isinstance(FlextWebConstants.WebSecurity.CORS_SAFE_HEADERS, list)
        assert "Content-Type" in FlextWebConstants.WebSecurity.CORS_SAFE_HEADERS
        assert FlextWebConstants.WebSecurity.SESSION_COOKIE_SECURE_DEFAULT is False
        assert FlextWebConstants.WebSecurity.SESSION_COOKIE_HTTPONLY_DEFAULT is True
        assert FlextWebConstants.WebSecurity.SESSION_COOKIE_SAMESITE_DEFAULT == "Lax"
        assert FlextWebConstants.WebSecurity.SSL_DEFAULT_PORT == 443
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
        assert isinstance(FlextWebConstants.WebServer.DEFAULT_HOST, str)
        assert isinstance(FlextWebConstants.WebServer.DEFAULT_PORT, int)
        assert isinstance(FlextWebConstants.WebServer.MIN_PORT, int)
        assert isinstance(FlextWebConstants.WebServer.MAX_PORT, int)
        assert isinstance(FlextWebConstants.WebServer.MIN_APP_NAME_LENGTH, int)
        assert isinstance(FlextWebConstants.WebServer.MAX_APP_NAME_LENGTH, int)
        assert isinstance(FlextWebConstants.WebServer.MIN_SECRET_KEY_LENGTH, int)

    def test_environment_type_values(self) -> None:
        """Test that environment type values are valid."""
        # These would be tested more thoroughly with actual type checking
        # but we can verify the constants exist and are accessible
        env_type = FlextWebConstants.WebEnvironment.EnvironmentType
        assert env_type is not None

        web_app_type = FlextWebConstants.WebEnvironment.WebAppType
        assert web_app_type is not None

        http_method = FlextWebConstants.WebEnvironment.HttpMethod
        assert http_method is not None

        web_status = FlextWebConstants.WebEnvironment.WebStatus
        assert web_status is not None

    def test_security_constants_types(self) -> None:
        """Test that security constants have correct types."""
        assert isinstance(FlextWebConstants.WebSecurity.CORS_DEFAULT_ORIGINS, list)
        assert all(
            isinstance(origin, str)
            for origin in FlextWebConstants.WebSecurity.CORS_DEFAULT_ORIGINS
        )
        assert isinstance(FlextWebConstants.WebSecurity.CORS_SAFE_METHODS, list)
        assert all(
            isinstance(method, str)
            for method in FlextWebConstants.WebSecurity.CORS_SAFE_METHODS
        )
        assert isinstance(FlextWebConstants.WebSecurity.CORS_SAFE_HEADERS, list)
        assert all(
            isinstance(header, str)
            for header in FlextWebConstants.WebSecurity.CORS_SAFE_HEADERS
        )
        assert isinstance(
            FlextWebConstants.WebSecurity.SESSION_COOKIE_SECURE_DEFAULT, bool
        )
        assert isinstance(
            FlextWebConstants.WebSecurity.SESSION_COOKIE_HTTPONLY_DEFAULT, bool
        )
        assert isinstance(
            FlextWebConstants.WebSecurity.SESSION_COOKIE_SAMESITE_DEFAULT, str
        )
        assert isinstance(FlextWebConstants.WebSecurity.SSL_DEFAULT_PORT, int)
        assert isinstance(FlextWebConstants.WebSecurity.SSL_ALT_PORT, int)

    def test_validation_constants_types(self) -> None:
        """Test that validation constants have correct types."""
        assert isinstance(
            FlextWebConstants.WebValidation.MAX_CONTENT_LENGTH_DEFAULT, int
        )
        assert isinstance(FlextWebConstants.WebValidation.MIN_CONTENT_LENGTH, int)
        assert isinstance(FlextWebConstants.WebValidation.REQUEST_TIMEOUT_DEFAULT, int)
        assert isinstance(FlextWebConstants.WebValidation.REQUEST_TIMEOUT_MAX, int)
        assert isinstance(FlextWebConstants.WebValidation.MAX_URL_LENGTH, int)
        assert isinstance(FlextWebConstants.WebValidation.MIN_URL_LENGTH, int)
        assert isinstance(FlextWebConstants.WebValidation.MAX_HEADER_LENGTH, int)
        assert isinstance(FlextWebConstants.WebValidation.MAX_HEADERS_COUNT, int)
