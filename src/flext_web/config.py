"""Generic HTTP Configuration - Domain-agnostic HTTP config using Python 3.13+.

Domain-agnostic HTTP configuration using flext-core patterns directly.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from flext_core import FlextConfig, FlextResult
from pydantic import BaseModel, Field, computed_field


class FlextWebConfig(BaseModel):
    """Generic HTTP configuration using flext-core patterns."""

    # Core HTTP configuration fields
    host: str = Field(default="localhost", min_length=1, max_length=255)
    port: int = Field(default=8080, ge=1, le=65535)
    app_name: str = Field(default="HTTP API", min_length=1, max_length=255)
    version: str = Field(default="1.0.0")
    max_content_length: int = Field(default=16777216, gt=0)
    request_timeout: int = Field(default=30, gt=0, le=600)
    enable_cors: bool = Field(default=False)
    cors_origins: list[str] = Field(default_factory=list)
    ssl_enabled: bool = Field(default=False)
    ssl_cert_path: Path | None = Field(default=None)
    ssl_key_path: Path | None = Field(default=None)

    @computed_field
    @property
    def protocol(self) -> str:
        """Get the protocol (http/https)."""
        return "https" if self.ssl_enabled else "http"

    @computed_field
    @property
    def base_url(self) -> str:
        """Get the base URL."""
        return f"{self.protocol}://{self.host}:{self.port}"

    def get_server_config(self) -> dict[str, Any]:
        """Get server-related configuration."""
        return {
            "host": self.host,
            "port": self.port,
            "protocol": self.protocol,
            "base_url": self.base_url,
            "ssl_enabled": self.ssl_enabled,
        }

    @classmethod
    def create_config(cls, **overrides: Any) -> FlextResult[FlextWebConfig]:
        """Generic configuration factory."""
        try:
            config = cls(**overrides)
            return FlextResult.ok(config)
        except Exception as e:
            return FlextResult.fail(f"Configuration creation failed: {e}")


__all__ = ["FlextWebConfig"]
