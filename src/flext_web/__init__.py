# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Web framework integration.

Provides web framework integration and HTTP handling for FLEXT applications.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes, d, e, h, r, s, x

    from flext_web import services
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
    from flext_web.api import FlextWeb, web
    from flext_web.base import FlextWebServiceBase
    from flext_web.constants import FlextWebConstants, FlextWebConstants as c
    from flext_web.models import FlextWebModels, FlextWebModels as m
    from flext_web.protocols import FlextWebProtocols, FlextWebProtocols as p
    from flext_web.services.app import FlextWebApp
    from flext_web.services.auth import FlextWebAuth
    from flext_web.services.entities import FlextWebEntities
    from flext_web.services.handlers import FlextWebHandlers
    from flext_web.services.health import FlextWebHealth
    from flext_web.services.web import FlextWebServices
    from flext_web.settings import FlextWebSettings
    from flext_web.typings import FlextWebTypes, FlextWebTypes as t
    from flext_web.utilities import FlextWebUtilities, FlextWebUtilities as u

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
    "FlextWebVersion": ["flext_web.__version__", "FlextWebVersion"],
    "VERSION": ["flext_web.__version__", "VERSION"],
    "_VersionMetadata": ["flext_web.__version__", "_VersionMetadata"],
    "__author__": ["flext_web.__version__", "__author__"],
    "__author_email__": ["flext_web.__version__", "__author_email__"],
    "__description__": ["flext_web.__version__", "__description__"],
    "__license__": ["flext_web.__version__", "__license__"],
    "__title__": ["flext_web.__version__", "__title__"],
    "__url__": ["flext_web.__version__", "__url__"],
    "__version__": ["flext_web.__version__", "__version__"],
    "__version_info__": ["flext_web.__version__", "__version_info__"],
    "c": ["flext_web.constants", "FlextWebConstants"],
    "d": ["flext_core", "d"],
    "e": ["flext_core", "e"],
    "h": ["flext_core", "h"],
    "m": ["flext_web.models", "FlextWebModels"],
    "p": ["flext_web.protocols", "FlextWebProtocols"],
    "r": ["flext_core", "r"],
    "s": ["flext_core", "s"],
    "services": ["flext_web.services", ""],
    "t": ["flext_web.typings", "FlextWebTypes"],
    "u": ["flext_web.utilities", "FlextWebUtilities"],
    "web": ["flext_web.api", "web"],
    "x": ["flext_core", "x"],
}

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
    "_VersionMetadata",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "services",
    "t",
    "u",
    "web",
    "x",
]


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
