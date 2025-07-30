"""Comprehensive tests for config.py to improve coverage."""

from __future__ import annotations

import os

import pytest
from pydantic import ValidationError

from flext_web.config import FlextWebConfig, get_web_settings


class TestWebConfigBasic:
    """Test WebConfig basic functionality."""

    def test_web_config_creation(self) -> None:
        """Test basic WebConfig creation."""
        config = FlextWebConfig()
        if config.app_name != "FLEXT Web":
            msg = f"Expected {'FLEXT Web'}, got {config.app_name}"
            raise AssertionError(msg)
        assert config.version == "0.9.0"

    def test_web_config_with_custom_settings(self) -> None:
        """Test WebConfig with custom settings."""
        config = FlextWebConfig(app_name="Custom Web App", version="0.9.0")
        if config.app_name != "Custom Web App":
            msg = f"Expected {'Custom Web App'}, got {config.app_name}"
            raise AssertionError(msg)
        assert config.version == "0.9.0"

    def test_web_config_security_settings(self) -> None:
        """Test security-related settings."""
        config = FlextWebConfig()
        assert config.secret_key is not None
        if len(config.secret_key) < 32:
            msg = f"Expected {len(config.secret_key)} >= {32}"
            raise AssertionError(msg)
        assert isinstance(config.debug, bool)

    def test_web_config_server_settings(self) -> None:
        """Test server-related settings."""
        config = FlextWebConfig()
        if config.host != "localhost":
            msg = f"Expected {'localhost'}, got {config.host}"
            raise AssertionError(msg)
        assert isinstance(config.port, int)
        assert 1 <= config.port <= 65535

    def test_web_config_validation(self) -> None:
        """Test configuration validation."""
        config = FlextWebConfig()
        result = config.validate_config()
        assert result.is_success

    def test_web_config_port_validation(self) -> None:
        """Test port validation."""
        with pytest.raises(ValidationError):
            FlextWebConfig(port=0)  # Below minimum

        with pytest.raises(ValidationError):
            FlextWebConfig(port=65536)  # Above maximum

    def test_get_web_settings_function(self) -> None:
        """Test get_web_settings function."""
        settings = get_web_settings()
        assert isinstance(settings, FlextWebConfig)
        if settings.app_name != "FLEXT Web":
            msg = f"Expected {'FLEXT Web'}, got {settings.app_name}"
            raise AssertionError(msg)


class TestConfigIntegration:
    """Integration tests for configuration."""

    def test_config_with_environment_variables(self) -> None:
        """Test configuration with environment variables."""
        # Set environment variable
        os.environ["FLEXT_WEB_APP_NAME"] = "Test App From Env"

        try:
            config = FlextWebConfig()
            if config.app_name != "Test App From Env":
                msg = f"Expected {'Test App From Env'}, got {config.app_name}"
                raise AssertionError(msg)
        finally:
            # Cleanup
            if "FLEXT_WEB_APP_NAME" in os.environ:
                del os.environ["FLEXT_WEB_APP_NAME"]

    def test_config_validation_empty_name(self) -> None:
        """Test validation with empty app name."""
        config = FlextWebConfig(app_name="")
        result = config.validate_config()
        assert not result.is_success
        if "App name is required" not in result.error:
            msg = f"Expected {'App name is required'} in {result.error}"
            raise AssertionError(msg)
