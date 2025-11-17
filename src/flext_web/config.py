"""HTTP Configuration - Domain-agnostic HTTP configuration.

Uses Pydantic 2 with flext-core patterns and FlextWebConstants.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextResult
from pydantic import BaseModel, ConfigDict, Field, computed_field

from flext_web.constants import FlextWebConstants


class FlextWebConfig(BaseModel):
    """HTTP server configuration.

    Pydantic 2 model with computed properties for derived values.
    Domain-agnostic configuration for any HTTP-based service.
    """

    model_config = ConfigDict(extra="forbid")

    host: str = Field(
        default=FlextWebConstants.WebDefaults.HOST,
        min_length=1,
        max_length=255,
        description="Web server host address",
    )
    port: int = Field(
        default=FlextWebConstants.WebDefaults.PORT,
        ge=FlextWebConstants.WebValidation.PORT_RANGE[0],
        le=FlextWebConstants.WebValidation.PORT_RANGE[1],
        description="Web server port number",
    )
    app_name: str = Field(
        default=FlextWebConstants.WebDefaults.APP_NAME,
        min_length=FlextWebConstants.WebValidation.NAME_LENGTH_RANGE[0],
        max_length=FlextWebConstants.WebValidation.NAME_LENGTH_RANGE[1],
        description="Web application name",
    )
    version: str = Field(
        default=FlextWebConstants.WebDefaults.VERSION_STRING,
        description="Application version",
    )
    debug_mode: bool = Field(
        default=FlextWebConstants.WebDefaults.DEBUG_MODE,
        alias="debug",
        description="Debug mode",
    )
    ssl_enabled: bool = Field(default=False, description="Enable SSL/TLS")
    ssl_cert_path: Path | None = Field(default=None, description="SSL certificate path")
    ssl_key_path: Path | None = Field(default=None, description="SSL key path")
    secret_key: str = Field(
        default=FlextWebConstants.WebDefaults.SECRET_KEY,
        min_length=FlextWebConstants.WebSecurity.MIN_SECRET_KEY_LENGTH,
        description="Secret key for session management",
    )
    testing: bool = Field(
        default=False, description="Testing mode"
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
    def create_web_config(cls) -> FlextResult[FlextWebConfig]:
        """Create default web configuration.

        Returns:
        FlextResult[FlextWebConfig]: Success contains default config,
        failure contains error message

        """
        try:
            config = cls()
            return FlextResult.ok(config)
        except Exception as e:
            return FlextResult.fail(f"Failed to create web config: {e}")


__all__ = ["FlextWebConfig"]
