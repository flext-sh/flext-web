#!/usr/bin/env python3
"""Precise test for line 872 - start_app failure path."""

from flext_web import FlextWebConfig, FlextWebService


def test_line_872_start_app_failure_precise() -> None:
    """Test line 872: start_app failure path with already running app."""
    config = FlextWebConfig(secret_key="test-key-32-characters-long-valid!")
    service = FlextWebService(config)
    client = service.app.test_client()

    # First create an app
    create_response = client.post(
      "/api/v1/apps",
      json={
          "name": "test-start-failure",
          "port": 8080,
          "host": "localhost",
      },
    )
    assert create_response.status_code == 200
    app_data = create_response.json["data"]
    app_id = app_data["id"]

    # Start the app first time (should succeed)
    start_response1 = client.post(f"/api/v1/apps/{app_id}/start")
    assert start_response1.status_code == 200

    # Try to start again (should fail and hit line 872)
    start_response2 = client.post(f"/api/v1/apps/{app_id}/start")
    assert start_response2.status_code == 400  # This hits line 872!

    error_data = start_response2.json
    assert error_data["success"] is False
    assert "already running" in error_data["message"].lower()


if __name__ == "__main__":
    test_line_872_start_app_failure_precise()
