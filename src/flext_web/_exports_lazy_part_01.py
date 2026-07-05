# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

FLEXT_WEB_LAZY_IMPORTS_PART_01 = build_lazy_import_map(
    {
        "._models": ("_models",),
        "._protocols": ("_protocols",),
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
        ".services": ("services",),
        ".services.app": ("FlextWebApp",),
        ".services.auth": ("FlextWebAuth",),
        ".services.entities": ("FlextWebEntities",),
        ".services.handlers": ("FlextWebHandlers",),
        ".services.health": ("FlextWebHealth",),
        ".services.web": ("FlextWebServices",),
        ".settings": ("FlextWebSettings",),
        ".typings": (
            "FlextWebTypes",
            "t",
        ),
        ".utilities": (
            "FlextWebUtilities",
            "u",
        ),
        "flext_core._root_typing_parts": (
            "d",
            "e",
            "h",
            "r",
            "x",
        ),
    },
)

__all__: list[str] = ["FLEXT_WEB_LAZY_IMPORTS_PART_01"]
