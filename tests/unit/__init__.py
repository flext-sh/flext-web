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
    from tests.unit import (
        test___init__,
        test___main__,
        test_api,
        test_app,
        test_config,
        test_constants,
        test_fields,
        test_handlers,
        test_models,
        test_protocols,
        test_services,
        test_typings,
        test_utilities,
        test_version,
    )
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

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
