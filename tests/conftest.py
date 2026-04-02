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
from collections.abc import Generator, Mapping
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

import pytest
from flask import Flask
from flext_tests import tk

from flext_web import web
from tests import c, t

if TYPE_CHECKING:
    from flext_web import FlextWebSettings


@pytest.fixture(autouse=True)
def setup_test_environment() -> Generator[None]:
    """Set up test environment with real configuration."""
    original_env: t.StrMapping = dict(os.environ)
    os.environ["FLEXT_ENV"] = "test"
    os.environ["FLEXT_LOG_LEVEL"] = "INFO"
    os.environ["FLEXT_WEB_DEBUG_MODE"] = "true"
    os.environ["FLEXT_WEB_HOST"] = c.Web.WebDefaults.HOST
    os.environ["FLEXT_WEB_SECRET_KEY"] = c.Web.WebDefaults.TEST_SECRET_KEY
    yield
    os.environ.clear()
    for key, value in original_env.items():
        os.environ[key] = value


@pytest.fixture
def real_config() -> FlextWebSettings:
    """Create real test configuration with required secret key.

    Fast fail if secret key cannot be provided - no fallback.
    """
    result = web.settings.create_web_config(
        secret_key=c.Web.WebDefaults.TEST_SECRET_KEY,
    )
    assert result.is_success, result.error
    return result.value


@pytest.fixture
def real_service(real_config: FlextWebSettings) -> object:
    """Create a real service instance through the public `web` facade."""
    result = web.create_service(real_config)
    assert result.is_success, f"Service creation failed: {result.error}"
    return result.value


@pytest.fixture
def real_app(real_config: FlextWebSettings) -> Flask:
    """Create real Flask app."""
    app = Flask(__name__)
    app.config.update(SECRET_KEY=real_config.secret_key, TESTING=True)
    return app


@pytest.fixture
def running_service(real_config: FlextWebSettings) -> Generator[object]:
    """Start a real service through the public `web` facade."""
    test_port = TestPortManager.allocate_port()
    test_config = real_config.model_copy(
        update={
            "host": real_config.host,
            "port": test_port,
            "app_name": real_config.app_name,
        },
    )
    result = web.create_service(test_config)
    assert result.is_success, f"Service creation failed: {result.error}"
    service = result.value

    def run_service() -> None:
        app_result = web.create_flask_app(test_config)
        if app_result.is_success:
            app = app_result.value
            app.run(
                host=test_config.host,
                port=test_config.port,
                debug=False,
                use_reloader=False,
                threaded=True,
            )

    server_thread = threading.Thread(target=run_service, daemon=True)
    server_thread.start()

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

    if not wait_for_port(test_config.port, timeout=5.0):
        pytest.fail(
            f"Service failed to start on port {test_config.port} within 5 seconds",
        )
    yield service
    TestPortManager.release_port(test_port)


@pytest.fixture
def test_app_data() -> Mapping[str, str | int]:
    """Real application data for testing."""
    return {
        "name": "test-application",
        "port": c.Web.WebDefaults.PORT + 1001,
        "host": c.Web.WebDefaults.HOST,
    }


@pytest.fixture
def invalid_app_data() -> Mapping[str, str | int]:
    """Invalid application data for error testing."""
    return {"name": "", "port": 99999, "host": ""}


@pytest.fixture
def production_config() -> t.StrMapping:
    """Production-like configuration for testing."""
    return {
        "FLEXT_WEB_HOST": c.Web.WebSpecific.ALL_INTERFACES,
        "FLEXT_WEB_PORT": str(c.Web.WebDefaults.PORT),
        "FLEXT_WEB_DEBUG": "false",
        "FLEXT_WEB_SECRET_KEY": c.Web.WebDefaults.DEV_SECRET_KEY,
    }


@pytest.fixture(scope="session")
def docker_manager() -> Generator[tk]:
    """Provide tk instance for integration tests."""
    try:
        yield tk(workspace_root=Path().absolute())
    except ImportError:
        pytest.skip("tk not available")
    except (ConnectionError, TimeoutError, OSError, RuntimeError) as e:
        pytest.skip(f"tk initialization failed: {e}")


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
            while cls._current_port in cls._allocated_ports:
                cls._current_port += 1
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
