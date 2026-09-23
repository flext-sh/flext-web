# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_cli import cli
    from flext_tests import (
        api,
        core,
        d,
        e,
        h,
        install_local_packages,
        lazy_attribute,
        load_infra_report,
        r,
        services,
        td,
        tf,
        tk,
        tm,
        tv,
        x,
    )

    from flext_web import config, main, s, settings, web

    from . import fixtures, integration, unit
    from .base import TestsFlextWebServiceBase
    from .constants import TestsFlextWebConstants, c
    from .models import TestsFlextWebModels, m
    from .protocols import TestsFlextWebProtocols, p
    from .settings import TestsFlextWebSettings
    from .typings import TestsFlextWebTypes, t
    from .utilities import TestsFlextWebUtilities, u


__all__: tuple[str, ...] = (
    "TestsFlextWebConstants",
    "TestsFlextWebModels",
    "TestsFlextWebProtocols",
    "TestsFlextWebServiceBase",
    "TestsFlextWebSettings",
    "TestsFlextWebTypes",
    "TestsFlextWebUtilities",
    "api",
    "c",
    "cli",
    "config",
    "core",
    "d",
    "e",
    "fixtures",
    "h",
    "install_local_packages",
    "integration",
    "lazy_attribute",
    "load_infra_report",
    "m",
    "main",
    "p",
    "r",
    "s",
    "services",
    "settings",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "unit",
    "web",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("TestsFlextWebServiceBase",),
            ".constants": ("TestsFlextWebConstants", "c"),
            ".fixtures": ("fixtures",),
            ".integration": ("integration",),
            ".models": ("TestsFlextWebModels", "m"),
            ".protocols": ("TestsFlextWebProtocols", "p"),
            ".settings": ("TestsFlextWebSettings",),
            ".typings": ("TestsFlextWebTypes", "t"),
            ".unit": ("unit",),
            ".utilities": ("TestsFlextWebUtilities", "u"),
            "flext_cli": ("cli",),
            "flext_tests": (
                "api",
                "core",
                "d",
                "e",
                "h",
                "install_local_packages",
                "lazy_attribute",
                "load_infra_report",
                "r",
                "services",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "x",
            ),
            "flext_web": ("config", "main", "s", "settings", "web"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
