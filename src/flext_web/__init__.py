# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports
from flext_web.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if TYPE_CHECKING:
    from flext_cli import d, e, h, r, x

    from ._settings import FlextWebSettings, settings
    from .api import FlextWeb, web
    from .base import FlextWebServiceBase, s
    from .constants import FlextWebConstants, FlextWebConstants as c
    from .models import FlextWebModels, FlextWebModels as m
    from .protocols import FlextWebProtocols, FlextWebProtocols as p
    from .typings import FlextWebTypes, FlextWebTypes as t
    from .utilities import FlextWebUtilities, FlextWebUtilities as u

    _ = (
        c,
        FlextWebConstants,
        t,
        FlextWebTypes,
        p,
        FlextWebProtocols,
        m,
        FlextWebModels,
        u,
        FlextWebUtilities,
        d,
        e,
        h,
        r,
        x,
        s,
        FlextWebServiceBase,
        FlextWebSettings,
        settings,
        FlextWeb,
        web,
    )


_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._settings": ("FlextWebSettings", "settings"),
    ".api": ("FlextWeb", "web"),
    ".base": ("FlextWebServiceBase", "s"),
    ".constants": ("FlextWebConstants", "c"),
    ".models": ("FlextWebModels", "m"),
    ".protocols": ("FlextWebProtocols", "p"),
    ".typings": ("FlextWebTypes", "t"),
    ".utilities": ("FlextWebUtilities", "u"),
    "flext_cli": ("d", "e", "h", "r", "x"),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_DIRECT_IMPORTS: tuple[str, ...] = (
    "FlextWeb",
    "FlextWebConstants",
    "FlextWebModels",
    "FlextWebProtocols",
    "FlextWebServiceBase",
    "FlextWebSettings",
    "FlextWebTypes",
    "FlextWebUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "build_lazy_import_map",
    "c",
    "d",
    "e",
    "h",
    "install_lazy_exports",
    "m",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "u",
    "web",
    "x",
)

__all__: tuple[str, ...] = (
    "FlextWeb",
    "FlextWebConstants",
    "FlextWebModels",
    "FlextWebProtocols",
    "FlextWebServiceBase",
    "FlextWebSettings",
    "FlextWebTypes",
    "FlextWebUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "u",
    "web",
    "x",
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
