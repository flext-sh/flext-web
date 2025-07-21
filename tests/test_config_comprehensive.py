"""Comprehensive tests for config.py to improve coverage."""

from __future__ import annotations

import pytest
from django.test import TestCase

from flext_web.config import (
    DjangoCacheConfig,
    DjangoDatabaseConfig,
    DjangoSecurityConfig,
    WebConfig,
    get_web_config,
)


class TestDjangoSecurityConfigValidation(TestCase):
    """Test DjangoSecurityConfig validation."""

    def test_secret_key_validation_success(self) -> None:
        """Test secret key validation with valid key."""
        config = DjangoSecurityConfig(
            secret_key="x" * 50,  # Exactly 50 characters
            debug=True,
        )
        assert len(config.secret_key) == 50

    def test_secret_key_validation_failure(self) -> None:
        """Test secret key validation with invalid key."""
        from pydantic import ValidationError

        with pytest.raises(
            ValidationError,
            match="String should have at least 50 characters",
        ):
            DjangoSecurityConfig(secret_key="short")

    def test_security_config_defaults(self) -> None:
        """Test DjangoSecurityConfig default values."""
        config = DjangoSecurityConfig()

        assert config.debug is False
        assert len(config.secret_key) >= 50
        assert "localhost" in config.allowed_hosts
        assert "127.0.0.1" in config.allowed_hosts
        assert config.csrf_trusted_origins == []
        assert config.secure_ssl_redirect is False
        assert config.secure_hsts_seconds == 0

    def test_security_config_custom_values(self) -> None:
        """Test DjangoSecurityConfig with custom values."""
        config = DjangoSecurityConfig(
            secret_key="x" * 60,
            debug=True,
            allowed_hosts=["example.com", "localhost"],
            csrf_trusted_origins=["https://example.com"],
            secure_ssl_redirect=True,
            secure_hsts_seconds=31536000,
        )

        assert config.debug is True
        assert config.allowed_hosts == ["example.com", "localhost"]
        assert config.csrf_trusted_origins == ["https://example.com"]
        assert config.secure_ssl_redirect is True
        assert config.secure_hsts_seconds == 31536000


class TestDjangoDatabaseConfig(TestCase):
    """Test DjangoDatabaseConfig functionality."""

    def test_database_config_defaults(self) -> None:
        """Test DjangoDatabaseConfig default values."""
        config = DjangoDatabaseConfig()

        assert config.engine == "django.db.backends.postgresql"
        assert config.name == "flext_web"
        assert config.user == "postgres"
        assert config.password == ""
        assert config.host == "localhost"
        assert config.port == 5432
        assert config.conn_max_age == 600

    def test_database_config_to_django_config(self) -> None:
        """Test conversion to Django database configuration."""
        config = DjangoDatabaseConfig(
            name="test_db",
            user="test_user",
            password="test_pass",
            host="db.example.com",
            port=5433,
        )

        django_config = config.to_django_config()

        assert django_config["ENGINE"] == "django.db.backends.postgresql"
        assert django_config["NAME"] == "test_db"
        assert django_config["USER"] == "test_user"
        assert django_config["PASSWORD"] == "test_pass"
        assert django_config["HOST"] == "db.example.com"
        assert django_config["PORT"] == 5433
        assert django_config["CONN_MAX_AGE"] == 600
        assert django_config["CONN_HEALTH_CHECKS"] is True

    def test_database_config_port_validation(self) -> None:
        """Test database port validation."""
        # Valid port
        config = DjangoDatabaseConfig(port=5432)
        assert config.port == 5432

        # Test boundary values
        config_min = DjangoDatabaseConfig(port=1)
        assert config_min.port == 1

        config_max = DjangoDatabaseConfig(port=65535)
        assert config_max.port == 65535


class TestDjangoCacheConfig(TestCase):
    """Test DjangoCacheConfig functionality."""

    def test_cache_config_defaults(self) -> None:
        """Test DjangoCacheConfig default values."""
        config = DjangoCacheConfig()

        assert config.backend == "django.core.cache.backends.redis.RedisCache"
        assert config.location == "redis://localhost:6379/1"
        assert config.timeout == 300

    def test_cache_config_to_django_config(self) -> None:
        """Test conversion to Django cache configuration."""
        config = DjangoCacheConfig(
            backend="django.core.cache.backends.dummy.DummyCache",
            location="dummy://localhost",
            timeout=600,
        )

        django_config = config.to_django_config()

        assert django_config["BACKEND"] == "django.core.cache.backends.dummy.DummyCache"
        assert django_config["LOCATION"] == "dummy://localhost"
        assert django_config["TIMEOUT"] == 600

    def test_cache_config_timeout_validation(self) -> None:
        """Test cache timeout validation."""
        # Valid timeout values
        config_min = DjangoCacheConfig(timeout=0)
        assert config_min.timeout == 0

        config_max = DjangoCacheConfig(timeout=3600)
        assert config_max.timeout == 3600


class TestWebConfigValidation(TestCase):
    """Test WebConfig validation and model validators."""

    def test_web_config_debug_consistency_validation(self) -> None:
        """Test that debug mode consistency is enforced."""
        # Test case where main debug=True but security.debug=False
        config = WebConfig(
            debug=True,
            security=DjangoSecurityConfig(debug=False),
        )

        # After validation, security.debug should be True
        assert config.debug is True
        assert config.security.debug is True

    def test_web_config_production_secret_key_validation(self) -> None:
        """Test production secret key validation."""
        # Should raise error when debug=False and secret key starts with 'development-key'
        with pytest.raises(ValueError, match="Production secret key must be set"):
            WebConfig(
                debug=False,
                security=DjangoSecurityConfig(
                    secret_key="development-key-" + "x" * 50,
                ),
            )

    def test_web_config_production_with_valid_secret(self) -> None:
        """Test production config with valid secret key."""
        config = WebConfig(
            debug=False,
            security=DjangoSecurityConfig(
                secret_key="production-secret-" + "x" * 50,
            ),
        )

        assert config.debug is False
        assert not config.security.secret_key.startswith("development-key")

    def test_web_config_development_mode_allowed(self) -> None:
        """Test that development mode allows development secret key."""
        config = WebConfig(
            debug=True,
            security=DjangoSecurityConfig(
                secret_key="development-key-" + "x" * 50,
            ),
        )

        assert config.debug is True
        assert config.security.secret_key.startswith("development-key")

    def test_web_config_get_django_databases(self) -> None:
        """Test get_django_databases method."""
        config = WebConfig(
            database=DjangoDatabaseConfig(
                name="test_db",
                user="test_user",
            ),
        )

        databases = config.get_django_databases()

        assert "default" in databases
        assert databases["default"]["NAME"] == "test_db"
        assert databases["default"]["USER"] == "test_user"

    def test_web_config_get_django_caches(self) -> None:
        """Test get_django_caches method."""
        config = WebConfig(
            cache=DjangoCacheConfig(
                timeout=1200,
                location="redis://cache.example.com:6379/2",
            ),
        )

        caches = config.get_django_caches()

        assert "default" in caches
        assert caches["default"]["TIMEOUT"] == 1200
        assert caches["default"]["LOCATION"] == "redis://cache.example.com:6379/2"

    def test_web_config_defaults(self) -> None:
        """Test WebConfig default values."""
        config = WebConfig()

        assert config.project_name == "flext-web"
        assert config.version == "0.7.0"
        assert config.time_zone == "UTC"
        assert config.language_code == "en-us"
        assert config.use_i18n is True
        assert config.use_tz is True
        assert config.api_version == "v1"
        assert config.api_title == "FLEXT Web API"
        assert config.session_cookie_age == 86400  # Actual default (1 day)
        assert config.debug is True  # Actual default in test environment

    def test_web_config_session_cookie_age_validation(self) -> None:
        """Test session cookie age validation."""
        # Valid values
        config_min = WebConfig(session_cookie_age=3600)  # 1 hour
        assert config_min.session_cookie_age == 3600

        config_max = WebConfig(session_cookie_age=2592000)  # 30 days
        assert config_max.session_cookie_age == 2592000


class TestGetWebConfig(TestCase):
    """Test get_web_config singleton function."""

    def test_get_web_config_returns_instance(self) -> None:
        """Test that get_web_config returns WebConfig instance."""
        config = get_web_config()

        assert isinstance(config, WebConfig)

    def test_get_web_config_has_expected_defaults(self) -> None:
        """Test that get_web_config has expected default values."""
        config = get_web_config()

        assert config.project_name == "flext-web"
        assert config.version == "0.7.0"
        assert hasattr(config, "security")
        assert hasattr(config, "database")
        assert hasattr(config, "cache")


class TestWebConfigComplexScenarios(TestCase):
    """Test complex WebConfig scenarios and edge cases."""

    def test_web_config_with_all_custom_values(self) -> None:
        """Test WebConfig with all custom configuration."""
        security_config = DjangoSecurityConfig(
            secret_key="custom-secret-" + "x" * 50,
            debug=True,
            allowed_hosts=["custom.com"],
            secure_ssl_redirect=True,
        )

        database_config = DjangoDatabaseConfig(
            name="custom_db",
            user="custom_user",
            password="custom_pass",
            host="custom.host.com",
            port=5433,
        )

        cache_config = DjangoCacheConfig(
            backend="django.core.cache.backends.locmem.LocMemCache",
            location="unique-snowflake",
            timeout=1800,
        )

        config = WebConfig(
            project_name="custom-project",
            version="1.0.0",
            security=security_config,
            database=database_config,
            cache=cache_config,
            debug=True,
            time_zone="America/New_York",
            language_code="es-es",
            api_version="v2",
            session_cookie_age=7200,
        )

        # Verify all custom values are set
        assert config.project_name == "custom-project"
        assert config.version == "1.0.0"
        assert config.debug is True
        assert config.time_zone == "America/New_York"
        assert config.language_code == "es-es"
        assert config.api_version == "v2"
        assert config.session_cookie_age == 7200

        # Verify nested configs
        assert config.security.allowed_hosts == ["custom.com"]
        assert config.database.name == "custom_db"
        assert config.cache.timeout == 1800

    def test_web_config_frozen_model(self) -> None:
        """Test that WebConfig is frozen (immutable)."""
        config = WebConfig()

        # Should not be able to modify after creation
        with pytest.raises(ValueError, match=".*frozen.*"):
            config.debug = True
