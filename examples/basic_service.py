#!/usr/bin/env python3
"""FLEXT Web Interface - Basic Service Example.

Simple example demonstrating how to start the FLEXT Web Interface service
with default configuration for development purposes using the refactored API.
"""

from flext_web import create_service, get_web_settings


def main() -> None:
    """Start FLEXT Web Interface with default configuration."""
    # Get default configuration using factory function
    config = get_web_settings()

    # Create service using the refactored factory function
    service = create_service(config)

    try:
        # Use keyword-only arguments for debug flag (FBT compliance)
        service.run(host=config.host, port=config.port, debug=config.debug)
    except KeyboardInterrupt:
        return
    except Exception:
        raise


if __name__ == "__main__":
    main()
