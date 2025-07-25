"""FLEXT Web Application Services - Web interface services.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Application services for web interface operations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import FlextContainer, FlextResult

if TYPE_CHECKING:
    from flext_web.domain.entities import (
        FlextDashboard,
        FlextResponse,
        FlextTemplate,
        FlextWebApp,
    )


class FlextWebAPIService:
    """Application service for web API operations.

    Clean Architecture application service that orchestrates domain operations.
    Stateless service with dependency injection support.
    """

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize web API service.

        Args:
            container: Dependency injection container

        """
        self._container = container or FlextContainer()

    @property
    def container(self) -> FlextContainer:
        """Get the dependency injection container."""
        return self._container

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
        try:
            # Import here to avoid circular imports
            import uuid

            from flext_web.domain.entities import FlextWebApp, FlextWebAppStatus

            if not name:
                return FlextResult.fail("Application name is required")

            if port < 1 or port > 65535:
                return FlextResult.fail("Port must be between 1 and 65535")

            app = FlextWebApp(
                entity_id=str(uuid.uuid4()),
                name=name,
                host=host,
                port=port,
                status=FlextWebAppStatus.STOPPED,
                config=config or {},
            )

            if not app.is_valid():
                return FlextResult.fail("Invalid web app data")

            return FlextResult.ok(app)

        except Exception as e:
            return FlextResult.fail(f"Web app creation failed: {e}")

    def start_app(self, app: FlextWebApp) -> FlextResult[bool]:
        """Start a web application.

        Args:
            app: Web app to start

        Returns:
            FlextResult indicating success

        """
        try:
            if not app.start():
                return FlextResult.fail("Application is not in a startable state")

            # Mark as running (simulated)
            app.mark_running()
            return FlextResult.ok(True)

        except Exception as e:
            return FlextResult.fail(f"Failed to start app: {e}")

    def stop_app(self, app: FlextWebApp) -> FlextResult[bool]:
        """Stop a web application.

        Args:
            app: Web app to stop

        Returns:
            FlextResult indicating success

        """
        try:
            if not app.stop():
                return FlextResult.fail("Application is not in a stoppable state")

            # Mark as stopped (simulated)
            app.mark_stopped()
            return FlextResult.ok(True)

        except Exception as e:
            return FlextResult.fail(f"Failed to stop app: {e}")

    def add_route(
        self,
        app: FlextWebApp,
        route: str,
    ) -> FlextResult[bool]:
        """Add a route to web application.

        Args:
            app: Web app to add route to
            route: Route to add

        Returns:
            FlextResult indicating success

        """
        try:
            if not route.startswith("/"):
                return FlextResult.fail("Route must start with /")

            if app.add_route(route):
                return FlextResult.ok(True)
            return FlextResult.fail("Route already exists")

        except Exception as e:
            return FlextResult.fail(f"Failed to add route: {e}")


class FlextDashboardService:
    """Application service for dashboard operations.

    Clean Architecture application service that orchestrates dashboard
    domain operations. Stateless service with dependency injection support.
    """

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize dashboard service.

        Args:
            container: Dependency injection container

        """
        self._container = container or FlextContainer()

    @property
    def container(self) -> FlextContainer:
        """Get the dependency injection container."""
        return self._container

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
        try:
            # Import here to avoid circular imports
            import uuid

            from flext_web.domain.entities import FlextDashboard

            if not title:
                return FlextResult.fail("Dashboard title is required")

            dashboard = FlextDashboard(
                entity_id=str(uuid.uuid4()),
                title=title,
                description=description,
                is_public=is_public,
            )

            if not dashboard.is_valid():
                return FlextResult.fail("Invalid dashboard data")

            return FlextResult.ok(dashboard)

        except Exception as e:
            return FlextResult.fail(f"Dashboard creation failed: {e}")

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
        try:
            if not widget.get("id"):
                return FlextResult.fail("Widget must have an ID")

            if dashboard.add_widget(widget):
                return FlextResult.ok(True)
            return FlextResult.fail("Widget with this ID already exists")

        except Exception as e:
            return FlextResult.fail(f"Failed to add widget: {e}")

    def remove_widget(
        self,
        dashboard: FlextDashboard,
        widget_id: str,
    ) -> FlextResult[bool]:
        """Remove a widget from dashboard.

        Args:
            dashboard: Dashboard to remove widget from
            widget_id: ID of widget to remove

        Returns:
            FlextResult indicating success

        """
        try:
            if dashboard.remove_widget(widget_id):
                return FlextResult.ok(True)
            return FlextResult.fail("Widget not found")

        except Exception as e:
            return FlextResult.fail(f"Failed to remove widget: {e}")

    def update_layout(
        self,
        dashboard: FlextDashboard,
        layout: dict[str, Any],
    ) -> FlextResult[bool]:
        """Update dashboard layout.

        Args:
            dashboard: Dashboard to update
            layout: New layout configuration

        Returns:
            FlextResult indicating success

        """
        try:
            object.__setattr__(dashboard, "layout", layout)
            return FlextResult.ok(True)

        except Exception as e:
            return FlextResult.fail(f"Failed to update layout: {e}")


class FlextTemplateService:
    """Application service for template operations.

    Clean Architecture application service that orchestrates template domain operations.
    Stateless service with dependency injection support.
    """

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize template service.

        Args:
            container: Dependency injection container

        """
        self._container = container or FlextContainer()

    @property
    def container(self) -> FlextContainer:
        """Get the dependency injection container."""
        return self._container

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
        try:
            # Import here to avoid circular imports
            import uuid

            from flext_web.domain.entities import FlextTemplate, FlextTemplateType

            if not name:
                return FlextResult.fail("Template name is required")

            if not content:
                return FlextResult.fail("Template content is required")

            # Convert string to enum
            try:
                template_type_enum = FlextTemplateType(template_type)
            except ValueError:
                return FlextResult.fail(f"Invalid template type: {template_type}")

            template = FlextTemplate(
                entity_id=str(uuid.uuid4()),
                name=name,
                content=content,
                template_type=template_type_enum,
                variables=variables or [],
            )

            if not template.is_valid():
                return FlextResult.fail("Invalid template data")

            return FlextResult.ok(template)

        except Exception as e:
            return FlextResult.fail(f"Template creation failed: {e}")

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
        try:
            rendered = template.render(context)
            return FlextResult.ok(rendered)

        except Exception as e:
            return FlextResult.fail(f"Template rendering failed: {e}")

    def extract_variables(
        self,
        template: FlextTemplate,
    ) -> FlextResult[list[str]]:
        """Extract variables from template.

        Args:
            template: Template to analyze

        Returns:
            FlextResult containing list of variables

        """
        try:
            variables = template.extract_variables()
            return FlextResult.ok(variables)

        except Exception as e:
            return FlextResult.fail(f"Variable extraction failed: {e}")

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
        try:
            # Import here to avoid circular imports
            import uuid

            from flext_web.domain.entities import FlextResponse

            response = FlextResponse(
                entity_id=str(uuid.uuid4()),
                status_code=status_code,
                content=content,
                headers=headers or {},
                content_type=content_type,
            )

            if not response.is_valid():
                return FlextResult.fail("Invalid response data")

            return FlextResult.ok(response)

        except Exception as e:
            return FlextResult.fail(f"Response creation failed: {e}")


# Backwards compatibility aliases
WebAPIService = FlextWebAPIService
DashboardService = FlextDashboardService
TemplateService = FlextTemplateService
