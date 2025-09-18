"""FLEXT Web Settings.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pydantic import Field, field_validator

from flext_core import FlextConfig, FlextResult


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

    @field_validator("debug", mode="before")
    @classmethod
    def validate_debug(cls, value: object) -> bool:
        """Validate debug field, converting string values."""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in {"true", "1", "yes", "on"}
        # For other types, convert to bool
        return bool(value)

    # Web-specific configuration fields
    secret_key: str = Field(default="")
    request_timeout: int = Field(default=30)
    enable_cors: bool = Field(default=True)

    def to_config(self) -> FlextResult[object]:
        """Convert settings to validated WebConfig model - import delayed to avoid circular import."""
        try:
            # Import only when needed to avoid circular dependency
            from flext_web.config import FlextWebConfigs  # noqa: PLC0415

            data = self.model_dump(exclude_none=True)
            model = FlextWebConfigs.WebConfig.model_validate(data)
            return FlextResult[object].ok(model)
        except Exception as e:
            return FlextResult[object].fail(
                f"Failed to build WebConfig: {e}",
            )


__all__ = ["FlextWebSettings"]
