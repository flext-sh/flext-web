# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
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

    from .constants import FlextWebExamplesConstants, FlextWebExamplesConstants as c
    from .models import FlextWebExamplesModels, FlextWebExamplesModels as m
    from .protocols import FlextWebExamplesProtocols, FlextWebExamplesProtocols as p
    from .typings import FlextWebExamplesTypes, FlextWebExamplesTypes as t
    from .utilities import FlextWebExamplesUtilities, FlextWebExamplesUtilities as u
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
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
