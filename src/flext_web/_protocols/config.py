"""Web configuration scalar protocol shard.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, override, runtime_checkable, TYPE_CHECKING


if TYPE_CHECKING:
    from flext_web import t


class FlextWebProtocolsConfig:
    """Configuration scalar protocol shard."""

    class Web:
        """Web configuration protocols."""

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


__all__: list[str] = ["FlextWebProtocolsConfig"]
