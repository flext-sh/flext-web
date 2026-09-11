# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web.services package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .app import FlextWebApp
    from .auth import FlextWebAuth
    from .entities import FlextWebEntities
    from .handlers import FlextWebHandlers
    from .health import FlextWebHealth
    from .web import FlextWebServices
__all__: tuple[str, ...] = (
    "FlextWebApp",
    "FlextWebAuth",
    "FlextWebEntities",
    "FlextWebHandlers",
    "FlextWebHealth",
    "FlextWebServices",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".app": ("FlextWebApp",),
            ".auth": ("FlextWebAuth",),
            ".entities": ("FlextWebEntities",),
            ".handlers": ("FlextWebHandlers",),
            ".health": ("FlextWebHealth",),
            ".web": ("FlextWebServices",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
