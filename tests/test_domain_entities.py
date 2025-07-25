"""Tests for FlextWeb domain entities."""

from __future__ import annotations

import uuid

from flext_web.domain.entities import (
    FlextDashboard,
    FlextResponse,
    FlextTemplate,
    FlextTemplateType,
    FlextWebApp,
    FlextWebAppStatus,
)


class TestFlextWebApp:
    """Test FlextWebApp entity."""

    def test_webapp_creation(self) -> None:
        """Test FlextWebApp creation with valid data."""
        app = FlextWebApp(
            entity_id=str(uuid.uuid4()),
            name="test-app",
            host="localhost",
            port=8080,
            status=FlextWebAppStatus.STOPPED,
        )

        assert app.is_valid()
        assert app.name == "test-app"
        assert app.port == 8080
        assert app.status == FlextWebAppStatus.STOPPED

    def test_webapp_state_transitions(self) -> None:
        """Test FlextWebApp state transitions."""
        app = FlextWebApp(
            entity_id=str(uuid.uuid4()),
            name="test-app",
            status=FlextWebAppStatus.STOPPED,
        )

        # Start transition
        start_result = app.start()
        assert start_result
        assert app.status == FlextWebAppStatus.STARTING

        # Mark running
        running_result = app.mark_running()
        assert running_result
        # Force type check bypass by casting
        assert app.status.value == FlextWebAppStatus.RUNNING.value
        assert app.is_running()

        # Stop transition
        stop_result = app.stop()
        assert stop_result
        assert app.status.value == FlextWebAppStatus.STOPPING.value

        # Mark stopped
        stopped_result = app.mark_stopped()
        assert stopped_result
        assert app.status.value == FlextWebAppStatus.STOPPED.value


class TestFlextDashboard:
    """Test FlextDashboard entity."""

    def test_dashboard_creation(self) -> None:
        """Test FlextDashboard creation with valid data."""
        dashboard = FlextDashboard(
            entity_id=str(uuid.uuid4()),
            title="Test Dashboard",
            description="A test dashboard",
            is_public=True,
        )

        assert dashboard.is_valid()
        assert dashboard.title == "Test Dashboard"
        assert dashboard.is_public is True

    def test_dashboard_widget_management(self) -> None:
        """Test FlextDashboard widget management."""
        dashboard = FlextDashboard(
            entity_id=str(uuid.uuid4()),
            title="Test Dashboard",
        )

        widget = {"id": "widget1", "type": "chart", "config": {}}

        # Add widget
        assert dashboard.add_widget(widget)
        assert dashboard.get_widget_count() == 1

        # Try to add duplicate widget
        assert not dashboard.add_widget(widget)
        assert dashboard.get_widget_count() == 1

        # Remove widget
        assert dashboard.remove_widget("widget1")
        assert dashboard.get_widget_count() == 0


class TestFlextTemplate:
    """Test FlextTemplate entity."""

    def test_template_creation(self) -> None:
        """Test FlextTemplate creation with valid data."""
        template = FlextTemplate(
            entity_id=str(uuid.uuid4()),
            name="test-template",
            content="Hello {{name}}!",
            template_type=FlextTemplateType.PAGE,
        )

        assert template.is_valid()
        assert template.name == "test-template"
        assert template.template_type == FlextTemplateType.PAGE

    def test_template_rendering(self) -> None:
        """Test FlextTemplate rendering with context."""
        template = FlextTemplate(
            entity_id=str(uuid.uuid4()),
            name="greeting",
            content="Hello {{name}}, welcome to {{app}}!",
        )

        context = {"name": "John", "app": "FlextWeb"}
        rendered = template.render(context)

        assert rendered == "Hello John, welcome to FlextWeb!"

    def test_template_variable_extraction(self) -> None:
        """Test FlextTemplate variable extraction."""
        template = FlextTemplate(
            entity_id=str(uuid.uuid4()),
            name="vars-test",
            content="{{user}} has {{count}} items in {{category}}",
        )

        variables = template.extract_variables()
        assert set(variables) == {"user", "count", "category"}


class TestFlextResponse:
    """Test FlextResponse entity."""

    def test_response_creation(self) -> None:
        """Test FlextResponse creation with valid data."""
        response = FlextResponse(
            entity_id=str(uuid.uuid4()),
            status_code=200,
            content="<h1>Success</h1>",
            content_type="text/html",
        )

        assert response.is_valid()
        assert response.status_code == 200
        assert response.is_success()
        assert not response.is_error()

    def test_response_status_checks(self) -> None:
        """Test FlextResponse status checks."""
        # Success response
        success_response = FlextResponse(
            entity_id=str(uuid.uuid4()),
            status_code=201,
        )
        assert success_response.is_success()
        assert not success_response.is_error()

        # Error response
        error_response = FlextResponse(
            entity_id=str(uuid.uuid4()),
            status_code=404,
        )
        assert not error_response.is_success()
        assert error_response.is_error()

    def test_response_headers(self) -> None:
        """Test FlextResponse header management."""
        response = FlextResponse(
            entity_id=str(uuid.uuid4()),
            content_type="application/json",
        )

        # Check default content-type header is set
        assert response.headers["Content-Type"] == "application/json"

        # Set custom header
        response.set_header("X-Custom", "test-value")
        assert response.headers["X-Custom"] == "test-value"

    def test_response_content_length(self) -> None:
        """Test FlextResponse content length calculation."""
        response = FlextResponse(
            entity_id=str(uuid.uuid4()),
            content="Hello World",
        )

        assert response.get_content_length() == len(b"Hello World")
