# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Canonical services package for flext-web."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_web.services import app, auth, entities, handlers, health, web
    from flext_web.services.app import FlextWebApp
    from flext_web.services.auth import FlextWebAuth
    from flext_web.services.entities import FlextWebEntities
    from flext_web.services.handlers import FlextWebHandlers
    from flext_web.services.health import FlextWebHealth
    from flext_web.services.web import FlextWebServices

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextWebApp": "flext_web.services.app",
    "FlextWebAuth": "flext_web.services.auth",
    "FlextWebEntities": "flext_web.services.entities",
    "FlextWebHandlers": "flext_web.services.handlers",
    "FlextWebHealth": "flext_web.services.health",
    "FlextWebServices": "flext_web.services.web",
    "app": "flext_web.services.app",
    "auth": "flext_web.services.auth",
    "entities": "flext_web.services.entities",
    "handlers": "flext_web.services.handlers",
    "health": "flext_web.services.health",
    "web": "flext_web.services.web",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
