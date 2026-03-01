"""FLEXT Web Tests - Test infrastructure and utilities.

Provides TestsFlextWeb classes extending FlextTests and FlextWeb for comprehensive testing.
Centralized runtime aliases: c, p, m, r, t, u, s from tests and flext_web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core._utilities.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import r
    from flext_web import (
        FlextWebApi,
        FlextWebApp,
        FlextWebHandlers,
        FlextWebServices,
        FlextWebServices as s,
        FlextWebSettings,
        _ApplicationConfig,
        _WebRequestConfig,
        _WebResponseConfig,
    )

    from tests.constants import TestsFlextWebConstants, TestsFlextWebConstants as c
    from tests.models import TestsFlextWebModels, TestsFlextWebModels as m
    from tests.protocols import TestsFlextWebProtocols, TestsFlextWebProtocols as p
    from tests.typings import TestsFlextWebTypes, TestsFlextWebTypes as t
    from tests.utilities import TestsFlextWebUtilities, TestsFlextWebUtilities as u

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FlextWebApi": ("flext_web", "FlextWebApi"),
    "FlextWebApp": ("flext_web", "FlextWebApp"),
    "FlextWebHandlers": ("flext_web", "FlextWebHandlers"),
    "FlextWebServices": ("flext_web", "FlextWebServices"),
    "FlextWebSettings": ("flext_web", "FlextWebSettings"),
    "TestsFlextWebConstants": ("tests.constants", "TestsFlextWebConstants"),
    "TestsFlextWebModels": ("tests.models", "TestsFlextWebModels"),
    "TestsFlextWebProtocols": ("tests.protocols", "TestsFlextWebProtocols"),
    "TestsFlextWebTypes": ("tests.typings", "TestsFlextWebTypes"),
    "TestsFlextWebUtilities": ("tests.utilities", "TestsFlextWebUtilities"),
    "_ApplicationConfig": ("flext_web", "_ApplicationConfig"),
    "_WebRequestConfig": ("flext_web", "_WebRequestConfig"),
    "_WebResponseConfig": ("flext_web", "_WebResponseConfig"),
    "c": ("tests.constants", "TestsFlextWebConstants"),
    "m": ("tests.models", "TestsFlextWebModels"),
    "p": ("tests.protocols", "TestsFlextWebProtocols"),
    "r": ("flext_core", "r"),
    "s": ("flext_web", "FlextWebServices"),
    "t": ("tests.typings", "TestsFlextWebTypes"),
    "u": ("tests.utilities", "TestsFlextWebUtilities"),
}

__all__ = [
    "FlextWebApi",
    "FlextWebApp",
    "FlextWebHandlers",
    "FlextWebServices",
    "FlextWebSettings",
    "TestsFlextWebConstants",
    "TestsFlextWebModels",
    "TestsFlextWebProtocols",
    "TestsFlextWebTypes",
    "TestsFlextWebUtilities",
    "_ApplicationConfig",
    "_WebRequestConfig",
    "_WebResponseConfig",
    "c",
    "m",
    "p",
    "r",
    "s",
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
