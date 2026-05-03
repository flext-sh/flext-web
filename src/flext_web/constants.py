"""FLEXT Web constants."""

from __future__ import annotations

from collections.abc import (
    Mapping,
)
from enum import IntEnum, StrEnum, unique
from ipaddress import IPv4Address
from types import MappingProxyType
from typing import Final

from flext_cli import c, t


class FlextWebConstants(c):
    """Immutable project-specific constants organized by domain."""

    class Web:
        """Web domain constants namespace.

        All web-specific constants are organized here for better namespace
        organization and to enable composition with other domain constants.
        """

        # ===== Enums (keep these) =====
        @unique
        class Method(StrEnum):
            """Enumeration of supported HTTP methods.

            DRY Pattern:
                StrEnum is the single source of truth. Use Method.GET.value
                or Method.GET directly - no base strings needed.
            """

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
            SWITCHING_PROTOCOLS = 101
            PROCESSING = 102
            EARLY_HINTS = 103
            OK = 200
            CREATED = 201
            ACCEPTED = 202
            NO_CONTENT = 204
            NOT_MODIFIED = 304
            MOVED_PERMANENTLY = 301
            FOUND = 302
            SEE_OTHER = 303
            TEMPORARY_REDIRECT = 307
            BAD_REQUEST = 400
            UNAUTHORIZED = 401
            FORBIDDEN = 403
            NOT_FOUND = 404
            METHOD_NOT_ALLOWED = 405
            CONFLICT = 409
            UNPROCESSABLE_ENTITY = 422
            TOO_MANY_REQUESTS = 429
            INTERNAL_SERVER_ERROR = 500
            NOT_IMPLEMENTED = 501
            BAD_GATEWAY = 502
            SERVICE_UNAVAILABLE = 503
            GATEWAY_TIMEOUT = 504

        @unique
        class Name(StrEnum):
            """Allowed deployment environments.

            DRY Pattern:
                StrEnum is the single source of truth. Use Name.DEVELOPMENT.value
                or Name.DEVELOPMENT directly - no base strings needed.
            """

            DEVELOPMENT = "development"
            STAGING = "staging"
            PRODUCTION = "production"
            TESTING = "testing"

        @unique
        class ApplicationType(StrEnum):
            """Supported application classifications.

            DRY Pattern:
                StrEnum is the single source of truth. Use ApplicationType.APPLICATION.value
                or ApplicationType.APPLICATION directly - no base strings needed.
            """

            APPLICATION = "application"
            SERVICE = "service"
            API = "api"
            MICROSERVICE = "microservice"
            WEBAPP = "webapp"
            SPA = "spa"
            DASHBOARD = "dashboard"
            ADMIN_PANEL = "admin-panel"

        @unique
        class Status(StrEnum):
            """Lifecycle status values for web applications.

            DRY Pattern:
                StrEnum is the single source of truth. Use Status.STOPPED.value
                or Status.STOPPED directly - no base strings needed.
            """

            STOPPED = "stopped"
            STARTING = "starting"
            RUNNING = "running"
            STOPPING = "stopping"
            ERROR = "error"
            MAINTENANCE = "maintenance"
            DEPLOYING = "deploying"

        @unique
        class ResponseStatus(StrEnum):
            """Canonical response status tokens for web service payloads."""

            SUCCESS = "success"
            ERROR = "error"
            OPERATIONAL = "operational"
            HEALTHY = "healthy"

        # ===== Status/Code mappings =====
        STATUS_CODES: Final[t.IntMapping] = MappingProxyType({
            status.name: status.value for status in StatusCode
        })
        STATUS_RANGES: Final[Mapping[str, tuple[int, int]]] = MappingProxyType({
            "INFORMATIONAL": (100, 199),
            "SUCCESS": (200, 299),
            "REDIRECTION": (300, 399),
            "CLIENT_ERROR": (400, 499),
            "SERVER_ERROR": (500, 599),
        })
        SUCCESS_RANGE: Final[tuple[int, int]] = (200, 299)
        ERROR_MIN: Final[int] = 400

        # ===== Enum-derived frozensets (not tuples) =====
        ENVIRONMENTS: Final[frozenset[str]] = frozenset(
            member.value for member in Name.__members__.values()
        )
        APPLICATION_TYPES: Final[frozenset[str]] = frozenset(
            member.value for member in ApplicationType.__members__.values()
        )
        STATUSES: Final[frozenset[str]] = frozenset(
            member.value for member in Status.__members__.values()
        )

        # ===== Flattened from WebDefaults =====
        DEFAULT_HOST: Final[str] = c.LOCALHOST
        DEFAULT_PORT: Final[int] = 8080
        DEFAULT_APP_NAME: Final[str] = "FLEXT Web"
        DEFAULT_ENVIRONMENT: Final[str] = Name.DEVELOPMENT.value
        DEFAULT_DEBUG_MODE: Final[bool] = False
        DEFAULT_VERSION_STRING: Final[str] = "1.0.0"
        DEFAULT_VERSION_INT: Final[int] = 1
        DEFAULT_SECRET_KEY: Final[str] = (
            "default-secret-key-32-characters-long-for-security"
        )
        DEFAULT_TEST_SECRET_KEY: Final[str] = (
            "test-secret-key-32-characters-long-for-tests"
        )
        DEFAULT_TIMEOUT_SECONDS: Final[float] = float(c.DEFAULT_TIMEOUT_SECONDS)
        DEFAULT_HTTP_PROTOCOL: Final[str] = "http"
        DEFAULT_HTTPS_PROTOCOL: Final[str] = "https"

        # ===== Flattened from WebService =====
        SERVICE_NAME: Final[str] = "flext-web"
        SERVICE_NAME_FLASK: Final[str] = "flext-web-flask"
        SERVICE_NAME_API: Final[str] = "flext-web-api"

        # ===== Flattened from WebSpecific =====
        ALL_INTERFACES: Final[str] = str(IPv4Address(0))
        LOCALHOST_IP: Final[str] = str(IPv4Address(2130706433))
        SYSTEM_PORTS_THRESHOLD: Final[int] = 1023
        PRIVILEGED_PORTS_MAX: Final[int] = 1023

        # ===== Flattened from WebValidation =====
        VALIDATION_PORT_RANGE: Final[tuple[int, int]] = (1, 65535)
        VALIDATION_NAME_LENGTH_RANGE: Final[tuple[int, int]] = (3, 100)
        VALIDATION_MAX_CONTENT_LENGTH_DEFAULT: Final[int] = 16 * 1024 * 1024
        VALIDATION_MIN_CONTENT_LENGTH: Final[int] = 0
        VALIDATION_REQUEST_TIMEOUT_DEFAULT: Final[int] = c.DEFAULT_TIMEOUT_SECONDS
        VALIDATION_REQUEST_TIMEOUT_MAX: Final[int] = 600
        VALIDATION_MAX_URL_LENGTH: Final[int] = 2048
        VALIDATION_MIN_URL_LENGTH: Final[int] = 1
        VALIDATION_MAX_HEADER_LENGTH: Final[int] = 8192
        VALIDATION_MAX_HEADERS_COUNT: Final[int] = 100
        VALIDATION_CONTENT_LENGTH_RANGE: Final[tuple[int, int]] = (
            VALIDATION_MIN_CONTENT_LENGTH,
            VALIDATION_MAX_CONTENT_LENGTH_DEFAULT,
        )
        VALIDATION_REQUEST_TIMEOUT_RANGE: Final[tuple[int, int]] = (
            1,
            VALIDATION_REQUEST_TIMEOUT_MAX,
        )
        VALIDATION_URL_LENGTH_RANGE: Final[tuple[int, int]] = (
            VALIDATION_MIN_URL_LENGTH,
            VALIDATION_MAX_URL_LENGTH,
        )
        VALIDATION_HEADER_LIMITS: Final[t.IntMapping] = MappingProxyType({
            "max_length": VALIDATION_MAX_HEADER_LENGTH,
            "max_count": VALIDATION_MAX_HEADERS_COUNT,
        })

        # ===== Flattened from Http =====
        HTTP_CONTENT_TYPE_JSON: Final[str] = "application/json"
        HTTP_CONTENT_TYPE_TEXT: Final[str] = "text/plain"
        HTTP_CONTENT_TYPE_HTML: Final[str] = "text/html"
        HTTP_HEADER_CONTENT_TYPE: Final[str] = "content-type"
        HTTP_HEADER_CONTENT_LENGTH: Final[str] = "content-length"
        HTTP_METHODS: Final[frozenset[str]] = frozenset(
            member.value for member in Method.__members__.values()
        )

        # ===== Flattened from WebSecurity =====
        SECURITY_MIN_SECRET_KEY_LENGTH: Final[int] = 32
        SECURITY_RESERVED_NAMES: Final[frozenset[str]] = frozenset({
            "admin",
            "root",
            "api",
            "system",
            "settings",
            "health",
        })
        SECURITY_DANGEROUS_PATTERNS: Final[frozenset[str]] = frozenset({
            "<script",
            "javascript:",
            "data:text/html",
            "'; DROP TABLE",
            "--",
            "/*",
            "*/",
        })
        SECURITY_CORS_DEFAULT_ORIGINS: Final[frozenset[str]] = frozenset({"*"})
        SECURITY_CORS_SAFE_METHODS: Final[frozenset[str]] = frozenset({
            Method.GET.value,
            Method.HEAD.value,
            Method.OPTIONS.value,
        })
        SECURITY_CORS_SAFE_HEADERS: Final[frozenset[str]] = frozenset({
            "Content-Type",
            "Authorization",
        })
        SECURITY_SESSION_DEFAULTS: Final[t.FeatureFlagMapping] = MappingProxyType({
            "secure": False,
            "httponly": True,
            "samesite": "Lax",
        })
        SECURITY_SSL_PORTS: Final[tuple[int, int]] = (443, 8443)
        SECURITY_SSL_ALT_PORT: Final[int] = 8443
        SECURITY_SESSION_COOKIE_SECURE_DEFAULT: Final[bool] = False
        SECURITY_SESSION_COOKIE_HTTPONLY_DEFAULT: Final[bool] = True
        SECURITY_SESSION_COOKIE_SAMESITE_DEFAULT: Final[str] = "Lax"
        SECURITY_MAX_DESCRIPTION_LENGTH: Final[int] = 500
        SECURITY_MAX_HOST_LENGTH: Final[int] = 255

        # ===== Flattened from WebFramework =====
        FRAMEWORK_INTERFACE_ASGI: Final[str] = "asgi"
        FRAMEWORK_INTERFACE_WSGI: Final[str] = "wsgi"
        FRAMEWORK_RUNNER_UVICORN: Final[str] = "uvicorn"
        FRAMEWORK_RUNNER_WERKZEUG: Final[str] = "werkzeug"
        FRAMEWORK_FASTAPI: Final[str] = "fastapi"
        FRAMEWORK_FLASK: Final[str] = "flask"
        FRAMEWORK_INTERFACES: Final[frozenset[str]] = frozenset({
            FRAMEWORK_INTERFACE_ASGI,
            FRAMEWORK_INTERFACE_WSGI,
        })
        FRAMEWORK_RUNNERS: Final[frozenset[str]] = frozenset({
            FRAMEWORK_RUNNER_UVICORN,
            FRAMEWORK_RUNNER_WERKZEUG,
        })
        FRAMEWORK_FRAMEWORKS: Final[frozenset[str]] = frozenset({
            FRAMEWORK_FASTAPI,
            FRAMEWORK_FLASK,
        })

        # ===== Flattened from WebActions =====
        ACTION_CREATE: Final[str] = "create"
        ACTION_START: Final[str] = "start"
        ACTION_STOP: Final[str] = "stop"
        ACTION_LIST: Final[str] = "list"
        ACTIONS: Final[frozenset[str]] = frozenset({
            ACTION_CREATE,
            ACTION_START,
            ACTION_STOP,
            ACTION_LIST,
        })

        # ===== Flattened from WebMessages =====
        MESSAGE_ENTITY_SERVICE_READY: Final[str] = "Entity service ready"
        MESSAGE_CONFIG_LOADED: Final[str] = "loaded"
        MESSAGE_HANDLERS_REGISTERED: Final[str] = "registered"

        # ===== Flattened from WebApi =====
        API_DOCS_URL: Final[str] = "/docs"
        API_REDOC_URL: Final[str] = "/redoc"
        API_OPENAPI_URL: Final[str] = "/openapi.json"
        API_DEFAULT_DESCRIPTION: Final[str] = "Generic HTTP Service"


c = FlextWebConstants

__all__: tuple[str, ...] = ("FlextWebConstants", "c")
