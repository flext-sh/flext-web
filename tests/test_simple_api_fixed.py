"""Tests for simple_api factory functions."""

from __future__ import annotations

from flext_web.domain.entities import (
    FlextDashboard,
    FlextResponse,
    FlextTemplate,
    FlextTemplateType,
    FlextWebApp,
    FlextWebAppStatus,
)
from flext_web.simple_api import (
    create_flext_dashboard,
    create_flext_response,
    create_flext_template,
    create_flext_web_app,
)


class TestSimpleAPIFactories:
    """Test simple API factory functions."""

    def test_create_flext_web_app_default(self) -> None:
        """Test create_flext_web_app with default parameters."""
        app = create_flext_web_app("test-app")

        assert isinstance(app, FlextWebApp)
        assert app.name == "test-app"
        assert app.status == FlextWebAppStatus.STOPPED
        assert app.host == "localhost"
        assert app.port == 8000

    def test_create_flext_web_app_custom(self) -> None:
        """Test create_flext_web_app with custom parameters."""
        config = {"debug": True}
        app = create_flext_web_app(
            "custom-app",
            host="0.0.0.0",
            port=9000,
            config=config,
        )

        assert isinstance(app, FlextWebApp)
        assert app.name == "custom-app"
        assert app.host == "0.0.0.0"
        assert app.port == 9000
        assert app.config == config

    def test_create_flext_template_default(self) -> None:
        """Test create_flext_template with default parameters."""
        content = "<html><body>{{ title }}</body></html>"
        template = create_flext_template("test-template", content)

        assert isinstance(template, FlextTemplate)
        assert template.name == "test-template"
        assert template.content == content
        assert template.template_type == FlextTemplateType.PAGE

    def test_create_flext_template_custom(self) -> None:
        """Test create_flext_template with custom parameters."""
        content = "{{ name }}: {{ value }}"
        variables = ["name", "value"]
        template = create_flext_template(
            "custom-template",
            content,
            template_type=FlextTemplateType.COMPONENT,
            variables=variables,
        )

        assert isinstance(template, FlextTemplate)
        assert template.template_type == FlextTemplateType.COMPONENT
        assert template.variables == variables

    def test_create_flext_dashboard_default(self) -> None:
        """Test create_flext_dashboard with default parameters."""
        dashboard = create_flext_dashboard("test-dashboard")

        assert isinstance(dashboard, FlextDashboard)
        assert dashboard.title == "test-dashboard"
        assert dashboard.widgets == []

    def test_create_flext_dashboard_with_widgets(self) -> None:
        """Test create_flext_dashboard with widgets."""
        widgets = [
            {"type": "chart", "title": "Chart 1"},
            {"type": "table", "title": "Table 1"},
        ]
        dashboard = create_flext_dashboard("dashboard-with-widgets", widgets=widgets)

        assert isinstance(dashboard, FlextDashboard)
        assert dashboard.widgets == widgets

    def test_create_flext_response_default(self) -> None:
        """Test create_flext_response with default parameters."""
        content = "Hello, World!"
        response = create_flext_response(content)

        assert isinstance(response, FlextResponse)
        assert response.content == content
        assert response.status_code == 200
        assert response.content_type == "text/html"

    def test_create_flext_response_custom(self) -> None:
        """Test create_flext_response with custom parameters."""
        content = '{"message": "success"}'
        headers = {"X-Custom": "value"}
        response = create_flext_response(
            content,
            status_code=201,
            content_type="application/json",
            headers=headers,
        )

        assert isinstance(response, FlextResponse)
        assert response.content == content
        assert response.status_code == 201
        assert response.content_type == "application/json"
        assert "X-Custom" in response.headers
        assert response.headers["X-Custom"] == "value"
