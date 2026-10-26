# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from examples.api_usage import FlextWebExamplesApiUsage
    from examples.basic_service import FlextWebExamplesBasicService
    from examples.constants import FlextWebExamplesConstants
    from examples.models import FlextWebExamplesModels
    from examples.protocols import FlextWebExamplesProtocols
    from examples.typings import FlextWebExamplesTypes
    from examples.utilities import ExamplesFlextWebUtilities
    from flext_web import (
        c,
        cli,
        config,
        d,
        e,
        h,
        m,
        main,
        p,
        r,
        s,
        settings,
        t,
        u,
        web,
        x,
    )


__all__: tuple[str, ...] = (
    "ExamplesFlextWebUtilities",
    "FlextWebExamplesApiUsage",
    "FlextWebExamplesBasicService",
    "FlextWebExamplesConstants",
    "FlextWebExamplesModels",
    "FlextWebExamplesProtocols",
    "FlextWebExamplesTypes",
    "c",
    "cli",
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
    "u",
    "web",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "ExamplesFlextWebUtilities": ".utilities",
        "FlextWebExamplesApiUsage": ".api_usage",
        "FlextWebExamplesBasicService": ".basic_service",
        "FlextWebExamplesConstants": ".constants",
        "FlextWebExamplesModels": ".models",
        "FlextWebExamplesProtocols": ".protocols",
        "FlextWebExamplesTypes": ".typings",
        "c": "flext_web",
        "cli": "flext_web",
        "config": "flext_web",
        "d": "flext_web",
        "e": "flext_web",
        "h": "flext_web",
        "m": "flext_web",
        "main": "flext_web",
        "p": "flext_web",
        "r": "flext_web",
        "s": "flext_web",
        "settings": "flext_web",
        "t": "flext_web",
        "u": "flext_web",
        "web": "flext_web",
        "x": "flext_web",
    }),
    public_exports=__all__,
)
