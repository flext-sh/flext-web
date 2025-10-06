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


class FlextWebProtocols:
    """Single unified web protocols class following FLEXT standards.

    Contains all protocol definitions for web domain operations.
    Follows FLEXT pattern: one class per module with nested subclasses.
    """

    # =========================================================================
    # RE-EXPORT FOUNDATION PROTOCOLS - Use FlextProtocols from flext-core
    # =========================================================================

    Foundation = FlextProtocols.Foundation
    Domain = FlextProtocols.Domain
    Application = FlextProtocols.Application
    Infrastructure = FlextProtocols.Infrastructure
    Extensions = FlextProtocols.Extensions
    Commands = FlextProtocols.Commands

    # =========================================================================
    # WEB-SPECIFIC PROTOCOLS - Domain extension for web operations
    # =========================================================================

    class Web:
        """Web domain-specific protocols."""

        @runtime_checkable
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

        @runtime_checkable
        class ResponseFormatterProtocol(Protocol):
            """Protocol for HTTP response formatting.

            Defines the interface contract for consistent response formatting
            across all web endpoints with proper error handling.
            """

            def format_success(
                self,
                data: FlextTypes.Dict,
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

        @runtime_checkable
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

            def get_request_data(self) -> FlextTypes.JsonValue:
                """Get request data in framework-agnostic way."""
                ...

            def is_json_request(self) -> bool:
                """Check if current request is JSON."""
                ...

        @runtime_checkable
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
            FlextProtocols.Domain.Repository,
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
                response: FlextTypes.Dict,
            ) -> FlextResult[FlextTypes.Dict]:
                """Process response after handler execution."""
                ...

            def handle__error(
                self, _error: Exception
            ) -> FlextWebTypes.Core.WebResponse:
                """Handle exceptions during request processing."""
                ...

        @runtime_checkable
        class TemplateEngineInterface(
            FlextProtocols.Infrastructure.Configurable, Protocol
        ):
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
                context: FlextTypes.NestedDict | None = None,
            ) -> None:
                """Record error occurrence."""
                ...

            def get_health_status(self) -> FlextTypes.NestedDict:
                """Get current service health status."""
                ...

            def get_metrics(self) -> FlextTypes.NestedDict:
                """Get collected metrics data."""
                ...


# =============================================================================
# PUBLIC API EXPORTS
__all__ = [
    "FlextWebProtocols",
]
