#!/usr/bin/env python3
"""FLEXT Web Interface - Basic Service Example.

Simple example demonstrating how to start the FLEXT Web Interface service
with default configuration for development purposes.
"""

from flext_web import create_service, get_web_settings


def main() -> None:
    """Start FLEXT Web Interface with default configuration."""
    # Get default configuration
    config = get_web_settings()

    # Create and start service
    service = create_service(config)

    try:
        service.run(host=config.host, port=config.port, debug=config.debug)
    except KeyboardInterrupt:
        # Allow graceful shutdown in examples
        return
    except Exception:
        # Log or handle as needed in real app; keep examples simple
        raise


if __name__ == "__main__":
    main()
