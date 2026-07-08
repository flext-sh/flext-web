"""Standalone web request/response models for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Annotated

from flext_web import c, m, t, u

from ._base import FlextWebModelsBase


class FlextWebModelsWebRequest:
    """Standalone web request/response models namespace."""

    class Web:
        """Standalone web request/response models."""

        class WebRequest(m.Value):
            """Web request model with complete tracking."""

            method: Annotated[
                c.Web.Method,
                u.PlainValidator(FlextWebModelsBase.coerce_method),
                u.Field(
                    description="HTTP method",
                ),
            ] = c.Web.Method.GET
            url: Annotated[
                str,
                u.Field(
                    min_length=1,
                    max_length=c.Web.VALIDATION_MAX_URL_LENGTH,
                    description="Request URL",
                ),
            ]
            headers: Annotated[
                t.MutableStrMapping,
                u.Field(
                    description="HTTP headers",
                ),
            ] = u.Field(default_factory=dict)
            body: Annotated[
                str | t.JsonValue | None,
                u.Field(
                    description="Request body (optional for GET/HEAD)",
                ),
            ] = None
            request_id: Annotated[
                str,
                u.Field(
                    description="Unique request identifier",
                ),
            ] = u.Field(default_factory=lambda: str(uuid.uuid4()))
            timestamp: Annotated[
                datetime,
                u.Field(
                    description="Request timestamp",
                ),
            ] = u.Field(default_factory=u.now)

        class WebResponse(m.Value):
            """Web response model with status tracking."""

            request_id: Annotated[
                str,
                u.Field(description="Associated request identifier"),
            ]
            status_code: Annotated[
                int,
                u.Field(
                    ge=c.Web.StatusCode.CONTINUE.value,
                    le=c.Web.StatusCode.GATEWAY_TIMEOUT.value,
                    description="HTTP status code",
                ),
            ]
            headers: Annotated[
                t.MutableStrMapping,
                u.Field(
                    description="HTTP response headers",
                ),
            ] = u.Field(default_factory=dict)
            body: Annotated[
                str | t.JsonValue | None,
                u.Field(
                    description="Response body (optional for 204 No Content)",
                ),
            ] = None
            response_id: Annotated[
                str,
                u.Field(
                    description="Unique response identifier",
                ),
            ] = u.Field(default_factory=lambda: str(uuid.uuid4()))
            timestamp: Annotated[
                datetime,
                u.Field(
                    description="Response timestamp",
                ),
            ] = u.Field(default_factory=u.now)


__all__: list[str] = ["FlextWebModelsWebRequest"]
