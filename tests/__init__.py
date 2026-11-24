# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import api, td, tf, tk, tm

    from flext_web import (
        FlextWeb,
        FlextWebCli,
        FlextWebConfig,
        FlextWebConstants,
        FlextWebModels,
        FlextWebModelsNamespace,
        FlextWebProtocols,
        FlextWebServiceBase,
        FlextWebSettings,
        FlextWebTypes,
        FlextWebUtilities,
        FlextWebVersion,
        config,
        d,
        e,
        h,
        main,
        r,
        settings,
        web,
        x,
    )
    from flext_web.services import (
        FlextWebApp,
        FlextWebAuth,
        FlextWebEntities,
        FlextWebHandlers,
        FlextWebHealth,
        FlextWebMonitoring,
        FlextWebServices,
    )
    from tests.base import TestsFlextWebServiceBase, s
    from tests.constants import TestsFlextWebConstants, c
    from tests.models import TestsFlextWebModels, m
    from tests.protocols import TestsFlextWebProtocols, p
    from tests.settings import TestsFlextWebSettings
    from tests.typings import TestsFlextWebTypes, t
    from tests.utilities import TestsFlextWebUtilities, u


__all__: tuple[str, ...] = (
    "FlextWeb",
    "FlextWebApp",
    "FlextWebAuth",
    "FlextWebCli",
    "FlextWebConfig",
    "FlextWebConstants",
    "FlextWebEntities",
    "FlextWebHandlers",
    "FlextWebHealth",
    "FlextWebModels",
    "FlextWebModelsNamespace",
    "FlextWebMonitoring",
    "FlextWebProtocols",
    "FlextWebServiceBase",
    "FlextWebServices",
    "FlextWebSettings",
    "FlextWebTypes",
    "FlextWebUtilities",
    "FlextWebVersion",
    "TestsFlextWebConstants",
    "TestsFlextWebModels",
    "TestsFlextWebProtocols",
    "TestsFlextWebServiceBase",
    "TestsFlextWebSettings",
    "TestsFlextWebTypes",
    "TestsFlextWebUtilities",
    "api",
    "c",
    "config",
    "d",
    "e",
    "h",
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
    {
        "FlextWeb": "flext_web",
        "FlextWebApp": "flext_web.services",
        "FlextWebAuth": "flext_web.services",
        "FlextWebCli": "flext_web",
        "FlextWebConfig": "flext_web",
        "FlextWebConstants": "flext_web",
        "FlextWebEntities": "flext_web.services",
        "FlextWebHandlers": "flext_web.services",
        "FlextWebHealth": "flext_web.services",
        "FlextWebModels": "flext_web",
        "FlextWebModelsNamespace": "flext_web",
        "FlextWebMonitoring": "flext_web.services",
        "FlextWebProtocols": "flext_web",
        "FlextWebServiceBase": "flext_web",
        "FlextWebServices": "flext_web.services",
        "FlextWebSettings": "flext_web",
        "FlextWebTypes": "flext_web",
        "FlextWebUtilities": "flext_web",
        "FlextWebVersion": "flext_web",
        "TestsFlextWebConstants": ".constants",
        "TestsFlextWebModels": ".models",
        "TestsFlextWebProtocols": ".protocols",
        "TestsFlextWebServiceBase": ".base",
        "TestsFlextWebSettings": ".settings",
        "TestsFlextWebTypes": ".typings",
        "TestsFlextWebUtilities": ".utilities",
        "api": "flext_tests",
        "c": ".constants",
        "config": "flext_web",
        "d": "flext_web",
        "e": "flext_web",
        "h": "flext_web",
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
    },
    public_exports=__all__,
)
