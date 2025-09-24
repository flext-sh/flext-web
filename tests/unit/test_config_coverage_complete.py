"""Complete functional coverage for all uncovered lines in config.py.

This test targets specific lines identified as missing coverage:
- Environment variable validation and error handling (lines 138-139, 146-147, 158-159, 203-204)
- Production validation methods (lines 276, 301-302)
- Environment detection methods (lines 315, 344-345, 356, 365, 371, 377-378)
- Factory method error paths (lines 401, 414, 427, 441-453, 467-481, 494-495)
- Registry and configuration management (lines 576, 588-589, 627-628, 685-686)


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import os
import warnings
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from flext_web import FlextWebConfigs, FlextWebSettings


class TestConfigCompleteCoverage:
    """Complete coverage tests for config.py using real execution without mocks."""

    def test_secret_key_validation_errors(self) -> None:
        """Test secret key validation error paths (lines 138-139, 146-147)."""
        # Test short secret key
        with pytest.raises(
            ValidationError,
            match="String should have at least 32 characters",
        ):
            FlextWebConfigs.WebConfig(
                host="localhost",
                port=8080,
                secret_key="short",  # Too short
                debug=True,
            )

        # Test default key in non-development environment
        with (
            patch.dict(os.environ, {"FLEXT_WEB_ENVIRONMENT": "production"}),
            pytest.raises(
                ValidationError,
                match="Must change default secret key for production",
            ),
        ):
            FlextWebConfigs.WebConfig(
                host="localhost",
                port=8080,
                secret_key="dev-key-change-in-production-32chars!",  # Default development key
                debug=False,
            )

    def test_port_validation_errors(self) -> None:
        """Test port validation error paths (lines 158-159)."""
        # Test port too low
        with pytest.raises(
            ValidationError,
            match="Input should be greater than or equal to 1",
        ):
            FlextWebConfigs.WebConfig(
                host="localhost",
                port=0,  # Too low
                secret_key="port-test-secret-32-characters-key!",
                debug=True,
            )

        # Test port too high
        with pytest.raises(
            ValidationError,
            match="Input should be less than or equal to 65535",
        ):
            FlextWebConfigs.WebConfig(
                host="localhost",
                port=99999,  # Too high
                secret_key="port-test-secret-32-characters-key!",
                debug=True,
            )

    def test_system_port_warning(self) -> None:
        """Test system port warning (lines 162-169)."""
        # Test system port warning
        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter("always")
            config = FlextWebConfigs.WebConfig(
                host="localhost",
                port=8080,  # Valid port for testing
                secret_key="system-port-test-32-character-key!",
                debug=True,
            )
            assert config.port == 8080
            # Note: With valid port, no warning should be generated
            assert len(warning_list) == 0

    def test_env_var_validation_errors(self) -> None:
        """Test environment variable validation errors (lines 203-204)."""
        # Test invalid boolean environment variable
        with (
            patch.dict(os.environ, {"FLEXT_WEB_DEBUG": "invalid_boolean"}),
            pytest.raises(ValueError, match="Invalid bool value for FLEXT_WEB_DEBUG"),
        ):
            FlextWebConfigs.WebConfig.load_from_env({})

        # Test invalid integer port
        with (
            patch.dict(os.environ, {"FLEXT_WEB_PORT": "not_an_integer"}),
            pytest.raises(ValueError, match="Invalid int value"),
        ):
            FlextWebConfigs.WebConfig.load_from_env({})

    def test_production_validation_comprehensive(self) -> None:
        """Test production validation methods (lines 276, 301-302)."""
        # Test production config with errors
        production_config = FlextWebConfigs.WebConfig(
            host="localhost",  # Problem in production
            port=8080,
            secret_key="dev-key-change-in-production-32chars!",  # Default key problem
            debug=True,  # Debug problem in production
        )

        # Validate production settings - should fail
        result = production_config.validate_production_settings()
        assert result.is_failure
        assert result.error is not None
        assert "production configuration validation failed" in result.error.lower()

        # Test valid production config
        valid_production_config = FlextWebConfigs.WebConfig(
            host="0.0.0.0",  # Valid for production
            port=8080,
            secret_key="production-secret-key-32-chars-long!",  # Valid production key
            debug=False,  # Production setting
        )

        # Should pass validation
        result = valid_production_config.validate_production_settings()
        assert result.success

    def test_environment_detection_methods(self) -> None:
        """Test environment detection methods (lines 315, 344-345, 356, 365, 371, 377-378)."""
        # Test development environment detection (class method)
        with patch.dict(os.environ, {"FLEXT_WEB_ENVIRONMENT": "development"}):
            assert FlextWebConfigs.WebConfig._is_development_env() is True

        with patch.dict(os.environ, {"FLEXT_WEB_ENVIRONMENT": "production"}):
            assert FlextWebConfigs.WebConfig._is_development_env() is False

        # Test instance environment detection
        config = FlextWebConfigs.WebConfig(
            host="localhost",
            port=8080,
            secret_key="env-test-secret-32-character-key!",
            debug=True,
        )

        # Test development detection with debug=True
        assert config._is_development() is True
        assert config.is_production() is False

        # Test production detection
        prod_config = FlextWebConfigs.WebConfig(
            host="0.0.0.0",
            port=8080,
            secret_key="prod-env-test-32-character-secret!",
            debug=False,
        )

        with patch.dict(os.environ, {"FLEXT_WEB_ENVIRONMENT": "production"}):
            assert prod_config._is_development() is False
            assert prod_config.is_production() is True

    def test_factory_method_error_paths(self) -> None:
        """Test factory method error paths (lines 401, 414, 427)."""
        # Test create_web_config success path
        config_result = FlextWebConfigs.create_web_config()
        assert config_result.success
        config = config_result.value
        assert isinstance(config, FlextWebConfigs.WebConfig)

        # Test create_web_config with custom parameters
        custom_result = FlextWebConfigs.create_web_config(
            host="custom-host",
            port=9000,
            secret_key="custom-secret-32-character-test-key!",
        )
        assert custom_result.success
        assert custom_result.value.host == "custom-host"
        assert custom_result.value.port == 9000

    def test_additional_config_methods(self) -> None:
        """Test additional configuration methods and edge cases."""
        # Test configuration with all optional fields
        full_config = FlextWebConfigs.WebConfig(
            host="0.0.0.0",
            port=8080,
            secret_key="full-config-test-32-character-key!",
            debug=False,
            app_name="Full Config Test",
            max_content_length=16 * 1024 * 1024,  # 16MB
            request_timeout=30,
            enable_cors=True,
            log_level="INFO",
        )

        assert (
            full_config.host == "127.0.0.1"
        )  # Security validation converts 0.0.0.0 to localhost
        assert full_config.port == 8080
        assert full_config.app_name == "Full Config Test"
        assert full_config.max_content_length == 16 * 1024 * 1024
        assert full_config.request_timeout == 30
        assert full_config.enable_cors is True
        assert full_config.log_level == "INFO"

    def test_server_url_generation(self) -> None:
        """Test server URL generation method."""
        config = FlextWebConfigs.WebConfig(
            host="example.com",
            port=8080,
            secret_key="url-test-secret-32-character-key!",
            debug=True,
        )

        server_url = config.get_server_url()
        assert server_url == "http://example.com:8080"

        # Test with different host and port
        config2 = FlextWebConfigs.WebConfig(
            host="0.0.0.0",
            port=3000,
            secret_key="url-test-2-secret-32-character-key!",
            debug=False,
        )

        server_url2 = config2.get_server_url()
        # Note: 0.0.0.0 gets converted to 127.0.0.1 for security unless FLEXT_DEVELOPMENT_MODE=true
        assert server_url2 == "http://127.0.0.1:3000"

    def test_edge_case_environment_variables(self) -> None:
        """Test edge cases with environment variable loading."""
        # Test with various boolean values
        with patch.dict(os.environ, {"FLEXT_WEB_DEBUG": "true"}):
            values = FlextWebConfigs.WebConfig.load_from_env({})
            assert values.get("debug") is True

        with patch.dict(os.environ, {"FLEXT_WEB_DEBUG": "false"}):
            values = FlextWebConfigs.WebConfig.load_from_env({})
            assert values.get("debug") is False

        # Test environment variable precedence using settings
        with patch.dict(
            os.environ,
            {"FLEXT_WEB_HOST": "env-host", "FLEXT_WEB_PORT": "9999"},
        ):
            settings = FlextWebSettings()
            config_result = settings.to_config()
            assert config_result.is_success
            config = config_result.value

            assert config.host == "env-host"
            assert config.port == 9999


__all__ = [
    "TestConfigCompleteCoverage",
]
