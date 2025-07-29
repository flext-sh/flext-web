"""FlextWeb - Main entry point using Flask + flext-core patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Main entry point for FlextWeb service using flext-core standardization.
"""

from __future__ import annotations

import argparse
import sys

from flext_core import get_logger

from . import create_service, get_web_settings

logger = get_logger(__name__)


def main() -> None:
    """Main entry point for FlextWeb service."""
    parser = argparse.ArgumentParser(description="FlextWeb - Enterprise Web Interface")
    parser.add_argument("--host", help="Host to bind to (overrides config)")
    parser.add_argument("--port", type=int, help="Port to bind to (overrides config)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--no-debug", action="store_true", help="Disable debug mode")

    args = parser.parse_args()

    # Get configuration
    config = get_web_settings()

    # Override with command line arguments
    host = args.host or config.host
    port = args.port or config.port

    if args.debug:
        debug = True
    elif args.no_debug:
        debug = False
    else:
        debug = config.debug

    # Validate port
    if not (1 <= port <= 65535):
        logger.error("Port must be between 1 and 65535")
        sys.exit(1)

    try:
        logger.info(f"🚀 Starting {config.app_name} v{config.version} on {host}:{port}")
        logger.info(f"📊 Debug: {debug} | Production: {config.is_production()}")

        service = create_service(config)
        service.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down FlextWeb service")
    except (RuntimeError, ValueError, TypeError):
        logger.exception("Failed to start FlextWeb service")
        sys.exit(1)


if __name__ == "__main__":
    main()
