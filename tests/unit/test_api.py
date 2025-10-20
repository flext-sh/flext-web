"""Unit tests for flext_web.api module.

Tests the main API facade functionality following flext standards.
"""

from flext_web.api import FlextWebApi


class TestFlextWebApi:
    """Test suite for FlextWebApi class."""

    def test_initialization(self) -> None:
        """Test FlextWebApi initialization."""
        api = FlextWebApi()
        assert api is not None
        assert hasattr(api, "_container")
        assert hasattr(api, "_logger")

    def test_create_fastapi_app_success(self) -> None:
        """Test successful FastAPI app creation."""
        result = FlextWebApi.create_fastapi_app()
        assert result.is_success
        app = result.unwrap()
        assert app is not None

    def test_create_fastapi_app_with_config(self) -> None:
        """Test FastAPI app creation with configuration."""
        config = {"host": "localhost", "port": 8080, "debug": True}

        result = FlextWebApi.create_fastapi_app(config)
        assert result.is_success
        app = result.unwrap()
        assert app is not None

    def test_create_http_service_success(self) -> None:
        """Test successful HTTP service creation."""
        result = FlextWebApi.create_http_service()
        assert result.is_success
        service = result.unwrap()
        assert service is not None

    def test_create_http_service_with_config(self) -> None:
        """Test HTTP service creation with configuration."""
        config = {"host": "localhost", "port": 8080, "debug": True}

        result = FlextWebApi.create_http_service(config)
        assert result.is_success
        service = result.unwrap()
        assert service is not None

    def test_create_http_config_success(self) -> None:
        """Test HTTP configuration creation."""
        result = FlextWebApi.create_http_config(host="localhost", port=8080, debug=True)
        assert result.is_success
        config = result.unwrap()
        assert config.host == "localhost"
        assert config.port == 8080

    def test_create_http_config_with_defaults(self) -> None:
        """Test HTTP configuration creation with defaults."""
        result = FlextWebApi.create_http_config()
        assert result.is_success
        config = result.unwrap()
        assert config is not None
        assert config.host == "localhost"
        assert config.port == 8080

    def test_validate_http_config_success(self) -> None:
        """Test HTTP configuration validation."""
        config = {"host": "localhost", "port": 8080, "debug": True}

        result = FlextWebApi.validate_http_config(config)
        assert result.is_success
        assert result.unwrap() is True

    def test_validate_http_config_invalid(self) -> None:
        """Test HTTP configuration validation with invalid data."""
        # Use config that should actually fail validation (invalid port)
        config = {"port": -1}

        result = FlextWebApi.validate_http_config(config)
        assert result.is_failure

    def test_get_service_status(self) -> None:
        """Test service status retrieval."""
        result = FlextWebApi.get_service_status()
        assert result.is_success
        status = result.unwrap()
        assert isinstance(status, dict)
        assert "http_services_available" in status

    def test_get_api_capabilities(self) -> None:
        """Test API capabilities retrieval."""
        result = FlextWebApi.get_api_capabilities()
        assert result.is_success
        capabilities = result.unwrap()
        assert isinstance(capabilities, dict)
        assert "application_management" in capabilities
        assert "service_management" in capabilities
