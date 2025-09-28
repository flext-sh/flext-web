"""FLEXT Web Constants - Domain-specific constants (eliminando duplicações com flext-core).

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextConstants


class FlextWebConstants(FlextConstants):
    """Enhanced web domain-specific constants extending FlextConstants.

    Contains comprehensive constants for FLEXT web applications with
    enhanced organization, validation limits, and security considerations.
    """

    # Web Server Constants
    class Web:
        """Web server constants and configuration values."""

        DEFAULT_HOST: str = "localhost"
        MIN_PORT: int = 1024
        MAX_PORT: int = 65535
        DEFAULT_PORT: int = 8080

        # HTTP Status Constants
        HTTP_OK: int = 200
        HTTP_CREATED: int = 201
        HTTP_MULTIPLE_CHOICES: int = 300
        HTTP_BAD_REQUEST: int = 400
        HTTP_NOT_FOUND: int = 404
        HTTP_INTERNAL_ERROR: int = 500
        MAX_HTTP_STATUS: int = 599

        # HTTP Status Ranges
        HTTP_INFORMATIONAL_MIN: int = 100
        HTTP_INFORMATIONAL_MAX: int = 199
        HTTP_SUCCESS_MIN: int = 200
        HTTP_SUCCESS_MAX: int = 299
        HTTP_REDIRECTION_MIN: int = 300
        HTTP_REDIRECTION_MAX: int = 399
        HTTP_CLIENT_ERROR_MIN: int = 400
        HTTP_CLIENT_ERROR_MAX: int = 499
        HTTP_SERVER_ERROR_MIN: int = 500
        HTTP_SERVER_ERROR_MAX: int = 599

        # HTTPS Ports
        HTTPS_PORT: int = 443
        HTTPS_ALT_PORT: int = 8443

        # App Name Validation
        MIN_APP_NAME_LENGTH: int = 3
        MAX_APP_NAME_LENGTH: int = 100

        # Security Constants
        MIN_SECRET_KEY_LENGTH: int = 32

    # Web-Specific Constants
    class WebSpecific:
        """Web-specific constants for development and security."""

        DEV_SECRET_KEY: str = "dev-secret-key-32-characters-long-for-development"
        DEV_ENVIRONMENT_KEY: str = "dev-environment-key-32-characters-long-for-testing"
        TEST_ENVIRONMENT_KEY: str = "test-environment-key-32-characters-long-for-tests"
        ALL_INTERFACES: str = "0.0.0.0"  # noqa: S104
        LOCALHOST_IP: str = "127.0.0.1"
        SYSTEM_PORTS_THRESHOLD: int = 1023
        PRIVILEGED_PORTS_MAX: int = 1023


__all__ = [
    "FlextWebConstants",
]
