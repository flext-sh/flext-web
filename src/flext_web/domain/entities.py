"""FLEXT Web Domain Entities - Core web interface business entities.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Core domain entities for web interface system.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from flext_core import FlextEntity
from pydantic import Field


class FlextWebAppStatus(Enum):
    """Web application status enumeration."""

    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"


class FlextTemplateType(Enum):
    """Template type enumeration."""

    PAGE = "page"
    COMPONENT = "component"
    EMAIL = "email"
    PDF = "pdf"


# TODO: Refactored to use FlextEntity pattern
class FlextWebApp(FlextEntity):
    """Web application entity representing a web app instance."""

    entity_id: str = Field(..., description="Unique entity identifier")
    name: str = Field(..., description="Web app name")
    host: str = Field(default="localhost", description="Host address")
    port: int = Field(default=8000, ge=1, le=65535, description="Port number")
    status: FlextWebAppStatus = Field(default=FlextWebAppStatus.STOPPED, description="App status")
    config: dict[str, Any] = Field(
        default_factory=dict, description="App configuration",
    )
    routes: list[str] = Field(
        default_factory=list, description="List of registered routes",
    )
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp",
    )

    def is_valid(self) -> bool:
        """Validate web app entity state.

        Returns:
            True if web app is valid, False otherwise

        """
        return bool(self.name and 1 <= self.port <= 65535)

    def is_running(self) -> bool:
        """Check if web app is running.

        Returns:
            True if app is running, False otherwise

        """
        return self.status == FlextWebAppStatus.RUNNING

    def start(self) -> bool:
        """Mark app as starting.

        Returns:
            True if state change successful, False otherwise

        """
        if self.status == FlextWebAppStatus.STOPPED:
            object.__setattr__(self, "status", FlextWebAppStatus.STARTING)
            return True
        return False

    def mark_running(self) -> bool:
        """Mark app as running.

        Returns:
            True if state change successful, False otherwise

        """
        if self.status == FlextWebAppStatus.STARTING:
            object.__setattr__(self, "status", FlextWebAppStatus.RUNNING)
            return True
        return False

    def stop(self) -> bool:
        """Mark app as stopping.

        Returns:
            True if state change successful, False otherwise

        """
        if self.status == FlextWebAppStatus.RUNNING:
            object.__setattr__(self, "status", FlextWebAppStatus.STOPPING)
            return True
        return False

    def mark_stopped(self) -> bool:
        """Mark app as stopped.

        Returns:
            True if state change successful, False otherwise

        """
        if self.status == FlextWebAppStatus.STOPPING:
            object.__setattr__(self, "status", FlextWebAppStatus.STOPPED)
            return True
        return False

    def validate_domain_rules(self) -> None:
        """Validate domain rules for web app entity.

        Raises:
            ValueError: If domain rules are violated

        """
        if not self.name.strip():
            msg = "Web app name cannot be empty"
            raise ValueError(msg)
        if not (1 <= self.port <= 65535):
            msg = "Port must be between 1 and 65535"
            raise ValueError(msg)
        if not self.host.strip():
            msg = "Host cannot be empty"
            raise ValueError(msg)

    def get_url(self) -> str:
        """Get web app URL.

        Returns:
            Web app URL as http://host:port

        """
        return f"http://{self.host}:{self.port}"

    def add_route(self, route: str) -> bool:
        """Add a route to the web app.

        Args:
            route: Route to add

        Returns:
            True if route was added, False if already exists

        """
        if route not in self.routes:
            self.routes.append(route)
            return True
        return False


# TODO: Refactored to use FlextEntity pattern
class FlextDashboard(FlextEntity):
    """Dashboard entity representing a web dashboard."""

    entity_id: str = Field(..., description="Unique entity identifier")
    title: str = Field(..., description="Dashboard title")
    description: str = Field(default="", description="Dashboard description")
    widgets: list[dict[str, Any]] = Field(
        default_factory=list, description="List of dashboard widgets",
    )
    layout: dict[str, Any] = Field(
        default_factory=dict, description="Dashboard layout configuration",
    )
    is_public: bool = Field(
        default=False, description="Whether dashboard is publicly accessible",
    )
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp",
    )

    def is_valid(self) -> bool:
        """Validate dashboard entity state.

        Returns:
            True if dashboard is valid, False otherwise

        """
        return bool(self.title)

    def add_widget(self, widget: dict[str, Any]) -> bool:
        """Add a widget to the dashboard.

        Args:
            widget: Widget configuration to add

        Returns:
            True if widget was added, False otherwise

        """
        if widget and "id" in widget:
            # Check if widget with same ID already exists
            if not any(w.get("id") == widget["id"] for w in self.widgets):
                self.widgets.append(widget)
                return True
        return False

    def remove_widget(self, widget_id: str) -> bool:
        """Remove a widget from the dashboard.

        Args:
            widget_id: ID of widget to remove

        Returns:
            True if widget was removed, False if not found

        """
        original_count = len(self.widgets)
        filtered_widgets = [w for w in self.widgets if w.get("id") != widget_id]
        object.__setattr__(self, "widgets", filtered_widgets)
        return len(self.widgets) < original_count

    def get_widget_count(self) -> int:
        """Get number of widgets in dashboard.

        Returns:
            Number of widgets

        """
        return len(self.widgets)

    def validate_domain_rules(self) -> None:
        """Validate domain rules for dashboard entity.

        Raises:
            ValueError: If domain rules are violated

        """
        if not self.title.strip():
            msg = "Dashboard title cannot be empty"
            raise ValueError(msg)


# TODO: Refactored to use FlextEntity pattern
class FlextTemplate(FlextEntity):
    """Template entity representing a web template."""

    entity_id: str = Field(..., description="Unique entity identifier")
    name: str = Field(..., description="Template name")
    content: str = Field(..., description="Template content")
    template_type: FlextTemplateType = Field(
        default=FlextTemplateType.PAGE, description="Type of template",
    )
    variables: list[str] = Field(
        default_factory=list, description="List of template variables",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Template metadata",
    )
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp",
    )

    def is_valid(self) -> bool:
        """Validate template entity state.

        Returns:
            True if template is valid, False otherwise

        """
        return bool(self.name and self.content)

    def render(self, context: dict[str, Any] | None = None) -> str:
        """Render template with context.

        Args:
            context: Template context variables

        Returns:
            Rendered template content

        """
        if not context:
            return self.content

        # Simple variable substitution
        rendered = self.content
        for key, value in context.items():
            placeholder = f"{{{{{key}}}}}"
            rendered = rendered.replace(placeholder, str(value))

        return rendered

    def extract_variables(self) -> list[str]:
        """Extract variables from template content.

        Returns:
            List of variable names found in template

        """
        import re

        # Find all {{variable}} patterns
        pattern = r"\{\{(\w+)\}\}"
        matches = re.findall(pattern, self.content)
        return list(set(matches))

    def validate_domain_rules(self) -> None:
        """Validate domain rules for template entity.

        Raises:
            ValueError: If domain rules are violated

        """
        if not self.name.strip():
            msg = "Template name cannot be empty"
            raise ValueError(msg)
        if not self.content.strip():
            msg = "Template content cannot be empty"
            raise ValueError(msg)


# TODO: Refactored to use FlextEntity pattern
class FlextResponse(FlextEntity):
    """Response entity representing an HTTP response."""

    entity_id: str = Field(..., description="Unique entity identifier")
    status_code: int = Field(
        default=200, ge=100, le=599, description="HTTP status code",
    )
    content: str = Field(default="", description="Response content")
    headers: dict[str, str] = Field(default_factory=dict, description="HTTP headers")
    content_type: str = Field(default="text/html", description="Content type")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp",
    )

    def model_post_init(self, /, __context: Any) -> None:
        """Post-initialization hook to set default headers."""
        # Set default content-type header
        if "Content-Type" not in self.headers:
            self.headers["Content-Type"] = self.content_type

    def is_valid(self) -> bool:
        """Validate response entity state.

        Returns:
            True if response is valid, False otherwise

        """
        return bool(100 <= self.status_code <= 599)

    def is_success(self) -> bool:
        """Check if response indicates success.

        Returns:
            True if status code is 2xx, False otherwise

        """
        return 200 <= self.status_code <= 299

    def is_error(self) -> bool:
        """Check if response indicates error.

        Returns:
            True if status code is 4xx or 5xx, False otherwise

        """
        return self.status_code >= 400

    def set_header(self, name: str, value: str) -> None:
        """Set a response header.

        Args:
            name: Header name
            value: Header value

        """
        self.headers[name] = value

    def get_content_length(self) -> int:
        """Get content length.

        Returns:
            Length of content in bytes

        """
        return len(self.content.encode("utf-8"))

    def validate_domain_rules(self) -> None:
        """Validate domain rules for response entity.

        Raises:
            ValueError: If domain rules are violated

        """
        if not (100 <= self.status_code <= 599):
            msg = "Status code must be between 100 and 599"
            raise ValueError(msg)
        if not self.content_type.strip():
            msg = "Content type cannot be empty"
            raise ValueError(msg)


# Backwards compatibility aliases
WebApp = FlextWebApp
Dashboard = FlextDashboard
Template = FlextTemplate
Response = FlextResponse
