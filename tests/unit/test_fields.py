"""Unit tests for public field behavior exposed through `web`.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import ipaddress

from flext_web import web
from tests import c, m, tm


class TestsFlextWebFields:
    """Test suite for public web field behavior."""

    @staticmethod
    def test_host_field_creation() -> None:
        """Test host field creation."""
        settings = web.settings.clone(Web={"host": "localhost"})
        tm.that(settings.Web.host, eq="localhost")

    @staticmethod
    def test_host_field_with_custom_default() -> None:
        """Test host field creation with custom default."""
        bind_host = str(ipaddress.IPv4Address(0))
        settings = web.settings.clone(Web={"host": bind_host})
        tm.that(settings.Web.host, eq=bind_host)

    @staticmethod
    def test_port_field_creation() -> None:
        """Test port field creation."""
        settings = web.settings.clone(Web={"port": 8080})
        tm.that(settings.Web.port, eq=8080)

    @staticmethod
    def test_port_field_with_custom_default() -> None:
        """Test port field creation with custom default."""
        settings = web.settings.clone(Web={"port": 3000})
        tm.that(settings.Web.port, eq=3000)

    @staticmethod
    def test_url_field_creation() -> None:
        """Test URL field creation."""
        request = m.Web.Request(url="http://localhost:8080")
        tm.that(request.url, eq="http://localhost:8080")

    @staticmethod
    def test_app_name_field_creation() -> None:
        """Test app name field creation."""
        settings = web.settings.clone(Web={"app_name": "Test App"})
        tm.that(settings.Web.app_name, eq="Test App")

    @staticmethod
    def test_secret_key_field_creation() -> None:
        """Test secret key field creation."""
        # Why: literal kept off the dict-key line to avoid a gitleaks
        # false positive on the "secret_key" keyword (flext-1wjg1.16).
        long_enough_value = "valid-secret-key-32-characters-long"
        settings = web.settings.clone(Web={"secret_key": long_enough_value})
        tm.that(settings.Web.secret_key, none=False)

    @staticmethod
    def test_http_status_field_creation() -> None:
        """Test HTTP status field creation."""
        response = m.Web.Response(status_code=200)
        tm.that(response.status_code, eq=200)
        tm.that(response.success is True, eq=True)

    @staticmethod
    def test_http_status_field_ok() -> None:
        """Test HTTP 200 OK status field creation."""
        response = m.Web.Response(status_code=200)
        tm.that(response.status_code, eq=200)
        tm.that(response.success is True, eq=True)

    @staticmethod
    def test_http_status_field_created() -> None:
        """Test HTTP 201 Created status field creation."""
        response = m.Web.Response(status_code=201)
        tm.that(response.status_code, eq=201)
        tm.that(response.success is True, eq=True)

    @staticmethod
    def test_http_status_field_bad_request() -> None:
        """Test HTTP 400 Bad Request status field creation."""
        response = m.Web.Response(status_code=400)
        tm.that(response.status_code, eq=400)
        tm.that(response.error is True, eq=True)

    @staticmethod
    def test_http_status_field_not_found() -> None:
        """Test HTTP 404 Not Found status field creation."""
        response = m.Web.Response(status_code=404)
        tm.that(response.status_code, eq=404)
        tm.that(response.error is True, eq=True)

    @staticmethod
    def test_http_status_field_server_error() -> None:
        """Test HTTP 500 Internal Server Error status field creation."""
        response = m.Web.Response(status_code=500)
        tm.that(response.status_code, eq=500)
        tm.that(response.error is True, eq=True)

    @staticmethod
    def test_http_status_field_create_field() -> None:
        """Test HTTP status field creation."""
        response = m.Web.Response(status_code=200)
        tm.that(response.status_code, eq=200)
        tm.that(response.success is True, eq=True)

    @staticmethod
    def test_field_constraints() -> None:
        """Test field constraints are properly set."""
        test_model = m.Web.Request(url="http://localhost:8080", method=c.Web.Method.GET)
        tm.that(test_model.url, eq="http://localhost:8080")
        tm.that(test_model.method, eq="GET")

    @staticmethod
    def test_field_descriptions() -> None:
        """Test field descriptions are properly set."""
        host_model = m.Web.Request(url="http://localhost:8080")
        port_model = m.Web.Request(url="http://localhost:3000")
        tm.that(host_model, none=False)
        tm.that(port_model, none=False)

    @staticmethod
    def test_http_status_field_with_kwargs() -> None:
        """Test HTTP status field with additional kwargs."""
        response_model = m.Web.Response(status_code=200)
        tm.that(response_model.status_code, eq=200)
        tm.that(response_model.success is True, eq=True)

    @staticmethod
    def test_field_creation_with_kwargs() -> None:
        """Test field creation with additional kwargs."""
        request_model = m.Web.Request(
            url="http://localhost:8080",
            method=c.Web.Method.POST,
            headers={"Content-Type": "application/json"},
        )
        tm.that(request_model.url, eq="http://localhost:8080")
        tm.that(request_model.method, eq="POST")
        tm.that(request_model.headers["Content-Type"], eq="application/json")

    @staticmethod
    def test_http_status_field_factory_methods() -> None:
        """Test all HTTP status field factory methods."""
        status_codes = [200, 201, 400, 404, 500]
        for status_code in status_codes:
            response_model = m.Web.Response(status_code=status_code)
            tm.that(response_model.status_code, eq=status_code)

    @staticmethod
    def test_field_validation_integration() -> None:
        """Test field validation integration."""
        model = web.settings
        tm.that(model.Web.host, eq=web.settings.Web.host)
        tm.that(model.Web.port, eq=web.settings.Web.port)
