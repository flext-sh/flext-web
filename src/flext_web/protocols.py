"""FLEXT Web Protocols - Consolidated protocol system extending flext-core patterns.

This module implements the consolidated protocol architecture following the
"one class per module" pattern, with FlextWebProtocols extending FlextProtocols
and containing all web-specific protocol functionality as nested classes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols, FlextResult, FlextTypes
from flext_web.models import FlextWebModels
from flext_web.typings import FlextWebTypes


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

    class AppManagerProtocol(Protocol):
        """Protocol for application management operations.

        Defines the interface contract for managing web applications
        including lifecycle operations and status tracking.
        """

        def create_app(
            self,
            name: str,
            port: int,
            host: str,
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

        def start_app(self, _app_id: str) -> FlextResult[FlextWebModels.WebApp]:
            """Start an application.

            Args:
                app_id: Application identifier

            Returns:
                FlextResult containing updated application or error.

            """
            ...

        def stop_app(self, _app_id: str) -> FlextResult[FlextWebModels.WebApp]:
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
            data: FlextTypes.Core.Dict,
            message: str = "Success",
            status_code: int = 200,
        ) -> FlextWebTypes.Core.WebResponse:
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
        ) -> FlextWebTypes.Core.WebResponse:
            """Format error response.

            Args:
                message: Error message
                status_code: HTTP status code
                details: Optional error details

            Returns:
                Formatted HTTP error response.

            """
            ...

    # Use flext-core Configurable protocol instead of custom ConfigurationProtocol
    # This reduces duplication and leverages existing abstractions
    ConfigurationProtocol = FlextProtocols.Infrastructure.Configurable

    # =========================================================================
    # WEB FRAMEWORK ABSTRACTION PROTOCOLS
    # =========================================================================

    class WebFrameworkInterface(Protocol):
        """Framework-agnostic web interface.

        Abstracts web framework dependencies (Flask, FastAPI, etc.)
        to enable framework independence.
        """

        def create_json_response(
            self,
            data: FlextWebTypes.Core.JsonResponse,
            status_code: int = 200,
        ) -> FlextWebTypes.Core.WebResponse:
            """Create a JSON response in framework-agnostic way."""
            ...

        def get_request_data(self) -> FlextTypes.Core.JsonObject:
            """Get request data in framework-agnostic way."""
            ...

        def is_json_request(self) -> bool:
            """Check if current request is JSON."""
            ...

    class TemplateRendererProtocol(Protocol):
        """Protocol for template rendering services.

        Defines the interface contract for template engines
        providing HTML rendering capabilities.
        """

        def render_template(self, _template_name: str, **context: object) -> str:
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
            apps: list[FlextWebModels.WebApp],
            **context: object,
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
    def create_web_service_protocol(cls: object) -> object:
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
                msg = "Protocol implementation for type checking only"
                raise NotImplementedError(msg)

            def health(self) -> FlextWebTypes.Core.WebResponse:
                return '{"status": "ok"}', 200

        return _WebServiceProtocolImpl()

    @classmethod
    def create_app_manager_protocol(cls: object) -> AppManagerProtocol:
        """Create app manager protocol instance.

        Returns:
            AppManagerProtocol for interface checking

        """

        class _AppManagerProtocolImpl:
            def create_app(
                self,
                name: str,
                port: int,
                host: str,
            ) -> FlextResult[FlextWebModels.WebApp]:
                app = FlextWebModels.WebApp(
                    id=f"app_{name}",
                    name=name,
                    port=port,
                    host=host,
                )
                return FlextResult[FlextWebModels.WebApp].ok(app)

            def start_app(self, _app_id: str) -> FlextResult[FlextWebModels.WebApp]:
                app = FlextWebModels.WebApp(
                    id=_app_id,
                    name="mock",
                    port=8080,
                    host="localhost",
                    status=FlextWebModels.WebAppStatus.RUNNING,
                )
                return FlextResult[FlextWebModels.WebApp].ok(app)

            def stop_app(self, _app_id: str) -> FlextResult[FlextWebModels.WebApp]:
                app = FlextWebModels.WebApp(
                    id=_app_id,
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
    # CONSOLIDATED INTERFACE PROTOCOLS
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
            self,
            host: str,
            port: int,
            *,
            debug: bool = False,
            **kwargs: object,
        ) -> None:
            """Start the web service with specified configuration."""
            ...

        def stop_service(self) -> None:
            """Stop the web service gracefully."""
            ...

    @runtime_checkable
    class AppRepositoryInterface(
        FlextProtocols.Domain.Repository[FlextWebModels.WebApp],
        Protocol,
    ):
        """Application repository protocol extending flext-core Repository patterns.

        Returns:
            object: Description of return value.

        """

        def create(
            self,
            app: FlextWebModels.WebApp,
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Create and store a new application."""
            ...

        def get(self, _app_id: str) -> FlextResult[FlextWebModels.WebApp]:
            """Retrieve application by ID."""
            ...

        def update(
            self,
            app: FlextWebModels.WebApp,
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Update existing application."""
            ...

        def find_by__name(self, _name: str) -> FlextResult[FlextWebModels.WebApp]:
            """Find application by name."""
            ...

    @runtime_checkable
    class MiddlewareInterface(FlextProtocols.Extensions.Middleware, Protocol):
        """Web middleware protocol extending flext-core Middleware patterns.

        Returns:
            FlextResult[FlextWebModels.WebApp]: Middleware processing result.

        """

        def before_request(
            self,
            request: FlextWebTypes.RequestContext,
        ) -> FlextResult[FlextWebTypes.RequestContext]:
            """Process request before routing to handlers."""
            ...

        def after_request(
            self,
            response: FlextTypes.Core.Dict,
        ) -> FlextResult[FlextTypes.Core.Dict]:
            """Process response after handler execution."""
            ...

        def handle__error(self, _error: Exception) -> FlextWebTypes.Core.WebResponse:
            """Handle exceptions during request processing."""
            ...

    @runtime_checkable
    class TemplateEngineInterface(FlextProtocols.Infrastructure.Configurable, Protocol):
        """Template engine protocol extending flext-core Configurable patterns.

        Returns:
            ResponseReturnValue: Template rendering result.

        """

        def render(self, _template_name: str, **context: object) -> str:
            """Render template with context variables."""
            ...

        def add_filter(self, _name: str, filter_func: Callable[[str], str]) -> None:
            """Add custom template filter."""
            ...

        def add_global(self, _name: str, value: object) -> None:
            """Add global template variable."""
            ...

    @runtime_checkable
    class MonitoringInterface(FlextProtocols.Extensions.Observability, Protocol):
        """Web monitoring protocol extending flext-core Observability patterns.

        Returns:
            object: Monitoring operation result.

        """

        def record_request(
            self,
            method: str,
            path: str,
            status_code: int,
            duration: float,
        ) -> None:
            """Record HTTP request metrics."""
            ...

        def record_error(
            self,
            error_type: str,
            error_message: str,
            context: dict[str, FlextTypes.Core.Dict] | None = None,
        ) -> None:
            """Record error occurrence."""
            ...

        def get_health_status(self) -> dict[str, FlextTypes.Core.Dict]:
            """Get current service health status."""
            ...

        def get_metrics(self) -> dict[str, FlextTypes.Core.Dict]:
            """Get collected metrics data."""
            ...


# =============================================================================
# PUBLIC API EXPORTS
__all__ = [
    "FlextWebProtocols",
]
