# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import tests.unit.test___init__ as _tests_unit_test___init__

    test___init__ = _tests_unit_test___init__
    import tests.unit.test___main__ as _tests_unit_test___main__
    from tests.unit.test___init__ import TestFlextWebInit

    test___main__ = _tests_unit_test___main__
    import tests.unit.test_api as _tests_unit_test_api
    from tests.unit.test___main__ import TestFlextWebCliService, TestMainFunction

    test_api = _tests_unit_test_api
    import tests.unit.test_app as _tests_unit_test_app
    from tests.unit.test_api import TestFlextWebApi

    test_app = _tests_unit_test_app
    import tests.unit.test_config as _tests_unit_test_config
    from tests.unit.test_app import TestFlextWebApp

    test_config = _tests_unit_test_config
    import tests.unit.test_constants as _tests_unit_test_constants
    from tests.unit.test_config import TestFlextWebSettings

    test_constants = _tests_unit_test_constants
    import tests.unit.test_fields as _tests_unit_test_fields
    from tests.unit.test_constants import TestFlextWebConstants

    test_fields = _tests_unit_test_fields
    import tests.unit.test_handlers as _tests_unit_test_handlers
    from tests.unit.test_fields import TestFlextWebFields

    test_handlers = _tests_unit_test_handlers
    import tests.unit.test_models as _tests_unit_test_models
    from tests.unit.test_handlers import TestFlextWebHandlers

    test_models = _tests_unit_test_models
    import tests.unit.test_protocols as _tests_unit_test_protocols

    test_protocols = _tests_unit_test_protocols
    import tests.unit.test_services as _tests_unit_test_services
    from tests.unit.test_protocols import TestFlextWebProtocols

    test_services = _tests_unit_test_services
    import tests.unit.test_typings as _tests_unit_test_typings
    from tests.unit.test_services import TestFlextWebService

    test_typings = _tests_unit_test_typings
    import tests.unit.test_utilities as _tests_unit_test_utilities
    from tests.unit.test_typings import TestFlextWebModels

    test_utilities = _tests_unit_test_utilities
    import tests.unit.test_version as _tests_unit_test_version
    from tests.unit.test_utilities import TestFlextWebUtilities

    test_version = _tests_unit_test_version
    from flext_core.constants import FlextConstants as c
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.models import FlextModels as m
    from flext_core.protocols import FlextProtocols as p
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_core.typings import FlextTypes as t
    from flext_core.utilities import FlextUtilities as u
    from tests.unit.test_version import TestFlextWebVersion, assert_version_info
_LAZY_IMPORTS = {
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
    "c": ("flext_core.constants", "FlextConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("flext_core.typings", "FlextTypes"),
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
    "u": ("flext_core.utilities", "FlextUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
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
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
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
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
