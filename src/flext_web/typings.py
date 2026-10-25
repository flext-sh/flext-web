# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Web Types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliTypes

from flext_web._typings import FlextWebTypingsBase, FlextWebTypingsWeb


class FlextWebTypes(FlextCliTypes):
    """Web-specific type definitions extending t via MRO."""

    class Web(FlextWebTypingsBase, FlextWebTypingsWeb):
        """Web domain namespace (flat members per AGENTS.md §149)."""


t = FlextWebTypes
__all__: list[str] = ["FlextWebTypes", "t"]
