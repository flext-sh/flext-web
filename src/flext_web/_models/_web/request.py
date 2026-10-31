"""Standalone web request/response models for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import uuid
from collections.abc import Mapping
from datetime import datetime
from types import MappingProxyType
from typing import Annotated

from flext_cli import m, u

from flext_web import c, t


class FlextWebModelsWebRequest:
    """Standalone web request/response models."""

    class WebRequest(m.Value):
        """Web request model with complete tracking."""

        method: Annotated[
            c.Web.Method,
            m.BeforeValidator(lambda value: c.Web.Method(str(value).upper())),
            m.Field(description="HTTP method"),
        ] = c.Web.Method.GET
        url: Annotated[
            str,
            m.Field(
                min_length=1,
                max_length=c.Web.VALIDATION_MAX_URL_LENGTH,
                description="Request URL",
            ),
        ]
        headers: Annotated[Mapping[str, str], m.Field(description="HTTP headers")] = (
            m.Field(default_factory=lambda: MappingProxyType[str, str]({}))
        )
        body: Annotated[
            str | t.JsonValue | None,
            m.Field(description="Request body (optional for GET/HEAD)"),
        ] = None
        request_id: Annotated[str, m.Field(description="Unique request identifier")] = (
            m.Field(default_factory=lambda: str(uuid.uuid4()))
        )
        timestamp: Annotated[datetime, m.Field(description="Request timestamp")] = (
            m.Field(default_factory=u.now)
        )

    class WebResponse(m.Value):
        """Web response model with status tracking."""

        request_id: Annotated[str, m.Field(description="Associated request identifier")]
        status_code: Annotated[
            int,
            m.Field(
                ge=c.Web.StatusCode.CONTINUE.value,
                le=c.Web.StatusCode.GATEWAY_TIMEOUT.value,
                description="HTTP status code",
            ),
        ]
        headers: Annotated[
            Mapping[str, str],
            m.Field(description="HTTP response headers"),
        ] = m.Field(default_factory=lambda: MappingProxyType[str, str]({}))
        body: Annotated[
            str | t.JsonValue | None,
            m.Field(description="Response body (optional for 204 No Content)"),
        ] = None
        response_id: Annotated[
            str,
            m.Field(description="Unique response identifier"),
        ] = m.Field(default_factory=lambda: str(uuid.uuid4()))
        timestamp: Annotated[datetime, m.Field(description="Response timestamp")] = (
            m.Field(default_factory=u.now)
        )


__all__: list[str] = ["FlextWebModelsWebRequest"]
