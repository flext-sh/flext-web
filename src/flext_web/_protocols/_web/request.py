# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_web/_protocols/_web/request
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


class FlextWebProtocolsWebRequest:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class WebRequest(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def method(self) -> FlextWebConstantsValues.Method:
            """HTTP method."""
            ...

        @property
        def url(self) -> str:
            """Request URL."""
            ...

        @property
        def headers(self) -> Mapping[str, str]:
            """HTTP headers."""
            ...

        @property
        def body(self) -> str | t.JsonValue | None:
            """Request body (optional for GET/HEAD)."""
            ...

        @property
        def request_id(self) -> str:
            """Unique request identifier."""
            ...

        @property
        def timestamp(self) -> datetime:
            """Request timestamp."""
            ...

    @runtime_checkable
    class WebResponse(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def request_id(self) -> str:
            """Associated request identifier."""
            ...

        @property
        def status_code(self) -> int:
            """HTTP status code."""
            ...

        @property
        def headers(self) -> Mapping[str, str]:
            """HTTP response headers."""
            ...

        @property
        def body(self) -> str | t.JsonValue | None:
            """Response body (optional for 204 No Content)."""
            ...

        @property
        def response_id(self) -> str:
            """Unique response identifier."""
            ...

        @property
        def timestamp(self) -> datetime:
            """Response timestamp."""
            ...


__all__: list[str] = [
    "FlextWebProtocolsWebRequest",
]
