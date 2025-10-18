"""FLEXT Web Constants - Generic Enterprise Constants System using Python 3.13+.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar, Literal

from flext_core import FlextConstants


class FlextWebConstants(FlextConstants):
    """Generic FLEXT web constants using advanced consolidation patterns."""

    # Consolidated server configuration
    DEFAULT_HOST: str = "localhost"
    DEFAULT_PORT: int = 8080
    PORT_RANGE: tuple[int, int] = (1024, 65535)
    NAME_LENGTH_RANGE: tuple[int, int] = (3, 100)

    # Security constants
    MIN_SECRET_KEY_LENGTH: int = 32
    DEFAULT_SECRET_KEY: str = "default-secret-key-32-characters-long-for-security"

    # Network configuration
    ALL_INTERFACES: str = "0.0.0.0"  # noqa: S104
    LOCALHOST_IP: str = "127.0.0.1"
    SYSTEM_PORT_THRESHOLD: int = 1023

    # Type definitions using advanced literals
    EnvironmentType = Literal["development", "staging", "production", "testing"]
    WebAppType = Literal[
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
    HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
    WebStatus = Literal[
        "stopped",
        "starting",
        "running",
        "stopping",
        "error",
        "maintenance",
        "deploying",
    ]

    # Consolidated security settings
    CORS_DEFAULT_ORIGINS: ClassVar[list[str]] = ["*"]
    CORS_SAFE_METHODS: ClassVar[list[str]] = ["GET", "HEAD", "OPTIONS"]
    CORS_SAFE_HEADERS: ClassVar[list[str]] = ["Content-Type", "Authorization"]
    SESSION_DEFAULTS: ClassVar[dict[str, str | bool]] = {
        "secure": False,
        "httponly": True,
        "samesite": "Lax",
    }
    SSL_PORTS: ClassVar[tuple[int, int]] = (443, 8443)

    # Consolidated validation limits
    CONTENT_LENGTH_RANGE: ClassVar[tuple[int, int]] = (0, 16 * 1024 * 1024)  # 0 to 16MB
    REQUEST_TIMEOUT_RANGE: ClassVar[tuple[int, int]] = (1, 600)  # 1s to 10min
    URL_LENGTH_RANGE: ClassVar[tuple[int, int]] = (1, 2048)
    HEADER_LIMITS: ClassVar[dict[str, int]] = {"max_length": 8192, "max_count": 100}

    # HTTP status codes using advanced consolidation
    class HttpStatus:
        """HTTP status codes with consolidated ranges."""

        # Consolidated status mappings
        STATUS_CODES: ClassVar[dict[str, int]] = {
            # 1xx Informational
            "CONTINUE": 100,
            "SWITCHING_PROTOCOLS": 101,
            "PROCESSING": 102,
            "EARLY_HINTS": 103,
            # 2xx Successful
            "OK": 200,
            "CREATED": 201,
            "ACCEPTED": 202,
            "NO_CONTENT": 204,
            "NOT_MODIFIED": 304,
            # 3xx Redirection
            "MOVED_PERMANENTLY": 301,
            "FOUND": 302,
            "SEE_OTHER": 303,
            "TEMPORARY_REDIRECT": 307,
            # 4xx Client Error
            "BAD_REQUEST": 400,
            "UNAUTHORIZED": 401,
            "FORBIDDEN": 403,
            "NOT_FOUND": 404,
            "METHOD_NOT_ALLOWED": 405,
            "CONFLICT": 409,
            "UNPROCESSABLE_ENTITY": 422,
            "TOO_MANY_REQUESTS": 429,
            # 5xx Server Error
            "INTERNAL_SERVER_ERROR": 500,
            "NOT_IMPLEMENTED": 501,
            "BAD_GATEWAY": 502,
            "SERVICE_UNAVAILABLE": 503,
            "GATEWAY_TIMEOUT": 504,
        }

        # Status ranges for classification
        RANGES: ClassVar[dict[str, tuple[int, int]]] = {
            "INFORMATIONAL": (100, 199),
            "SUCCESS": (200, 299),
            "REDIRECTION": (300, 399),
            "CLIENT_ERROR": (400, 499),
            "SERVER_ERROR": (500, 599),
        }

        @classmethod
        def get_status(cls, name: str) -> int:
            """Get status code by name."""
            return cls.STATUS_CODES.get(name.upper(), 500)

        @classmethod
        def is_success(cls, code: int) -> bool:
            """Check if status code indicates success."""
            return cls.RANGES["SUCCESS"][0] <= code <= cls.RANGES["SUCCESS"][1]

        @classmethod
        def is_error(cls, code: int) -> bool:
            """Check if status code indicates error."""
            return code >= cls.RANGES["CLIENT_ERROR"][0]


__all__ = ["FlextWebConstants"]
