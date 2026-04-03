# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext web package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_web.__version__ import *

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_web import (
        api,
        base,
        constants,
        models,
        protocols,
        services,
        settings,
        typings,
        utilities,
    )
    from flext_web.__version__ import (
        VERSION,
        FlextWebVersion,
        VersionMetadata,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
    from flext_web.api import FlextWeb, web
    from flext_web.base import FlextWebServiceBase
    from flext_web.constants import FlextWebConstants, FlextWebConstants as c
    from flext_web.models import FlextWebModels, FlextWebModels as m
    from flext_web.protocols import FlextWebProtocols, FlextWebProtocols as p
    from flext_web.services import (
        FlextWebApp,
        FlextWebAuth,
        FlextWebEntities,
        FlextWebHandlers,
        FlextWebHealth,
        FlextWebServices,
        app,
        auth,
        entities,
        handlers,
        health,
    )
    from flext_web.settings import FlextWebSettings
    from flext_web.typings import FlextWebTypes, FlextWebTypes as t
    from flext_web.utilities import FlextWebUtilities, FlextWebUtilities as u

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
    ("flext_web.services",),
    {
        "FlextWeb": "flext_web.api",
        "FlextWebConstants": "flext_web.constants",
        "FlextWebModels": "flext_web.models",
        "FlextWebProtocols": "flext_web.protocols",
        "FlextWebServiceBase": "flext_web.base",
        "FlextWebSettings": "flext_web.settings",
        "FlextWebTypes": "flext_web.typings",
        "FlextWebUtilities": "flext_web.utilities",
        "FlextWebVersion": "flext_web.__version__",
        "VERSION": "flext_web.__version__",
        "VersionMetadata": "flext_web.__version__",
        "__author__": "flext_web.__version__",
        "__author_email__": "flext_web.__version__",
        "__description__": "flext_web.__version__",
        "__license__": "flext_web.__version__",
        "__title__": "flext_web.__version__",
        "__url__": "flext_web.__version__",
        "__version__": "flext_web.__version__",
        "__version_info__": "flext_web.__version__",
        "api": "flext_web.api",
        "base": "flext_web.base",
        "c": ("flext_web.constants", "FlextWebConstants"),
        "constants": "flext_web.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": ("flext_web.models", "FlextWebModels"),
        "models": "flext_web.models",
        "p": ("flext_web.protocols", "FlextWebProtocols"),
        "protocols": "flext_web.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "services": "flext_web.services",
        "settings": "flext_web.settings",
        "t": ("flext_web.typings", "FlextWebTypes"),
        "typings": "flext_web.typings",
        "u": ("flext_web.utilities", "FlextWebUtilities"),
        "utilities": "flext_web.utilities",
        "web": "flext_web.api",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
