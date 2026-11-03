# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_web/_protocols/_web/message
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

from flext_web import t

if TYPE_CHECKING:
    from flext_web._constants import FlextWebConstantsValues


class FlextWebProtocolsWebMessage:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class AppRequest(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def headers(self) -> Mapping[str, str]:
            """HTTP headers for message."""
            ...

        @property
        def body(self) -> str | Mapping[str, t.Scalar] | None:
            """Message body content (optional for GET/HEAD)."""
            ...

        @property
        def timestamp(self) -> datetime:
            """Timestamp of message creation (configured timezone)."""
            ...

        @property
        def url(self) -> str:
            """Request URL."""
            ...

        @property
        def method(self) -> FlextWebConstantsValues.Method:
            """HTTP method (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)."""
            ...

        @property
        def timeout(self) -> t.PositiveTimeout:
            """Request timeout in seconds."""
            ...

        @property
        def request_id(self) -> str:
            """Unique request identifier."""
            ...

        @property
        def query_params(self) -> t.ConfigurationMapping:
            """Query string parameters."""
            ...

        @property
        def client_ip(self) -> str:
            """Client IP address."""
            ...

        @property
        def user_agent(self) -> str:
            """Client user agent."""
            ...

        @property
        def has_body(self) -> bool:
            """Whether HTTP request has a message body."""
            ...

        @property
        def secure(self) -> bool:
            """Whether HTTP request uses HTTPS protocol."""
            ...

    @runtime_checkable
    class AppResponse(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def headers(self) -> Mapping[str, str]:
            """HTTP headers for message."""
            ...

        @property
        def body(self) -> str | Mapping[str, t.Scalar] | None:
            """Message body content (optional for GET/HEAD)."""
            ...

        @property
        def timestamp(self) -> datetime:
            """Timestamp of message creation (configured timezone)."""
            ...

        @property
        def status_code(self) -> t.HttpStatusCode:
            """HTTP status code."""
            ...

        @property
        def elapsed_time(self) -> t.NonNegativeFloat | None:
            """Response elapsed time in seconds."""
            ...

        @property
        def response_id(self) -> str:
            """Unique response identifier."""
            ...

        @property
        def request_id(self) -> str:
            """Associated request identifier."""
            ...

        @property
        def content_type(self) -> str:
            """Response content type."""
            ...

        @property
        def content_length(self) -> t.NonNegativeInt:
            """Response body length in bytes."""
            ...

        @property
        def processing_time_ms(self) -> t.NonNegativeFloat:
            """Processing time in milliseconds."""
            ...

        @property
        def error(self) -> bool:
            """Whether HTTP status indicates client or server error."""
            ...

        @property
        def success(self) -> bool:
            """Whether HTTP status indicates success (2xx range)."""
            ...

        @property
        def processing_time_seconds(self) -> float:
            """Convert processing time from milliseconds to seconds."""
            ...


__all__: list[str] = [
    "FlextWebProtocolsWebMessage",
]
