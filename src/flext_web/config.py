"""FLEXT Web Configuration using flext-core patterns.

Built on flext-core foundation for Django enterprise web application.
Uses modern Python 3.13 patterns with comprehensive configuration management.
"""

from __future__ import annotations

from typing import Any

from pydantic import field_validator, model_validator
from pydantic_settings import SettingsConfigDict

from flext_core.config.base import BaseSettings
from flext_core.domain.pydantic_base import DomainValueObject, Field
from flext_core.domain.types import (
    FlextConstants,
    LogLevelLiteral,
    ProjectName,
    Version,
)


class DjangoSecurityConfig(DomainValueObject):
    """Django security configuration using flext-core patterns."""

    secret_key: str = Field(
        default="development-key-change-in-production-" + "x" * 50,
        min_length=50,
        description="Django secret key for cryptographic signing",
    )
    debug: bool = Field(default=False, description="Enable Django debug mode")
    allowed_hosts: list[str] = Field(
        default_factory=lambda: ["localhost", "127.0.0.1"],
        min_length=1,
        max_length=100,
        description="Allowed hosts for Django application",
    )
    csrf_trusted_origins: list[str] = Field(
        default_factory=list,
        description="CSRF trusted origins",
    )
    secure_ssl_redirect: bool = Field(default=False, description="Force SSL redirect")
    secure_hsts_seconds: int = Field(
        default=0,
        ge=0,
        le=31536000,
        description="HSTS max age in seconds",
    )

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Validate Django secret key length and complexity."""
        if len(v) < 50:
            msg = "Secret key must be at least 50 characters"
            raise ValueError(msg)
        return v


class DjangoDatabaseConfig(DomainValueObject):
    """Django database configuration using flext-core patterns."""

    engine: str = Field(
        default="django.db.backends.postgresql",
        description="Database engine",
    )
    name: str = Field(default="flext_web", description="Database name")
    user: str = Field(default="postgres", description="Database user")
    password: str = Field(default="", description="Database password")
    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=5432, ge=1, le=65535, description="Database port")
    conn_max_age: int = Field(
        default=600,
        ge=0,
        le=3600,
        description="Connection max age in seconds",
    )

    def to_django_config(self) -> dict[str, Any]:
        """Convert to Django database configuration format."""
        return {
            "ENGINE": self.engine,
            "NAME": self.name,
            "USER": self.user,
            "PASSWORD": self.password,
            "HOST": self.host,
            "PORT": self.port,
            "CONN_MAX_AGE": self.conn_max_age,
            "CONN_HEALTH_CHECKS": True,
        }


class DjangoCacheConfig(DomainValueObject):
    """Django cache configuration using flext-core patterns."""

    backend: str = Field(
        default="django.core.cache.backends.redis.RedisCache",
        description="Cache backend",
    )
    location: str = Field(
        default="redis://localhost:6379/1",
        description="Cache location/connection string",
    )
    timeout: int = Field(
        default=300,
        ge=0,
        le=3600,
        description="Default cache timeout in seconds",
    )

    def to_django_config(self) -> dict[str, Any]:
        """Convert to Django cache configuration format."""
        return {
            "BACKEND": self.backend,
            "LOCATION": self.location,
            "TIMEOUT": self.timeout,
        }


class WebConfig(BaseSettings):
    """FLEXT Web configuration using flext-core patterns."""

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_WEB_",
        env_nested_delimiter="__",
        case_sensitive=False,
        validate_assignment=True,
        extra="ignore",
        frozen=True,
    )

    # Core project metadata
    project_name: ProjectName = Field(
        default="flext-web",
        description="Project name",
    )
    version: Version = Field(
        default="0.7.0",
        description="Project version",
    )

    # Django configuration
    security: DjangoSecurityConfig = Field(
        default_factory=DjangoSecurityConfig,
        description="Django security configuration",
    )
    database: DjangoDatabaseConfig = Field(
        default_factory=DjangoDatabaseConfig,
        description="Database configuration",
    )
    cache: DjangoCacheConfig = Field(
        default_factory=DjangoCacheConfig,
        description="Cache configuration",
    )

    # Web-specific settings
    time_zone: str = Field(default="UTC", description="Django timezone")
    language_code: str = Field(default="en-us", description="Django language code")
    use_i18n: bool = Field(default=True, description="Enable internationalization")
    use_tz: bool = Field(default=True, description="Enable timezone support")

    # API settings
    api_version: str = Field(default="v1", description="API version")
    api_title: str = Field(default="FLEXT Web API", description="API title")

    # Performance settings
    session_cookie_age: int = Field(
        default=1209600,  # 2 weeks
        ge=3600,
        le=2592000,  # 30 days
        description="Session cookie age in seconds",
    )

    # Global logging configuration
    log_level: LogLevelLiteral = Field(
        default=FlextConstants.DEFAULT_LOG_LEVEL,
        description="Global log level",
    )
    debug: bool = Field(default=False, description="Enable debug mode")

    @model_validator(mode="after")
    def validate_configuration(self) -> WebConfig:
        """Validate configuration consistency."""
        # Ensure debug mode consistency
        if self.debug and not self.security.debug:
            self.security.debug = True

        # Validate production settings
        if not self.debug and self.security.secret_key == "development-key":
            msg = "Production secret key must be set"
            raise ValueError(msg)

        return self

    def get_django_databases(self) -> dict[str, Any]:
        """Get Django database configuration."""
        return {"default": self.database.to_django_config()}

    def get_django_caches(self) -> dict[str, Any]:
        """Get Django cache configuration."""
        return {"default": self.cache.to_django_config()}


# Singleton configuration instance
def get_web_config() -> WebConfig:
    """Get web configuration singleton."""
    return WebConfig()
