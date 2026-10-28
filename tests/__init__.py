# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import api, install_local_packages, td, tf, tk, tm

    from flext_web import cli, config, d, e, h, main, r, settings, web, x
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
    "cli",
    "config",
    "d",
    "e",
    "h",
    "install_local_packages",
    "m",
    "main",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "u",
    "web",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "TestsFlextWebConstants": ".constants",
        "TestsFlextWebModels": ".models",
        "TestsFlextWebProtocols": ".protocols",
        "TestsFlextWebServiceBase": ".base",
        "TestsFlextWebSettings": ".settings",
        "TestsFlextWebTypes": ".typings",
        "TestsFlextWebUtilities": ".utilities",
        "api": "flext_tests",
        "c": ".constants",
        "cli": "flext_web",
        "config": "flext_web",
        "d": "flext_web",
        "e": "flext_web",
        "h": "flext_web",
        "install_local_packages": "flext_tests",
        "m": ".models",
        "main": "flext_web",
        "p": ".protocols",
        "r": "flext_web",
        "s": ".base",
        "settings": "flext_web",
        "t": ".typings",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "web": "flext_web",
        "x": "flext_web",
    }),
    public_exports=__all__,
)
