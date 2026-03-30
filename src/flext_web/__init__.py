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
    VERSION,
    FlextWebVersion,
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
    _VersionMetadata,
)

if TYPE_CHECKING:
    from flext_core import *

    from flext_web import (
        api,
        base,
        constants,
        models,
        protocols,
        settings,
        typings,
        utilities,
    )
    from flext_web.api import *
    from flext_web.base import *
    from flext_web.constants import *
    from flext_web.models import *
    from flext_web.protocols import *
    from flext_web.services import *
    from flext_web.settings import *
    from flext_web.typings import *
    from flext_web.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextWeb": "flext_web.api",
    "FlextWebApp": "flext_web.services.app",
    "FlextWebAuth": "flext_web.services.auth",
    "FlextWebConstants": "flext_web.constants",
    "FlextWebEntities": "flext_web.services.entities",
    "FlextWebHandlers": "flext_web.services.handlers",
    "FlextWebHealth": "flext_web.services.health",
    "FlextWebModels": "flext_web.models",
    "FlextWebProtocols": "flext_web.protocols",
    "FlextWebServiceBase": "flext_web.base",
    "FlextWebServices": "flext_web.services.web",
    "FlextWebSettings": "flext_web.settings",
    "FlextWebTypes": "flext_web.typings",
    "FlextWebUtilities": "flext_web.utilities",
    "api": "flext_web.api",
    "app": "flext_web.services.app",
    "auth": "flext_web.services.auth",
    "base": "flext_web.base",
    "c": ["flext_web.constants", "FlextWebConstants"],
    "constants": "flext_web.constants",
    "d": "flext_core",
    "e": "flext_core",
    "entities": "flext_web.services.entities",
    "h": "flext_core",
    "handlers": "flext_web.services.handlers",
    "health": "flext_web.services.health",
    "m": ["flext_web.models", "FlextWebModels"],
    "models": "flext_web.models",
    "p": ["flext_web.protocols", "FlextWebProtocols"],
    "protocols": "flext_web.protocols",
    "r": "flext_core",
    "s": "flext_core",
    "services": "flext_web.services",
    "settings": "flext_web.settings",
    "t": ["flext_web.typings", "FlextWebTypes"],
    "typings": "flext_web.typings",
    "u": ["flext_web.utilities", "FlextWebUtilities"],
    "utilities": "flext_web.utilities",
    "web": "flext_web.api",
    "x": "flext_core",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
