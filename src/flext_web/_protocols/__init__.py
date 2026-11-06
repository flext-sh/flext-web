# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_web._protocols.auth import FlextWebProtocolsAuth
    from flext_web._protocols.base import FlextWebProtocolsBase
    from flext_web._protocols.config import FlextWebProtocolsConfig
    from flext_web._protocols.data import FlextWebProtocolsData
    from flext_web._protocols.entity import FlextWebProtocolsEntity
    from flext_web._protocols.framework import FlextWebProtocolsFramework
    from flext_web._protocols.http import FlextWebProtocolsHttp
    from flext_web._protocols.lifecycle import FlextWebProtocolsLifecycle
    from flext_web._protocols.monitoring import FlextWebProtocolsMonitoring
    from flext_web._protocols.namespace import FlextWebProtocolsNamespace
    from flext_web._protocols.responses import FlextWebProtocolsResponses
    from flext_web._protocols.system import FlextWebProtocolsSystem
    from flext_web._protocols.template import FlextWebProtocolsTemplate
    from flext_web._protocols.web import FlextWebProtocolsWeb


__all__: tuple[str, ...] = (
    "FlextWebProtocolsAuth",
    "FlextWebProtocolsBase",
    "FlextWebProtocolsConfig",
    "FlextWebProtocolsData",
    "FlextWebProtocolsEntity",
    "FlextWebProtocolsFramework",
    "FlextWebProtocolsHttp",
    "FlextWebProtocolsLifecycle",
    "FlextWebProtocolsMonitoring",
    "FlextWebProtocolsNamespace",
    "FlextWebProtocolsResponses",
    "FlextWebProtocolsSystem",
    "FlextWebProtocolsTemplate",
    "FlextWebProtocolsWeb",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextWebProtocolsAuth": ".auth",
        "FlextWebProtocolsBase": ".base",
        "FlextWebProtocolsConfig": ".config",
        "FlextWebProtocolsData": ".data",
        "FlextWebProtocolsEntity": ".entity",
        "FlextWebProtocolsFramework": ".framework",
        "FlextWebProtocolsHttp": ".http",
        "FlextWebProtocolsLifecycle": ".lifecycle",
        "FlextWebProtocolsMonitoring": ".monitoring",
        "FlextWebProtocolsNamespace": ".namespace",
        "FlextWebProtocolsResponses": ".responses",
        "FlextWebProtocolsSystem": ".system",
        "FlextWebProtocolsTemplate": ".template",
        "FlextWebProtocolsWeb": ".web",
    },
    public_exports=__all__,
)
