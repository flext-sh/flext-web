"""FLEXT Web Settings — Settings → Config bridge following flext-core patterns.

Single settings class that loads from env/CLI/dicts and converts to
`FlextWebConfigs.WebConfig` via Pydantic validation.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

"""
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""


from flext_core import FlextConfig, FlextResult
from pydantic import Field
from pydantic_settings import SettingsConfigDict

from flext_web.config import FlextWebConfigs


class FlextWebSettings(FlextConfig.Settings):
    """Web settings with environment support and bridge to WebConfig."""

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_WEB_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        validate_assignment=True,
        extra="allow",
        str_strip_whitespace=True,
    )

    # Core web fields (optional to allow defaults from WebConfig)
    host: str | None = Field(default=None)
    port: int | None = Field(default=None)
    debug: bool | None = Field(default=None)
    secret_key: str | None = Field(default=None)
    request_timeout: int | None = Field(default=None)
    enable_cors: bool | None = Field(default=None)

    def to_config(self) -> FlextResult[FlextWebConfigs.WebConfig]:
        """Convert settings to validated `WebConfig` model."""
        try:
            data = self.model_dump(exclude_none=True)
            model = FlextWebConfigs.WebConfig.model_validate(data)
            return FlextResult[FlextWebConfigs.WebConfig].ok(model)
        except Exception as e:
            return FlextResult[FlextWebConfigs.WebConfig].fail(
                f"Failed to build WebConfig: {e}",
            )


__all__ = ["FlextWebSettings"]
