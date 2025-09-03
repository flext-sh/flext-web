#!/usr/bin/env python3
"""FLEXT Web Interface - Docker-Ready Service Example.

Docker-optimized service configuration with proper signal handling,
environment variable support, and production-ready patterns.
"""

import os
import secrets
import signal
import sys

from flext_core.loggings import FlextLogger

from flext_web import FlextWebConfigs

logger = FlextLogger(__name__)


def create_docker_config() -> FlextWebConfigs.WebConfig:
    """Create Docker-optimized configuration from environment variables."""
    # Read configuration from environment
    host = os.environ.get("FLEXT_WEB_HOST", "127.0.0.1")
    port = int(os.environ.get("FLEXT_WEB_PORT", "8080"))
    debug = os.environ.get("FLEXT_WEB_DEBUG", "false").lower() == "true"
    secret_key = os.environ.get("FLEXT_WEB_SECRET_KEY")

    # Generate secure secret key if not provided
    if not secret_key:
        secret_key = secrets.token_urlsafe(32)
        logger.warning("No SECRET_KEY provided, generated temporary key")

    config = FlextWebConfigs.WebConfig(
        host=host, port=port, debug=debug, secret_key=secret_key
    )

    # Validate configuration
    validation_result = config.validate_config()
    if not validation_result.success:
        logger.error(f"Configuration validation failed: {validation_result.error}")
        sys.exit(1)

    return config


def setup_signal_handlers() -> None:
    """Setup graceful shutdown signal handlers."""

    def signal_handler(signum: int, _frame: object) -> None:
        signal_name = signal.Signals(signum).name
        logger.info(f"Received {signal_name}, shutting down gracefully...")
        sys.exit(0)

    # Handle common Docker signals
    signal.signal(signal.SIGTERM, signal_handler)  # Docker stop
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C

    logger.info("Signal handlers configured for graceful shutdown")


def main() -> None:
    """Docker container entry point."""
    logger.info("🐳 Starting FLEXT Web Interface in Docker container")

    # Setup signal handling
    setup_signal_handlers()

    # Create configuration
    config = create_docker_config()
    logger.info(
        f"📊 Configuration: {config.host}:{config.port} (debug: {config.debug})",
    )

    # Validate production requirements
    if not config.debug:
        logger.info("🔒 Running in production mode")
        if "change-in-production" in config.secret_key:
            logger.error("❌ Default secret key detected in production mode")
            sys.exit(1)

    # Create service
    from flext_web import FlextWebServices

    service_result = FlextWebServices.create_web_service(config)
    if service_result.is_failure:
        logger.error(f"Failed to create service: {service_result.error}")
        sys.exit(1)
    service = service_result.value
    logger.info("✅ Service created successfully")

    try:
        logger.info(
            f"🌐 Service starting on all interfaces ({config.host}:{config.port})",
        )
        logger.info("🔍 Health check: /health")
        logger.info("📋 API endpoints: /api/v1/*")
        logger.info("🎛️ Dashboard: /")

        # Start service (this blocks until shutdown)
        service.run()

    except KeyboardInterrupt:
        logger.info("🛑 Service interrupted by user")
    except Exception:
        logger.exception("❌ Service error")
        sys.exit(1)
    finally:
        logger.info("🔄 Service shutdown complete")


if __name__ == "__main__":
    main()
