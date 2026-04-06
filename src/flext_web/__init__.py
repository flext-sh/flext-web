# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext web package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_web.__version__ import *

if _t.TYPE_CHECKING:
    import flext_web.api as _flext_web_api

    api = _flext_web_api
    import flext_web.base as _flext_web_base
    from flext_web.api import FlextWeb, web

    base = _flext_web_base
    import flext_web.constants as _flext_web_constants
    from flext_web.base import FlextWebServiceBase

    constants = _flext_web_constants
    import flext_web.models as _flext_web_models
    from flext_web.constants import FlextWebConstants, FlextWebConstants as c

    models = _flext_web_models
    import flext_web.protocols as _flext_web_protocols
    from flext_web.models import FlextWebModels, FlextWebModels as m

    protocols = _flext_web_protocols
    import flext_web.services as _flext_web_services
    from flext_web.protocols import FlextWebProtocols, FlextWebProtocols as p

    services = _flext_web_services
    import flext_web.settings as _flext_web_settings
    from flext_web.services import (
        FlextWebApp,
        FlextWebAuth,
        FlextWebEntities,
        FlextWebHandlers,
        FlextWebHandlers as h,
        FlextWebHealth,
        FlextWebServices,
        app,
        auth,
        entities,
        handlers,
        health,
    )

    settings = _flext_web_settings
    import flext_web.typings as _flext_web_typings
    from flext_web.settings import FlextWebSettings

    typings = _flext_web_typings
    import flext_web.utilities as _flext_web_utilities
    from flext_web.typings import FlextWebTypes, FlextWebTypes as t

    utilities = _flext_web_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
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
        "s": ("flext_core.service", "FlextService"),
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
