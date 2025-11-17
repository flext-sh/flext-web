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

from flext_web import FlextWebConfig, FlextWebServices
from flext_web.constants import FlextWebConstants
from tests.port_manager import TestPortManager


@pytest.fixture(autouse=True)
def setup_test_environment() -> Generator[None]:
    """Set up test environment with real configuration."""
    # Save original environment
    original_env = dict[str, object](os.environ)

    # Set test environment variables
    os.environ["FLEXT_ENV"] = "test"
    os.environ["FLEXT_LOG_LEVEL"] = "info"  # Reduce noise
    os.environ["FLEXT_WEB_DEBUG"] = "true"
    os.environ["FLEXT_WEB_HOST"] = FlextWebConstants.WebDefaults.HOST
    os.environ["FLEXT_WEB_SECRET_KEY"] = FlextWebConstants.WebDefaults.TEST_SECRET_KEY

    yield

    # Restore original environment
    os.environ.clear()
    for key, value in original_env.items():
        if isinstance(value, str):
            os.environ[key] = value


@pytest.fixture
def real_config() -> FlextWebConfig:
    """Create real test configuration with required secret key.

    Fast fail if secret key cannot be provided - no fallback.
    """
    return FlextWebConfig(secret_key=FlextWebConstants.WebDefaults.TEST_SECRET_KEY)


@pytest.fixture
def real_service(
    real_config: FlextWebConfig,
) -> FlextWebServices:
    """Create real FlextWebServices instance with clean state."""
    # Pass config object directly - no dict conversion
    service_result = FlextWebServices.create_service(real_config)
    assert service_result.is_success, f"Service creation failed: {service_result.error}"
    return service_result.unwrap()
    # Clean up service state after each test
    # Note: services don't have apps attribute in current implementation


@pytest.fixture
def real_app(real_config: FlextWebConfig) -> Flask:
    """Create real Flask app."""
    from flask import Flask

    # Create a basic Flask app for testing
    app = Flask(__name__)
    # Fast fail if secret_key is None - no fallback
    if real_config.secret_key is None:
        msg = "Secret key must be provided in test configuration"
        raise ValueError(msg)
    app.config.update(
        SECRET_KEY=real_config.secret_key,
        TESTING=True,
    )
    return app


@pytest.fixture
def running_service(
    real_config: FlextWebConfig,
) -> Generator[FlextWebServices]:
    """Start real service in background thread with clean state."""
    # Allocate unique port to avoid conflicts
    test_port = TestPortManager.allocate_port()

    test_config = FlextWebConfig(
        host=real_config.host,
        port=test_port,
        app_name=real_config.app_name,
        version=real_config.version,
    )

    service = FlextWebServices(test_config)

    # Start service in background thread
    def run_service() -> None:
        from flext_web.app import FlextWebApp

        app_result = FlextWebApp.create_flask_app(test_config)
        if app_result.is_success:
            app = app_result.unwrap()
            app.run(
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

    # Release the allocated port
    TestPortManager.release_port(test_port)
    # Service will be killed when thread ends (daemon=True)


# Real test data for application testing
@pytest.fixture
def test_app_data() -> dict[str, str | int]:
    """Real application data for testing."""
    return {
        "name": "test-application",
        "port": FlextWebConstants.WebDefaults.PORT + 1001,
        "host": FlextWebConstants.WebDefaults.HOST,
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
def production_config() -> dict[str, str]:
    """Production-like configuration for testing."""
    return {
        "FLEXT_WEB_HOST": FlextWebConstants.WebSpecific.ALL_INTERFACES,
        "FLEXT_WEB_PORT": str(FlextWebConstants.WebDefaults.PORT),
        "FLEXT_WEB_DEBUG": "false",
        "FLEXT_WEB_SECRET_KEY": FlextWebConstants.WebDefaults.DEV_SECRET_KEY,
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
