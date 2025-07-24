#!/usr/bin/env python3
"""Startup script for FLEXT Web Interface."""

import logging
import os
import sys

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "flext-core", "src"))

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def main() -> None:
    """Run the FLEXT Web Interface."""
    try:
        from flext_web.api import FlextWebAPI

        web_api = FlextWebAPI()
        web_api.run(host="0.0.0.0", port=8080, debug=True)

    except KeyboardInterrupt:
        pass
    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    main()
