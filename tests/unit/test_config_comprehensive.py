"""FLEXT Web Interface - Comprehensive Configuration Testing.

Enterprise-grade test suite for FlextWebConfigs.WebConfig validation, environment variable
integration, and configuration management patterns. Ensures configuration
follows business rules, security requirements, and production deployment standards.

Test Categories:
    - Basic configuration creation and validation
    - Environment variable integration and precedence
    - Production vs development mode behavior
    - Security validation for production deployment
    - Configuration error handling and validation

Integration:
    - Tests flext-core configuration patterns
    - Validates environment-based settings management
    - Ensures production safety and security compliance
    - Verifies enterprise deployment scenarios

Author: FLEXT Development Team
Version: 0.9.0
Status: Enterprise testing standards with comprehensive coverage
"""

from __future__ import annotations

import os

import pytest
from pydantic import ValidationError

from flext_web import FlextWebConfigs


class TestWebConfigBasic:
    """Enterprise configuration testing for basic functionality and validation.

    Test suite covering fundamental FlextWebConfigs.WebConfig creation, default values,
    and basic validation patterns. Ensures configuration follows enterprise
    standards with proper type safety and business rule enforcement.
    """

    def test_web_config_creation(self) -> None:
        """Test basic FlextWebConfigs.WebConfig creation with default values.

        Validates that configuration instance creates successfully with
        all default values properly set and business rules satisfied.
        Tests fundamental configuration patterns used throughout the system.
        """
        config = FlextWebConfigs.WebConfig()
        if config.app_name != "FLEXT Web":
            msg: str = f"Expected {'FLEXT Web'}, got {config.app_name}"
            raise AssertionError(msg)
        assert config.version == "0.9.0"

    def test_web_config_with_custom_settings(self) -> None:
        """Test WebConfig with custom settings."""
        config = FlextWebConfigs.WebConfig(app_name="Custom Web App", version="0.9.0")
        if config.app_name != "Custom Web App":
            msg: str = f"Expected {'Custom Web App'}, got {config.app_name}"
            raise AssertionError(msg)
        assert config.version == "0.9.0"

    def test_web_config_security_settings(self) -> None:
        """Test security-related settings."""
        config = FlextWebConfigs.WebConfig()
        assert config.secret_key is not None
        if len(config.secret_key) < 32:
            msg: str = f"Expected {len(config.secret_key)} >= {32}"
            raise AssertionError(msg)
        assert isinstance(config.debug, bool)

    def test_web_config_server_settings(self) -> None:
        """Test server-related settings."""
        config = FlextWebConfigs.WebConfig()
        if config.host != "localhost":
            msg: str = f"Expected {'localhost'}, got {config.host}"
            raise AssertionError(msg)
        assert isinstance(config.port, int)
        assert 1 <= config.port <= 65535

    def test_web_config_validation(self) -> None:
        """Test configuration validation."""
        config = FlextWebConfigs.WebConfig()
        result = config.validate_config()
        assert result.success

    def test_web_config_port_validation(self) -> None:
        """Test port validation."""
        with pytest.raises(ValidationError):
            FlextWebConfigs.WebConfig(port=0)  # Below minimum

        with pytest.raises(ValidationError):
            FlextWebConfigs.WebConfig(port=65536)  # Above maximum

    def test_create_web_config_function(self) -> None:
        """Test create_web_config function."""
        settings = FlextWebConfigs.create_web_config()
        assert isinstance(settings, FlextWebConfigs.WebConfig)
        if settings.app_name != "FLEXT Web":
            msg: str = f"Expected {'FLEXT Web'}, got {settings.app_name}"
            raise AssertionError(msg)


class TestConfigIntegration:
    """Integration tests for configuration."""

    def test_config_with_environment_variables(self) -> None:
        """Test configuration with environment variables."""
        # Set environment variable
        os.environ["FLEXT_WEB_APP_NAME"] = "Test App From Env"

        try:
            config = FlextWebConfigs.WebConfig()
            if config.app_name != "Test App From Env":
                msg: str = f"Expected {'Test App From Env'}, got {config.app_name}"
                raise AssertionError(msg)
        finally:
            # Cleanup
            if "FLEXT_WEB_APP_NAME" in os.environ:
                del os.environ["FLEXT_WEB_APP_NAME"]

    def test_config_validation_empty_name(self) -> None:
        """Test validation with empty app name."""
        # Empty app name should fail at construction time with Pydantic validation
        with pytest.raises(
            ValidationError, match="String should have at least 1 character"
        ):
            FlextWebConfigs.WebConfig(app_name="")
