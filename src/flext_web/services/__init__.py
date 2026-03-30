# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Canonical services package for flext-web."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_web.services import (
        app as app,
        auth as auth,
        entities as entities,
        handlers as handlers,
        health as health,
        web as web,
    )
    from flext_web.services.app import FlextWebApp as FlextWebApp
    from flext_web.services.auth import FlextWebAuth as FlextWebAuth
    from flext_web.services.entities import FlextWebEntities as FlextWebEntities
    from flext_web.services.handlers import FlextWebHandlers as FlextWebHandlers
    from flext_web.services.health import FlextWebHealth as FlextWebHealth
    from flext_web.services.web import FlextWebServices as FlextWebServices

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextWebApp": ["flext_web.services.app", "FlextWebApp"],
    "FlextWebAuth": ["flext_web.services.auth", "FlextWebAuth"],
    "FlextWebEntities": ["flext_web.services.entities", "FlextWebEntities"],
    "FlextWebHandlers": ["flext_web.services.handlers", "FlextWebHandlers"],
    "FlextWebHealth": ["flext_web.services.health", "FlextWebHealth"],
    "FlextWebServices": ["flext_web.services.web", "FlextWebServices"],
    "app": ["flext_web.services.app", ""],
    "auth": ["flext_web.services.auth", ""],
    "entities": ["flext_web.services.entities", ""],
    "handlers": ["flext_web.services.handlers", ""],
    "health": ["flext_web.services.health", ""],
    "web": ["flext_web.services.web", ""],
}

_EXPORTS: Sequence[str] = [
    "FlextWebApp",
    "FlextWebAuth",
    "FlextWebEntities",
    "FlextWebHandlers",
    "FlextWebHealth",
    "FlextWebServices",
    "app",
    "auth",
    "entities",
    "handlers",
    "health",
    "web",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
