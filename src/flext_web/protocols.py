"""FLEXT Web Protocols - Type protocols and interfaces for web components.

This module defines protocols (structural typing interfaces) for web components,
extending the base protocols from flext-core with web-specific requirements.

Protocols provide type-safe contracts for web operations without requiring
inheritance, supporting dependency injection and testing patterns.

Key Components:
    - Web service protocols
    - Request/response protocols
    - Application management protocols
    - Integration protocols for external services
"""

from __future__ import annotations

from typing import Protocol

from flask.typing import ResponseReturnValue
from flext_core import FlextResult

from flext_web.models import FlextWebApp
from flext_web.type_aliases import ErrorDetails, ResponseData, TemplateContext


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
        **kwargs: object
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

    def create_app(self, name: str, port: int, host: str) -> FlextResult[FlextWebApp]:
        """Create a new application.

        Args:
            name: Application name
            port: Application port
            host: Application host

        Returns:
            FlextResult containing created application or error.

        """
        ...

    def start_app(self, app_id: str) -> FlextResult[FlextWebApp]:
        """Start an application.

        Args:
            app_id: Application identifier

        Returns:
            FlextResult containing updated application or error.

        """
        ...

    def stop_app(self, app_id: str) -> FlextResult[FlextWebApp]:
        """Stop an application.

        Args:
            app_id: Application identifier

        Returns:
            FlextResult containing updated application or error.

        """
        ...

    def list_apps(self) -> FlextResult[list[FlextWebApp]]:
        """List all applications.

        Returns:
            FlextResult containing list of applications or error.

        """
        ...


class ResponseFormatterProtocol(Protocol):
    """Protocol for HTTP response formatting.

    Defines the interface contract for consistent response formatting
    across all web endpoints with proper error handling.
    """

    def format_success(
        self,
        data: ResponseData,
        message: str = "Success",
        status_code: int = 200
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
        details: ErrorDetails = None
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

    def render_template(
        self,
        template_name: str,
        **context: TemplateContext
    ) -> str:
        """Render template with provided context.

        Args:
            template_name: Name of template to render
            **context: Template context variables

        Returns:
            Rendered HTML string.

        """
        ...

    def render_dashboard(
        self,
        apps: list[FlextWebApp],
        **context: TemplateContext
    ) -> str:
        """Render dashboard template.

        Args:
            apps: List of applications to display
            **context: Additional context variables

        Returns:
            Rendered dashboard HTML.

        """
        ...
