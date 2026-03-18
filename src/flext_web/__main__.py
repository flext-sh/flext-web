"""Generic HTTP CLI Service - flext-cli Integration.

Domain-agnostic CLI service using flext-cli exclusively for all CLI operations.
Follows SOLID principles with single responsibility and proper delegation.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys

from flext_core import FlextLogger, r

from flext_web import FlextWebApi, FlextWebModels


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

    @staticmethod
    def main() -> None:
        """CLI entry point - static method following flext-core patterns."""
        logger = FlextLogger(__name__)
        cli_service = FlextWebCliService()
        result = cli_service.run()
        if result.is_failure:
            _ = logger.error(f"Service failed: {result.error}")
            sys.exit(1)
        sys.exit(0)

    def run(self) -> r[bool]:
        """Run HTTP service operations.

        Returns:
            r[bool]: Success contains True if service is operational,
                             failure contains error message

        """
        status_result = self._api.get_service_status()
        return status_result.map(self._log_status_and_return)

    def _log_status_and_return(
        self,
        status_data: FlextWebModels.Web.ServiceResponse,
    ) -> bool:
        """Log service status and return True for success - internal state management.

        Args:
            status_data: Service status response data

        Returns:
            bool: Always True when called (indicates successful status check)

        """
        _ = self._logger.info(f"Service status: {status_data.service}")
        return True


if __name__ == "__main__":
    FlextWebCliService.main()
__all__ = ["FlextWebCliService"]
