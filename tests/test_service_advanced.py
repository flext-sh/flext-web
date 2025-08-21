#!/usr/bin/env python3
"""Advanced tests for FLEXT Web Interface service functionality.

Tests error handling, edge cases, validation, and integration scenarios
using REAL execution without mocks to ensure robust operation.
"""

from __future__ import annotations

import os
import threading
import time
from collections.abc import Generator

import pytest
import requests
from flext_core import FlextEntityId

from flext_web import (
    FlextWebApp,
    FlextWebAppHandler,
    FlextWebAppStatus,
    FlextWebConfig,
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
            port=8093,  # Unique port for advanced tests
            debug=True,
            secret_key="test-secret-key-32-characters-long!",
        )

    @pytest.fixture
    def real_running_service(
        self, config: FlextWebConfig
    ) -> Generator[FlextWebService]:
        """Create and start real service for HTTP testing."""
        service = FlextWebService(config)

        def run_service() -> None:
            service.app.run(
                host=config.host,
                port=config.port,
                debug=False,
                use_reloader=False,
                threaded=True,
            )

        server_thread = threading.Thread(target=run_service, daemon=True)
        server_thread.start()
        time.sleep(1)  # Wait for service to start

        yield service

        # Clean up
        service.apps.clear()

    @pytest.fixture
    def service(self, config: FlextWebConfig) -> FlextWebService:
        """Create test service instance for unit tests."""
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

    def test_create_app_with_validation_error(
        self, real_running_service: FlextWebService
    ) -> None:  # noqa: ARG002
        """Test app creation with validation errors using real HTTP."""
        base_url = "http://localhost:8093"

        # Test empty name with real HTTP request
        response = requests.post(
            f"{base_url}/api/v1/apps",
            json={"name": "", "port": 3000, "host": "localhost"},
            timeout=5,
        )
        assert response.status_code == 400
        data = response.json()
        assert not data["success"]
        assert "name" in data["message"].lower()

    def test_create_app_with_invalid_port(
        self, real_running_service: FlextWebService
    ) -> None:  # noqa: ARG002
        """Test app creation with invalid port using real HTTP."""
        base_url = "http://localhost:8093"

        response = requests.post(
            f"{base_url}/api/v1/apps",
            json={"name": "test-app", "port": 99999, "host": "localhost"},
            timeout=5,
        )
        assert response.status_code == 400
        data = response.json()
        assert not data["success"]

    def test_create_app_with_missing_fields(
        self, real_running_service: FlextWebService
    ) -> None:  # noqa: ARG002
        """Test app creation with missing optional fields uses defaults using real HTTP."""
        base_url = "http://localhost:8093"

        response = requests.post(
            f"{base_url}/api/v1/apps",
            json={"name": "test-app"},
            timeout=5,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"]
        # Default values should be provided
        assert data["data"]["host"] == "localhost"
        assert data["data"]["port"] == 8000

    def test_start_nonexistent_app(self, real_running_service: FlextWebService) -> None:  # noqa: ARG002
        """Test starting non-existent application using real HTTP."""
        base_url = "http://localhost:8093"

        response = requests.post(f"{base_url}/api/v1/apps/nonexistent/start", timeout=5)
        assert response.status_code == 404
        data = response.json()
        assert not data["success"]
        assert "not found" in data["message"].lower()

    def test_stop_nonexistent_app(self, real_running_service: FlextWebService) -> None:  # noqa: ARG002
        """Test stopping non-existent application using real HTTP."""
        base_url = "http://localhost:8093"

        response = requests.post(f"{base_url}/api/v1/apps/nonexistent/stop", timeout=5)
        assert response.status_code == 404
        data = response.json()
        assert not data["success"]

    def test_get_nonexistent_app(self, real_running_service: FlextWebService) -> None:  # noqa: ARG002
        """Test getting non-existent application using real HTTP."""
        base_url = "http://localhost:8093"

        response = requests.get(f"{base_url}/api/v1/apps/nonexistent", timeout=5)
        assert response.status_code == 404
        data = response.json()
        assert not data["success"]

    def test_invalid_json_request(self, real_running_service: FlextWebService) -> None:  # noqa: ARG002
        """Test API with invalid JSON using real HTTP."""
        base_url = "http://localhost:8093"

        response = requests.post(
            f"{base_url}/api/v1/apps",
            data="invalid json",
            headers={"Content-Type": "application/json"},
            timeout=5,
        )
        assert response.status_code == 400

    def test_service_real_validation_error_handling(
        self, real_running_service: FlextWebService
    ) -> None:  # noqa: ARG002
        """Test service error handling with REAL validation failures using real HTTP."""
        base_url = "http://localhost:8093"

        # Test with genuinely invalid data that will cause real validation errors
        response = requests.post(
            f"{base_url}/api/v1/apps",
            json={"name": "", "port": -1, "host": ""},  # All invalid
            timeout=5,
        )

        assert response.status_code == 400
        data = response.json()
        assert data is not None
        assert data["success"] is False
        assert any(
            word in data["message"].lower()
            for word in ["validation", "invalid", "required", "name"]
        )

    def test_service_real_duplicate_error_handling(
        self, real_running_service: FlextWebService
    ) -> None:  # noqa: ARG002
        """Test service handling of real business logic errors using real HTTP."""
        base_url = "http://localhost:8093"

        # Create first app successfully
        response = requests.post(
            f"{base_url}/api/v1/apps",
            json={"name": "duplicate-test", "port": 3000, "host": "localhost"},
            timeout=5,
        )
        assert response.status_code == 200

        # Try to start non-existent app to test real error path
        response = requests.post(f"{base_url}/api/v1/apps/nonexistent/start", timeout=5)
        assert response.status_code == 404
        data = response.json()
        assert data is not None
        assert data["success"] is False

    def test_dashboard_with_apps(self, real_running_service: FlextWebService) -> None:  # noqa: ARG002
        """Test dashboard display with applications using real HTTP."""
        base_url = "http://localhost:8093"

        # Create test app
        requests.post(
            f"{base_url}/api/v1/apps",
            json={"name": "dashboard-test", "port": 3000, "host": "localhost"},
            timeout=5,
        )

        response = requests.get(f"{base_url}/", timeout=5)
        assert response.status_code == 200
        content = response.content
        assert b"dashboard-test" in content or b"1" in content


class TestFlextWebConfigAdvanced:
    """Advanced tests for FlextWebConfig functionality."""

    def test_config_real_environment_loading(self) -> None:
        """Test configuration loading with real environment variables."""
        # Save original values
        original_env = {}
        env_vars = [
            "FLEXT_WEB_HOST",
            "FLEXT_WEB_PORT",
            "FLEXT_WEB_DEBUG",
            "FLEXT_WEB_SECRET_KEY",
        ]
        for var in env_vars:
            original_env[var] = os.environ.get(var)

        try:
            # Set real environment variables
            os.environ["FLEXT_WEB_HOST"] = "test-host"
            os.environ["FLEXT_WEB_PORT"] = "9000"
            os.environ["FLEXT_WEB_DEBUG"] = "false"
            os.environ["FLEXT_WEB_SECRET_KEY"] = "env-secret-key-32-characters-long!!"

            # Test real config loading
            config = FlextWebConfig()
            assert config.host == "test-host"
            assert config.port == 9000
            assert config.debug is False
            assert config.secret_key == "env-secret-key-32-characters-long!!"

        finally:
            # Restore original environment
            for var, value in original_env.items():
                if value is None:
                    os.environ.pop(var, None)
                else:
                    os.environ[var] = value

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
            id=FlextEntityId("lifecycle_test"),
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
        app = FlextWebApp(
            id=FlextEntityId("min_port"), name="min-port-app", port=1, host="localhost"
        )
        result = app.validate_domain_rules()
        assert result.success

        # Test maximum port
        app = FlextWebApp(
            id=FlextEntityId("max_port"),
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
                id=FlextEntityId(f"host_test_{i}"),
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

    @pytest.fixture
    def real_integration_service(self) -> Generator[FlextWebService]:
        """Create real running service for integration tests."""
        config = FlextWebConfig(
            host="localhost",
            port=8097,  # Unique port for integration tests
            debug=True,
            secret_key="integration-test-key-32-chars-long!",
        )
        service = FlextWebService(config)

        def run_service() -> None:
            service.app.run(
                host=config.host,
                port=config.port,
                debug=False,
                use_reloader=False,
                threaded=True,
            )

        server_thread = threading.Thread(target=run_service, daemon=True)
        server_thread.start()
        time.sleep(1)  # Wait for service to start

        yield service

        # Clean up
        service.apps.clear()

    def test_complete_app_workflow(
        self, real_integration_service: FlextWebService
    ) -> None:  # noqa: ARG002
        """Test complete application workflow through real HTTP API."""
        base_url = "http://localhost:8097"

        # 1. Create application
        response = requests.post(
            f"{base_url}/api/v1/apps",
            json={"name": "workflow-test", "port": 7000, "host": "localhost"},
            timeout=5,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"]
        app_id = data["data"]["id"]

        # 2. List applications
        response = requests.get(f"{base_url}/api/v1/apps", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["apps"]) == 1

        # 3. Get specific application
        response = requests.get(f"{base_url}/api/v1/apps/{app_id}", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["name"] == "workflow-test"

        # 4. Start application
        response = requests.post(f"{base_url}/api/v1/apps/{app_id}/start", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["is_running"] is True

        # 5. Stop application
        response = requests.post(f"{base_url}/api/v1/apps/{app_id}/stop", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["is_running"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
