"""Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

# !/usr/bin/env python3
"""Precise test for line 903 - stop_app failure path using REAL HTTP execution."""

import threading
import time
from collections.abc import Generator

import pytest
import requests

from flext_web import (
    FlextWebConfigs,
    FlextWebServices,
)


@pytest.fixture
def real_line_903_service() -> Generator[FlextWebServices.WebService]:
    """Create real running service for line 903 test."""
    config = FlextWebConfigs.WebConfig(
        host="localhost",
        port=8099,  # Unique port for line 903 test
        secret_key="line903-test-key-32-characters-long!",
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


def test_line_903_stop_app_failure_precise(
    real_line_903_service: FlextWebServices.WebService,
) -> None:
    """Test line 903: stop_app failure path with already stopped app using real HTTP."""
    assert real_line_903_service is not None
    base_url = "http://localhost:8099"

    # Create an app (starts in STOPPED state)
    create_response = requests.post(
        f"{base_url}/api/v1/apps",
        json={
            "name": "test-stop-failure",
            "port": 8080,
            "host": "localhost",
        },
        timeout=5,
    )
    assert create_response.status_code == 201
    app_data = create_response.json()["data"]
    app_id = app_data["id"]

    # Try to stop an already stopped app (should fail and hit line 903)
    stop_response = requests.post(f"{base_url}/api/v1/apps/{app_id}/stop", timeout=5)
    assert stop_response.status_code == 400  # This hits line 903!

    error_data = stop_response.json()
    assert error_data["success"] is False
    assert "already stopped" in error_data["message"].lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
