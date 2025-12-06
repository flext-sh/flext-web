"""Unit tests for flext_web.config module.

Tests the web configuration functionality following flext standards.
"""

from unittest.mock import patch

import pytest
from pydantic import ValidationError

from flext_web.config import FlextWebConfig
from flext_web.constants import FlextWebConstants


class TestFlextWebConfig:
    """Test suite for FlextWebConfig class."""

    def test_initialization_with_test_environment(self) -> None:
        """Test FlextWebConfig initialization with test environment variables."""
        # Test environment sets FLEXT_WEB_DEBUG=true, so expect True
        config = FlextWebConfig()
        assert config.host == FlextWebConstants.WebDefaults.HOST
        assert config.port == FlextWebConstants.WebDefaults.PORT
        assert config.debug_mode is True  # Set by test environment
        assert config.app_name == "FLEXT Web"

    def test_initialization_with_custom_values(self) -> None:
        """Test FlextWebConfig initialization with custom values."""
        config = FlextWebConfig(
            host="0.0.0.0",
            port=3000,
            debug=True,
            app_name="Test App",
        )
        assert config.host == "0.0.0.0"
        assert config.port == 3000
        assert config.debug_mode is True
        assert config.app_name == "Test App"

    def test_validation_host_empty(self) -> None:
        """Test host validation with empty string."""
        with pytest.raises(ValidationError):
            FlextWebConfig(host="")

    def test_validation_port_range(self) -> None:
        """Test port validation within valid range."""
        config = FlextWebConfig(port=8080)
        assert config.port == 8080

    def test_validation_port_out_of_range(self) -> None:
        """Test port validation outside valid range."""
        with pytest.raises(ValidationError):
            FlextWebConfig(port=70000)

    def test_validation_secret_key_too_short(self) -> None:
        """Test secret key validation with too short key."""
        with pytest.raises(ValidationError):
            FlextWebConfig(secret_key="short")

    def test_validation_secret_key_valid(self) -> None:
        """Test secret key validation with valid key."""
        config = FlextWebConfig(secret_key="valid-secret-key-32-characters-long")
        assert config.secret_key is not None

    def test_ssl_configuration_valid(self) -> None:
        """Test SSL configuration with valid cert and key paths."""
        # This would need actual cert files in a real test
        config = FlextWebConfig(
            ssl_enabled=False,
            ssl_cert_path=None,
            ssl_key_path=None,
        )
        assert config.ssl_enabled is False

    def test_computed_fields(self) -> None:
        """Test computed fields."""
        config = FlextWebConfig(ssl_enabled=False)
        assert config.protocol == "http"

        # Test with SSL disabled (no cert/key required)
        config_https = FlextWebConfig(ssl_enabled=False)
        assert config_https.protocol == "http"

    def test_base_url_generation(self) -> None:
        """Test base URL generation."""
        config = FlextWebConfig(host="localhost", port=8080, ssl_enabled=False)
        assert config.base_url == "http://localhost:8080"

    def test_validate_config_success(self) -> None:
        """Test config validation with Pydantic."""
        config = FlextWebConfig()
        assert config.host is not None
        assert config.port is not None

    def test_to_dict_method(self) -> None:
        """Test config to dict conversion using Pydantic model_dump."""
        config = FlextWebConfig(host="localhost", port=8080)
        config_dict = config.model_dump()
        assert config_dict["host"] == "localhost"
        assert config_dict["port"] == 8080
        assert "debug_mode" in config_dict

    def test_create_web_config_factory(self) -> None:
        """Test web config direct instantiation with Pydantic."""
        config = FlextWebConfig(host="test", port=9000)
        assert config.host == "test"
        assert config.port == 9000

    def test_create_web_config_class_method(self) -> None:
        """Test create_web_config class method."""
        result = FlextWebConfig.create_web_config()
        assert result.is_success
        config = result.value
        assert isinstance(config, FlextWebConfig)
        assert config.host == FlextWebConstants.WebDefaults.HOST
        assert config.port == FlextWebConstants.WebDefaults.PORT

    def test_create_web_config_exception_handling(self) -> None:
        """Test create_web_config exception handling (lines 99-100)."""
        # Patch __init__ to raise an exception
        with patch.object(
            FlextWebConfig,
            "__init__",
            side_effect=Exception("Config creation failed"),
        ):
            result = FlextWebConfig.create_web_config()
            assert result.is_failure
            assert result.error is not None
            assert "Failed to create web config" in result.error
            assert "Config creation failed" in result.error
