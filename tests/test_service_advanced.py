#!/usr/bin/env python3
"""Advanced tests for FLEXT Web Interface service functionality.

Tests error handling, edge cases, validation, and integration scenarios
to improve code coverage and ensure robust operation.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest

from flext_web import (
    FlextWebApp,
    FlextWebAppHandler,
    FlextWebAppStatus,
    FlextWebConfig,
    FlextWebProcessingError,
    FlextWebService,
    get_web_settings,
)


class TestFlextWebServiceAdvanced:
    """Advanced tests for FlextWebService functionality."""

    @pytest.fixture
    def config(self) -> FlextWebConfig:
        """Create test configuration."""
        return FlextWebConfig(
            host="localhost",
            port=8080,
            debug=True,
            secret_key="test-secret-key-32-characters-long!",
        )

    @pytest.fixture
    def service(self, config: FlextWebConfig) -> FlextWebService:
        """Create test service instance."""
        return FlextWebService(config)

    def test_service_app_registration(self, service: FlextWebService) -> None:
        """Test Flask app registration and configuration."""
        app = service.app
        assert app.config["SECRET_KEY"] == "test-secret-key-32-characters-long!"
        # Flask debug is independent of business logic debug setting
        assert service.config.debug is True

    def test_service_with_production_config(self) -> None:
        """Test service with production configuration."""
        config = FlextWebConfig(
            host="0.0.0.0",
            port=80,
            debug=False,
            secret_key="production-secret-key-very-secure-32chars!",
        )
        service = FlextWebService(config)

        # Flask debug is controlled separately from config debug
        assert service.config.debug is False
        assert service.config.is_production() is True

    def test_create_app_with_validation_error(self, service: FlextWebService) -> None:
        """Test app creation with validation errors."""
        # Test empty name
        response = service.app.test_client().post(
            "/api/v1/apps",
            json={"name": "", "port": 3000, "host": "localhost"},
        )
        assert response.status_code == 400
        data = response.get_json()
        assert not data["success"]
        assert "name" in data["message"].lower()

    def test_create_app_with_invalid_port(self, service: FlextWebService) -> None:
        """Test app creation with invalid port."""
        response = service.app.test_client().post(
            "/api/v1/apps",
            json={"name": "test-app", "port": 99999, "host": "localhost"},
        )
        assert response.status_code == 400
        data = response.get_json()
        assert not data["success"]

    def test_create_app_with_missing_fields(self, service: FlextWebService) -> None:
        """Test app creation with missing optional fields uses defaults."""
        response = service.app.test_client().post(
            "/api/v1/apps",
            json={"name": "test-app"},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"]
        # Default values should be provided
        assert data["data"]["host"] == "localhost"
        assert data["data"]["port"] == 8000

    def test_start_nonexistent_app(self, service: FlextWebService) -> None:
        """Test starting non-existent application."""
        response = service.app.test_client().post("/api/v1/apps/nonexistent/start")
        assert response.status_code == 404
        data = response.get_json()
        assert not data["success"]
        assert "not found" in data["message"].lower()

    def test_stop_nonexistent_app(self, service: FlextWebService) -> None:
        """Test stopping non-existent application."""
        response = service.app.test_client().post("/api/v1/apps/nonexistent/stop")
        assert response.status_code == 404
        data = response.get_json()
        assert not data["success"]

    def test_get_nonexistent_app(self, service: FlextWebService) -> None:
        """Test getting non-existent application."""
        response = service.app.test_client().get("/api/v1/apps/nonexistent")
        assert response.status_code == 404
        data = response.get_json()
        assert not data["success"]

    def test_invalid_json_request(self, service: FlextWebService) -> None:
        """Test API with invalid JSON."""
        response = service.app.test_client().post(
            "/api/v1/apps",
            data="invalid json",
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_service_error_handling(self, service: FlextWebService) -> None:
        """Test service error handling with mock failure."""
        with patch.object(service.handler, "create") as mock_create:
            mock_create.side_effect = FlextWebProcessingError("Mock failure")

            response = service.app.test_client().post(
                "/api/v1/apps",
                json={"name": "test-app", "port": 3000, "host": "localhost"},
            )

            # The service should return a 500 error when handler fails
            assert response.status_code == 500
            # We don't expect JSON response for unhandled exceptions
            # The error is logged but not converted to JSON API response

    def test_dashboard_with_apps(self, service: FlextWebService) -> None:
        """Test dashboard display with applications."""
        # Create test app
        service.app.test_client().post(
            "/api/v1/apps",
            json={"name": "dashboard-test", "port": 3000, "host": "localhost"},
        )

        response = service.app.test_client().get("/")
        assert response.status_code == 200
        assert b"dashboard-test" in response.data or b"1" in response.data


class TestFlextWebConfigAdvanced:
    """Advanced tests for FlextWebConfig functionality."""

    def test_config_environment_loading(self) -> None:
        """Test configuration loading from environment."""
        with patch.dict(
            "os.environ",
            {
                "FLEXT_WEB_HOST": "test-host",
                "FLEXT_WEB_PORT": "9000",
                "FLEXT_WEB_DEBUG": "false",
                "FLEXT_WEB_SECRET_KEY": "env-secret-key-32-characters-long!!",
            },
        ):
            config = FlextWebConfig()
            assert config.host == "test-host"
            assert config.port == 9000
            assert config.debug is False
            assert config.secret_key == "env-secret-key-32-characters-long!!"

    def test_config_validation_edge_cases(self) -> None:
        """Test configuration validation edge cases."""
        # Test minimum valid port
        config = FlextWebConfig(
            port=1,
            secret_key="valid-secret-key-32-characters-long!",
        )
        result = config.validate_config()
        assert result.success

        # Test maximum valid port
        config = FlextWebConfig(
            port=65535,
            secret_key="valid-secret-key-32-characters-long!",
        )
        result = config.validate_config()
        assert result.success

    def test_config_production_detection(self) -> None:
        """Test production environment detection."""
        # Test debug=False as production indicator
        config = FlextWebConfig(
            debug=False,
            secret_key="prod-secret-key-32-characters-long!!",
        )
        assert config.is_production() is True

        # Test debug=True as development indicator
        config = FlextWebConfig(
            debug=True,
            secret_key="dev-secret-key-32-characters-long!!!",
        )
        assert config.is_production() is False

    def test_config_secret_key_validation(self) -> None:
        """Test secret key validation scenarios."""
        # Test production with default key (should fail)
        config = FlextWebConfig(
            debug=False,
            secret_key="change-in-production-placeholder-key",
        )
        result = config.validate_config()
        assert result.is_failure
        assert "production" in result.error.lower()

    def test_get_web_settings_caching(self) -> None:
        """Test settings caching functionality."""
        # First call creates instance
        settings1 = get_web_settings()

        # Second call should return same instance
        settings2 = get_web_settings()

        assert settings1 is settings2


class TestFlextWebAppAdvanced:
    """Advanced tests for FlextWebApp functionality."""

    def test_app_lifecycle_complete(self) -> None:
        """Test complete application lifecycle."""
        app = FlextWebApp(
            id="lifecycle_test",
            name="lifecycle-app",
            port=4000,
            host="localhost",
            status=FlextWebAppStatus.STOPPED,
        )

        # Test initial state
        assert not app.is_running
        assert app.status == FlextWebAppStatus.STOPPED

        # Test validation
        result = app.validate_domain_rules()
        assert result.success

    def test_app_edge_case_ports(self) -> None:
        """Test application with edge case ports."""
        # Test minimum port
        app = FlextWebApp(id="min_port", name="min-port-app", port=1, host="localhost")
        result = app.validate_domain_rules()
        assert result.success

        # Test maximum port
        app = FlextWebApp(
            id="max_port",
            name="max-port-app",
            port=65535,
            host="localhost",
        )
        result = app.validate_domain_rules()
        assert result.success

    def test_app_host_variations(self) -> None:
        """Test application with different host formats."""
        hosts = ["localhost", "127.0.0.1", "0.0.0.0", "example.com"]

        for i, host in enumerate(hosts):
            app = FlextWebApp(
                id=f"host_test_{i}",
                name=f"host-app-{i}",
                port=3000 + i,
                host=host,
            )
            result = app.validate_domain_rules()
            assert result.success


class TestFlextWebAppHandlerAdvanced:
    """Advanced tests for FlextWebAppHandler functionality."""

    def test_handler_error_scenarios(self) -> None:
        """Test handler error scenarios with invalid app objects."""
        handler = FlextWebAppHandler()

        # Create a valid app first
        result = handler.create("test-app", 8000, "localhost")
        assert result.success
        app = result.data

        # Test stopping a stopped app
        result = handler.stop(app)
        # App is already stopped, so this should fail with appropriate message
        assert result.is_failure
        assert (
            "already stopped" in result.error.lower()
            or "not running" in result.error.lower()
        )

    def test_handler_duplicate_app_creation(self) -> None:
        """Test creating applications with same name but different ports."""
        handler = FlextWebAppHandler()

        # Create first app
        result1 = handler.create("duplicate-test", 5000, "localhost")
        assert result1.success

        # Create another app with same name but different port (allowed)
        result2 = handler.create("duplicate-test", 5001, "localhost")
        assert result2.success
        # Apps have same name but different ports
        assert result1.data.name == result2.data.name
        assert result1.data.port != result2.data.port

    def test_handler_app_state_transitions(self) -> None:
        """Test application state transitions."""
        handler = FlextWebAppHandler()

        # Create app
        result = handler.create("state-test", 6000, "localhost")
        assert result.success
        app = result.data

        # Start app
        result = handler.start(app)
        assert result.success
        assert result.data.status == FlextWebAppStatus.RUNNING
        running_app = result.data

        # Try to start already running app
        result = handler.start(running_app)
        assert result.is_failure
        assert "already running" in result.error.lower()

        # Stop app
        result = handler.stop(running_app)
        assert result.success
        assert result.data.status == FlextWebAppStatus.STOPPED
        stopped_app = result.data

        # Try to stop already stopped app
        result = handler.stop(stopped_app)
        assert result.is_failure
        assert (
            "already stopped" in result.error.lower()
            or "not running" in result.error.lower()
        )


class TestServiceIntegration:
    """Test service integration scenarios."""

    def test_complete_app_workflow(self) -> None:
        """Test complete application workflow through API."""
        config = FlextWebConfig(
            host="localhost",
            port=8080,
            debug=True,
            secret_key="integration-test-key-32-chars-long!",
        )
        service = FlextWebService(config)
        client = service.app.test_client()

        # 1. Create application
        response = client.post(
            "/api/v1/apps",
            json={"name": "workflow-test", "port": 7000, "host": "localhost"},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"]
        app_id = data["data"]["id"]

        # 2. List applications
        response = client.get("/api/v1/apps")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["data"]["apps"]) == 1

        # 3. Get specific application
        response = client.get(f"/api/v1/apps/{app_id}")
        assert response.status_code == 200
        data = response.get_json()
        assert data["data"]["name"] == "workflow-test"

        # 4. Start application
        response = client.post(f"/api/v1/apps/{app_id}/start")
        assert response.status_code == 200
        data = response.get_json()
        assert data["data"]["is_running"] is True

        # 5. Stop application
        response = client.post(f"/api/v1/apps/{app_id}/stop")
        assert response.status_code == 200
        data = response.get_json()
        assert data["data"]["is_running"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
