"""FLEXT Web protocols — pure ``@runtime_checkable`` Protocol surface.

Per AGENTS.md §2.7 (Library Abstraction) + python.md §5a: this module
contains ONLY Protocol class definitions. All runtime/implementation code
lives in ``flext_web.utilities`` (``FlextWebUtilities.Web``).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol, runtime_checkable

from flext_cli import p
from starlette.responses import Response as StarletteResponse

from flext_web import t


class FlextWebProtocols(p):
    """Web-specific ``@runtime_checkable`` Protocol surface extending ``p``."""

    class Web:
        """Web domain-specific Protocols."""

        @runtime_checkable
        class FastApiLikeApp(Protocol):
            """Duck-type protocol for FastAPI-like framework apps."""

            def add_api_route(
                self,
                path: str,
                endpoint: Callable[..., t.Web.ResponseDict],
                **kwargs: t.Scalar,
            ) -> None:
                """Register an API route."""
                ...

            def middleware(
                self,
                middleware_type: str,
            ) -> Callable[..., Callable[..., StarletteResponse]]:
                """Register middleware."""
                ...

        @runtime_checkable
        class FlaskLikeApp(Protocol):
            """Duck-type protocol for Flask-like framework apps."""

            def before_request(self, f: Callable[..., None]) -> Callable[..., None]:
                """Register a before-request hook."""
                ...

            def route(
                self,
                rule: str,
                **options: t.Scalar,
            ) -> Callable[..., Callable[..., t.Web.ResponseDict]]:
                """Register a URL route."""
                ...


__all__: list[str] = ["FlextWebProtocols"]
