# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_web/_protocols/system
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Protocol, runtime_checkable

from flext_cli import FlextCliProtocols


class FlextWebProtocolsSystem:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class SystemInfo(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        service_name: str
        service_type: str
        architecture: str
        patterns: Sequence[str]
        integrations: Sequence[str]
        capabilities: Sequence[str]

    @runtime_checkable
    class HealthStatus(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        status: str
        service: str
        version: str
        timestamp: str
        components: Mapping[str, str]


__all__: list[str] = [
    "FlextWebProtocolsSystem",
]
