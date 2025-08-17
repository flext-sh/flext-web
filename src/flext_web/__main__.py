"""FLEXT Web Interface - Command Line Entry Point.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Command-line interface entry point for the FLEXT Web Interface service.
Provides argument parsing, configuration management, and service initialization
with comprehensive error handling and logging integration.

The CLI supports configuration override through command-line arguments while
maintaining compatibility with environment-based configuration patterns from
flext-core. All operations follow enterprise-grade error handling and logging
standards.

Command Line Options:
    --host: Override server bind address from configuration
    --port: Override server port number from configuration
    --debug: Force enable debug mode regardless of configuration
    --no-debug: Force disable debug mode regardless of configuration

Integration:
    - Built on flext-core logging and configuration patterns
    - Integrates with FlextWebConfig for environment variable support
    - Uses FlextWebService for actual service implementation
    - Follows enterprise CLI design patterns with proper error codes

Example:
    Basic service startup with default configuration:

    >>> python -m flext_web

    Production deployment with custom host and port:

    >>> python -m flext_web --host 0.0.0.0 --port 8080 --no-debug

Author: FLEXT Development Team
Version: 0.9.0
Status: Development (targeting 1.0.0 production release)

"""

from __future__ import annotations

import argparse
import sys

from flext_core import get_logger

from flext_web.web_config import FlextWebConfig

# Import directly from modules to avoid circular imports
from flext_web.web_service import FlextWebService

logger = get_logger(__name__)


def main() -> None:
    """Provide CLI entry point for FLEXT Web Interface.

    Provides comprehensive command-line interface for starting the FLEXT Web
    Interface service with argument parsing, configuration validation, and
    enterprise-grade error handling. Supports configuration override through
    command-line arguments while maintaining environment variable integration.

    The function handles the complete service lifecycle including:
    - Command-line argument parsing and validation
    - Configuration loading and validation
    - Service initialization and startup
    - Graceful shutdown handling
    - Comprehensive error reporting and logging

    Command Line Arguments:
      --host: Server bind address override (default from config)
      --port: Server port number override (default from config)
      --debug: Force enable debug mode
      --no-debug: Force disable debug mode

    Exit Codes:
      0: Successful execution or graceful shutdown
      1: Configuration error, startup failure, or runtime exception

    Raises:
      SystemExit: On configuration validation failure or startup error

    Side Effects:
      - Initializes logging system with structured output
      - Validates configuration against business rules
      - Starts HTTP server with specified configuration
      - Registers signal handlers for graceful shutdown

    Example:
      Development mode with custom configuration:

      >>> main()  # Uses default configuration

      The function is typically called from the command line:

      $ python -m flext_web --host localhost --port 8080 --debug

    """
    parser = argparse.ArgumentParser(description="FlextWeb - Enterprise Web Interface")
    parser.add_argument("--host", help="Host to bind to (overrides config)")
    parser.add_argument("--port", type=int, help="Port to bind to (overrides config)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--no-debug", action="store_true", help="Disable debug mode")

    args = parser.parse_args()

    # Get configuration
    config = FlextWebConfig()

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
    max_port_number = 65535
    if not (1 <= port <= max_port_number):
      logger.error("Port must be between 1 and 65535")
      sys.exit(1)

    try:
      logger.info(
          "🚀 Starting %s v%s on %s:%d",
          config.app_name,
          config.version,
          host,
          port,
      )
      logger.info("📊 Debug: %s | Production: %s", debug, config.is_production())

      service = FlextWebService(config)
      service.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
      logger.info("🛑 Shutting down FlextWeb service")
    except (RuntimeError, ValueError, TypeError):
      logger.exception("Failed to start FlextWeb service")
      sys.exit(1)


if __name__ == "__main__":
    main()
