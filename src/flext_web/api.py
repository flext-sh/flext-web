"""Public MRO facade for flext-web.

This module exposes the canonical public interface: one facade class and one
shared alias instance.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar, Self

from flext_web import (
    FlextWebApp,
    FlextWebAuth,
    FlextWebEntities,
    FlextWebHandlers,
    FlextWebHealth,
    FlextWebServices,
)


class FlextWeb(
    FlextWebApp,
    FlextWebServices,
    FlextWebAuth,
    FlextWebEntities,
    FlextWebHealth,
    FlextWebHandlers,
):
    """Canonical public facade composed via MRO."""

    _instance: ClassVar[Self | None] = None

    @classmethod
    def instance(cls) -> Self:
        """Return the shared facade instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


web = FlextWeb.instance()


__all__: list[str] = ["FlextWeb", "web"]
