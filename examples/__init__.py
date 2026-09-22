# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
<<<<<<< HEAD
    from flext_cli import cli
    from pydantic_core import from_json, to_json, to_jsonable_python

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
=======
    from flext_core import d, e, h, r, x
    from flext_web import FlextWebConstants, s
>>>>>>> origin/0.12.0-dev

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
<<<<<<< HEAD
            ".constants": ("FlextWebExamplesConstants",),
            ".models": ("FlextWebExamplesModels",),
            ".protocols": ("FlextWebExamplesProtocols",),
            ".typings": ("FlextWebExamplesTypes",),
            ".utilities": ("FlextWebExamplesUtilities",),
            "flext_cli": ("cli",),
            "flext_core": (
                "core",
                "d",
                "e",
                "h",
                "lazy",
                "lazy_attribute",
                "normalize_lazy_imports",
                "r",
                "x",
            ),
            "flext_web": (
                "c",
                "config",
                "m",
                "main",
                "p",
                "s",
                "settings",
                "t",
                "u",
                "web",
            ),
            "pydantic_core": ("from_json", "to_json", "to_jsonable_python"),
=======
            ".constants": ("ExamplesFlextWebConstants", "c"),
            ".models": ("ExamplesFlextWebModels", "m"),
            ".protocols": ("ExamplesFlextWebProtocols", "p"),
            ".typings": ("ExamplesFlextWebTypes", "t"),
            ".utilities": ("ExamplesFlextWebUtilities", "u"),
            "flext_core": ("d", "e", "h", "r", "x"),
            "flext_web": ("FlextWebConstants", "s"),
>>>>>>> origin/0.12.0-dev
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
