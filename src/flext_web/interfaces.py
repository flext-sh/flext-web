"""FLEXT Web Interfaces - Web-specific protocol extensions.

This module defines web-specific protocol extensions that build upon
the hierarchical protocol architecture from flext-core, eliminating
local abstract base classes in favor of composition patterns.

All interfaces now use flext-core protocols following the ZERO TOLERANCE
methodology for architectural compliance.

Key Components:
    - Protocol-based web service contracts
    - Repository protocols extending flext-core patterns
    - Middleware protocols for request processing
    - Integration protocols for external systems
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flask.typing import ResponseReturnValue
from flext_core import FlextProtocols, FlextResult

from flext_web.models import FlextWebApp
from flext_web.type_aliases import (
    RequestContext,
    ResponseData,
    TemplateContext,
    TemplateFilter,
    TemplateGlobal,
)


@runtime_checkable
class WebServiceInterface(FlextProtocols.Domain.Service, Protocol):
    """Web service protocol extending flext-core Service patterns.

    Composing with FlextProtocols.Domain.Service provides standard
    service lifecycle management (start/stop/health_check) while
    adding web-specific contract requirements.
    """

    def initialize_routes(self) -> None:
        """Initialize web service routes and endpoints.

        Web-specific method for route registration beyond base service contract.
        """
        ...

    def configure_middleware(self) -> None:
        """Configure request/response middleware.

        Web-specific method for middleware setup beyond base service contract.
        """
        ...

    def start_service(
        self, host: str, port: int, *, debug: bool = False, **kwargs: object
    ) -> None:
        """Start the web service with specified configuration.

        Args:
            host: Host address to bind to
            port: Port number to bind to
            debug: Debug mode flag
            **kwargs: Additional service configuration

        Note: This extends the base Service.start() method with web-specific parameters.

        """
        ...

    def stop_service(self) -> None:
        """Stop the web service gracefully.

        Extends the base Service.stop() method with web-specific shutdown logic.
        """
        ...


@runtime_checkable
class AppRepositoryInterface(FlextProtocols.Domain.Repository[FlextWebApp], Protocol):
    """Application repository protocol extending flext-core Repository patterns.

    Inherits standard repository operations (get_by_id, save, delete, find_all)
    from FlextProtocols.Domain.Repository[FlextWebApp] while adding web-specific
    query methods for application management.
    """

    def create(self, app: FlextWebApp) -> FlextResult[FlextWebApp]:
        """Create and store a new application.

        Args:
            app: Application entity to create

        Returns:
            FlextResult containing created application or error.

        Note: This extends the base Repository.save() method with creation semantics.

        """
        ...

    def get(self, app_id: str) -> FlextResult[FlextWebApp]:
        """Retrieve application by ID.

        Args:
            app_id: Unique application identifier

        Returns:
            FlextResult containing application or error if not found.

        Note: This aliases the base Repository.get_by_id() method for consistency.

        """
        ...

    def update(self, app: FlextWebApp) -> FlextResult[FlextWebApp]:
        """Update existing application.

        Args:
            app: Updated application entity

        Returns:
            FlextResult containing updated application or error.

        Note: This extends the base Repository.save() method with update semantics.

        """
        ...

    def find_by_name(self, name: str) -> FlextResult[FlextWebApp]:
        """Find application by name.

        Args:
            name: Application name to search for

        Returns:
            FlextResult containing application or error if not found.

        Web-specific query method beyond base repository contract.

        """
        ...


@runtime_checkable
class MiddlewareInterface(FlextProtocols.Extensions.Middleware, Protocol):
    """Web middleware protocol extending flext-core Middleware patterns.

    Inherits the base Middleware.process() method while adding web-specific
    request/response processing and error handling capabilities.
    """

    def before_request(self, request: RequestContext) -> FlextResult[RequestContext]:
        """Process request before routing to handlers.

        Args:
            request: HTTP request object

        Returns:
            FlextResult containing processed request or error.

        Web-specific method for request preprocessing beyond base middleware contract.

        """
        ...

    def after_request(self, response: ResponseData) -> FlextResult[ResponseData]:
        """Process response after handler execution.

        Args:
            response: HTTP response object

        Returns:
            FlextResult containing processed response or error.

        Web-specific method for response postprocessing beyond base middleware contract.

        """
        ...

    def handle_error(self, error: Exception) -> ResponseReturnValue:
        """Handle exceptions during request processing.

        Args:
            error: Exception that occurred during processing

        Returns:
            HTTP error response.

        Web-specific error handling method for HTTP error responses.

        """
        ...


@runtime_checkable
class TemplateEngineInterface(FlextProtocols.Infrastructure.Configurable, Protocol):
    """Template engine protocol extending flext-core Configurable patterns.

    Inherits configuration management (configure, get_config) from base
    Configurable protocol while adding template-specific rendering capabilities.
    """

    def render(self, template_name: str, **context: TemplateContext) -> str:
        """Render template with context variables.

        Args:
            template_name: Name of template file
            **context: Template context variables

        Returns:
            Rendered HTML string.

        """
        ...

    def add_filter(self, name: str, filter_func: TemplateFilter) -> None:
        """Add custom template filter.

        Args:
            name: Filter name for use in templates
            filter_func: Filter function implementation

        """
        ...

    def add_global(self, name: str, value: TemplateGlobal) -> None:
        """Add global template variable.

        Args:
            name: Variable name for use in templates
            value: Variable value

        """
        ...


@runtime_checkable
class MonitoringInterface(FlextProtocols.Extensions.Observability, Protocol):
    """Web monitoring protocol extending flext-core Observability patterns.

    Inherits metrics recording and health checks from base Observability
    protocol while adding web-specific monitoring capabilities.
    """

    def record_request(
        self, method: str, path: str, status_code: int, duration: float
    ) -> None:
        """Record HTTP request metrics.

        Args:
            method: HTTP method
            path: Request path
            status_code: Response status code
            duration: Request processing duration

        Web-specific method beyond base observability contract.

        """
        ...

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

        Web-specific error recording beyond base observability contract.

        """
        ...

    def get_health_status(self) -> dict[str, ResponseData]:
        """Get current service health status.

        Returns:
            Dictionary containing health metrics and status.

        Web-specific health status format extending base health_check.

        """
        ...

    def get_metrics(self) -> dict[str, ResponseData]:
        """Get collected metrics data.

        Returns:
            Dictionary containing service metrics.

        Web-specific metrics format beyond base observability contract.

        """
        ...
