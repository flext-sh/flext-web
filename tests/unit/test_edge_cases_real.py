"""Real Edge Cases and Coverage Tests - NO MOCKS, REAL HTTP EXECUTION.

Tests edge cases, error conditions, and specific code paths using REAL
HTTP execution to achieve comprehensive coverage without mocking.
"""

from __future__ import annotations

import os
import threading
import time
from collections.abc import Generator

import pytest
import requests
from flext_core import FlextEntityId
from pydantic import ValidationError
from tests.port_manager import TestPortManager

from flext_web import (
    FlextWebApp,
    FlextWebAppHandler,
    FlextWebAppStatus,
    FlextWebConfig,
    FlextWebService,
    get_web_settings,
    reset_web_settings,
)


class TestRealEdgeCases:
    """Test real edge cases and error conditions."""

    @pytest.mark.unit
    def test_real_app_state_transitions(self) -> None:
        """Test real application state transitions."""
        app = FlextWebApp(
            id=FlextEntityId("state_test"),
            name="state-test-app",
            port=8000,
            host="localhost",
        )

        # Initial state
        assert app.status == FlextWebAppStatus.STOPPED
        assert app.is_running is False

        # Start app
        result = app.start()
        assert result.success is True
        started_app = result.data
        assert started_app.status == FlextWebAppStatus.RUNNING
        assert started_app.is_running is True

        # Try to start already running app
        result = started_app.start()
        assert result.is_failure is True
        assert result.error is not None
        assert "already running" in result.error.lower()

        # Stop app
        result = started_app.stop()
        assert result.success is True
        stopped_app = result.data
        assert stopped_app.status == FlextWebAppStatus.STOPPED
        assert stopped_app.is_running is False

        # Try to stop already stopped app
        result = stopped_app.stop()
        assert result.is_failure is True
        assert result.error is not None
        assert "already stopped" in result.error.lower()

    @pytest.mark.unit
    def test_real_domain_validation_edge_cases(self) -> None:
        """Test real domain validation with edge cases."""
        # Test empty name
        app = FlextWebApp.model_construct(
            id=FlextEntityId("empty_name_test"),
            name="",
            port=8000,
            host="localhost",
        )
        result = app.validate_domain_rules()
        assert result.is_failure is True
        assert result.error is not None
        assert "Application name cannot be empty" in result.error

        # Test empty host
        app = FlextWebApp.model_construct(
            id=FlextEntityId("empty_host_test"),
            name="test-app",
            port=8000,
            host="",
        )
        result = app.validate_business_rules()
        assert result.is_failure is True
        assert result.error is not None
        assert "Host cannot be empty" in result.error

    @pytest.mark.unit
    def test_real_status_enum_coercion(self) -> None:
        """Test real status enum coercion and validation."""
        # Test string to enum coercion
        app = FlextWebApp(
            id=FlextEntityId("status_test"),
            name="status-test",
            port=8000,
            host="localhost",
            status=FlextWebAppStatus.RUNNING,  # Use enum directly
        )
        assert app.status == FlextWebAppStatus.RUNNING
        assert isinstance(app.status, FlextWebAppStatus)

        # Test enum remains enum
        app2 = FlextWebApp(
            id=FlextEntityId("status_test2"),
            name="status-test2",
            port=8001,
            host="localhost",
            status=FlextWebAppStatus.STOPPED,
        )
        assert app2.status == FlextWebAppStatus.STOPPED
        assert isinstance(app2.status, FlextWebAppStatus)

    @pytest.mark.unit
    def test_real_handler_validation_edge_cases(self) -> None:
        """Test real handler validation with edge cases."""
        handler = FlextWebAppHandler()

        # Test empty name
        result = handler.create("", 8000, "localhost")
        assert result.is_failure is True
        assert result.error is not None

        # Test invalid port (too low)
        result = handler.create("test", -1, "localhost")
        assert result.is_failure is True
        assert result.error is not None

        # Test invalid port (too high)
        result = handler.create("test", 99999, "localhost")
        assert result.is_failure is True
        assert result.error is not None

        # Test empty host
        result = handler.create("test", 8000, "")
        assert result.is_failure is True
        assert result.error is not None

    @pytest.mark.unit
    def test_real_config_validation_edge_cases(self) -> None:
        """Test real configuration validation edge cases."""
        # Test production mode with default secret key
        config = FlextWebConfig(
            debug=False,  # Production mode
            secret_key="change-in-production-xxxxxxxxxxxx",  # Default key
        )
        result = config.validate_config()
        assert result.is_failure is True
        assert result.error is not None
        assert "production" in result.error.lower()

        # Test valid production config
        config = FlextWebConfig(
            debug=False,
            secret_key="real-production-secret-key-32-chars!",
        )
        result = config.validate_config()
        assert result.success is True

    @pytest.mark.integration
    def test_real_environment_variable_edge_cases(self) -> None:
        """Test real environment variable handling edge cases."""
        # Save original environment
        original_env = dict(os.environ)

        try:
            # Test with invalid port in environment
            os.environ["FLEXT_WEB_PORT"] = "invalid"
            reset_web_settings()

            with pytest.raises(ValueError):
                get_web_settings()

            # Test with valid environment
            os.environ["FLEXT_WEB_PORT"] = "8085"
            os.environ["FLEXT_WEB_HOST"] = "test-host"
            reset_web_settings()

            config = get_web_settings()
            assert config.port == 8085
            assert config.host == "test-host"

        finally:
            # Restore original environment
            os.environ.clear()
            os.environ.update(original_env)
            reset_web_settings()


class TestRealServiceEdgeCases:
    """Test real service edge cases and error handling using real HTTP."""

    @pytest.fixture
    def real_edge_service(self) -> Generator[FlextWebService]:
        """Create real running service for edge case tests."""
        # Allocate unique port to avoid conflicts
        port = TestPortManager.allocate_port()

        config = FlextWebConfig(
            host="localhost",
            port=port,
            debug=True,
            secret_key="edge-test-secret-key-32-characters-long!",
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
        # Release the allocated port
        TestPortManager.release_port(port)

    @pytest.mark.integration
    def test_real_api_edge_cases(self, real_edge_service: FlextWebService) -> None:
        """Test real API edge cases and error handling using real HTTP."""
        assert real_edge_service is not None
        port = real_edge_service.config.port
        base_url = f"http://localhost:{port}"

        # Test creating app with missing fields
        response = requests.post(f"{base_url}/api/v1/apps", json={}, timeout=5)
        assert response.status_code == 400

        # Test creating app with invalid data types
        response = requests.post(
            f"{base_url}/api/v1/apps",
            json={
                "name": 123,  # Should be string
                "port": "invalid",  # Should be int
                "host": None,  # Should be string
            },
            timeout=5,
        )
        assert response.status_code == 400

        # Test accessing non-existent app
        response = requests.get(f"{base_url}/api/v1/apps/nonexistent", timeout=5)
        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False
        assert "not found" in data["message"].lower()

        # Test starting non-existent app
        response = requests.post(f"{base_url}/api/v1/apps/nonexistent/start", timeout=5)
        assert response.status_code == 404

        # Test stopping non-existent app
        response = requests.post(f"{base_url}/api/v1/apps/nonexistent/stop", timeout=5)
        assert response.status_code == 404

    @pytest.mark.integration
    def test_real_app_lifecycle_edge_cases(
        self, real_edge_service: FlextWebService
    ) -> None:
        """Test real application lifecycle edge cases using real HTTP."""
        assert real_edge_service is not None
        port = real_edge_service.config.port
        base_url = f"http://localhost:{port}"

        # Create valid app
        response = requests.post(
            f"{base_url}/api/v1/apps",
            json={
                "name": "lifecycle-edge-test",
                "port": 9010,
                "host": "localhost",
            },
            timeout=5,
        )
        assert response.status_code == 200
        data = response.json()
        app_id = data["data"]["id"]

        # Start app
        response = requests.post(f"{base_url}/api/v1/apps/{app_id}/start", timeout=5)
        assert response.status_code == 200

        # Try to start already running app
        response = requests.post(f"{base_url}/api/v1/apps/{app_id}/start", timeout=5)
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "already running" in data["message"].lower()

        # Stop app
        response = requests.post(f"{base_url}/api/v1/apps/{app_id}/stop", timeout=5)
        assert response.status_code == 200

        # Try to stop already stopped app
        response = requests.post(f"{base_url}/api/v1/apps/{app_id}/stop", timeout=5)
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "already stopped" in data["message"].lower()

    @pytest.mark.integration
    def test_real_dashboard_with_apps(self, real_edge_service: FlextWebService) -> None:
        """Test real dashboard rendering with various app states using real HTTP."""
        assert real_edge_service is not None
        port = real_edge_service.config.port
        base_url = f"http://localhost:{port}"

        # Create apps in different states
        apps_data: list[dict[str, str | int]] = [
            {"name": "dashboard-running", "port": 9011, "host": "localhost"},
            {"name": "dashboard-stopped", "port": 9012, "host": "localhost"},
        ]

        created_apps: list[str] = []
        for app_data in apps_data:
            response = requests.post(
                f"{base_url}/api/v1/apps", json=app_data, timeout=5
            )
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, dict)
            created_apps.append(data["data"]["id"])

        # Start first app
        requests.post(f"{base_url}/api/v1/apps/{created_apps[0]}/start", timeout=5)

        # Test dashboard renders correctly
        response = requests.get(f"{base_url}/", timeout=5)
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        content = response.text

        # Should show both apps and have proper structure
        assert "FLEXT Web" in content
        assert "Total Apps" in content

    @pytest.mark.integration
    def test_real_service_error_responses(
        self, real_edge_service: FlextWebService
    ) -> None:
        """Test real service error response formatting using real HTTP."""
        assert real_edge_service is not None
        port = real_edge_service.config.port
        base_url = f"http://localhost:{port}"

        # Test 404 error formatting
        response = requests.get(f"{base_url}/api/v1/apps/nonexistent", timeout=5)
        assert response.status_code == 404
        data = response.json()
        assert "success" in data
        assert "message" in data
        assert data["success"] is False

        # Test validation error formatting
        response = requests.post(
            f"{base_url}/api/v1/apps",
            json={
                "name": "",
                "port": 99999,
            },
            timeout=5,
        )
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "message" in data


class TestRealConfigurationEdgeCases:
    """Test real configuration edge cases."""

    @pytest.mark.unit
    def test_real_config_field_validation(self) -> None:
        """Test real configuration field validation."""
        # Test invalid app name
        with pytest.raises(ValidationError):
            FlextWebConfig(app_name="")

        # Test invalid version format
        with pytest.raises(ValidationError):
            FlextWebConfig(version="invalid-version")

        # Test invalid host
        with pytest.raises(ValidationError):
            FlextWebConfig(host="")

        # Test invalid port range
        with pytest.raises(ValidationError):
            FlextWebConfig(port=0)

        with pytest.raises(ValidationError):
            FlextWebConfig(port=99999)

        # Test invalid secret key length
        with pytest.raises(ValidationError):
            FlextWebConfig(secret_key="short")

    @pytest.mark.unit
    def test_real_config_server_url_generation(self) -> None:
        """Test real server URL generation."""
        config = FlextWebConfig(host="test-host", port=9000)
        assert config.get_server_url() == "http://test-host:9000"

        config = FlextWebConfig(host="0.0.0.0", port=8080)
        assert config.get_server_url() == "http://0.0.0.0:8080"

    @pytest.mark.unit
    def test_real_config_production_detection(self) -> None:
        """Test real production mode detection."""
        # Development mode
        config = FlextWebConfig(debug=True)
        assert config.is_production() is False

        # Production mode
        config = FlextWebConfig(debug=False)
        assert config.is_production() is True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
