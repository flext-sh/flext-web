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
    from flext_web import (
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
    from flext_web.test___init__ import TestFlextWebInit
    from flext_web.test___main__ import TestFlextWebCliService
    from flext_web.test_api import TestFlextWebApi
    from flext_web.test_app import TestFlextWebApp
    from flext_web.test_config import TestFlextWebSettings
    from flext_web.test_constants import TestFlextWebConstants
    from flext_web.test_fields import TestFlextWebFields
    from flext_web.test_handlers import TestFlextWebHandlers
    from flext_web.test_protocols import TestFlextWebProtocols
    from flext_web.test_services import TestFlextWebService
    from flext_web.test_typings import TestFlextWebModels
    from flext_web.test_utilities import TestFlextWebUtilities
    from flext_web.test_version import assert_version_info

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "TestFlextWebApi": "flext_web.test_api",
    "TestFlextWebApp": "flext_web.test_app",
    "TestFlextWebCliService": "flext_web.test___main__",
    "TestFlextWebConstants": "flext_web.test_constants",
    "TestFlextWebFields": "flext_web.test_fields",
    "TestFlextWebHandlers": "flext_web.test_handlers",
    "TestFlextWebInit": "flext_web.test___init__",
    "TestFlextWebModels": "flext_web.test_typings",
    "TestFlextWebProtocols": "flext_web.test_protocols",
    "TestFlextWebService": "flext_web.test_services",
    "TestFlextWebSettings": "flext_web.test_config",
    "TestFlextWebUtilities": "flext_web.test_utilities",
    "assert_version_info": "flext_web.test_version",
    "c": ("flext_core.constants", "FlextConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("flext_core.typings", "FlextTypes"),
    "test___init__": "flext_web.test___init__",
    "test___main__": "flext_web.test___main__",
    "test_api": "flext_web.test_api",
    "test_app": "flext_web.test_app",
    "test_config": "flext_web.test_config",
    "test_constants": "flext_web.test_constants",
    "test_fields": "flext_web.test_fields",
    "test_handlers": "flext_web.test_handlers",
    "test_models": "flext_web.test_models",
    "test_protocols": "flext_web.test_protocols",
    "test_services": "flext_web.test_services",
    "test_typings": "flext_web.test_typings",
    "test_utilities": "flext_web.test_utilities",
    "test_version": "flext_web.test_version",
    "u": ("flext_core.utilities", "FlextUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
