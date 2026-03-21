# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from .test___init__ import TestFlextWebInit
    from .test___main__ import TestFlextWebCliService, TestMainFunction
    from .test_api import TestFlextWebApi
    from .test_app import TestFlextWebApp
    from .test_config import TestFlextWebSettings
    from .test_constants import TestFlextWebConstants
    from .test_fields import TestFlextWebFields
    from .test_handlers import TestFlextWebHandlers
    from .test_protocols import TestFlextWebProtocols
    from .test_services import TestFlextWebService
    from .test_typings import TestFlextWebModels
    from .test_utilities import TestFlextWebUtilities
    from .test_version import TestFlextWebVersion, assert_version_info

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
]


_LAZY_CACHE: dict[str, object] = {}


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


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
