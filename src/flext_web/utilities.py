"""FLEXT Web utilities facade.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliUtilities

from flext_web import t
from flext_web._utilities.base import FlextWebUtilitiesBase
from flext_web._utilities.web import FlextWebUtilitiesWeb


class FlextWebUtilities(FlextCliUtilities):
    """Web-specific utilities delegating to flext-core.

    Inherits from u and ensures consistency.
    Provides only web-domain-specific functionality not available in u.
    All generic operations delegate to flext-core utilities.
    Uses advanced builder/DSL patterns for composition.
    """

    class Web(FlextWebUtilitiesBase, FlextWebUtilitiesWeb):
        """Web domain-specific runtime utilities."""


u = FlextWebUtilities

__all__: t.MutableSequenceOf[str] = ["FlextWebUtilities", "u"]
