"""FLEXT Web Interface - Basic Service Example.

Simple example demonstrating how to start the FLEXT Web Interface service
with default configuration for development purposes using the refactored API.
"""

from __future__ import annotations

from flext_web import FlextWebServices, FlextWebSettings


def main() -> None:
    """Start FLEXT Web Interface with default configuration."""
    config = FlextWebSettings(
        app_name="flext-web",
        host="127.0.0.1",
        port=8000,
        debug_mode=True,
        debug=True,
        testing=False,
        secret_key="dev-secret-key-32-characters-long",
    )
    service_result = FlextWebServices.create_web_service(config)
    if service_result.is_failure:
        return
    service = service_result.value
    try:
        _ = service.start_service("127.0.0.1", 8000, _debug=True)
    except KeyboardInterrupt:
        return
    except Exception:
        raise


if __name__ == "__main__":
    main()
