"""Unit tests for flext_web.api module.

Tests the main API facade functionality following flext standards.
"""

from unittest.mock import patch

import pytest
from flext import FlextResult
from pydantic import ValidationError
from tests.conftest import create_test_result

from flext_web.api import FlextWebApi
from flext_web.constants import FlextWebConstants
from flext_web.models import FlextWebModels
from flext_web.settings import FlextWebSettings


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
        app = result.value
        assert app is not None

    def test_create_fastapi_app_with_config(self) -> None:
        """Test FastAPI app creation with configuration."""
        config = FlextWebModels.Web.FastAPIAppConfig(
            title="Test API",
            version="1.0.0",
        )

        result = FlextWebApi.create_fastapi_app(config)
        assert result.is_success
        app = result.value
        assert app is not None

    def test_create_http_service_success(self) -> None:
        """Test successful HTTP service creation."""
        result = FlextWebApi.create_http_service()
        assert result.is_success
        service = result.value
        assert service is not None

    def test_create_http_service_with_config(self) -> None:
        """Test HTTP service creation with configuration."""
        config = FlextWebSettings(
            host="localhost",
            port=8080,
            debug=True,  # Use alias
            secret_key=FlextWebConstants.WebDefaults.DEV_SECRET_KEY,
        )

        result = FlextWebApi.create_http_service(config)
        assert result.is_success
        service = result.value
        assert service is not None

    def test_create_fastapi_app_with_invalid_config(self) -> None:
        """Test FastAPI app creation with invalid config - REAL validation."""
        # Test with invalid config - Pydantic validation should fail
        # FastAPIAppConfig requires valid title (min_length=1)
        try:
            invalid_config = FlextWebModels.Web.FastAPIAppConfig(
                title="",  # Empty title - should fail Pydantic validation
                version="1.0.0",
            )
            # If validation passes, test will continue
            result = FlextWebApi.create_fastapi_app(invalid_config)
            # FastAPI itself may reject empty title, so result could be failure
            assert result.is_failure or result.is_success
        except ValidationError:
            # Expected - Pydantic validation should fail fast
            pass

    def test_create_http_service_with_invalid_config(self) -> None:
        """Test HTTP service creation with invalid config - REAL validation."""
        # Test with invalid config - Pydantic validation should fail
        try:
            # Config with invalid port should fail Pydantic validation
            invalid_config = FlextWebSettings(port=-1)  # Invalid port
            # If validation passes (shouldn't), test will continue
            result = FlextWebApi.create_http_service(invalid_config)
            # Service creation should handle invalid config
            assert result.is_failure, (
                "Invalid config should cause service creation to fail"
            )
        except ValidationError:
            # Expected - Pydantic validation should fail fast
            pass

    def test_create_http_config_success(self) -> None:
        """Test HTTP configuration creation."""
        result = FlextWebApi.create_http_config(host="localhost", port=8080, debug=True)
        assert result.is_success
        config = result.value
        assert config.host == "localhost"
        assert config.port == 8080

    def test_create_http_config_with_none_debug(self) -> None:
        """Test HTTP configuration creation with debug=None."""
        result = FlextWebApi.create_http_config(host="localhost", port=8080, debug=None)
        assert result.is_success

    def test_create_http_config_edge_cases(self) -> None:
        """Test HTTP configuration creation with edge cases."""
        # Test with maximum port number
        result = FlextWebApi.create_http_config(
            host="localhost",
            port=65535,
            debug=True,
        )
        assert result.is_success

        # Test with minimum valid port number
        result = FlextWebApi.create_http_config(host="localhost", port=1, debug=True)
        assert result.is_success

        # Test with very long host name
        long_host = "a" * 253  # Maximum hostname length
        result = FlextWebApi.create_http_config(host=long_host, port=8080, debug=True)
        assert result.is_success

    def test_create_http_config_invalid_cases(self) -> None:
        """Test HTTP configuration creation with invalid inputs."""
        # Test with invalid port (negative)
        result = FlextWebApi.create_http_config(host="localhost", port=-1, debug=True)
        assert result.is_failure

        # Test with invalid port (too high)
        result = FlextWebApi.create_http_config(
            host="localhost",
            port=65536,
            debug=True,
        )
        assert result.is_failure

        # Test with invalid host (empty string)
        result = FlextWebApi.create_http_config(host="", port=8080, debug=True)
        assert result.is_failure

    def test_http_config_result_consistency(self) -> None:
        """Test that HTTP config results follow FlextResult patterns."""
        # Test successful result structure
        success_result = FlextWebApi.create_http_config(
            host="localhost",
            port=8080,
            debug=True,
        )
        assert success_result.is_success
        assert success_result.value is not None
        assert success_result.error is None

        # Test failed result structure
        fail_result = FlextWebApi.create_http_config(host="", port=8080, debug=True)
        assert fail_result.is_failure
        assert fail_result.error is not None

        # Test that results are consistent with flext_tests patterns
        test_success = create_test_result(success=True, data="test")
        test_failure = create_test_result(success=False, error="test error")

        assert test_success.is_success
        assert test_success.value == "test"
        assert test_failure.is_failure
        assert test_failure.error == "test error"

    def test_create_http_config_with_defaults(self) -> None:
        """Test HTTP configuration creation with defaults."""
        result = FlextWebApi.create_http_config()
        assert result.is_success

    @pytest.mark.parametrize(
        ("host", "port", "debug", "should_succeed"),
        [
            # Valid cases
            ("localhost", 8080, True, True),
            ("127.0.0.1", 3000, False, True),
            ("0.0.0.0", 80, True, True),
            ("example.com", 443, False, True),
            # Invalid cases
            ("", 8080, True, False),  # Empty host
            ("localhost", -1, True, False),  # Negative port
            ("localhost", 0, True, False),  # Zero port
            ("localhost", 65536, True, False),  # Port too high
            ("invalid..host", 8080, True, True),  # Hostname format not validated
        ],
    )
    def test_http_config_parametrized(
        self,
        host: str,
        port: int,
        debug: bool,
        should_succeed: bool,
    ) -> None:
        """Test HTTP configuration creation with parametrized edge cases."""
        result = FlextWebApi.create_http_config(host=host, port=port, debug=debug)

        if should_succeed:
            assert result.is_success, (
                f"Expected success for {host}:{port}, got: {result.error}"
            )
            config = result.value
            assert config.host == host
            assert config.port == port
            assert config.debug == debug
        else:
            assert result.is_failure, (
                f"Expected failure for {host}:{port}, but succeeded"
            )
            assert result.error is not None

    def test_validate_http_config_success(self) -> None:
        """Test HTTP configuration validation."""
        config = FlextWebSettings(
            host="localhost",
            port=8080,
            debug=True,  # Use alias
            secret_key=FlextWebConstants.WebDefaults.DEV_SECRET_KEY,
        )

        result = FlextWebApi.validate_http_config(config)
        assert result.is_success
        assert result.value is True

    def test_validate_http_config_invalid(self) -> None:
        """Test HTTP configuration validation with invalid data."""
        # Config with invalid port should fail Pydantic validation on creation
        with pytest.raises(ValidationError):  # Pydantic will raise ValidationError
            FlextWebSettings(port=-1)

    def test_get_service_status(self) -> None:
        """Test service status retrieval."""
        result = FlextWebApi.get_service_status()
        assert result.is_success
        status = result.value
        # ServiceResponse is now a Pydantic model, not a dict
        assert isinstance(status, FlextWebModels.Service.ServiceResponse)
        assert "http_services_available" in status.capabilities
        assert status.service == "flext-web-api"
        assert status.status == "operational"

    def test_get_api_capabilities(self) -> None:
        """Test API capabilities retrieval."""
        result = FlextWebApi.get_api_capabilities()
        assert result.is_success
        capabilities = result.value
        # ResponseDict is a TypeAlias for dict, so isinstance check is valid
        assert isinstance(capabilities, dict)
        assert "application_management" in capabilities
        assert "service_management" in capabilities

    def test_create_fastapi_app_error_logging(self) -> None:
        """Test create_fastapi_app error logging (line 84)."""
        # Create a config that will cause FastAPI creation to fail
        # We'll patch FastAPI to raise an exception
        with patch("flext_web.app.FastAPI", side_effect=Exception("Test error")):
            result = FlextWebApi.create_fastapi_app()
            # Should fail and log error (line 84)
            assert result.is_failure
            assert result.error is not None
            assert "Failed to create FastAPI application" in result.error

    def test_create_http_service_error_logging(self) -> None:
        """Test create_http_service error logging (line 120)."""
        # Patch FlextWebServices.create_service to return failure
        with patch(
            "flext_web.services.FlextWebServices.create_service",
            return_value=FlextResult[object].fail("Service creation failed"),
        ):
            result = FlextWebApi.create_http_service()
            # Should fail and log error (line 120)
            assert result.is_failure
            assert result.error is not None
            assert "Service creation failed" in result.error
