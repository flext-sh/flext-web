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
from flext_core import FlextCore

from flext_web import FlextWebConfig, FlextWebService
from flext_web.constants import FlextWebConstants
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
    os.environ["FLEXT_WEB_HOST"] = FlextWebConstants.WebServer.DEFAULT_HOST
    os.environ["FLEXT_WEB_SECRET_KEY"] = (
        FlextWebConstants.WebSpecific.TEST_ENVIRONMENT_KEY
    )

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def real_config() -> FlextWebConfig:
    """Create real test configuration."""
    config_result = FlextWebConfig.create_web_config()
    assert config_result.is_success, (
        f"Test config creation failed: {config_result.error}"
    )
    return config_result.value


@pytest.fixture
def real_service(
    real_config: FlextWebConfig,
) -> Generator[FlextWebService]:
    """Create real FlextWebService instance with clean state."""
    service_result = FlextWebService.create_web_service(real_config.model_dump())
    assert service_result.is_success, f"Service creation failed: {service_result.error}"
    service = service_result.value
    yield service
    # Clean up service state after each test
    service.apps.clear()


@pytest.fixture
def real_app(real_config: FlextWebConfig) -> Flask:
    """Create real Flask app."""
    service_result = FlextWebService.create_web_service(real_config.model_dump())
    assert service_result.is_success, f"Service creation failed: {service_result.error}"
    return service_result.value.app


@pytest.fixture
def running_service(
    real_config: FlextWebConfig,
) -> Generator[FlextWebService]:
    """Start real service in background thread with clean state."""
    # Allocate unique port to avoid conflicts
    test_port = TestPortManager.allocate_port()

    test_config = FlextWebConfig.model_validate(
        {
            "host": real_config.host,
            "port": test_port,
            "debug": real_config.debug,
            "secret_key": real_config.secret_key,
        },
    )

    service = FlextWebService(test_config.model_dump())

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
        "port": FlextWebConstants.WebServer.DEFAULT_PORT + 1001,
        "host": FlextWebConstants.WebServer.DEFAULT_HOST,
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
def production_config() -> FlextCore.Types.StringDict:
    """Production-like configuration for testing."""
    return {
        "FLEXT_WEB_HOST": FlextWebConstants.WebSpecific.ALL_INTERFACES,
        "FLEXT_WEB_PORT": str(FlextWebConstants.WebServer.DEFAULT_PORT),
        "FLEXT_WEB_DEBUG": "false",
        "FLEXT_WEB_SECRET_KEY": FlextWebConstants.WebSpecific.DEV_SECRET_KEY,
    }


# Pytest configuration
def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest markers for real testing."""
    config.addinivalue_line("markers", "unit: Unit tests with real execution")
    config.addinivalue_line(
        "markers",
        "integration: Integration tests with real services",
    )
    config.addinivalue_line("markers", "api: API tests with real HTTP")
    config.addinivalue_line("markers", "web: Web interface tests with real Flask")
    config.addinivalue_line("markers", "slow: Slow tests (may take >5 seconds)")
