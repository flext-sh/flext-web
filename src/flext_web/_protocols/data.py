"""Web data-access and request-handling protocol shard.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from flext_cli import p

    from flext_web import t


class FlextWebProtocolsData:
    """Data-access protocol shard: repository and handler patterns."""

    @runtime_checkable
    class WebRepository(Protocol):
        """Protocol for web application persistence operations."""

        @staticmethod
        def fetch_by_id(entity_id: str) -> p.Result[t.Web.ResponseDict]:
            """Fetch a single application record by id.

            Args:
                entity_id: Identifier of the record to fetch.

            Returns:
                Ok with the stored record, or Fail when no record exists.

            """
            ...

        @staticmethod
        def save(entity: t.Web.ResponseDict) -> p.Result[t.Web.ResponseDict]:
            """Persist an application record.

            Args:
                entity: Record payload to store.

            Returns:
                Ok with the stored record, or Fail when persistence fails.

            """
            ...

        @staticmethod
        def delete(entity_id: str) -> p.Result[bool]:
            """Delete an application record.

            Args:
                entity_id: Identifier of the record to delete.

            Returns:
                Ok with ``True`` when a record was removed, ``False``
                when the identifier is unknown.

            """
            ...

        @staticmethod
        def find_all() -> p.Result[Sequence[t.Web.ResponseDict]]:
            """Return all application records."""
            ...

        @staticmethod
        def find_by_criteria(
            criteria: t.Web.RequestDict,
        ) -> p.Result[Sequence[t.Web.ResponseDict]]:
            """Return records matching the given criteria.

            Args:
                criteria: Field/value pairs every record must satisfy.

            Returns:
                Ok with the matching records.

            """
            ...

    @runtime_checkable
    class WebHandler(Protocol):
        """Protocol for request handling helpers."""

        @staticmethod
        def handle_request(request: t.Web.RequestDict) -> p.Result[t.Web.ResponseDict]:
            """Handle a web request payload.

            Args:
                request: Request payload to process.

            Returns:
                Ok with the response payload, or Fail with the handling
                error.

            """
            ...

        def execute(self, command: t.Web.RequestDict) -> p.Result[t.Web.ResponseDict]:
            """Execute a handler command.

            Args:
                command: Command payload to execute.

            Returns:
                Ok with the response payload, or Fail with the execution
                error.

            """
            ...


__all__: list[str] = ["FlextWebProtocolsData"]
