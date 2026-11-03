# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_web/_protocols/_web/message
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_web._protocols import FlextWebProtocolsHttp

if TYPE_CHECKING:
    from flext_web import t


class FlextWebProtocolsWebMessage:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class AppRequest(FlextWebProtocolsHttp.Request, Protocol):
        """Structural data contract projected from the owning model."""

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

    @runtime_checkable
    class AppResponse(FlextWebProtocolsHttp.Response, Protocol):
        """Structural data contract projected from the owning model."""

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
        def processing_time_seconds(self) -> float:
            """Convert processing time from milliseconds to seconds."""
            ...


__all__: list[str] = [
    "FlextWebProtocolsWebMessage",
]
