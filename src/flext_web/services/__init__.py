# AUTO-GENERATED FILE — Regenerate with: make gen
"""Services package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_web.services.app import FlextWebApp as FlextWebApp
    from flext_web.services.auth import FlextWebAuth as FlextWebAuth
    from flext_web.services.entities import FlextWebEntities as FlextWebEntities
    from flext_web.services.handlers import FlextWebHandlers as FlextWebHandlers
    from flext_web.services.health import FlextWebHealth as FlextWebHealth
    from flext_web.services.web import FlextWebServices as FlextWebServices
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
