"""Web configuration scalar protocol shard.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, override, runtime_checkable

from flext_cli import FlextCliProtocols

if TYPE_CHECKING:
    from flext_web import t


class FlextWebProtocolsConfig:
    """Configuration scalar protocol shard."""

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
    class FastAPIAppConfig(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        title: str
        version: str
        description: str
        debug: bool
        testing: bool
        docs_url: str
        redoc_url: str
        openapi_url: str


__all__: list[str] = ["FlextWebProtocolsConfig"]
