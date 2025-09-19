"""Real test configuration for flext-web - NO MOCKS, REAL EXECUTION.

Provides pytest fixtures for testing web interface functionality using REAL
Flask applications, HTTP requests, and actual service execution.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
import threading
import time
from collections.abc import Generator

import pytest
from flask import Flask

from flext_core import FlextTypes
from flext_web import FlextWebConfigs, FlextWebServices
from tests.port_manager import TestPortManager


@pytest.fixture(autouse=True)
def setup_test_environment() -> Generator[None]:
    """Set up test environment with real configuration."""
    # Save original environment
    original_env = dict(os.environ)

    # Set test environment variables
    os.environ["FLEXT_ENV"] = "test"
    os.environ["FLEXT_LOG_LEVEL"] = "info"  # Reduce noise
    os.environ["FLEXT_WEB_DEBUG"] = "true"
    os.environ["FLEXT_WEB_HOST"] = "localhost"
    os.environ["FLEXT_WEB_SECRET_KEY"] = "test-secret-key-32-characters-long!!"

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def real_config() -> FlextWebConfigs.WebConfig:
    """Create real test configuration."""
    config_result = FlextWebConfigs.create_test_config()
    assert config_result.is_success, (
        f"Test config creation failed: {config_result.error}"
    )
    return config_result.value


@pytest.fixture
def real_service(
    real_config: FlextWebConfigs.WebConfig,
) -> Generator[FlextWebServices.WebService]:
    """Create real FlextWebServices.WebService instance with clean state."""
    service_result = FlextWebServices.create_web_service(real_config)
    assert service_result.is_success, f"Service creation failed: {service_result.error}"
    service = service_result.value
    yield service
    # Clean up service state after each test
    service.apps.clear()


@pytest.fixture
def real_app(real_config: FlextWebConfigs.WebConfig) -> Flask:
    """Create real Flask app."""
    service_result = FlextWebServices.create_web_service(real_config)
    assert service_result.is_success, f"Service creation failed: {service_result.error}"
    return service_result.value.app


@pytest.fixture
def running_service(
    real_config: FlextWebConfigs.WebConfig,
) -> Generator[FlextWebServices.WebService]:
    """Start real service in background thread with clean state."""
    # Allocate unique port to avoid conflicts
    test_port = TestPortManager.allocate_port()

    test_config = FlextWebConfigs.WebConfig.model_validate(
        {
            "host": real_config.host,
            "port": test_port,
            "debug": real_config.debug,
            "secret_key": real_config.secret_key,
        },
    )

    service = FlextWebServices.WebService(test_config)

    # Start service in background thread
    def run_service() -> None:
        service.app.run(
            host=test_config.host,
            port=test_config.port,
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
    # Release the allocated port
    TestPortManager.release_port(test_port)
    # Service will be killed when thread ends (daemon=True)


# Real test data for application testing
@pytest.fixture
def test_app_data() -> dict[str, str | int]:
    """Real application data for testing."""
    return {
        "name": "test-application",
        "port": 9001,
        "host": "localhost",
    }


@pytest.fixture
def invalid_app_data() -> dict[str, str | int]:
    """Invalid application data for error testing."""
    return {
        "name": "",  # Invalid empty name
        "port": 99999,  # Invalid port
        "host": "",  # Invalid empty host
    }


# Configuration for real environment tests
@pytest.fixture
def production_config() -> FlextTypes.Core.Headers:
    """Production-like configuration for testing."""
    return {
        "FLEXT_WEB_HOST": "0.0.0.0",
        "FLEXT_WEB_PORT": "8080",
        "FLEXT_WEB_DEBUG": "false",
        "FLEXT_WEB_SECRET_KEY": "production-secret-key-32-chars-long!!",
    }


# Pytest configuration
def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest markers for real testing."""
    config.addinivalue_line("markers", "unit: Unit tests with real execution")
    config.addinivalue_line(
        "markers", "integration: Integration tests with real services",
    )
    config.addinivalue_line("markers", "api: API tests with real HTTP")
    config.addinivalue_line("markers", "web: Web interface tests with real Flask")
    config.addinivalue_line("markers", "slow: Slow tests (may take >5 seconds)")
