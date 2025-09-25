"""Precise test for line 872 - start_app failure path using REAL HTTP execution.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

import threading
import time
from collections.abc import Generator

import pytest
import requests

from flext_web import (
    FlextWebConfig,
    FlextWebServices,
)


@pytest.fixture
def real_line_872_service() -> Generator[FlextWebServices.WebService]:
    """Create real running service for line 872 test."""
    config = FlextWebConfig.WebConfig(
        host="localhost",
        port=8098,  # Unique port for line 872 test
        secret_key="line872-test-key-32-characters-long!",
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


def test_line_872_start_app_failure_precise(
    real_line_872_service: FlextWebServices.WebService,
) -> None:
    """Test line 872: start_app failure path with already running app using real HTTP."""
    assert real_line_872_service is not None
    base_url = "http://localhost:8098"

    # First create an app
    create_response = requests.post(
        f"{base_url}/api/v1/apps",
        json={
            "name": "test-start-failure",
            "port": 8080,
            "host": "localhost",
        },
        timeout=5,
    )
    assert create_response.status_code == 201
    app_data = create_response.json()["data"]
    app_id = app_data["id"]

    # Start the app first time (should succeed)
    start_response1 = requests.post(f"{base_url}/api/v1/apps/{app_id}/start", timeout=5)
    assert start_response1.status_code == 200

    # Verify app is running
    start_data1 = start_response1.json()
    assert start_data1["success"] is True

    # Try to start again (should fail and hit line 872)
    start_response2 = requests.post(f"{base_url}/api/v1/apps/{app_id}/start", timeout=5)
    assert start_response2.status_code == 400  # This hits line 872!

    error_data = start_response2.json()
    assert error_data["success"] is False
    assert "already running" in error_data["message"].lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
