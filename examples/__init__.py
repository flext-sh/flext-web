# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_cli import d, e, h, r, x

    from flext_core import (
        core,
        d,
        e,
        h,
        lazy,
        lazy_attribute,
        normalize_lazy_imports,
        r,
        x,
    )
    from flext_web import c, config, m, main, p, s, settings, t, u, web

    from .constants import FlextWebExamplesConstants
    from .models import FlextWebExamplesModels
    from .protocols import FlextWebExamplesProtocols
    from .typings import FlextWebExamplesTypes
    from .utilities import FlextWebExamplesUtilities
__all__: tuple[str, ...] = (
    "FlextWebExamplesConstants",
    "FlextWebExamplesModels",
    "FlextWebExamplesProtocols",
    "FlextWebExamplesTypes",
    "FlextWebExamplesUtilities",
    "c",
    "cli",
    "config",
    "core",
    "d",
    "e",
    "from_json",
    "h",
    "lazy",
    "lazy_attribute",
    "m",
    "main",
    "normalize_lazy_imports",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "to_json",
    "to_jsonable_python",
    "u",
    "web",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".constants": ("ExamplesFlextWebConstants", "c"),
            ".models": ("ExamplesFlextWebModels", "m"),
            ".protocols": ("ExamplesFlextWebProtocols", "p"),
            ".typings": ("ExamplesFlextWebTypes", "t"),
            ".utilities": ("ExamplesFlextWebUtilities", "u"),
            "flext_cli": ("d", "e", "h", "r", "x"),
            "flext_web": ("FlextWebConstants", "s"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
