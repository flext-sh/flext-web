# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Services package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_web.services.app as _flext_web_services_app

    app = _flext_web_services_app
    import flext_web.services.auth as _flext_web_services_auth
    from flext_web.services.app import FlextWebApp

    auth = _flext_web_services_auth
    import flext_web.services.entities as _flext_web_services_entities
    from flext_web.services.auth import FlextWebAuth

    entities = _flext_web_services_entities
    import flext_web.services.handlers as _flext_web_services_handlers
    from flext_web.services.entities import FlextWebEntities

    handlers = _flext_web_services_handlers
    import flext_web.services.health as _flext_web_services_health
    from flext_web.services.handlers import FlextWebHandlers, FlextWebHandlers as h

    health = _flext_web_services_health
    import flext_web.services.web as _flext_web_services_web
    from flext_web.services.health import FlextWebHealth

    web = _flext_web_services_web
    from flext_core.constants import FlextConstants as c
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.mixins import FlextMixins as x
    from flext_core.models import FlextModels as m
    from flext_core.protocols import FlextProtocols as p
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_core.typings import FlextTypes as t
    from flext_core.utilities import FlextUtilities as u
    from flext_web.services.web import FlextWebServices
_LAZY_IMPORTS = {
    "FlextWebApp": "flext_web.services.app",
    "FlextWebAuth": "flext_web.services.auth",
    "FlextWebEntities": "flext_web.services.entities",
    "FlextWebHandlers": "flext_web.services.handlers",
    "FlextWebHealth": "flext_web.services.health",
    "FlextWebServices": "flext_web.services.web",
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

__all__ = [
    "FlextWebApp",
    "FlextWebAuth",
    "FlextWebEntities",
    "FlextWebHandlers",
    "FlextWebHealth",
    "FlextWebServices",
    "app",
    "auth",
    "c",
    "d",
    "e",
    "entities",
    "h",
    "handlers",
    "health",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "web",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
