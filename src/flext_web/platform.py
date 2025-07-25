"""FLEXT Web Platform - Unified web interface platform.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Platform class providing unified access to web interface services.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import FlextContainer, FlextError, FlextResult

from flext_web.application.services import (
    FlextDashboardService,
    FlextTemplateService,
    FlextWebAPIService,
)

if TYPE_CHECKING:
    from flext_web.domain.entities import (
        FlextDashboard,
        FlextResponse,
        FlextTemplate,
        FlextWebApp,
    )


class FlextWebPlatform:
    """Platform for web interface operations."""

    def __init__(self, config: dict[str, object] | None = None) -> None:
        """Initialize web platform.

        Args:
            config: Platform configuration

        """
        self.config = config or {}
        self.container = FlextContainer()
        self._setup_services()

    def _setup_services(self) -> None:
        """Setup platform services."""
        # Import here to avoid circular imports
        from flext_web.application.services import (
            FlextDashboardService,
            FlextTemplateService,
            FlextWebAPIService,
        )

        # Register services in container
        self.container.register("web_api_service", FlextWebAPIService(self.container))
        self.container.register(
            "dashboard_service",
            FlextDashboardService(self.container),
        )
        self.container.register(
            "template_service",
            FlextTemplateService(self.container),
        )

    @property
    def web_api_service(self) -> FlextWebAPIService:
        """Get web API service."""
        result = self.container.get("web_api_service")
        if result.is_success and isinstance(result.data, FlextWebAPIService):
            return result.data
        msg = f"Failed to get web API service: {result.error}"
        raise FlextError(msg)

    @property
    def dashboard_service(self) -> FlextDashboardService:
        """Get dashboard service."""
        result = self.container.get("dashboard_service")
        if result.is_success and isinstance(result.data, FlextDashboardService):
            return result.data
        msg = f"Failed to get dashboard service: {result.error}"
        raise FlextError(msg)

    @property
    def template_service(self) -> FlextTemplateService:
        """Get template service."""
        result = self.container.get("template_service")
        if result.is_success and isinstance(result.data, FlextTemplateService):
            return result.data
        msg = f"Failed to get template service: {result.error}"
        raise FlextError(msg)

    def create_app(
        self,
        name: str,
        host: str = "localhost",
        port: int = 8000,
        config: dict[str, Any] | None = None,
    ) -> FlextResult[FlextWebApp]:
        """Create a new web application.

        Args:
            name: Application name
            host: Host address
            port: Port number
            config: Application configuration

        Returns:
            FlextResult containing created web app

        """
        return self.web_api_service.create_app(name, host, port, config)

    def start_app(self, app: FlextWebApp) -> FlextResult[bool]:
        """Start a web application.

        Args:
            app: Web app to start

        Returns:
            FlextResult indicating success

        """
        return self.web_api_service.start_app(app)

    def stop_app(self, app: FlextWebApp) -> FlextResult[bool]:
        """Stop a web application.

        Args:
            app: Web app to stop

        Returns:
            FlextResult indicating success

        """
        return self.web_api_service.stop_app(app)

    def create_dashboard(
        self,
        title: str,
        description: str = "",
        is_public: bool = False,
    ) -> FlextResult[FlextDashboard]:
        """Create a new dashboard.

        Args:
            title: Dashboard title
            description: Dashboard description
            is_public: Whether dashboard is public

        Returns:
            FlextResult containing created dashboard

        """
        return self.dashboard_service.create_dashboard(title, description, is_public)

    def add_widget(
        self,
        dashboard: FlextDashboard,
        widget: dict[str, Any],
    ) -> FlextResult[bool]:
        """Add a widget to dashboard.

        Args:
            dashboard: Dashboard to add widget to
            widget: Widget configuration

        Returns:
            FlextResult indicating success

        """
        return self.dashboard_service.add_widget(dashboard, widget)

    def create_template(
        self,
        name: str,
        content: str,
        template_type: str = "page",
        variables: list[str] | None = None,
    ) -> FlextResult[FlextTemplate]:
        """Create a new template.

        Args:
            name: Template name
            content: Template content
            template_type: Type of template
            variables: Template variables

        Returns:
            FlextResult containing created template

        """
        return self.template_service.create_template(
            name,
            content,
            template_type,
            variables,
        )

    def render_template(
        self,
        template: FlextTemplate,
        context: dict[str, Any] | None = None,
    ) -> FlextResult[str]:
        """Render template with context.

        Args:
            template: Template to render
            context: Context variables

        Returns:
            FlextResult containing rendered content

        """
        return self.template_service.render_template(template, context)

    def create_response(
        self,
        content: str,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
        content_type: str = "text/html",
    ) -> FlextResult[FlextResponse]:
        """Create HTTP response.

        Args:
            content: Response content
            status_code: HTTP status code
            headers: Response headers
            content_type: Content type

        Returns:
            FlextResult containing created response

        """
        return self.template_service.create_response(
            content,
            status_code,
            headers,
            content_type,
        )

    def get_web_api(self) -> FlextWebAPIService:
        """Get the web API service (alias for web_api_service).

        Returns:
            Web API service

        """
        return self.web_api_service

    def get_dashboard(self) -> FlextDashboardService:
        """Get the dashboard service (alias for dashboard_service).

        Returns:
            Dashboard service

        """
        return self.dashboard_service

    def get_template(self) -> FlextTemplateService:
        """Get the template service (alias for template_service).

        Returns:
            Template service

        """
        return self.template_service


# Backwards compatibility alias
WebPlatform = FlextWebPlatform
