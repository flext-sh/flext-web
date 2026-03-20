# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""FLEXT Web framework integration.

Provides web framework integration and HTTP handling for FLEXT applications.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import d, e, r, s, x
    from flext_core.typings import FlextTypes

    from flext_web.__version__ import __all__
    from flext_web.api import FlextWebApi
    from flext_web.app import FlextWebApp
    from flext_web.constants import FlextWebConstants, FlextWebConstants as c
    from flext_web.handlers import FlextWebHandlers, FlextWebHandlers as h
    from flext_web.models import FlextWebModels, FlextWebModels as m
    from flext_web.protocols import (
        FlextWebProtocols,
        FlextWebProtocols as p,
        create_app,
        list_apps,
        start_app,
        stop_app,
    )
    from flext_web.services import FlextWebServices
    from flext_web.settings import FlextWebSettings
    from flext_web.typings import (
        FlextWebTypes,
        FlextWebTypes as t,
        _ApplicationConfig,
        _WebRequestConfig,
        _WebResponseConfig,
    )
    from flext_web.utilities import FlextWebUtilities, FlextWebUtilities as u

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FlextWebApi": ("flext_web.api", "FlextWebApi"),
    "FlextWebApp": ("flext_web.app", "FlextWebApp"),
    "FlextWebConstants": ("flext_web.constants", "FlextWebConstants"),
    "FlextWebHandlers": ("flext_web.handlers", "FlextWebHandlers"),
    "FlextWebModels": ("flext_web.models", "FlextWebModels"),
    "FlextWebProtocols": ("flext_web.protocols", "FlextWebProtocols"),
    "FlextWebServices": ("flext_web.services", "FlextWebServices"),
    "FlextWebSettings": ("flext_web.settings", "FlextWebSettings"),
    "FlextWebTypes": ("flext_web.typings", "FlextWebTypes"),
    "FlextWebUtilities": ("flext_web.utilities", "FlextWebUtilities"),
    "_ApplicationConfig": ("flext_web.typings", "_ApplicationConfig"),
    "_WebRequestConfig": ("flext_web.typings", "_WebRequestConfig"),
    "_WebResponseConfig": ("flext_web.typings", "_WebResponseConfig"),
    "__all__": ("flext_web.__version__", "__all__"),
    "c": ("flext_web.constants", "FlextWebConstants"),
    "create_app": ("flext_web.protocols", "create_app"),
    "d": ("flext_core", "d"),
    "e": ("flext_core", "e"),
    "h": ("flext_web.handlers", "FlextWebHandlers"),
    "list_apps": ("flext_web.protocols", "list_apps"),
    "m": ("flext_web.models", "FlextWebModels"),
    "p": ("flext_web.protocols", "FlextWebProtocols"),
    "r": ("flext_core", "r"),
    "s": ("flext_core", "s"),
    "start_app": ("flext_web.protocols", "start_app"),
    "stop_app": ("flext_web.protocols", "stop_app"),
    "t": ("flext_web.typings", "FlextWebTypes"),
    "u": ("flext_web.utilities", "FlextWebUtilities"),
    "x": ("flext_core", "x"),
}

__all__ = [
    "FlextWebApi",
    "FlextWebApp",
    "FlextWebConstants",
    "FlextWebHandlers",
    "FlextWebModels",
    "FlextWebProtocols",
    "FlextWebServices",
    "FlextWebSettings",
    "FlextWebTypes",
    "FlextWebUtilities",
    "_ApplicationConfig",
    "_WebRequestConfig",
    "_WebResponseConfig",
    "__all__",
    "c",
    "create_app",
    "d",
    "e",
    "h",
    "list_apps",
    "m",
    "p",
    "r",
    "s",
    "start_app",
    "stop_app",
    "t",
    "u",
    "x",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
