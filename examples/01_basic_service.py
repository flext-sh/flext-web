#!/usr/bin/env python3
"""FLEXT Web Interface - Basic Service Example.

Simple example demonstrating how to start the FLEXT Web Interface service
with default configuration for development purposes using the refactored API.
"""

from flext_web import FlextWebServices, FlextWebSettings


def main() -> None:
    """Start FLEXT Web Interface with default configuration."""
    # Get default configuration using factory function
    config_result = FlextWebSettings.create_web_config()
    if config_result.is_failure:
        return
    config = config_result.value

    # Create service using the refactored factory function - pass config object directly
    service_result = FlextWebServices.create_web_service(config)
    if service_result.is_failure:
        return
    service = service_result.value

    try:
        # Start service with configuration already set during service creation
        service.start_service("127.0.0.1", 8000, debug=True)
    except KeyboardInterrupt:
        return
    except Exception:
        raise


if __name__ == "__main__":
    main()
