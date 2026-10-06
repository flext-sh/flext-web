# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web.services package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_web.services.app import FlextWebApp
    from flext_web.services.auth import FlextWebAuth
    from flext_web.services.entities import FlextWebEntities
    from flext_web.services.handlers import FlextWebHandlers
    from flext_web.services.health import FlextWebHealth
    from flext_web.services.web import FlextWebMonitoring, FlextWebServices


__all__: tuple[str, ...] = (
    "FlextWebApp",
    "FlextWebAuth",
    "FlextWebEntities",
    "FlextWebHandlers",
    "FlextWebHealth",
    "FlextWebMonitoring",
    "FlextWebServices",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextWebApp": ".app",
        "FlextWebAuth": ".auth",
        "FlextWebEntities": ".entities",
        "FlextWebHandlers": ".handlers",
        "FlextWebHealth": ".health",
        "FlextWebMonitoring": ".monitoring",
        "FlextWebServices": ".web",
    }),
    public_exports=__all__,
)
