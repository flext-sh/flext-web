"""Runtime mixin for the public flext-web facade."""

from __future__ import annotations

from typing import ClassVar, Self


class FlextWebApiRuntime:
    """Provide shared instance lifecycle for the public API facade."""

    _instance: ClassVar[Self | None] = None

    @classmethod
    def instance(cls) -> Self:
        """Return the shared facade instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


__all__: list[str] = ["FlextWebApiRuntime"]
