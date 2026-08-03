# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web.services package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .app import FlextWebApp as FlextWebApp
    from .auth import FlextWebAuth as FlextWebAuth
    from .entities import FlextWebEntities as FlextWebEntities
    from .handlers import FlextWebHandlers as FlextWebHandlers
    from .health import FlextWebHealth as FlextWebHealth
    from .web import FlextWebServices as FlextWebServices

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    ".app": ("FlextWebApp",),
    ".auth": ("FlextWebAuth",),
    ".entities": ("FlextWebEntities",),
    ".handlers": ("FlextWebHandlers",),
    ".health": ("FlextWebHealth",),
    ".web": ("FlextWebServices",),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextWebApp",
    "FlextWebAuth",
    "FlextWebEntities",
    "FlextWebHandlers",
    "FlextWebHealth",
    "FlextWebServices",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
