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
    from flext_cli import d as d, e as e, h as h, r as r, x as x
    from flext_web.api import FlextWeb as FlextWeb, web as web
    from flext_web.base import FlextWebServiceBase as FlextWebServiceBase, s as s
    from flext_web.constants import FlextWebConstants as FlextWebConstants, c as c
    from flext_web.models import FlextWebModels as FlextWebModels, m as m
    from flext_web.protocols import FlextWebProtocols as FlextWebProtocols, p as p
    from flext_web.settings import FlextWebSettings as FlextWebSettings
    from flext_web.typings import FlextWebTypes as FlextWebTypes, t as t
    from flext_web.utilities import FlextWebUtilities as FlextWebUtilities, u as u
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".api": (
            "FlextWeb",
            "web",
        ),
        ".base": (
            "FlextWebServiceBase",
            "s",
        ),
        ".constants": (
            "FlextWebConstants",
            "c",
        ),
        ".models": (
            "FlextWebModels",
            "m",
        ),
        ".protocols": (
            "FlextWebProtocols",
            "p",
        ),
        ".settings": ("FlextWebSettings",),
        ".typings": (
            "FlextWebTypes",
            "t",
        ),
        ".utilities": (
            "FlextWebUtilities",
            "u",
        ),
        "flext_cli": (
            "d",
            "e",
            "h",
            "r",
            "x",
        ),
    },
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
    "t",
    "u",
    "web",
    "x",
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    public_exports=__all__,
)
