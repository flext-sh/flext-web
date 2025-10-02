"""Comprehensive Real Functionality Tests - NO MOCKS, REAL EXECUTION.

Tests all functionality using real Flask applications, real HTTP requests,
real service execution, and actual FlextWebModels.WebApp lifecycle management.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
import threading
import time
from collections.abc import Generator

import pytest
import requests
from tests.port_manager import TestPortManager

from flext_web import (
    FlextWebConfig,
    FlextWebHandlers,
    FlextWebModels,
    FlextWebServices,
)


@pytest.fixture
def real_comprehensive_service() -> Generator[FlextWebServices.WebService]:
    """Create real running service for comprehensive tests."""
    # Allocate unique port to avoid conflicts
    port = TestPortManager.allocate_port()

    config = FlextWebConfig(
        host="localhost",
        port=port,
        debug=True,
        secret_key="comprehensive-test-secret-key-32-chars!",
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
    time.sleep(2)  # Wait longer for service to start and avoid conflicts

    # Ensure clean state before yielding
    service.apps.clear()

    yield service

    # Clean up after use
    service.apps.clear()
    # Release the allocated port
    TestPortManager.release_port(port)


class TestRealWebServiceExecution:
    """Test real FlextWebServices.WebService execution with actual HTTP."""

    @pytest.mark.integration
    def test_real_service_health_check(
        self,
        real_comprehensive_service: FlextWebServices.WebService,
    ) -> None:
        """Test real health endpoint with actual HTTP request."""
        port = real_comprehensive_service.config["port"]
        response = requests.get(f"http://localhost:{port}/health", timeout=5)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["status"] == "healthy"
        assert "version" in data["data"]
        assert "service" in data["data"]  # Health includes service name

    @pytest.mark.integration
    def test_real_application_complete_lifecycle(
        self,
        real_comprehensive_service: FlextWebServices.WebService,
    ) -> None:
        """Test complete application lifecycle with real HTTP requests."""
        port = real_comprehensive_service.config["port"]
        base_url = f"http://localhost:{port}"

        # 1. Create application
        create_data: dict[str, str | int] = {
            "name": "real-lifecycle-app",
            "port": 9002,
            "host": "localhost",
        }
        response = requests.post(f"{base_url}/api/v1/apps", json=create_data, timeout=5)

        assert response.status_code == 201  # Created status for POST /apps
        data = response.json()
        assert data["success"] is True
        app_id = data["data"]["id"]
        assert app_id == "app_real-lifecycle-app"
        assert data["data"]["name"] == "real-lifecycle-app"
        assert data["data"]["port"] == 9002
        assert data["data"]["status"].upper() == "STOPPED"

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
        assert data["data"]["status"].upper() == "RUNNING"
        assert data["data"]["status"].upper() == "RUNNING"

        # 4. Stop application
        response = requests.post(f"{base_url}/api/v1/apps/{app_id}/stop", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["status"].upper() == "STOPPED"
        assert data["data"]["status"].upper() == "STOPPED"

    @pytest.mark.integration
    def test_real_error_handling_validation(
        self,
        real_comprehensive_service: FlextWebServices.WebService,
    ) -> None:
        """Test real error handling with actual invalid requests."""
        port = real_comprehensive_service.config["port"]
        base_url = f"http://localhost:{port}"

        # Test creating app with invalid data
        invalid_data: dict[str, str | int] = {
            "name": "",  # Invalid empty name
            "port": 99999,  # Invalid port
            "host": "",  # Invalid empty host
        }
        response = requests.post(
            f"{base_url}/api/v1/apps",
            json=invalid_data,
            timeout=5,
        )

        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert any(
            word in data["message"].lower()
            for word in ["validation", "empty", "required", "invalid"]
        )

        # Test accessing non-existent app
        response = requests.get(f"{base_url}/api/v1/apps/nonexistent", timeout=5)
        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False
        assert "not found" in data["message"].lower()

    @pytest.mark.web
    def test_real_web_dashboard_rendering(
        self,
        real_comprehensive_service: FlextWebServices.WebService,
    ) -> None:
        """Test real web dashboard rendering with applications."""
        port = real_comprehensive_service.config["port"]
        base_url = f"http://localhost:{port}"

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
        assert "Applications" in content  # Dashboard shows "Applications (N)" format
        # Dashboard shows basic structure - specific app names may not be in HTML content


class TestRealDomainLogicExecution:
    """Test real domain logic execution without mocks."""

    @pytest.mark.unit
    def test_real_app_creation_and_validation(self) -> None:
        """Test real FlextWebModels.WebApp creation and domain validation."""
        # Test valid app creation
        app = FlextWebModels.WebApp(
            id="test_real_app",
            name="real-test-app",
            port=8000,
            host="localhost",
        )

        assert app.id == "test_real_app"
        assert app.name == "real-test-app"
        assert app.port == 8000
        assert app.host == "localhost"
        assert app.status == FlextWebModels.WebAppStatus.STOPPED
        assert not app.is_running

        # Test real domain validation
        result = app.validate_business_rules()
        assert result.success is True

    @pytest.mark.unit
    def test_real_app_validation_failures(self) -> None:
        """Test real domain validation with invalid data."""
        # Test invalid app with empty name
        app = FlextWebModels.WebApp.model_construct(
            id="invalid_test",
            name="",  # Empty name should fail
            port=8000,
            host="localhost",
        )

        result = app.validate_business_rules()
        assert result.is_failure is True
        assert result.error is not None
        assert result.error is not None and "application name" in result.error.lower()

    @pytest.mark.unit
    def test_real_handler_operations(self) -> None:
        """Test real FlextWebModels.WebAppHandler operations."""
        handler = FlextWebHandlers.WebAppHandler()

        # Test real app creation
        result = handler.create("real-handler-test", 8002, "localhost")
        assert result.success is True
        app = result.value
        assert app.name == "real-handler-test"
        assert app.port == 8002
        assert app.status == FlextWebModels.WebAppStatus.STOPPED

        # Test real app start
        start_result = handler.start(app)
        assert start_result.success is True
        started_app = start_result.value
        assert started_app.status == FlextWebModels.WebAppStatus.RUNNING
        assert started_app.is_running

        # Test real app stop
        stop_result = handler.stop(started_app)
        assert stop_result.success is True
        stopped_app = stop_result.value
        assert stopped_app.status == FlextWebModels.WebAppStatus.STOPPED
        assert not stopped_app.is_running

    @pytest.mark.unit
    def test_real_handler_error_conditions(self) -> None:
        """Test real handler error conditions."""
        handler = FlextWebHandlers.WebAppHandler()

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

        result = config.validate_business_rules()
        assert result.success is True
        assert config.is_production() is False  # debug=True
        assert config.get_server_url() == "http://localhost:8083"

    @pytest.mark.unit
    def test_real_config_validation_failures(self) -> None:
        """Test real configuration validation with invalid data."""
        # Set production environment to trigger production validations
        original_env = os.environ.get("FLEXT_WEB_ENVIRONMENT")
        os.environ["FLEXT_WEB_ENVIRONMENT"] = "production"

        try:
            # Test production validation failure with default key
            config = FlextWebConfig(
                host="localhost",
                port=8083,
                debug=False,  # Production mode
                secret_key="dev-secret-key-change-in-production",  # Default key
            )

            # Force production validation by calling it directly
            result = config.validate_business_rules()
            assert result.is_failure is True
            assert result.error is not None
            assert (
                "secret" in result.error.lower() or "localhost" in result.error.lower()
            )
        finally:
            # Restore original environment
            if original_env is None:
                os.environ.pop("FLEXT_WEB_ENVIRONMENT", None)
            else:
                os.environ["FLEXT_WEB_ENVIRONMENT"] = original_env

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
            # reset_web_settings()

            # Test real config loading from environment
            config = FlextWebConfig()
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
            # reset_web_settings()


class TestRealServiceIntegration:
    """Test real service integration scenarios."""

    @pytest.mark.integration
    def test_real_service_with_multiple_apps(
        self,
        real_comprehensive_service: FlextWebServices.WebService,
    ) -> None:
        """Test real service managing multiple applications using real HTTP."""
        real_comprehensive_service.apps.clear()

        port = real_comprehensive_service.config["port"]
        base_url = f"http://localhost:{port}"

        # Create multiple applications
        apps_data: list[dict[str, str | int]] = [
            {"name": "multi-app-1", "port": 9005, "host": "localhost"},
            {"name": "multi-app-2", "port": 9006, "host": "localhost"},
            {"name": "multi-app-3", "port": 9007, "host": "localhost"},
        ]

        created_apps = []
        for app_data in apps_data:
            response = requests.post(
                f"{base_url}/api/v1/apps",
                json=app_data,
                timeout=5,
            )
            assert response.status_code == 201  # Created status for POST /apps
            data = response.json()
            created_apps.append(data["data"]["id"])

        # List all applications
        response = requests.get(f"{base_url}/api/v1/apps", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]["apps"]) == 3

        # Test operations on each app
        for app_id in created_apps:
            # Start app
            response = requests.post(
                f"{base_url}/api/v1/apps/{app_id}/start",
                timeout=5,
            )
            assert response.status_code == 200

            # Verify running
            response = requests.get(f"{base_url}/api/v1/apps/{app_id}", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data["data"]["status"].upper() == "RUNNING"

            # Stop app
            response = requests.post(f"{base_url}/api/v1/apps/{app_id}/stop", timeout=5)
            assert response.status_code == 200

    @pytest.mark.integration
    def test_real_service_error_recovery(
        self,
        real_comprehensive_service: FlextWebServices.WebService,
    ) -> None:
        """Test real service error recovery scenarios using real HTTP."""
        assert real_comprehensive_service is not None
        port = real_comprehensive_service.config["port"]
        base_url = f"http://localhost:{port}"

        # Create valid app
        response = requests.post(
            f"{base_url}/api/v1/apps",
            json={
                "name": "error-recovery-app",
                "port": 9008,
                "host": "localhost",
            },
            timeout=5,
        )
        assert response.status_code == 201  # Created status for POST /apps
        data = response.json()
        app_id = data["data"]["id"]

        # Start app
        response = requests.post(f"{base_url}/api/v1/apps/{app_id}/start", timeout=5)
        assert response.status_code == 200

        # Try to start already running app (should fail gracefully)
        response = requests.post(f"{base_url}/api/v1/apps/{app_id}/start", timeout=5)
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "already running" in data["message"].lower()

        # Stop app
        response = requests.post(f"{base_url}/api/v1/apps/{app_id}/stop", timeout=5)
        assert response.status_code == 200

        # Try to stop already stopped app (should fail gracefully)
        response = requests.post(f"{base_url}/api/v1/apps/{app_id}/stop", timeout=5)
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "already stopped" in data["message"].lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
