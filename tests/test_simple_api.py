"""Tests for simple_api.py web configuration functions."""

from __future__ import annotations

from typing import Any
from unittest.mock import patch

from django.test import TestCase
from flext_core import ServiceResult

from flext_web.config import WebConfig
from flext_web.simple_api import get_web_settings, setup_web


class TestGetWebSettings(TestCase):
    """Test get_web_settings function."""

    def test_get_web_settings_returns_config(self) -> None:
        """Test that get_web_settings returns a WebConfig instance."""
        config = get_web_settings()

        assert isinstance(config, WebConfig)
        assert config.project_name == "flext-web"
        assert config.version == "0.7.0"

    def test_get_web_settings_has_default_values(self) -> None:
        """Test that returned config has expected default values."""
        config = get_web_settings()

        assert config.debug is True  # Actual default in test environment
        assert config.time_zone == "UTC"
        assert config.language_code == "en-us"
        assert config.use_i18n is True
        assert config.use_tz is True

    def test_get_web_settings_has_security_config(self) -> None:
        """Test that security configuration is properly initialized."""
        config = get_web_settings()

        assert hasattr(config, "security")
        # In test environment, debug modes should be consistent
        assert config.security.debug == config.debug
        assert config.security.allowed_hosts == ["localhost", "127.0.0.1"]
        assert len(config.security.secret_key) >= 50

    def test_get_web_settings_has_database_config(self) -> None:
        """Test that database configuration is properly initialized."""
        config = get_web_settings()

        assert hasattr(config, "database")
        assert config.database.engine == "django.db.backends.postgresql"
        assert config.database.name == "flext_web"
        assert config.database.port == 5432

    def test_get_web_settings_has_cache_config(self) -> None:
        """Test that cache configuration is properly initialized."""
        config = get_web_settings()

        assert hasattr(config, "cache")
        assert config.cache.backend == "django.core.cache.backends.redis.RedisCache"
        assert config.cache.location == "redis://localhost:6379/1"
        assert config.cache.timeout == 300


class TestSetupWeb(TestCase):
    """Test setup_web function."""

    def test_setup_web_with_default_settings(self) -> None:
        """Test setup_web with default settings (None)."""
        result = setup_web()

        assert isinstance(result, ServiceResult)
        assert result.is_successful is True
        assert result.data is True

    def test_setup_web_with_provided_settings(self) -> None:
        """Test setup_web with provided WebConfig."""
        config = WebConfig()
        result = setup_web(config)

        assert isinstance(result, ServiceResult)
        assert result.is_successful is True
        assert result.data is True

    def test_setup_web_success_result(self) -> None:
        """Test that setup_web returns success ServiceResult."""
        result = setup_web()

        assert result.is_successful is True
        assert result.error is None
        assert result.data is True

    @patch("flext_web.simple_api.WebConfig", side_effect=Exception("Config error"))
    def test_setup_web_handles_exception(self, mock_config: Any) -> None:
        """Test that setup_web handles exceptions gracefully."""
        result = setup_web()

        assert isinstance(result, ServiceResult)
        assert result.is_successful is False
        assert result.is_successful is False
        assert "Web setup failed: Config error" in result.error

    @patch("flext_web.simple_api.WebConfig")
    def test_setup_web_creates_config_when_none(self, mock_config: Any) -> None:
        """Test that setup_web creates WebConfig when None is provided."""
        result = setup_web(None)

        # Should call WebConfig() once when settings is None
        mock_config.assert_called_once()
        assert result.is_successful is True

    def test_setup_web_with_custom_config(self) -> None:
        """Test setup_web with a custom WebConfig instance."""
        custom_config = WebConfig(
            debug=True,
            time_zone="America/New_York",
        )

        result = setup_web(custom_config)

        assert result.is_successful is True
        assert result.data is True

    def test_setup_web_validates_config_object(self) -> None:
        """Test that setup_web works with valid WebConfig object."""
        config = get_web_settings()  # Get a valid config
        result = setup_web(config)

        assert result.is_successful is True
        assert isinstance(result, ServiceResult)


class TestSimpleApiIntegration(TestCase):
    """Integration tests for simple_api module."""

    def test_module_imports_correctly(self) -> None:
        """Test that all imports work correctly."""
        from flext_web import simple_api

        # Check main functions are available
        assert hasattr(simple_api, "get_web_settings")
        assert hasattr(simple_api, "setup_web")
        assert callable(simple_api.get_web_settings)
        assert callable(simple_api.setup_web)

    def test_integration_get_settings_and_setup(self) -> None:
        """Test integration between get_web_settings and setup_web."""
        # Get settings first
        config = get_web_settings()

        # Use those settings in setup
        result = setup_web(config)

        assert isinstance(config, WebConfig)
        assert result.is_successful is True

    def test_service_result_type_annotations(self) -> None:
        """Test that ServiceResult is properly typed."""
        result = setup_web()

        # Verify ServiceResult methods work
        assert hasattr(result, "is_successful")
        assert hasattr(result, "is_success")
        assert hasattr(result, "error")
        assert hasattr(result, "data")

        # Test success case properties
        assert result.is_successful is True
        assert result.is_success is True
        assert result.error is None
        assert result.data is True
