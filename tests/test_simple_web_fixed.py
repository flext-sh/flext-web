"""Tests for simple_web module."""

from __future__ import annotations


class TestSimpleWebFunctions:
    """Test simple web utility functions."""

    def test_create_response(self) -> None:
        """Test create_response function."""
        from flext_web.simple_web import create_response

        data = {"test": "value"}
        response = create_response(data)

        assert response["data"] == data
        assert response["status"] == 200
        assert response["success"] is True

    def test_create_response_with_status_code(self) -> None:
        """Test create_response with custom status code."""
        from flext_web.simple_web import create_response

        data = {"test": "value"}
        response = create_response(data, 201)

        assert response["data"] == data
        assert response["status"] == 201
        assert response["success"] is True

    def test_create_response_error_status(self) -> None:
        """Test create_response with error status code."""
        from flext_web.simple_web import create_response

        data = {"test": "value"}
        response = create_response(data, 500)

        assert response["data"] == data
        assert response["status"] == 500
        assert response["success"] is False

    def test_create_success_response(self) -> None:
        """Test create_success_response function."""
        from flext_web.simple_web import create_success_response

        data = {"result": "success"}
        message = "Operation completed"
        response = create_success_response(data, message)

        assert response["data"] == data
        assert response["message"] == message
        assert response["status"] == 200
        assert response["success"] is True

    def test_create_success_response_default_message(self) -> None:
        """Test create_success_response with default message."""
        from flext_web.simple_web import create_success_response

        data = {"result": "success"}
        response = create_success_response(data)

        assert response["data"] == data
        assert response["message"] == "Success"
        assert response["status"] == 200
        assert response["success"] is True

    def test_create_error_response(self) -> None:
        """Test create_error_response function."""
        from flext_web.simple_web import create_error_response

        error_message = "Something went wrong"
        response = create_error_response(error_message, 400)

        assert response["error"] == error_message
        assert response["status"] == 400
        assert response["success"] is False

    def test_create_error_response_default_status(self) -> None:
        """Test create_error_response with default status."""
        from flext_web.simple_web import create_error_response

        error_message = "Something went wrong"
        response = create_error_response(error_message)

        assert response["error"] == error_message
        assert response["status"] == 400
        assert response["success"] is False

    def test_validate_request_data_success(self) -> None:
        """Test validate_request_data with valid data."""
        from flext_web.simple_web import validate_request_data

        data = {"name": "test", "value": 123}
        required_fields = ["name", "value"]

        result = validate_request_data(data, required_fields)

        assert result.success is True
        assert result.data is True

    def test_validate_request_data_missing_field(self) -> None:
        """Test validate_request_data with missing field."""
        from flext_web.simple_web import validate_request_data

        data = {"name": "test"}
        required_fields = ["name", "value"]

        result = validate_request_data(data, required_fields)

        assert result.success is False
        assert "value" in (result.error or "")

    def test_validate_request_data_empty_required(self) -> None:
        """Test validate_request_data with empty required fields."""
        from flext_web.simple_web import validate_request_data

        data = {"name": "test"}
        result = validate_request_data(data, [])

        assert result.success is True

    def test_format_pagination(self) -> None:
        """Test format_pagination function."""
        from flext_web.simple_web import format_pagination

        pagination = format_pagination(page=2, page_size=10, total=25)

        assert pagination["page"] == 2
        assert pagination["page_size"] == 10
        assert pagination["total"] == 25
        assert pagination["total_pages"] == 3
        assert pagination["has_next"] is True
        assert pagination["has_previous"] is True

    def test_format_pagination_first_page(self) -> None:
        """Test format_pagination for first page."""
        from flext_web.simple_web import format_pagination

        pagination = format_pagination(page=1, page_size=10, total=25)

        assert pagination["has_next"] is True
        assert pagination["has_previous"] is False

    def test_format_pagination_last_page(self) -> None:
        """Test format_pagination for last page."""
        from flext_web.simple_web import format_pagination

        pagination = format_pagination(page=3, page_size=10, total=25)

        assert pagination["has_next"] is False
        assert pagination["has_previous"] is True

    def test_simple_template_render_success(self) -> None:
        """Test SimpleTemplate render with valid context."""
        from flext_web.simple_web import FlextSimpleTemplate

        template = FlextSimpleTemplate("Hello, {name}!")
        result = template.render({"name": "World"})

        assert result.success is True
        assert result.data == "Hello, World!"

    def test_simple_template_render_missing_variable(self) -> None:
        """Test SimpleTemplate render with missing variable."""
        from flext_web.simple_web import FlextSimpleTemplate

        template = FlextSimpleTemplate("Hello, {name}!")
        result = template.render({})

        assert result.success is False
        assert "Missing template variable" in (result.error or "")

    def test_create_template(self) -> None:
        """Test create_template factory function."""
        from flext_web.simple_web import FlextSimpleTemplate, create_template

        template = create_template("Test template: {value}")

        assert isinstance(template, FlextSimpleTemplate)
        assert template.template == "Test template: {value}"
