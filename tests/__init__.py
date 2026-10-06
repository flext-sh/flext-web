# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import api, td, tf, tk, tm
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
        "d": "flext_web",
        "e": "flext_web",
        "fixtures": ".fixtures",
        "h": "flext_web",
        "integration": ".integration",
        "m": ".models",
        "p": ".protocols",
        "r": "flext_web",
        "s": ".base",
        "t": ".typings",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "unit": ".unit",
        "x": "flext_web",
    }),
    public_exports=__all__,
)
