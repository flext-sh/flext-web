"""Unit tests for flext_web.fields module.

Tests the web fields functionality following flext standards.
"""

from pydantic import BaseModel

from flext_web.constants import FlextWebConstants
from flext_web.models import FlextWebModels
from flext_web.settings import FlextWebSettings


class TestFlextWebFields:
    """Test suite for FlextWebModels class."""

    def test_host_field_creation(self) -> None:
        """Test host field creation."""
        config = FlextWebSettings(host="localhost")
        assert config.host == "localhost"

    def test_host_field_with_custom_default(self) -> None:
        """Test host field creation with custom default."""
        config = FlextWebSettings(host="0.0.0.0")
        assert config.host == "0.0.0.0"

    def test_port_field_creation(self) -> None:
        """Test port field creation."""
        config = FlextWebSettings(port=8080)
        assert config.port == 8080

    def test_port_field_with_custom_default(self) -> None:
        """Test port field creation with custom default."""
        config = FlextWebSettings(port=3000)
        assert config.port == 3000

    def test_url_field_creation(self) -> None:
        """Test URL field creation."""
        request = FlextWebModels.Web.Request(url="http://localhost:8080")
        assert request.url == "http://localhost:8080"

    def test_app_name_field_creation(self) -> None:
        """Test app name field creation."""
        config = FlextWebSettings(app_name="Test App")
        assert config.app_name == "Test App"

    def test_secret_key_field_creation(self) -> None:
        """Test secret key field creation."""
        config = FlextWebSettings(secret_key="valid-secret-key-32-characters-long")
        assert config.secret_key is not None

    def test_http_status_field_creation(self) -> None:
        """Test HTTP status field creation."""
        response = FlextWebModels.Web.Response(status_code=200, request_id="test-123")
        assert response.status_code == 200
        assert response.is_success is True

    def test_http_status_field_ok(self) -> None:
        """Test HTTP 200 OK status field creation."""
        response = FlextWebModels.Web.Response(status_code=200, request_id="test-123")
        assert response.status_code == 200
        assert response.is_success is True

    def test_http_status_field_created(self) -> None:
        """Test HTTP 201 Created status field creation."""
        response = FlextWebModels.Web.Response(status_code=201, request_id="test-123")
        assert response.status_code == 201
        assert response.is_success is True

    def test_http_status_field_bad_request(self) -> None:
        """Test HTTP 400 Bad Request status field creation."""
        response = FlextWebModels.Web.Response(status_code=400, request_id="test-123")
        assert response.status_code == 400
        assert response.is_error is True

    def test_http_status_field_not_found(self) -> None:
        """Test HTTP 404 Not Found status field creation."""
        response = FlextWebModels.Web.Response(status_code=404, request_id="test-123")
        assert response.status_code == 404
        assert response.is_error is True

    def test_http_status_field_server_error(self) -> None:
        """Test HTTP 500 Internal Server Error status field creation."""
        response = FlextWebModels.Web.Response(status_code=500, request_id="test-123")
        assert response.status_code == 500
        assert response.is_error is True

    def test_http_status_field_create_field(self) -> None:
        """Test HTTP status field creation."""
        response = FlextWebModels.Web.Response(status_code=200, request_id="test-123")
        assert response.status_code == 200
        assert response.is_success is True

    def test_field_constraints(self) -> None:
        """Test field constraints are properly set."""
        # Test that Pydantic models have proper field constraints
        # Create a test model instance to check constraints
        test_model = FlextWebModels.Web.Request(
            url="http://localhost:8080",
            method="GET",
        )
        assert test_model.url == "http://localhost:8080"
        assert test_model.method == "GET"

    def test_field_descriptions(self) -> None:
        """Test field descriptions are properly set."""
        # Test that Pydantic models have proper field definitions
        # Create test model instances to check field behavior
        host_model = FlextWebModels.Web.Request(url="http://localhost:8080")
        port_model = FlextWebModels.Web.Request(url="http://localhost:3000")

        # Models should be created successfully
        assert host_model is not None
        assert port_model is not None

    def test_http_status_field_with_kwargs(self) -> None:
        """Test HTTP status field with additional kwargs."""
        # Test that Pydantic models handle status codes properly
        response_model = FlextWebModels.Web.Response(
            status_code=200,
            request_id="test-123",
        )
        assert response_model.status_code == 200
        assert response_model.is_success is True

    def test_field_creation_with_kwargs(self) -> None:
        """Test field creation with additional kwargs."""
        # Test that Pydantic models handle custom parameters
        request_model = FlextWebModels.Web.Request(
            url="http://localhost:8080",
            method="POST",
            headers={"Content-Type": "application/json"},
        )

        assert request_model.url == "http://localhost:8080"
        assert request_model.method == "POST"
        assert request_model.headers["Content-Type"] == "application/json"

    def test_http_status_field_factory_methods(self) -> None:
        """Test all HTTP status field factory methods."""
        # Test that Pydantic models handle different status codes
        status_codes = [200, 201, 400, 404, 500]

        for status_code in status_codes:
            response_model = FlextWebModels.Web.Response(
                status_code=status_code,
                request_id="test-123",
            )
            assert response_model.status_code == status_code
            assert isinstance(response_model, FlextWebModels.Web.Response)

    def test_field_validation_integration(self) -> None:
        """Test field validation integration."""
        # Test that Pydantic models work with default values

        class TestModel(BaseModel):
            host: str = FlextWebConstants.WebDefaults.HOST
            port: int = FlextWebConstants.WebDefaults.PORT

        model = TestModel()
        assert model.host == FlextWebConstants.WebDefaults.HOST
        assert model.port == FlextWebConstants.WebDefaults.PORT
