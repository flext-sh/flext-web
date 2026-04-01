# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from tests.unit.test___init__ import TestFlextWebInit
    from tests.unit.test___main__ import TestFlextWebCliService, TestMainFunction
    from tests.unit.test_api import TestFlextWebApi
    from tests.unit.test_app import TestFlextWebApp
    from tests.unit.test_config import TestFlextWebSettings
    from tests.unit.test_constants import TestFlextWebConstants
    from tests.unit.test_fields import TestFlextWebFields
    from tests.unit.test_handlers import TestFlextWebHandlers
    from tests.unit.test_protocols import TestFlextWebProtocols
    from tests.unit.test_services import TestFlextWebService
    from tests.unit.test_typings import TestFlextWebModels
    from tests.unit.test_utilities import TestFlextWebUtilities
    from tests.unit.test_version import TestFlextWebVersion, assert_version_info

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "TestFlextWebApi": "tests.unit.test_api",
    "TestFlextWebApp": "tests.unit.test_app",
    "TestFlextWebCliService": "tests.unit.test___main__",
    "TestFlextWebConstants": "tests.unit.test_constants",
    "TestFlextWebFields": "tests.unit.test_fields",
    "TestFlextWebHandlers": "tests.unit.test_handlers",
    "TestFlextWebInit": "tests.unit.test___init__",
    "TestFlextWebModels": "tests.unit.test_typings",
    "TestFlextWebProtocols": "tests.unit.test_protocols",
    "TestFlextWebService": "tests.unit.test_services",
    "TestFlextWebSettings": "tests.unit.test_config",
    "TestFlextWebUtilities": "tests.unit.test_utilities",
    "TestFlextWebVersion": "tests.unit.test_version",
    "TestMainFunction": "tests.unit.test___main__",
    "assert_version_info": "tests.unit.test_version",
    "test___init__": "tests.unit.test___init__",
    "test___main__": "tests.unit.test___main__",
    "test_api": "tests.unit.test_api",
    "test_app": "tests.unit.test_app",
    "test_config": "tests.unit.test_config",
    "test_constants": "tests.unit.test_constants",
    "test_fields": "tests.unit.test_fields",
    "test_handlers": "tests.unit.test_handlers",
    "test_models": "tests.unit.test_models",
    "test_protocols": "tests.unit.test_protocols",
    "test_services": "tests.unit.test_services",
    "test_typings": "tests.unit.test_typings",
    "test_utilities": "tests.unit.test_utilities",
    "test_version": "tests.unit.test_version",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
