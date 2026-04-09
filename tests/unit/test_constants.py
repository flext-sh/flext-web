"""Unit tests for flext_web.constants module.

Tests the web constants functionality following flext standards.
"""

from __future__ import annotations

from collections.abc import Mapping

from flext_tests import tm

from tests import c


class TestFlextWebConstants:
    """Test suite for c class."""

    def test_web_server_constants(self) -> None:
        """Test web server constants."""
        tm.that(c.Web.WebDefaults.HOST, eq="localhost")
        tm.that(c.Web.WebDefaults.PORT, eq=8080)
        tm.that(c.Web.WebServer.MIN_PORT, eq=1024)
        tm.that(c.Web.WebServer.MAX_PORT, eq=65535)
        tm.that(c.Web.WebServer.MIN_APP_NAME_LENGTH, eq=3)
        tm.that(c.Web.WebServer.MAX_APP_NAME_LENGTH, eq=100)
        tm.that(c.Web.WebServer.MIN_SECRET_KEY_LENGTH, eq=32)

    def test_web_specific_constants(self) -> None:
        """Test web-specific constants."""
        tm.that(c.Web.WebDefaults.HOST, eq="localhost")
        tm.that(c.Web.WebDefaults.PORT, eq=8080)
        tm.that(len(c.Web.WebDefaults.DEV_SECRET_KEY), gte=32)
        tm.that(len(c.Web.WebSpecific.DEV_ENVIRONMENT_KEY), gte=32)
        tm.that(len(c.Web.WebSpecific.TEST_ENVIRONMENT_KEY), gte=32)
        tm.that(c.Web.WebSpecific.ALL_INTERFACES, eq="0.0.0.0")
        tm.that(c.Web.WebSpecific.LOCALHOST_IP, eq="127.0.0.1")
        tm.that(c.Web.WebSpecific.SYSTEM_PORTS_THRESHOLD, eq=1023)
        tm.that(c.Web.WebSpecific.PRIVILEGED_PORTS_MAX, eq=1023)

    def test_web_environment_types(self) -> None:
        """Test web environment type definitions."""

    def test_web_security_constants(self) -> None:
        """Test web security constants."""
        tm.that(c.Web.WebSecurity.CORS_DEFAULT_ORIGINS, is_=tuple)
        tm.that(c.Web.WebSecurity.CORS_DEFAULT_ORIGINS, has="*")
        tm.that(c.Web.WebSecurity.CORS_SAFE_METHODS, is_=tuple)
        tm.that(c.Web.WebSecurity.CORS_SAFE_METHODS, has="GET")
        tm.that(c.Web.WebSecurity.CORS_SAFE_HEADERS, is_=tuple)
        tm.that(c.Web.WebSecurity.CORS_SAFE_HEADERS, has="Content-Type")
        tm.that(c.Web.WebSecurity.SESSION_COOKIE_SECURE_DEFAULT is False, eq=True)
        tm.that(c.Web.WebSecurity.SESSION_COOKIE_HTTPONLY_DEFAULT is True, eq=True)
        tm.that(c.Web.WebSecurity.SESSION_COOKIE_SAMESITE_DEFAULT, eq="Lax")
        tm.that(c.Web.WebSecurity.SSL_ALT_PORT, eq=8443)

    def test_web_validation_constants(self) -> None:
        """Test web validation constants."""
        tm.that(c.Web.WebValidation.MAX_CONTENT_LENGTH_DEFAULT, eq=16 * 1024 * 1024)
        tm.that(c.Web.WebValidation.MIN_CONTENT_LENGTH, eq=0)
        tm.that(c.Web.WebValidation.REQUEST_TIMEOUT_DEFAULT, eq=30)
        tm.that(c.Web.WebValidation.REQUEST_TIMEOUT_MAX, eq=600)
        tm.that(c.Web.WebValidation.MAX_URL_LENGTH, eq=2048)
        tm.that(c.Web.WebValidation.MIN_URL_LENGTH, eq=1)
        tm.that(c.Web.WebValidation.MAX_HEADER_LENGTH, eq=8192)
        tm.that(c.Web.WebValidation.MAX_HEADERS_COUNT, eq=100)

    def test_constants_are_immutable(self) -> None:
        """Test that constants are properly defined and immutable."""
        tm.that(c.Web.WebDefaults.HOST, is_=str)
        tm.that(c.Web.WebDefaults.PORT, is_=int)
        tm.that(c.Web.WebValidation.PORT_RANGE, is_=tuple)
        tm.that(c.Web.WebValidation.NAME_LENGTH_RANGE, is_=tuple)
        tm.that(c.Web.WebServer.MIN_SECRET_KEY_LENGTH, is_=int)

    def test_environment_type_values(self) -> None:
        """Test that environment type values are valid."""
        tm.that(c.Web.Name, none=False)
        tm.that(c.Web.ApplicationType, none=False)
        tm.that(c.Web.Method, none=False)
        tm.that(c.Web.Status, none=False)

    def test_security_constants_types(self) -> None:
        """Test that security constants have correct types."""
        tm.that(c.Web.WebSecurity.MIN_SECRET_KEY_LENGTH, is_=int)
        tm.that(c.Web.WebDefaults.SECRET_KEY, is_=str)
        tm.that(c.Web.WebSecurity.SSL_PORTS, is_=tuple)
        tm.that(c.Web.WebSecurity.SESSION_DEFAULTS, is_=Mapping)

    def test_validation_constants_types(self) -> None:
        """Test that validation constants have correct types."""
        tm.that(c.Web.WebValidation.CONTENT_LENGTH_RANGE, is_=tuple)
        tm.that(c.Web.WebValidation.REQUEST_TIMEOUT_RANGE, is_=tuple)
        tm.that(c.Web.WebValidation.URL_LENGTH_RANGE, is_=tuple)
        tm.that(c.Web.WebValidation.MIN_URL_LENGTH, is_=int)
        tm.that(c.Web.WebValidation.MAX_HEADER_LENGTH, is_=int)
        tm.that(c.Web.WebValidation.MAX_HEADERS_COUNT, is_=int)
