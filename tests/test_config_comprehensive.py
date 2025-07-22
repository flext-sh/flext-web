"""Comprehensive tests for config.py to improve coverage."""

from __future__ import annotations

import pytest

from flext_web.config import WebConfig, get_web_settings


class TestWebConfigBasic:
    """Test WebConfig basic functionality."""

    def test_web_config_creation(self) -> None:
        """Test basic WebConfig creation."""
        config = WebConfig()
        assert config.title == "FLEXT Web"
        assert config.version is not None

    def test_web_config_with_custom_title(self) -> None:
        """Test WebConfig with custom title."""
        config = WebConfig(title="Custom Web App")
        assert config.title == "Custom Web App"

    def test_web_config_django_settings(self) -> None:
        """Test Django-related settings."""
        config = WebConfig()
        assert config.django_secret_key is not None
        assert len(config.django_secret_key) >= 50
        assert isinstance(config.django_debug, bool)
        assert isinstance(config.django_allowed_hosts, list)

    def test_web_config_database_config(self) -> None:
        """Test database configuration."""
        config = WebConfig()
        db_config = config.django_database_config
        assert "default" in db_config
        assert "ENGINE" in db_config["default"]
        assert db_config["default"]["ENGINE"] == "django.db.backends.postgresql"

    def test_web_config_secret_key_validation(self) -> None:
        """Test secret key validation."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError, match="String should have at least 50 characters"):
            WebConfig(django_secret_key="short")

    def test_web_config_x_frame_options_validation(self) -> None:
        """Test X-Frame-Options validation."""
        config = WebConfig(x_frame_options="DENY")
        assert config.x_frame_options == "DENY"

        config = WebConfig(x_frame_options="sameorigin")
        assert config.x_frame_options == "SAMEORIGIN"

        from pydantic import ValidationError

        with pytest.raises(ValidationError, match="X-Frame-Options must be one of"):
            WebConfig(x_frame_options="INVALID")

    def test_web_config_development_production_properties(self) -> None:
        """Test development/production detection properties."""
        config = WebConfig(django_debug=True)
        assert config.is_development is True
        assert config.is_production is False

        config = WebConfig(django_debug=False)
        # is_production depends on database URL and debug flag
        assert isinstance(config.is_production, bool)

    def test_web_config_validation_method(self) -> None:
        """Test configuration validation method."""
        config = WebConfig()
        errors = config.validate_configuration()
        assert isinstance(errors, list)

    def test_get_web_settings_function(self) -> None:
        """Test get_web_settings singleton function."""
        settings1 = get_web_settings()
        settings2 = get_web_settings()

        assert isinstance(settings1, WebConfig)
        assert settings1 is settings2  # Should be same instance (singleton)
