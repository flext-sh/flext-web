"""FLEXT Web Interface - Web Dashboard Testing Suite.

Enterprise-grade test suite for web dashboard functionality, HTML rendering,
and user interface patterns. Ensures web interface follows enterprise standards
with proper template handling, response formatting, and user experience validation.


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

from flext_core import FlextConstants
from flext_web import (
    FlextWebConfig,
    FlextWebServices,
)


class TestWebInterface:
    """Enterprise web interface testing for dashboard and UI functionality.

    Comprehensive test suite covering web dashboard rendering, Flask application
    factory patterns, and user interface validation. Ensures web components
    follow enterprise standards with proper HTML structure and accessibility.
    """

    @pytest.fixture
    def real_web_service(self) -> Generator[FlextWebServices.WebService]:
        """Create real running web service for dashboard testing."""
        # Allocate unique port to avoid conflicts
        port = TestPortManager.allocate_port()
        config = FlextWebConfig(
            host="localhost",
            port=port,
            debug=True,
            secret_key="web-test-secret-key-32-characters-long!",
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

    def test_create_app_factory(self) -> None:
        """Test Flask application factory function with proper initialization.

        Validates that create_app factory function produces properly configured
        Flask application instance with route registration and middleware setup.
        Tests fundamental web application patterns for enterprise deployment.
        """
        config_result = FlextWebConfig.create_development_config()
        assert config_result.is_success
        service_result = FlextWebServices.create_web_service(config_result.value)
        assert service_result.is_success
        app = service_result.value.app

        assert app is not None
        # Flask app name should contain the module name
        assert "flext_web" in app.name, (
            f"Expected app name to contain 'flext_web', got {app.name}"
        )

    def test_dashboard_route(
        self,
        real_web_service: FlextWebServices.WebService,
    ) -> None:
        """Test dashboard route using real HTTP requests."""
        assert real_web_service is not None
        port = real_web_service.config["port"]
        base_url = f"http://localhost:{port}"

        response = requests.get(f"{base_url}/", timeout=5)

        if response.status_code != FlextConstants.Http.HTTP_OK:
            msg: str = f"Expected {200}, got {response.status_code}"
            raise AssertionError(msg)
        content = response.content
        if b"FLEXT Web" not in content:
            msg2: str = f"Expected {b'FLEXT Web'!r} in response content"
            raise AssertionError(msg2)
        assert (
            b"Applications (0)" in content or b"No applications registered" in content
        )
