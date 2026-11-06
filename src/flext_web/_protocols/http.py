# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_web/_protocols/http
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

if TYPE_CHECKING:
    from flext_web import c, t


class FlextWebProtocolsHttp:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class Message(FlextCliProtocols.BaseModel, Protocol):
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

    @runtime_checkable
    class Request(Message, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def url(self) -> str:
            """Request URL."""
            ...

        @property
        def method(self) -> c.Web.Method:
            """HTTP method (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)."""
            ...

        @property
        def timeout(self) -> t.PositiveTimeout:
            """Request timeout in seconds."""
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
    class Response(Message, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def status_code(self) -> t.HttpStatusCode:
            """HTTP status code."""
            ...

        @property
        def elapsed_time(self) -> t.NonNegativeFloat | None:
            """Response processing time in seconds."""
            ...

        @property
        def error(self) -> bool:
            """Whether HTTP status indicates client or server error."""
            ...

        @property
        def success(self) -> bool:
            """Whether HTTP status indicates success (2xx range)."""
            ...


__all__: list[str] = [
    "FlextWebProtocolsHttp",
]
