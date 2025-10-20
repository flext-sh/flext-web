"""Generic HTTP CLI Service - flext-cli Integration.

Domain-agnostic CLI service using flext-cli exclusively for all CLI operations.
Follows SOLID principles with single responsibility and proper delegation.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys

from flext_core import FlextLogger, FlextResult

from flext_web.api import FlextWebApi


class FlextWebCliService:
    """Generic HTTP CLI service.

    Single Responsibility: Provides HTTP service operations.
    Uses FlextWebApi for HTTP operations following SOLID patterns.
    """

    def __init__(self) -> None:
        """Initialize HTTP service."""
        super().__init__()
        self._logger = FlextLogger(__name__)
        self._api = FlextWebApi()

    def run(self) -> FlextResult[None]:
        """Run HTTP service operations."""
        try:
            # Get service status as health check
            status_result = self._api.get_service_status()
            if status_result.is_success:
                self._logger.info(
                    f"Service status: {status_result.unwrap().get('service', 'unknown')}"
                )
                return FlextResult[None].ok(None)
            return FlextResult[None].fail(
                f"Service status check failed: {status_result.error}"
            )
        except Exception as e:
            return FlextResult[None].fail(f"Service execution failed: {e}")


def main() -> None:
    """CLI entry point."""
    cli_service = FlextWebCliService()
    result = cli_service.run()

    if result.is_failure:
        FlextLogger(__name__).error(f"Service failed: {result.error}")
        sys.exit(1)


if __name__ == "__main__":
    main()


__all__ = ["FlextWebCliService", "main"]
