# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web. Protocols package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .config import FlextWebProtocolsConfig as FlextWebProtocolsConfig
    from .data import FlextWebProtocolsData as FlextWebProtocolsData
    from .framework import FlextWebProtocolsFramework as FlextWebProtocolsFramework
    from .lifecycle import FlextWebProtocolsLifecycle as FlextWebProtocolsLifecycle
    from .monitoring import FlextWebProtocolsMonitoring as FlextWebProtocolsMonitoring
    from .template import FlextWebProtocolsTemplate as FlextWebProtocolsTemplate

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    ".config": ("FlextWebProtocolsConfig",),
    ".data": ("FlextWebProtocolsData",),
    ".framework": ("FlextWebProtocolsFramework",),
    ".lifecycle": ("FlextWebProtocolsLifecycle",),
    ".monitoring": ("FlextWebProtocolsMonitoring",),
    ".template": ("FlextWebProtocolsTemplate",),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextWebProtocolsConfig",
    "FlextWebProtocolsData",
    "FlextWebProtocolsFramework",
    "FlextWebProtocolsLifecycle",
    "FlextWebProtocolsMonitoring",
    "FlextWebProtocolsTemplate",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
