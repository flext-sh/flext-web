"""HTTP Configuration - Domain-agnostic HTTP configuration.

Uses Pydantic 2 with flext-core patterns and c.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from flext import FlextResult, FlextSettings
from flext_web.constants import c


@FlextSettings.auto_register("web")
class FlextWebSettings(BaseSettings):
    """HTTP server configuration using AutoConfig pattern.

    **ARCHITECTURAL PATTERN**: Zero-Boilerplate Auto-Registration

    This class uses FlextSettings.AutoConfig for automatic:
    - Singleton pattern (thread-safe)
    - Namespace registration (accessible via config.web)
    - Environment variable loading from FLEXT_WEB_* variables
    - .env file loading (production/development)
    - Automatic type conversion and validation via Pydantic v2

    Pydantic 2 model with computed properties for derived values.
    Domain-agnostic configuration for any HTTP-based service.
    """

    # Use FlextSettings.resolve_env_file() to ensure all FLEXT configs use same .env
    model_config = SettingsConfigDict(
        env_prefix="FLEXT_WEB_",
        env_file=FlextSettings.resolve_env_file(),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        validate_assignment=True,
        str_strip_whitespace=True,
        validate_default=True,
        frozen=False,
        strict=False,
    )

    host: str = Field(
        default=c.Web.WebDefaults.HOST,
        min_length=1,
        max_length=255,
        description="Web server host address",
    )
    port: int = Field(
        default=c.Web.WebDefaults.PORT,
        ge=c.Web.WebValidation.PORT_RANGE[0],
        le=c.Web.WebValidation.PORT_RANGE[1],
        description="Web server port number",
    )
    app_name: str = Field(
        default=c.Web.WebDefaults.APP_NAME,
        min_length=c.Web.WebValidation.NAME_LENGTH_RANGE[0],
        max_length=c.Web.WebValidation.NAME_LENGTH_RANGE[1],
        description="Web application name",
    )
    version: str = Field(
        default=c.Web.WebDefaults.VERSION_STRING,
        description="Application version",
    )
    debug_mode: bool = Field(
        default=c.Web.WebDefaults.DEBUG_MODE,
        description="Debug mode",
    )
    ssl_enabled: bool = Field(default=False, description="Enable SSL/TLS")
    ssl_cert_path: Path | None = Field(default=None, description="SSL certificate path")
    ssl_key_path: Path | None = Field(default=None, description="SSL key path")
    secret_key: str = Field(
        default=c.Web.WebDefaults.SECRET_KEY,
        min_length=c.Web.WebSecurity.MIN_SECRET_KEY_LENGTH,
        description="Secret key for session management",
    )
    testing: bool = Field(
        default=False,
        description="Testing mode",
    )  # Testing mode is False by default, not in Constants as it's runtime-specific

    @computed_field
    def debug(self) -> bool:
        """Debug property for compatibility."""
        return self.debug_mode

    @computed_field
    def protocol(self) -> str:
        """Protocol: https if SSL enabled, http otherwise."""
        return "https" if self.ssl_enabled else "http"

    @computed_field
    def base_url(self) -> str:
        """Base URL from protocol, host, and port."""
        return f"{self.protocol}://{self.host}:{self.port}"

    @computed_field
    def server_address(self) -> tuple[str, int]:
        """Server address as (host, port) tuple."""
        return (self.host, self.port)

    @classmethod
    def create_web_config(cls) -> FlextResult[FlextWebSettings]:
        """Create default web configuration.

        Returns:
        FlextResult[FlextWebSettings]: Success contains default config,
        failure contains error message

        """
        try:
            config = cls()
            return FlextResult.ok(config)
        except Exception as e:
            return FlextResult.fail(f"Failed to create web config: {e}")


__all__ = ["FlextWebSettings"]
