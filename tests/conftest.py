"""Real test configuration for flext-web - NO MOCKS, REAL EXECUTION.

Provides pytest fixtures for testing web interface functionality using REAL
Flask applications, HTTP requests, and actual service execution.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os
import socket
import threading
import time
from collections.abc import Callable, Generator
from pathlib import Path
from typing import Any, ClassVar

import pytest
from flask import Flask
from flext_core import FlextResult
from flext_tests import (
    FlextTestsDocker,
    FlextTestsFactories,
    FlextTestsMatchers,
    FlextTestsUtilities,
)

from flext_web import FlextWebConfig, FlextWebModels, FlextWebServices, FlextWebTypes
from flext_web.app import FlextWebApp
from flext_web.constants import FlextWebConstants
from flext_web.typings import (
    _ApplicationConfig,
    _WebRequestConfig,
    _WebResponseConfig,
)


def assert_success(
    result: FlextResult[object],
    message: str = "Operation should succeed",
) -> None:
    """Assert that a FlextResult is successful using flext_tests matchers."""
    matchers = FlextTestsMatchers()
    matchers.assert_result_success(result, message)


def assert_failure(
    result: FlextResult[object],
    message: str = "Operation should fail",
) -> None:
    """Assert that a FlextResult is a failure using flext_tests matchers."""
    matchers = FlextTestsMatchers()
    matchers.assert_result_failure(result, message)


def assert_result(
    result: FlextResult[object],
    *,
    expected_success: bool = True,
) -> None:
    """Assert FlextResult state with appropriate message using flext_tests."""
    if expected_success:
        assert_success(result)
    else:
        assert_failure(result)


def create_entry(entry_type: str, **kwargs: object) -> FlextResult[object]:
    """Generalized entry creation function using flext-core patterns.

    This function replaces multiple specific create_* methods by providing
    a unified interface for creating different types of entries in tests.

    Args:
        entry_type: Type of entry to create ('web_app', 'http_request', 'http_response', etc.)
        **kwargs: Parameters for the specific entry type

    Returns:
        FlextResult with created entry

    Raises:
        ValueError: If entry_type is not supported

    """
    if entry_type == "web_app":
        return FlextWebModels.create_web_app(**kwargs)
    if entry_type == "http_request":
        return FlextWebTypes.create_http_request(**kwargs)
    if entry_type == "http_response":
        return FlextWebTypes.create_http_response(**kwargs)
    if entry_type == "web_request":
        config: _WebRequestConfig = kwargs
        return FlextWebTypes.create_web_request(config)
    if entry_type == "web_response":
        config: _WebResponseConfig = kwargs
        return FlextWebTypes.create_web_response(config)
    if entry_type == "application":
        config: _ApplicationConfig = kwargs
        return FlextWebTypes.create_application(config)
    msg = f"Unsupported entry type: {entry_type}"
    raise ValueError(msg)


def create_test_data(data_type: str, **kwargs: object) -> dict[str, object]:
    """Create test data using flext_tests factories.

    This function provides a standardized way to create test data,
    reducing code duplication across test files by using flext_tests.FlextTestsFactories.

    Args:
        data_type: Type of test data to create
        **kwargs: Override default data values

    Returns:
        Dictionary with test data

    """
    # Use flext_tests factories for standardized test data
    if data_type == "app_data":
        return FlextTestsFactories.create_service(
            service_type="web_app",
            name="test-app",
            host="localhost",
            port=8080,
            **kwargs,
        )
    if data_type == "entity_data":
        return {
            "data": FlextTestsFactories.create_service(
                service_type="entity",
                service_id="test-entity",
                name="Test Entity",
                **kwargs,
            ),
        }
    if data_type == "config_data":
        return FlextTestsFactories.create_config(
            service_type="web",
            host="localhost",
            port=8080,
            debug=True,
            **kwargs,
        )
    if data_type == "request_data":
        return FlextTestsFactories.create_config(
            service_type="http_request",
            method="GET",
            url="http://localhost:8080",
            headers={"Content-Type": "application/json"},
            **kwargs,
        )
    if data_type == "response_data":
        return FlextTestsFactories.create_config(
            service_type="http_response",
            status_code=200,
            request_id="test-123",
            **kwargs,
        )
    msg = f"Unsupported data type: {data_type}"
    raise ValueError(msg)


def create_test_app(**kwargs: object) -> FlextWebModels.Application.Entity:
    """Create a test application entity using flext-core patterns.

    This function provides a standardized way to create test applications,
    reducing code duplication across test files.

    Args:
        **kwargs: Override default app properties

    Returns:
        FlextWebModels.Application.Entity instance

    """
    defaults: dict[str, Any] = {
        "id": "test-id",
        "name": "test-app",
        "host": "localhost",
        "port": 8080,
    }

    defaults.update(kwargs)
    return FlextWebModels.Application.Entity(**defaults)


def create_test_result(
    *,
    success: bool = True,
    **kwargs: object,
) -> FlextResult[object]:
    """Create a test FlextResult using flext_tests utilities.

    This function provides a standardized way to create test results,
    reducing code duplication across test files.

    Args:
        success: Whether the result should be successful
        **kwargs: Additional parameters for result creation

    Returns:
        FlextResult instance

    """
    return FlextTestsUtilities.create_test_result(success=success, **kwargs)


def run_parameterized_test(
    test_cases: list[tuple[Any, ...]],
    test_function: Callable[[Any], FlextResult[object]],
    expected_results: list[bool],
    test_name: str = "parameterized_test",
) -> None:
    """Run parameterized tests using flext_tests patterns.

    This function provides a standardized way to run multiple test cases
    with expected results, reducing boilerplate code.

    Args:
        test_cases: List of tuples containing test case parameters
        test_function: Function to test that returns FlextResult
        expected_results: List of expected success/failure for each case
        test_name: Name for the test (for error messages)

    Raises:
        AssertionError: If any test case doesn't match expected result

    """
    for i, (test_case, expected_success) in enumerate(
        zip(test_cases, expected_results, strict=True),
    ):
        try:
            result = (
                test_function(*test_case)
                if isinstance(test_case, tuple)
                else test_function(test_case)
            )

            if expected_success:
                assert_success(result, f"{test_name} case {i} should succeed")
            else:
                assert_failure(result, f"{test_name} case {i} should fail")

        except Exception as e:
            pytest.fail(f"{test_name} case {i} raised unexpected exception: {e}")


def create_comprehensive_test_suite(
    entity_type: str,
    valid_cases: list[dict[str, Any]],
    invalid_cases: list[dict[str, Any]],
    test_name_prefix: str = "comprehensive",
) -> None:
    """Create comprehensive test suite using flext_tests patterns.

    This function generates a full test suite for an entity type,
    testing both valid and invalid cases.

    Args:
        entity_type: Type of entity to test
        valid_cases: List of valid parameter combinations
        invalid_cases: List of invalid parameter combinations
        test_name_prefix: Prefix for generated test names

    """
    # Test valid cases
    for i, params in enumerate(valid_cases):
        test_name = f"{test_name_prefix}_valid_case_{i}"
        result = create_entry(entity_type, **params)
        assert_success(result, f"{test_name} should succeed")

    # Test invalid cases
    for i, params in enumerate(invalid_cases):
        test_name = f"{test_name_prefix}_invalid_case_{i}"
        result = create_entry(entity_type, **params)
        assert_failure(result, f"{test_name} should fail")


@pytest.fixture(autouse=True)
def setup_test_environment() -> Generator[None]:
    """Set up test environment with real configuration."""
    # Save original environment
    original_env = dict[str, object](os.environ)

    # Set test environment variables
    os.environ["FLEXT_ENV"] = "test"
    os.environ["FLEXT_LOG_LEVEL"] = "info"  # Reduce noise
    os.environ["FLEXT_WEB_DEBUG_MODE"] = "true"
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
    # Create a basic Flask app for testing
    app = Flask(__name__)
    # secret_key now has default from Constants, no None check needed
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

    service_result = FlextWebServices.create_service(test_config)
    assert service_result.is_success, f"Service creation failed: {service_result.error}"
    service = service_result.unwrap()

    # Start service in background thread
    def run_service() -> None:
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

    # Wait for service to start (check if port is open)
    def wait_for_port(port: int, timeout: float = 5.0) -> bool:
        """Wait for port to be open."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(0.1)
                    result = sock.connect_ex((test_config.host, port))
                    if result == 0:
                        return True
            except OSError:
                pass
            time.sleep(0.1)
        return False

    # Wait for the service to be ready
    if not wait_for_port(test_config.port, timeout=5.0):
        pytest.fail(
            f"Service failed to start on port {test_config.port} within 5 seconds",
        )

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


@pytest.fixture(scope="session")
def docker_manager() -> Generator[FlextTestsDocker]:
    """Provide FlextTestsDocker instance for integration tests."""
    try:
        manager = FlextTestsDocker(workspace_root=Path().absolute())
        yield manager
    except ImportError:
        # FlextTestsDocker may not be available in all environments
        pytest.skip("FlextTestsDocker not available")
    except Exception as e:
        pytest.skip(f"FlextTestsDocker initialization failed: {e}")


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
    config.addinivalue_line("markers", "docker: Tests that require Docker containers")


class TestPortManager:
    """Thread-safe port allocation manager for tests."""

    # Port range constants
    _PORT_START: ClassVar[int] = 9000
    _PORT_END: ClassVar[int] = 9999

    _lock: ClassVar[threading.Lock] = threading.Lock()
    _allocated_ports: ClassVar[set[int]] = set()
    _current_port: ClassVar[int] = _PORT_START

    @classmethod
    def allocate_port(cls) -> int:
        """Allocate a unique port for testing.

        Returns:
            Unique port number in the range 9000-9999

        Thread Safety:
            This method is thread-safe and can be called from
            multiple test threads simultaneously.

        """
        with cls._lock:
            # Find next available port
            while cls._current_port in cls._allocated_ports:
                cls._current_port += 1

                # Wrap around if we hit the limit
                if cls._current_port > cls._PORT_END:
                    cls._current_port = cls._PORT_START

            port = cls._current_port
            cls._allocated_ports.add(port)
            cls._current_port += 1

            return port

    @classmethod
    def release_port(cls, port: int) -> None:
        """Release a previously allocated port.

        Args:
            port: Port number to release

        Thread Safety:
            This method is thread-safe.

        """
        with cls._lock:
            cls._allocated_ports.discard(port)

    @classmethod
    def reset(cls) -> None:
        """Reset the port manager (for testing only).

        Thread Safety:
            This method is thread-safe.
        """
        with cls._lock:
            cls._allocated_ports.clear()
            cls._current_port = 9000
