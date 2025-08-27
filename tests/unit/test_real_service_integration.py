"""Real Service Integration Tests - NO MOCKS, REAL EXECUTION.

Executes real FlextWebService instances to validate functionality.
Tests actual HTTP endpoints, real Flask integration, and genuine error handling.
"""

from __future__ import annotations

import threading
import time
from typing import TYPE_CHECKING

import pytest
import requests
from flext_core import FlextEntityId
from tests.port_manager import TestPortManager

from flext_web import (
    FlextWebConfig,
    FlextWebService,
    get_web_settings,
    reset_web_settings,
)
from flext_web.handlers import FlextWebAppHandler
from flext_web.models import FlextWebApp, FlextWebAppStatus

if TYPE_CHECKING:
    from collections.abc import Generator


class TestRealServiceExecution:
    """Test real FlextWebService execution without mocks."""

    @pytest.fixture
    def real_config(self) -> FlextWebConfig:
        """Create real test configuration."""
        # Allocate unique port to avoid conflicts
        port = TestPortManager.allocate_port()
        return FlextWebConfig(
            host="localhost",
            port=port,
            debug=True,
            secret_key="real-test-secret-key-32-characters!",
        )

    @pytest.fixture
    def running_service_integration(
        self, real_config: FlextWebConfig
    ) -> Generator[FlextWebService]:
        """Start real service in background thread for integration tests."""
        # Use different unique port for integration tests
        integration_port = TestPortManager.allocate_port()
        integration_config = FlextWebConfig(
            host=real_config.host,
            port=integration_port,
            debug=real_config.debug,
            secret_key=real_config.secret_key,
        )

        service = FlextWebService(integration_config)

        # Start service in background thread
        def run_service() -> None:
            service.app.run(
                host=integration_config.host,
                port=integration_config.port,
                debug=False,  # Disable debug for clean testing
                use_reloader=False,
                threaded=True,
            )

        server_thread = threading.Thread(target=run_service, daemon=True)
        server_thread.start()

        # Wait for service to start
        time.sleep(2)

        yield service

        # Clean up service state after each test
        service.apps.clear()
        # Release allocated ports
        TestPortManager.release_port(real_config.port)
        TestPortManager.release_port(integration_port)
        # Service will be killed when thread ends (daemon=True)

    def test_real_service_health_endpoint(
        self, running_service_integration: FlextWebService
    ) -> None:
        """Test real health endpoint with actual HTTP request."""
        assert running_service_integration is not None
        port = running_service_integration.config.port
        response = requests.get(f"http://localhost:{port}/health", timeout=5)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["status"] == "healthy"
        assert "version" in data["data"]
        assert "service" in data["data"]  # Health includes service name

    def test_real_application_lifecycle(
        self, running_service_integration: FlextWebService
    ) -> None:
        """Test complete application lifecycle with real HTTP requests."""
        assert running_service_integration is not None
        port = running_service_integration.config.port
        base_url = f"http://localhost:{port}"

        # 1. Create application
        create_data: dict[str, str | int] = {
            "name": "real-test-app",
            "port": 9001,
            "host": "localhost",
        }
        response = requests.post(f"{base_url}/api/v1/apps", json=create_data, timeout=5)

        assert response.status_code == 201  # Created status for POST /apps
        data = response.json()
        assert data["success"] is True
        app_id = data["data"]["id"]
        assert app_id == "app_real-test-app"
        assert data["data"]["name"] == "real-test-app"
        assert data["data"]["port"] == 9001
        assert data["data"]["status"].upper() == "STOPPED"

        # 2. List applications - should contain our app
        response = requests.get(f"{base_url}/api/v1/apps", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        apps = data["data"]["apps"]
        assert len(apps) == 1
        assert apps[0]["name"] == "real-test-app"

        # 3. Get specific application
        response = requests.get(f"{base_url}/api/v1/apps/{app_id}", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "real-test-app"
        assert data["data"]["status"].upper() == "STOPPED"

        # 4. Start application
        response = requests.post(f"{base_url}/api/v1/apps/{app_id}/start", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["status"].upper() == "RUNNING"
        assert data["data"]["status"].upper() == "RUNNING"

        # 5. Stop application
        response = requests.post(f"{base_url}/api/v1/apps/{app_id}/stop", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["status"].upper() == "STOPPED"
        assert data["data"]["status"].upper() == "STOPPED"

    def test_real_error_handling(
        self, running_service_integration: FlextWebService
    ) -> None:
        """Test real error handling with actual invalid requests."""
        assert running_service_integration is not None
        port = running_service_integration.config.port
        base_url = f"http://localhost:{port}"

        # Test creating app with invalid data
        invalid_data: dict[str, str | int] = {
            "name": "",  # Invalid empty name
            "port": 99999,  # Invalid port
            "host": "",  # Invalid empty host
        }
        response = requests.post(
            f"{base_url}/api/v1/apps", json=invalid_data, timeout=5
        )

        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert any(
            word in data["message"].lower()
            for word in ["validation", "empty", "required", "invalid", "name"]
        )

        # Test accessing non-existent app
        response = requests.get(f"{base_url}/api/v1/apps/nonexistent", timeout=5)
        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False
        assert "not found" in data["message"].lower()

        # Test starting non-existent app
        response = requests.post(f"{base_url}/api/v1/apps/nonexistent/start", timeout=5)
        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False

    def test_real_web_dashboard(
        self, running_service_integration: FlextWebService
    ) -> None:
        """Test real web dashboard rendering."""
        assert running_service_integration is not None
        port = running_service_integration.config.port
        response = requests.get(f"http://localhost:{port}/", timeout=5)

        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        content = response.text
        assert "FLEXT Web" in content
        assert "Applications" in content


class TestRealDomainLogic:
    """Test real domain logic execution without mocks."""

    def test_real_app_creation_and_validation(self) -> None:
        """Test real FlextWebApp creation and domain validation."""
        # Test valid app creation
        app = FlextWebApp(
            id=FlextEntityId("real_test_app"),
            name="real-test-app",
            port=8000,
            host="localhost",
        )

        assert app.id == "real_test_app"
        assert app.name == "real-test-app"
        assert app.port == 8000
        assert app.host == "localhost"
        assert app.status == FlextWebAppStatus.STOPPED
        assert app.is_running is False

        # Test real domain validation
        result = app.validate_domain_rules()
        assert result.success is True

        # Test real business rules with invalid data by creating invalid app
        with pytest.raises((ValueError, RuntimeError)):
            FlextWebApp(
                id=FlextEntityId("invalid_test"),
                name="",  # Empty name should fail - Pydantic validation will catch this
                port=8000,
                host="localhost",
            )

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

        # Test real error conditions
        error_result = handler.start(started_app)  # Try to start already running
        assert error_result.is_failure is True
        assert error_result.error is not None

    def test_real_config_validation(self) -> None:
        """Test real configuration validation."""
        # Test valid config
        config = FlextWebConfig(
            host="localhost",
            port=8083,
            debug=True,
            secret_key="real-config-test-key-32-characters!",
        )

        result = config.validate_config()
        assert result.success is True

        # Test real validation errors with invalid port (create new config)
        try:
            invalid_config = FlextWebConfig(
                host="localhost",
                port=99999,  # Invalid port - should fail during creation
                debug=True,
                secret_key="real-config-test-key-32-characters!",
            )
            # If creation succeeds, test validation
            result = invalid_config.validate_config()
            assert result.is_failure is True
            assert result.error is not None
        except ValueError:
            # Pydantic validation caught it during creation - this is also valid
            pass

    def test_real_settings_factory(self) -> None:
        """Test real settings factory without mocks."""
        # Clear any cached settings first
        reset_web_settings()

        # Test real settings creation
        settings = get_web_settings()
        assert isinstance(settings, FlextWebConfig)
        assert settings.host == "localhost"  # Default value
        assert settings.port == 8080  # Default value

        # Test settings caching (should return same instance)
        settings2 = get_web_settings()
        assert settings is settings2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
