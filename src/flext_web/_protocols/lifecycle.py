"""Web lifecycle protocol shard.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from flext_cli import p
from flext_web import t


class FlextWebProtocolsLifecycle:
    """Lifecycle protocol shard: application and service management."""

    class Web:
        """Web lifecycle protocols."""

        @runtime_checkable
        class WebAppManager(p.Service[t.Web.ResponseDict], Protocol):
            """Protocol for web application lifecycle management."""

            @staticmethod
            def create_app(
                name: str, port: int, host: str
            ) -> p.Result[t.Web.ResponseDict]:
                """Create a new web application."""
                ...

            @staticmethod
            def start_app(app_id: str) -> p.Result[t.Web.ResponseDict]:
                """Start a web application."""
                ...

            @staticmethod
            def stop_app(app_id: str) -> p.Result[t.Web.ResponseDict]:
                """Stop a web application."""
                ...

            @staticmethod
            def list_apps() -> p.Result[Sequence[t.Web.ResponseDict]]:
                """List all registered web applications."""
                ...

        @runtime_checkable
        class WebService(p.Service[t.Web.ResponseDict], Protocol):
            """Protocol for web service lifecycle operations."""

            @staticmethod
            def configure_middleware() -> p.Result[bool]:
                """Configure web middleware."""
                ...

            @staticmethod
            def initialize_routes() -> p.Result[bool]:
                """Initialize service routes."""
                ...

            @staticmethod
            def start_service() -> p.Result[bool]:
                """Start the web service."""
                ...

            @staticmethod
            def stop_service() -> p.Result[bool]:
                """Stop the web service."""
                ...


__all__: list[str] = ["FlextWebProtocolsLifecycle"]
