# AUTO-GENERATED FILE — Regenerate with: make gen
"""Services package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_web.services.app import FlextWebApp
    from flext_web.services.auth import FlextWebAuth
    from flext_web.services.entities import FlextWebEntities
    from flext_web.services.handlers import FlextWebHandlers
    from flext_web.services.health import FlextWebHealth
    from flext_web.services.web import FlextWebServices
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".app": ("FlextWebApp",),
        ".auth": ("FlextWebAuth",),
        ".entities": ("FlextWebEntities",),
        ".handlers": ("FlextWebHandlers",),
        ".health": ("FlextWebHealth",),
        ".web": ("FlextWebServices",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
