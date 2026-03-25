# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
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
    from flext_core import FlextTypes
    from flext_core import d, e, r, s, x

    from flext_web.__version__ import __all__
    from flext_web.api import FlextWebApi
    from flext_web.app import FlextWebApp
    from flext_web.constants import FlextWebConstants, FlextWebConstants as c
    from flext_web.handlers import FlextWebHandlers, FlextWebHandlers as h
    from flext_web.models import FlextWebModels, FlextWebModels as m
    from flext_web.protocols import FlextWebProtocols, FlextWebProtocols as p
    from flext_web.services import FlextWebServices
    from flext_web.settings import FlextWebSettings
    from flext_web.typings import (
        FlextWebApplicationConfig,
        FlextWebRequestConfig,
        FlextWebResponseConfig,
        FlextWebTypes,
        FlextWebTypes as t,
    )
    from flext_web.utilities import FlextWebUtilities, FlextWebUtilities as u

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextWebApi": ["flext_web.api", "FlextWebApi"],
    "FlextWebApp": ["flext_web.app", "FlextWebApp"],
    "FlextWebApplicationConfig": ["flext_web.typings", "FlextWebApplicationConfig"],
    "FlextWebConstants": ["flext_web.constants", "FlextWebConstants"],
    "FlextWebHandlers": ["flext_web.handlers", "FlextWebHandlers"],
    "FlextWebModels": ["flext_web.models", "FlextWebModels"],
    "FlextWebProtocols": ["flext_web.protocols", "FlextWebProtocols"],
    "FlextWebRequestConfig": ["flext_web.typings", "FlextWebRequestConfig"],
    "FlextWebResponseConfig": ["flext_web.typings", "FlextWebResponseConfig"],
    "FlextWebServices": ["flext_web.services", "FlextWebServices"],
    "FlextWebSettings": ["flext_web.settings", "FlextWebSettings"],
    "FlextWebTypes": ["flext_web.typings", "FlextWebTypes"],
    "FlextWebUtilities": ["flext_web.utilities", "FlextWebUtilities"],
    "__all__": ["flext_web.__version__", "__all__"],
    "c": ["flext_web.constants", "FlextWebConstants"],
    "d": ["flext_core", "d"],
    "e": ["flext_core", "e"],
    "h": ["flext_web.handlers", "FlextWebHandlers"],
    "m": ["flext_web.models", "FlextWebModels"],
    "p": ["flext_web.protocols", "FlextWebProtocols"],
    "r": ["flext_core", "r"],
    "s": ["flext_core", "s"],
    "t": ["flext_web.typings", "FlextWebTypes"],
    "u": ["flext_web.utilities", "FlextWebUtilities"],
    "x": ["flext_core", "x"],
}

__all__ = [
    "FlextWebApi",
    "FlextWebApp",
    "FlextWebApplicationConfig",
    "FlextWebConstants",
    "FlextWebHandlers",
    "FlextWebModels",
    "FlextWebProtocols",
    "FlextWebRequestConfig",
    "FlextWebResponseConfig",
    "FlextWebServices",
    "FlextWebSettings",
    "FlextWebTypes",
    "FlextWebUtilities",
    "__all__",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
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