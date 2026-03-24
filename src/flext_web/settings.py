"""HTTP configuration management.

Provides configuration for HTTP-based services using Pydantic.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_core import FlextModels, r, t
from pydantic import Field, computed_field

from flext_web import c


class FlextWebSettings(FlextModels.Value):
    """Validated settings for web runtime and HTTP endpoints."""

    app_name: Annotated[
        str,
        Field(
            default=c.Web.WebDefaults.APP_NAME,
            min_length=c.Web.WebValidation.NAME_LENGTH_RANGE[0],
            max_length=c.Web.WebValidation.NAME_LENGTH_RANGE[1],
            description="Application name",
        ),
    ]
    host: Annotated[
        str,
        Field(
            default=c.Web.WebDefaults.HOST,
            min_length=1,
            max_length=c.Web.WebSecurity.MAX_HOST_LENGTH,
            description="Bind host",
        ),
    ]
    port: Annotated[
        t.PortNumber,
        Field(
            default=c.Web.WebDefaults.PORT,
            description="Bind port",
        ),
    ]
    debug_mode: Annotated[
        bool,
        Field(
            default=c.Web.WebDefaults.DEBUG_MODE,
            description="Debug mode",
        ),
    ]
    debug: Annotated[bool, Field(default=False, description="Flask debug flag")]
    testing: Annotated[bool, Field(default=False, description="Flask testing flag")]
    secret_key: Annotated[
        str,
        Field(
            default=c.Web.WebDefaults.SECRET_KEY,
            min_length=c.Web.WebSecurity.MIN_SECRET_KEY_LENGTH,
            description="Application secret key",
        ),
    ]
    ssl_enabled: Annotated[
        bool,
        Field(default=False, description="Enable TLS endpoints"),
    ]
    ssl_cert_path: Annotated[
        str | None,
        Field(default=None, description="TLS certificate file path"),
    ]
    ssl_key_path: Annotated[
        str | None,
        Field(default=None, description="TLS key file path"),
    ]

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
