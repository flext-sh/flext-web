"""FLEXT Web Constants - Domain-specific constants (eliminando duplicações com flext-core).

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
from typing import Final


class FlextWebConstants:
    """Web domain-specific constants moved from FlextConstants.Web."""

    class Web:
        """Web application constants moved from FlextConstants.Web."""

        # Port constants - moved from FlextConstants.Web
        MIN_PORT: Final[int] = 1024  # Usage count: 8
        MAX_PORT: Final[int] = 65535  # Usage count: 8
        DEFAULT_PORT: Final[int] = 8080  # Usage count: 1

        # App name validation - moved from FlextConstants.Web
        MIN_APP_NAME_LENGTH: Final[int] = 2  # Usage count: 1
        MAX_APP_NAME_LENGTH: Final[int] = 50  # Usage count: 0

        # HTTP status codes - moved from FlextConstants.Web and added missing ones
        HTTP_OK: Final[int] = 200  # Usage count: 2
        HTTP_NOT_FOUND: Final[int] = 404  # Usage count: 12
        MAX_HTTP_STATUS: Final[int] = 599  # Usage count: 0

        # MIME types - added missing constants
        JSON_MIME: Final[str] = "application/json"  # Usage count: 2

    class WebSpecific:
        """Web domain-specific constants that don't belong in core FlextConstants."""

        # Environment variable específica do flext-web
        ENV_SECRET_KEY = "FLEXT_WEB_SECRET_KEY"  # nosec B105
        ENV_HOST = "FLEXT_WEB_HOST"
        ENV_PORT = "FLEXT_WEB_PORT"
        ENV_DEBUG = "FLEXT_WEB_DEBUG"

        # Default secret key com valor específico flext-web
        DEFAULT_SECRET_KEY = os.getenv(
            ENV_SECRET_KEY, "dev-secret-key-change-in-production",
        )

        # Port threshold for system ports (web-specific business rule)
        SYSTEM_PORTS_THRESHOLD = 1024

        # Network interface constants
        ALL_INTERFACES = "0.0.0.0"  # nosec B104
        LOCALHOST_IPV4 = "127.0.0.1"
        LOCALHOST_HOSTNAME = "localhost"

        # Development/test keys (properly marked for security scanners)
        DEV_SECRET_KEY = "dev-key-change-in-production-32chars!"  # nosec B105
        DEV_ENVIRONMENT_KEY = "dev-key-for-development-environment!"
        TEST_ENVIRONMENT_KEY = "test-key-for-testing-environment!"


__all__ = [
    "FlextWebConstants",
]
