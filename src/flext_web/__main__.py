"""FLEXT Web Interface - Main entry point."""

from __future__ import annotations

import argparse
import logging
import sys

from .api import FlextWebAPI

logger = logging.getLogger(__name__)


def main() -> None:
    """Main entry point for FLEXT Web Interface."""
    parser = argparse.ArgumentParser(
        description="FLEXT FlexCore Management Web Interface"
    )
    parser.add_argument(
        "--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", type=int, default=5000, help="Port to bind to (default: 5000)"
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    try:
        logger.info("🚀 Starting FLEXT FlexCore Management Web Interface")
        logger.info(f"   Host: {args.host}")
        logger.info(f"   Port: {args.port}")
        logger.info(f"   Debug: {args.debug}")

        # Create and run the web API
        web_api = FlextWebAPI()
        web_api.run(host=args.host, port=args.port, debug=args.debug)

    except KeyboardInterrupt:
        logger.info("🛑 Shutting down FLEXT Web Interface")
        sys.exit(0)
    except Exception:
        logger.exception("❌ Failed to start FLEXT Web Interface")
        sys.exit(1)


if __name__ == "__main__":
    main()
