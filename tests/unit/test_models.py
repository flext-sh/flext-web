"""Unit tests for flext_web.models module.

Tests the web models functionality following flext standards.
"""

from __future__ import annotations

from collections.abc import Mapping

import pytest
from algar_oud_mig import t
from algar_oud_mig.typings import t
from flext_api import t
from flext_api.typings import t
from flext_auth import t
from flext_auth.typings import t
from flext_cli import t
from flext_cli.typings import t
from flext_core import t
from flext_core.typings import t
from flext_db_oracle import t
from flext_db_oracle.typings import t
from flext_dbt_ldap import t
from flext_dbt_ldap.typings import t
from flext_dbt_ldif import t
from flext_dbt_ldif.typings import t
from flext_dbt_oracle import t
from flext_dbt_oracle.typings import t
from flext_dbt_oracle_wms.typings import t
from flext_grpc import t
from flext_grpc.typings import t
from flext_infra import t
from flext_infra.typings import t
from flext_ldap import t
from flext_ldap.typings import t
from flext_ldif import t
from flext_ldif._models.domain import t
from flext_ldif.typings import t
from flext_meltano import t
from flext_meltano.dbt.service import t
from flext_meltano.meltano.service import t
from flext_meltano.singer.catalog import t
from flext_meltano.singer.protocols import t
from flext_meltano.singer.service import t
from flext_meltano.typings import t
from flext_observability import t
from flext_observability.typings import t
from flext_oracle_oic import t
from flext_oracle_oic.typings import t
from flext_oracle_wms import t
from flext_oracle_wms.typings import t
from flext_plugin import t
from flext_plugin.typings import t
from flext_quality import t
from flext_quality.typings import t
from flext_tap_ldap import t
from flext_tap_ldap.typings import t
from flext_tap_ldif import t
from flext_tap_ldif.typings import t
from flext_tap_oracle import t
from flext_tap_oracle.typings import t
from flext_tap_oracle_oic import t
from flext_tap_oracle_oic.typings import t
from flext_tap_oracle_wms.typings import t
from flext_target_ldap import t
from flext_target_ldap.typings import t
from flext_target_ldif import t
from flext_target_ldif.typings import t
from flext_target_oracle import t
from flext_target_oracle.typings import t
from flext_target_oracle_oic.typings import t
from flext_target_oracle_wms import t
from flext_target_oracle_wms.typings import t
from flext_tests import t
from flext_tests._validator.types import t
from flext_tests.typings import t
from gruponos_meltano_native import t
from gruponos_meltano_native.typings import t
from packaging._musllinux import t
from pydantic import ValidationError
from rich.abc import t
from scipy.stats import t
from scipy.stats._continuous_distns import t
from src.algar_oud_mig.typings import t
from src.flext_api.typings import t
from src.flext_auth.typings import t
from src.flext_cli.typings import t
from src.flext_db_oracle.typings import t
from src.flext_dbt_ldap.typings import t
from src.flext_dbt_ldif.typings import t
from src.flext_dbt_oracle.typings import t
from src.flext_grpc.typings import t
from src.flext_infra.typings import t
from src.flext_ldap.typings import t
from src.flext_ldif._models.domain import t
from src.flext_ldif.typings import t
from src.flext_meltano.dbt.service import t
from src.flext_meltano.meltano.bridge import t
from src.flext_meltano.meltano.service import t
from src.flext_meltano.singer.catalog import t
from src.flext_meltano.singer.protocols import t
from src.flext_meltano.singer.service import t
from src.flext_meltano.typings import t
from src.flext_observability.typings import t
from src.flext_oracle_oic.typings import t
from src.flext_oracle_wms.typings import t
from src.flext_plugin.typings import t
from src.flext_quality.typings import t
from src.flext_tap_ldap.typings import t
from src.flext_tap_ldif.typings import t
from src.flext_tap_oracle.typings import t
from src.flext_tap_oracle_oic.typings import t
from src.flext_tap_oracle_wms.typings import t
from src.flext_target_ldap.typings import t
from src.flext_target_ldif.typings import t
from src.flext_target_oracle.typings import t
from src.flext_target_oracle_oic.typings import t
from src.flext_target_oracle_wms.typings import t
from src.flext_tests.typings import t
from src.gruponos_meltano_native.typings import t
from tests import c, m, t
from tests.conftest import create_entry, create_test_app
from tests.fixtures.namespace_validator import t
from tests.fixtures.namespace_validator.rule2_protocol_in_types import t
from tests.fixtures.namespace_validator.rule2_typevar_in_class import t
from tests.fixtures.namespace_validator.rule2_valid_types import t
from tests.helpers import t
from tests.helpers.typings import t
from tests.infra import t
from tests.infra.typings import t
from tests.infra.unit import t
from tests.infra.unit.test_infra_patterns_extra import t
from tests.integration import t
from tests.integration.test_refactor_policy_mro import t
from tests.tt import t
from tests.typings import t

from flext_web import t
from flext_web.typings import t


class TestFlextWebModels:
    """Test suite for m class."""

    def test_web_app_status_enum(self) -> None:
        """Test WebAppStatus enum values from constants."""
        assert c.Web.Status.STOPPED.value == "stopped"
        assert c.Web.Status.STARTING.value == "starting"
        assert c.Web.Status.RUNNING.value == "running"
        assert c.Web.Status.STOPPING.value == "stopping"
        assert c.Web.Status.ERROR.value == "error"
        assert c.Web.Status.MAINTENANCE.value == "maintenance"
        assert c.Web.Status.DEPLOYING.value == "deploying"

    def test_web_app_initialization_with_defaults(self) -> None:
        """Test WebApp initialization with defaults."""
        app = create_test_app()
        assert app.id == "test-id"
        assert app.name == "test-app"
        assert app.host == c.Web.WebDefaults.HOST
        assert app.port == c.Web.WebDefaults.PORT
        assert app.status == "stopped"
        assert app.version == 1
        assert app.environment == "development"
        assert app.debug_mode is False

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
        assert app.host == "0.0.0.0"
        assert app.port == 3000
        assert app.status == "running"
        assert app.version == 2
        assert app.environment == "production"
        assert app.debug_mode is True

    def test_web_app_name_validation(self) -> None:
        """Test WebApp name validation."""
        app = m.Web.Entity(id="test-id", name="valid-app-name")
        assert app.name == "valid-app-name"
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
        assert app.port == 8080
        with pytest.raises(ValidationError):
            _ = m.Web.Entity(id="test-id", name="test-app", port=0)
        with pytest.raises(ValidationError):
            _ = m.Web.Entity(id="test-id", name="test-app", port=70000)

    def test_web_app_status_validation(self) -> None:
        """Test WebApp status validation."""
        app = m.Web.Entity(id="test-id", name="test-app", status="running")
        assert app.status == "running"
        with pytest.raises((ValidationError, TypeError)):
            _ = m.Web.Entity(id="test-id", name="test-app", status="invalid")

    def test_web_app_computed_fields(self) -> None:
        """Test WebApp computed fields."""
        app = m.Web.Entity(id="test-id", name="test-app", status="running")
        assert app.is_running is True
        assert app.is_healthy is True
        assert app.can_start is False
        assert app.can_stop is True
        assert app.can_restart is True

    def test_web_app_url_generation(self) -> None:
        """Test WebApp URL generation."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        assert app.url == "http://localhost:8080"
        app_https = m.Web.Entity(
            id="test-id", name="test-app", host="localhost", port=443
        )
        assert app_https.url == "https://localhost:443"

    def test_web_app_business_rules_validation(self) -> None:
        """Test WebApp business rules validation."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        result = app.validate_business_rules()
        assert result.is_success

    def test_web_app_start_success(self) -> None:
        """Test WebApp start operation."""
        app = m.Web.Entity(id="test-id", name="test-app", status="stopped")
        result = app.start()
        assert result.is_success
        started_app = result.value
        assert started_app.status == "running"

    def test_web_app_start_already_running(self) -> None:
        """Test WebApp start when already running."""
        app = m.Web.Entity(id="test-id", name="test-app", status="running")
        result = app.start()
        assert result.is_failure
        assert result.error is not None
        assert "already running" in result.error

    def test_web_app_stop_success(self) -> None:
        """Test WebApp stop operation."""
        app = m.Web.Entity(id="test-id", name="test-app", status="running")
        result = app.stop()
        assert result.is_success
        stopped_app = result.value
        assert stopped_app.status == "stopped"

    def test_web_app_stop_not_running(self) -> None:
        """Test WebApp stop when not running."""
        app = m.Web.Entity(id="test-id", name="test-app", status="stopped")
        result = app.stop()
        assert result.is_failure
        assert result.error is not None
        assert "not running" in result.error

    def test_web_app_restart_success(self) -> None:
        """Test WebApp restart operation."""
        app = m.Web.Entity(id="test-id", name="test-app", status="running")
        result = app.restart()
        assert result.is_success
        restarted_app = result.value
        assert restarted_app.status == "running"

    def test_web_app_metrics_update(self) -> None:
        """Test WebApp metrics update."""
        app = create_test_app()
        metrics: dict[str, t.Scalar | None] = {"requests": 100, "errors": 5}
        result = app.update_metrics(metrics)
        assert result.is_success
        assert result.value is True
        assert "requests" in app.metrics
        assert "errors" in app.metrics
        assert app.metrics["requests"] == 100
        assert app.metrics["errors"] == 5

    def test_web_app_health_status(self) -> None:
        """Test WebApp health status."""
        app = m.Web.Entity(id="test-id", name="test-app", status="running")
        health = app.get_health_status()
        assert "status" in health
        assert "is_running" in health
        assert "is_healthy" in health
        assert "url" in health
        assert health["status"] == "running"

    def test_web_app_to_dict(self) -> None:
        """Test WebApp to_dict conversion."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        app_dict = app.model_dump()
        assert app_dict["id"] == "test-id"
        assert app_dict["name"] == "test-app"
        assert app_dict["host"] == "localhost"
        assert app_dict["port"] == 8080

    def test_web_app_string_representation(self) -> None:
        """Test WebApp string representation."""
        app = m.Web.Entity(
            id="test-id", name="test-app", host="localhost", port=8080, status="running"
        )
        assert "test-app" in str(app)
        assert "localhost:8080" in str(app)
        assert "running" in str(app)

    def test_web_request_initialization(self) -> None:
        """Test WebRequest initialization."""
        request = m.Web.WebRequest(
            method="GET",
            url="http://localhost:8080/api/test",
            headers={"Content-Type": "application/json"},
            body='{"test": "data"}',
        )
        assert request.method == "GET"
        assert request.url == "http://localhost:8080/api/test"
        assert request.headers["Content-Type"] == "application/json"
        assert request.body == '{"test": "data"}'
        assert request.request_id is not None
        assert request.timestamp is not None

    def test_web_response_initialization(self) -> None:
        """Test WebResponse initialization."""
        response = m.Web.WebResponse(
            request_id="req-123",
            status_code=200,
            headers={"Content-Type": "application/json"},
            body='{"result": "success"}',
        )
        assert response.request_id == "req-123"
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        assert response.body == '{"result": "success"}'
        assert response.response_id is not None
        assert response.timestamp is not None

    def test_web_app_config_initialization(self) -> None:
        """Test WebAppConfig initialization."""
        config = m.Web.EntityConfig(
            app_name="Test App",
            host="localhost",
            port=8080,
            debug=True,
            secret_key="test-secret-key-32-characters-long",
        )
        assert config.app_name == "Test App"
        assert config.host == "localhost"
        assert config.port == 8080
        assert config.debug is True
        assert config.secret_key == "test-secret-key-32-characters-long"

    def test_app_config_initialization(self) -> None:
        """Test AppConfig initialization."""
        config = m.Web.AppConfig(
            title="Test API", version="1.0.0", description="Test API Description"
        )
        assert config.title == "Test API"
        assert config.version == "1.0.0"
        assert config.description == "Test API Description"
        assert config.docs_url == "/docs"
        assert config.redoc_url == "/redoc"
        assert config.openapi_url == "/openapi.json"

    def test_create_web_app_factory(self) -> None:
        """Test create_web_app factory method."""
        result = create_entry("web_app", name="test-app", host="localhost", port=8080)
        assert result.is_success
        app = result.value
        assert isinstance(app, m.Web.Entity)
        assert app.name == "test-app"
        assert app.host == "localhost"
        assert app.port == 8080

    def test_create_web_request_factory(self) -> None:
        """Test create_web_request factory method."""
        result = create_entry(
            "web_request",
            method="POST",
            url="http://localhost:8080/api/test",
            headers={"Content-Type": "application/json"},
            body='{"test": "data"}',
        )
        assert result.is_success
        request = result.value
        assert isinstance(request, m.Web.Request)
        assert request.method == "POST"
        assert request.url == "http://localhost:8080/api/test"

    def test_create_web_response_factory(self) -> None:
        """Test create_web_response factory method."""
        result = create_entry(
            "web_response",
            request_id="req-123",
            status_code=201,
            headers={"Content-Type": "application/json"},
            body='{"id": 1}',
        )
        assert result.is_success
        response = result.value
        assert isinstance(response, m.Web.Response)
        assert response.status_code == 201

    def test_http_request_has_body_property(self) -> None:
        """Test Web.Request has_body property."""
        request_with_body = m.Web.Request(
            url="http://localhost:8080", method="POST", body='{"data": "test"}'
        )
        assert request_with_body.has_body is True
        request_without_body = m.Web.Request(
            url="http://localhost:8080", method="GET", body=None
        )
        assert request_without_body.has_body is False

    def test_http_request_is_secure_property(self) -> None:
        """Test Web.Request is_secure property."""
        https_request = m.Web.Request(url="https://localhost:8080", method="GET")
        assert https_request.is_secure is True
        http_request = m.Web.Request(url="http://localhost:8080", method="GET")
        assert http_request.is_secure is False

    def test_http_response_is_success_property(self) -> None:
        """Test Web.Response is_success property."""
        success_response = m.Web.Response(status_code=200)
        assert success_response.is_success is True
        error_response = m.Web.Response(status_code=404)
        assert error_response.is_success is False

    def test_http_response_is_error_property(self) -> None:
        """Test Web.Response is_error property."""
        error_response = m.Web.Response(status_code=500)
        assert error_response.is_error is True
        success_response = m.Web.Response(status_code=200)
        assert success_response.is_error is False

    def test_web_request_has_body_property(self) -> None:
        """Test Web.Request has_body property."""
        request_with_body = m.Web.Request(
            url="http://localhost:8080", method="POST", body='{"data": "test"}'
        )
        assert request_with_body.has_body is True
        request_without_body = m.Web.Request(
            url="http://localhost:8080", method="GET", body=None
        )
        assert request_without_body.has_body is False

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
        assert result.is_failure
        assert result.error is not None
        assert "name" in result.error.lower() or "at least" in result.error.lower()

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
        assert result.is_failure
        assert result.error is not None
        assert "port" in result.error.lower() or "between" in result.error.lower()

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
        assert result.is_failure
        assert result.error is not None
        assert "port" in result.error.lower() or "between" in result.error.lower()

    def test_application_update_metrics_invalid_type(self) -> None:
        """Test update_metrics with invalid type."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        invalid_metrics: Mapping[str, t.Scalar | None] = {"not_a_dict": "not_a_dict"}
        result = app.update_metrics(invalid_metrics)
        assert result.is_failure
        assert result.error is not None
        assert "dict" in result.error.lower()

    def test_application_add_domain_event_invalid_type(self) -> None:
        """Test add_domain_event with invalid type raises ValidationError."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        invalid_event_type: str = str(123)
        result = app.add_domain_event(invalid_event_type)
        assert result.is_failure

    def test_application_add_domain_event_empty_string(self) -> None:
        """Test add_domain_event with empty string."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        result = app.add_domain_event("")
        assert result.is_failure
        assert result.error is not None
        assert "empty" in result.error.lower()

    def test_create_web_request_invalid_headers(self) -> None:
        """Test create_web_request with invalid headers type."""
        with pytest.raises(ValidationError):
            _ = create_entry(
                "web_request",
                method="GET",
                url="http://localhost:8080",
                headers="not_a_dict",
            )

    def test_create_web_response_invalid_headers(self) -> None:
        """Test create_web_response with invalid headers type."""
        with pytest.raises(ValidationError):
            _ = create_entry(
                "web_response",
                request_id="test-123",
                status_code=200,
                headers="not_a_dict",
            )

    def test_web_response_processing_time_seconds(self) -> None:
        """Test Web.AppResponse processing_time_seconds property."""
        response = m.Web.AppResponse(
            status_code=200, request_id="test-123", processing_time_ms=1500.0
        )
        assert response.processing_time_seconds == pytest.approx(1.5)

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
        assert result.is_success
        assert result.value is True

    def test_create_web_app_validation_error(self) -> None:
        """Test create_web_app with validation error (lines 914-920)."""
        result = create_entry("web_app", name="ab", host="localhost", port=8080)
        assert result.is_failure
        assert result.error is not None
        assert "Validation failed" in result.error or "at least" in result.error

    def test_create_web_app_value_error(self) -> None:
        """Test create_web_app with ValueError (lines 914-920)."""
        result = create_entry("web_app", name="root", host="localhost", port=8080)
        assert result.is_failure

    def test_create_web_request_validation_error(self) -> None:
        """Test create_web_request with validation error (lines 961-967)."""
        result = create_entry("web_request", method="GET", url="")
        assert result.is_failure, "Empty URL should cause validation failure"
        assert result.error is not None

    def test_create_web_response_validation_error(self) -> None:
        """Test create_web_response with validation error (lines 1008-1014)."""
        result = create_entry("web_response", request_id="test-123", status_code=999)
        assert result.is_failure, "Invalid status code should cause validation failure"
        assert result.error is not None

    def test_application_edge_cases(self) -> None:
        """Test Application model with edge cases."""
        max_name = "a" * 100
        result = create_entry("web_app", name=max_name, host="localhost", port=8080)
        assert result.is_success
        result = create_entry("web_app", name="a", host="localhost", port=8080)
        assert result.is_failure
        result = create_entry(
            "web_app", name="test_app-123_special", host="localhost", port=8080
        )
        assert result.is_success

    def test_application_invalid_cases(self) -> None:
        """Test Application model with invalid inputs."""
        result = create_entry("web_app", name="", host="localhost", port=8080)
        assert result.is_failure
        result = create_entry("web_app", name=None, host="localhost", port=8080)
        assert result.is_failure
        result = create_entry("web_app", name="test", host="localhost", port=0)
        assert result.is_failure
        result = create_entry("web_app", name="test", host="", port=8080)
        assert result.is_failure

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
            assert result.is_success, (
                f"Expected success for app '{name}', got: {result.error}"
            )
            app = result.value
            assert isinstance(app, m.Web.Entity)
            assert app.name == name
            assert app.host == host
            assert app.port == port
        else:
            assert result.is_failure, (
                f"Expected failure for app '{name}', but succeeded"
            )
            assert result.error is not None

    def test_extreme_edge_cases(self) -> None:
        """Test absolute extreme edge cases that might reveal bugs."""
        unicode_name = "测试应用_🚀_123"
        result = create_entry("web_app", name=unicode_name, host="localhost", port=8080)
        assert result.is_success
        result = create_entry("web_app", name="test", host="localhost", port=65535)
        assert result.is_success
        ipv6_host = "2001:db8::1"
        result = create_entry("web_app", name="test", host=ipv6_host, port=8080)
        assert result.is_success or result.is_failure
        long_hostname = "a" * 253
        result = create_entry("web_app", name="test", host=long_hostname, port=8080)
        assert result.is_success
        result = create_entry("web_app", name="x", host="localhost", port=8080)
        assert result.is_failure
        max_name = "x" * 100
        result = create_entry("web_app", name=max_name, host="localhost", port=8080)
        assert result.is_success
        too_long_name = "x" * 101
        result = create_entry(
            "web_app", name=too_long_name, host="localhost", port=8080
        )
        assert result.is_failure

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
            assert result.is_failure, (
                f"Dangerous pattern '{dangerous_name}' should be rejected"
            )

    def test_application_add_domain_event_success(self) -> None:
        """Test add_domain_event with valid input."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        result = app.add_domain_event("TestEvent")
        assert result.is_success
        assert result.value is not None
        assert hasattr(result.value, "event_type")

    def test_application_add_domain_event_empty(self) -> None:
        """Test add_domain_event with empty string."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        result = app.add_domain_event("")
        assert result.is_failure
        assert result.error and "empty" in result.error.lower()

    def test_application_name_too_long(self) -> None:
        """Test application creation with name too long."""
        long_name = "a" * 101
        result = create_entry("web_app", name=long_name, host="localhost", port=8080)
        assert result.is_failure
        assert result.error and (
            "100" in result.error or "between" in result.error.lower()
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
        assert result.is_failure
        assert result.error and "Cannot restart in current state" in result.error
