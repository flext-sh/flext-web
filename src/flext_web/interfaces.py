"""FLEXT Web Interfaces - Abstract base classes and contracts for web components.

This module defines abstract interfaces for web components, extending
the base interfaces from flext-core with web-specific contracts.

Interfaces provide formal contracts through inheritance, supporting
polymorphism and enforcing implementation requirements across the
web domain.

Key Components:
    - Abstract web service interfaces
    - Repository interfaces for data persistence
    - Middleware interfaces for request processing
    - Integration interfaces for external systems
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from flask.typing import ResponseReturnValue
from flext_core import FlextResult

from flext_web.models import FlextWebApp
from flext_web.type_aliases import (
    RequestContext,
    ResponseData,
    TemplateContext,
    TemplateFilter,
    TemplateGlobal,
)


class WebServiceInterface(ABC):
    """Abstract interface for web service implementations.

    Defines the contract that all web service implementations must follow,
    ensuring consistent behavior across different service implementations.
    """

    @abstractmethod
    def initialize_routes(self) -> None:
        """Initialize web service routes and endpoints.

        Must be implemented by concrete web service classes to define
        all HTTP routes and their corresponding handlers.
        """

    @abstractmethod
    def configure_middleware(self) -> None:
        """Configure request/response middleware.

        Must be implemented to set up middleware for security,
        logging, error handling, and other cross-cutting concerns.
        """

    @abstractmethod
    def start_service(
        self, host: str, port: int, *, debug: bool = False, **kwargs: object
    ) -> None:
        """Start the web service with specified configuration.

        Args:
            host: Host address to bind to
            port: Port number to bind to
            debug: Debug mode flag
            **kwargs: Additional service configuration

        """

    @abstractmethod
    def stop_service(self) -> None:
        """Stop the web service gracefully.

        Must handle cleanup of resources, connection closure,
        and graceful shutdown procedures.
        """


class AppRepositoryInterface(ABC):
    """Abstract interface for application data persistence.

    Defines the contract for application repository implementations
    supporting different storage backends (memory, database, etc.).
    """

    @abstractmethod
    def create(self, app: FlextWebApp) -> FlextResult[FlextWebApp]:
        """Create and store a new application.

        Args:
            app: Application entity to create

        Returns:
            FlextResult containing created application or error.

        """

    @abstractmethod
    def get(self, app_id: str) -> FlextResult[FlextWebApp]:
        """Retrieve application by ID.

        Args:
            app_id: Unique application identifier

        Returns:
            FlextResult containing application or error if not found.

        """

    @abstractmethod
    def update(self, app: FlextWebApp) -> FlextResult[FlextWebApp]:
        """Update existing application.

        Args:
            app: Updated application entity

        Returns:
            FlextResult containing updated application or error.

        """

    @abstractmethod
    def delete(self, app_id: str) -> FlextResult[None]:
        """Delete application by ID.

        Args:
            app_id: Unique application identifier

        Returns:
            FlextResult indicating success or error.

        """

    @abstractmethod
    def list_all(self) -> FlextResult[list[FlextWebApp]]:
        """List all applications.

        Returns:
            FlextResult containing list of applications or error.

        """

    @abstractmethod
    def find_by_name(self, name: str) -> FlextResult[FlextWebApp]:
        """Find application by name.

        Args:
            name: Application name to search for

        Returns:
            FlextResult containing application or error if not found.

        """


class MiddlewareInterface(ABC):
    """Abstract interface for request/response middleware.

    Defines the contract for middleware components that process
    HTTP requests and responses with cross-cutting concerns.
    """

    @abstractmethod
    def before_request(self, request: RequestContext) -> FlextResult[RequestContext]:
        """Process request before routing to handlers.

        Args:
            request: HTTP request object

        Returns:
            FlextResult containing processed request or error.

        """

    @abstractmethod
    def after_request(self, response: ResponseData) -> FlextResult[ResponseData]:
        """Process response after handler execution.

        Args:
            response: HTTP response object

        Returns:
            FlextResult containing processed response or error.

        """

    @abstractmethod
    def handle_error(self, error: Exception) -> ResponseReturnValue:
        """Handle exceptions during request processing.

        Args:
            error: Exception that occurred during processing

        Returns:
            HTTP error response.

        """


class TemplateEngineInterface(ABC):
    """Abstract interface for template rendering engines.

    Defines the contract for template engines supporting
    HTML rendering with context variables and layouts.
    """

    @abstractmethod
    def configure(self, template_folder: str) -> None:
        """Configure template engine with template directory.

        Args:
            template_folder: Path to template directory

        """

    @abstractmethod
    def render(self, template_name: str, **context: TemplateContext) -> str:
        """Render template with context variables.

        Args:
            template_name: Name of template file
            **context: Template context variables

        Returns:
            Rendered HTML string.

        """

    @abstractmethod
    def add_filter(self, name: str, filter_func: TemplateFilter) -> None:
        """Add custom template filter.

        Args:
            name: Filter name for use in templates
            filter_func: Filter function implementation

        """

    @abstractmethod
    def add_global(self, name: str, value: TemplateGlobal) -> None:
        """Add global template variable.

        Args:
            name: Variable name for use in templates
            value: Variable value

        """


class MonitoringInterface(ABC):
    """Abstract interface for monitoring and observability.

    Defines the contract for monitoring systems providing
    metrics collection, health checks, and observability features.
    """

    @abstractmethod
    def record_request(
        self, method: str, path: str, status_code: int, duration: float
    ) -> None:
        """Record HTTP request metrics.

        Args:
            method: HTTP method
            path: Request path
            status_code: Response status code
            duration: Request processing duration

        """

    @abstractmethod
    def record_error(
        self,
        error_type: str,
        error_message: str,
        context: dict[str, ResponseData] | None = None,
    ) -> None:
        """Record error occurrence.

        Args:
            error_type: Type of error
            error_message: Error description
            context: Optional error context

        """

    @abstractmethod
    def get_health_status(self) -> dict[str, ResponseData]:
        """Get current service health status.

        Returns:
            Dictionary containing health metrics and status.

        """

    @abstractmethod
    def get_metrics(self) -> dict[str, ResponseData]:
        """Get collected metrics data.

        Returns:
            Dictionary containing service metrics.

        """
