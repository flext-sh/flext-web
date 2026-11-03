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
    class SystemInfo(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def service_name(self) -> str:
            """Service name."""
            ...

        @property
        def service_type(self) -> str:
            """Service type."""
            ...

        @property
        def architecture(self) -> str:
            """Architecture pattern."""
            ...

        @property
        def patterns(self) -> Sequence[str]:
            """Design patterns used."""
            ...

        @property
        def integrations(self) -> Sequence[str]:
            """Integrated components."""
            ...

        @property
        def capabilities(self) -> Sequence[str]:
            """Service capabilities."""
            ...

    @runtime_checkable
    class HealthStatus(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def status(self) -> str:
            """Health status."""
            ...

        @property
        def service(self) -> str:
            """Service name."""
            ...

        @property
        def version(self) -> str:
            """Service version."""
            ...

        @property
        def timestamp(self) -> str:
            """Status timestamp."""
            ...

        @property
        def components(self) -> Mapping[str, str]:
            """Component statuses."""
            ...


__all__: list[str] = [
    "FlextWebProtocolsSystem",
]
