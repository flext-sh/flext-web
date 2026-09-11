# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web. Protocols package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .config import FlextWebProtocolsConfig
    from .data import FlextWebProtocolsData
    from .framework import FlextWebProtocolsFramework
    from .lifecycle import FlextWebProtocolsLifecycle
    from .monitoring import FlextWebProtocolsMonitoring
    from .template import FlextWebProtocolsTemplate
__all__: tuple[str, ...] = (
    "FlextWebProtocolsConfig",
    "FlextWebProtocolsData",
    "FlextWebProtocolsFramework",
    "FlextWebProtocolsLifecycle",
    "FlextWebProtocolsMonitoring",
    "FlextWebProtocolsTemplate",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".config": ("FlextWebProtocolsConfig",),
            ".data": ("FlextWebProtocolsData",),
            ".framework": ("FlextWebProtocolsFramework",),
            ".lifecycle": ("FlextWebProtocolsLifecycle",),
            ".monitoring": ("FlextWebProtocolsMonitoring",),
            ".template": ("FlextWebProtocolsTemplate",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
