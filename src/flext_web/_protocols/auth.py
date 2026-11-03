# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_web/_protocols/auth
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

from flext_web import t


class FlextWebProtocolsAuth:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class Credentials(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def username(self) -> str:
            """Username."""
            ...

        @property
        def password(self) -> str:
            """Password."""
            ...

    @runtime_checkable
    class UserData(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def username(self) -> str:
            """Username."""
            ...

        @property
        def email(self) -> str:
            """Email address."""
            ...

        @property
        def password(self) -> str:
            """Password (empty string if not provided)."""
            ...

    @runtime_checkable
    class AppData(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def name(self) -> str:
            """Application name."""
            ...

        @property
        def host(self) -> str:
            """Application host."""
            ...

        @property
        def port(self) -> t.PortNumber:
            """Application port."""
            ...

    @runtime_checkable
    class EntityData(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def data(self) -> t.ConfigurationMapping:
            """Entity data dictionary."""
            ...


__all__: list[str] = [
    "FlextWebProtocolsAuth",
]
