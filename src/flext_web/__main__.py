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
from flext_web.models import FlextWebModels


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

    def run(self) -> FlextResult[bool]:
        """Run HTTP service operations.

        Returns:
            FlextResult[bool]: Success contains True if service is operational,
                             failure contains error message

        """
        # Use monadic pattern for status check with side-effect logging
        return self._api.get_service_status().map(self._log_status_and_return)

    def _log_status_and_return(
        self,
        status_data: FlextWebModels.Service.ServiceResponse,
    ) -> bool:
        """Log service status and return True for success - internal state management.

        Args:
            status_data: Service status response data

        Returns:
            bool: Always True when called (indicates successful status check)

        """
        self._logger.info(f"Service status: {status_data.service}")
        return True

    @staticmethod
    def main() -> None:
        """CLI entry point - static method following flext-core patterns."""
        logger = FlextLogger(__name__)
        cli_service = FlextWebCliService()

        # Use monadic pattern - handle failure and exit
        result = cli_service.run()

        # Process result - fast fail on error, no fallback
        if result.is_failure:  # pragma: no cover
            logger.error(f"Service failed: {result.error}")
            sys.exit(1)

        # Success - exit normally
        sys.exit(0)


if __name__ == "__main__":  # pragma: no cover
    FlextWebCliService.main()


__all__ = ["FlextWebCliService"]
