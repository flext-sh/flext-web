"""FLEXT Web Simple API - Factory functions for web components.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Simple factory functions for creating web interface components.
"""

from __future__ import annotations

import uuid
from typing import Any

from flext_core import FlextResult

from flext_web.domain.entities import (
    FlextDashboard,
    FlextResponse,
    FlextTemplate,
    FlextTemplateType,
    FlextWebApp,
    FlextWebAppStatus,
)


def create_flext_web_app(
    name: str,
    host: str = "localhost",
    port: int = 8000,
    config: dict[str, Any] | None = None,
) -> FlextWebApp:
    """Create a new FLEXT web application.

    Args:
        name: Application name
        host: Host address
        port: Port number
        config: Application configuration

    Returns:
        FlextWebApp instance

    """
    return FlextWebApp(
        entity_id=str(uuid.uuid4()),
        name=name,
        host=host,
        port=port,
        status=FlextWebAppStatus.STOPPED,
        config=config or {},
    )


def create_flext_dashboard(
    title: str,
    description: str = "",
    is_public: bool = False,
    widgets: list[dict[str, Any]] | None = None,
) -> FlextDashboard:
    """Create a new FLEXT dashboard.

    Args:
        title: Dashboard title
        description: Dashboard description
        is_public: Whether dashboard is public
        widgets: Initial widgets

    Returns:
        FlextDashboard instance

    """
    return FlextDashboard(
        entity_id=str(uuid.uuid4()),
        title=title,
        description=description,
        is_public=is_public,
        widgets=widgets or [],
    )


def create_flext_template(
    name: str,
    content: str,
    template_type: str = "page",
    variables: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> FlextTemplate:
    """Create a new FLEXT template.

    Args:
        name: Template name
        content: Template content
        template_type: Type of template
        variables: Template variables
        metadata: Template metadata

    Returns:
        FlextTemplate instance

    """
    # Convert string to enum
    try:
        template_type_enum = FlextTemplateType(template_type)
    except ValueError:
        template_type_enum = FlextTemplateType.PAGE

    return FlextTemplate(
        entity_id=str(uuid.uuid4()),
        name=name,
        content=content,
        template_type=template_type_enum,
        variables=variables or [],
        metadata=metadata or {},
    )


def create_flext_response(
    content: str,
    status_code: int = 200,
    headers: dict[str, str] | None = None,
    content_type: str = "text/html",
) -> FlextResponse:
    """Create a new FLEXT HTTP response.

    Args:
        content: Response content
        status_code: HTTP status code
        headers: Response headers
        content_type: Content type

    Returns:
        FlextResponse instance

    """
    return FlextResponse(
        entity_id=str(uuid.uuid4()),
        status_code=status_code,
        content=content,
        headers=headers or {},
        content_type=content_type,
    )


def create_success_response(content: str) -> FlextResponse:
    """Create a success response (200 OK).

    Args:
        content: Response content

    Returns:
        FlextResponse instance with 200 status

    """
    return create_flext_response(content, 200)


def create_error_response(message: str, status_code: int = 500) -> FlextResponse:
    """Create an error response.

    Args:
        message: Error message
        status_code: HTTP error status code

    Returns:
        FlextResponse instance with error status

    """
    return create_flext_response(
        f"<html><body><h1>Error {status_code}</h1><p>{message}</p></body></html>",
        status_code,
        content_type="text/html",
    )


def create_json_response(data: dict[str, Any], status_code: int = 200) -> FlextResponse:
    """Create a JSON response.

    Args:
        data: Data to serialize as JSON
        status_code: HTTP status code

    Returns:
        FlextResponse instance with JSON content

    """
    import json

    return create_flext_response(
        json.dumps(data),
        status_code,
        content_type="application/json",
    )


def start_web_app(app: FlextWebApp) -> FlextResult[bool]:
    """Start a web application.

    Args:
        app: Web app to start

    Returns:
        FlextResult indicating success

    """
    if app.start():
        app.mark_running()
        return FlextResult.ok(True)
    return FlextResult.fail("Application is not in a startable state")


def stop_web_app(app: FlextWebApp) -> FlextResult[bool]:
    """Stop a web application.

    Args:
        app: Web app to stop

    Returns:
        FlextResult indicating success

    """
    if app.stop():
        app.mark_stopped()
        return FlextResult.ok(True)
    return FlextResult.fail("Application is not in a stoppable state")


def add_dashboard_widget(
    dashboard: FlextDashboard,
    widget_id: str,
    widget_type: str,
    config: dict[str, Any] | None = None,
) -> FlextResult[bool]:
    """Add a widget to dashboard.

    Args:
        dashboard: Dashboard to add widget to
        widget_id: Unique widget ID
        widget_type: Type of widget
        config: Widget configuration

    Returns:
        FlextResult indicating success

    """
    widget = {
        "id": widget_id,
        "type": widget_type,
        "config": config or {},
    }

    if dashboard.add_widget(widget):
        return FlextResult.ok(True)
    return FlextResult.fail("Widget with this ID already exists")


def render_template_with_context(
    template: FlextTemplate,
    context: dict[str, Any],
) -> FlextResult[str]:
    """Render template with context variables.

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


# Backwards compatibility aliases
create_web_app = create_flext_web_app
create_dashboard = create_flext_dashboard
create_template = create_flext_template
create_response = create_flext_response
