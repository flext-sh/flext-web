"""Simple tests to increase services.py coverage.

Focus on specific uncovered lines without complex integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json

from flext_web import FlextWebConfig, FlextWebServices


class TestServicesCoverage:
    """Simple tests for uncovered services.py lines."""

    def test_service_basic_functionality(self) -> None:
        """Test basic service functionality."""
        config = FlextWebConfig()
        service = FlextWebServices.WebService(config)

        # Basic service properties
        assert service.config is not None
        assert service.app is not None

    def test_health_endpoint_structure(self) -> None:
        """Test health endpoint response structure."""
        config = FlextWebConfig()
        service = FlextWebServices.WebService(config)

        with service.app.test_client() as client:
            response = client.get("/health")
            assert response.status_code == 200

            data = json.loads(response.data)
            # Test structure - response has success, message, data
            assert "success" in data
            assert data["success"] is True
            assert "message" in data
            assert "data" in data

            # Test data structure
            health_data = data["data"]
            assert "service" in health_data
            assert "applications" in health_data

    def test_create_app_success_path(self) -> None:
        """Test successful app creation."""
        config = FlextWebConfig()
        service = FlextWebServices.WebService(config)

        with service.app.test_client() as client:
            response = client.post(
                "/api/v1/apps",
                json={"name": "test-app", "host": "localhost", "port": 3000},
            )
            assert response.status_code == 201

            data = json.loads(response.data)
            assert data["success"] is True
            assert "data" in data

    def test_create_app_validation_error(self) -> None:
        """Test app creation with validation errors."""
        config = FlextWebConfig()
        service = FlextWebServices.WebService(config)

        with service.app.test_client() as client:
            # Empty request should fail
            response = client.post("/api/v1/apps", json={})
            assert response.status_code == 400

            data = json.loads(response.data)
            assert data["success"] is False

    def test_list_apps_endpoint(self) -> None:
        """Test list apps endpoint."""
        config = FlextWebConfig()
        service = FlextWebServices.WebService(config)

        with service.app.test_client() as client:
            response = client.get("/api/v1/apps")
            assert response.status_code == 200

            data = json.loads(response.data)
            assert data["success"] is True
            assert "data" in data

    def test_get_nonexistent_app(self) -> None:
        """Test getting a non-existent app."""
        config = FlextWebConfig()
        service = FlextWebServices.WebService(config)

        with service.app.test_client() as client:
            response = client.get("/api/v1/apps/nonexistent")
            assert response.status_code == 404

    def test_malformed_json_request(self) -> None:
        """Test handling of malformed JSON."""
        config = FlextWebConfig()
        service = FlextWebServices.WebService(config)

        with service.app.test_client() as client:
            response = client.post(
                "/api/v1/apps",
                data="invalid json",
                content_type="application/json",
            )
            # Should handle malformed JSON gracefully
            assert response.status_code in {400, 500}

    def test_service_with_custom_config(self) -> None:
        """Test service with custom configuration values."""
        config = FlextWebConfig(host="0.0.0.0", port=9000, debug=False)
        service = FlextWebServices.WebService(config)

        assert (
            config.host == "127.0.0.1"
        )  # Security validation converts 0.0.0.0 to localhost
        assert service.config.port == 9000
        assert service.config.debug is False

        with service.app.test_client() as client:
            response = client.get("/health")
            assert response.status_code == 200
