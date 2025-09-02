"""FLEXT Web Protocols - Consolidated protocol system extending flext-core patterns.

This module implements the consolidated protocol architecture following the
"one class per module" pattern, with FlextWebProtocols extending FlextProtocols
and containing all web-specific protocol functionality as nested classes.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flask.typing import ResponseReturnValue
from flext_core import FlextProtocols, FlextResult

from flext_web.models import FlextWebModels
from flext_web.typings import FlextWebTypes

# =============================================================================
# CONSOLIDATED PROTOCOLS CLASS
# =============================================================================


class FlextWebProtocols(FlextProtocols):
    """Consolidated web protocol system extending flext-core patterns.

    This class serves as the single point of access for all web-specific
    protocols and interfaces while extending FlextProtocols from flext-core
    for proper architectural inheritance.

    All protocol functionality is accessible through this single class following the
    "one class per module" architectural requirement.
    """

    # =========================================================================
    # WEB SERVICE PROTOCOLS
    # =========================================================================

    class WebServiceProtocol(Protocol):
        """Protocol for web service implementations.

        Defines the interface contract for web services providing
        HTTP endpoints and application management capabilities.
        """

        def run(
            self,
            host: str | None = None,
            port: int | None = None,
            *,
            debug: bool | None = None,
            **kwargs: object,
        ) -> None:
            """Run the web service with specified configuration.

            Args:
                host: Optional host override
                port: Optional port override
                debug: Optional debug mode override
                **kwargs: Additional configuration options

            """
            ...

        def health(self) -> ResponseReturnValue:
            """Return health check response.

            Returns:
                HTTP response indicating service health status.

            """
            ...

    class AppManagerProtocol(Protocol):
        """Protocol for application management operations.

        Defines the interface contract for managing web applications
        including lifecycle operations and status tracking.
        """

        def create_app(
            self, name: str, port: int, host: str
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Create a new application.

            Args:
                name: Application name
                port: Application port
                host: Application host

            Returns:
                FlextResult containing created application or error.

            """
            ...

        def start_app(self, app_id: str) -> FlextResult[FlextWebModels.WebApp]:
            """Start an application.

            Args:
                app_id: Application identifier

            Returns:
                FlextResult containing updated application or error.

            """
            ...

        def stop_app(self, app_id: str) -> FlextResult[FlextWebModels.WebApp]:
            """Stop an application.

            Args:
                app_id: Application identifier

            Returns:
                FlextResult containing updated application or error.

            """
            ...

        def list_apps(self) -> FlextResult[list[FlextWebModels.WebApp]]:
            """List all applications.

            Returns:
                FlextResult containing list of applications or error.

            """
            ...

    # =========================================================================
    # RESPONSE AND CONFIGURATION PROTOCOLS
    # =========================================================================

    class ResponseFormatterProtocol(Protocol):
        """Protocol for HTTP response formatting.

        Defines the interface contract for consistent response formatting
        across all web endpoints with proper error handling.
        """

        def format_success(
            self,
            data: dict[str, object],
            message: str = "Success",
            status_code: int = 200,
        ) -> ResponseReturnValue:
            """Format success response.

            Args:
                data: Response data
                message: Success message
                status_code: HTTP status code

            Returns:
                Formatted HTTP response.

            """
            ...

        def format_error(
            self,
            message: str,
            status_code: int = 500,
            details: str | None = None,
        ) -> ResponseReturnValue:
            """Format error response.

            Args:
                message: Error message
                status_code: HTTP status code
                details: Optional error details

            Returns:
                Formatted HTTP error response.

            """
            ...

    class ConfigurationProtocol(Protocol):
        """Protocol for web configuration management.

        Defines the interface contract for configuration providers
        with environment integration and validation.
        """

        def get_host(self) -> str:
            """Get configured host address.

            Returns:
                Host address for server binding.

            """
            ...

        def get_port(self) -> int:
            """Get configured port number.

            Returns:
                Port number for server binding.

            """
            ...

        def is_debug_mode(self) -> bool:
            """Check if debug mode is enabled.

            Returns:
                True if debug mode is enabled, False otherwise.

            """
            ...

        def is_production(self) -> bool:
            """Check if running in production mode.

            Returns:
                True if in production mode, False otherwise.

            """
            ...

        def validate(self) -> FlextResult[None]:
            """Validate configuration settings.

            Returns:
                FlextResult indicating validation success or failure.

            """
            ...

    class TemplateRendererProtocol(Protocol):
        """Protocol for template rendering services.

        Defines the interface contract for template engines
        providing HTML rendering capabilities.
        """

        def render_template(self, template_name: str, **context: object) -> str:
            """Render template with provided context.

            Args:
                template_name: Name of template to render
                **context: Template context variables

            Returns:
                Rendered HTML string.

            """
            ...

        def render_dashboard(
            self, apps: list[FlextWebModels.WebApp], **context: object
        ) -> str:
            """Render dashboard template.

            Args:
                apps: List of applications to display
                **context: Additional context variables

            Returns:
                Rendered dashboard HTML.

            """
            ...

    # =========================================================================
    # PROTOCOL FACTORY METHODS
    # =========================================================================

    @classmethod
    def create_web_service_protocol(cls) -> WebServiceProtocol:
        """Create web service protocol instance.

        Returns:
            WebServiceProtocol for interface checking

        """

        # This is primarily for type checking and interface validation
        class _WebServiceProtocolImpl:
            def run(
                self,
                host: str | None = None,
                port: int | None = None,
                *,
                debug: bool | None = None,
                **kwargs: object,
            ) -> None:
                pass

            def health(self) -> ResponseReturnValue:
                from flask import jsonify

                return jsonify({"status": "ok"})

        return _WebServiceProtocolImpl()

    @classmethod
    def create_app_manager_protocol(cls) -> AppManagerProtocol:
        """Create app manager protocol instance.

        Returns:
            AppManagerProtocol for interface checking

        """

        class _AppManagerProtocolImpl:
            def create_app(
                self, name: str, port: int, host: str
            ) -> FlextResult[FlextWebModels.WebApp]:
                app = FlextWebModels.WebApp(
                    id=f"app_{name}", name=name, port=port, host=host
                )
                return FlextResult[FlextWebModels.WebApp].ok(app)

            def start_app(self, app_id: str) -> FlextResult[FlextWebModels.WebApp]:
                app = FlextWebModels.WebApp(
                    id=app_id,
                    name="mock",
                    port=8080,
                    host="localhost",
                    status=FlextWebModels.WebAppStatus.RUNNING,
                )
                return FlextResult[FlextWebModels.WebApp].ok(app)

            def stop_app(self, app_id: str) -> FlextResult[FlextWebModels.WebApp]:
                app = FlextWebModels.WebApp(
                    id=app_id,
                    name="mock",
                    port=8080,
                    host="localhost",
                    status=FlextWebModels.WebAppStatus.STOPPED,
                )
                return FlextResult[FlextWebModels.WebApp].ok(app)

            def list_apps(self) -> FlextResult[list[FlextWebModels.WebApp]]:
                return FlextResult[list[FlextWebModels.WebApp]].ok([])

        return _AppManagerProtocolImpl()

    @classmethod
    def validate_web_service_protocol(cls, service: object) -> bool:
        """Validate if object implements WebServiceProtocol.

        Args:
            service: Object to validate

        Returns:
            True if object implements the protocol

        """
        required_methods = ["run", "health"]
        return all(hasattr(service, method) for method in required_methods)

    @classmethod
    def validate_app_manager_protocol(cls, manager: object) -> bool:
        """Validate if object implements AppManagerProtocol.

        Args:
            manager: Object to validate

        Returns:
            True if object implements the protocol

        """
        required_methods = ["create_app", "start_app", "stop_app", "list_apps"]
        return all(hasattr(manager, method) for method in required_methods)

    # =========================================================================
    # CONSOLIDATED INTERFACE PROTOCOLS (from interfaces.py)
    # =========================================================================

    @runtime_checkable
    class WebServiceInterface(FlextProtocols.Domain.Service, Protocol):
        """Web service protocol extending flext-core Service patterns.

        Composing with FlextProtocols.Domain.Service provides standard
        service lifecycle management (start/stop/health_check) while
        adding web-specific contract requirements.
        """

        def initialize_routes(self) -> None:
            """Initialize web service routes and endpoints."""
            ...

        def configure_middleware(self) -> None:
            """Configure request/response middleware."""
            ...

        def start_service(
            self, host: str, port: int, *, debug: bool = False, **kwargs: object
        ) -> None:
            """Start the web service with specified configuration."""
            ...

        def stop_service(self) -> None:
            """Stop the web service gracefully."""
            ...

    @runtime_checkable
    class AppRepositoryInterface(
        FlextProtocols.Domain.Repository[FlextWebModels.WebApp], Protocol
    ):
        """Application repository protocol extending flext-core Repository patterns."""

        def create(
            self, app: FlextWebModels.WebApp
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Create and store a new application."""
            ...

        def get(self, app_id: str) -> FlextResult[FlextWebModels.WebApp]:
            """Retrieve application by ID."""
            ...

        def update(
            self, app: FlextWebModels.WebApp
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Update existing application."""
            ...

        def find_by_name(self, name: str) -> FlextResult[FlextWebModels.WebApp]:
            """Find application by name."""
            ...

    @runtime_checkable
    class MiddlewareInterface(FlextProtocols.Extensions.Middleware, Protocol):
        """Web middleware protocol extending flext-core Middleware patterns."""

        def before_request(
            self, request: FlextWebTypes.RequestContext
        ) -> FlextResult[FlextWebTypes.RequestContext]:
            """Process request before routing to handlers."""
            ...

        def after_request(
            self, response: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Process response after handler execution."""
            ...

        def handle_error(self, error: Exception) -> ResponseReturnValue:
            """Handle exceptions during request processing."""
            ...

    @runtime_checkable
    class TemplateEngineInterface(FlextProtocols.Infrastructure.Configurable, Protocol):
        """Template engine protocol extending flext-core Configurable patterns."""

        def render(self, template_name: str, **context: object) -> str:
            """Render template with context variables."""
            ...

        def add_filter(
            self, name: str, filter_func: FlextWebTypes.TemplateFilter
        ) -> None:
            """Add custom template filter."""
            ...

        def add_global(self, name: str, value: object) -> None:
            """Add global template variable."""
            ...

    @runtime_checkable
    class MonitoringInterface(FlextProtocols.Extensions.Observability, Protocol):
        """Web monitoring protocol extending flext-core Observability patterns."""

        def record_request(
            self, method: str, path: str, status_code: int, duration: float
        ) -> None:
            """Record HTTP request metrics."""
            ...

        def record_error(
            self,
            error_type: str,
            error_message: str,
            context: dict[str, dict[str, object]] | None = None,
        ) -> None:
            """Record error occurrence."""
            ...

        def get_health_status(self) -> dict[str, dict[str, object]]:
            """Get current service health status."""
            ...

        def get_metrics(self) -> dict[str, dict[str, object]]:
            """Get collected metrics data."""
            ...


# =============================================================================
# BACKWARD COMPATIBILITY ALIASES
__all__ = [
    "FlextWebProtocols",
]
