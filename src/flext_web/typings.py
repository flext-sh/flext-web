"""FLEXT Web Types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliTypes

from ._typings.base import FlextWebTypingsBase
from ._typings.web import FlextWebTypingsWeb


class FlextWebTypes(FlextCliTypes):
    """Web-specific type definitions extending t via MRO."""

    class Web(FlextWebTypingsWeb, FlextWebTypingsBase):
        """Web domain namespace (flat members per AGENTS.md §149)."""


t = FlextWebTypes

__all__: list[str] = ["FlextWebTypes", "t"]
