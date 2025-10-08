#!/usr/bin/env python3
"""FLEXT Web Interface - Basic Service Example.

Simple example demonstrating how to start the FLEXT Web Interface service
with default configuration for development purposes using the refactored API.
"""

from flext_web import FlextWebConfig, FlextWebService


def main() -> None:
    """Start FLEXT Web Interface with default configuration."""
    # Get default configuration using factory function
    config_result = FlextWebConfig.create_web_config()
    if config_result.is_failure:
        print(f"Configuration creation failed: {config_result.error}")
        return
    config = config_result.value

    # Create service using the refactored factory function
    service_result = FlextWebService.create_web_service(config.model_dump())
    if service_result.is_failure:
        print(f"Service creation failed: {service_result.error}")
        return
    service = service_result.value

    try:
        # Start service with configuration already set during service creation
        service.start_service("127.0.0.1", 8000, debug=True)
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(f"Service error: {e}")
        raise


if __name__ == "__main__":
    main()
