# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_cli import cli, core, d, e, h, lazy_attribute, r, services, x

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
    "h",
    "lazy_attribute",
    "m",
    "main",
    "p",
    "r",
    "s",
    "services",
    "settings",
    "t",
    "u",
    "web",
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
            "flext_cli": (
                "cli",
                "core",
                "d",
                "e",
                "h",
                "lazy_attribute",
                "r",
                "services",
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
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
