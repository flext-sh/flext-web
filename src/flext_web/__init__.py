"""FLEXT Web framework integration.

Provides web framework integration and HTTP handling for FLEXT applications.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_web import (
        FlextWebApi,
        FlextWebApp,
        FlextWebConstants,
        FlextWebConstants as c,
        FlextWebHandlers,
        FlextWebModels,
        FlextWebModels as m,
        FlextWebProtocols,
        FlextWebProtocols as p,
        FlextWebServices,
        FlextWebSettings,
        FlextWebTypes,
        FlextWebTypes as t,
        FlextWebUtilities,
        FlextWebUtilities as u,
        __version__,
        __version_info__,
    )

# Lazy import mapping: export_name -> (module_path, attr_name)
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
    "__version__": ("flext_web.__version__", "__version__"),
    "__version_info__": ("flext_web.__version__", "__version_info__"),
    "c": ("flext_web.constants", "FlextWebConstants"),
    "m": ("flext_web.models", "FlextWebModels"),
    "p": ("flext_web.protocols", "FlextWebProtocols"),
    "t": ("flext_web.typings", "FlextWebTypes"),
    "u": ("flext_web.utilities", "FlextWebUtilities"),
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
    "__version__",
    "__version_info__",
    "c",
    "m",
    "p",
    "t",
    "u",
]


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
