# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from tests.unit.test___init__ import TestFlextWebInit
    from tests.unit.test___main__ import (
        TestFlextWebCliService,
        TestFlextWebCliService as s,
        TestMainFunction,
    )
    from tests.unit.test_api import TestFlextWebApi
    from tests.unit.test_app import TestFlextWebApp
    from tests.unit.test_config import TestFlextWebSettings
    from tests.unit.test_constants import (
        TestFlextWebConstants,
        TestFlextWebConstants as c,
    )
    from tests.unit.test_fields import TestFlextWebFields
    from tests.unit.test_handlers import TestFlextWebHandlers, TestFlextWebHandlers as h
    from tests.unit.test_protocols import (
        TestFlextWebProtocols,
        TestFlextWebProtocols as p,
    )
    from tests.unit.test_services import TestFlextWebService
    from tests.unit.test_typings import TestFlextWebModels, TestFlextWebModels as m
    from tests.unit.test_utilities import (
        TestFlextWebUtilities,
        TestFlextWebUtilities as u,
    )
    from tests.unit.test_version import TestFlextWebVersion, assert_version_info

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "TestFlextWebApi": ("tests.unit.test_api", "TestFlextWebApi"),
    "TestFlextWebApp": ("tests.unit.test_app", "TestFlextWebApp"),
    "TestFlextWebCliService": ("tests.unit.test___main__", "TestFlextWebCliService"),
    "TestFlextWebConstants": ("tests.unit.test_constants", "TestFlextWebConstants"),
    "TestFlextWebFields": ("tests.unit.test_fields", "TestFlextWebFields"),
    "TestFlextWebHandlers": ("tests.unit.test_handlers", "TestFlextWebHandlers"),
    "TestFlextWebInit": ("tests.unit.test___init__", "TestFlextWebInit"),
    "TestFlextWebModels": ("tests.unit.test_typings", "TestFlextWebModels"),
    "TestFlextWebProtocols": ("tests.unit.test_protocols", "TestFlextWebProtocols"),
    "TestFlextWebService": ("tests.unit.test_services", "TestFlextWebService"),
    "TestFlextWebSettings": ("tests.unit.test_config", "TestFlextWebSettings"),
    "TestFlextWebUtilities": ("tests.unit.test_utilities", "TestFlextWebUtilities"),
    "TestFlextWebVersion": ("tests.unit.test_version", "TestFlextWebVersion"),
    "TestMainFunction": ("tests.unit.test___main__", "TestMainFunction"),
    "assert_version_info": ("tests.unit.test_version", "assert_version_info"),
    "c": ("tests.unit.test_constants", "TestFlextWebConstants"),
    "h": ("tests.unit.test_handlers", "TestFlextWebHandlers"),
    "m": ("tests.unit.test_typings", "TestFlextWebModels"),
    "p": ("tests.unit.test_protocols", "TestFlextWebProtocols"),
    "s": ("tests.unit.test___main__", "TestFlextWebCliService"),
    "u": ("tests.unit.test_utilities", "TestFlextWebUtilities"),
}

__all__ = [
    "TestFlextWebApi",
    "TestFlextWebApp",
    "TestFlextWebCliService",
    "TestFlextWebConstants",
    "TestFlextWebFields",
    "TestFlextWebHandlers",
    "TestFlextWebInit",
    "TestFlextWebModels",
    "TestFlextWebProtocols",
    "TestFlextWebService",
    "TestFlextWebSettings",
    "TestFlextWebUtilities",
    "TestFlextWebVersion",
    "TestMainFunction",
    "assert_version_info",
    "c",
    "h",
    "m",
    "p",
    "s",
    "u",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
