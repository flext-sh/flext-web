"""Web framework duck-type protocol shard.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Callable

    from flext_web import t


class FlextWebProtocolsFramework:
    """Framework duck-type protocol shard."""

    class Web:
        """Web framework protocols."""

        @runtime_checkable
        class FrameworkResponse(Protocol):
            """Protocol for framework response objects exposed by middleware."""

            @property
            def status_code(self) -> int:
                """The HTTP status code."""
                ...

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
                self, middleware_type: str
            ) -> Callable[
                ..., Callable[..., FlextWebProtocolsFramework.Web.FrameworkResponse]
            ]:
                """Register middleware."""
                ...

        @runtime_checkable
        class FlaskLikeApp(Protocol):
            """Duck-type protocol for Flask-like framework apps."""

            def before_request(self, f: Callable[..., None]) -> Callable[..., None]:
                """Register a before-request hook."""
                ...

            def route(
                self, rule: str, **options: t.Scalar
            ) -> Callable[..., Callable[..., t.Web.ResponseDict]]:
                """Register a URL route."""
                ...


__all__: list[str] = ["FlextWebProtocolsFramework"]
