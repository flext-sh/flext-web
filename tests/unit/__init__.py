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
    from tests.unit.test___init__ import *
    from tests.unit.test___main__ import *
    from tests.unit.test_api import *
    from tests.unit.test_app import *
    from tests.unit.test_config import *
    from tests.unit.test_constants import *
    from tests.unit.test_fields import *
    from tests.unit.test_handlers import *
    from tests.unit.test_protocols import *
    from tests.unit.test_services import *
    from tests.unit.test_typings import *
    from tests.unit.test_utilities import *
    from tests.unit.test_version import *

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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
