"""Settings for flext-web — namespaced under ``settings.Web``.

Layer-0: imports only stdlib + pydantic + ``FlextSettings``. Universal runtime
fields (``debug``/``trace``/``log_level``/``timezone``/``async_logging``) come
from ``FlextSettings`` by MRO and are NOT redeclared. Every project field lives
in the ``Web`` namespace group with simple scalar types so each is settable via
``.env`` / env vars / params (``FLEXT_WEB_WEB__HOST`` …). Derived values
(protocol/base_url) and construction helpers belong to consumers, not settings.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

from flext_cli import FlextCliSettings


class FlextWebSettings(FlextCliSettings):
    """Web runtime settings; all project fields under ``settings.Web.*``."""

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_WEB_", env_nested_delimiter="__", extra="ignore"
    )

    class _Web(BaseModel):
        """Namespaced web runtime settings (pure declaration)."""

        app_name: Annotated[
            str, Field(default="FLEXT Web", description="Application name")
        ]
        version: Annotated[
            str, Field(default="1.0.0", description="Service semantic version")
        ]
        host: Annotated[
            str,
            Field(
                default="localhost",
                min_length=1,
                pattern=r"\S",
                description="Bind host",
            ),
        ]
        port: Annotated[
            int, Field(default=8080, ge=1, le=65535, description="Bind port")
        ]
        testing: Annotated[bool, Field(default=False, description="Testing flag")]
        secret_key: Annotated[
            str,
            Field(
                default="default-secret-key-32-characters-long-for-security",
                min_length=32,
                description="Application secret key",
            ),
        ]
        ssl_enabled: Annotated[
            bool, Field(default=False, description="Enable TLS endpoints")
        ]
        ssl_cert_path: Annotated[
            str | None, Field(default=None, description="TLS certificate file path")
        ]
        ssl_key_path: Annotated[
            str | None, Field(default=None, description="TLS key file path")
        ]

    if TYPE_CHECKING:
        Web: _Web
    else:
        Web: _Web = Field(default_factory=_Web, description="Namespaced web settings.")


settings: FlextWebSettings = FlextWebSettings.fetch_global()
"""Pre-instantiated project settings singleton — ``from flext_web import settings``."""

__all__: list[str] = ["FlextWebSettings", "settings"]
