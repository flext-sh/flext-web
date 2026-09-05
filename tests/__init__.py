# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from typing import Final

    from flext_tests import FlextTestsConstants, d, e, h, r, td, tf, tk, tm, tv, x
    from flext_web import FlextWebConstants

    from . import fixtures as fixtures, integration as integration, unit as unit
    from .base import TestsFlextWebServiceBase, TestsFlextWebServiceBase as s
    from .constants import TestsFlextWebConstants, TestsFlextWebConstants as c
    from .models import TestsFlextWebModels, TestsFlextWebModels as m
    from .protocols import TestsFlextWebProtocols, TestsFlextWebProtocols as p
    from .settings import TestsFlextWebSettings
    from .typings import TestsFlextWebTypes, TestsFlextWebTypes as t
    from .utilities import TestsFlextWebUtilities, TestsFlextWebUtilities as u
__all__: tuple[str, ...] = (
    "Final",
    "FlextTestsConstants",
    "FlextWebConstants",
    "TestsFlextWebConstants",
    "TestsFlextWebModels",
    "TestsFlextWebProtocols",
    "TestsFlextWebServiceBase",
    "TestsFlextWebSettings",
    "TestsFlextWebTypes",
    "TestsFlextWebUtilities",
    "c",
    "d",
    "e",
    "fixtures",
    "h",
    "integration",
    "m",
    "p",
    "r",
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "unit",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("TestsFlextWebServiceBase", "s"),
            ".constants": ("TestsFlextWebConstants", "c"),
            ".fixtures": ("fixtures",),
            ".integration": ("integration",),
            ".models": ("TestsFlextWebModels", "m"),
            ".protocols": ("TestsFlextWebProtocols", "p"),
            ".settings": ("TestsFlextWebSettings",),
            ".typings": ("TestsFlextWebTypes", "t"),
            ".unit": ("unit",),
            ".utilities": ("TestsFlextWebUtilities", "u"),
            "flext_tests": (
                "FlextTestsConstants",
                "d",
                "e",
                "h",
                "r",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "x",
            ),
            "flext_web": ("FlextWebConstants",),
            "typing": ("Final",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
