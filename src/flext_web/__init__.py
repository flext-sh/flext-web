"""FLEXT Web framework integration.

Provides web framework integration and HTTP handling for FLEXT applications.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core._utilities.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
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
    from flext_web.api import FlextWebApi
    from flext_web.app import FlextWebApp
    from flext_web.constants import FlextWebConstants, FlextWebConstants as c
    from flext_web.handlers import FlextWebHandlers
    from flext_web.models import FlextWebModels, FlextWebModels as m
    from flext_web.protocols import FlextWebProtocols, FlextWebProtocols as p
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
    "FlextWebVersion": ("flext_web.__version__", "FlextWebVersion"),
    "VERSION": ("flext_web.__version__", "VERSION"),
    "_ApplicationConfig": ("flext_web.typings", "_ApplicationConfig"),
    "_VersionMetadata": ("flext_web.__version__", "_VersionMetadata"),
    "_WebRequestConfig": ("flext_web.typings", "_WebRequestConfig"),
    "_WebResponseConfig": ("flext_web.typings", "_WebResponseConfig"),
    "__author__": ("flext_web.__version__", "__author__"),
    "__author_email__": ("flext_web.__version__", "__author_email__"),
    "__description__": ("flext_web.__version__", "__description__"),
    "__license__": ("flext_web.__version__", "__license__"),
    "__title__": ("flext_web.__version__", "__title__"),
    "__url__": ("flext_web.__version__", "__url__"),
    "__version__": ("flext_web.__version__", "__version__"),
    "__version_info__": ("flext_web.__version__", "__version_info__"),
    "c": ("flext_web.constants", "FlextWebConstants"),
    "m": ("flext_web.models", "FlextWebModels"),
    "p": ("flext_web.protocols", "FlextWebProtocols"),
    "t": ("flext_web.typings", "FlextWebTypes"),
    "u": ("flext_web.utilities", "FlextWebUtilities"),
}

__all__ = [
    "VERSION",
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
    "FlextWebVersion",
    "_ApplicationConfig",
    "_VersionMetadata",
    "_WebRequestConfig",
    "_WebResponseConfig",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
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
