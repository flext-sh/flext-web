"""Comprehensive Real Functionality Tests - NO MOCKS, REAL EXECUTION.

Tests all functionality using real Flask applications, real HTTP requests,
real service execution, and actual FlextWebApp lifecycle management.
"""

from __future__ import annotations

import os

import pytest
import requests
from flext_core.root_models import FlextEntityId

from flext_web import (
    FlextWebApp,
    FlextWebAppHandler,
    FlextWebAppStatus,
    FlextWebConfig,
    FlextWebService,
    get_web_settings,
    reset_web_settings,
)


class TestRealWebServiceExecution:
    """Test real FlextWebService execution with actual HTTP."""

    @pytest.mark.integration
    @pytest.mark.usefixtures("running_service")
    def test_real_service_health_check(self) -> None:
        """Test real health endpoint with actual HTTP request."""
        response = requests.get("http://localhost:8091/health", timeout=5)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["status"] == "healthy"
        assert "version" in data["data"]
        assert "config" in data["data"]

    @pytest.mark.integration
    @pytest.mark.usefixtures("running_service")
    def test_real_application_complete_lifecycle(self) -> None:
        """Test complete application lifecycle with real HTTP requests."""
        base_url = "http://localhost:8091"

        # 1. Create application
        create_data: dict[str, str | int] = {
            "name": "real-lifecycle-app",
            "port": 9002,
            "host": "localhost",
        }
        response = requests.post(f"{base_url}/api/v1/apps", json=create_data, timeout=5)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        app_id = data["data"]["id"]
        assert app_id == "app_real-lifecycle-app"
        assert data["data"]["name"] == "real-lifecycle-app"
        assert data["data"]["port"] == 9002
        assert data["data"]["is_running"] is False

        # 2. Get specific application
        response = requests.get(f"{base_url}/api/v1/apps/{app_id}", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "real-lifecycle-app"
        assert data["data"]["status"].upper() == "STOPPED"

        # 3. Start application
        response = requests.post(f"{base_url}/api/v1/apps/{app_id}/start", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["is_running"] is True
        assert data["data"]["status"].upper() == "RUNNING"

        # 4. Stop application
        response = requests.post(f"{base_url}/api/v1/apps/{app_id}/stop", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["is_running"] is False
        assert data["data"]["status"].upper() == "STOPPED"

    @pytest.mark.integration
    @pytest.mark.usefixtures("running_service")
    def test_real_error_handling_validation(self) -> None:
        """Test real error handling with actual invalid requests."""
        base_url = "http://localhost:8091"

        # Test creating app with invalid data
        invalid_data: dict[str, str | int] = {
            "name": "",  # Invalid empty name
            "port": 99999,  # Invalid port
            "host": "",  # Invalid empty host
        }
        response = requests.post(f"{base_url}/api/v1/apps", json=invalid_data, timeout=5)

        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert any(word in data["message"].lower() for word in ["validation", "empty", "required", "invalid"])

        # Test accessing non-existent app
        response = requests.get(f"{base_url}/api/v1/apps/nonexistent", timeout=5)
        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False
        assert "not found" in data["message"].lower()

    @pytest.mark.web
    @pytest.mark.usefixtures("running_service")
    def test_real_web_dashboard_rendering(self) -> None:
        """Test real web dashboard rendering with applications."""
        base_url = "http://localhost:8091"

        # Create test applications first
        test_apps: list[dict[str, str | int]] = [
            {"name": "dashboard-app-1", "port": 9003, "host": "localhost"},
            {"name": "dashboard-app-2", "port": 9004, "host": "localhost"},
        ]

        for app_data in test_apps:
            requests.post(f"{base_url}/api/v1/apps", json=app_data, timeout=5)

        # Test dashboard renders correctly
        response = requests.get(f"{base_url}/", timeout=5)

        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        content = response.text
        assert "FLEXT Web" in content
        assert "Total Apps" in content
        # Dashboard shows basic structure - specific app names may not be in HTML content


class TestRealDomainLogicExecution:
    """Test real domain logic execution without mocks."""

    @pytest.mark.unit
    def test_real_app_creation_and_validation(self) -> None:
        """Test real FlextWebApp creation and domain validation."""
        # Test valid app creation
        app = FlextWebApp(
            id=FlextEntityId("test_real_app"),
            name="real-test-app",
            port=8000,
            host="localhost",
        )

        assert app.id == "test_real_app"
        assert app.name == "real-test-app"
        assert app.port == 8000
        assert app.host == "localhost"
        assert app.status == FlextWebAppStatus.STOPPED
        assert app.is_running is False

        # Test real domain validation
        result = app.validate_domain_rules()
        assert result.success is True

    @pytest.mark.unit
    def test_real_app_validation_failures(self) -> None:
        """Test real domain validation with invalid data."""
        # Test invalid app with empty name
        app = FlextWebApp.model_construct(
            id=FlextEntityId("invalid_test"),
            name="",  # Empty name should fail
            port=8000,
            host="localhost",
        )

        result = app.validate_domain_rules()
        assert result.is_failure is True
        assert result.error is not None
        assert "Application name cannot be empty" in result.error

    @pytest.mark.unit
    def test_real_handler_operations(self) -> None:
        """Test real FlextWebAppHandler operations."""
        handler = FlextWebAppHandler()

        # Test real app creation
        result = handler.create("real-handler-test", 8002, "localhost")
        assert result.success is True
        app = result.data
        assert app.name == "real-handler-test"
        assert app.port == 8002
        assert app.status == FlextWebAppStatus.STOPPED

        # Test real app start
        start_result = handler.start(app)
        assert start_result.success is True
        started_app = start_result.data
        assert started_app.status == FlextWebAppStatus.RUNNING
        assert started_app.is_running is True

        # Test real app stop
        stop_result = handler.stop(started_app)
        assert stop_result.success is True
        stopped_app = stop_result.data
        assert stopped_app.status == FlextWebAppStatus.STOPPED
        assert stopped_app.is_running is False

    @pytest.mark.unit
    def test_real_handler_error_conditions(self) -> None:
        """Test real handler error conditions."""
        handler = FlextWebAppHandler()

        # Test creating app with invalid parameters
        result = handler.create("", 8080, "localhost")  # Empty name
        assert result.is_failure is True
        assert result.error is not None

        # Test invalid port
        result = handler.create("test", -1, "localhost")
        assert result.is_failure is True
        assert result.error is not None

        # Test empty host
        result = handler.create("test", 8080, "")
        assert result.is_failure is True
        assert result.error is not None


class TestRealConfigurationManagement:
    """Test real configuration management and validation."""

    @pytest.mark.unit
    def test_real_config_validation_success(self) -> None:
        """Test real configuration validation with valid data."""
        config = FlextWebConfig(
            host="localhost",
            port=8083,
            debug=True,
            secret_key="real-config-test-key-32-characters!",
        )

        result = config.validate_config()
        assert result.success is True
        assert config.is_production() is False  # debug=True
        assert config.get_server_url() == "http://localhost:8083"

    @pytest.mark.unit
    def test_real_config_validation_failures(self) -> None:
        """Test real configuration validation with invalid data."""
        # Test invalid port
        config = FlextWebConfig(
            host="localhost",
            port=8083,
            debug=False,  # Production mode
            secret_key="change-in-production-" + "x" * 32,  # Default key in production
        )

        result = config.validate_config()
        assert result.is_failure is True
        assert result.error is not None
        assert "production" in result.error.lower()

    @pytest.mark.integration
    def test_real_environment_configuration_loading(self) -> None:
        """Test real configuration loading from environment variables."""
        # Save original values
        original_env = {}
        env_vars = ["FLEXT_WEB_HOST", "FLEXT_WEB_PORT", "FLEXT_WEB_DEBUG"]
        for var in env_vars:
            original_env[var] = os.environ.get(var)

        try:
            # Set real environment variables
            os.environ["FLEXT_WEB_HOST"] = "test-host"
            os.environ["FLEXT_WEB_PORT"] = "9000"
            os.environ["FLEXT_WEB_DEBUG"] = "false"

            # Reset to force reload
            reset_web_settings()

            # Test real config loading
            config = get_web_settings()
            assert config.host == "test-host"
            assert config.port == 9000
            assert config.debug is False

        finally:
            # Restore original environment
            for var, value in original_env.items():
                if value is None:
                    os.environ.pop(var, None)
                else:
                    os.environ[var] = value
            reset_web_settings()


class TestRealServiceIntegration:
    """Test real service integration scenarios."""

    @pytest.mark.integration
    def test_real_service_with_multiple_apps(self, real_service: FlextWebService) -> None:
        """Test real service managing multiple applications."""
        client = real_service.app.test_client()

        # Create multiple applications
        apps_data: list[dict[str, str | int]] = [
            {"name": "multi-app-1", "port": 9005, "host": "localhost"},
            {"name": "multi-app-2", "port": 9006, "host": "localhost"},
            {"name": "multi-app-3", "port": 9007, "host": "localhost"},
        ]

        created_apps = []
        for app_data in apps_data:
            response = client.post("/api/v1/apps", json=app_data)
            assert response.status_code == 200
            data = response.get_json()
            created_apps.append(data["data"]["id"])

        # List all applications
        response = client.get("/api/v1/apps")
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert len(data["data"]["apps"]) == 3

        # Test operations on each app
        for app_id in created_apps:
            # Start app
            response = client.post(f"/api/v1/apps/{app_id}/start")
            assert response.status_code == 200

            # Verify running
            response = client.get(f"/api/v1/apps/{app_id}")
            assert response.status_code == 200
            data = response.get_json()
            assert data["data"]["status"].upper() == "RUNNING"

            # Stop app
            response = client.post(f"/api/v1/apps/{app_id}/stop")
            assert response.status_code == 200

    @pytest.mark.integration
    def test_real_service_error_recovery(self, real_service: FlextWebService) -> None:
        """Test real service error recovery scenarios."""
        client = real_service.app.test_client()

        # Create valid app
        response = client.post("/api/v1/apps", json={
            "name": "error-recovery-app",
            "port": 9008,
            "host": "localhost",
        })
        assert response.status_code == 200
        data = response.get_json()
        app_id = data["data"]["id"]

        # Start app
        response = client.post(f"/api/v1/apps/{app_id}/start")
        assert response.status_code == 200

        # Try to start already running app (should fail gracefully)
        response = client.post(f"/api/v1/apps/{app_id}/start")
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "already running" in data["message"].lower()

        # Stop app
        response = client.post(f"/api/v1/apps/{app_id}/stop")
        assert response.status_code == 200

        # Try to stop already stopped app (should fail gracefully)
        response = client.post(f"/api/v1/apps/{app_id}/stop")
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "already stopped" in data["message"].lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
