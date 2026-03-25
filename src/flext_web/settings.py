"""HTTP configuration management.

Provides configuration for HTTP-based services using Pydantic.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_core import FlextModels, r
from pydantic import Field, computed_field

from flext_web import c, t


class FlextWebSettings(FlextModels.Value):
    """Validated settings for web runtime and HTTP endpoints."""

    app_name: Annotated[
        str,
        Field(
            min_length=c.Web.WebValidation.NAME_LENGTH_RANGE[0],
            max_length=c.Web.WebValidation.NAME_LENGTH_RANGE[1],
            description="Application name",
        ),
    ] = c.Web.WebDefaults.APP_NAME
    host: Annotated[
        str,
        Field(
            min_length=1,
            max_length=c.Web.WebSecurity.MAX_HOST_LENGTH,
            description="Bind host",
        ),
    ] = c.Web.WebDefaults.HOST
    port: Annotated[
        t.PortNumber,
        Field(
            description="Bind port",
        ),
    ] = c.Web.WebDefaults.PORT
    debug_mode: Annotated[
        bool,
        Field(
            description="Debug mode",
        ),
    ] = c.Web.WebDefaults.DEBUG_MODE
    debug: Annotated[bool, Field(description="Flask debug flag")] = False
    testing: Annotated[bool, Field(description="Flask testing flag")] = False
    secret_key: Annotated[
        str,
        Field(
            min_length=c.Web.WebSecurity.MIN_SECRET_KEY_LENGTH,
            description="Application secret key",
        ),
    ] = c.Web.WebDefaults.SECRET_KEY
    ssl_enabled: Annotated[
        bool,
        Field(description="Enable TLS endpoints"),
    ] = False
    ssl_cert_path: Annotated[
        str | None,
        Field(description="TLS certificate file path"),
    ] = None
    ssl_key_path: Annotated[
        str | None,
        Field(description="TLS key file path"),
    ] = None

    @computed_field
    @property
    def protocol(self) -> str:
        """Return active URL protocol based on TLS setting."""
        return (
            c.Web.WebDefaults.HTTPS_PROTOCOL
            if self.ssl_enabled
            else c.Web.WebDefaults.HTTP_PROTOCOL
        )

    @computed_field
    @property
    def base_url(self) -> str:
        """Build base URL from protocol, host, and port."""
        return f"{self.protocol}://{self.host}:{self.port}"

    @classmethod
    def create_web_config(cls) -> r[FlextWebSettings]:
        """Create and wrap web settings using r result type."""
        return r[FlextWebSettings].ok(cls.model_validate({}))


__all__ = ["FlextWebSettings"]
