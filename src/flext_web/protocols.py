"""FLEXT Web protocols — pure ``@runtime_checkable`` Protocol surface.

Per AGENTS.md §2.7 (Library Abstraction) + python.md §5a: this module
contains ONLY Protocol class definitions. All runtime/implementation code
lives in ``flext_web.utilities`` (``FlextWebUtilities.Web``).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Protocol, override, runtime_checkable

from flext_cli import p

from flext_web import t

if TYPE_CHECKING:
    from starlette.responses import Response as StarletteResponse


class FlextWebProtocols(p):
    """Web-specific ``@runtime_checkable`` Protocol surface extending ``p``."""

    class Web:
        """Web domain-specific Protocols."""

        @runtime_checkable
        class WebAppManager(p.Service[t.Web.ResponseDict], Protocol):
            """Protocol for web application lifecycle management."""

            @staticmethod
            def create_app(
                name: str,
                port: int,
                host: str,
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

        @runtime_checkable
        class WebTemplateEngine(p.Service[t.Web.ResponseDict], Protocol):
            """Protocol for template-engine operations."""

            @staticmethod
            def template_config() -> p.Result[t.Web.ResponseDict]:
                """Return template configuration."""
                ...

            @staticmethod
            def load_template_config(
                settings: t.Web.RequestDict,
            ) -> p.Result[bool]:
                """Load template configuration."""
                ...

            @staticmethod
            def render(
                template: str,
                context: t.Web.RequestDict,
            ) -> p.Result[str]:
                """Render a template string with context."""
                ...

            @staticmethod
            def validate_template_config(
                settings: t.Web.RequestDict,
            ) -> p.Result[bool]:
                """Validate template configuration."""
                ...

            def add_filter(self, name: str, filter_func: Callable[[str], str]) -> None:
                """Register a template filter."""
                ...

            def add_global(self, name: str, *, value: t.JsonValue) -> None:
                """Register a template global."""
                ...

        @runtime_checkable
        class WebMonitoring(p.Service[t.Web.ResponseDict], Protocol):
            """Protocol for web monitoring helpers."""

            @staticmethod
            def web_health_status() -> t.Web.ResponseDict:
                """Return web health status."""
                ...

            @staticmethod
            def web_metrics() -> t.Web.ResponseDict:
                """Return web metrics payload."""
                ...

            def record_web_request(
                self,
                request: t.Web.RequestDict,
                response_time: float,
            ) -> None:
                """Record a request observation."""
                ...

        @runtime_checkable
        class ConfigValue(Protocol):
            """Protocol for configuration scalar wrappers."""

            value: t.Scalar

            @override
            def __str__(self) -> str:
                """Convert the value to string."""
                ...

            def __bool__(self) -> bool:
                """Convert the value to boolean."""
                ...

            def __int__(self) -> int:
                """Convert the value to integer."""
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


p = FlextWebProtocols

__all__: list[str] = ["FlextWebProtocols", "p"]
