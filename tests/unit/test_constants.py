"""Unit tests for flext_web.constants module.

Tests the web constants functionality following flext standards.
"""

from __future__ import annotations

from collections.abc import Mapping

from flext_tests import c, u

from tests import c


class TestFlextWebConstants:
    """Test suite for c class."""

    def test_web_server_constants(self) -> None:
        """Test web server constants."""
        u.Tests.Matchers.that(c.Web.WebDefaults.HOST, eq="localhost")
        u.Tests.Matchers.that(c.Web.WebDefaults.PORT, eq=8080)
        u.Tests.Matchers.that(c.Web.WebServer.MIN_PORT, eq=1024)
        u.Tests.Matchers.that(c.Web.WebServer.MAX_PORT, eq=65535)
        u.Tests.Matchers.that(c.Web.WebServer.MIN_APP_NAME_LENGTH, eq=3)
        u.Tests.Matchers.that(c.Web.WebServer.MAX_APP_NAME_LENGTH, eq=100)
        u.Tests.Matchers.that(c.Web.WebServer.MIN_SECRET_KEY_LENGTH, eq=32)

    def test_web_specific_constants(self) -> None:
        """Test web-specific constants."""
        u.Tests.Matchers.that(c.Web.WebDefaults.HOST, eq="localhost")
        u.Tests.Matchers.that(c.Web.WebDefaults.PORT, eq=8080)
        u.Tests.Matchers.that(len(c.Web.WebDefaults.DEV_SECRET_KEY) >= 32, eq=True)
        u.Tests.Matchers.that(len(c.Web.WebSpecific.DEV_ENVIRONMENT_KEY) >= 32, eq=True)
        u.Tests.Matchers.that(
            len(c.Web.WebSpecific.TEST_ENVIRONMENT_KEY) >= 32, eq=True
        )
        u.Tests.Matchers.that(c.Web.WebSpecific.ALL_INTERFACES, eq="0.0.0.0")
        u.Tests.Matchers.that(c.Web.WebSpecific.LOCALHOST_IP, eq="127.0.0.1")
        u.Tests.Matchers.that(c.Web.WebSpecific.SYSTEM_PORTS_THRESHOLD, eq=1023)
        u.Tests.Matchers.that(c.Web.WebSpecific.PRIVILEGED_PORTS_MAX, eq=1023)

    def test_web_environment_types(self) -> None:
        """Test web environment type definitions."""
        u.Tests.Matchers.that(hasattr(c.Web, "Name"), eq=True)
        u.Tests.Matchers.that(hasattr(c.Web, "ApplicationType"), eq=True)
        u.Tests.Matchers.that(hasattr(c.Web, "Method"), eq=True)
        u.Tests.Matchers.that(hasattr(c.Web, "Status"), eq=True)

    def test_web_security_constants(self) -> None:
        """Test web security constants."""
        u.Tests.Matchers.that(
            isinstance(c.Web.WebSecurity.CORS_DEFAULT_ORIGINS, tuple), eq=True
        )
        u.Tests.Matchers.that("*" in c.Web.WebSecurity.CORS_DEFAULT_ORIGINS, eq=True)
        u.Tests.Matchers.that(
            isinstance(c.Web.WebSecurity.CORS_SAFE_METHODS, tuple), eq=True
        )
        u.Tests.Matchers.that("GET" in c.Web.WebSecurity.CORS_SAFE_METHODS, eq=True)
        u.Tests.Matchers.that(
            isinstance(c.Web.WebSecurity.CORS_SAFE_HEADERS, tuple), eq=True
        )
        u.Tests.Matchers.that(
            "Content-Type" in c.Web.WebSecurity.CORS_SAFE_HEADERS, eq=True
        )
        u.Tests.Matchers.that(
            c.Web.WebSecurity.SESSION_COOKIE_SECURE_DEFAULT is False, eq=True
        )
        u.Tests.Matchers.that(
            c.Web.WebSecurity.SESSION_COOKIE_HTTPONLY_DEFAULT is True, eq=True
        )
        u.Tests.Matchers.that(
            c.Web.WebSecurity.SESSION_COOKIE_SAMESITE_DEFAULT, eq="Lax"
        )
        u.Tests.Matchers.that(c.Web.WebSecurity.SSL_ALT_PORT, eq=8443)

    def test_web_validation_constants(self) -> None:
        """Test web validation constants."""
        u.Tests.Matchers.that(
            c.Web.WebValidation.MAX_CONTENT_LENGTH_DEFAULT, eq=16 * 1024 * 1024
        )
        u.Tests.Matchers.that(c.Web.WebValidation.MIN_CONTENT_LENGTH, eq=0)
        u.Tests.Matchers.that(c.Web.WebValidation.REQUEST_TIMEOUT_DEFAULT, eq=30)
        u.Tests.Matchers.that(c.Web.WebValidation.REQUEST_TIMEOUT_MAX, eq=600)
        u.Tests.Matchers.that(c.Web.WebValidation.MAX_URL_LENGTH, eq=2048)
        u.Tests.Matchers.that(c.Web.WebValidation.MIN_URL_LENGTH, eq=1)
        u.Tests.Matchers.that(c.Web.WebValidation.MAX_HEADER_LENGTH, eq=8192)
        u.Tests.Matchers.that(c.Web.WebValidation.MAX_HEADERS_COUNT, eq=100)

    def test_constants_are_immutable(self) -> None:
        """Test that constants are properly defined and immutable."""
        u.Tests.Matchers.that(isinstance(c.Web.WebDefaults.HOST, str), eq=True)
        u.Tests.Matchers.that(isinstance(c.Web.WebDefaults.PORT, int), eq=True)
        u.Tests.Matchers.that(
            isinstance(c.Web.WebValidation.PORT_RANGE, tuple), eq=True
        )
        u.Tests.Matchers.that(
            isinstance(c.Web.WebValidation.NAME_LENGTH_RANGE, tuple), eq=True
        )
        u.Tests.Matchers.that(
            isinstance(c.Web.WebServer.MIN_SECRET_KEY_LENGTH, int), eq=True
        )

    def test_environment_type_values(self) -> None:
        """Test that environment type values are valid."""
        u.Tests.Matchers.that(c.Web.Name is not None, eq=True)
        u.Tests.Matchers.that(c.Web.ApplicationType is not None, eq=True)
        u.Tests.Matchers.that(c.Web.Method is not None, eq=True)
        u.Tests.Matchers.that(c.Web.Status is not None, eq=True)

    def test_security_constants_types(self) -> None:
        """Test that security constants have correct types."""
        u.Tests.Matchers.that(
            isinstance(c.Web.WebSecurity.MIN_SECRET_KEY_LENGTH, int), eq=True
        )
        u.Tests.Matchers.that(isinstance(c.Web.WebDefaults.SECRET_KEY, str), eq=True)
        u.Tests.Matchers.that(isinstance(c.Web.WebSecurity.SSL_PORTS, tuple), eq=True)
        u.Tests.Matchers.that(
            isinstance(c.Web.WebSecurity.SESSION_DEFAULTS, Mapping), eq=True
        )

    def test_validation_constants_types(self) -> None:
        """Test that validation constants have correct types."""
        u.Tests.Matchers.that(
            isinstance(c.Web.WebValidation.CONTENT_LENGTH_RANGE, tuple), eq=True
        )
        u.Tests.Matchers.that(
            isinstance(c.Web.WebValidation.REQUEST_TIMEOUT_RANGE, tuple), eq=True
        )
        u.Tests.Matchers.that(
            isinstance(c.Web.WebValidation.URL_LENGTH_RANGE, tuple), eq=True
        )
        u.Tests.Matchers.that(
            isinstance(c.Web.WebValidation.MIN_URL_LENGTH, int), eq=True
        )
        u.Tests.Matchers.that(
            isinstance(c.Web.WebValidation.MAX_HEADER_LENGTH, int), eq=True
        )
        u.Tests.Matchers.that(
            isinstance(c.Web.WebValidation.MAX_HEADERS_COUNT, int), eq=True
        )
