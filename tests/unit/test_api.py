"""FLEXT Web Interface - REST API Integration Testing Suite.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import threading
import time
from collections.abc import Generator

import pytest
import requests
from tests.port_manager import TestPortManager

from flext_web import FlextWebConfigs, FlextWebServices
from flext_web.constants import FlextWebConstants

# Type alias for readability
FlextWebService = FlextWebServices.WebService


class TestFlextWebService:
    """Enterprise REST API testing for FlextWebService functionality.

    Test constants consolidated following flext-core patterns.
    """

    # Test constants within class scope
    HTTP_OK = FlextWebConstants.Web.HTTP_OK
    HTTP_CREATED = 201
    EXPECTED_TOTAL_PAGES = 8
    """Enterprise REST API testing for FlextWebService functionality.

    Comprehensive test suite covering REST API endpoint implementation,
    HTTP request/response handling, and service integration patterns.
    Ensures API follows enterprise standards with proper validation.
    """

    @pytest.fixture
    def real_api_service(self) -> Generator[FlextWebServices.WebService]:
        """Create real running service for API testing."""
        # Allocate unique port to avoid conflicts
        port = TestPortManager.allocate_port()
        config = FlextWebConfigs.WebConfig.model_validate(
            {
                "host": "localhost",
                "port": port,
                "debug": True,
                "secret_key": "api-test-secret-key-32-characters-long!",
            }
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
        # Release the allocated port
        TestPortManager.release_port(port)

    def test_service_creation(self) -> None:
        """Test FlextWebService creation with proper initialization.

        Validates that service instance creates successfully with Flask
        application, route registration, and handler initialization.
        Tests fundamental service patterns used in enterprise deployment.
        """
        service_result = FlextWebServices.create_web_service()
        assert service_result.is_success
        service = service_result.value

        assert service.app is not None
        if service.apps != {}:
            msg: str = f"Expected {{}}, got {service.apps}"
            raise AssertionError(msg)
        assert hasattr(service, "config")

    def test_health_check(self, real_api_service: FlextWebService) -> None:
        """Test health check endpoint using real HTTP."""
        assert real_api_service is not None
        base_url = f"http://localhost:{real_api_service.config.port}"

        response = requests.get(f"{base_url}/health", timeout=5)

        if response.status_code != self.HTTP_OK:
            msg: str = f"Expected {200}, got {response.status_code}"
            raise AssertionError(msg)
        data = response.json()
        if not (data["success"]):
            success_msg: str = f"Expected True, got {data['success']}"
            raise AssertionError(success_msg)
        if "healthy" not in data["message"]:
            health_msg: str = f"Expected {'healthy'} in {data['message']}"
            raise AssertionError(health_msg)

    def test_list_apps_empty(self, real_api_service: FlextWebService) -> None:
        """Test listing empty apps using real HTTP."""
        assert real_api_service is not None
        base_url = f"http://localhost:{real_api_service.config.port}"

        response = requests.get(f"{base_url}/api/v1/apps", timeout=5)

        if response.status_code != self.HTTP_OK:
            msg: str = f"Expected {200}, got {response.status_code}"
            raise AssertionError(msg)
        data = response.json()
        if not (data["success"]):
            success_msg: str = f"Expected True, got {data['success']}"
            raise AssertionError(success_msg)
        if data["data"]["apps"] != []:
            apps_msg: str = f"Expected {[]}, got {data['data']['apps']}"
            raise AssertionError(apps_msg)

    def test_create_app(self, real_api_service: FlextWebService) -> None:
        """Test creating an app using real HTTP."""
        assert real_api_service is not None
        base_url = f"http://localhost:{real_api_service.config.port}"

        response = requests.post(
            f"{base_url}/api/v1/apps",
            json={
                "name": "TestApp",
                "port": 8080,
            },
            timeout=5,
        )

        if response.status_code != self.HTTP_CREATED:
            msg: str = f"Expected {self.HTTP_CREATED}, got {response.status_code}"
            raise AssertionError(msg)
        data = response.json()
        if not (data["success"]):
            success_msg: str = f"Expected True, got {data['success']}"
            raise AssertionError(success_msg)
        if data["data"]["name"] != "TestApp":
            name_msg: str = f"Expected {'TestApp'}, got {data['data']['name']}"
            raise AssertionError(
                name_msg,
            )
        assert data["data"]["port"] == 8080

    def test_create_app_missing_name(self, real_api_service: FlextWebService) -> None:
        """Test creating app with missing name using real HTTP."""
        assert real_api_service is not None
        base_url = f"http://localhost:{real_api_service.config.port}"

        response = requests.post(
            f"{base_url}/api/v1/apps",
            json={
                "port": 8080,
            },
            timeout=5,
        )

        if response.status_code != 400:
            msg: str = f"Expected {400}, got {response.status_code}"
            raise AssertionError(msg)
        data = response.json()
        if data["success"]:
            failure_msg: str = f"Expected False, got {data['success']}"
            raise AssertionError(failure_msg)
        assert "name is required" in data["message"].lower()
