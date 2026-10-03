# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from examples.constants import FlextWebExamplesConstants
    from examples.models import FlextWebExamplesModels
    from examples.protocols import FlextWebExamplesProtocols
    from examples.typings import FlextWebExamplesTypes
    from examples.utilities import FlextWebExamplesUtilities
    from flext_web import c, d, e, h, m, p, r, s, t, u, x


__all__: tuple[str, ...] = (
    "FlextWebExamplesConstants",
    "FlextWebExamplesModels",
    "FlextWebExamplesProtocols",
    "FlextWebExamplesTypes",
    "FlextWebExamplesUtilities",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".constants": ("FlextWebExamplesConstants",),
            ".models": ("FlextWebExamplesModels",),
            ".protocols": ("FlextWebExamplesProtocols",),
            ".typings": ("FlextWebExamplesTypes",),
            ".utilities": ("FlextWebExamplesUtilities",),
            "flext_web": ("c", "d", "e", "h", "m", "p", "r", "s", "t", "u", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
