"""Real functional tests for flext_web.services using flext_tests utilities.

Tests focus on real execution patterns without mocks, using flext_tests library
for comprehensive functional validation of service operations and error handling.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from collections.abc import Generator

import pytest
from flext_tests import (
    FlextTestsFactories,
)

from flext_web import FlextWebConfigs, FlextWebServices


class TestWebServiceFunctionalExecution:
    """Functional tests for FlextWebServices.WebService using real execution."""

    @pytest.fixture
    def functional_config(self) -> FlextWebConfigs.WebConfig:
        """Create real config for functional tests."""
        return FlextWebConfigs.WebConfig(
            host="127.0.0.1",
            port=8085,  # Different port to avoid conflicts
            debug=True,
            secret_key="functional-test-secret-key-32-chars-long!!",
            app_name="Functional Test Service",
        )

    @pytest.fixture
    def running_service(
        self, functional_config: FlextWebConfigs.WebConfig
    ) -> Generator[FlextWebServices.WebService]:
        """Create service for functional testing using Flask test client."""
        service = FlextWebServices.WebService(functional_config)
        service.app.config["TESTING"] = True
        try:
            yield service
        finally:
            # Add any cleanup if needed in future
            ...

    def test_functional_service_creation_with_flext_tests(self) -> None:
        """Test service creation using standard configuration."""
        # Create config data directly (flext_tests ConfigBuilder may not have all methods)
        config = FlextWebConfigs.WebConfig(
            host="127.0.0.1",
            port=8086,
            debug=True,
            secret_key="test-key-functional-32-characters!",
            app_name="Test Service",
        )

        # Test service creation with real execution
        service = FlextWebServices.WebService(config)

        assert service is not None
        assert hasattr(service, "app")
        assert hasattr(service, "config")
        assert service.config.host == "127.0.0.1"
        assert service.config.port == 8086

    def test_functional_app_creation_lifecycle(
        self, running_service: FlextWebServices.WebService
    ) -> None:
        """Test complete app creation lifecycle using Flask test client."""
        client = running_service.app.test_client()

        # Test create app via Flask test client
        create_data = {"name": "functional-test-app", "host": "localhost", "port": 3001}

        response = client.post("/api/v1/apps", json=create_data)
        assert response.status_code == 201
        data = response.get_json()
        assert data["success"] is True
        assert data["message"] == "Application created successfully"
        assert data["data"]["name"] == "functional-test-app"
        app_id = data["data"]["id"]

        # Test app retrieval via Flask test client
        response = client.get(f"/api/v1/apps/{app_id}")
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["data"]["name"] == "functional-test-app"

        # Test app listing via Flask test client
        response = client.get("/api/v1/apps")
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert len(data["data"]["apps"]) >= 1
        assert any(app["id"] == app_id for app in data["data"]["apps"])

    def test_functional_app_operations_with_flext_tests(
        self, running_service: FlextWebServices.WebService
    ) -> None:
        """Test app start/stop operations using flext_tests patterns."""
        client = running_service.app.test_client()

        # Create app using standard dict
        app_data = {"name": "operations-test-app", "host": "localhost", "port": 3002}

        # Create app via Flask test client
        response = client.post("/api/v1/apps", json=app_data)
        assert response.status_code == 201
        app_id = response.get_json()["data"]["id"]

        # Test start app operation
        response = client.post(f"/api/v1/apps/{app_id}/start")
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["data"]["status"] == "running"

        # Test stop app operation
        response = client.post(f"/api/v1/apps/{app_id}/stop")
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["data"]["status"] == "stopped"

    def test_functional_error_handling_paths(
        self, running_service: FlextWebServices.WebService
    ) -> None:
        """Test error handling paths using Flask test client."""
        client = running_service.app.test_client()

        # Test creating app with invalid data
        invalid_data = {"name": "", "host": "invalid-host-name", "port": "not-a-number"}

        response = client.post("/api/v1/apps", json=invalid_data)
        # Should handle validation error
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert (
            "error" in data["message"].lower()
            or "invalid" in data["message"].lower()
            or "required" in data["message"].lower()
        )

        # Test accessing non-existent app
        response = client.get("/api/v1/apps/non-existent-app")
        assert response.status_code == 404
        data = response.get_json()
        assert data["success"] is False

    def test_functional_service_health_with_apps(
        self, running_service: FlextWebServices.WebService
    ) -> None:
        """Test service health endpoint with real apps created using Flask test client."""
        client = running_service.app.test_client()

        # Get initial health status
        response = client.get("/health")
        assert response.status_code == 200
        initial_response = response.get_json()
        assert initial_response["success"] is True
        initial_count = initial_response["data"]["applications"]

        # Create some apps using Flask test client
        for i in range(3):
            app_data = {
                "name": f"health-test-app-{i}",
                "host": "localhost",
                "port": 3010 + i,
            }
            response = client.post("/api/v1/apps", json=app_data)
            assert response.status_code == 201  # Created

        # Check updated health status
        response = client.get("/health")
        assert response.status_code == 200
        updated_response = response.get_json()
        assert updated_response["success"] is True
        updated_data = updated_response["data"]
        assert updated_data["applications"] == initial_count + 3
        assert updated_data["status"] == "healthy"
        assert "service_id" in updated_data
        assert "timestamp" in updated_data

    def test_functional_service_with_result_patterns(self) -> None:
        """Test service creation using FlextResult patterns from flext_tests."""
        # Use FlextTestsFactories from flext_tests
        config_result = FlextTestsFactories.FlextResultFactory.create_success(
            FlextWebConfigs.WebConfig(
                host="127.0.0.1",
                port=8087,
                debug=True,
                secret_key="result-pattern-test-key-32-chars!!",
                app_name="Result Pattern Test",
            )
        )

        assert config_result.success
        config = config_result.value
        assert isinstance(config, FlextWebConfigs.WebConfig)

        # Test service creation with the config
        service_result = FlextWebServices.create_web_service(config)
        assert service_result.success
        service = service_result.value

        assert isinstance(service, FlextWebServices.WebService)
        assert service.config.host == "127.0.0.1"
        assert service.config.port == 8087

    def test_functional_web_service_registry_real_execution(self) -> None:
        """Test WebServiceRegistry with real service instances."""
        # Create registry
        registry_result = FlextWebServices.create_service_registry()
        assert registry_result.success
        registry = registry_result.value

        # Create real services
        config1 = FlextWebConfigs.WebConfig(
            host="127.0.0.1",
            port=8088,
            secret_key="registry-test-1-key-32-characters!",
            app_name="Registry Test 1",
        )

        config2 = FlextWebConfigs.WebConfig(
            host="127.0.0.1",
            port=8089,
            secret_key="registry-test-2-key-32-characters!",
            app_name="Registry Test 2",
        )

        service1 = FlextWebServices.WebService(config1)
        service2 = FlextWebServices.WebService(config2)

        # Register services
        result1 = registry.register_service("service1", service1)
        result2 = registry.register_service("service2", service2)

        assert result1.success
        assert result2.success

        # Retrieve services
        retrieved1 = registry.get_service("service1")
        retrieved2 = registry.get_service("service2")

        assert retrieved1.success
        assert retrieved2.success
        assert retrieved1.value is service1
        assert retrieved2.value is service2

        # Test duplicate registration
        duplicate_result = registry.register_service("service1", service2)
        assert duplicate_result.is_failure
        assert duplicate_result.error is not None
        assert "already registered" in duplicate_result.error


__all__ = [
    "TestWebServiceFunctionalExecution",
]
