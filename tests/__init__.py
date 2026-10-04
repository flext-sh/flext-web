# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import api, td, tf, tk, tm

    from flext_web import d, e, h, r, x
    from tests import fixtures, integration, unit
    from tests.base import TestsFlextWebServiceBase, s
    from tests.constants import TestsFlextWebConstants, c
    from tests.models import TestsFlextWebModels, m
    from tests.protocols import TestsFlextWebProtocols, p
    from tests.settings import TestsFlextWebSettings
    from tests.typings import TestsFlextWebTypes, t
    from tests.utilities import TestsFlextWebUtilities, u


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
            "flext_tests": ("api", "td", "tf", "tk", "tm"),
            "flext_web": ("d", "e", "h", "r", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
