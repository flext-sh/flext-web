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
            """Register an API route.

            Args:
                path: URL path served by the route.
                endpoint: Callable producing the route response.
                **kwargs: Framework-specific route options.

            """
            ...

        def middleware(
            self,
            middleware_type: str,
        ) -> Callable[..., Callable[..., FlextWebProtocolsFramework.FrameworkResponse]]:
            """Register middleware.

            Args:
                middleware_type: Framework middleware class name.

            Returns:
                Decorator wrapping the middleware handler.

            """
            ...


__all__: list[str] = ["FlextWebProtocolsFramework"]
