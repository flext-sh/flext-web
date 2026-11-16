"""Scalar, enum, and domain constants for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
from enum import IntEnum, StrEnum, unique
from ipaddress import IPv4Address
from types import MappingProxyType
from typing import ClassVar

from flext_cli import c, t


class FlextWebConstantsValues:
    """Scalar, enum, and domain constants mixed into ``c.Web``."""

    SUCCESS_RANGE: ClassVar[tuple[int, int]] = (200, 299)
    ERROR_MIN: ClassVar[int] = 400
    ENVIRONMENTS: ClassVar[frozenset[str]] = frozenset({
        "development",
        "staging",
        "production",
        "testing",
    })

    SLUG_NON_WORD_RE: ClassVar[t.RegexPattern] = re.compile(r"[^\w\s-]+")
    SLUG_SPLIT_RE: ClassVar[t.RegexPattern] = re.compile(r"[-\s]+")

    @unique
    class Method(StrEnum):
        """Enumeration of supported HTTP methods."""

        GET = "GET"
        POST = "POST"
        PUT = "PUT"
        DELETE = "DELETE"
        PATCH = "PATCH"
        HEAD = "HEAD"
        OPTIONS = "OPTIONS"

    class StatusCode(IntEnum):
        """Enumeration of canonical HTTP status codes."""

        CONTINUE = 100
        PROCESSING = 102
        OK = 200
        CREATED = 201
        FOUND = 302
        BAD_REQUEST = 400
        FORBIDDEN = 403
        NOT_FOUND = 404
        CONFLICT = 409
        GATEWAY_TIMEOUT = 504

    @unique
    class ApplicationType(StrEnum):
        """Supported application classifications."""

        APPLICATION = c.ContextScope.APPLICATION
        SERVICE = "service"
        API = "api"
        DASHBOARD = "dashboard"

    @unique
    class ResponseStatus(StrEnum):
        """Canonical response status tokens for web service payloads."""

        SUCCESS = "success"
        ERROR = "error"
        OPERATIONAL = "operational"
        HEALTHY = "healthy"

    @unique
    class Name(StrEnum):
        """Allowed deployment environments."""

        DEVELOPMENT = "development"
        STAGING = "staging"
        PRODUCTION = "production"
        TESTING = "testing"

    @unique
    class Status(StrEnum):
        """Lifecycle status values for web applications."""

        STOPPED = "stopped"
        STARTING = "starting"
        RUNNING = "running"
        STOPPING = "stopping"
        ERROR = "error"
        MAINTENANCE = "maintenance"
        DEPLOYING = "deploying"

    STATUSES: ClassVar[frozenset[str]] = frozenset(
        member.value for member in Status.__members__.values()
    )

    DEFAULT_TIMEOUT_SECONDS: ClassVar[float] = float(c.DEFAULT_TIMEOUT_SECONDS)
    DEFAULT_HTTP_PROTOCOL: ClassVar[str] = "http"
    DEFAULT_HTTPS_PROTOCOL: ClassVar[str] = "https"

    SERVICE_NAME: ClassVar[str] = "flext-web"
    SERVICE_NAME_API: ClassVar[str] = "flext-web-api"

    ALL_INTERFACES: ClassVar[str] = str(IPv4Address(0))
    LOCALHOST_IP: ClassVar[str] = str(IPv4Address(2130706433))
    SYSTEM_PORTS_THRESHOLD: ClassVar[int] = 1023
    PRIVILEGED_PORTS_MAX: ClassVar[int] = 1023

    VALIDATION_PORT_RANGE: ClassVar[tuple[int, int]] = (1, 65535)
    VALIDATION_MAX_CONTENT_LENGTH_DEFAULT: ClassVar[int] = 16 * 1024 * 1024
    VALIDATION_MIN_CONTENT_LENGTH: ClassVar[int] = 0
    VALIDATION_REQUEST_TIMEOUT_DEFAULT: ClassVar[int] = c.DEFAULT_TIMEOUT_SECONDS
    VALIDATION_REQUEST_TIMEOUT_MAX: ClassVar[int] = 600
    VALIDATION_MAX_URL_LENGTH: ClassVar[int] = 2048
    VALIDATION_MIN_URL_LENGTH: ClassVar[int] = 1
    VALIDATION_MAX_HEADER_LENGTH: ClassVar[int] = 8192
    VALIDATION_MAX_HEADERS_COUNT: ClassVar[int] = 100
    VALIDATION_CONTENT_LENGTH_RANGE: ClassVar[tuple[int, int]] = (
        VALIDATION_MIN_CONTENT_LENGTH,
        VALIDATION_MAX_CONTENT_LENGTH_DEFAULT,
    )
    VALIDATION_REQUEST_TIMEOUT_RANGE: ClassVar[tuple[int, int]] = (
        1,
        VALIDATION_REQUEST_TIMEOUT_MAX,
    )
    VALIDATION_URL_LENGTH_RANGE: ClassVar[tuple[int, int]] = (
        VALIDATION_MIN_URL_LENGTH,
        VALIDATION_MAX_URL_LENGTH,
    )

    HTTP_CONTENT_TYPE_JSON: ClassVar[str] = "application/json"

    SECURITY_MIN_SECRET_KEY_LENGTH: ClassVar[int] = 32
    SECURITY_RESERVED_NAMES: ClassVar[frozenset[str]] = frozenset({
        "admin",
        "root",
        "api",
        "system",
        "settings",
        "health",
    })
    SECURITY_DANGEROUS_PATTERNS: ClassVar[frozenset[str]] = frozenset({
        "<script",
        "javascript:",
        "data:text/html",
        "'; DROP TABLE",
        "--",
        "/*",
        "*/",
    })
    SECURITY_CORS_DEFAULT_ORIGINS: ClassVar[frozenset[str]] = frozenset({"*"})
    SECURITY_CORS_SAFE_METHODS: ClassVar[frozenset[str]] = frozenset({
        Method.GET.value,
        Method.HEAD.value,
        Method.OPTIONS.value,
    })
    SECURITY_CORS_SAFE_HEADERS: ClassVar[frozenset[str]] = frozenset({
        "Content-Type",
        "Authorization",
    })
    SECURITY_SESSION_DEFAULTS: ClassVar[t.FeatureFlagMapping] = MappingProxyType({
        "secure": False,
        "httponly": True,
        "samesite": "Lax",
    })
    SECURITY_SSL_PORTS: ClassVar[tuple[int, int]] = (443, 8443)
    SECURITY_SSL_ALT_PORT: ClassVar[int] = 8443
    SECURITY_SESSION_COOKIE_SECURE_DEFAULT: ClassVar[bool] = False
    SECURITY_SESSION_COOKIE_HTTPONLY_DEFAULT: ClassVar[bool] = True
    SECURITY_SESSION_COOKIE_SAMESITE_DEFAULT: ClassVar[str] = "Lax"
    SECURITY_MAX_HOST_LENGTH: ClassVar[int] = 255

    FRAMEWORK_INTERFACE_ASGI: ClassVar[str] = "asgi"
    FRAMEWORK_INTERFACE_WSGI: ClassVar[str] = "wsgi"
    FRAMEWORK_RUNNER_UVICORN: ClassVar[str] = "uvicorn"
    FRAMEWORK_FASTAPI: ClassVar[str] = "fastapi"

    ACTION_CREATE: ClassVar[str] = "create"
    ACTION_START: ClassVar[str] = "start"
    ACTION_STOP: ClassVar[str] = "stop"
    ACTION_LIST: ClassVar[str] = c.Action.LIST

    MESSAGE_CONFIG_LOADED: ClassVar[str] = "loaded"
    MESSAGE_HANDLERS_REGISTERED: ClassVar[str] = "registered"


__all__: list[str] = ["FlextWebConstantsValues"]
