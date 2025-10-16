"""FLEXT Web Constants - Domain-specific constants extending flext-core.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar, Literal

from flext_core import FlextConstants, FlextTypes


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

        # Default Keys (32+ characters for security)
        DEFAULT_SECRET_KEY: str = "default-secret-key-32-characters-long-for-security"
        DEV_SECRET_KEY: str = "dev-secret-key-32-characters-long-for-dev-environment"
        DEV_ENVIRONMENT_KEY: str = "dev-environment-key-32-characters-long-for-dev"
        TEST_ENVIRONMENT_KEY: str = "test-environment-key-32-characters-long-for-test"

        # Network Configuration
        # Note: Binding to all interfaces (0.0.0.0) is legitimate for web servers
        # that need to accept connections from any network interface
        ALL_INTERFACES: str = "0.0.0.0"
        LOCALHOST_IP: str = "127.0.0.1"
        SYSTEM_PORTS_THRESHOLD: int = 1023
        PRIVILEGED_PORTS_MAX: int = 1023

    # =============================================================================
    # WEB TYPES - Type definitions for web applications
    # =============================================================================

    class WebEnvironment:
        """Web environment type definitions."""

        # Environment Types
        type EnvironmentType = Literal[
            "development",
            "staging",
            "production",
            "testing",
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
        CORS_DEFAULT_ORIGINS: ClassVar[FlextTypes.StringList] = ["*"]
        CORS_SAFE_METHODS: ClassVar[FlextTypes.StringList] = [
            "GET",
            "HEAD",
            "OPTIONS",
        ]
        CORS_SAFE_HEADERS: ClassVar[FlextTypes.StringList] = [
            "Content-Type",
            "Authorization",
        ]

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

    # =============================================================================
    # HTTP STATUS CODES - Standard HTTP status code constants
    # =============================================================================

    class HttpStatus:
        """HTTP status code constants for web responses."""

        # 1xx Informational
        CONTINUE: int = 100
        SWITCHING_PROTOCOLS: int = 101
        PROCESSING: int = 102
        EARLY_HINTS: int = 103

        # 2xx Successful
        OK: int = 200
        CREATED: int = 201
        ACCEPTED: int = 202
        NON_AUTHORITATIVE_INFORMATION: int = 203
        NO_CONTENT: int = 204
        RESET_CONTENT: int = 205
        PARTIAL_CONTENT: int = 206
        MULTI_STATUS: int = 207
        ALREADY_REPORTED: int = 208
        IM_USED: int = 226

        # 3xx Redirection
        MULTIPLE_CHOICES: int = 300
        MOVED_PERMANENTLY: int = 301
        FOUND: int = 302
        SEE_OTHER: int = 303
        NOT_MODIFIED: int = 304
        USE_PROXY: int = 305
        TEMPORARY_REDIRECT: int = 307
        PERMANENT_REDIRECT: int = 308

        # 4xx Client Error
        BAD_REQUEST: int = 400
        UNAUTHORIZED: int = 401
        PAYMENT_REQUIRED: int = 402
        FORBIDDEN: int = 403
        NOT_FOUND: int = 404
        METHOD_NOT_ALLOWED: int = 405
        NOT_ACCEPTABLE: int = 406
        PROXY_AUTHENTICATION_REQUIRED: int = 407
        REQUEST_TIMEOUT: int = 408
        CONFLICT: int = 409
        GONE: int = 410
        LENGTH_REQUIRED: int = 411
        PRECONDITION_FAILED: int = 412
        PAYLOAD_TOO_LARGE: int = 413
        URI_TOO_LONG: int = 414
        UNSUPPORTED_MEDIA_TYPE: int = 415
        RANGE_NOT_SATISFIABLE: int = 416
        EXPECTATION_FAILED: int = 417
        IM_A_TEAPOT: int = 418
        MISDIRECTED_REQUEST: int = 421
        UNPROCESSABLE_ENTITY: int = 422
        LOCKED: int = 423
        FAILED_DEPENDENCY: int = 424
        TOO_EARLY: int = 425
        UPGRADE_REQUIRED: int = 426
        PRECONDITION_REQUIRED: int = 428
        TOO_MANY_REQUESTS: int = 429
        REQUEST_HEADER_FIELDS_TOO_LARGE: int = 431
        UNAVAILABLE_FOR_LEGAL_REASONS: int = 451

        # 5xx Server Error
        INTERNAL_SERVER_ERROR: int = 500
        NOT_IMPLEMENTED: int = 501
        BAD_GATEWAY: int = 502
        SERVICE_UNAVAILABLE: int = 503
        GATEWAY_TIMEOUT: int = 504
        HTTP_VERSION_NOT_SUPPORTED: int = 505
        VARIANT_ALSO_NEGOTIATES: int = 506
        INSUFFICIENT_STORAGE: int = 507
        LOOP_DETECTED: int = 508
        NOT_EXTENDED: int = 510
        NETWORK_AUTHENTICATION_REQUIRED: int = 511

        # Status code ranges
        INFORMATIONAL_MAX: int = 199
        SUCCESS_MAX: int = 299
        REDIRECTION_MAX: int = 399
        CLIENT_ERROR_MAX: int = 499
        SERVER_ERROR_MAX: int = 599


__all__ = [
    "FlextWebConstants",
]
