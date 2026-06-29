"""Web data-access protocol shard.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from flext_cli import p
from flext_web import t


class FlextWebProtocolsData:
    """Data-access protocol shard."""

    class Web:
        """Web data protocols."""

        @runtime_checkable
        class WebRepository(Protocol):
            """Protocol for web application persistence operations."""

            @staticmethod
            def fetch_by_id(entity_id: str) -> p.Result[t.Web.ResponseDict]:
                """Fetch a single application record by id."""
                ...

            @staticmethod
            def save(entity: t.Web.ResponseDict) -> p.Result[t.Web.ResponseDict]:
                """Persist an application record."""
                ...

            @staticmethod
            def delete(entity_id: str) -> p.Result[bool]:
                """Delete an application record."""
                ...

            @staticmethod
            def find_all() -> p.Result[Sequence[t.Web.ResponseDict]]:
                """Return all application records."""
                ...

            @staticmethod
            def find_by_criteria(
                criteria: t.Web.RequestDict,
            ) -> p.Result[Sequence[t.Web.ResponseDict]]:
                """Return records matching the given criteria."""
                ...

        @runtime_checkable
        class WebHandler(Protocol):
            """Protocol for request handling helpers."""

            @staticmethod
            def handle_request(
                request: t.Web.RequestDict,
            ) -> p.Result[t.Web.ResponseDict]:
                """Handle a web request payload."""
                ...

            def execute(
                self,
                command: t.Web.RequestDict,
            ) -> p.Result[t.Web.ResponseDict]:
                """Execute a handler command."""
                ...


__all__: list[str] = ["FlextWebProtocolsData"]
