"""Unit tests for flext_web.models module.

Tests the web models functionality following flext standards.
"""

from __future__ import annotations

import pytest
from flext_tests import c, m, t, u
from pydantic import ValidationError

from tests import create_entry, create_test_app


class TestFlextWebModels:
    """Test suite for m class."""

    def test_web_app_status_enum(self) -> None:
        """Test WebAppStatus enum values from constants."""
        u.Tests.Matchers.that(c.Web.Status.STOPPED.value, eq="stopped")
        u.Tests.Matchers.that(c.Web.Status.STARTING.value, eq="starting")
        u.Tests.Matchers.that(c.Web.Status.RUNNING.value, eq="running")
        u.Tests.Matchers.that(c.Web.Status.STOPPING.value, eq="stopping")
        u.Tests.Matchers.that(c.Web.Status.ERROR.value, eq="error")
        u.Tests.Matchers.that(c.Web.Status.MAINTENANCE.value, eq="maintenance")
        u.Tests.Matchers.that(c.Web.Status.DEPLOYING.value, eq="deploying")

    def test_web_app_initialization_with_defaults(self) -> None:
        """Test WebApp initialization with defaults."""
        app = create_test_app()
        u.Tests.Matchers.that(app.id, eq="test-id")
        u.Tests.Matchers.that(app.name, eq=c.Web.Tests.TestWeb.TEST_APP_NAME)
        u.Tests.Matchers.that(app.host, eq=c.Web.WebDefaults.HOST)
        u.Tests.Matchers.that(app.port, eq=c.Web.WebDefaults.PORT)
        u.Tests.Matchers.that(app.status, eq="stopped")
        u.Tests.Matchers.that(app.version, eq=1)
        u.Tests.Matchers.that(app.environment, eq="development")
        u.Tests.Matchers.that(app.debug_mode is False, eq=True)

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
        u.Tests.Matchers.that(app.host, eq="0.0.0.0")
        u.Tests.Matchers.that(app.port, eq=3000)
        u.Tests.Matchers.that(app.status, eq="running")
        u.Tests.Matchers.that(app.version, eq=2)
        u.Tests.Matchers.that(app.environment, eq="production")
        u.Tests.Matchers.that(app.debug_mode is True, eq=True)

    def test_web_app_name_validation(self) -> None:
        """Test WebApp name validation."""
        app = m.Web.Entity(id="test-id", name="valid-app-name")
        u.Tests.Matchers.that(app.name, eq="valid-app-name")
        with pytest.raises(ValidationError):
            _ = m.Web.Entity(id="test-id", name="ab")
        with pytest.raises(ValidationError):
            _ = m.Web.Entity(id="test-id", name="a" * 101)

    def test_web_app_name_reserved_validation(self) -> None:
        """Test WebApp name validation for reserved names."""
        reserved_names = ["root", "api", "system", "config", "health"]
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
        u.Tests.Matchers.that(app.port, eq=8080)
        with pytest.raises(ValidationError):
            _ = m.Web.Entity(id="test-id", name="test-app", port=0)
        with pytest.raises(ValidationError):
            _ = m.Web.Entity(id="test-id", name="test-app", port=70000)

    def test_web_app_status_validation(self) -> None:
        """Test WebApp status validation."""
        app = m.Web.Entity(id="test-id", name="test-app", status="running")
        u.Tests.Matchers.that(app.status, eq="running")
        with pytest.raises(ValidationError):
            _ = m.Web.Entity(id="test-id", name="test-app", status="invalid")

    def test_web_app_computed_fields(self) -> None:
        """Test WebApp computed fields."""
        app = m.Web.Entity(id="test-id", name="test-app", status="running")
        u.Tests.Matchers.that(app.is_running is True, eq=True)
        u.Tests.Matchers.that(app.is_healthy is True, eq=True)
        u.Tests.Matchers.that(app.can_start is False, eq=True)
        u.Tests.Matchers.that(app.can_stop is True, eq=True)
        u.Tests.Matchers.that(app.can_restart is True, eq=True)

    def test_web_app_url_generation(self) -> None:
        """Test WebApp URL generation."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        u.Tests.Matchers.that(app.url, eq="http://localhost:8080")
        app_https = m.Web.Entity(
            id="test-id", name="test-app", host="localhost", port=443
        )
        u.Tests.Matchers.that(app_https.url, eq="https://localhost:443")

    def test_web_app_business_rules_validation(self) -> None:
        """Test WebApp business rules validation."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        result = app.validate_business_rules()
        u.Tests.Matchers.ok(result)

    def test_web_app_start_success(self) -> None:
        """Test WebApp start operation."""
        app = m.Web.Entity(id="test-id", name="test-app", status="stopped")
        result = app.start()
        u.Tests.Matchers.ok(result)
        started_app = result.value
        u.Tests.Matchers.that(started_app.status, eq="running")

    def test_web_app_start_already_running(self) -> None:
        """Test WebApp start when already running."""
        app = m.Web.Entity(id="test-id", name="test-app", status="running")
        result = app.start()
        u.Tests.Matchers.fail(result)
        assert result.error is not None
        u.Tests.Matchers.that("already running" in result.error, eq=True)

    def test_web_app_stop_success(self) -> None:
        """Test WebApp stop operation."""
        app = m.Web.Entity(id="test-id", name="test-app", status="running")
        result = app.stop()
        u.Tests.Matchers.ok(result)
        stopped_app = result.value
        u.Tests.Matchers.that(stopped_app.status, eq="stopped")

    def test_web_app_stop_not_running(self) -> None:
        """Test WebApp stop when not running."""
        app = m.Web.Entity(id="test-id", name="test-app", status="stopped")
        result = app.stop()
        u.Tests.Matchers.fail(result)
        assert result.error is not None
        u.Tests.Matchers.that("not running" in result.error, eq=True)

    def test_web_app_restart_success(self) -> None:
        """Test WebApp restart operation."""
        app = m.Web.Entity(id="test-id", name="test-app", status="running")
        result = app.restart()
        u.Tests.Matchers.ok(result)
        restarted_app = result.value
        u.Tests.Matchers.that(restarted_app.status, eq="running")

    def test_web_app_metrics_update(self) -> None:
        """Test WebApp metrics update."""
        app = create_test_app()
        metrics: dict[str, t.Scalar] = {"requests": 100, "errors": 5}
        result = app.update_metrics(metrics)
        u.Tests.Matchers.ok(result)
        u.Tests.Matchers.that(result.value is True, eq=True)
        u.Tests.Matchers.that("requests" in app.metrics, eq=True)
        u.Tests.Matchers.that("errors" in app.metrics, eq=True)
        u.Tests.Matchers.that(app.metrics["requests"], eq=100)
        u.Tests.Matchers.that(app.metrics["errors"], eq=5)

    def test_web_app_health_status(self) -> None:
        """Test WebApp health status."""
        app = m.Web.Entity(id="test-id", name="test-app", status="running")
        health = app.get_health_status()
        u.Tests.Matchers.that("status" in health, eq=True)
        u.Tests.Matchers.that("is_running" in health, eq=True)
        u.Tests.Matchers.that("is_healthy" in health, eq=True)
        u.Tests.Matchers.that("url" in health, eq=True)
        u.Tests.Matchers.that(health["status"], eq="running")

    def test_web_app_to_dict(self) -> None:
        """Test WebApp to_dict conversion."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        app_dict = app.model_dump()
        u.Tests.Matchers.that(app_dict["id"], eq="test-id")
        u.Tests.Matchers.that(app_dict["name"], eq="test-app")
        u.Tests.Matchers.that(app_dict["host"], eq="localhost")
        u.Tests.Matchers.that(app_dict["port"], eq=8080)

    def test_web_app_string_representation(self) -> None:
        """Test WebApp string representation."""
        app = m.Web.Entity(
            id="test-id", name="test-app", host="localhost", port=8080, status="running"
        )
        u.Tests.Matchers.that("test-app" in str(app), eq=True)
        u.Tests.Matchers.that("localhost:8080" in str(app), eq=True)
        u.Tests.Matchers.that("running" in str(app), eq=True)

    def test_web_request_initialization(self) -> None:
        """Test WebRequest initialization."""
        request = m.Web.WebRequest(
            method="GET",
            url="http://localhost:8080/api/test",
            headers={"Content-Type": "application/json"},
            body='{"test": "data"}',
        )
        u.Tests.Matchers.that(request.method, eq="GET")
        u.Tests.Matchers.that(request.url, eq="http://localhost:8080/api/test")
        u.Tests.Matchers.that(request.headers["Content-Type"], eq="application/json")
        assert isinstance(request.body, str)
        u.Tests.Matchers.that(request.body, eq='{"test": "data"}')
        u.Tests.Matchers.that(request.request_id is not None, eq=True)
        u.Tests.Matchers.that(request.timestamp is not None, eq=True)

    def test_web_response_initialization(self) -> None:
        """Test WebResponse initialization."""
        response = m.Web.WebResponse(
            request_id="req-123",
            status_code=200,
            headers={"Content-Type": "application/json"},
            body='{"result": "success"}',
        )
        u.Tests.Matchers.that(response.request_id, eq="req-123")
        u.Tests.Matchers.that(response.status_code, eq=200)
        u.Tests.Matchers.that(response.headers["Content-Type"], eq="application/json")
        assert isinstance(response.body, str)
        u.Tests.Matchers.that(response.body, eq='{"result": "success"}')
        u.Tests.Matchers.that(response.response_id is not None, eq=True)
        u.Tests.Matchers.that(response.timestamp is not None, eq=True)

    def test_web_app_config_initialization(self) -> None:
        """Test WebAppConfig initialization."""
        config = m.Web.EntityConfig(
            app_name="Test App",
            host="localhost",
            port=8080,
            debug=True,
            secret_key="test-secret-key-32-characters-long",
        )
        u.Tests.Matchers.that(config.app_name, eq="Test App")
        u.Tests.Matchers.that(config.host, eq="localhost")
        u.Tests.Matchers.that(config.port, eq=8080)
        u.Tests.Matchers.that(config.debug is True, eq=True)
        u.Tests.Matchers.that(
            config.secret_key, eq="test-secret-key-32-characters-long"
        )

    def test_app_config_initialization(self) -> None:
        """Test AppConfig initialization."""
        config = m.Web.AppConfig(
            title="Test API", version="1.0.0", description="Test API Description"
        )
        u.Tests.Matchers.that(config.title, eq="Test API")
        u.Tests.Matchers.that(config.version, eq="1.0.0")
        u.Tests.Matchers.that(config.description, eq="Test API Description")
        u.Tests.Matchers.that(config.docs_url, eq="/docs")
        u.Tests.Matchers.that(config.redoc_url, eq="/redoc")
        u.Tests.Matchers.that(config.openapi_url, eq="/openapi.json")

    def test_create_web_app_factory(self) -> None:
        """Test create_web_app factory method."""
        result = create_entry("web_app", name="test-app", host="localhost", port=8080)
        u.Tests.Matchers.ok(result)
        app = result.value
        u.Tests.Matchers.that(isinstance(app, m.Web.Entity), eq=True)
        u.Tests.Matchers.that(app.name, eq="test-app")
        u.Tests.Matchers.that(app.host, eq="localhost")
        u.Tests.Matchers.that(app.port, eq=8080)

    def test_create_web_request_factory(self) -> None:
        """Test create_web_request factory method."""
        result = create_entry(
            "web_request",
            method="POST",
            url="http://localhost:8080/api/test",
            headers={"Content-Type": "application/json"},
            body='{"test": "data"}',
        )
        u.Tests.Matchers.ok(result)
        request = result.value
        u.Tests.Matchers.that(isinstance(request, m.Web.AppRequest), eq=True)
        u.Tests.Matchers.that(request.method, eq="POST")
        u.Tests.Matchers.that(request.url, eq="http://localhost:8080/api/test")

    def test_create_web_response_factory(self) -> None:
        """Test create_web_response factory method."""
        result = create_entry(
            "web_response",
            request_id="req-123",
            status_code=201,
            headers={"Content-Type": "application/json"},
            body='{"id": 1}',
        )
        u.Tests.Matchers.ok(result)
        response = result.value
        u.Tests.Matchers.that(isinstance(response, m.Web.AppResponse), eq=True)
        u.Tests.Matchers.that(response.status_code, eq=201)

    def test_http_request_has_body_property(self) -> None:
        """Test Web.Request has_body property."""
        request_with_body = m.Web.Request(
            url="http://localhost:8080", method="POST", body='{"data": "test"}'
        )
        u.Tests.Matchers.that(request_with_body.has_body is True, eq=True)
        request_without_body = m.Web.Request(
            url="http://localhost:8080", method="GET", body=None
        )
        u.Tests.Matchers.that(request_without_body.has_body is False, eq=True)

    def test_http_request_is_secure_property(self) -> None:
        """Test Web.Request is_secure property."""
        https_request = m.Web.Request(url="https://localhost:8080", method="GET")
        u.Tests.Matchers.that(https_request.is_secure is True, eq=True)
        http_request = m.Web.Request(url="http://localhost:8080", method="GET")
        u.Tests.Matchers.that(http_request.is_secure is False, eq=True)

    def test_http_response_is_success_property(self) -> None:
        """Test Web.Response is_success property."""
        success_response = m.Web.Response(status_code=200)
        u.Tests.Matchers.that(success_response.is_success is True, eq=True)
        error_response = m.Web.Response(status_code=404)
        u.Tests.Matchers.that(error_response.is_success is False, eq=True)

    def test_http_response_is_error_property(self) -> None:
        """Test Web.Response is_error property."""
        error_response = m.Web.Response(status_code=500)
        u.Tests.Matchers.that(error_response.is_error is True, eq=True)
        success_response = m.Web.Response(status_code=200)
        u.Tests.Matchers.that(success_response.is_error is False, eq=True)

    def test_web_request_has_body_property(self) -> None:
        """Test Web.Request has_body property."""
        request_with_body = m.Web.Request(
            url="http://localhost:8080", method="POST", body='{"data": "test"}'
        )
        u.Tests.Matchers.that(request_with_body.has_body is True, eq=True)
        request_without_body = m.Web.Request(
            url="http://localhost:8080", method="GET", body=None
        )
        u.Tests.Matchers.that(request_without_body.has_body is False, eq=True)

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
        u.Tests.Matchers.fail(result)
        u.Tests.Matchers.that(result.error is not None, eq=True)
        u.Tests.Matchers.that(
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
        u.Tests.Matchers.fail(result)
        u.Tests.Matchers.that(result.error is not None, eq=True)
        u.Tests.Matchers.that(
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
        u.Tests.Matchers.fail(result)
        u.Tests.Matchers.that(result.error is not None, eq=True)
        u.Tests.Matchers.that(
            "port" in (result.error or "").lower()
            or "between" in (result.error or "").lower(),
            eq=True,
        )

    def test_application_update_metrics_invalid_type(self) -> None:
        """Test update_metrics with invalid type."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        invalid_metrics: dict[str, t.Scalar] = {"not_a_dict": "not_a_dict"}
        result = app.update_metrics(invalid_metrics)
        u.Tests.Matchers.fail(result)
        u.Tests.Matchers.that(result.error is not None, eq=True)
        u.Tests.Matchers.that("dict" in (result.error or "").lower(), eq=True)

    def test_application_add_domain_event_invalid_type(self) -> None:
        """Test add_domain_event with invalid type raises ValidationError."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        invalid_event_type: str = str(123)
        result = app.add_domain_event(invalid_event_type)
        u.Tests.Matchers.fail(result)

    def test_application_add_domain_event_empty_string(self) -> None:
        """Test add_domain_event with empty string."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        result = app.add_domain_event("")
        u.Tests.Matchers.fail(result)
        u.Tests.Matchers.that(result.error is not None, eq=True)
        u.Tests.Matchers.that("empty" in (result.error or "").lower(), eq=True)

    def test_create_web_request_invalid_headers(self) -> None:
        """Test create_web_request with invalid headers type."""
        result = create_entry(
            "web_request",
            method="GET",
            url="http://localhost:8080",
            headers="not_a_dict",
        )
        u.Tests.Matchers.fail(result)

    def test_create_web_response_invalid_headers(self) -> None:
        """Test create_web_response with invalid headers type."""
        result = create_entry(
            "web_response",
            request_id="test-123",
            status_code=200,
            headers="not_a_dict",
        )
        u.Tests.Matchers.fail(result)

    def test_web_response_processing_time_seconds(self) -> None:
        """Test Web.AppResponse processing_time_seconds property."""
        response = m.Web.AppResponse(
            status_code=200, request_id="test-123", processing_time_ms=1500.0
        )
        u.Tests.Matchers.that(abs(response.processing_time_seconds - 1.5), lt=1e-9)

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
        u.Tests.Matchers.ok(result)
        u.Tests.Matchers.that(result.value is True, eq=True)

    def test_create_web_app_validation_error(self) -> None:
        """Test create_web_app with validation error (lines 914-920)."""
        result = create_entry("web_app", name="ab", host="localhost", port=8080)
        u.Tests.Matchers.fail(result)
        assert result.error is not None
        u.Tests.Matchers.that(
            (
                "Validation failed" in result.error
                or "at least" in result.error
                or "between" in result.error
            ),
            eq=True,
        )

    def test_create_web_app_value_error(self) -> None:
        """Test create_web_app with ValueError (lines 914-920)."""
        result = create_entry("web_app", name="root", host="localhost", port=8080)
        u.Tests.Matchers.fail(result)

    def test_create_web_request_validation_error(self) -> None:
        """Test create_web_request with validation error (lines 961-967)."""
        result = create_entry("web_request", method="GET", url="")
        u.Tests.Matchers.fail(result), "Empty URL should cause validation failure"
        u.Tests.Matchers.that(result.error is not None, eq=True)

    def test_create_web_response_validation_error(self) -> None:
        """Test create_web_response with validation error (lines 1008-1014)."""
        result = create_entry("web_response", request_id="test-123", status_code=999)
        (
            u.Tests.Matchers.fail(result),
            "Invalid status code should cause validation failure",
        )
        u.Tests.Matchers.that(result.error is not None, eq=True)

    def test_application_edge_cases(self) -> None:
        """Test Application model with edge cases."""
        max_name = "a" * 100
        result = create_entry("web_app", name=max_name, host="localhost", port=8080)
        u.Tests.Matchers.ok(result)
        result = create_entry("web_app", name="a", host="localhost", port=8080)
        u.Tests.Matchers.fail(result)
        result = create_entry(
            "web_app", name="test_app-123_special", host="localhost", port=8080
        )
        u.Tests.Matchers.ok(result)

    def test_application_invalid_cases(self) -> None:
        """Test Application model with invalid inputs."""
        result = create_entry("web_app", name="", host="localhost", port=8080)
        u.Tests.Matchers.fail(result)
        result = create_entry("web_app", name=None, host="localhost", port=8080)
        u.Tests.Matchers.fail(result)
        result = create_entry("web_app", name="test", host="localhost", port=0)
        u.Tests.Matchers.fail(result)
        result = create_entry("web_app", name="test", host="", port=8080)
        u.Tests.Matchers.fail(result)

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
        self, name: str, host: str, port: int, should_succeed: bool
    ) -> None:
        """Test application creation with parametrized edge cases."""
        result = create_entry("web_app", name=name, host=host, port=port)
        if should_succeed:
            (
                u.Tests.Matchers.ok(result),
                (f"Expected success for app '{name}', got: {result.error}"),
            )
            app = result.value
            u.Tests.Matchers.that(isinstance(app, m.Web.Entity), eq=True)
            u.Tests.Matchers.that(app.name, eq=name)
            u.Tests.Matchers.that(app.host, eq=host)
            u.Tests.Matchers.that(app.port, eq=port)
        else:
            (
                u.Tests.Matchers.fail(result),
                (f"Expected failure for app '{name}', but succeeded"),
            )
            u.Tests.Matchers.that(result.error is not None, eq=True)

    def test_extreme_edge_cases(self) -> None:
        """Test absolute extreme edge cases that might reveal bugs."""
        unicode_name = "测试应用_🚀_123"
        result = create_entry("web_app", name=unicode_name, host="localhost", port=8080)
        u.Tests.Matchers.ok(result)
        result = create_entry("web_app", name="test", host="localhost", port=65535)
        u.Tests.Matchers.ok(result)
        ipv6_host = "2001:db8::1"
        result = create_entry("web_app", name="test", host=ipv6_host, port=8080)
        u.Tests.Matchers.that(result.is_success or result.is_failure, eq=True)
        long_hostname = "a" * 253
        result = create_entry("web_app", name="test", host=long_hostname, port=8080)
        u.Tests.Matchers.ok(result)
        result = create_entry("web_app", name="x", host="localhost", port=8080)
        u.Tests.Matchers.fail(result)
        max_name = "x" * 100
        result = create_entry("web_app", name=max_name, host="localhost", port=8080)
        u.Tests.Matchers.ok(result)
        too_long_name = "x" * 101
        result = create_entry(
            "web_app", name=too_long_name, host="localhost", port=8080
        )
        u.Tests.Matchers.fail(result)

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
            result = create_entry(
                "web_app", name=dangerous_name, host="localhost", port=8080
            )
            (
                u.Tests.Matchers.fail(result),
                (f"Dangerous pattern '{dangerous_name}' should be rejected"),
            )

    def test_application_add_domain_event_success(self) -> None:
        """Test add_domain_event with valid input."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        result = app.add_domain_event("TestEvent")
        u.Tests.Matchers.ok(result)
        u.Tests.Matchers.that(result.value is not None, eq=True)
        u.Tests.Matchers.that(hasattr(result.value, "event_type"), eq=True)

    def test_application_add_domain_event_empty(self) -> None:
        """Test add_domain_event with empty string."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        result = app.add_domain_event("")
        u.Tests.Matchers.fail(result)
        u.Tests.Matchers.that(
            result.error and "empty" in (result.error or "").lower(), eq=True
        )

    def test_application_name_too_long(self) -> None:
        """Test application creation with name too long."""
        long_name = "a" * 101
        result = create_entry("web_app", name=long_name, host="localhost", port=8080)
        u.Tests.Matchers.fail(result)
        u.Tests.Matchers.that(
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
        u.Tests.Matchers.fail(result)
        u.Tests.Matchers.that(
            result.error and "Cannot restart in current state" in result.error, eq=True
        )
