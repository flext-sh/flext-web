# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_web._protocols.base import FlextWebProtocolsBase
    from flext_web._protocols.config import FlextWebProtocolsConfig
    from flext_web._protocols.data import FlextWebProtocolsData
    from flext_web._protocols.framework import FlextWebProtocolsFramework
    from flext_web._protocols.lifecycle import FlextWebProtocolsLifecycle
    from flext_web._protocols.monitoring import FlextWebProtocolsMonitoring
    from flext_web._protocols.template import FlextWebProtocolsTemplate
    from flext_web._protocols.web import FlextWebProtocolsWeb


__all__: tuple[str, ...] = (
    "FlextWebProtocolsBase",
    "FlextWebProtocolsConfig",
    "FlextWebProtocolsData",
    "FlextWebProtocolsFramework",
    "FlextWebProtocolsLifecycle",
    "FlextWebProtocolsMonitoring",
    "FlextWebProtocolsTemplate",
    "FlextWebProtocolsWeb",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextWebProtocolsBase": ".base",
        "FlextWebProtocolsConfig": ".config",
        "FlextWebProtocolsData": ".data",
        "FlextWebProtocolsFramework": ".framework",
        "FlextWebProtocolsLifecycle": ".lifecycle",
        "FlextWebProtocolsMonitoring": ".monitoring",
        "FlextWebProtocolsTemplate": ".template",
        "FlextWebProtocolsWeb": ".web",
    }),
    public_exports=__all__,
)
