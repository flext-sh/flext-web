"""Web template-engine protocol shard.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import p

from flext_web import t

if TYPE_CHECKING:
    from collections.abc import Callable


class FlextWebProtocolsTemplate:
    """Template-engine protocol shard."""

    @runtime_checkable
    class WebTemplateEngine(p.Service[t.Web.ResponseDict], Protocol):
        """Protocol for template-engine operations."""

        @staticmethod
        def template_config() -> p.Result[t.Web.ResponseDict]:
            """Return template configuration."""
            ...

        @staticmethod
        def load_template_config(settings: t.Web.RequestDict) -> p.Result[bool]:
            """Load template configuration.

            Args:
                settings: Configuration payload to load.

            Returns:
                Ok with ``True`` when the configuration loads, or Fail
                with the load error.

            """
            ...

        @staticmethod
        def render(template: str, context: t.Web.RequestDict) -> p.Result[str]:
            """Render a template string with context.

            Args:
                template: Template source text.
                context: Values substituted into the template.

            Returns:
                Ok with the rendered text, or Fail with the render error.

            """
            ...

        @staticmethod
        def validate_template_config(settings: t.Web.RequestDict) -> p.Result[bool]:
            """Validate template configuration.

            Args:
                settings: Configuration payload to validate.

            Returns:
                Ok with ``True`` when the configuration is valid, or Fail
                with the validation error.

            """
            ...

        def add_filter(self, name: str, filter_func: Callable[[str], str]) -> None:
            """Register a template filter.

            Args:
                name: Filter name available inside templates.
                filter_func: Callable applied to template values.

            """
            ...

        def add_global(self, name: str, *, value: t.JsonValue) -> None:
            """Register a template global.

            Args:
                name: Global name available inside templates.
                value: JSON-compatible value exposed to templates.

            """
            ...


__all__: list[str] = ["FlextWebProtocolsTemplate"]
