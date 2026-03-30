# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from tests.unit import (
        test___init__ as test___init__,
        test___main__ as test___main__,
        test_api as test_api,
        test_app as test_app,
        test_config as test_config,
        test_constants as test_constants,
        test_fields as test_fields,
        test_handlers as test_handlers,
        test_models as test_models,
        test_protocols as test_protocols,
        test_services as test_services,
        test_typings as test_typings,
        test_utilities as test_utilities,
        test_version as test_version,
    )
    from tests.unit.test___init__ import TestFlextWebInit as TestFlextWebInit
    from tests.unit.test___main__ import (
        TestFlextWebCliService as TestFlextWebCliService,
        TestMainFunction as TestMainFunction,
    )
    from tests.unit.test_api import TestFlextWebApi as TestFlextWebApi
    from tests.unit.test_app import TestFlextWebApp as TestFlextWebApp
    from tests.unit.test_config import TestFlextWebSettings as TestFlextWebSettings
    from tests.unit.test_constants import TestFlextWebConstants as TestFlextWebConstants
    from tests.unit.test_fields import TestFlextWebFields as TestFlextWebFields
    from tests.unit.test_handlers import TestFlextWebHandlers as TestFlextWebHandlers
    from tests.unit.test_protocols import TestFlextWebProtocols as TestFlextWebProtocols
    from tests.unit.test_services import TestFlextWebService as TestFlextWebService
    from tests.unit.test_typings import TestFlextWebModels as TestFlextWebModels
    from tests.unit.test_utilities import TestFlextWebUtilities as TestFlextWebUtilities
    from tests.unit.test_version import (
        TestFlextWebVersion as TestFlextWebVersion,
        assert_version_info as assert_version_info,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "TestFlextWebApi": ["tests.unit.test_api", "TestFlextWebApi"],
    "TestFlextWebApp": ["tests.unit.test_app", "TestFlextWebApp"],
    "TestFlextWebCliService": ["tests.unit.test___main__", "TestFlextWebCliService"],
    "TestFlextWebConstants": ["tests.unit.test_constants", "TestFlextWebConstants"],
    "TestFlextWebFields": ["tests.unit.test_fields", "TestFlextWebFields"],
    "TestFlextWebHandlers": ["tests.unit.test_handlers", "TestFlextWebHandlers"],
    "TestFlextWebInit": ["tests.unit.test___init__", "TestFlextWebInit"],
    "TestFlextWebModels": ["tests.unit.test_typings", "TestFlextWebModels"],
    "TestFlextWebProtocols": ["tests.unit.test_protocols", "TestFlextWebProtocols"],
    "TestFlextWebService": ["tests.unit.test_services", "TestFlextWebService"],
    "TestFlextWebSettings": ["tests.unit.test_config", "TestFlextWebSettings"],
    "TestFlextWebUtilities": ["tests.unit.test_utilities", "TestFlextWebUtilities"],
    "TestFlextWebVersion": ["tests.unit.test_version", "TestFlextWebVersion"],
    "TestMainFunction": ["tests.unit.test___main__", "TestMainFunction"],
    "assert_version_info": ["tests.unit.test_version", "assert_version_info"],
    "test___init__": ["tests.unit.test___init__", ""],
    "test___main__": ["tests.unit.test___main__", ""],
    "test_api": ["tests.unit.test_api", ""],
    "test_app": ["tests.unit.test_app", ""],
    "test_config": ["tests.unit.test_config", ""],
    "test_constants": ["tests.unit.test_constants", ""],
    "test_fields": ["tests.unit.test_fields", ""],
    "test_handlers": ["tests.unit.test_handlers", ""],
    "test_models": ["tests.unit.test_models", ""],
    "test_protocols": ["tests.unit.test_protocols", ""],
    "test_services": ["tests.unit.test_services", ""],
    "test_typings": ["tests.unit.test_typings", ""],
    "test_utilities": ["tests.unit.test_utilities", ""],
    "test_version": ["tests.unit.test_version", ""],
}

_EXPORTS: Sequence[str] = [
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
    "test___init__",
    "test___main__",
    "test_api",
    "test_app",
    "test_config",
    "test_constants",
    "test_fields",
    "test_handlers",
    "test_models",
    "test_protocols",
    "test_services",
    "test_typings",
    "test_utilities",
    "test_version",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
