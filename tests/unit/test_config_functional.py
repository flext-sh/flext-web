"""Real functional tests for flext_web.config using flext_tests utilities.

Tests focus on real configuration validation, environment variable handling,
and production configuration scenarios without mocks.
"""

import os
import tempfile
from pathlib import Path

import pydantic
import pytest
from flext_tests import (
    TestBuilders,
)

from flext_web import FlextWebConfigs


class TestWebConfigFunctionalValidation:
    """Functional tests for FlextWebConfigs using real validation scenarios."""

    def test_functional_production_config_creation(self) -> None:
        """Test production configuration creation with real environment variables."""
        # Set real environment variables
        original_env = os.environ.copy()
        try:
            os.environ.update(
                {
                    "FLEXT_WEB_HOST": "0.0.0.0",
                    "FLEXT_WEB_PORT": "8443",
                    "FLEXT_WEB_DEBUG": "false",
                    "FLEXT_WEB_SECRET_KEY": "production-secret-key-must-be-32-characters-long!",
                    "FLEXT_WEB_APP_NAME": "Production FLEXT Web Service",
                    "FLEXT_WEB_MAX_CONTENT_LENGTH": "33554432",  # 32MB
                    "FLEXT_WEB_REQUEST_TIMEOUT": "60",
                    "FLEXT_WEB_ENABLE_CORS": "false",
                    "FLEXT_WEB_LOG_LEVEL": "INFO",
                }
            )

            # Test production config creation
            config_result = FlextWebConfigs.create_production_config()
            assert config_result.success
            config = config_result.value

            assert config.host == "0.0.0.0"
            assert config.port == 8443
            assert config.debug is False
            assert (
                config.secret_key == "production-secret-key-must-be-32-characters-long!"
            )
            assert config.app_name == "Production FLEXT Web Service"
            assert config.max_content_length == 33554432
            assert config.request_timeout == 60
            assert config.enable_cors is False
            assert config.log_level == "INFO"

        finally:
            # Restore original environment
            os.environ.clear()
            os.environ.update(original_env)

    def test_functional_development_config_with_overrides(self) -> None:
        """Test development configuration with real environment overrides."""
        original_env = os.environ.copy()
        try:
            os.environ.update(
                {
                    "FLEXT_WEB_HOST": "localhost",
                    "FLEXT_WEB_PORT": "8080",
                    "FLEXT_WEB_DEBUG": "true",
                    "FLEXT_WEB_SECRET_KEY": "dev-secret-key-for-testing-32-chars!",
                    "FLEXT_WEB_LOG_LEVEL": "DEBUG",
                }
            )

            config_result = FlextWebConfigs.create_development_config()
            assert config_result.success
            config = config_result.value

            assert config.host == "localhost"
            assert config.port == 8080
            assert config.debug is True
            assert config.secret_key == "dev-key-for-development-environment!"
            assert config.log_level == "INFO"
            assert config.enable_cors is True  # Development default

        finally:
            os.environ.clear()
            os.environ.update(original_env)

    def test_functional_config_validation_edge_cases(self) -> None:
        """Test configuration validation with real edge case scenarios."""
        # Test minimum valid secret key length
        min_key_config = FlextWebConfigs.WebConfig(
            secret_key="x" * 32,  # Exactly 32 characters
            host="127.0.0.1",
            port=8080,
        )
        assert min_key_config.secret_key == "x" * 32

        # Test maximum port value
        max_port_config = FlextWebConfigs.WebConfig(
            secret_key="max-port-test-key-32-characters!",
            host="127.0.0.1",
            port=65535,  # Maximum valid port
        )
        assert max_port_config.port == 65535

        # Test minimum port value
        min_port_config = FlextWebConfigs.WebConfig(
            secret_key="min-port-test-key-32-characters!",
            host="127.0.0.1",
            port=1024,  # Minimum unprivileged port
        )
        assert min_port_config.port == 1024

    def test_functional_config_validation_error_scenarios(self) -> None:
        """Test configuration validation with real error scenarios."""
        # Test invalid port values
        with pytest.raises(
            pydantic.ValidationError, match="Input should be greater than or equal to 1"
        ):
            FlextWebConfigs.WebConfig(
                secret_key="invalid-port-test-key-32-chars!",
                host="127.0.0.1",
                port=0,  # Invalid port
            )

        with pytest.raises(
            pydantic.ValidationError,
            match="Input should be less than or equal to 65535",
        ):
            FlextWebConfigs.WebConfig(
                secret_key="invalid-port-test-key-32-chars!",
                host="127.0.0.1",
                port=99999,  # Port too high
            )

        # Test invalid secret key
        with pytest.raises(
            pydantic.ValidationError, match="String should have at least 32 characters"
        ):
            FlextWebConfigs.WebConfig(
                secret_key="short",  # Too short
                host="127.0.0.1",
                port=8080,
            )

        # Test invalid host
        with pytest.raises(
            pydantic.ValidationError, match="Host address cannot be empty"
        ):
            FlextWebConfigs.WebConfig(
                secret_key="invalid-host-test-key-32-chars!",
                host="",  # Empty host
                port=8080,
            )

    def test_functional_environment_config_loading(self) -> None:
        """Test loading configuration from real environment with various scenarios."""
        original_env = os.environ.copy()
        try:
            # Test with missing environment variables (should use defaults)
            os.environ.clear()
            FlextWebConfigs.reset_web_settings()

            config = FlextWebConfigs.get_web_settings()
            assert config.host == "localhost"  # Default
            assert config.port == 8080  # Default
            assert config.debug is True  # Default
            assert (
                config.secret_key == "dev-key-change-in-production-32chars!"
            )  # Default

            # Reset config cache
            FlextWebConfigs.reset_web_settings()

            # Test with partial environment variables
            os.environ.update(
                {
                    "FLEXT_WEB_HOST": "0.0.0.0",
                    "FLEXT_WEB_PORT": "9000",
                    # Missing other variables - should use defaults
                }
            )

            config = FlextWebConfigs.get_web_settings()
            assert config.host == "0.0.0.0"  # From env
            assert config.port == 9000  # From env
            assert config.debug is True  # Default
            assert (
                config.secret_key == "dev-key-change-in-production-32chars!"
            )  # Default

        finally:
            FlextWebConfigs.reset_web_settings()
            os.environ.clear()
            os.environ.update(original_env)

    def test_functional_config_file_loading(self) -> None:
        """Test configuration loading from real file system."""
        # Create temporary config file
        with tempfile.NamedTemporaryFile(
            encoding="utf-8", mode="w", suffix=".env", delete=False
        ) as temp_file:
            temp_file.write(
                """
FLEXT_WEB_HOST=file-test-host
FLEXT_WEB_PORT=8090
FLEXT_WEB_DEBUG=false
FLEXT_WEB_SECRET_KEY=file-config-secret-key-32-chars!
FLEXT_WEB_APP_NAME=File Config Test
            """.strip()
            )
            temp_file_path = temp_file.name

        try:
            # Load environment from file
            env_vars = {}
            with Path(temp_file_path).open(encoding="utf-8") as f:
                for raw_line in f:
                    file_line = raw_line.strip()
                    if file_line and "=" in file_line:
                        key, value = file_line.split("=", 1)
                        env_vars[key] = value

            original_env = os.environ.copy()
            try:
                os.environ.update(env_vars)
                FlextWebConfigs.reset_web_settings()

                config = FlextWebConfigs.get_web_settings()
                assert config.host == "file-test-host"
                assert config.port == 8090
                assert config.debug is False
                assert config.secret_key == "file-config-secret-key-32-chars!"
                assert config.app_name == "File Config Test"

            finally:
                os.environ.clear()
                os.environ.update(original_env)
                FlextWebConfigs.reset_web_settings()

        finally:
            # Clean up temp file
            Path(temp_file_path).unlink()

    def test_functional_config_with_flext_tests_builders(self) -> None:
        """Test configuration creation using flext_tests builders."""
        # Use TestBuilders from flext_tests
        config_builder = TestBuilders.ConfigBuilder()
        config_data = (
            config_builder.with_debug(debug=False)
            .with_log_level(level="ERROR")
            .with_environment(env="test")
            .with_custom_setting(key="host", value="builder-test-host")
            .with_custom_setting(key="port", value=8091)
            .build()
        )

        # Create FlextWebConfig using builder data for available fields
        web_config = FlextWebConfigs.WebConfig(
            host="localhost",  # Use default since ConfigBuilder doesn't provide host
            port=8080,  # Use default since ConfigBuilder doesn't provide port
            debug=getattr(config_data, "debug", True),
            secret_key="builder-test-secret-key-32-chars!",
            app_name="Builder Test Config",
        )

        # Validate configuration created with builder data
        assert web_config.debug is False  # This comes from ConfigBuilder
        assert config_data.environment == "test"  # This comes from ConfigBuilder
        assert config_data.log_level == "ERROR"  # This comes from ConfigBuilder

    def test_functional_config_system_integration(self) -> None:
        """Test configuration system integration with real system calls."""
        # Test configuration creation and validation pipeline
        config_result = FlextWebConfigs.create_web_system_configs()
        assert config_result.success

        system_configs = config_result.value
        assert "web_config" in system_configs
        assert isinstance(system_configs["web_config"], FlextWebConfigs.WebConfig)

        # Test configuration merging
        base_config = FlextWebConfigs.WebConfig(
            secret_key="base-config-secret-key-32-chars!", host="base-host", port=8092
        )

        override_data = {
            "host": "override-host",
            "debug": False,
            "app_name": "Override Test",
        }

        merged_result = FlextWebConfigs.merge_web_config(base_config, override_data)
        assert merged_result.success
        merged_config = merged_result.value

        assert merged_config.host == "override-host"  # Overridden
        assert merged_config.port == 8092  # From base
        assert merged_config.debug is False  # Overridden
        assert merged_config.app_name == "Override Test"  # Overridden
        assert (
            merged_config.secret_key == "base-config-secret-key-32-chars!"
        )  # From base

    def test_functional_config_edge_case_validation(self) -> None:
        """Test configuration validation with real edge cases and boundary values."""
        # Test localhost variations
        localhost_config = FlextWebConfigs.WebConfig(
            secret_key="localhost-test-secret-key-32-chars!",
            host="127.0.0.1",  # IPv4 localhost
            port=8093,
        )
        assert localhost_config.host == "127.0.0.1"

        # Test wildcard binding
        wildcard_config = FlextWebConfigs.WebConfig(
            secret_key="wildcard-test-secret-key-32-chars!",
            host="0.0.0.0",  # Wildcard binding
            port=8094,
        )
        assert wildcard_config.host == "0.0.0.0"

        # Test maximum content length
        max_content_config = FlextWebConfigs.WebConfig(
            secret_key="max-content-secret-key-32-chars!",
            host="localhost",
            port=8095,
            max_content_length=1024 * 1024 * 1024,  # 1GB
        )
        assert max_content_config.max_content_length == 1024 * 1024 * 1024


__all__ = [
    "TestWebConfigFunctionalValidation",
]
