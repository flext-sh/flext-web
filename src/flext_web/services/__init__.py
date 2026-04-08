# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Services package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "FlextWebApp": ("flext_web.services.app", "FlextWebApp"),
    "FlextWebAuth": ("flext_web.services.auth", "FlextWebAuth"),
    "FlextWebEntities": ("flext_web.services.entities", "FlextWebEntities"),
    "FlextWebHandlers": ("flext_web.services.handlers", "FlextWebHandlers"),
    "FlextWebHealth": ("flext_web.services.health", "FlextWebHealth"),
    "FlextWebServices": ("flext_web.services.web", "FlextWebServices"),
    "h": ("flext_web.services.handlers", "FlextWebHandlers"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
