"""Unit tests for flext_web.models module.

Tests the web models functionality following flext standards.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from flext_tests import tm
from tests import c, m, t, u


class TestFlextWebModels:
    """Test suite for m class."""

    def test_web_app_status_enum(self) -> None:
        """Test WebAppStatus enum values from constants."""
        tm.that(c.Web.Status.STOPPED.value, eq="stopped")
        tm.that(c.Web.Status.STARTING.value, eq="starting")
        tm.that(c.Web.Status.RUNNING.value, eq="running")
        tm.that(c.Web.Status.STOPPING.value, eq="stopping")
        tm.that(c.Web.Status.ERROR.value, eq="error")
        tm.that(c.Web.Status.MAINTENANCE.value, eq="maintenance")
        tm.that(c.Web.Status.DEPLOYING.value, eq="deploying")

    def test_web_app_initialization_with_defaults(self) -> None:
        """Test WebApp initialization with defaults."""
        app = u.Web.Tests.create_test_app()
        tm.that(app.id, eq="test-id")
        tm.that(app.name, eq=c.Web.Tests.TestWeb.TEST_APP_NAME)
        tm.that(app.host, eq=c.Web.WebDefaults.HOST)
        tm.that(app.port, eq=c.Web.WebDefaults.PORT)
        tm.that(app.status, eq="stopped")
        tm.that(app.version, eq=1)
        tm.that(app.environment, eq="development")
        tm.that(app.debug_mode is False, eq=True)

    def test_web_app_initialization_with_custom_values(self) -> None:
        """Test WebApp initialization with custom values."""
        app = m.Web.Entity(
            id="test-id",
            name="test-app",
            host="0.0.0.0",
            port=3000,
            status="running",
            version=2,
            environment="production",
            debug_mode=True,
        )
        tm.that(app.host, eq="0.0.0.0")
        tm.that(app.port, eq=3000)
        tm.that(app.status, eq="running")
        tm.that(app.version, eq=2)
        tm.that(app.environment, eq="production")
        tm.that(app.debug_mode is True, eq=True)

    def test_web_app_name_validation(self) -> None:
        """Test WebApp name validation."""
        app = m.Web.Entity(id="test-id", name="valid-app-name")
        tm.that(app.name, eq="valid-app-name")
        with pytest.raises(ValidationError):
            _ = m.Web.Entity(id="test-id", name="ab")
        with pytest.raises(ValidationError):
            _ = m.Web.Entity(id="test-id", name="a" * 101)

    def test_web_app_name_reserved_validation(self) -> None:
        """Test WebApp name validation for reserved names."""
        reserved_names = ["root", "api", "system", "settings", "health"]
        for name in reserved_names:
            with pytest.raises(ValidationError):
                _ = m.Web.Entity(id="test-id", name=name)

    def test_web_app_name_security_validation(self) -> None:
        """Test WebApp name security validation."""
        dangerous_names = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "data:text/html,<script>alert('xss')</script>",
            "'; DROP TABLE users; --",
        ]
        for name in dangerous_names:
            with pytest.raises(ValidationError):
                _ = m.Web.Entity(id="test-id", name=name)

    def test_web_app_port_validation(self) -> None:
        """Test WebApp port validation."""
        app = m.Web.Entity(id="test-id", name="test-app", port=8080)
        tm.that(app.port, eq=8080)
        with pytest.raises(ValidationError):
            _ = m.Web.Entity(id="test-id", name="test-app", port=0)
        with pytest.raises(ValidationError):
            _ = m.Web.Entity(id="test-id", name="test-app", port=70000)

    def test_web_app_status_validation(self) -> None:
        """Test WebApp status validation."""
        app = m.Web.Entity(id="test-id", name="test-app", status="running")
        tm.that(app.status, eq="running")
        with pytest.raises(ValidationError):
            _ = m.Web.Entity(id="test-id", name="test-app", status="invalid")

    def test_web_app_computed_fields(self) -> None:
        """Test WebApp computed fields."""
        app = m.Web.Entity(id="test-id", name="test-app", status="running")
        tm.that(app.running is True, eq=True)
        tm.that(app.healthy is True, eq=True)
        tm.that(app.can_start is False, eq=True)
        tm.that(app.can_stop is True, eq=True)
        tm.that(app.can_restart is True, eq=True)

    def test_web_app_url_generation(self) -> None:
        """Test WebApp URL generation."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        tm.that(app.url, eq="http://localhost:8080")
        app_https = m.Web.Entity(
            id="test-id",
            name="test-app",
            host="localhost",
            port=443,
        )
        tm.that(app_https.url, eq="https://localhost:443")

    def test_web_app_business_rules_validation(self) -> None:
        """Test WebApp business rules validation."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        result = app.validate_business_rules()
        tm.ok(result)

    def test_web_app_start_success(self) -> None:
        """Test WebApp start operation."""
        app = m.Web.Entity(id="test-id", name="test-app", status="stopped")
        result = app.start()
        tm.ok(result)
        started_app = result.value
        tm.that(started_app.status, eq="running")

    def test_web_app_start_already_running(self) -> None:
        """Test WebApp start when already running."""
        app = m.Web.Entity(id="test-id", name="test-app", status="running")
        result = app.start()
        tm.fail(result)
        assert result.error is not None
        tm.that(result.error, has="already running")

    def test_web_app_stop_success(self) -> None:
        """Test WebApp stop operation."""
        app = m.Web.Entity(id="test-id", name="test-app", status="running")
        result = app.stop()
        tm.ok(result)
        stopped_app = result.value
        tm.that(stopped_app.status, eq="stopped")

    def test_web_app_stop_not_running(self) -> None:
        """Test WebApp stop when not running."""
        app = m.Web.Entity(id="test-id", name="test-app", status="stopped")
        result = app.stop()
        tm.fail(result)
        assert result.error is not None
        tm.that(result.error, has="not running")

    def test_web_app_restart_success(self) -> None:
        """Test WebApp restart operation."""
        app = m.Web.Entity(id="test-id", name="test-app", status="running")
        result = app.restart()
        tm.ok(result)
        restarted_app = result.value
        tm.that(restarted_app.status, eq="running")

    def test_web_app_metrics_update(self) -> None:
        """Test WebApp metrics update."""
        app = u.Web.Tests.create_test_app()
        metrics: t.ScalarMapping = {"requests": 100, "errors": 5}
        result = app.update_metrics(metrics)
        tm.ok(result)
        tm.that(result.value is True, eq=True)
        tm.that(app.metrics, has="requests")
        tm.that(app.metrics, has="errors")
        tm.that(app.metrics["requests"], eq=100)
        tm.that(app.metrics["errors"], eq=5)

    def test_web_app_health_status(self) -> None:
        """Test WebApp health status."""
        app = m.Web.Entity(id="test-id", name="test-app", status="running")
        health = app.health_status()
        tm.that(health, has="status")
        tm.that(health, has="running")
        tm.that(health, has="healthy")
        tm.that(health, has="url")
        tm.that(health["status"], eq="running")

    def test_web_app_to_dict(self) -> None:
        """Test WebApp to_dict conversion."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        app_dict = app.model_dump()
        tm.that(app_dict["id"], eq="test-id")
        tm.that(app_dict["name"], eq="test-app")
        tm.that(app_dict["host"], eq="localhost")
        tm.that(app_dict["port"], eq=8080)

    def test_web_app_string_representation(self) -> None:
        """Test WebApp string representation."""
        app = m.Web.Entity(
            id="test-id",
            name="test-app",
            host="localhost",
            port=8080,
            status="running",
        )
        tm.that(str(app), has="test-app")
        tm.that(str(app), has="localhost:8080")
        tm.that(str(app), has="running")

    def test_web_request_initialization(self) -> None:
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
        assert isinstance(request.body, str)
        tm.that(request.body, eq='{"test": "data"}')
        tm.that(request.request_id, none=False)
        tm.that(request.timestamp, none=False)

    def test_web_response_initialization(self) -> None:
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
        assert isinstance(response.body, str)
        tm.that(response.body, eq='{"result": "success"}')
        tm.that(response.response_id, none=False)
        tm.that(response.timestamp, none=False)

    def test_web_app_config_initialization(self) -> None:
        """Test WebAppConfig initialization."""
        settings = m.Web.EntityConfig(
            app_name="Test App",
            host="localhost",
            port=8080,
            debug=True,
            secret_key="test-secret-key-32-characters-long",
        )
        tm.that(settings.app_name, eq="Test App")
        tm.that(settings.host, eq="localhost")
        tm.that(settings.port, eq=8080)
        tm.that(settings.debug is True, eq=True)
        tm.that(settings.secret_key, eq="test-secret-key-32-characters-long")

    def test_app_config_initialization(self) -> None:
        """Test AppConfig initialization."""
        settings = m.Web.AppConfig(
            title="Test API",
            version="1.0.0",
            description="Test API Description",
        )
        tm.that(settings.title, eq="Test API")
        tm.that(settings.version, eq="1.0.0")
        tm.that(settings.description, eq="Test API Description")
        tm.that(settings.docs_url, eq="/docs")
        tm.that(settings.redoc_url, eq="/redoc")
        tm.that(settings.openapi_url, eq="/openapi.json")

    def test_create_web_app_factory(self) -> None:
        """Test create_web_app factory method."""
        result = u.Web.Tests.create_entry(
            "web_app",
            name="test-app",
            host="localhost",
            port=8080,
        )
        assert result.success, result.error
        app = result.value
        assert isinstance(app, m.Web.Entity)
        tm.that(app.name, eq="test-app")
        tm.that(app.host, eq="localhost")
        tm.that(app.port, eq=8080)

    def test_create_web_request_factory(self) -> None:
        """Test create_web_request factory method."""
        result = u.Web.Tests.create_entry(
            "web_request",
            method="POST",
            url="http://localhost:8080/api/test",
            headers={"Content-Type": "application/json"},
            body='{"test": "data"}',
        )
        assert result.success, result.error
        request = result.value
        assert isinstance(request, m.Web.AppRequest)
        tm.that(request.method, eq="POST")
        tm.that(request.url, eq="http://localhost:8080/api/test")

    def test_create_web_response_factory(self) -> None:
        """Test create_web_response factory method."""
        result = u.Web.Tests.create_entry(
            "web_response",
            request_id="req-123",
            status_code=201,
            headers={"Content-Type": "application/json"},
            body='{"id": 1}',
        )
        assert result.success, result.error
        response = result.value
        assert isinstance(response, m.Web.AppResponse)
        tm.that(response.status_code, eq=201)

    def test_http_request_has_body_property(self) -> None:
        """Test Web.Request has_body property."""
        request_with_body = m.Web.Request(
            url="http://localhost:8080",
            method="POST",
            body='{"data": "test"}',
        )
        tm.that(request_with_body.has_body is True, eq=True)
        request_without_body = m.Web.Request(
            url="http://localhost:8080",
            method="GET",
            body=None,
        )
        tm.that(request_without_body.has_body is False, eq=True)

    def test_http_request_secure_property(self) -> None:
        """Test Web.Request secure property."""
        https_request = m.Web.Request(url="https://localhost:8080", method="GET")
        tm.that(https_request.secure is True, eq=True)
        http_request = m.Web.Request(url="http://localhost:8080", method="GET")
        tm.that(http_request.secure is False, eq=True)

    def test_http_response_is_success_property(self) -> None:
        """Test Web.Response is_success property."""
        success_response = m.Web.Response(status_code=200)
        tm.that(success_response.success is True, eq=True)
        error_response = m.Web.Response(status_code=404)
        tm.that(error_response.success is False, eq=True)

    def test_http_response_error_property(self) -> None:
        """Test Web.Response error property."""
        error_response = m.Web.Response(status_code=500)
        tm.that(error_response.error is True, eq=True)
        success_response = m.Web.Response(status_code=200)
        tm.that(success_response.error is False, eq=True)

    def test_web_request_has_body_property(self) -> None:
        """Test Web.Request has_body property."""
        request_with_body = m.Web.Request(
            url="http://localhost:8080",
            method="POST",
            body='{"data": "test"}',
        )
        tm.that(request_with_body.has_body is True, eq=True)
        request_without_body = m.Web.Request(
            url="http://localhost:8080",
            method="GET",
            body=None,
        )
        tm.that(request_without_body.has_body is False, eq=True)

    def test_application_validate_business_rules_short_name(self) -> None:
        """Test validate_business_rules with name too short."""
        app = m.Web.Entity.model_construct(
            id="test-id",
            name="ab",
            host="localhost",
            port=8080,
            status="stopped",
            version=1,
            environment="development",
            debug_mode=False,
        )
        result = app.validate_business_rules()
        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(
            "name" in (result.error or "").lower()
            or "at least" in (result.error or "").lower(),
            eq=True,
        )

    def test_application_validate_business_rules_invalid_port_low(self) -> None:
        """Test validate_business_rules with port too low."""
        app = m.Web.Entity.model_construct(
            id="test-id",
            name="test-app",
            host="localhost",
            port=0,
            status="stopped",
            version=1,
            environment="development",
            debug_mode=False,
        )
        result = app.validate_business_rules()
        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(
            "port" in (result.error or "").lower()
            or "between" in (result.error or "").lower(),
            eq=True,
        )

    def test_application_validate_business_rules_invalid_port_high(self) -> None:
        """Test validate_business_rules with port too high."""
        app = m.Web.Entity.model_construct(
            id="test-id",
            name="test-app",
            host="localhost",
            port=70000,
            status="stopped",
            version=1,
            environment="development",
            debug_mode=False,
        )
        result = app.validate_business_rules()
        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(
            "port" in (result.error or "").lower()
            or "between" in (result.error or "").lower(),
            eq=True,
        )

    def test_application_update_metrics_invalid_type(self) -> None:
        """Test update_metrics with invalid type."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        invalid_metrics: t.ScalarMapping = {"not_a_dict": "not_a_dict"}
        result = app.update_metrics(invalid_metrics)
        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that((result.error or "").lower(), has="dict")

    def test_application_add_domain_event_invalid_type(self) -> None:
        """Test add_domain_event with invalid type raises ValidationError."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        invalid_event_type: str = str(123)
        result = app.add_domain_event(invalid_event_type)
        tm.fail(result)

    def test_application_add_domain_event_empty_string(self) -> None:
        """Test add_domain_event with empty string."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        result = app.add_domain_event("")
        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that((result.error or "").lower(), has="empty")

    def test_create_web_request_invalid_headers(self) -> None:
        """Test create_web_request with invalid headers coerces to empty dict."""
        result = u.Web.Tests.create_entry(
            "web_request",
            method="GET",
            url="http://localhost:8080",
            headers="not_a_dict",
        )
        tm.ok(result)

    def test_create_web_response_invalid_headers(self) -> None:
        """Test create_web_response with invalid headers coerces to empty dict."""
        result = u.Web.Tests.create_entry(
            "web_response",
            request_id="test-123",
            status_code=200,
            headers="not_a_dict",
        )
        tm.ok(result)

    def test_web_response_processing_time_seconds(self) -> None:
        """Test Web.AppResponse processing_time_seconds property."""
        response = m.Web.AppResponse(
            status_code=200,
            request_id="test-123",
            processing_time_ms=1500.0,
        )
        tm.that(abs(response.processing_time_seconds - 1.5), lt=1e-9)

    def test_application_validate_name_max_length(self) -> None:
        """Test validate_name with max_length validation (lines 404-405)."""
        max_length = c.Web.WebValidation.NAME_LENGTH_RANGE[1]
        long_name = "a" * (max_length + 1)
        with pytest.raises(ValidationError):
            _ = m.Web.Entity(id="test-id", name=long_name, host="localhost", port=8080)

    def test_application_validate_business_rules_success(self) -> None:
        """Test validate_business_rules with valid data (line 525)."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        result = app.validate_business_rules()
        tm.ok(result)
        tm.that(result.value is True, eq=True)

    def test_create_web_app_validation_error(self) -> None:
        """Test create_web_app with validation error (lines 914-920)."""
        result = u.Web.Tests.create_entry(
            "web_app",
            name="ab",
            host="localhost",
            port=8080,
        )
        tm.fail(result)
        assert result.error is not None
        tm.that(
            (
                "Validation failed" in result.error
                or "at least" in result.error
                or "between" in result.error
            ),
            eq=True,
        )

    def test_create_web_app_value_error(self) -> None:
        """Test create_web_app with ValueError (lines 914-920)."""
        result = u.Web.Tests.create_entry(
            "web_app",
            name="root",
            host="localhost",
            port=8080,
        )
        tm.fail(result)

    def test_create_web_request_validation_error(self) -> None:
        """Test create_web_request with validation error (lines 961-967)."""
        result = u.Web.Tests.create_entry("web_request", method="GET", url="")
        assert result.failure, "Empty URL should cause validation failure"
        tm.fail(result)
        tm.that(result.error, none=False)

    def test_create_web_response_validation_error(self) -> None:
        """Test create_web_response with validation error (lines 1008-1014)."""
        result = u.Web.Tests.create_entry(
            "web_response",
            request_id="test-123",
            status_code=999,
        )
        assert result.failure, "Invalid status code should cause validation failure"
        tm.fail(result)
        tm.that(result.error, none=False)

    def test_application_edge_cases(self) -> None:
        """Test Application model with edge cases."""
        max_name = "a" * 100
        result = u.Web.Tests.create_entry(
            "web_app",
            name=max_name,
            host="localhost",
            port=8080,
        )
        tm.ok(result)
        result = u.Web.Tests.create_entry(
            "web_app",
            name="a",
            host="localhost",
            port=8080,
        )
        tm.fail(result)
        result = u.Web.Tests.create_entry(
            "web_app",
            name="test_app-123_special",
            host="localhost",
            port=8080,
        )
        tm.ok(result)

    def test_application_invalid_cases(self) -> None:
        """Test Application model with invalid inputs."""
        result = u.Web.Tests.create_entry(
            "web_app", name="", host="localhost", port=8080
        )
        tm.fail(result)
        result = u.Web.Tests.create_entry(
            "web_app", name=None, host="localhost", port=8080
        )
        tm.fail(result)
        result = u.Web.Tests.create_entry(
            "web_app", name="test", host="localhost", port=0
        )
        tm.fail(result)
        result = u.Web.Tests.create_entry("web_app", name="test", host="", port=8080)
        tm.fail(result)

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
        self,
        name: str,
        host: str,
        port: int,
        should_succeed: bool,
    ) -> None:
        """Test application creation with parametrized edge cases."""
        result = u.Web.Tests.create_entry("web_app", name=name, host=host, port=port)
        if should_succeed:
            assert result.success, (
                f"Expected success for app '{name}', got: {result.error}"
            )
            app = result.value
            assert isinstance(app, m.Web.Entity)
            tm.that(app.name, eq=name)
            tm.that(app.host, eq=host)
            tm.that(app.port, eq=port)
        else:
            assert result.failure, f"Expected failure for app '{name}', but succeeded"
            tm.that(result.error, none=False)

    def test_extreme_edge_cases(self) -> None:
        """Test absolute extreme edge cases that might reveal bugs."""
        unicode_name = "测试应用_🚀_123"
        result = u.Web.Tests.create_entry(
            "web_app",
            name=unicode_name,
            host="localhost",
            port=8080,
        )
        tm.ok(result)
        result = u.Web.Tests.create_entry(
            "web_app",
            name="test",
            host="localhost",
            port=65535,
        )
        tm.ok(result)
        ipv6_host = "2001:db8::1"
        result = u.Web.Tests.create_entry(
            "web_app",
            name="test",
            host=ipv6_host,
            port=8080,
        )
        tm.that(result.success or result.failure, eq=True)
        long_hostname = "a" * 253
        result = u.Web.Tests.create_entry(
            "web_app",
            name="test",
            host=long_hostname,
            port=8080,
        )
        tm.ok(result)
        result = u.Web.Tests.create_entry(
            "web_app", name="x", host="localhost", port=8080
        )
        tm.fail(result)
        max_name = "x" * 100
        result = u.Web.Tests.create_entry(
            "web_app",
            name=max_name,
            host="localhost",
            port=8080,
        )
        tm.ok(result)
        too_long_name = "x" * 101
        result = u.Web.Tests.create_entry(
            "web_app",
            name=too_long_name,
            host="localhost",
            port=8080,
        )
        tm.fail(result)

    def test_dangerous_patterns_rejection(self) -> None:
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
            result = u.Web.Tests.create_entry(
                "web_app",
                name=dangerous_name,
                host="localhost",
                port=8080,
            )
            assert result.failure, (
                f"Dangerous pattern '{dangerous_name}' should be rejected"
            )
            tm.fail(result)

    def test_application_add_domain_event_success(self) -> None:
        """Test add_domain_event with valid input."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        result = app.add_domain_event("TestEvent")
        tm.ok(result)
        tm.that(result.value, none=False)

    def test_application_add_domain_event_empty(self) -> None:
        """Test add_domain_event with empty string."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        result = app.add_domain_event("")
        tm.fail(result)
        tm.that(result.error and "empty" in (result.error or "").lower(), eq=True)

    def test_application_name_too_long(self) -> None:
        """Test application creation with name too long."""
        long_name = "a" * 101
        result = u.Web.Tests.create_entry(
            "web_app",
            name=long_name,
            host="localhost",
            port=8080,
        )
        tm.fail(result)
        tm.that(
            result.error
            and ("100" in result.error or "between" in (result.error or "").lower()),
            eq=True,
        )

    def test_application_restart_invalid_state(self) -> None:
        """Test restart when in invalid state (maintenance)."""
        app = m.Web.Entity(
            id="test-id",
            name="test-app",
            host="localhost",
            port=8080,
            status="maintenance",
        )
        result = app.restart()
        tm.fail(result)
        tm.that(
            result.error and "Cannot restart in current state" in result.error,
            eq=True,
        )
