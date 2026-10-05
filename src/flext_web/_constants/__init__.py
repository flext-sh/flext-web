# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web. Constants package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_web._constants.base import FlextWebConstantsBase
    from flext_web._constants.values import FlextWebConstantsValues


__all__: tuple[str, ...] = ("FlextWebConstantsBase", "FlextWebConstantsValues")

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextWebConstantsBase": ".base",
        "FlextWebConstantsValues": ".values",
    }),
    public_exports=__all__,
)
