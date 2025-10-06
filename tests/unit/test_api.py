"""Unit tests for flext_web.api module.

Tests the main API facade functionality following flext standards.
"""

from flext_web.api import FlextWeb
from flext_web.models import FlextWebModels


class TestFlextWeb:
    """Test suite for FlextWeb class."""

    def test_initialization(self) -> None:
        """Test FlextWeb initialization."""
        web = FlextWeb()
        assert web is not None
        assert hasattr(web, "_container")
        assert hasattr(web, "_logger")

    def test_create_fastapi_app_success(self) -> None:
        """Test successful FastAPI app creation."""
        config = FlextWebModels.AppConfig(
            title="Test API", version="1.0.0", description="Test API Description"
        )

        result = FlextWeb.create_fastapi_app(config)
        assert result.is_success
        app = result.unwrap()
        assert app is not None

    def test_create_web_service_success(self) -> None:
        """Test successful web service creation."""
        result = FlextWeb.create_web_service()
        assert result.is_success
        service = result.unwrap()
        assert service is not None

    def test_create_web_service_with_config(self) -> None:
        """Test web service creation with configuration."""
        config = {"host": "localhost", "port": 8080, "debug": True}

        result = FlextWeb.create_web_service(config)
        assert result.is_success
        service = result.unwrap()
        assert service is not None

    def test_create_web_config_success(self) -> None:
        """Test web configuration creation."""
        result = FlextWeb.create_web_config(host="localhost", port=8080, debug=True)
        assert result.is_success
        config = result.unwrap()
        assert config.host == "localhost"
        assert config.port == 8080
        assert config.debug is True

    def test_create_web_config_with_defaults(self) -> None:
        """Test web configuration creation with defaults."""
        result = FlextWeb.create_web_config()
        assert result.is_success
        config = result.unwrap()
        assert config is not None

    def test_validate_web_config_success(self) -> None:
        """Test web configuration validation."""
        config = {"host": "localhost", "port": 8080, "debug": True}

        result = FlextWeb.validate_web_config(config)
        assert result.is_success
        assert result.unwrap() is True

    def test_validate_web_config_invalid(self) -> None:
        """Test web configuration validation with invalid data."""
        config = "invalid_config"

        result = FlextWeb.validate_web_config(config)
        assert result.is_failure

    def test_get_service_status(self) -> None:
        """Test service status retrieval."""
        result = FlextWeb.get_service_status()
        assert result.is_success
        status = result.unwrap()
        assert isinstance(status, dict)
        assert "web_services_available" in status
