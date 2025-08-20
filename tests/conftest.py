"""Real test configuration for flext-web - NO MOCKS, REAL EXECUTION.

Provides pytest fixtures for testing web interface functionality using REAL
Flask applications, HTTP requests, and actual service execution.
"""

from __future__ import annotations

import os
import threading
import time
from collections.abc import Generator
from typing import TYPE_CHECKING

import pytest
from flask.testing import FlaskClient

from flext_web import (
    FlextWebConfig,
    FlextWebService,
    create_app,
    create_service,
    reset_web_settings,
)

if TYPE_CHECKING:
    from flask import Flask


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

    # Reset web settings to force reload
    reset_web_settings()

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)
    reset_web_settings()


@pytest.fixture
def real_config() -> FlextWebConfig:
    """Create real test configuration."""
    return FlextWebConfig(
        host="localhost",
        port=8081,  # Use different port to avoid conflicts
        debug=True,
        secret_key="test-secret-key-32-characters-long!!",
    )


@pytest.fixture
def real_service(real_config: FlextWebConfig) -> Generator[FlextWebService]:
    """Create real FlextWebService instance with clean state."""
    service = create_service(real_config)
    yield service
    # Clean up service state after each test
    service.apps.clear()


@pytest.fixture
def real_app(real_config: FlextWebConfig) -> Flask:
    """Create real Flask app."""
    return create_app(real_config)


@pytest.fixture
def real_client(real_app: Flask) -> FlaskClient:
    """Create real Flask test client."""
    return real_app.test_client()


@pytest.fixture
def running_service(real_config: FlextWebConfig) -> Generator[FlextWebService]:
    """Start real service in background thread with clean state."""
    # Use different port for each test to avoid conflicts
    test_port = real_config.port + 10  # Use 8091 instead of 8081
    test_config = FlextWebConfig(
        host=real_config.host,
        port=test_port,
        debug=real_config.debug,
        secret_key=real_config.secret_key,
    )

    service = FlextWebService(test_config)

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
def production_config() -> dict[str, str]:
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
    config.addinivalue_line("markers", "integration: Integration tests with real services")
    config.addinivalue_line("markers", "api: API tests with real HTTP")
    config.addinivalue_line("markers", "web: Web interface tests with real Flask")
    config.addinivalue_line("markers", "slow: Slow tests (may take >5 seconds)")
