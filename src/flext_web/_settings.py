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

from flext_cli import FlextCliSettings, m


class FlextWebSettings(FlextCliSettings):
    """Web runtime settings; all project fields under ``settings.Web.*``."""

    model_config = m.SettingsConfigDict(
        env_prefix="FLEXT_WEB_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    class _Web(m.BaseModel):
        """Namespaced web runtime settings (pure declaration)."""

        app_name: Annotated[str, m.Field(description="Application name")] = "FLEXT Web"
        version: Annotated[str, m.Field(description="Service semantic version")] = (
            "1.0.0"
        )
        host: Annotated[
            str,
            m.Field(min_length=1, pattern=r"\S", description="Bind host"),
        ] = "localhost"
        port: Annotated[int, m.Field(ge=1, le=65535, description="Bind port")] = 8080
        testing: Annotated[bool, m.Field(description="Testing flag")] = False
        secret_key: Annotated[
            str | None,
            m.Field(
                min_length=32,
                description="Application secret key sourced from the environment; "
                "required at runtime.",
            ),
        ] = None
        auth_username: Annotated[
            str | None,
            m.Field(
                description="Credential username sourced from the environment; "
                "required to authenticate.",
            ),
        ] = None
        auth_password: Annotated[
            str | None,
            m.Field(
                description="Credential password sourced from the environment; "
                "required to authenticate.",
            ),
        ] = None
        ssl_enabled: Annotated[
            bool,
            m.Field(description="Enable TLS endpoints"),
        ] = False
        ssl_cert_path: Annotated[
            str | None,
            m.Field(description="TLS certificate file path"),
        ] = None
        ssl_key_path: Annotated[
            str | None,
            m.Field(description="TLS key file path"),
        ] = None

    if TYPE_CHECKING:
        Web: _Web = _Web()
    else:
        Web: _Web = m.Field(
            default_factory=_Web,
            description="Namespaced web settings.",
        )


settings: FlextWebSettings = FlextWebSettings.fetch_global()
"""Pre-instantiated project settings singleton — ``from flext_web import settings``."""

__all__: list[str] = ["FlextWebSettings", "settings"]
