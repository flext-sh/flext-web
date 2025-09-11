"""FLEXT Web Settings — Settings → Config bridge following flext-core patterns.

Single settings class that loads from env/CLI/dicts and converts to
`FlextWebConfigs.WebConfig` via Pydantic validation.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextConfig, FlextResult
from pydantic import Field


class FlextWebSettings(FlextConfig):
    """Web settings with environment support and bridge to WebConfig."""

    model_config = FlextConfig.model_config.copy()
    model_config.update(
        {
            "env_prefix": "FLEXT_WEB_",
            "env_file": ".env",
            "env_file_encoding": "utf-8",
            "case_sensitive": False,
            "validate_assignment": True,
            "extra": "allow",
            "str_strip_whitespace": True,
        }
    )

    # Core web fields (inherit from FlextConfig, override with web-specific defaults)
    host: str = Field(default="localhost")
    port: int = Field(default=8080)
    debug: bool = Field(default=False)
    # Web-specific configuration fields
    secret_key: str = Field(default="")
    request_timeout: int = Field(default=30)
    enable_cors: bool = Field(default=True)

    def to_config(self) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Convert settings to validated WebConfig model - import delayed to avoid circular import."""
        try:
            # Import only when needed to avoid circular dependency
            from flext_web.config import FlextWebConfigs

            data = self.model_dump(exclude_none=True)
            model = FlextWebConfigs.WebConfig.model_validate(data)
            return FlextResult["FlextWebConfigs.WebConfig"].ok(model)
        except Exception as e:
            return FlextResult["FlextWebConfigs.WebConfig"].fail(
                f"Failed to build WebConfig: {e}",
            )


__all__ = ["FlextWebSettings"]
