"""FLEXT Web constants following the unified FLEXT pattern."""

from __future__ import annotations

from collections.abc import Mapping
from enum import IntEnum, StrEnum
from ipaddress import IPv4Address
from types import MappingProxyType
from typing import ClassVar, Final

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

    class WebServer:
        """Server boundaries and validation values."""

        MIN_PORT: Final[int] = 1024
        MAX_PORT: Final[int] = 65535
        MIN_APP_NAME_LENGTH: Final[int] = 3
        MAX_APP_NAME_LENGTH: Final[int] = 100
        MIN_SECRET_KEY_LENGTH: Final[int] = 32

    class WebSpecific:
        """Deployment specific identifiers and network defaults."""

        DEV_SECRET_KEY: Final[str] = "dev-secret-key-32-characters-long-for-development"
        TEST_SECRET_KEY: Final[str] = "test-secret-key-32-characters-long-for-tests"
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

        PORT_RANGE: Final[tuple[int, int]] = (1024, 65535)
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
        METHODS: ClassVar[tuple[str, ...]] = (
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "PATCH",
            "HEAD",
            "OPTIONS",
        )
        EnvironmentType: ClassVar[tuple[str, ...]] = ENVIRONMENTS
        WebAppType: ClassVar[tuple[str, ...]] = APPLICATION_TYPES
        FlextWebMethod: ClassVar[tuple[str, ...]] = METHODS
        WebStatus: ClassVar[tuple[str, ...]] = STATUSES

    class Application:
        """Application level enumerations."""

        ENVIRONMENTS: ClassVar[tuple[str, ...]] = (
            "development",
            "staging",
            "production",
            "testing",
        )
        APPLICATION_TYPES: ClassVar[tuple[str, ...]] = (
            "application",
            "service",
            "api",
            "microservice",
            "webapp",
            "spa",
            "dashboard",
            "REDACTED_LDAP_BIND_PASSWORD-panel",
        )
        STATUSES: ClassVar[tuple[str, ...]] = (
            "stopped",
            "starting",
            "running",
            "stopping",
            "error",
            "maintenance",
            "deploying",
        )

    PORT_RANGE: Final[tuple[int, int]] = WebValidation.PORT_RANGE
    NAME_LENGTH_RANGE: Final[tuple[int, int]] = WebValidation.NAME_LENGTH_RANGE
    MIN_SECRET_KEY_LENGTH: Final[int] = WebValidation.MIN_SECRET_KEY_LENGTH
    CONTENT_LENGTH_RANGE: Final[tuple[int, int]] = WebValidation.CONTENT_LENGTH_RANGE
    REQUEST_TIMEOUT_RANGE: Final[tuple[int, int]] = WebValidation.REQUEST_TIMEOUT_RANGE
    URL_LENGTH_RANGE: Final[tuple[int, int]] = WebValidation.URL_LENGTH_RANGE
    SSL_PORTS: Final[tuple[int, int]] = WebSecurity.SSL_PORTS
    SESSION_DEFAULTS: ClassVar[Mapping[str, str | bool]] = WebSecurity.SESSION_DEFAULTS
    EnvironmentType: ClassVar[tuple[str, ...]] = Application.ENVIRONMENTS
    ApplicationType: ClassVar[tuple[str, ...]] = Application.APPLICATION_TYPES
    HttpMethod: ClassVar[tuple[str, ...]] = Http.METHODS
    ApplicationStatus: ClassVar[tuple[str, ...]] = Application.STATUSES


__all__ = ["FlextWebConstants"]
