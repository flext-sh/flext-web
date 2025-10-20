"""FLEXT Web Constants - Web application constants following standardization plan.

**Standardization Compliance:**
- ✅ Layer 0 purity: Only constants, no functions or behavior
- ✅ Direct FlextConstants inheritance: Clean dependency chain
- ✅ Composition pattern: CoreErrors, CoreNetwork, etc. for easy access
- ✅ Nested namespace organization: Logical constant grouping
- ✅ HTTP protocol specialization: Status codes, methods, headers

**Domain Coverage:**
- Web server configuration, environment management
- HTTP protocol constants, security settings, CORS
- Application lifecycle, validation constraints
- Web-specific timeouts, limits, and defaults

**Architecture Layer**: Layer 0 (Pure Constants)
**Organization**: Nested namespaces for logical grouping and discoverability

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import ClassVar, Final, Literal

from flext_core import FlextConstants


class FlextWebConstants(FlextConstants):
    """Web application constants extending flext-core foundation patterns.

    Organizes all web-specific constants using nested namespaces for clarity,
    discoverability, and maintenance. All constants are immutable and used
    throughout web applications for configuration and validation.

    **Usage Examples:**

    1. Access default values:
        >>> from flext_web.constants import FlextWebConstants
        >>> host = FlextWebConstants.Defaults.HOST
        >>> port = FlextWebConstants.Defaults.PORT

    2. Access validation constraints:
        >>> port_range = FlextWebConstants.WebValidation.PORT_RANGE

    3. Access HTTP status codes:
        >>> ok_status = FlextWebConstants.Http.STATUS_OK

    4. Core composition access:
        >>> error = FlextWebConstants.CoreErrors.VALIDATION_ERROR
        >>> timeout = FlextWebConstants.CoreNetwork.DEFAULT_TIMEOUT
    """

    # =========================================================================
    # COMPOSITION REFERENCES (Standardization Pattern)
    # =========================================================================

    # Core composition - reference core constants for easy access
    CoreErrors = FlextConstants.Errors
    CoreNetwork = FlextConstants.Network
    CorePlatform = FlextConstants.Platform
    CoreSecurity = FlextConstants.Security
    CoreValidation = FlextConstants.Validation
    CoreWeb = FlextConstants.FlextWeb

    # =========================================================================
    # WEB DEFAULTS NAMESPACE - Web-specific default values
    # =========================================================================

    class WebDefaults:
        """Default values for web application configuration.

        Contains all immutable default values used for web server
        configuration initialization and fallback values.
        """

        HOST: Final[str] = "localhost"
        """Default host address for web server."""

        PORT: Final[int] = 8080
        """Default port number for web server."""

        APP_NAME: Final[str] = "FLEXT Web"
        """Default application name."""

        ENVIRONMENT: Final[str] = "development"
        """Default environment (development, staging, production, testing)."""

        DEBUG_MODE: Final[bool] = False
        """Default debug mode flag (disabled for security)."""

        SECRET_KEY: Final[str] = "default-secret-key-32-characters-long-for-security"
        """Default secret key (should be replaced in production)."""

        TEST_SECRET_KEY: Final[str] = "test-secret-key-32-characters-long-for-tests"
        """Secret key for test environment."""

        DEV_SECRET_KEY: Final[str] = "dev-secret-key-32-characters-long-for-development"
        """Secret key for development environment."""

        TIMEOUT: Final[float] = 30.0
        """Default request timeout in seconds."""

    # =========================================================================
    # WEB SERVER NAMESPACE - Server-specific configuration constants
    # =========================================================================

    class WebServer:
        """Server-specific configuration constants for web applications.

        Contains server configuration parameters and constraints for
        web server initialization and operation.
        """

        MIN_PORT: Final[int] = 1024
        """Minimum valid port number (above system ports)."""

        MAX_PORT: Final[int] = 65535
        """Maximum valid port number."""

        MIN_APP_NAME_LENGTH: Final[int] = 3
        """Minimum application name length."""

        MAX_APP_NAME_LENGTH: Final[int] = 100
        """Maximum application name length."""

        MIN_SECRET_KEY_LENGTH: Final[int] = 32
        """Minimum secret key length for security."""

    # =========================================================================
    # WEB SPECIFIC NAMESPACE - Web-specific implementation constants
    # =========================================================================

    class WebSpecific:
        """Web-specific implementation constants and keys.

        Contains web-specific configuration keys, IP addresses,
        and system-specific constants for web applications.
        """

        DEV_SECRET_KEY: Final[str] = "dev-secret-key-32-characters-long-for-development"
        """Development environment secret key."""

        DEV_ENVIRONMENT_KEY: Final[str] = (
            "dev-environment-key-32-characters-long-for-dev"
        )
        """Development environment configuration key."""

        TEST_ENVIRONMENT_KEY: Final[str] = (
            "test-environment-key-32-characters-long-for-tests"
        )
        """Test environment configuration key."""

        ALL_INTERFACES: Final[str] = "0.0.0.0"  # noqa: S104
        """Listen on all network interfaces."""

        LOCALHOST_IP: Final[str] = "127.0.0.1"
        """Localhost IP address."""

        SYSTEM_PORTS_THRESHOLD: Final[int] = 1023
        """System port threshold (0-1023 are system ports)."""

        PRIVILEGED_PORTS_MAX: Final[int] = 1023
        """Maximum privileged port number."""

    # =========================================================================
    # WEB ENVIRONMENT NAMESPACE - Environment and application type definitions
    # =========================================================================

    class WebEnvironment:
        """Environment and application type definitions for web services.

        Contains type literals and enums for environment configuration,
        application types, and web service classification.
        """

        EnvironmentType: Final = Literal[
            "development", "staging", "production", "testing"
        ]
        """Valid environment type literal."""

        WebAppType: Final = Literal[
            "application",
            "service",
            "api",
            "microservice",
            "webapp",
            "spa",
            "dashboard",
            "REDACTED_LDAP_BIND_PASSWORD-panel",
        ]
        """Valid web application type literal."""

        FlextWebMethod: Final = Literal[
            "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"
        ]
        """Valid HTTP method literal for web operations."""

        WebStatus: Final = Literal[
            "stopped",
            "starting",
            "running",
            "stopping",
            "error",
            "maintenance",
            "deploying",
        ]
        """Valid web application status literal."""

    # =========================================================================
    # WEB SECURITY NAMESPACE - Security-related constants
    # =========================================================================

    # =========================================================================
    # WEB VALIDATION NAMESPACE - Web-specific constraint definitions
    # =========================================================================

    class WebValidation:
        """Web-specific validation constants for web applications.

        Contains validation constraints specific to web requests,
        responses, and web application configuration.
        """

        PORT_RANGE: Final[tuple[int, int]] = (1024, 65535)
        """Valid port number range (1024-65535)."""

        NAME_LENGTH_RANGE: Final[tuple[int, int]] = (3, 100)
        """Valid application name length range (3-100)."""

        MIN_SECRET_KEY_LENGTH: Final[int] = 32
        """Minimum secret key length for security."""

        MAX_CONTENT_LENGTH_DEFAULT: Final[int] = 16 * 1024 * 1024
        """Default maximum content length (16MB)."""

        MIN_CONTENT_LENGTH: Final[int] = 0
        """Minimum content length."""

        REQUEST_TIMEOUT_DEFAULT: Final[int] = 30
        """Default request timeout in seconds."""

        REQUEST_TIMEOUT_MAX: Final[int] = 600
        """Maximum request timeout in seconds (10 minutes)."""

        MAX_URL_LENGTH: Final[int] = 2048
        """Maximum URL length."""

        MIN_URL_LENGTH: Final[int] = 1
        """Minimum URL length."""

        MAX_HEADER_LENGTH: Final[int] = 8192
        """Maximum HTTP header length."""

        MAX_HEADERS_COUNT: Final[int] = 100
        """Maximum number of HTTP headers."""

        # Additional validation constants for backward compatibility
        CONTENT_LENGTH_RANGE: Final[tuple[int, int]] = (0, 16 * 1024 * 1024)
        """Valid content length range (0 to 16MB)."""

        REQUEST_TIMEOUT_RANGE: Final[tuple[int, int]] = (1, 600)
        """Valid request timeout range in seconds (1s to 10min)."""

        URL_LENGTH_RANGE: Final[tuple[int, int]] = (1, 2048)
        """Valid URL length range."""

        HEADER_LIMITS: ClassVar[dict[str, int]] = {
            "max_length": 8192,
            "max_count": 100,
        }
        """HTTP header size and count limits."""

    # =========================================================================
    # HTTP NAMESPACE - HTTP protocol constants
    # =========================================================================

    class Http:
        """HTTP protocol constants including methods, headers, and status codes."""

        METHOD: Final = Literal[
            "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"
        ]
        """Valid HTTP method literal type."""

        METHODS: ClassVar[list[str]] = [
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "PATCH",
            "HEAD",
            "OPTIONS",
        ]
        """List of supported HTTP methods."""

        SAFE_METHODS: ClassVar[list[str]] = ["GET", "HEAD", "OPTIONS"]
        """Safe HTTP methods that don't modify server state."""

        DEFAULT_TIMEOUT: Final[float] = 30.0
        """Default HTTP request timeout in seconds."""

        class HttpStatus:
            """HTTP status code constants and classification.

            Provides comprehensive HTTP status code mapping and helper methods
            for status classification following RFC 7231.
            """

            # Status code mappings
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
            """HTTP status codes mapping (name -> code)."""

            # Status ranges for classification
            RANGES: ClassVar[dict[str, tuple[int, int]]] = {
                "INFORMATIONAL": (100, 199),
                "SUCCESS": (200, 299),
                "REDIRECTION": (300, 399),
                "CLIENT_ERROR": (400, 499),
                "SERVER_ERROR": (500, 599),
            }
            """HTTP status code ranges for classification."""

            SUCCESS_MIN: Final[int] = 200
            """Minimum success status code."""

            SUCCESS_MAX: Final[int] = 299
            """Maximum success status code."""

            ERROR_MIN: Final[int] = 400
            """Minimum error status code."""

            @classmethod
            def get_status(cls, name: str) -> int:
                """Get HTTP status code by name.

                Args:
                    name: Status code name (e.g., 'OK', 'NOT_FOUND')

                Returns:
                    HTTP status code or 500 if not found

                """
                return cls.STATUS_CODES.get(name.upper(), 500)

            @classmethod
            def is_success(cls, code: int) -> bool:
                """Check if HTTP status code indicates success.

                Args:
                    code: HTTP status code

                Returns:
                    True if code is in 2xx range (200-299)

                """
                return cls.RANGES["SUCCESS"][0] <= code <= cls.RANGES["SUCCESS"][1]

            @classmethod
            def is_error(cls, code: int) -> bool:
                """Check if HTTP status code indicates error.

                Args:
                    code: HTTP status code

                Returns:
                    True if code is >= 400 (4xx or 5xx)

                """
                return code >= cls.RANGES["CLIENT_ERROR"][0]

    # =========================================================================
    # SECURITY NAMESPACE - Security-related constants
    # =========================================================================

    class WebSecurity:
        """Security-related constants for web applications.

        Includes CORS settings, SSL configuration, and session defaults.
        """

        MIN_SECRET_KEY_LENGTH: Final[int] = 32
        """Minimum secret key length for security."""

        CORS_DEFAULT_ORIGINS: ClassVar[list[str]] = ["*"]
        """Default CORS allowed origins."""

        CORS_SAFE_METHODS: ClassVar[list[str]] = ["GET", "HEAD", "OPTIONS"]
        """Safe HTTP methods for CORS."""

        CORS_SAFE_HEADERS: ClassVar[list[str]] = ["Content-Type", "Authorization"]
        """Safe HTTP headers for CORS."""

        SESSION_DEFAULTS: ClassVar[dict[str, str | bool]] = {
            "secure": False,
            "httponly": True,
            "samesite": "Lax",
        }
        """Default session cookie configuration."""

        SSL_PORTS: ClassVar[tuple[int, int]] = (443, 8443)
        """Standard HTTPS ports."""

        # Session cookie defaults
        SESSION_COOKIE_SECURE_DEFAULT: Final[bool] = False
        """Default session cookie secure flag."""

        SESSION_COOKIE_HTTPONLY_DEFAULT: Final[bool] = True
        """Default session cookie httponly flag."""

        SESSION_COOKIE_SAMESITE_DEFAULT: Final[str] = "Lax"
        """Default session cookie samesite policy."""

        SSL_ALT_PORT: Final[int] = 8443
        """Alternative SSL port for HTTPS."""

        LOCALHOST_IP: Final[str] = "127.0.0.1"
        """Localhost IP address."""

        SYSTEM_PORT_THRESHOLD: Final[int] = 1023
        """System port threshold (0-1023 are system ports)."""

    # =========================================================================
    # APPLICATION NAMESPACE - Application domain constants
    # =========================================================================

    class Application:
        """Application domain constants for web services.

        Includes environment types, application types, status literals.
        """

        ENVIRONMENT_TYPE: Final = Literal[
            "development", "staging", "production", "testing"
        ]
        """Valid environment type literal."""

        APPLICATION_TYPE: Final = Literal[
            "application",
            "service",
            "api",
            "microservice",
            "webapp",
            "spa",
            "dashboard",
            "REDACTED_LDAP_BIND_PASSWORD-panel",
        ]
        """Valid application type literal."""

        STATUS: Final = Literal[
            "stopped",
            "starting",
            "running",
            "stopping",
            "error",
            "maintenance",
            "deploying",
        ]
        """Valid application status literal."""

        STATUSES: ClassVar[list[str]] = [
            "stopped",
            "starting",
            "running",
            "stopping",
            "error",
            "maintenance",
            "deploying",
        ]
        """List of valid application statuses."""

        ENVIRONMENTS: ClassVar[list[str]] = [
            "development",
            "staging",
            "production",
            "testing",
        ]
        """List of valid environments."""

    # =========================================================================
    # TOP-LEVEL CONSTANTS - Direct access constants for backward compatibility
    # =========================================================================

    # Web-specific defaults (for backward compatibility)
    Defaults: type = WebDefaults
    """Alias for WebDefaults for backward compatibility."""

    # Web-specific validation (for backward compatibility - use CoreValidation)
    # Note: Use CoreValidation for parent class validation constants

    # Web-specific security (for backward compatibility - use CoreSecurity)
    # Note: Use CoreSecurity for parent class security constants

    # Port and name validation ranges
    PORT_RANGE: Final[tuple[int, int]] = WebValidation.PORT_RANGE
    """Valid port number range (1024-65535)."""

    NAME_LENGTH_RANGE: Final[tuple[int, int]] = WebValidation.NAME_LENGTH_RANGE
    """Valid application name length range (3-100)."""

    MIN_SECRET_KEY_LENGTH: Final[int] = WebValidation.MIN_SECRET_KEY_LENGTH
    """Minimum secret key length (32)."""

    # Environment and application types (aliases for backward compatibility)
    EnvironmentType: Final = WebEnvironment.EnvironmentType
    """Valid environment type literal."""

    ApplicationType: Final = WebEnvironment.WebAppType
    """Valid application type literal."""

    HttpMethod: Final = WebEnvironment.FlextWebMethod
    """Valid HTTP method literal."""

    ApplicationStatus: Final = WebEnvironment.WebStatus
    """Valid application status literal."""

    # Security constants (aliases for backward compatibility)
    SSL_PORTS: Final[tuple[int, int]] = WebSecurity.SSL_PORTS
    """Standard HTTPS ports."""

    SESSION_DEFAULTS: ClassVar[dict[str, str | bool]] = WebSecurity.SESSION_DEFAULTS
    """Default session cookie configuration."""

    # Validation constants (aliases for backward compatibility)
    CONTENT_LENGTH_RANGE: Final[tuple[int, int]] = WebValidation.CONTENT_LENGTH_RANGE
    """Valid content length range."""

    REQUEST_TIMEOUT_RANGE: Final[tuple[int, int]] = WebValidation.REQUEST_TIMEOUT_RANGE
    """Valid request timeout range."""

    URL_LENGTH_RANGE: Final[tuple[int, int]] = WebValidation.URL_LENGTH_RANGE
    """Valid URL length range."""


__all__ = ["FlextWebConstants"]
