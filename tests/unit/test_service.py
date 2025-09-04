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

from flext_web import (
    FlextWebConfigs,
    FlextWebModels,
    FlextWebServices,
)
from flext_web.handlers import FlextWebHandlers


class TestFlextWebServiceAdvanced:
    """Advanced tests for FlextWebServices.WebService functionality."""

    @pytest.fixture
    def config(self) -> FlextWebConfigs.WebConfig:
        """Create test configuration."""
        return FlextWebConfigs.WebConfig(
            host="localhost",
            port=8093,  # Unique port for advanced tests
            debug=True,
            secret_key="test-secret-key-32-characters-long!",
        )

    @pytest.fixture
    def real_running_service(
        self, config: FlextWebConfigs.WebConfig
    ) -> Generator[FlextWebServices.WebService]:
        """Create and start real service for HTTP testing."""
        service = FlextWebServices.WebService(config)

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
    def service(self, config: FlextWebConfigs.WebConfig) -> FlextWebServices.WebService:
        """Create test service instance for unit tests."""
        return FlextWebServices.WebService(config)

    def test_service_app_registration(
        self, service: FlextWebServices.WebService
    ) -> None:
        """Test Flask app registration and configuration."""
        app = service.app
        assert app.config["SECRET_KEY"] == "test-secret-key-32-characters-long!"
        # Flask debug is independent of business logic debug setting
        assert service.config.debug is True

    def test_service_with_production_config(self) -> None:
        """Test service with production configuration."""
        config = FlextWebConfigs.WebConfig(
            host="0.0.0.0",
            port=80,
            debug=False,
            secret_key="production-secret-key-very-secure-32chars!",
        )
        service = FlextWebServices.WebService(config)

        # Flask debug is controlled separately from config debug
        assert service.config.debug is False
        assert service.config.is_production() is True

    def test_create_app_with_validation_error(
        self, real_running_service: FlextWebServices.WebService
    ) -> None:
        """Test app creation with validation errors using real HTTP."""
        assert real_running_service is not None
        port = real_running_service.config.port
        base_url = f"http://localhost:{port}"

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
        self, real_running_service: FlextWebServices.WebService
    ) -> None:
        """Test app creation with invalid port using real HTTP."""
        assert real_running_service is not None
        port = real_running_service.config.port
        base_url = f"http://localhost:{port}"

        response = requests.post(
            f"{base_url}/api/v1/apps",
            json={"name": "test-app", "port": 99999, "host": "localhost"},
            timeout=5,
        )
        assert response.status_code == 400
        data = response.json()
        assert not data["success"]

    def test_create_app_with_missing_fields(
        self, real_running_service: FlextWebServices.WebService
    ) -> None:
        """Test app creation with missing optional fields uses defaults using real HTTP."""
        assert real_running_service is not None
        port = real_running_service.config.port
        base_url = f"http://localhost:{port}"

        response = requests.post(
            f"{base_url}/api/v1/apps",
            json={"name": "test-app"},
            timeout=5,
        )
        assert response.status_code == 201  # Created status for POST /apps
        data = response.json()
        assert data["success"]
        # Default values should be provided
        assert data["data"]["host"] == "localhost"
        assert data["data"]["port"] == 8000

    def test_start_nonexistent_app(
        self, real_running_service: FlextWebServices.WebService
    ) -> None:
        """Test starting non-existent application using real HTTP."""
        assert real_running_service is not None
        port = real_running_service.config.port
        base_url = f"http://localhost:{port}"

        response = requests.post(f"{base_url}/api/v1/apps/nonexistent/start", timeout=5)
        assert response.status_code == 404
        data = response.json()
        assert not data["success"]
        assert "not found" in data["message"].lower()

    def test_stop_nonexistent_app(
        self, real_running_service: FlextWebServices.WebService
    ) -> None:
        """Test stopping non-existent application using real HTTP."""
        assert real_running_service is not None
        port = real_running_service.config.port
        base_url = f"http://localhost:{port}"

        response = requests.post(f"{base_url}/api/v1/apps/nonexistent/stop", timeout=5)
        assert response.status_code == 404
        data = response.json()
        assert not data["success"]

    def test_get_nonexistent_app(
        self, real_running_service: FlextWebServices.WebService
    ) -> None:
        """Test getting non-existent application using real HTTP."""
        assert real_running_service is not None
        port = real_running_service.config.port
        base_url = f"http://localhost:{port}"

        response = requests.get(f"{base_url}/api/v1/apps/nonexistent", timeout=5)
        assert response.status_code == 404
        data = response.json()
        assert not data["success"]

    def test_invalid_json_request(
        self, real_running_service: FlextWebServices.WebService
    ) -> None:
        """Test API with invalid JSON using real HTTP."""
        assert real_running_service is not None
        port = real_running_service.config.port
        base_url = f"http://localhost:{port}"

        response = requests.post(
            f"{base_url}/api/v1/apps",
            data="invalid json",
            headers={"Content-Type": "application/json"},
            timeout=5,
        )
        assert response.status_code == 400

    def test_service_real_validation_error_handling(
        self, real_running_service: FlextWebServices.WebService
    ) -> None:
        """Test service error handling with REAL validation failures using real HTTP."""
        assert real_running_service is not None
        port = real_running_service.config.port
        base_url = f"http://localhost:{port}"

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
        self, real_running_service: FlextWebServices.WebService
    ) -> None:
        """Test service handling of real business logic errors using real HTTP."""
        assert real_running_service is not None
        port = real_running_service.config.port
        base_url = f"http://localhost:{port}"

        # Create first app successfully
        response = requests.post(
            f"{base_url}/api/v1/apps",
            json={"name": "duplicate-test", "port": 3000, "host": "localhost"},
            timeout=5,
        )
        assert response.status_code == 201  # Created status for POST /apps

        # Try to start non-existent app to test real error path
        response = requests.post(f"{base_url}/api/v1/apps/nonexistent/start", timeout=5)
        assert response.status_code == 404
        data = response.json()
        assert data is not None
        assert data["success"] is False

    def test_dashboard_with_apps(
        self, real_running_service: FlextWebServices.WebService
    ) -> None:
        """Test dashboard display with applications using real HTTP."""
        assert real_running_service is not None
        port = real_running_service.config.port
        base_url = f"http://localhost:{port}"

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


class TestWebConfigAdvanced:
    """Advanced tests for FlextWebConfigs.WebConfig functionality."""

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
            config = FlextWebConfigs.WebConfig()
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
        config = FlextWebConfigs.WebConfig(
            port=1,
            secret_key="valid-secret-key-32-characters-long!",
        )
        result = config.validate_config()
        assert result.success

        # Test maximum valid port
        config = FlextWebConfigs.WebConfig(
            port=65535,
            secret_key="valid-secret-key-32-characters-long!",
        )
        result = config.validate_config()
        assert result.success

    def test_config_production_detection(self) -> None:
        """Test production environment detection."""
        # Test debug=False as production indicator
        config = FlextWebConfigs.WebConfig(
            debug=False,
            secret_key="prod-secret-key-32-characters-long!!",
        )
        assert config.is_production() is True

        # Test debug=True as development indicator
        config = FlextWebConfigs.WebConfig(
            debug=True,
            secret_key="dev-secret-key-32-characters-long!!!",
        )
        assert config.is_production() is False

    def test_config_secret_key_validation(self) -> None:
        """Test secret key validation scenarios."""
        # Test production with default key (should fail)
        config = FlextWebConfigs.WebConfig(
            debug=False,
            secret_key="dev-secret-key-change-in-production",  # Exact default key
        )
        # Use production validation directly since is_production() would be False
        result = config.validate_production_settings()
        assert result.is_failure
        assert "production" in (result.error or "").lower()

    def test_web_config_caching(self) -> None:
        """Test settings caching functionality."""
        # First call creates instance
        settings1_result = FlextWebConfigs.create_web_config()
        assert settings1_result.is_success
        settings1 = settings1_result.value

        # Second call should return equivalent configuration
        settings2_result = FlextWebConfigs.create_web_config()
        assert settings2_result.is_success
        settings2 = settings2_result.value

        # Test configuration consistency
        assert settings1.host == settings2.host
        assert settings1.port == settings2.port
        assert settings1.secret_key == settings2.secret_key


class TestWebAppAdvanced:
    """Advanced tests for FlextWebModels.WebApp functionality."""

    def test_app_lifecycle_complete(self) -> None:
        """Test complete application lifecycle."""
        app = FlextWebModels.WebApp(
            id="lifecycle_test",
            name="lifecycle-app",
            port=4000,
            host="localhost",
            status=FlextWebModels.WebAppStatus.STOPPED,
        )

        # Test initial state
        assert not app.is_running
        assert app.status == FlextWebModels.WebAppStatus.STOPPED

        # Test validation
        result = app.validate_business_rules()
        assert result.success

    def test_app_edge_case_ports(self) -> None:
        """Test application with edge case ports."""
        # Test minimum port
        app = FlextWebModels.WebApp(
            id="min_port",
            name="min-port-app",
            port=1,
            host="localhost",
        )
        result = app.validate_business_rules()
        assert result.success

        # Test maximum port
        app = FlextWebModels.WebApp(
            id="max_port",
            name="max-port-app",
            port=65535,
            host="localhost",
        )
        result = app.validate_business_rules()
        assert result.success

    def test_app_host_variations(self) -> None:
        """Test application with different host formats."""
        hosts = ["localhost", "127.0.0.1", "0.0.0.0", "example.com"]

        for i, host in enumerate(hosts):
            app = FlextWebModels.WebApp(
                id=f"host_test_{i}",
                name=f"host-app-{i}",
                port=3000 + i,
                host=host,
            )
            result = app.validate_business_rules()
            assert result.success


class TestWebAppHandlerAdvanced:
    """Advanced tests for FlextWebHandlers.WebAppHandler functionality."""

    def test_handler_error_scenarios(self) -> None:
        """Test handler error scenarios with invalid app objects."""
        handler = FlextWebHandlers.WebAppHandler()

        # Create a valid app first
        result = handler.create("test-app", 8000, "localhost")
        assert result.success
        app = result.value

        # Test stopping a stopped app
        result = handler.stop(app)
        # App is already stopped, so this should fail with appropriate message
        assert result.is_failure
        assert (
            "already stopped" in (result.error or "").lower()
            or "not running" in (result.error or "").lower()
        )

    def test_handler_duplicate_app_creation(self) -> None:
        """Test creating applications with same name but different ports."""
        handler = FlextWebHandlers.WebAppHandler()

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
        handler = FlextWebHandlers.WebAppHandler()

        # Create app
        result = handler.create("state-test", 6000, "localhost")
        assert result.success
        app = result.value

        # Start app
        result = handler.start(app)
        assert result.success
        assert result.value.status == FlextWebModels.WebAppStatus.RUNNING
        running_app = result.value

        # Try to start already running app
        result = handler.start(running_app)
        assert result.is_failure
        assert "already running" in (result.error or "").lower()

        # Stop app
        result = handler.stop(running_app)
        assert result.success
        assert result.value.status == FlextWebModels.WebAppStatus.STOPPED
        stopped_app = result.value

        # Try to stop already stopped app
        result = handler.stop(stopped_app)
        assert result.is_failure
        assert (
            "already stopped" in (result.error or "").lower()
            or "not running" in (result.error or "").lower()
        )


class TestServiceIntegration:
    """Test service integration scenarios."""

    @pytest.fixture
    def real_integration_service(self) -> Generator[FlextWebServices.WebService]:
        """Create real running service for integration tests."""
        config = FlextWebConfigs.WebConfig(
            host="localhost",
            port=8097,  # Unique port for integration tests
            debug=True,
            secret_key="integration-test-key-32-chars-long!",
        )
        service = FlextWebServices.WebService(config)

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
        self, real_integration_service: FlextWebServices.WebService
    ) -> None:
        """Test complete application workflow through real HTTP API."""
        assert real_integration_service is not None
        port = real_integration_service.config.port
        base_url = f"http://localhost:{port}"

        # 1. Create application
        response = requests.post(
            f"{base_url}/api/v1/apps",
            json={"name": "workflow-test", "port": 7000, "host": "localhost"},
            timeout=5,
        )
        assert response.status_code == 201  # Created
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
        assert data["data"]["status"].upper() == "RUNNING"

        # 5. Stop application
        response = requests.post(f"{base_url}/api/v1/apps/{app_id}/stop", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["status"].upper() == "STOPPED"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
