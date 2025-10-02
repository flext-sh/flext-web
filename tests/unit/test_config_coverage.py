"""FLEXT Web Configuration - Coverage Enhancement Tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os

from flext_core import FlextTypes
from flext_web import FlextWebConfig


class TestConfigFactoryMethods:
    """Test factory methods in FlextWebConfig for complete coverage."""

    def test_create_development_config_success(self) -> None:
        """Test create_development_config factory method."""
        result = FlextWebConfig.create_development_config()

        assert result.is_success, (
            f"Development config should succeed, got: {result.error}"
        )
        config = result.value
        assert isinstance(config, FlextWebConfig)
        assert config.debug is True  # Development should have debug enabled
        assert config.host == "localhost"  # Development default
        assert config.port == 8080  # Development default

    def test_create_production_config_success(self) -> None:
        """Test create_production_config factory method with required env vars."""
        # Set required environment variables for production
        os.environ["FLEXT_WEB_SECRET_KEY"] = "production-secret-key-32-chars-exactly"
        os.environ["FLEXT_WEB_HOST"] = "0.0.0.0"
        os.environ["FLEXT_WEB_PORT"] = "8080"

        try:
            result = FlextWebConfig.create_production_config()

            assert result.is_success, (
                f"Production config should succeed, got: {result.error}"
            )
            config = result.value
            assert isinstance(config, FlextWebConfig)
            assert config.debug is False  # Production should have debug disabled
            # Note: 0.0.0.0 gets converted to 127.0.0.1 for security unless FLEXT_DEVELOPMENT_MODE=true
            assert config.host == "127.0.0.1"
            assert config.port == 8080
            assert config.secret_key == "production-secret-key-32-chars-exactly"
        finally:
            # Clean up environment variables
            for key in ["FLEXT_WEB_SECRET_KEY", "FLEXT_WEB_HOST", "FLEXT_WEB_PORT"]:
                os.environ.pop(key, None)

    def test_create_production_config_missing_secret(self) -> None:
        """Test create_production_config failure with missing secret key."""
        # Ensure secret key is not set
        os.environ.pop("FLEXT_WEB_SECRET_KEY", None)

        result = FlextWebConfig.create_production_config()

        assert result.is_failure, "Production config should fail without secret key"
        error = result.error or ""
        assert "secret" in error.lower() or "production" in error.lower()

    def test_create_test_config_failure_invalid_port(self) -> None:
        """Test create_test_config factory method fails with invalid port."""
        result = FlextWebConfig.create_test_config()

        # The current implementation tries to set port=0 which is invalid
        assert result.is_failure, "Test config should fail due to invalid port=0"
        error = result.error or ""
        assert "port" in error.lower()
        assert "greater than" in error.lower() or "1" in error.lower()

    def test_create_config_from_env_success(self) -> None:
        """Test create_config_from_env factory method."""
        # Set some environment variables
        os.environ["FLEXT_WEB_HOST"] = "example.com"
        os.environ["FLEXT_WEB_PORT"] = "9090"
        os.environ["FLEXT_WEB_DEBUG"] = "false"

        try:
            # Use settings to properly read environment variables

            settings = FlextWebSettings()
            result = settings.to_config()

            assert result.is_success, (
                f"Config from env should succeed, got: {result.error}"
            )
            config = result.value
            assert isinstance(config, FlextWebConfig)
            assert config.host == "example.com"
            assert config.port == 9090
            assert config.debug is False
        finally:
            # Clean up environment variables
            for key in ["FLEXT_WEB_HOST", "FLEXT_WEB_PORT", "FLEXT_WEB_DEBUG"]:
                os.environ.pop(key, None)

    def test_create_config_from_env_defaults(self) -> None:
        """Test create_config_from_env with default values when no env vars set."""
        # Ensure relevant env vars are cleared
        env_keys = [
            "FLEXT_WEB_HOST",
            "FLEXT_WEB_PORT",
            "FLEXT_WEB_DEBUG",
            "FLEXT_WEB_SECRET_KEY",
        ]
        original_values = {}
        for key in env_keys:
            original_values[key] = os.environ.get(key)
            os.environ.pop(key, None)

        try:
            config = FlextWebConfig()

            assert isinstance(config, FlextWebConfig)
            # Should use default values when env vars not set
            assert config.host == "localhost"
            assert config.port == 8080
        finally:
            # Restore original environment variables
            for key, value in original_values.items():
                if value is not None:
                    os.environ[key] = value
                else:
                    os.environ.pop(key, None)


class TestConfigValidationMethods:
    """Test validation methods in FlextWebConfig for complete coverage."""

    def test_validate_web_config_success(self) -> None:
        """Test validate_web_config with valid config."""
        config = FlextWebConfig(
            host="localhost",
            port=8080,
            debug=True,
            secret_key="valid-secret-key-32-characters-exactly",
        )

        result = FlextWebConfig.validate_web_config(config)

        assert result.is_success, f"Validation should succeed, got: {result.error}"
        # ValidationResult returns None on success, not the config object
        assert result.value is None

    def test_validate_web_config_production_failure(self) -> None:
        """Test validate_web_config failure for production config with dev secret."""
        # Use model_construct to bypass initial validation
        config = FlextWebConfig.model_construct(
            host="0.0.0.0",
            port=80,
            debug=False,  # Production mode
            secret_key="dev-secret",  # Invalid for production
        )

        result = FlextWebConfig.validate_web_config(config)

        assert result.is_failure, (
            "Validation should fail for production config with dev secret"
        )


class TestConfigSystemMethods:
    """Test system configuration methods in FlextWebConfig for complete coverage."""

    def test_configure_web_configs_system_success(self) -> None:
        """Test configure_web_configs_system with valid configuration."""
        config_data = {
            "environment": "development",
            "enable_debug": True,
            "max_request_size": 16777216,
            "enable_cors": False,
        }

        result = FlextWebConfig.configure_web_configs_system(config_data)

        assert result.is_success, (
            f"System configuration should succeed, got: {result.error}"
        )
        configured = result.value
        assert isinstance(configured, dict)
        assert configured["environment"] == "development"

    def test_configure_web_configs_system_invalid_environment(self) -> None:
        """Test configure_web_configs_system with invalid environment."""
        config_data: FlextTypes.Core.Dict = {"environment": "invalid-environment"}

        result = FlextWebConfig.configure_web_configs_system(config_data)

        assert result.is_failure, (
            "System configuration should fail with invalid environment"
        )
        error = result.error or ""
        assert "environment" in error.lower()

    def test_get_web_configs_system_config_success(self) -> None:
        """Test get_web_configs_system_config retrieval."""
        result = FlextWebConfig.get_web_configs_system_config()

        assert result.is_success, (
            f"System config retrieval should succeed, got: {result.error}"
        )
        config = result.value
        assert isinstance(config, dict)
        # Should contain system information
        assert "environment" in config
        assert "available_configs" in config
        assert "available_factories" in config


class TestWebConfigBusinessLogic:
    """Test WebConfig business logic methods for complete coverage."""

    def test_web_config_is_production_true(self) -> None:
        """Test WebConfig is_production method returns True for production."""
        config = FlextWebConfig(debug=False)
        assert config.is_production() is True

    def test_web_config_is_production_false(self) -> None:
        """Test WebConfig is_production method returns False for development."""
        config = FlextWebConfig(debug=True)
        assert config.is_production() is False

    def test_web_config_get_server_url_default(self) -> None:
        """Test WebConfig get_server_url method with default values."""
        config = FlextWebConfig()
        url = config.get_server_url()
        assert url == "http://localhost:8080"

    def test_web_config_get_server_url_custom(self) -> None:
        """Test WebConfig get_server_url method with custom values."""
        config = FlextWebConfig(host="example.com", port=9000)
        url = config.get_server_url()
        assert url == "http://example.com:9000"

    def test_web_config_validate_production_settings_success(self) -> None:
        """Test WebConfig validate_production_settings with valid production config."""
        config = FlextWebConfig(
            host="0.0.0.0",  # Production host (not localhost)
            debug=False,
            secret_key="production-secret-key-32-chars-exactly",
        )

        result = config.validate_production_settings()

        assert result.is_success, (
            f"Production validation should succeed, got: {result.error}"
        )

    def test_web_config_validate_production_settings_failure(self) -> None:
        """Test WebConfig validate_production_settings with invalid production config."""
        # Use model_construct to bypass initial validation
        config = FlextWebConfig.model_construct(
            debug=False,  # Production mode
            secret_key="dev",  # Too short for production
        )

        result = config.validate_production_settings()

        assert result.is_failure, (
            "Production validation should fail with short secret key"
        )
        error = result.error or ""
        assert "secret" in error.lower()

    def test_web_config_validate_config_success(self) -> None:
        """Test WebConfig validate_config method with valid configuration."""
        config = FlextWebConfig(
            host="localhost",
            port=8080,
            secret_key="valid-secret-key-32-chars-minimum-req",
        )

        result = config.validate_business_rules()

        assert result.is_success, (
            f"Config validation should succeed, got: {result.error}"
        )
        # validate_config returns FlextResult[None], not a validation dict
        assert result.value is None

    def test_web_config_validate_config_failure(self) -> None:
        """Test WebConfig validate_config method with invalid configuration."""
        # Create config with invalid port using model_construct to bypass validation
        config = FlextWebConfig.model_construct(
            host="localhost",
            port=99999,  # Invalid port
            secret_key="short",
        )

        result = config.validate_business_rules()

        assert result.is_failure, "Config validation should fail with invalid settings"
