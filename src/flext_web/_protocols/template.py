"""Web template-engine protocol shard.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable, TYPE_CHECKING

from flext_cli import p
from flext_web import t

if TYPE_CHECKING:
    from collections.abc import Callable


class FlextWebProtocolsTemplate:
    """Template-engine protocol shard."""

    class Web:
        """Web template protocols."""

        @runtime_checkable
        class WebTemplateEngine(p.Service[t.Web.ResponseDict], Protocol):
            """Protocol for template-engine operations."""

            @staticmethod
            def template_config() -> p.Result[t.Web.ResponseDict]:
                """Return template configuration."""
                ...

            @staticmethod
            def load_template_config(settings: t.Web.RequestDict) -> p.Result[bool]:
                """Load template configuration."""
                ...

            @staticmethod
            def render(template: str, context: t.Web.RequestDict) -> p.Result[str]:
                """Render a template string with context."""
                ...

            @staticmethod
            def validate_template_config(settings: t.Web.RequestDict) -> p.Result[bool]:
                """Validate template configuration."""
                ...

            def add_filter(self, name: str, filter_func: Callable[[str], str]) -> None:
                """Register a template filter."""
                ...

            def add_global(self, name: str, *, value: t.JsonValue) -> None:
                """Register a template global."""
                ...


__all__: list[str] = ["FlextWebProtocolsTemplate"]
