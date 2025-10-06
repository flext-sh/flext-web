"""FLEXT Web Constants - Domain-specific constants extending flext-core.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar, Literal

from flext_core import FlextConstants


class FlextWebConstants(FlextConstants):
    """Enhanced web domain-specific constants extending FlextConstants.

    Contains comprehensive constants for FLEXT web applications with
    enhanced organization, validation limits, and security considerations.
    Follows flext-core namespace pattern with nested constant groups.
    """

    # =============================================================================
    # WEB SERVER CONSTANTS - Server configuration and validation
    # =============================================================================

    class WebServer:
        """Web server constants and configuration values."""

        # Server Configuration
        DEFAULT_HOST: str = "localhost"
        MIN_PORT: int = 1024
        MAX_PORT: int = 65535
        DEFAULT_PORT: int = 8080

        # App Name Validation
        MIN_APP_NAME_LENGTH: int = 3
        MAX_APP_NAME_LENGTH: int = 100

        # Security Constants
        MIN_SECRET_KEY_LENGTH: int = 32

    # =============================================================================
    # WEB-SPECIFIC CONSTANTS - Development and security
    # =============================================================================

    class WebSpecific:
        """Web-specific constants for development and security."""

        # Default server configuration
        DEFAULT_HOST: str = "localhost"
        DEFAULT_PORT: int = 8080

        # Development Keys (32+ characters for security)
        DEV_SECRET_KEY: str = "dev-secret-key-32-characters-long-for-development"
        DEV_ENVIRONMENT_KEY: str = "dev-environment-key-32-characters-long-for-testing"
        TEST_ENVIRONMENT_KEY: str = "test-environment-key-32-characters-long-for-tests"

        # Network Configuration
        ALL_INTERFACES: str = "0.0.0.0"
        LOCALHOST_IP: str = "127.0.0.1"
        SYSTEM_PORTS_THRESHOLD: int = 1023
        PRIVILEGED_PORTS_MAX: int = 1023

    # =============================================================================
    # WEB ENVIRONMENT TYPES - Literal types for environment validation
    # =============================================================================

    class WebEnvironment:
        """Web environment type definitions."""

        # Environment Types
        type EnvironmentType = Literal[
            "development", "testing", "staging", "production"
        ]

        # Web Application Types
        type WebAppType = Literal[
            "webapp",
            "spa",
            "api-server",
            "web-service",
            "microservice",
            "rest-api",
            "web-portal",
            "dashboard",
            "REDACTED_LDAP_BIND_PASSWORD-panel",
        ]

        # HTTP Methods
        type HttpMethod = Literal[
            "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"
        ]

        # Web Status Types
        type WebStatus = Literal[
            "stopped",
            "starting",
            "running",
            "stopping",
            "error",
            "maintenance",
            "deploying",
        ]

    # =============================================================================
    # WEB SECURITY CONSTANTS - Security-related constants
    # =============================================================================

    class WebSecurity:
        """Web security constants and validation rules."""

        # CORS Configuration
        CORS_DEFAULT_ORIGINS: ClassVar[list[str]] = ["*"]
        CORS_SAFE_METHODS: ClassVar[list[str]] = ["GET", "HEAD", "OPTIONS"]
        CORS_SAFE_HEADERS: ClassVar[list[str]] = ["Content-Type", "Authorization"]

        # Session Security
        SESSION_COOKIE_SECURE_DEFAULT: bool = False
        SESSION_COOKIE_HTTPONLY_DEFAULT: bool = True
        SESSION_COOKIE_SAMESITE_DEFAULT: str = "Lax"

        # SSL/TLS Configuration
        SSL_DEFAULT_PORT: int = 443
        SSL_ALT_PORT: int = 8443

    # =============================================================================
    # WEB VALIDATION CONSTANTS - Input validation rules
    # =============================================================================

    class WebValidation:
        """Web validation constants and rules."""

        # Content Length Limits
        MAX_CONTENT_LENGTH_DEFAULT: int = 16 * 1024 * 1024  # 16MB
        MIN_CONTENT_LENGTH: int = 0

        # Request Timeout
        REQUEST_TIMEOUT_DEFAULT: int = 30  # seconds
        REQUEST_TIMEOUT_MAX: int = 600  # 10 minutes

        # URL Validation
        MAX_URL_LENGTH: int = 2048
        MIN_URL_LENGTH: int = 1

        # Header Validation
        MAX_HEADER_LENGTH: int = 8192
        MAX_HEADERS_COUNT: int = 100


__all__ = [
    "FlextWebConstants",
]
