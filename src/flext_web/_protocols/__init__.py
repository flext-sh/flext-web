# AUTO-GENERATED FILE — Regenerate with: make gen
"""Protocols package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_web._protocols.config import (
        FlextWebProtocolsConfig as FlextWebProtocolsConfig,
    )
    from flext_web._protocols.data import FlextWebProtocolsData as FlextWebProtocolsData
    from flext_web._protocols.framework import (
        FlextWebProtocolsFramework as FlextWebProtocolsFramework,
    )
    from flext_web._protocols.lifecycle import (
        FlextWebProtocolsLifecycle as FlextWebProtocolsLifecycle,
    )
    from flext_web._protocols.monitoring import (
        FlextWebProtocolsMonitoring as FlextWebProtocolsMonitoring,
    )
    from flext_web._protocols.template import (
        FlextWebProtocolsTemplate as FlextWebProtocolsTemplate,
    )
_LAZY_IMPORTS = build_lazy_import_map({
    ".config": ("FlextWebProtocolsConfig",),
    ".data": ("FlextWebProtocolsData",),
    ".framework": ("FlextWebProtocolsFramework",),
    ".lifecycle": ("FlextWebProtocolsLifecycle",),
    ".monitoring": ("FlextWebProtocolsMonitoring",),
    ".template": ("FlextWebProtocolsTemplate",),
})


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
