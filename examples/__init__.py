# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_core import d, e, h, r, x
<<<<<<< HEAD
    from flext_web import FlextWebConstants, s
=======
    from flext_web import FlextWebConstants, FlextWebConstants as c, m, p, s, t, u
>>>>>>> refs/remotes/origin/0.12.0-dev

    from .constants import ExamplesFlextWebConstants, ExamplesFlextWebConstants as c
    from .models import ExamplesFlextWebModels, ExamplesFlextWebModels as m
    from .protocols import ExamplesFlextWebProtocols, ExamplesFlextWebProtocols as p
    from .typings import ExamplesFlextWebTypes, ExamplesFlextWebTypes as t
    from .utilities import ExamplesFlextWebUtilities, ExamplesFlextWebUtilities as u
__all__: tuple[str, ...] = (
    "ExamplesFlextWebConstants",
    "ExamplesFlextWebModels",
    "ExamplesFlextWebProtocols",
    "ExamplesFlextWebTypes",
    "ExamplesFlextWebUtilities",
    "FlextWebConstants",
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
<<<<<<< HEAD
            ".constants": ("ExamplesFlextWebConstants", "c"),
            ".models": ("ExamplesFlextWebModels", "m"),
            ".protocols": ("ExamplesFlextWebProtocols", "p"),
            ".typings": ("ExamplesFlextWebTypes", "t"),
            ".utilities": ("ExamplesFlextWebUtilities", "u"),
            "flext_core": ("d", "e", "h", "r", "x"),
            "flext_web": ("FlextWebConstants", "s"),
=======
            ".constants": ("ExamplesFlextWebConstants",),
            ".models": ("ExamplesFlextWebModels",),
            ".protocols": ("ExamplesFlextWebProtocols",),
            ".typings": ("ExamplesFlextWebTypes",),
            ".utilities": ("ExamplesFlextWebUtilities",),
            "flext_core": ("d", "e", "h", "r", "x"),
            "flext_web": ("FlextWebConstants", "c", "m", "p", "s", "t", "u"),
>>>>>>> refs/remotes/origin/0.12.0-dev
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
