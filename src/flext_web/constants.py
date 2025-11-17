"""FLEXT Web constants following the unified FLEXT pattern."""

from __future__ import annotations

from collections.abc import Mapping
from enum import IntEnum, StrEnum
from ipaddress import IPv4Address
from types import MappingProxyType
from typing import TYPE_CHECKING, ClassVar, Final, Literal

from flext_core import FlextConstants


class FlextWebConstants(FlextConstants):
    """Immutable project-specific constants organised by domain."""

    CONSTANTS_VERSION: Final[str] = "1.1.0"
    PROJECT_PREFIX: Final[str] = "FLEXT_WEB"
    PROJECT_NAME: Final[str] = "FLEXT Web"

    class WebDefaults:
        """Default bootstrap values for web services."""

        HOST: Final[str] = "localhost"
        PORT: Final[int] = 8080
        APP_NAME: Final[str] = "FLEXT Web"
        ENVIRONMENT: Final[str] = "development"
        DEBUG_MODE: Final[bool] = False
        SECRET_KEY: Final[str] = "default-secret-key-32-characters-long-for-security"
        DEV_SECRET_KEY: Final[str] = "dev-secret-key-32-characters-long-for-development"
        TEST_SECRET_KEY: Final[str] = "test-secret-key-32-characters-long-for-tests"
        TIMEOUT_SECONDS: Final[float] = 30.0
        HTTP_PROTOCOL: Final[str] = "http"
        HTTPS_PROTOCOL: Final[str] = "https"

    class WebResponse:
        """Web response status constants."""

        STATUS_SUCCESS: Final[str] = "success"
        STATUS_ERROR: Final[str] = "error"
        STATUS_OPERATIONAL: Final[str] = "operational"
        STATUS_HEALTHY: Final[str] = "healthy"

    class WebService:
        """Web service name constants."""

        SERVICE_NAME: Final[str] = "flext-web"
        SERVICE_NAME_FLASK: Final[str] = "flext-web-flask"
        SERVICE_NAME_API: Final[str] = "flext-web-api"
        SERVICE_NAME_HANDLERS: Final[str] = "flext-web-handlers"
        SERVICE_NAME_SERVICES: Final[str] = "flext-web-services"

    class WebServer:
        """Server boundaries and validation values."""

        MIN_PORT: Final[int] = 1024
        MAX_PORT: Final[int] = 65535
        MIN_APP_NAME_LENGTH: Final[int] = 3
        MAX_APP_NAME_LENGTH: Final[int] = 100
        MIN_SECRET_KEY_LENGTH: Final[int] = 32

    class WebSpecific:
        """Deployment specific identifiers and network defaults."""

        DEV_ENVIRONMENT_KEY: Final[str] = (
            "dev-environment-key-32-characters-long-for-dev"
        )
        TEST_ENVIRONMENT_KEY: Final[str] = (
            "test-environment-key-32-characters-long-for-tests"
        )
        ALL_INTERFACES: Final[str] = str(IPv4Address(0))
        LOCALHOST_IP: Final[str] = str(IPv4Address(0x7F000001))
        SYSTEM_PORTS_THRESHOLD: Final[int] = 1023
        PRIVILEGED_PORTS_MAX: Final[int] = 1023

    class WebValidation:
        """Validation constants for configuration and HTTP payloads."""

        PORT_RANGE: Final[tuple[int, int]] = (1, 65535)  # Allow system ports for SSL (443, 8443)
        NAME_LENGTH_RANGE: Final[tuple[int, int]] = (3, 100)
        MIN_SECRET_KEY_LENGTH: Final[int] = 32
        MAX_CONTENT_LENGTH_DEFAULT: Final[int] = 16 * 1024 * 1024
        MIN_CONTENT_LENGTH: Final[int] = 0
        REQUEST_TIMEOUT_DEFAULT: Final[int] = 30
        REQUEST_TIMEOUT_MAX: Final[int] = 600
        MAX_URL_LENGTH: Final[int] = 2048
        MIN_URL_LENGTH: Final[int] = 1
        MAX_HEADER_LENGTH: Final[int] = 8192
        MAX_HEADERS_COUNT: Final[int] = 100
        CONTENT_LENGTH_RANGE: Final[tuple[int, int]] = (
            MIN_CONTENT_LENGTH,
            MAX_CONTENT_LENGTH_DEFAULT,
        )
        REQUEST_TIMEOUT_RANGE: Final[tuple[int, int]] = (1, REQUEST_TIMEOUT_MAX)
        URL_LENGTH_RANGE: Final[tuple[int, int]] = (MIN_URL_LENGTH, MAX_URL_LENGTH)
        HEADER_LIMITS: ClassVar[Mapping[str, int]] = MappingProxyType({
            "max_length": MAX_HEADER_LENGTH,
            "max_count": MAX_HEADERS_COUNT,
        })

    class Http:
        """HTTP protocol constants, methods and status codes."""

        class Method(StrEnum):
            """Enumeration of supported HTTP methods."""

            GET = "GET"
            POST = "POST"
            PUT = "PUT"
            DELETE = "DELETE"
            PATCH = "PATCH"
            HEAD = "HEAD"
            OPTIONS = "OPTIONS"

        # HTTP Content Types
        CONTENT_TYPE_JSON: Final[str] = "application/json"
        CONTENT_TYPE_TEXT: Final[str] = "text/plain"
        CONTENT_TYPE_HTML: Final[str] = "text/html"

        # HTTP Header Names
        HEADER_CONTENT_TYPE: Final[str] = "content-type"
        HEADER_CONTENT_LENGTH: Final[str] = "content-length"

        METHODS: ClassVar[tuple[str, ...]] = tuple(method.value for method in Method)
        SAFE_METHODS: ClassVar[tuple[str, ...]] = (
            Method.GET.value,
            Method.HEAD.value,
            Method.OPTIONS.value,
        )
        DEFAULT_TIMEOUT_SECONDS: Final[float] = 30.0

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

        STATUS_CODES: ClassVar[Mapping[str, int]] = MappingProxyType({
            status.name: int(status.value) for status in StatusCode
        })
        STATUS_RANGES: ClassVar[Mapping[str, tuple[int, int]]] = MappingProxyType({
            "INFORMATIONAL": (100, 199),
            "SUCCESS": (200, 299),
            "REDIRECTION": (300, 399),
            "CLIENT_ERROR": (400, 499),
            "SERVER_ERROR": (500, 599),
        })
        SUCCESS_RANGE: Final[tuple[int, int]] = (200, 299)
        ERROR_MIN: Final[int] = 400

    class WebSecurity:
        """Security settings and safe defaults."""

        MIN_SECRET_KEY_LENGTH: Final[int] = 32
        RESERVED_NAMES: ClassVar[tuple[str, ...]] = (
            "REDACTED_LDAP_BIND_PASSWORD",
            "root",
            "api",
            "system",
            "config",
            "health",
        )
        DANGEROUS_PATTERNS: ClassVar[tuple[str, ...]] = (
            "<script",
            "javascript:",
            "data:text/html",
            "'; DROP TABLE",
            "--",
            "/*",
            "*/",
        )
        CORS_DEFAULT_ORIGINS: ClassVar[tuple[str, ...]] = ("*",)
        CORS_SAFE_METHODS: ClassVar[tuple[str, ...]] = ("GET", "HEAD", "OPTIONS")
        CORS_SAFE_HEADERS: ClassVar[tuple[str, ...]] = (
            "Content-Type",
            "Authorization",
        )
        SESSION_DEFAULTS: ClassVar[Mapping[str, str | bool]] = MappingProxyType({
            "secure": False,
            "httponly": True,
            "samesite": "Lax",
        })
        SSL_PORTS: Final[tuple[int, int]] = (443, 8443)
        SSL_ALT_PORT: Final[int] = 8443
        SESSION_COOKIE_SECURE_DEFAULT: Final[bool] = False
        SESSION_COOKIE_HTTPONLY_DEFAULT: Final[bool] = True
        SESSION_COOKIE_SAMESITE_DEFAULT: Final[str] = "Lax"

    class WebEnvironment:
        """Enumerations for environments, application types and status."""

        class Name(StrEnum):
            """Allowed deployment environments."""

            DEVELOPMENT = "development"
            STAGING = "staging"
            PRODUCTION = "production"
            TESTING = "testing"

        class ApplicationType(StrEnum):
            """Supported application classifications."""

            APPLICATION = "application"
            SERVICE = "service"
            API = "api"
            MICROSERVICE = "microservice"
            WEBAPP = "webapp"
            SPA = "spa"
            DASHBOARD = "dashboard"
            ADMIN_PANEL = "REDACTED_LDAP_BIND_PASSWORD-panel"

        class Status(StrEnum):
            """Lifecycle status values for web applications."""

            STOPPED = "stopped"
            STARTING = "starting"
            RUNNING = "running"
            STOPPING = "stopping"
            ERROR = "error"
            MAINTENANCE = "maintenance"
            DEPLOYING = "deploying"

        ENVIRONMENTS: ClassVar[tuple[str, ...]] = tuple(name.value for name in Name)
        APPLICATION_TYPES: ClassVar[tuple[str, ...]] = tuple(
            app.value for app in ApplicationType
        )
        STATUSES: ClassVar[tuple[str, ...]] = tuple(status.value for status in Status)

    PORT_RANGE: Final[tuple[int, int]] = WebValidation.PORT_RANGE
    NAME_LENGTH_RANGE: Final[tuple[int, int]] = WebValidation.NAME_LENGTH_RANGE
    MIN_SECRET_KEY_LENGTH: Final[int] = WebValidation.MIN_SECRET_KEY_LENGTH
    CONTENT_LENGTH_RANGE: Final[tuple[int, int]] = WebValidation.CONTENT_LENGTH_RANGE
    REQUEST_TIMEOUT_RANGE: Final[tuple[int, int]] = WebValidation.REQUEST_TIMEOUT_RANGE
    URL_LENGTH_RANGE: Final[tuple[int, int]] = WebValidation.URL_LENGTH_RANGE
    SSL_PORTS: Final[tuple[int, int]] = WebSecurity.SSL_PORTS
    SESSION_DEFAULTS: ClassVar[Mapping[str, str | bool]] = WebSecurity.SESSION_DEFAULTS
    EnvironmentType: ClassVar[tuple[str, ...]] = WebEnvironment.ENVIRONMENTS
    ApplicationType: ClassVar[tuple[str, ...]] = WebEnvironment.APPLICATION_TYPES
    HttpMethod: ClassVar[tuple[str, ...]] = Http.METHODS
    ApplicationStatus: ClassVar[tuple[str, ...]] = WebEnvironment.STATUSES

    # =========================================================================
    # TYPE LITERALS - Centralized type definitions for type checking
    # =========================================================================

    # HTTP Method Literal - must match Http.Method enum values
    if TYPE_CHECKING:
        HttpMethodLiteral = Literal[
            "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"
        ]
    else:
        # Runtime: validate against Http.Method enum
        HttpMethodLiteral = Literal[
            "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"
        ]

    # Environment Name Literal - must match WebEnvironment.Name enum values
    if TYPE_CHECKING:
        EnvironmentNameLiteral = Literal[
            "development", "staging", "production", "testing"
        ]
    else:
        EnvironmentNameLiteral = Literal[
            "development", "staging", "production", "testing"
        ]

    # Application Status Literal - must match WebEnvironment.Status enum values
    if TYPE_CHECKING:
        ApplicationStatusLiteral = Literal[
            "stopped",
            "starting",
            "running",
            "stopping",
            "error",
            "maintenance",
            "deploying",
        ]
    else:
        ApplicationStatusLiteral = Literal[
            "stopped",
            "starting",
            "running",
            "stopping",
            "error",
            "maintenance",
            "deploying",
        ]

    # Application Type Literal - must match WebEnvironment.ApplicationType enum values
    if TYPE_CHECKING:
        ApplicationTypeLiteral = Literal[
            "application",
            "service",
            "api",
            "microservice",
            "webapp",
            "spa",
            "dashboard",
            "REDACTED_LDAP_BIND_PASSWORD-panel",
        ]
    else:
        ApplicationTypeLiteral = Literal[
            "application",
            "service",
            "api",
            "microservice",
            "webapp",
            "spa",
            "dashboard",
            "REDACTED_LDAP_BIND_PASSWORD-panel",
        ]


__all__ = ["FlextWebConstants"]
