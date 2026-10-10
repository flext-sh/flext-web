"""Unit tests for flext_web.constants module.

Tests the web constants functionality following flext standards.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import ipaddress
from collections.abc import Mapping

from flext_tests import tm

from tests import c


class TestsFlextWebConstantsUnit:
    """Test suite for c class."""

    @staticmethod
    def test_web_server_constants() -> None:
        """Test web server constants."""
        tm.that(c.Web.VALIDATION_PORT_RANGE, eq=(1, 65535))
        tm.that(c.Web.VALIDATION_NAME_LENGTH_RANGE, eq=(3, 100))

    @staticmethod
    def test_web_specific_constants() -> None:
        """Test web-specific constants."""
        tm.that(c.Web.ALL_INTERFACES, eq=str(ipaddress.IPv4Address(0)))

    def test_web_environment_types(self) -> None:
        """Test web environment type definitions."""

    @staticmethod
    def test_web_security_constants() -> None:
        """Test web security constants."""
        tm.that(c.Web.SECURITY_CORS_DEFAULT_ORIGINS, is_=frozenset)
        tm.that(c.Web.SECURITY_CORS_DEFAULT_ORIGINS, has="*")
        tm.that(c.Web.SECURITY_CORS_SAFE_METHODS, is_=frozenset)
        tm.that(c.Web.SECURITY_CORS_SAFE_METHODS, has="GET")
        tm.that(c.Web.SECURITY_CORS_SAFE_HEADERS, is_=frozenset)
        tm.that(c.Web.SECURITY_CORS_SAFE_HEADERS, has="Content-Type")
        tm.that(c.Web.SECURITY_SESSION_COOKIE_SECURE_DEFAULT is False, eq=True)
        tm.that(c.Web.SECURITY_SESSION_COOKIE_HTTPONLY_DEFAULT is True, eq=True)

    @staticmethod
    def test_web_validation_constants() -> None:
        """Test web validation constants."""
        tm.that(c.Web.VALIDATION_MAX_CONTENT_LENGTH_DEFAULT, eq=16 * 1024 * 1024)

    @staticmethod
    def test_constants_are_immutable() -> None:
        """Test that constants are properly defined and immutable."""
        tm.that(c.Web.VALIDATION_PORT_RANGE, is_=tuple)
        tm.that(c.Web.VALIDATION_NAME_LENGTH_RANGE, is_=tuple)
        tm.that(c.Web.SECURITY_MIN_SECRET_KEY_LENGTH, is_=int)

    @staticmethod
    def test_environment_type_values() -> None:
        """Test that environment type values are valid."""
        tm.that(c.Web.Name, none=False)
        tm.that(c.Web.ApplicationType, none=False)
        tm.that(c.Web.Method, none=False)
        tm.that(c.Web.Status, none=False)

    @staticmethod
    def test_security_constants_types() -> None:
        """Test that security constants have correct types."""
        tm.that(c.Web.SECURITY_MIN_SECRET_KEY_LENGTH, is_=int)
        tm.that(c.Web.SECURITY_SSL_PORTS, is_=tuple)
        tm.that(c.Web.SECURITY_SESSION_DEFAULTS, is_=Mapping)

    @staticmethod
    def test_validation_constants_types() -> None:
        """Test that validation constants have correct types."""
        tm.that(c.Web.VALIDATION_CONTENT_LENGTH_RANGE, is_=tuple)
        tm.that(c.Web.VALIDATION_REQUEST_TIMEOUT_RANGE, is_=tuple)
        tm.that(c.Web.VALIDATION_URL_LENGTH_RANGE, is_=tuple)
        tm.that(c.Web.VALIDATION_MIN_URL_LENGTH, is_=int)
        tm.that(c.Web.VALIDATION_MAX_HEADER_LENGTH, is_=int)
        tm.that(c.Web.VALIDATION_MAX_HEADERS_COUNT, is_=int)
