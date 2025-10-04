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
    class WebServer:
        """Web server constants and configuration values."""

        DEFAULT_HOST: str = "localhost"
        MIN_PORT: int = 1024
        MAX_PORT: int = 65535
        DEFAULT_PORT: int = 8080

        # =============================================================================
        # HTTP CONSTANTS - Moved to flext-core.FlextConstants.Http
        # Use FlextConstants.Http.HTTP_OK, FlextConstants.Http.HTTP_CREATED, etc.
        # Use FlextConstants.Http.HTTP_SUCCESS_MIN, HTTP_SUCCESS_MAX, etc.
        # Use FlextConstants.Http.HTTPS_PORT, HTTPS_ALT_PORT, etc.
        # =============================================================================

        # App Name Validation
        MIN_APP_NAME_LENGTH: int = 3
        MAX_APP_NAME_LENGTH: int = 100

        # Security Constants
        MIN_SECRET_KEY_LENGTH: int = 32

    # Web-Specific Constants
    class WebSpecific:
        """Web-specific constants for development and security."""

        # Default server configuration
        DEFAULT_HOST: str = "localhost"
        DEFAULT_PORT: int = 8080

        DEV_SECRET_KEY: str = "dev-secret-key-32-characters-long-for-development"
        DEV_ENVIRONMENT_KEY: str = "dev-environment-key-32-characters-long-for-testing"
        TEST_ENVIRONMENT_KEY: str = "test-environment-key-32-characters-long-for-tests"
        ALL_INTERFACES: str = "0.0.0.0"
        LOCALHOST_IP: str = "127.0.0.1"
        SYSTEM_PORTS_THRESHOLD: int = 1023
        PRIVILEGED_PORTS_MAX: int = 1023


__all__ = [
    "FlextWebConstants",
]
