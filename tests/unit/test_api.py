"""Unit tests for flext_web.api module.

Tests the main API facade functionality following flext standards.
"""

import pytest

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
        from flext_web.models import FlextWebModels

        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API", version="1.0.0"
        )

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
        from flext_web.config import FlextWebConfig
        from flext_web.constants import FlextWebConstants

        config = FlextWebConfig(
            host="localhost",
            port=8080,
            debug=True,  # Use alias
            secret_key=FlextWebConstants.WebDefaults.DEV_SECRET_KEY,
        )

        result = FlextWebApi.create_http_service(config)
        assert result.is_success
        service = result.unwrap()
        assert service is not None

    def test_create_fastapi_app_failure_logging(self) -> None:
        """Test FastAPI app creation failure logging."""
        from unittest.mock import patch

        from flext_core import FlextResult

        from flext_web.app import FlextWebApp

        # Mock create_fastapi_app to return failure
        with patch.object(
            FlextWebApp,
            "create_fastapi_app",
            return_value=FlextResult.fail("FastAPI creation failed"),
        ):
            result = FlextWebApi.create_fastapi_app()
            assert result.is_failure
            assert "FastAPI creation failed" in result.error

    def test_create_http_service_failure_logging(self) -> None:
        """Test HTTP service creation failure logging."""
        from unittest.mock import patch

        from flext_core import FlextResult

        from flext_web.services import FlextWebServices

        # Mock create_service to return failure
        with patch.object(
            FlextWebServices,
            "create_service",
            return_value=FlextResult.fail("Service creation failed"),
        ):
            result = FlextWebApi.create_http_service()
            assert result.is_failure
            assert "Service creation failed" in result.error

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
        from flext_web.config import FlextWebConfig
        from flext_web.constants import FlextWebConstants

        config = FlextWebConfig(
            host="localhost",
            port=8080,
            debug=True,  # Use alias
            secret_key=FlextWebConstants.WebDefaults.DEV_SECRET_KEY,
        )

        result = FlextWebApi.validate_http_config(config)
        assert result.is_success
        assert result.unwrap() is True

    def test_validate_http_config_invalid(self) -> None:
        """Test HTTP configuration validation with invalid data."""
        from pydantic import ValidationError

        from flext_web.config import FlextWebConfig

        # Config with invalid port should fail Pydantic validation on creation
        with pytest.raises(ValidationError):  # Pydantic will raise ValidationError
            FlextWebConfig(port=-1)

    def test_get_service_status(self) -> None:
        """Test service status retrieval."""
        from flext_web.models import FlextWebModels

        result = FlextWebApi.get_service_status()
        assert result.is_success
        status = result.unwrap()
        # ServiceResponse is now a Pydantic model, not a dict
        assert isinstance(status, FlextWebModels.Service.ServiceResponse)
        assert "http_services_available" in status.capabilities
        assert status.service == "flext-web-api"
        assert status.status == "operational"

    def test_get_api_capabilities(self) -> None:
        """Test API capabilities retrieval."""
        result = FlextWebApi.get_api_capabilities()
        assert result.is_success
        capabilities = result.unwrap()
        # ResponseDict is a TypeAlias for dict, so isinstance check is valid
        assert isinstance(capabilities, dict)
        assert "application_management" in capabilities
        assert "service_management" in capabilities
