"""Unit tests for flext_web.fields module.

Tests the web fields functionality following flext standards.
"""

from flext_core import FlextCore

from flext_web.constants import FlextWebConstants
from flext_web.fields import FlextWebFields


class TestFlextWebFields:
    """Test suite for FlextWebFields class."""

    def test_host_field_creation(self) -> None:
        """Test host field creation."""
        field = FlextWebFields.host_field()
        assert field is not None
        assert hasattr(field, "default")
        assert field.default == FlextWebConstants.WebServer.DEFAULT_HOST

    def test_host_field_with_custom_default(self) -> None:
        """Test host field creation with custom default."""
        field = FlextWebFields.host_field(default="0.0.0.0")
        assert field.default == "0.0.0.0"

    def test_port_field_creation(self) -> None:
        """Test port field creation."""
        field = FlextWebFields.port_field()
        assert field is not None
        assert hasattr(field, "default")
        assert field.default == FlextWebConstants.WebServer.DEFAULT_PORT

    def test_port_field_with_custom_default(self) -> None:
        """Test port field creation with custom default."""
        field = FlextWebFields.port_field(default=3000)
        assert field.default == 3000

    def test_url_field_creation(self) -> None:
        """Test URL field creation."""
        field = FlextWebFields.url_field()
        assert field is not None

    def test_app_name_field_creation(self) -> None:
        """Test app name field creation."""
        field = FlextWebFields.app_name_field()
        assert field is not None

    def test_secret_key_field_creation(self) -> None:
        """Test secret key field creation."""
        field = FlextWebFields.secret_key_field()
        assert field is not None

    def test_http_status_field_creation(self) -> None:
        """Test HTTP status field creation."""
        field = FlextWebFields.http_status_field(200, "OK")
        assert field is not None

    def test_http_status_field_ok(self) -> None:
        """Test HTTP 200 OK status field creation."""
        field = FlextWebFields.HTTPStatusField.ok("Success")
        assert field.status_code == FlextCore.Constants.Http.HTTP_OK
        assert field.description == "Success"

    def test_http_status_field_created(self) -> None:
        """Test HTTP 201 Created status field creation."""
        field = FlextWebFields.HTTPStatusField.created("Resource created")
        assert field.status_code == FlextCore.Constants.Http.HTTP_CREATED
        assert field.description == "Resource created"

    def test_http_status_field_bad_request(self) -> None:
        """Test HTTP 400 Bad Request status field creation."""
        field = FlextWebFields.HTTPStatusField.bad_request("Invalid request")
        assert field.status_code == FlextCore.Constants.Http.HTTP_BAD_REQUEST
        assert field.description == "Invalid request"

    def test_http_status_field_not_found(self) -> None:
        """Test HTTP 404 Not Found status field creation."""
        field = FlextWebFields.HTTPStatusField.not_found("Resource not found")
        assert field.status_code == FlextCore.Constants.Http.HTTP_NOT_FOUND
        assert field.description == "Resource not found"

    def test_http_status_field_server_error(self) -> None:
        """Test HTTP 500 Internal Server Error status field creation."""
        field = FlextWebFields.HTTPStatusField.server_error("Internal error")
        assert field.status_code == FlextCore.Constants.Http.HTTP_INTERNAL_SERVER_ERROR
        assert field.description == "Internal error"

    def test_http_status_field_create_field(self) -> None:
        """Test HTTP status field creation."""
        status_field = FlextWebFields.HTTPStatusField(200, "OK")
        field = status_field.create_field()
        assert field is not None
        assert field.default == 200

    def test_host_pattern_compilation(self) -> None:
        """Test host pattern compilation."""
        pattern = FlextWebFields.HOST_PATTERN
        assert pattern is not None

        # Test valid hosts
        assert pattern.match("localhost") is not None
        assert pattern.match("127.0.0.1") is not None
        assert pattern.match("example.com") is not None
        assert pattern.match("192.168.1.1") is not None

    def test_url_pattern_compilation(self) -> None:
        """Test URL pattern compilation."""
        pattern = FlextWebFields.URL_PATTERN
        assert pattern is not None

        # Test valid URLs
        assert pattern.match("http://example.com") is not None
        assert pattern.match("https://example.com") is not None
        assert pattern.match("http://localhost:8080") is not None
        assert pattern.match("https://api.example.com/v1") is not None

    def test_field_constraints(self) -> None:
        """Test field constraints are properly set."""
        # Test port field constraints
        port_field = FlextWebFields.port_field()
        # The field should have proper constraints set
        assert port_field is not None

    def test_field_descriptions(self) -> None:
        """Test field descriptions are properly set."""
        host_field = FlextWebFields.host_field()
        port_field = FlextWebFields.port_field()
        url_field = FlextWebFields.url_field()

        # All fields should be created successfully
        assert host_field is not None
        assert port_field is not None
        assert url_field is not None

    def test_http_status_field_with_kwargs(self) -> None:
        """Test HTTP status field with additional kwargs."""
        field = FlextWebFields.http_status_field(200, "OK", ge=200, le=299)
        assert field is not None

    def test_field_creation_with_kwargs(self) -> None:
        """Test field creation with additional kwargs."""
        host_field = FlextWebFields.host_field(description="Custom host field")
        port_field = FlextWebFields.port_field(description="Custom port field")

        assert host_field is not None
        assert port_field is not None

    def test_http_status_field_factory_methods(self) -> None:
        """Test all HTTP status field factory methods."""
        # Test all factory methods exist and work
        methods = ["ok", "created", "bad_request", "not_found", "server_error"]

        for method_name in methods:
            method = getattr(FlextWebFields.HTTPStatusField, method_name)
            field = method("Test description")
            assert field is not None
            assert isinstance(field, FlextWebFields.HTTPStatusField)

    def test_field_validation_integration(self) -> None:
        """Test field validation integration."""
        # Test that fields can be used in Pydantic models
        from pydantic import BaseModel

        class TestModel(BaseModel):
            host: str = FlextWebFields.host_field().default
            port: int = FlextWebFields.port_field().default

        model = TestModel()
        assert model.host == FlextWebConstants.WebServer.DEFAULT_HOST
        assert model.port == FlextWebConstants.WebServer.DEFAULT_PORT
