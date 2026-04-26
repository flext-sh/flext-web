"""HTTP configuration management for flext-web.

Provides the registered `web` settings namespace on top of FlextSettings with
explicit validation for runtime host/port/security fields.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated, ClassVar, Self, Unpack

from flext_core import FlextSettings
from flext_web import c, m, p, r, t, u


@FlextSettings.auto_register("web")
class FlextWebSettings(FlextSettings):
    """Validated settings for web runtime and HTTP endpoints."""

    model_config: ClassVar[m.SettingsConfigDict] = m.SettingsConfigDict(
        env_prefix="FLEXT_WEB_", extra="ignore"
    )

    app_name: Annotated[
        str,
        u.Field(
            min_length=c.Web.WebValidation.NAME_LENGTH_RANGE[0],
            max_length=c.Web.WebValidation.NAME_LENGTH_RANGE[1],
            description="Application name",
        ),
    ] = c.Web.WebDefaults.APP_NAME
    host: Annotated[
        str,
        u.Field(
            min_length=1,
            max_length=c.Web.WebSecurity.MAX_HOST_LENGTH,
            description="Bind host",
        ),
    ] = c.Web.WebDefaults.HOST
    port: Annotated[
        t.PortNumber,
        u.Field(
            description="Bind port",
        ),
    ] = c.Web.WebDefaults.PORT
    debug_mode: Annotated[
        bool,
        u.Field(
            description="Debug mode",
        ),
    ] = c.Web.WebDefaults.DEBUG_MODE
    debug: Annotated[bool, u.Field(description="Flask debug flag")] = False
    testing: Annotated[bool, u.Field(description="Flask testing flag")] = False
    secret_key: Annotated[
        str,
        u.Field(
            min_length=c.Web.WebSecurity.MIN_SECRET_KEY_LENGTH,
            description="Application secret key",
        ),
    ] = c.Web.WebDefaults.SECRET_KEY
    ssl_enabled: Annotated[
        bool,
        u.Field(description="Enable TLS endpoints"),
    ] = False
    ssl_cert_path: Annotated[
        str | None,
        u.Field(description="TLS certificate file path"),
    ] = None
    ssl_key_path: Annotated[
        str | None,
        u.Field(description="TLS key file path"),
    ] = None

    @u.field_validator("host")
    @classmethod
    def validate_host(cls, value: str) -> str:
        """Ensure host is non-empty after trimming."""
        host_value = value.strip()
        if not host_value:
            msg = "Host cannot be empty"
            raise ValueError(msg)
        return host_value

    @u.field_validator("port")
    @classmethod
    def validate_port(cls, value: int) -> int:
        """Ensure port stays inside the configured range."""
        min_port, max_port = c.Web.WebValidation.PORT_RANGE
        if not min_port <= value <= max_port:
            msg = f"Port must be between {min_port} and {max_port}"
            raise ValueError(msg)
        return value

    @u.field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, value: str) -> str:
        """Ensure the secret key is present after trimming."""
        secret_key = value.strip()
        if not secret_key:
            msg = "Secret key cannot be empty"
            raise ValueError(msg)
        return secret_key

    @u.field_validator("ssl_cert_path", "ssl_key_path")
    @classmethod
    def normalize_optional_path(cls, value: str | None) -> str | None:
        """Normalize optional TLS paths by stripping empty strings."""
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @u.model_validator(mode="after")
    def synchronize_debug_flags(self) -> Self:
        """Keep Flask debug flags aligned from a single effective toggle."""
        effective_debug = bool(self.debug or self.debug_mode)
        if self.debug == effective_debug and self.debug_mode == effective_debug:
            return self
        return self.model_copy(
            update={"debug": effective_debug, "debug_mode": effective_debug}
        )

    @u.computed_field()
    @property
    def protocol(self) -> str:
        """Return active URL protocol based on TLS setting."""
        return str(
            c.Web.WebDefaults.HTTPS_PROTOCOL
            if self.ssl_enabled
            else c.Web.WebDefaults.HTTP_PROTOCOL,
        )

    @u.computed_field()
    @property
    def base_url(self) -> str:
        """Build base URL from protocol, host, and port."""
        return f"{self.protocol}://{self.host}:{self.port}"

    @classmethod
    def create_web_config(
        cls,
        **overrides: Unpack[t.Web.CreateWebConfigKwargs],
    ) -> p.Result[Self]:
        """Create web settings with validated overrides."""
        payload: t.Web.CreateWebConfigKwargs = {}
        if "host" in overrides:
            payload["host"] = overrides["host"]
        if "port" in overrides:
            payload["port"] = overrides["port"]
        if "debug" in overrides:
            payload["debug"] = overrides["debug"]
        if "secret_key" in overrides:
            payload["secret_key"] = overrides["secret_key"]
        return r[Self].create_from_callable(lambda: cls.model_validate(payload))

    @classmethod
    def validate_settings(cls, settings: Self) -> p.Result[bool]:
        """Validate a settings instance against the canonical schema."""
        try:
            _ = cls(**settings.model_dump())
        except c.ValidationError as exc:
            return r[bool].fail(str(exc))
        return r[bool].ok(True)


__all__: list[str] = ["FlextWebSettings"]
