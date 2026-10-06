"""FLEXT Web constants.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_cli import FlextCliConstants

from flext_web._constants.base import FlextWebConstantsBase
from flext_web._constants.values import FlextWebConstantsValues

if TYPE_CHECKING:
    from flext_web import t


class FlextWebConstants(FlextCliConstants):
    """Immutable project-specific constants organized by domain."""

    class Web(FlextWebConstantsBase, FlextWebConstantsValues):
        """Web domain constants namespace."""


c = FlextWebConstants

__all__: t.StrSequence = ("FlextWebConstants", "c")
