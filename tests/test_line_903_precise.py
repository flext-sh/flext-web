#!/usr/bin/env python3
"""Precise test for line 903 - stop_app failure path."""

from flext_web import FlextWebConfig, FlextWebService


def test_line_903_stop_app_failure_precise() -> None:
    """Test line 903: stop_app failure path with already stopped app."""
    config = FlextWebConfig(secret_key="test-key-32-characters-long-valid!")
    service = FlextWebService(config)
    client = service.app.test_client()

    # Create an app (starts in STOPPED state)
    create_response = client.post(
      "/api/v1/apps",
      json={
          "name": "test-stop-failure",
          "port": 8080,
          "host": "localhost",
      },
    )
    assert create_response.status_code == 200
    app_data = create_response.json["data"]
    app_id = app_data["id"]

    # Try to stop an already stopped app (should fail and hit line 903)
    stop_response = client.post(f"/api/v1/apps/{app_id}/stop")
    assert stop_response.status_code == 400  # This hits line 903!

    error_data = stop_response.json
    assert error_data["success"] is False
    assert "already stopped" in error_data["message"].lower()


if __name__ == "__main__":
    test_line_903_stop_app_failure_precise()
