# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web. Utilities package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_web._utilities.base import FlextWebUtilitiesBase
    from flext_web._utilities.web import FlextWebUtilitiesWeb


__all__: tuple[str, ...] = ("FlextWebUtilitiesBase", "FlextWebUtilitiesWeb")

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextWebUtilitiesBase": ".base",
        "FlextWebUtilitiesWeb": ".web",
    }),
    public_exports=__all__,
)
