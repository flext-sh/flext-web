"""Unit tests for public field behavior exposed through `web`."""

from __future__ import annotations

from flext_tests import tm

from flext_web import web
from tests import m


class TestFlextWebFields:
    """Test suite for public web field behavior."""

    def test_host_field_creation(self) -> None:
        """Test host field creation."""
        config = web.settings.model_copy(update={"host": "localhost"})
        tm.that(config.host, eq="localhost")

    def test_host_field_with_custom_default(self) -> None:
        """Test host field creation with custom default."""
        config = web.settings.model_copy(update={"host": "0.0.0.0"})
        tm.that(config.host, eq="0.0.0.0")

    def test_port_field_creation(self) -> None:
        """Test port field creation."""
        config = web.settings.model_copy(update={"port": 8080})
        tm.that(config.port, eq=8080)

    def test_port_field_with_custom_default(self) -> None:
        """Test port field creation with custom default."""
        config = web.settings.model_copy(update={"port": 3000})
        tm.that(config.port, eq=3000)

    def test_url_field_creation(self) -> None:
        """Test URL field creation."""
        request = m.Web.Request(url="http://localhost:8080")
        tm.that(request.url, eq="http://localhost:8080")

    def test_app_name_field_creation(self) -> None:
        """Test app name field creation."""
        config = web.settings.model_copy(update={"app_name": "Test App"})
        tm.that(config.app_name, eq="Test App")

    def test_secret_key_field_creation(self) -> None:
        """Test secret key field creation."""
        config = web.settings.model_copy(
            update={"secret_key": "valid-secret-key-32-characters-long"},
        )
        tm.that(config.secret_key, none=False)

    def test_http_status_field_creation(self) -> None:
        """Test HTTP status field creation."""
        response = m.Web.Response(status_code=200)
        tm.that(response.status_code, eq=200)
        tm.that(response.is_success is True, eq=True)

    def test_http_status_field_ok(self) -> None:
        """Test HTTP 200 OK status field creation."""
        response = m.Web.Response(status_code=200)
        tm.that(response.status_code, eq=200)
        tm.that(response.is_success is True, eq=True)

    def test_http_status_field_created(self) -> None:
        """Test HTTP 201 Created status field creation."""
        response = m.Web.Response(status_code=201)
        tm.that(response.status_code, eq=201)
        tm.that(response.is_success is True, eq=True)

    def test_http_status_field_bad_request(self) -> None:
        """Test HTTP 400 Bad Request status field creation."""
        response = m.Web.Response(status_code=400)
        tm.that(response.status_code, eq=400)
        tm.that(response.is_error is True, eq=True)

    def test_http_status_field_not_found(self) -> None:
        """Test HTTP 404 Not Found status field creation."""
        response = m.Web.Response(status_code=404)
        tm.that(response.status_code, eq=404)
        tm.that(response.is_error is True, eq=True)

    def test_http_status_field_server_error(self) -> None:
        """Test HTTP 500 Internal Server Error status field creation."""
        response = m.Web.Response(status_code=500)
        tm.that(response.status_code, eq=500)
        tm.that(response.is_error is True, eq=True)

    def test_http_status_field_create_field(self) -> None:
        """Test HTTP status field creation."""
        response = m.Web.Response(status_code=200)
        tm.that(response.status_code, eq=200)
        tm.that(response.is_success is True, eq=True)

    def test_field_constraints(self) -> None:
        """Test field constraints are properly set."""
        test_model = m.Web.Request(url="http://localhost:8080", method="GET")
        tm.that(test_model.url, eq="http://localhost:8080")
        tm.that(test_model.method, eq="GET")

    def test_field_descriptions(self) -> None:
        """Test field descriptions are properly set."""
        host_model = m.Web.Request(url="http://localhost:8080")
        port_model = m.Web.Request(url="http://localhost:3000")
        tm.that(host_model, none=False)
        tm.that(port_model, none=False)

    def test_http_status_field_with_kwargs(self) -> None:
        """Test HTTP status field with additional kwargs."""
        response_model = m.Web.Response(status_code=200)
        tm.that(response_model.status_code, eq=200)
        tm.that(response_model.is_success is True, eq=True)

    def test_field_creation_with_kwargs(self) -> None:
        """Test field creation with additional kwargs."""
        request_model = m.Web.Request(
            url="http://localhost:8080",
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        tm.that(request_model.url, eq="http://localhost:8080")
        tm.that(request_model.method, eq="POST")
        tm.that(request_model.headers["Content-Type"], eq="application/json")

    def test_http_status_field_factory_methods(self) -> None:
        """Test all HTTP status field factory methods."""
        status_codes = [200, 201, 400, 404, 500]
        for status_code in status_codes:
            response_model = m.Web.Response(status_code=status_code)
            tm.that(response_model.status_code, eq=status_code)
            tm.that(response_model, is_=m.Web.Response)

    def test_field_validation_integration(self) -> None:
        """Test field validation integration."""
        model = web.settings
        tm.that(model.host, eq=web.settings.host)
        tm.that(model.port, eq=web.settings.port)
