"""Comprehensive test coverage for flext_web.config module.

This test module targets specific missing coverage areas identified in the coverage report.
Focus on real execution tests without mocks for maximum functional coverage.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import os
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from flext_web import FlextWebConfigs


class TestWebConfigValidation:
    """Test WebConfig validation and edge cases."""

    def test_config_with_invalid_port_negative(self) -> None:
        """Test config creation with negative port."""
        with pytest.raises(ValidationError) as exc_info:
            FlextWebConfigs.WebConfig(port=-1)

        assert "greater than or equal to 1" in str(exc_info.value)

    def test_config_with_invalid_port_too_high(self) -> None:
        """Test config creation with port too high."""
        with pytest.raises(ValidationError) as exc_info:
            FlextWebConfigs.WebConfig(port=70000)

        assert "less than or equal to 65535" in str(exc_info.value)

    def test_config_with_empty_secret_key_production(self) -> None:
        """Test config with empty secret key in production."""
        with pytest.raises(ValidationError) as exc_info:
            FlextWebConfigs.WebConfig(
                secret_key="",  # Empty secret key
                debug=False,  # Production mode
            )

        assert "secret_key" in str(exc_info.value).lower()

    def test_config_with_weak_secret_key_production(self) -> None:
        """Test config with weak secret key in production."""
        with pytest.raises(ValidationError) as exc_info:
            FlextWebConfigs.WebConfig(
                secret_key="weak",  # Too short
                debug=False,  # Production mode
            )

        assert "secret_key" in str(exc_info.value).lower()

    def test_config_cors_enabled_debug_disabled(self) -> None:
        """Test config with CORS enabled but debug disabled."""
        config = FlextWebConfigs.WebConfig(
            enable_cors=True,
            debug=False,
            secret_key="very-secure-production-secret-key-12345",
        )

        # Should work but might trigger warnings
        assert config.enable_cors is True
        assert config.debug is False

    def test_config_max_content_length_validation(self) -> None:
        """Test max_content_length validation."""
        config = FlextWebConfigs.WebConfig(max_content_length=1024)
        assert config.max_content_length == 1024

        # Test with very large value
        config = FlextWebConfigs.WebConfig(
            max_content_length=100 * 1024 * 1024  # 100MB
        )
        assert config.max_content_length == 100 * 1024 * 1024

    def test_config_request_timeout_validation(self) -> None:
        """Test request_timeout validation."""
        config = FlextWebConfigs.WebConfig(request_timeout=60)
        assert config.request_timeout == 60

        # Test with maximum allowed timeout
        config = FlextWebConfigs.WebConfig(
            request_timeout=300  # Maximum allowed (5 minutes)
        )
        assert config.request_timeout == 300


class TestWebConfigEnvironmentVariables:
    """Test environment variable handling in WebConfig."""

    def test_config_from_env_all_variables(self) -> None:
        """Test config creation from complete environment variables."""
        env_vars = {
            "FLEXT_WEB_HOST": "0.0.0.0",
            "FLEXT_WEB_PORT": "9000",
            "FLEXT_WEB_DEBUG": "false",
            "FLEXT_WEB_SECRET_KEY": "production-secret-key-from-env-12345",
            "FLEXT_WEB_APP_NAME": "Production FLEXT Web",
            "FLEXT_WEB_MAX_CONTENT_LENGTH": "32777216",  # 32MB
            "FLEXT_WEB_REQUEST_TIMEOUT": "120",
            "FLEXT_WEB_ENABLE_CORS": "true",
        }

        with patch.dict(os.environ, env_vars, clear=False):
            config_result = FlextWebConfigs.create_config_from_env()
            assert config_result.is_success
            config = config_result.value

            assert (
                config.host == "127.0.0.1"
            )  # Security validation converts 0.0.0.0 to localhost
            assert config.port == 9000
            assert config.debug is False
            assert config.secret_key == "production-secret-key-from-env-12345"
            assert config.app_name == "Production FLEXT Web"
            assert config.max_content_length == 32777216
            assert config.request_timeout == 120
            assert config.enable_cors is True

    def test_config_from_env_partial_variables(self) -> None:
        """Test config creation from partial environment variables."""
        env_vars = {
            "FLEXT_WEB_HOST": "custom-host",
            "FLEXT_WEB_PORT": "8888",
        }

        with patch.dict(os.environ, env_vars, clear=False):
            config_result = FlextWebConfigs.create_config_from_env()
            assert config_result.is_success
            config = config_result.value

            assert config.host == "custom-host"
            assert config.port == 8888
            # Other values should be from environment/conftest/env file
            assert (
                config.debug is False
            )  # From inherited FlextConfig which defaults to False
            assert config.app_name == "flext-app"  # From FlextConfig inheritance

    def test_config_from_env_invalid_types(self) -> None:
        """Test config creation with invalid environment variable types."""
        env_vars = {
            "FLEXT_WEB_PORT": "not_a_number",
            "FLEXT_WEB_DEBUG": "not_a_boolean",
        }

        with (
            patch.dict(os.environ, env_vars, clear=False),
            pytest.raises(ValidationError),
        ):
            FlextWebConfigs.WebConfig()

    def test_config_env_override_precedence(self) -> None:
        """Test that explicit parameters override environment variables."""
        env_vars = {
            "FLEXT_WEB_HOST": "env-host",
            "FLEXT_WEB_PORT": "8000",
        }

        with patch.dict(os.environ, env_vars, clear=False):
            config = FlextWebConfigs.WebConfig(
                host="explicit-host",  # Should override env
                port=9000,  # Should override env
            )

            assert config.host == "explicit-host"
            assert config.port == 9000


class TestWebConfigFactoryMethods:
    """Test FlextWebConfigs factory methods."""

    def test_create_web_config_no_overrides(self) -> None:
        """Test creating web config without overrides."""
        result = FlextWebConfigs.create_web_config()

        assert result.is_success
        config = result.value
        assert isinstance(config, FlextWebConfigs.WebConfig)
        assert config.host == "localhost"  # Default

    def test_create_web_config_with_overrides(self) -> None:
        """Test creating web config with overrides."""
        result = FlextWebConfigs.create_web_config(
            host="custom-host", port=9999, debug=False
        )

        assert result.is_success
        config = result.value
        assert config.host == "custom-host"
        assert config.port == 9999
        assert config.debug is False

    def test_create_development_config(self) -> None:
        """Test creating development-optimized config."""
        result = FlextWebConfigs.create_development_config()

        assert result.is_success
        config = result.value
        assert config.debug is True
        assert config.host == "localhost"
        assert "dev" in config.secret_key.lower()

    def test_create_production_config_with_env(self) -> None:
        """Test creating production config with required environment."""
        env_vars = {
            "FLEXT_WEB_SECRET_KEY": "production-secret-key-that-is-long-enough-for-validation-12345",
            "FLEXT_WEB_HOST": "0.0.0.0",  # Override conftest.py localhost for production test
        }

        with patch.dict(os.environ, env_vars, clear=False):
            result = FlextWebConfigs.create_production_config()

            assert result.is_success
            config = result.value
            assert config.debug is False
            assert (
                config.secret_key
                == "production-secret-key-that-is-long-enough-for-validation-12345"
            )

    def test_create_production_config_missing_secret(self) -> None:
        """Test creating production config without required secret key."""
        # Clear any existing FLEXT_WEB_SECRET_KEY
        env_vars = {}
        if "FLEXT_WEB_SECRET_KEY" in os.environ:
            env_vars["FLEXT_WEB_SECRET_KEY"] = ""

        with patch.dict(os.environ, env_vars, clear=True):
            result = FlextWebConfigs.create_production_config()

            # Should fail due to missing secret key
            assert result.is_failure
            assert result.error is not None
            assert "secret" in result.error.lower()

    def test_create_test_config(self) -> None:
        """Test creating test-optimized config."""
        result = FlextWebConfigs.create_test_config()

        # Test config creation should fail due to port=0 validation
        assert result.is_failure
        assert result.error is not None
        assert "port" in result.error.lower()
        assert "greater than or equal to 1" in result.error

    def test_create_config_from_env_success(self) -> None:
        """Test creating config from environment."""
        env_vars = {"FLEXT_WEB_HOST": "env-host", "FLEXT_WEB_PORT": "7777"}

        with patch.dict(os.environ, env_vars, clear=False):
            result = FlextWebConfigs.create_config_from_env()

            assert result.is_success
            config = result.value
            assert config.host == "env-host"
            assert config.port == 7777

    def test_create_config_from_env_validation_error(self) -> None:
        """Test creating config from environment with validation errors."""
        env_vars = {
            "FLEXT_WEB_PORT": "invalid_port",
            "FLEXT_WEB_DEBUG": "invalid_boolean",
        }

        with patch.dict(os.environ, env_vars, clear=False):
            result = FlextWebConfigs.create_config_from_env()

            assert result.is_failure
            # Environment variable conversion error is now caught properly
            assert result.error is not None
            assert (
                "invalid literal for int()" in result.error.lower()
                or "validation" in result.error.lower()
            )

    def test_create_web_config_alternative_methods(self) -> None:
        """Test alternative config creation methods."""
        # Test with custom parameters passed directly to WebConfig
        config = FlextWebConfigs.WebConfig(
            host="dict-host",
            port=6666,
            debug=False,
            secret_key="dict-secret-key-that-is-long-enough-for-validation-12345",
        )

        assert config.host == "dict-host"
        assert config.port == 6666
        assert config.debug is False

    def test_create_config_validation_error_direct(self) -> None:
        """Test config validation through direct instantiation."""
        # This should fail due to invalid port
        with pytest.raises((ValueError, ValidationError)) as exc_info:
            FlextWebConfigs.WebConfig(
                host="valid-host",
                port=-1,  # Invalid port
                debug=False,
                secret_key="valid-secret-key-that-is-long-enough-12345",
            )
        assert (
            "port" in str(exc_info.value).lower()
            or "validation" in str(exc_info.value).lower()
        )


class TestWebConfigEdgeCases:
    """Test edge cases and error conditions."""

    def test_config_with_extreme_values(self) -> None:
        """Test config with boundary values."""
        config = FlextWebConfigs.WebConfig(
            host="a" * 255,  # Very long hostname
            port=65535,  # Maximum port
            app_name="X" * 100,  # Long app name
            max_content_length=1,  # Minimum content length
            request_timeout=1,  # Minimum timeout
        )

        assert len(config.host) == 255
        assert config.port == 65535
        assert len(config.app_name) == 100

    def test_config_model_dump(self) -> None:
        """Test config serialization."""
        config = FlextWebConfigs.WebConfig(host="test-host", port=8080, debug=True)

        config_dict = config.model_dump()

        assert isinstance(config_dict, dict)
        assert config_dict["host"] == "test-host"
        assert config_dict["port"] == 8080
        assert config_dict["debug"] is True

    def test_config_model_copy(self) -> None:
        """Test config copying with updates."""
        original = FlextWebConfigs.WebConfig(host="original-host", port=8080)

        copied = original.model_copy(update={"host": "updated-host"})

        assert original.host == "original-host"
        assert copied.host == "updated-host"
        assert copied.port == 8080  # Preserved from original

    def test_config_repr_and_str(self) -> None:
        """Test config string representations."""
        config = FlextWebConfigs.WebConfig(host="test-host", port=8080)

        repr_str = repr(config)
        str_str = str(config)

        assert "WebConfig" in repr_str
        assert "test-host" in str_str
        assert "8080" in str_str
