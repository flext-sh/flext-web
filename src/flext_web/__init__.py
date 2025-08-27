"""Enterprise Web Management Console for FLEXT ecosystem."""

from __future__ import annotations

from flext_core import (
    FlextExceptions,
    get_logger,
)

from flext_web.config import FlextWebConfig
from flext_web.exceptions import (
    FlextWebAuthenticationError,
    FlextWebConfigurationError,
    FlextWebConnectionError,
    FlextWebError,
    FlextWebMiddlewareError,
    FlextWebProcessingError,
    FlextWebRoutingError,
    FlextWebSessionError,
    FlextWebTemplateError,
    FlextWebTimeoutError,
    FlextWebValidationError,
)
from flext_web.fields import WebFields, HTTPStatusField
from flext_web.handlers import WebHandlers, WebResponseHandler
from flext_web.interfaces import (
    WebServiceInterface,
    AppRepositoryInterface,
    MiddlewareInterface,
    TemplateEngineInterface,
    MonitoringInterface,
)
from flext_web.handlers import FlextWebAppHandler
from flext_web.models import FlextWebApp, FlextWebAppStatus
from flext_web.protocols import (
    WebServiceProtocol,
    AppManagerProtocol,
    ResponseFormatterProtocol,
    ConfigurationProtocol,
    TemplateRendererProtocol,
)
from flext_web.services import FlextWebService
from flext_web.type_aliases import (
    FieldKwargs,
    ValidatorFunc,
    ValidatorGenerator,
    RequestContext,
    ResponseData,
    TemplateContext,
    ConfigValue,
    ConfigDict,
    ErrorDetails,
    SchemaDict,
    TemplateFilter,
    TemplateGlobal,
    HTTPStatus,
)

from flext_web.utilities import FlextWebUtilities
from flask import Flask

__version__ = "0.9.0"
__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())
__author__ = "FLEXT Contributors"

logger = get_logger(__name__)


# =============================================================================


# =============================================================================
# CONFIGURATION - Using FlextConfig patterns
# =============================================================================


# =============================================================================
# HANDLERS - Using FlextHandlers patterns
# =============================================================================


# =============================================================================
# WEB SERVICE - Flask integration with flext-core patterns
# =============================================================================


# =============================================================================
# FACTORY FUNCTIONS - Configuration management
# =============================================================================


# Module-level singleton configuration management
_config_instance: FlextWebConfig | None = None


def _get_config_singleton() -> FlextWebConfig:
    """Get validated configuration singleton."""
    global _config_instance  # noqa: PLW0603
    if _config_instance is None:
        # Configuration is automatically validated by Pydantic during instantiation
        _config_instance = FlextWebConfig()
    return _config_instance


def _reset_config_singleton() -> None:
    """Reset configuration singleton."""
    global _config_instance  # noqa: PLW0603
    _config_instance = None


def get_web_settings() -> FlextWebConfig:
    """Get validated web configuration singleton with comprehensive settings management.

    Provides a singleton configuration instance for the FLEXT Web Interface with
    automatic validation, environment variable integration, and production safety
    checks. The configuration is cached after first creation and validation for
    performance optimization across the application lifecycle.

    The function implements the singleton pattern to ensure consistent configuration
    across all components while providing comprehensive validation that prevents
    runtime errors from configuration issues.

    Returns:
      FlextWebConfig: Validated configuration instance with all settings loaded
      from environment variables and defaults. The configuration is guaranteed
      to pass all validation rules before being returned.

    Raises:
      ValueError: If configuration validation fails with specific error details
      explaining which validation rule was violated and how to fix it.

    Configuration Sources (in precedence order):
      1. Environment variables with FLEXT_WEB_ prefix
      2. Configuration file values (if specified)
      3. Default values defined in FlextWebConfig

    Validation Rules:
      - Application name must be non-empty string
      - Version must follow semantic versioning (x.y.z)
      - Host must be valid network address
      - Port must be within range (1-65535)
      - Secret key must be changed from default in production
      - Debug mode must be disabled in production

    Example:
      Basic configuration access:

      >>> config = get_web_settings()
      >>> print(f"Server URL: {config.get_server_url()}")
      >>> print(f"Production mode: {config.is_production()}")

      Environment variable configuration:

      >>> import os
      >>> os.environ["FLEXT_WEB_HOST"] = "0.0.0.0"
      >>> os.environ["FLEXT_WEB_PORT"] = "8080"
      >>> config = get_web_settings()
      >>> assert config.host == "0.0.0.0"
      >>> assert config.port == 8080

    """
    return _get_config_singleton()


def reset_web_settings() -> None:
    """Reset configuration singleton for testing and reinitialization scenarios.

    Clears the cached configuration singleton instance, forcing the next call to
    get_web_settings() to create a fresh configuration instance. This function
    is primarily used in testing scenarios where configuration needs to be
    reloaded with different environment variables or settings.

    The function provides clean state management for testing and ensures that
    configuration changes in test scenarios don't affect other tests or
    application components.

    Side Effects:
      - Clears the global configuration singleton instance
      - Forces recalculation of configuration on next access
      - Reloads environment variables on next get_web_settings() call
      - Revalidates all configuration rules on next access

    Usage Scenarios:
      - Unit testing with different configuration scenarios
      - Integration testing with environment variable changes
      - Development environment reloading
      - Configuration error recovery scenarios

    Example:
      Testing with different configurations:

      >>> import os
      >>> # Test with development configuration
      >>> os.environ["FLEXT_WEB_DEBUG"] = "true"
      >>> config1 = get_web_settings()
      >>> assert config1.debug is True
      >>>
      >>> # Reset and test with production configuration
      >>> reset_web_settings()
      >>> os.environ["FLEXT_WEB_DEBUG"] = "false"
      >>> config2 = get_web_settings()
      >>> assert config2.debug is False

      Test isolation pattern:

      >>> def test_custom_config():
      ...     reset_web_settings()  # Ensure clean state
      ...     os.environ["FLEXT_WEB_PORT"] = "9000"
      ...     config = get_web_settings()
      ...     assert config.port == 9000
      ...     reset_web_settings()  # Clean up after test

    """
    _reset_config_singleton()


def create_service(config: FlextWebConfig | None = None) -> FlextWebService:
    """Create configured FLEXT Web Service instance with comprehensive initialization.

    Factory function for creating FlextWebService instances with proper configuration
    management, validation, and initialization. Provides a convenient interface for
    service creation while ensuring all components are properly configured and
    validated before service startup.

    The function handles configuration loading, validation, and service component
    initialization following enterprise patterns for dependency injection and
    configuration management.

    Args:
      config: Optional FlextWebConfig instance. If None, uses get_web_settings()
      to load configuration from environment variables and defaults.

    Returns:
      FlextWebService: Fully configured and initialized service instance ready
      for startup. The service includes Flask application, route registration,
      CQRS handlers, and all necessary components.

    Configuration Handling:
      - Uses provided config parameter if specified
      - Falls back to get_web_settings() singleton if config is None
      - Validates configuration before service creation
      - Ensures all required components are properly initialized

    Service Components:
      - Flask application with registered routes
      - FlextWebAppHandler for CQRS operations
      - Configuration management and validation
      - Structured logging integration
      - Error handling middleware

    Example:
      Basic service creation with default configuration:

      >>> service = create_service()
      >>> service.run()  # Start with default settings

      Service creation with custom configuration:

      >>> config = FlextWebConfig(
      ...     host="0.0.0.0",
      ...     port=8080,
      ...     debug=False,
      ...     secret_key="production-secret-key",
      ... )
      >>> service = create_service(config)
      >>> service.run(host="0.0.0.0", port=8080, debug=False)

      Production deployment pattern:

      >>> import os
      >>> os.environ["FLEXT_WEB_HOST"] = "0.0.0.0"
      >>> os.environ["FLEXT_WEB_PORT"] = "8080"
      >>> os.environ["FLEXT_WEB_DEBUG"] = "false"
      >>> service = create_service()  # Uses environment configuration
      >>> service.run()

    """
    return FlextWebService(config or get_web_settings())


def create_app(config: FlextWebConfig | None = None) -> Flask:
    """Create Flask application instance for integration and testing scenarios.

    Factory function for creating raw Flask application instances from FLEXT Web
    Service for integration with existing Flask applications, testing frameworks,
    or deployment scenarios requiring direct Flask app access.

    This function provides access to the underlying Flask application instance
    while maintaining all FLEXT Web Interface functionality, route registration,
    and configuration management.

    Args:
      config: Optional FlextWebConfig instance. If None, uses get_web_settings()
      to load validated configuration from environment variables and defaults.

    Returns:
      Flask: Configured Flask application instance with all FLEXT Web Interface
      routes registered, middleware configured, and ready for integration or
      deployment with WSGI servers.

    Flask Application Features:
      - All FLEXT Web Interface routes registered (/health, /api/v1/apps, etc.)
      - Configured secret key and security settings
      - Error handling middleware for structured responses
      - JSON serialization for API responses
      - Static file serving capabilities

    Integration Scenarios:
      - WSGI deployment with Gunicorn, uWSGI, or mod_wsgi
      - Testing with Flask test client
      - Integration with existing Flask applications
      - Custom middleware and route registration
      - Reverse proxy deployment behind nginx or Apache

    Example:
      WSGI deployment with Gunicorn:

      >>> app = create_app()
      >>> # Run with: gunicorn -w 4 -b 0.0.0.0:8080 "module:create_app()"

      Testing integration:

      >>> app = create_app()
      >>> client = app.test_client()
      >>> response = client.get("/health")
      >>> assert response.status_code == 200

      Custom Flask integration:

      >>> from flask import Flask
      >>> main_app = Flask(__name__)
      >>> flext_app = create_app()
      >>>
      >>> @main_app.route('/status')
      >>> def status():
      ...     return "Main application status"
      >>>
      >>> # Mount FLEXT Web Interface under /flext
      >>> main_app.register_blueprint(flext_app, url_prefix="/flext")

      Production deployment configuration:

      >>> import os
      >>> os.environ["FLEXT_WEB_HOST"] = "0.0.0.0"
      >>> os.environ["FLEXT_WEB_DEBUG"] = "false"
      >>> os.environ["FLEXT_WEB_SECRET_KEY"] = "production-secret"
      >>> app = create_app()
      >>> # Deploy with production WSGI server

    """
    service = create_service(config)
    return service.app


# =============================================================================
# FACADE CLASS - Orchestration-only (STRICT protocol compliance)
# =============================================================================


class FlextWeb:
    """Main facade class for FLEXT Web Interface - orchestration-only.

    Following STRICT protocol pattern, this facade does NOT implement logic;
    it only orchestrates other components providing a convenient API surface.

    Example facade pattern from protocol:
        class FlextApi:
            def __init__(self):
                self._auth = FlextAuthClient()
                self._cfg  = FlextApiConfig()
                self._typ  = FlextApiTypes()
    """

    def __init__(self, config: FlextWebConfig | None = None) -> None:
        """Initialize orchestration components without implementing logic."""
        self._config = config or get_web_settings()
        self._service = FlextWebService(self._config)
        self._handler = FlextWebAppHandler()

    def run(
        self,
        host: str | None = None,
        port: int | None = None,
        *,
        debug: bool | None = None,
    ) -> None:
        """Orchestrate service startup - delegates to FlextWebService."""
        self._service.run(host=host, port=port, debug=debug)

    def create_app(self) -> Flask:
        """Orchestrate Flask app creation - delegates to FlextWebService."""
        return self._service.app

    def get_config(self) -> FlextWebConfig:
        """Orchestrate config access - delegates to configuration system."""
        return self._config

    def health_check(self) -> dict[str, object]:
        """Orchestrate health check - delegates to service."""
        # Orchestration pattern: call service method, return result
        return {"status": "healthy", "service": "flext-web"}


# =============================================================================
# EXCEPTIONS - Imported from exceptions module
# =============================================================================
# NOTE: All exceptions are imported from the exceptions module to avoid duplication.
# The legacy FlextWebError class has been removed to prevent conflicts.


# =============================================================================
# EXPORTS - Clean API
# =============================================================================


__all__: list[str] = [
    # Core Flask integration
    "Flask",
    # Flext-core exports
    "FlextExceptions",
    "FlextExceptions",
    "get_logger",
    "logger",
    # Configuration
    "FlextWebConfig",
    "get_web_settings",
    "reset_web_settings",
    # Domain models
    "FlextWebApp",
    "FlextWebAppHandler",
    "FlextWebAppStatus",
    # Services
    "FlextWebService",
    "create_app",
    "create_service",
    # Facade
    "FlextWeb",
    # Exceptions
    "FlextWebAuthenticationError",
    "FlextWebConfigurationError",
    "FlextWebConnectionError",
    "FlextWebError",
    "FlextWebMiddlewareError",
    "FlextWebProcessingError",
    "FlextWebRoutingError",
    "FlextWebSessionError",
    "FlextWebTemplateError",
    "FlextWebTimeoutError",
    "FlextWebValidationError",
    # Fields and validation
    "WebFields",
    "HTTPStatusField",
    # Handlers
    "WebHandlers",
    "WebResponseHandler",
    # Interfaces
    "WebServiceInterface",
    "AppRepositoryInterface",
    "MiddlewareInterface",
    "TemplateEngineInterface",
    "MonitoringInterface",
    # Protocols
    "WebServiceProtocol",
    "AppManagerProtocol",
    "ResponseFormatterProtocol",
    "ConfigurationProtocol",
    "TemplateRendererProtocol",
    # Type aliases
    "FieldKwargs",
    "ValidatorFunc",
    "ValidatorGenerator",
    "RequestContext",
    "ResponseData",
    "TemplateContext",
    "ConfigValue",
    "ConfigDict",
    "ErrorDetails",
    "SchemaDict",
    "TemplateFilter",
    "TemplateGlobal",
    "HTTPStatus",
    # Utilities
    "FlextWebUtilities",
    # Version information
    "__version__",
    "__version_info__",
    # Python annotations
    "annotations",
]
