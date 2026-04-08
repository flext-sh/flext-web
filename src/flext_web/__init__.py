# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext web package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_web.__version__ import *

if _t.TYPE_CHECKING:
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
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
    from flext_web.api import FlextWeb, web
    from flext_web.base import FlextWebServiceBase, FlextWebServiceBase as s
    from flext_web.constants import FlextWebConstants, FlextWebConstants as c
    from flext_web.models import FlextWebModels, FlextWebModels as m
    from flext_web.protocols import FlextWebProtocols, FlextWebProtocols as p
    from flext_web.services.app import FlextWebApp
    from flext_web.services.auth import FlextWebAuth
    from flext_web.services.entities import FlextWebEntities
    from flext_web.services.handlers import FlextWebHandlers, FlextWebHandlers as h
    from flext_web.services.health import FlextWebHealth
    from flext_web.services.web import FlextWebServices
    from flext_web.settings import FlextWebSettings
    from flext_web.typings import FlextWebTypes, FlextWebTypes as t
    from flext_web.utilities import FlextWebUtilities, FlextWebUtilities as u
_LAZY_IMPORTS = merge_lazy_imports(
    ("flext_web.services",),
    {
        "FlextWeb": ("flext_web.api", "FlextWeb"),
        "FlextWebConstants": ("flext_web.constants", "FlextWebConstants"),
        "FlextWebModels": ("flext_web.models", "FlextWebModels"),
        "FlextWebProtocols": ("flext_web.protocols", "FlextWebProtocols"),
        "FlextWebServiceBase": ("flext_web.base", "FlextWebServiceBase"),
        "FlextWebSettings": ("flext_web.settings", "FlextWebSettings"),
        "FlextWebTypes": ("flext_web.typings", "FlextWebTypes"),
        "FlextWebUtilities": ("flext_web.utilities", "FlextWebUtilities"),
        "FlextWebVersion": ("flext_web.__version__", "FlextWebVersion"),
        "VERSION": ("flext_web.__version__", "VERSION"),
        "VersionMetadata": ("flext_web.__version__", "VersionMetadata"),
        "__author__": ("flext_web.__version__", "__author__"),
        "__author_email__": ("flext_web.__version__", "__author_email__"),
        "__description__": ("flext_web.__version__", "__description__"),
        "__license__": ("flext_web.__version__", "__license__"),
        "__title__": ("flext_web.__version__", "__title__"),
        "__url__": ("flext_web.__version__", "__url__"),
        "__version__": ("flext_web.__version__", "__version__"),
        "__version_info__": ("flext_web.__version__", "__version_info__"),
        "api": "flext_web.api",
        "base": "flext_web.base",
        "c": ("flext_web.constants", "FlextWebConstants"),
        "constants": "flext_web.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "m": ("flext_web.models", "FlextWebModels"),
        "models": "flext_web.models",
        "p": ("flext_web.protocols", "FlextWebProtocols"),
        "protocols": "flext_web.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_web.base", "FlextWebServiceBase"),
        "services": "flext_web.services",
        "settings": "flext_web.settings",
        "t": ("flext_web.typings", "FlextWebTypes"),
        "typings": "flext_web.typings",
        "u": ("flext_web.utilities", "FlextWebUtilities"),
        "utilities": "flext_web.utilities",
        "web": ("flext_web.api", "web"),
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)
_ = _LAZY_IMPORTS.pop("cleanup_submodule_namespace", None)
_ = _LAZY_IMPORTS.pop("install_lazy_exports", None)
_ = _LAZY_IMPORTS.pop("lazy_getattr", None)
_ = _LAZY_IMPORTS.pop("logger", None)
_ = _LAZY_IMPORTS.pop("merge_lazy_imports", None)
_ = _LAZY_IMPORTS.pop("output", None)
_ = _LAZY_IMPORTS.pop("output_reporting", None)

__all__ = [
    "VERSION",
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
    "VersionMetadata",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "api",
    "base",
    "c",
    "constants",
    "d",
    "e",
    "h",
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
