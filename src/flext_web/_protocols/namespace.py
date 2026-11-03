# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_web/_protocols/namespace
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_cli import FlextCliProtocols


class FlextWebProtocolsNamespace:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class ConfigNamespace(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""


__all__: list[str] = [
    "FlextWebProtocolsNamespace",
]
