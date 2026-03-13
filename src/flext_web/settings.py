"""HTTP configuration management.

Provides configuration for HTTP-based services using Pydantic.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_core import FlextModels
from pydantic import Field

from flext_web.constants import FlextWebConstants as c


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
        int,
        Field(
            default=c.Web.WebDefaults.PORT,
            ge=c.Web.WebValidation.PORT_RANGE[0],
            le=c.Web.WebValidation.PORT_RANGE[1],
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


__all__ = ["FlextWebSettings"]
