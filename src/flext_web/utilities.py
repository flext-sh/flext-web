# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Web utilities facade.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from flext_cli import u

from flext_web._utilities import FlextWebUtilitiesBase, FlextWebUtilitiesWeb


class FlextWebUtilities(u):
    """Web-specific utilities delegating to flext-core.

    Inherits from u and ensures consistency.
    Provides only web-domain-specific functionality not available in u.
    All generic operations delegate to flext-core utilities.
    Uses advanced builder/DSL patterns for composition.
    """

    class Web(FlextWebUtilitiesWeb, FlextWebUtilitiesBase):
        """Web domain-specific runtime utilities."""


u = FlextWebUtilities
__all__: list[str] = ["FlextWebUtilities", "u"]
