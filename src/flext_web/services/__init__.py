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
    "app": "flext_web.services.app",
    "auth": "flext_web.services.auth",
    "c": ("flext_core.constants", "FlextConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "entities": "flext_web.services.entities",
    "h": ("flext_web.services.handlers", "FlextWebHandlers"),
    "handlers": "flext_web.services.handlers",
    "health": "flext_web.services.health",
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("flext_core.typings", "FlextTypes"),
    "u": ("flext_core.utilities", "FlextUtilities"),
    "web": "flext_web.services.web",
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
