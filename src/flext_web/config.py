"""FLEXT Web Configuration - Consolidated using flext-core patterns.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

This module provides Django web configuration using consolidated flext-core patterns.
"""

from __future__ import annotations

from pydantic import BaseSettings, Field, field_validator
from pydantic_settings import SettingsConfigDict


class WebConfig(BaseSettings):
    """Django web configuration using consolidated flext-core patterns."""

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_WEB_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Project identification
    title: str = Field(
        default="FLEXT Web",
        max_length=255,
    )
    description: str = Field(
        default="Enterprise Data Integration Web Interface",
        max_length=500,
    )
    version: str = Field(default="1.0.0")

    # Database configuration
    database_url: str = Field(
        default="postgresql://localhost/flext_web",
        description="Database connection URL",
    )

    # Django-specific settings
    django_secret_key: str = Field(
        default="development-key-change-in-production-" + "x" * 50,
        min_length=50,
        description="Django secret key for cryptographic signing",
        json_schema_extra={"secret": True},
    )
    django_debug: bool = Field(default=False, description="Enable Django debug mode")
    django_allowed_hosts: list[str] = Field(
        default_factory=lambda: ["localhost", "127.0.0.1"],
        description="Django allowed hosts",
    )

    # Static files configuration
    static_url: str = Field(default="/static/", description="Static files URL")
    media_url: str = Field(default="/media/", description="Media files URL")
    static_root: str = Field(
        default="staticfiles",
        description="Static files root directory",
    )
    media_root: str = Field(default="media", description="Media files root directory")

    # Session configuration
    session_cookie_age: int = Field(
        default=3600,
        ge=300,
        le=86400,
        description="Session cookie age in seconds",
    )
    session_cookie_secure: bool = Field(
        default=False,
        description="Use secure session cookies",
    )
    session_cookie_httponly: bool = Field(
        default=True,
        description="Make session cookies HTTP only",
    )

    # Security settings
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
    secure_hsts_include_subdomains: bool = Field(
        default=False,
        description="Include subdomains in HSTS",
    )
    secure_hsts_preload: bool = Field(default=False, description="Enable HSTS preload")
    secure_content_type_nosniff: bool = Field(
        default=True,
        description="Enable content type nosniff",
    )
    secure_browser_xss_filter: bool = Field(
        default=True,
        description="Enable browser XSS filter",
    )
    x_frame_options: str = Field(
        default="DENY",
        description="X-Frame-Options header value",
    )

    # Email configuration
    email_backend: str = Field(
        default="django.core.mail.backends.console.EmailBackend",
        description="Django email backend",
    )
    email_host: str = Field(default="localhost", description="Email server host")
    email_port: int = Field(
        default=587,
        ge=1,
        le=65535,
        description="Email server port",
    )
    email_use_tls: bool = Field(default=True, description="Use TLS for email")
    email_host_user: str = Field(default="", description="Email server username")
    email_host_password: str = Field(
        default="",
        description="Email server password",
        json_schema_extra={"secret": True},
    )
    default_from_email: str = Field(
        default="noreply@flext.com",
        description="Default from email address",
    )

    # Redis configuration for Django
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL",
    )
    cache_timeout: int = Field(
        default=300,
        ge=60,
        le=3600,
        description="Default cache timeout in seconds",
    )

    # Celery configuration
    celery_broker_url: str = Field(
        default="redis://localhost:6379/0",
        description="Celery broker URL",
    )
    celery_result_backend: str = Field(
        default="redis://localhost:6379/0",
        description="Celery result backend URL",
    )
    celery_task_serializer: str = Field(
        default="json",
        description="Celery task serializer",
    )
    celery_result_serializer: str = Field(
        default="json",
        description="Celery result serializer",
    )
    celery_accept_content: list[str] = Field(
        default_factory=lambda: ["json"],
        description="Celery accepted content types",
    )

    # Logging configuration specific to Django
    django_log_level: str = Field(default="INFO", description="Django log level")
    disable_django_logging: bool = Field(
        default=False,
        description="Disable Django's default logging configuration",
    )

    # File upload settings
    max_upload_size: int = Field(
        default=10 * 1024 * 1024,
        ge=1024,
        description="Maximum file upload size in bytes",
    )
    allowed_upload_types: list[str] = Field(
        default_factory=lambda: [".txt", ".csv", ".json", ".yaml", ".yml"],
        description="Allowed file upload types",
    )

    # Pagination settings
    default_page_size: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Default pagination size",
    )
    max_page_size: int = Field(
        default=100,
        ge=1,
        le=1000,
        description="Maximum pagination size",
    )

    # Feature flags
    enable_api: bool = Field(default=True, description="Enable REST API")
    enable_REDACTED_LDAP_BIND_PASSWORD: bool = Field(default=True, description="Enable Django REDACTED_LDAP_BIND_PASSWORD")
    enable_debug_toolbar: bool = Field(
        default=False,
        description="Enable Django debug toolbar",
    )

    @field_validator("django_secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Validate Django secret key."""
        if len(v) < 50:
            msg = "Django secret key must be at least 50 characters"
            raise ValueError(msg)
        return v

    @field_validator(
        "csrf_trusted_origins",
        "django_allowed_hosts",
        "celery_accept_content",
        "allowed_upload_types",
        mode="before",
    )
    @classmethod
    def validate_list_fields(cls, v: list[str] | str) -> list[str]:
        """Validate list fields - convert comma-separated strings to lists."""
        if isinstance(v, str):
            # Split by comma and strip whitespace
            return [item.strip() for item in v.split(",") if item.strip()]
        return v

    @field_validator("x_frame_options")
    @classmethod
    def validate_x_frame_options(cls, v: str) -> str:
        """Validate X-Frame-Options value."""
        allowed_values = {"DENY", "SAMEORIGIN", "ALLOWALL"}
        if v.upper() not in allowed_values:
            msg = f"X-Frame-Options must be one of: {allowed_values}"
            raise ValueError(msg)
        return v.upper()

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.django_debug or "localhost" in self.database_url

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.is_development

    @property
    def django_database_config(self) -> dict[str, dict[str, str]]:
        """Get Django database configuration."""
        return {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": (
                    self.database_url.split("/")[-1]
                    if "/" in self.database_url
                    else "flext_web"
                ),
                "USER": (
                    self.database_url.split("//")[1].split(":")[0]
                    if "@" in self.database_url
                    else ""
                ),
                "PASSWORD": (
                    self.database_url.split("://")[1].split("@")[0].split(":")[1]
                    if "@" in self.database_url
                    and ":" in self.database_url.split("://")[1].split("@")[0]
                    else ""
                ),
                "HOST": (
                    self.database_url.split("@")[1].split(":")[0]
                    if "@" in self.database_url
                    else "localhost"
                ),
                "PORT": (
                    self.database_url.split("@")[1].split(":")[1].split("/")[0]
                    if "@" in self.database_url
                    and ":" in self.database_url.split("@")[1]
                    else "5432"
                ),
            },
        }

    def validate_configuration(self) -> list[str]:
        """Validate Django web configuration settings.

        Returns:
            List of validation error messages.

        """
        errors: list[str] = []

        if self.session_cookie_age < 300:
            errors.append("Session cookie age must be at least 300 seconds")

        if self.max_upload_size < 1024:
            errors.append("Max upload size must be at least 1024 bytes")

        if self.default_page_size > self.max_page_size:
            errors.append("Default page size cannot be greater than max page size")

        if self.is_production and self.django_debug:
            errors.append("Debug mode must be disabled in production")

        if self.is_production and not self.secure_ssl_redirect:
            errors.append("SSL redirect should be enabled in production")

        return errors


# Global settings instance
_settings: WebConfig | None = None


def get_web_settings() -> WebConfig:
    """Get Django web configuration settings.

    Returns:
        WebConfig: Consolidated Django web configuration using flext-core patterns.

    """
    global _settings
    if _settings is None:
        _settings = WebConfig()
    return _settings


# Export aliases for backward compatibility
WebSettings = WebConfig
DjangoSettings = WebConfig

__all__ = [
    "DjangoSettings",
    "WebConfig",
    "WebSettings",
    "get_web_settings",
]
