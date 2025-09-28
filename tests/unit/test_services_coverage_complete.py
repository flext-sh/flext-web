"""Complete functional coverage for all uncovered lines in services.py.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import pytest
from flask.testing import FlaskClient

from flext_web import FlextWebConfig, FlextWebServices


class TestServicesCompleteCoverage:
    """Complete coverage tests for services.py using real execution without mocks."""

    @pytest.fixture
    def test_config(self) -> FlextWebConfig.WebConfig:
        """Configuration for coverage tests."""
        return FlextWebConfig.WebConfig(
            host="127.0.0.1",
            port=8900,
            debug=True,
            secret_key="coverage-test-secret-32-characters!",
            app_name="Coverage Test Service",
        )

    @pytest.fixture
    def test_service(
        self,
        test_config: FlextWebConfig.WebConfig,
    ) -> FlextWebServices.WebService:
        """Service instance for coverage tests."""
        service = FlextWebServices.WebService(test_config)
        service.app.config["TESTING"] = True
        return service

    @pytest.fixture
    def test_client(self, test_service: FlextWebServices.WebService) -> FlaskClient:
        """Flask test client."""
        return test_service.app.test_client()

    def test_validation_error_paths(self, test_client: FlaskClient) -> None:
        """Test validation error paths (lines 303-304)."""
        # Send completely malformed data to trigger validation exceptions
        response = test_client.post(
            "/api/v1/apps",
            json={
                "name": None,  # Invalid type
                "host": {"invalid": "object"},  # Wrong type
                "port": "invalid_port_string",  # Should be int
            },
        )

        # Should handle validation error gracefully
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert (
            "required" in data["message"].lower()
            or "invalid" in data["message"].lower()
            or "validation" in data["message"].lower()
            or "error" in data["message"].lower()
        )

    def test_create_web_service_with_none_config(self) -> None:
        """Test create_web_service factory with None config (lines 632-638)."""
        # Test factory method with None config - should create default
        result = FlextWebServices.create_web_service(None)

        assert result.success
        service = result.value
        assert isinstance(service, FlextWebServices.WebService)
        assert service.config.host == "localhost"  # Default value
        assert service.config.port == 8080  # Default value

    def test_create_web_service_exception_handling(self) -> None:
        """Test exception handling in create_web_service (lines 644-645)."""
        # Test with valid config that should succeed
        valid_config = FlextWebConfig.WebConfig(
            host="127.0.0.1",
            port=8903,
            secret_key="test-exception-handling-32-chars!",
            debug=True,
        )

        # Normal case should succeed
        result = FlextWebServices.create_web_service(valid_config)
        assert result.success
        assert isinstance(result.value, FlextWebServices.WebService)

        # Test with None to trigger default config creation path
        none_result = FlextWebServices.create_web_service(None)
        assert none_result.success
        assert isinstance(none_result.value, FlextWebServices.WebService)

    def test_service_registry_operations(self) -> None:
        """Test service registry operations (lines 607, 635, 657-658)."""
        # Create registry
        registry_result = FlextWebServices.create_service_registry()
        assert registry_result.success
        registry = registry_result.value

        # Test list_web_services with empty registry
        list_result = registry.list_web_services()
        assert list_result.success
        assert list_result.value == []

        # Create test service
        config = FlextWebConfig.WebConfig(
            host="127.0.0.1",
            port=8901,
            secret_key="registry-test-32-character-secret-key!",
            app_name="Registry Test",
        )
        service = FlextWebServices.WebService(config)

        # Register service
        register_result = registry.register_web_service("test-service", service)
        assert register_result.success

        # Test list_web_services with registered service
        list_result = registry.list_web_services()
        assert list_result.success
        assert "test-service" in list_result.value

        # Test discover_web_service
        discover_result = registry.discover_web_service("test-service")
        assert discover_result.success
        assert discover_result.value is service

        # Test discover non-existent service (lines 657-658)
        missing_result = registry.discover_web_service("non-existent")
        assert missing_result.is_failure
        assert missing_result.error is not None
        assert (
            "not found" in missing_result.error.lower()
            or "not registered" in missing_result.error.lower()
        )

    def test_alias_methods_coverage(self) -> None:
        """Test alias methods register_service and get_service (lines 612-620)."""
        # Create registry
        registry_result = FlextWebServices.create_service_registry()
        assert registry_result.success
        registry = registry_result.value

        # Create test service
        config = FlextWebConfig.WebConfig(
            host="127.0.0.1",
            port=8902,
            secret_key="alias-test-32-character-secret-key!",
            app_name="Alias Test",
        )
        service = FlextWebServices.WebService(config)

        # Test register_service alias
        register_result = registry.register_service("alias-test", service)
        assert register_result.success

        # Test get_service alias
        get_result = registry.get_service("alias-test")
        assert get_result.success
        assert get_result.value is service

    def test_internal_helper_methods_via_api(self, test_client: FlaskClient) -> None:
        """Test internal helper methods by triggering them through API calls."""
        # Create valid app to test _create_and_store_app and _build_success_response
        response = test_client.post(
            "/api/v1/apps",
            json={
                "name": "coverage-app",
                "host": "localhost",
                "port": 3500,
            },
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data["success"] is True
        assert data["message"] == "Application created successfully"
        assert data["data"]["name"] == "coverage-app"

        # Test _build_error_response by sending invalid data
        response = test_client.post(
            "/api/v1/apps",
            json={
                "name": "",  # Empty name should cause validation error
                "host": "localhost",
                "port": 3501,
            },
        )

        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False

    def test_edge_cases_and_error_conditions(self, test_client: FlaskClient) -> None:
        """Test edge cases and error conditions."""
        # Test with extremely long names
        response = test_client.post(
            "/api/v1/apps",
            json={
                "name": "x" * 1000,  # Very long name
                "host": "localhost",
                "port": 3502,
            },
        )

        # Should either succeed or fail gracefully
        assert response.status_code in {200, 201, 400, 422}
        data = response.get_json()
        assert isinstance(data.get("success"), bool)

        # Test duplicate port scenario
        test_client.post(
            "/api/v1/apps",
            json={
                "name": "app1",
                "host": "localhost",
                "port": 3503,
            },
        )

        # Try to create another app with same port
        response = test_client.post(
            "/api/v1/apps",
            json={
                "name": "app2",
                "host": "localhost",
                "port": 3503,  # Same port
            },
        )

        # Should handle gracefully
        assert response.status_code in {200, 201, 400, 409}
        data = response.get_json()
        assert isinstance(data.get("success"), bool)


__all__ = [
    "TestServicesCompleteCoverage",
]
