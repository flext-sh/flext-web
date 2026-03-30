# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Web framework integration.

Provides web framework integration and HTTP handling for FLEXT applications.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

from flext_web.__version__ import (
    VERSION as VERSION,
    FlextWebVersion as FlextWebVersion,
    __author__ as __author__,
    __author_email__ as __author_email__,
    __description__ as __description__,
    __license__ as __license__,
    __title__ as __title__,
    __url__ as __url__,
    __version__ as __version__,
    __version_info__ as __version_info__,
    _VersionMetadata as _VersionMetadata,
)

if TYPE_CHECKING:
    from flext_core import d, e, h, r, s, x

    from flext_web import (
        api as api,
        base as base,
        constants as constants,
        models as models,
        protocols as protocols,
        services as services,
        settings as settings,
        typings as typings,
        utilities as utilities,
    )
    from flext_web.api import FlextWeb as FlextWeb, web as web
    from flext_web.base import FlextWebServiceBase as FlextWebServiceBase
    from flext_web.constants import (
        FlextWebConstants as FlextWebConstants,
        FlextWebConstants as c,
    )
    from flext_web.models import FlextWebModels as FlextWebModels, FlextWebModels as m
    from flext_web.protocols import (
        FlextWebProtocols as FlextWebProtocols,
        FlextWebProtocols as p,
    )
    from flext_web.services import (
        app as app,
        auth as auth,
        entities as entities,
        handlers as handlers,
        health as health,
    )
    from flext_web.services.app import FlextWebApp as FlextWebApp
    from flext_web.services.auth import FlextWebAuth as FlextWebAuth
    from flext_web.services.entities import FlextWebEntities as FlextWebEntities
    from flext_web.services.handlers import FlextWebHandlers as FlextWebHandlers
    from flext_web.services.health import FlextWebHealth as FlextWebHealth
    from flext_web.services.web import FlextWebServices as FlextWebServices
    from flext_web.settings import FlextWebSettings as FlextWebSettings
    from flext_web.typings import FlextWebTypes as FlextWebTypes, FlextWebTypes as t
    from flext_web.utilities import (
        FlextWebUtilities as FlextWebUtilities,
        FlextWebUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextWeb": ["flext_web.api", "FlextWeb"],
    "FlextWebApp": ["flext_web.services.app", "FlextWebApp"],
    "FlextWebAuth": ["flext_web.services.auth", "FlextWebAuth"],
    "FlextWebConstants": ["flext_web.constants", "FlextWebConstants"],
    "FlextWebEntities": ["flext_web.services.entities", "FlextWebEntities"],
    "FlextWebHandlers": ["flext_web.services.handlers", "FlextWebHandlers"],
    "FlextWebHealth": ["flext_web.services.health", "FlextWebHealth"],
    "FlextWebModels": ["flext_web.models", "FlextWebModels"],
    "FlextWebProtocols": ["flext_web.protocols", "FlextWebProtocols"],
    "FlextWebServiceBase": ["flext_web.base", "FlextWebServiceBase"],
    "FlextWebServices": ["flext_web.services.web", "FlextWebServices"],
    "FlextWebSettings": ["flext_web.settings", "FlextWebSettings"],
    "FlextWebTypes": ["flext_web.typings", "FlextWebTypes"],
    "FlextWebUtilities": ["flext_web.utilities", "FlextWebUtilities"],
    "api": ["flext_web.api", ""],
    "app": ["flext_web.services.app", ""],
    "auth": ["flext_web.services.auth", ""],
    "base": ["flext_web.base", ""],
    "c": ["flext_web.constants", "FlextWebConstants"],
    "constants": ["flext_web.constants", ""],
    "d": ["flext_core", "d"],
    "e": ["flext_core", "e"],
    "entities": ["flext_web.services.entities", ""],
    "h": ["flext_core", "h"],
    "handlers": ["flext_web.services.handlers", ""],
    "health": ["flext_web.services.health", ""],
    "m": ["flext_web.models", "FlextWebModels"],
    "models": ["flext_web.models", ""],
    "p": ["flext_web.protocols", "FlextWebProtocols"],
    "protocols": ["flext_web.protocols", ""],
    "r": ["flext_core", "r"],
    "s": ["flext_core", "s"],
    "services": ["flext_web.services", ""],
    "settings": ["flext_web.settings", ""],
    "t": ["flext_web.typings", "FlextWebTypes"],
    "typings": ["flext_web.typings", ""],
    "u": ["flext_web.utilities", "FlextWebUtilities"],
    "utilities": ["flext_web.utilities", ""],
    "web": ["flext_web.api", "web"],
    "x": ["flext_core", "x"],
}

_EXPORTS: Sequence[str] = [
    "FlextWeb",
    "FlextWebApp",
    "FlextWebAuth",
    "FlextWebConstants",
    "FlextWebEntities",
    "FlextWebHandlers",
    "FlextWebHealth",
    "FlextWebModels",
    "FlextWebProtocols",
    "FlextWebServiceBase",
    "FlextWebServices",
    "FlextWebSettings",
    "FlextWebTypes",
    "FlextWebUtilities",
    "FlextWebVersion",
    "VERSION",
    "_VersionMetadata",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "api",
    "app",
    "auth",
    "base",
    "c",
    "constants",
    "d",
    "e",
    "entities",
    "h",
    "handlers",
    "health",
    "m",
    "models",
    "p",
    "protocols",
    "r",
    "s",
    "services",
    "settings",
    "t",
    "typings",
    "u",
    "utilities",
    "web",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
