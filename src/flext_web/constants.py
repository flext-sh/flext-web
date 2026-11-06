# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Web constants.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import c

from flext_web._constants import FlextWebConstantsBase, FlextWebConstantsValues


class FlextWebConstants(c):
    """Immutable project-specific constants organized by domain."""

    class Web(FlextWebConstantsBase, FlextWebConstantsValues):
        """Web domain constants namespace."""


c = FlextWebConstants
__all__: list[str] = ["FlextWebConstants", "c"]
