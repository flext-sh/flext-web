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
from typing import ClassVar

import pytest
from flask import Flask
from flext_tests import FlextTestsDocker

from tests import (
    FlextWebApp,
    FlextWebServices,
    FlextWebSettings,
    _ApplicationConfig,
    _WebRequestConfig,
    _WebResponseConfig,
    c,
    m,
    r,
    t,
)


def assert_success(
    result: r[object],
    message: str = "Operation should succeed",
) -> None:
    """Assert that a r is successful using flext_tests matchers."""
    if not result.is_success:
        raise AssertionError(f"{message}: {result.error}")


def assert_failure(
    result: r[object],
    message: str = "Operation should fail",
) -> None:
    """Assert that a r is a failure using flext_tests matchers."""
    if result.is_success:
        raise AssertionError(message)


def assert_result(
    result: r[object],
    *,
    expected_success: bool = True,
) -> None:
    """Assert r state with appropriate message using flext_tests."""
    if expected_success:
        assert_success(result)
    else:
        assert_failure(result)


def create_entry(entry_type: str, **kwargs: object) -> r[object]:
    """Generalized entry creation function using flext-core patterns.

    This function replaces multiple specific create_* methods by providing
    a unified interface for creating different types of entries in tests.

    Args:
        entry_type: Type of entry to create (e.g., 'web_app', 'http_request')
        **kwargs: Parameters for the specific entry type

    Returns:
        r with created entry

    Raises:
        ValueError: If entry_type is not supported

    """
    if entry_type == "web_app":
        name: object = kwargs.get("name")
        host: object = kwargs.get("host")
        port: object = kwargs.get("port")
        if (
            not isinstance(name, str)
            or not isinstance(host, str)
            or not isinstance(port, int)
        ):
            return r[object].fail("Invalid parameters for web_app")
        return m.Web.create_web_app(
            name=name,
            host=host,
            port=port,
        )
    if entry_type == "http_request":
        url: object = kwargs.get("url")
        method: object = kwargs.get("method")
        req_headers: object = kwargs.get("headers")
        req_body: object = kwargs.get("body")
        timeout: object = kwargs.get("timeout")
        if not isinstance(url, str) or not isinstance(method, str):
            return r[object].fail("Invalid parameters for http_request")
        if req_headers is not None and not isinstance(req_headers, dict):
            return r[object].fail("Invalid headers for http_request")
        if req_body is not None and not isinstance(req_body, (str, dict)):
            return r[object].fail("Invalid body for http_request")
        if not isinstance(timeout, (float, int)):
            return r[object].fail("Invalid timeout for http_request")
        return t.create_http_request(
            url=url,
            method=method,
            headers=req_headers,
            body=req_body,
            timeout=float(timeout),
        )
    if entry_type == "http_response":
        status_code: object = kwargs.get("status_code")
        headers: object = kwargs.get("headers")
        body: object = kwargs.get("body")
        elapsed_time: object = kwargs.get("elapsed_time")
        if not isinstance(status_code, int):
            return r[object].fail("Invalid status_code for http_response")
        if headers is not None and not isinstance(headers, dict):
            return r[object].fail("Invalid headers for http_response")
        if body is not None and not isinstance(body, (str, dict)):
            return r[object].fail("Invalid body for http_response")
        if elapsed_time is not None and not isinstance(elapsed_time, (float, int)):
            return r[object].fail("Invalid elapsed_time for http_response")
        return t.create_http_response(
            status_code=status_code,
            headers=headers,
            body=body,
            elapsed_time=float(elapsed_time) if elapsed_time else None,
        )
    if entry_type == "web_request":
        config_dict = dict(kwargs)
        return t.create_web_request(
            _WebRequestConfig(**config_dict),
        )
    if entry_type == "web_response":
        config_dict = dict(kwargs)
        return t.create_web_response(
            _WebResponseConfig(**config_dict),
        )
    if entry_type == "application":
        config_dict = dict(kwargs)
        return t.create_application(
            _ApplicationConfig(**config_dict),
        )
    msg = f"Unsupported entry type: {entry_type}"
    raise ValueError(msg)


def create_test_data(data_type: str, **kwargs: object) -> dict[str, t.GeneralValueType]:
    """Create test data for tests.

    This function provides a standardized way to create test data,
    reducing code duplication across test files.

    Args:
        data_type: Type of test data to create
        **kwargs: Override default data values

    Returns:
        Dictionary with test data

    """
    if data_type == "app_data":
        return {
            "name": c.Web.Tests.TestWeb.TEST_APP_NAME,
            "host": c.Web.Tests.TestWeb.DEFAULT_HOST,
            "port": c.Web.Tests.TestWeb.DEFAULT_PORT,
        } | {k: v for k, v in kwargs.items() if isinstance(v, (str, int))}
    if data_type == "entity_data":
        return {
            "id": "test-entity",
            "name": "Test Entity",
        } | {k: v for k, v in kwargs.items() if isinstance(v, (str, int))}
    if data_type == "config_data":
        return {
            "host": c.Web.Tests.TestWeb.DEFAULT_HOST,
            "port": c.Web.Tests.TestWeb.DEFAULT_PORT,
            "debug": True,
        } | {k: v for k, v in kwargs.items() if isinstance(v, (str, int, bool))}
    if data_type == "request_data":
        return {
            "method": c.Web.Tests.TestHttp.TEST_METHOD,
            "url": f"http://{c.Web.Tests.TestWeb.DEFAULT_HOST}:{c.Web.Tests.TestWeb.DEFAULT_PORT}",
            "headers": {"Content-Type": c.Web.Tests.TestHttp.TEST_CONTENT_TYPE},
        } | {k: v for k, v in kwargs.items() if isinstance(v, (str, dict))}
    if data_type == "response_data":
        return {
            "status_code": 200,
            "request_id": "test-123",
        } | {k: v for k, v in kwargs.items() if isinstance(v, (int, str))}
    msg = f"Unsupported data type: {data_type}"
    raise ValueError(msg)


def create_test_app(**kwargs: object) -> m.Web.Entity:
    """Create a test application entity using flext-core patterns.

    This function provides a standardized way to create test applications,
    reducing code duplication across test files.

    Args:
        **kwargs: Override default app properties

    Returns:
        m.Web.Entity instance

    """
    defaults: dict[str, str | int] = {
        "id": "test-id",
        "name": c.Web.Tests.TestWeb.TEST_APP_NAME,
        "host": c.Web.Tests.TestWeb.DEFAULT_HOST,
        "port": c.Web.Tests.TestWeb.DEFAULT_PORT,
    }

    defaults.update(
        {k: v for k, v in kwargs.items() if isinstance(v, (str, int))},
    )

    return m.Web.Entity(**defaults)


def create_test_result(
    *,
    success: bool = True,
    **kwargs: object,
) -> r[object]:
    """Create a test r using r API directly.

    This function provides a standardized way to create test results,
    reducing code duplication across test files.

    Args:
        success: Whether the result should be successful
        **kwargs: Additional parameters for result creation
            - data: Value for success result
            - value: Alternative key for success value
            - error: Error message for failure result

    Returns:
        r instance

    """
    if success:
        # Get value from kwargs (could be 'data' or 'value')
        value = kwargs.get("data") or kwargs.get("value")
        return r[object].ok(value)
    # Failure case
    error = str(kwargs.get("error", "Test error"))
    return r[object].fail(error)


def run_parameterized_test(
    test_cases: list[tuple[object, ...]],
    test_function: Callable[[object], r[object]],
    expected_results: list[bool],
    test_name: str = "parameterized_test",
) -> None:
    """Run parameterized tests using flext_tests patterns.

    This function provides a standardized way to run multiple test cases
    with expected results, reducing boilerplate code.

    Args:
        test_cases: List of tuples containing test case parameters
        test_function: Function to test that returns r
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
    valid_cases: list[dict[str, object]],
    invalid_cases: list[dict[str, object]],
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
    original_env: dict[str, str] = {
        k: v for k, v in os.environ.items() if isinstance(v, str)
    }

    # Set test environment variables
    os.environ["FLEXT_ENV"] = "test"
    os.environ["FLEXT_LOG_LEVEL"] = "INFO"  # Reduce noise
    os.environ["FLEXT_WEB_DEBUG_MODE"] = "true"
    os.environ["FLEXT_WEB_HOST"] = c.Web.WebDefaults.HOST
    os.environ["FLEXT_WEB_SECRET_KEY"] = c.Web.WebDefaults.TEST_SECRET_KEY

    yield

    # Restore original environment
    os.environ.clear()
    for key, value in original_env.items():
        os.environ[key] = value


@pytest.fixture
def real_config() -> FlextWebSettings:
    """Create real test configuration with required secret key.

    Fast fail if secret key cannot be provided - no fallback.
    """
    return FlextWebSettings(
        secret_key=c.Web.WebDefaults.TEST_SECRET_KEY,
    )


@pytest.fixture
def real_service(
    real_config: FlextWebSettings,
) -> FlextWebServices:
    """Create real FlextWebServices instance with clean state."""
    # Pass config object directly - no dict conversion
    result = FlextWebServices.create_service(real_config)
    assert result.is_success, f"Service creation failed: {result.error}"
    return result.value
    # Clean up service state after each test
    # Note: services don't have apps attribute in current implementation


@pytest.fixture
def real_app(real_config: FlextWebSettings) -> Flask:
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
    real_config: FlextWebSettings,
) -> Generator[FlextWebServices]:
    """Start real service in background thread with clean state."""
    # Allocate unique port to avoid conflicts
    test_port = TestPortManager.allocate_port()

    test_config = FlextWebSettings(
        host=real_config.host,
        port=test_port,
        app_name=real_config.app_name,
        version=real_config.version,
    )

    result = FlextWebServices.create_service(test_config)
    assert result.is_success, f"Service creation failed: {result.error}"
    service = result.value

    # Start service in background thread
    def run_service() -> None:
        app_result = FlextWebApp.create_flask_app(test_config)
        if app_result.is_success:
            app = app_result.value
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
        "port": c.Web.WebDefaults.PORT + 1001,
        "host": c.Web.WebDefaults.HOST,
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
        "FLEXT_WEB_HOST": c.Web.WebSpecific.ALL_INTERFACES,
        "FLEXT_WEB_PORT": str(c.Web.WebDefaults.PORT),
        "FLEXT_WEB_DEBUG": "false",
        "FLEXT_WEB_SECRET_KEY": c.Web.WebDefaults.DEV_SECRET_KEY,
    }


@pytest.fixture(scope="session")
def docker_manager() -> Generator[FlextTestsDocker]:
    """Provide FlextTestsDocker instance for integration tests."""
    try:
        yield FlextTestsDocker(workspace_root=Path().absolute())
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
