"""Unit tests for flext_web.models module.

Tests the web models functionality following flext standards.
"""

import pytest
from pydantic import ValidationError

from flext_web.constants import FlextWebConstants
from flext_web.models import FlextWebModels


class TestFlextWebModels:
    """Test suite for FlextWebModels class."""

    def test_web_app_status_enum(self) -> None:
        """Test WebAppStatus enum values."""
        assert FlextWebModels.Application.EntityStatus.STOPPED.value == "stopped"
        assert FlextWebModels.Application.EntityStatus.STARTING.value == "starting"
        assert FlextWebModels.Application.EntityStatus.RUNNING.value == "running"
        assert FlextWebModels.Application.EntityStatus.STOPPING.value == "stopping"
        assert FlextWebModels.Application.EntityStatus.ERROR.value == "error"
        assert (
            FlextWebModels.Application.EntityStatus.MAINTENANCE.value == "maintenance"
        )
        assert FlextWebModels.Application.EntityStatus.DEPLOYING.value == "deploying"

    def test_web_app_initialization_with_defaults(self) -> None:
        """Test WebApp initialization with defaults."""
        app = FlextWebModels.Application.Entity(id="test-id", name="test-app")
        assert app.id == "test-id"
        assert app.name == "test-app"
        assert app.host == FlextWebConstants.WebDefaults.HOST
        assert app.port == FlextWebConstants.WebDefaults.PORT
        assert app.status == "stopped"
        assert app.version == 1
        assert app.environment == "development"
        assert app.debug_mode is False

    def test_web_app_initialization_with_custom_values(self) -> None:
        """Test WebApp initialization with custom values."""
        app = FlextWebModels.Application.Entity(
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
        # Valid name
        app = FlextWebModels.Application.Entity(id="test-id", name="valid-app-name")
        assert app.name == "valid-app-name"

        # Name too short
        with pytest.raises(ValidationError):
            FlextWebModels.Application.Entity(id="test-id", name="ab")

        # Name too long
        with pytest.raises(ValidationError):
            FlextWebModels.Application.Entity(id="test-id", name="a" * 101)

    def test_web_app_name_reserved_validation(self) -> None:
        """Test WebApp name validation for reserved names."""
        reserved_names = ["REDACTED_LDAP_BIND_PASSWORD", "root", "api", "system", "config", "health"]
        for name in reserved_names:
            with pytest.raises(ValidationError):
                FlextWebModels.Application.Entity(id="test-id", name=name)

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
                FlextWebModels.Application.Entity(id="test-id", name=name)

    def test_web_app_port_validation(self) -> None:
        """Test WebApp port validation."""
        # Valid port
        app = FlextWebModels.Application.Entity(
            id="test-id", name="test-app", port=8080
        )
        assert app.port == 8080

        # Port too low
        with pytest.raises(ValidationError):
            FlextWebModels.Application.Entity(id="test-id", name="test-app", port=0)

        # Port too high
        with pytest.raises(ValidationError):
            FlextWebModels.Application.Entity(id="test-id", name="test-app", port=70000)

    def test_web_app_status_validation(self) -> None:
        """Test WebApp status validation."""
        # Valid status
        app = FlextWebModels.Application.Entity(
            id="test-id", name="test-app", status="running"
        )
        assert app.status == "running"

        # Invalid status
        with pytest.raises(ValidationError):
            FlextWebModels.Application.Entity(
                id="test-id", name="test-app", status="invalid"
            )

    def test_web_app_computed_fields(self) -> None:
        """Test WebApp computed fields."""
        app = FlextWebModels.Application.Entity(
            id="test-id", name="test-app", status="running"
        )
        assert app.is_running is True
        assert app.is_healthy is True
        assert app.can_start is False
        assert app.can_stop is True
        assert app.can_restart is True

    def test_web_app_url_generation(self) -> None:
        """Test WebApp URL generation."""
        app = FlextWebModels.Application.Entity(
            id="test-id", name="test-app", host="localhost", port=8080
        )
        assert app.url == "http://localhost:8080"

        # HTTPS port
        app_https = FlextWebModels.Application.Entity(
            id="test-id", name="test-app", host="localhost", port=443
        )
        assert app_https.url == "https://localhost:443"

    def test_web_app_business_rules_validation(self) -> None:
        """Test WebApp business rules validation."""
        app = FlextWebModels.Application.Entity(
            id="test-id", name="test-app", host="localhost", port=8080
        )
        result = app.validate_business_rules()
        assert result.is_success

    def test_web_app_start_success(self) -> None:
        """Test WebApp start operation."""
        app = FlextWebModels.Application.Entity(
            id="test-id", name="test-app", status="stopped"
        )
        result = app.start()
        assert result.is_success
        started_app = result.unwrap()
        assert started_app.status == "running"

    def test_web_app_start_already_running(self) -> None:
        """Test WebApp start when already running."""
        app = FlextWebModels.Application.Entity(
            id="test-id", name="test-app", status="running"
        )
        result = app.start()
        assert result.is_failure
        assert result.error is not None and "already running" in result.error

    def test_web_app_stop_success(self) -> None:
        """Test WebApp stop operation."""
        app = FlextWebModels.Application.Entity(
            id="test-id", name="test-app", status="running"
        )
        result = app.stop()
        assert result.is_success
        stopped_app = result.unwrap()
        assert stopped_app.status == "stopped"

    def test_web_app_stop_not_running(self) -> None:
        """Test WebApp stop when not running."""
        app = FlextWebModels.Application.Entity(
            id="test-id", name="test-app", status="stopped"
        )
        result = app.stop()
        assert result.is_failure
        assert result.error is not None and "not running" in result.error

    def test_web_app_restart_success(self) -> None:
        """Test WebApp restart operation."""
        app = FlextWebModels.Application.Entity(
            id="test-id", name="test-app", status="running"
        )
        result = app.restart()
        assert result.is_success
        restarted_app = result.unwrap()
        assert restarted_app.status == "running"

    def test_web_app_metrics_update(self) -> None:
        """Test WebApp metrics update."""
        app = FlextWebModels.Application.Entity(id="test-id", name="test-app")
        metrics = {"requests": 100, "errors": 5}
        app.update_metrics(metrics)
        # The update_metrics method should merge with existing metrics
        assert "requests" in app.metrics
        assert "errors" in app.metrics
        assert app.metrics["requests"] == 100
        assert app.metrics["errors"] == 5

    def test_web_app_health_status(self) -> None:
        """Test WebApp health status."""
        app = FlextWebModels.Application.Entity(
            id="test-id", name="test-app", status="running"
        )
        health = app.get_health_status()
        assert "status" in health
        assert "is_running" in health
        assert "is_healthy" in health
        assert "url" in health
        assert health["status"] == "running"

    def test_web_app_to_dict(self) -> None:
        """Test WebApp to_dict conversion."""
        app = FlextWebModels.Application.Entity(
            id="test-id", name="test-app", host="localhost", port=8080
        )
        app_dict = app.to_dict()
        assert app_dict["id"] == "test-id"
        assert app_dict["name"] == "test-app"
        assert app_dict["host"] == "localhost"
        assert app_dict["port"] == 8080

    def test_web_app_string_representation(self) -> None:
        """Test WebApp string representation."""
        app = FlextWebModels.Application.Entity(
            id="test-id",
            name="test-app",
            host="localhost",
            port=8080,
            status="running",
        )
        assert "test-app" in str(app)
        assert "localhost:8080" in str(app)
        assert "running" in str(app)

    def test_web_request_initialization(self) -> None:
        """Test WebRequest initialization."""
        request = FlextWebModels.WebRequest(
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
        response = FlextWebModels.WebResponse(
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
        config = FlextWebModels.Application.EntityConfig(
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
        config = FlextWebModels.AppConfig(
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
        app_data = {"name": "test-app", "host": "localhost", "port": 8080}
        result = FlextWebModels.create_web_app(app_data)
        assert result.is_success
        app = result.unwrap()
        assert app.name == "test-app"
        assert app.host == "localhost"
        assert app.port == 8080

    def test_create_web_request_factory(self) -> None:
        """Test create_web_request factory method."""
        result = FlextWebModels.create_web_request(
            "POST",
            "http://localhost:8080/api/test",
            headers={"Content-Type": "application/json"},
            body='{"test": "data"}',
        )
        assert result.is_success
        request = result.unwrap()
        assert request.method == "POST"
        assert request.url == "http://localhost:8080/api/test"

    def test_create_web_response_factory(self) -> None:
        """Test create_web_response factory method."""
        result = FlextWebModels.create_web_response(
            "req-123",
            201,
            headers={"Content-Type": "application/json"},
            body='{"id": 1}',
        )
        assert result.is_success
        response = result.unwrap()
        assert response.request_id == "req-123"
        assert response.status_code == 201
