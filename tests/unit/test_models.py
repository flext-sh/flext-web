"""Unit tests for flext_web.models module.

Tests the web models functionality following flext standards.
Only tests public model construction, validation, and computed properties.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import ipaddress

import pytest
from flext_tests import tm

from flext_web import settings
from tests import c, m


class TestsFlextWebModelsUnit:
    """Test suite for m.Web models."""

    @staticmethod
    def test_web_app_status_enum() -> None:
        """Test WebAppStatus enum values from constants."""
        tm.that(c.Web.Status.STOPPED.value, eq="stopped")
        tm.that(c.Web.Status.STARTING.value, eq="starting")
        tm.that(c.Web.Status.RUNNING.value, eq="running")
        tm.that(c.Web.Status.STOPPING.value, eq="stopping")
        tm.that(c.Web.Status.ERROR.value, eq="error")
        tm.that(c.Web.Status.MAINTENANCE.value, eq="maintenance")
        tm.that(c.Web.Status.DEPLOYING.value, eq="deploying")

    @staticmethod
    def test_web_app_initialization_with_defaults() -> None:
        """Test WebApp initialization with defaults."""
        app = m.Web.Entity(id="test-id", name="test-app")
        tm.that(app.id, eq="test-id")
        tm.that(app.name, eq="test-app")
        tm.that(app.host, eq=settings.Web.host)
        tm.that(app.port, eq=settings.Web.port)
        tm.that(app.status, eq="stopped")
        tm.that(app.version, eq=1)
        tm.that(app.environment, eq="development")
        tm.that(app.debug_mode is False, eq=True)

    @staticmethod
    def test_web_app_initialization_with_custom_values() -> None:
        """Test WebApp initialization with custom values."""
        bind_host = str(ipaddress.IPv4Address(0))
        app = m.Web.Entity(
            id="test-id",
            name="test-app",
            host=bind_host,
            port=3000,
            status="running",
            version=2,
            environment="production",
            debug_mode=True,
        )
        tm.that(app.host, eq=bind_host)
        tm.that(app.port, eq=3000)
        tm.that(app.status, eq="running")
        tm.that(app.version, eq=2)
        tm.that(app.environment, eq="production")
        tm.that(app.debug_mode is True, eq=True)

    @staticmethod
    def test_web_app_name_validation() -> None:
        """Test WebApp name validation."""
        app = m.Web.Entity(id="test-id", name="valid-app-name")
        tm.that(app.name, eq="valid-app-name")
        with pytest.raises(m.ValidationError):
            _ = m.Web.Entity(id="test-id", name="ab")
        with pytest.raises(m.ValidationError):
            _ = m.Web.Entity(id="test-id", name="a" * 101)

    @staticmethod
    def test_web_app_name_reserved_validation() -> None:
        """Test WebApp name validation for reserved names."""
        reserved_names = ["root", "api", "system", "settings", "health"]
        for name in reserved_names:
            with pytest.raises(m.ValidationError):
                _ = m.Web.Entity(id="test-id", name=name)

    @staticmethod
    def test_web_app_name_security_validation() -> None:
        """Test WebApp name security validation."""
        dangerous_names = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "data:text/html,<script>alert('xss')</script>",
            "'; DROP TABLE users; --",
        ]
        for name in dangerous_names:
            with pytest.raises(m.ValidationError):
                _ = m.Web.Entity(id="test-id", name=name)

    @staticmethod
    def test_web_app_port_validation() -> None:
        """Test WebApp port validation."""
        app = m.Web.Entity(id="test-id", name="test-app", port=8080)
        tm.that(app.port, eq=8080)
        with pytest.raises(m.ValidationError):
            _ = m.Web.Entity(id="test-id", name="test-app", port=0)
        with pytest.raises(m.ValidationError):
            _ = m.Web.Entity(id="test-id", name="test-app", port=70000)

    @staticmethod
    def test_web_app_status_validation() -> None:
        """Test WebApp status validation."""
        app = m.Web.Entity(id="test-id", name="test-app", status="running")
        tm.that(app.status, eq="running")
        with pytest.raises(m.ValidationError):
            _ = m.Web.Entity(id="test-id", name="test-app", status="invalid")

    @staticmethod
    def test_web_app_computed_fields() -> None:
        """Test WebApp computed fields."""
        app = m.Web.Entity(id="test-id", name="test-app", status="running")
        tm.that(app.running is True, eq=True)
        tm.that(app.healthy is True, eq=True)
        tm.that(app.can_start is False, eq=True)
        tm.that(app.can_stop is True, eq=True)
        tm.that(app.can_restart is True, eq=True)

        stopped_app = m.Web.Entity(id="test-id", name="test-app", status="stopped")
        tm.that(stopped_app.running is False, eq=True)
        tm.that(stopped_app.can_start is True, eq=True)
        tm.that(stopped_app.can_stop is False, eq=True)

    @staticmethod
    def test_web_app_url_generation() -> None:
        """Test WebApp URL generation."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        tm.that(app.url, eq="http://localhost:8080")
        app_https = m.Web.Entity(
            id="test-id", name="test-app", host="localhost", port=443,
        )
        tm.that(app_https.url, eq="https://localhost:443")

    @staticmethod
    def test_web_app_to_dict() -> None:
        """Test WebApp to_dict conversion."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        app_dict = app.model_dump()
        tm.that(app_dict["id"], eq="test-id")
        tm.that(app_dict["name"], eq="test-app")
        tm.that(app_dict["host"], eq="localhost")
        tm.that(app_dict["port"], eq=8080)

    @staticmethod
    def test_web_app_string_representation() -> None:
        """Test WebApp string representation."""
        app = m.Web.Entity(
            id="test-id", name="test-app", host="localhost", port=8080,
            status="running",
        )
        tm.that(str(app), has="test-app")
        tm.that(str(app), has="localhost:8080")
        tm.that(str(app), has="running")

    @staticmethod
    def test_web_request_initialization() -> None:
        """Test WebRequest initialization."""
        request = m.Web.WebRequest(
            method=c.Web.Method.GET,
            url="http://localhost:8080/api/test",
            headers={"Content-Type": "application/json"},
            body='{"test": "data"}',
        )
        tm.that(request.method, eq=c.Web.Method.GET)
        tm.that(request.url, eq="http://localhost:8080/api/test")
        tm.that(request.headers["Content-Type"], eq="application/json")
        tm.that(request.body, is_=str)
        tm.that(request.body, eq='{"test": "data"}')
        tm.that(request.request_id, none=False)
        tm.that(request.timestamp, none=False)

    @staticmethod
    def test_web_response_initialization() -> None:
        """Test WebResponse initialization."""
        response = m.Web.WebResponse(
            request_id="req-123",
            status_code=200,
            headers={"Content-Type": "application/json"},
            body='{"result": "success"}',
        )
        tm.that(response.request_id, eq="req-123")
        tm.that(response.status_code, eq=200)
        tm.that(response.headers["Content-Type"], eq="application/json")
        tm.that(response.body, is_=str)
        tm.that(response.body, eq='{"result": "success"}')
        tm.that(response.response_id, none=False)
        tm.that(response.timestamp, none=False)

    @staticmethod
    def test_http_request_has_body_property() -> None:
        """Test Web.Request has_body property."""
        request_with_body = m.Web.Request(
            url="http://localhost:8080",
            method=c.Web.Method.POST,
            body='{"data": "test"}',
        )
        tm.that(request_with_body.has_body is True, eq=True)
        request_without_body = m.Web.Request(
            url="http://localhost:8080", method=c.Web.Method.GET, body=None,
        )
        tm.that(request_without_body.has_body is False, eq=True)

    @staticmethod
    def test_http_request_secure_property() -> None:
        """Test Web.Request secure property."""
        https_request = m.Web.Request(
            url="https://localhost:8080", method=c.Web.Method.GET,
        )
        tm.that(https_request.secure is True, eq=True)
        http_request = m.Web.Request(
            url="http://localhost:8080", method=c.Web.Method.GET,
        )
        tm.that(http_request.secure is False, eq=True)

    @staticmethod
    def test_http_response_is_success_property() -> None:
        """Test Web.Response is_success property."""
        success_response = m.Web.Response(status_code=200)
        tm.that(success_response.success is True, eq=True)
        error_response = m.Web.Response(status_code=404)
        tm.that(error_response.success is False, eq=True)

    @staticmethod
    def test_http_response_error_property() -> None:
        """Test Web.Response error property."""
        error_response = m.Web.Response(status_code=500)
        tm.that(error_response.error is True, eq=True)
        success_response = m.Web.Response(status_code=200)
        tm.that(success_response.error is False, eq=True)

    @staticmethod
    def test_web_response_processing_time_seconds() -> None:
        """Test Web.AppResponse processing_time_seconds property."""
        response = m.Web.AppResponse(
            status_code=200, request_id="test-123", processing_time_ms=1500.0,
        )
        tm.that(abs(response.processing_time_seconds - 1.5), lt=1e-9)

    @staticmethod
    def test_application_validate_name_max_length() -> None:
        """Test validate_name with max_length validation."""
        max_length = c.Web.VALIDATION_NAME_LENGTH_RANGE[1]
        long_name = "a" * (max_length + 1)
        with pytest.raises(m.ValidationError):
            _ = m.Web.Entity(id="test-id", name=long_name, host="localhost", port=8080)

    @staticmethod
    @pytest.mark.parametrize(
        ("name", "host", "port", "should_succeed"),
        [
            ("test-app", "localhost", 8080, True),
            ("my_app_123", "127.0.0.1", 3000, True),
            ("app-with-dashes", "example.com", 443, True),
            ("abc", "localhost", 80, True),
            ("a" * 50, "localhost", 8080, True),
            ("", "localhost", 8080, False),
            ("test", "", 8080, False),
            ("test", "localhost", -1, False),
            ("test", "localhost", 0, False),
            ("test", "localhost", 65536, False),
            ("test", "invalid..host", 8080, True),
        ],
    )
    def test_application_parametrized_creation(
        *, name: str, host: str, port: int, should_succeed: bool,
    ) -> None:
        """Test application creation with parametrized edge cases."""
        try:
            app = m.Web.Entity(id="test-id", name=name, host=host, port=port)
        except m.ValidationError:
            if should_succeed:
                pytest.fail(
                    "Unexpected validation failure for "
                    f"name={name}, host={host}, port={port}",
                )
            return
        if not should_succeed:
            pytest.fail(
                "Expected validation failure for "
                f"name={name}, host={host}, port={port}",
            )
        tm.that(app.name, eq=name)
        tm.that(app.host, eq=host)
        tm.that(app.port, eq=port)

    @staticmethod
    def test_extreme_edge_cases() -> None:
        """Test absolute extreme edge cases that might reveal bugs."""
        unicode_name = "测试应用_🚀_123"
        app = m.Web.Entity(id="test-id", name=unicode_name, host="localhost", port=8080)
        tm.that(app.name, eq=unicode_name)

        app = m.Web.Entity(id="test-id", name="test", host="localhost", port=65535)
        tm.that(app.port, eq=65535)

        ipv6_host = "2001:db8::1"
        app = m.Web.Entity(id="test-id", name="test", host=ipv6_host, port=8080)
        tm.that(app.host, eq=ipv6_host)

        long_hostname = "a" * 253
        app = m.Web.Entity(id="test-id", name="test", host=long_hostname, port=8080)
        tm.that(app.host, eq=long_hostname)

        with pytest.raises(m.ValidationError):
            _ = m.Web.Entity(id="test-id", name="x", host="localhost", port=8080)

        max_name = "x" * 100
        app = m.Web.Entity(id="test-id", name=max_name, host="localhost", port=8080)
        tm.that(app.name, eq=max_name)

        with pytest.raises(m.ValidationError):
            _ = m.Web.Entity(id="test-id", name="x" * 101, host="localhost", port=8080)

    @staticmethod
    def test_dangerous_patterns_rejection() -> None:
        """Test that dangerous patterns in names are properly rejected."""
        dangerous_patterns = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "data:text/html,<script>alert('xss')</script>",
            "'; DROP TABLE users; --",
            "-- DROP TABLE users",
            "/* DROP TABLE users */",
            "root",
            "system",
        ]
        for dangerous_name in dangerous_patterns:
            with pytest.raises(m.ValidationError):
                _ = m.Web.Entity(
                    id="test-id", name=dangerous_name, host="localhost", port=8080,
                )
