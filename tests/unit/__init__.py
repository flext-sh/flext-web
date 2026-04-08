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

    test___main__ = _tests_unit_test___main__
    import tests.unit.test_api as _tests_unit_test_api

    test_api = _tests_unit_test_api
    import tests.unit.test_app as _tests_unit_test_app

    test_app = _tests_unit_test_app
    import tests.unit.test_config as _tests_unit_test_config

    test_config = _tests_unit_test_config
    import tests.unit.test_constants as _tests_unit_test_constants

    test_constants = _tests_unit_test_constants
    import tests.unit.test_fields as _tests_unit_test_fields

    test_fields = _tests_unit_test_fields
    import tests.unit.test_handlers as _tests_unit_test_handlers

    test_handlers = _tests_unit_test_handlers
    import tests.unit.test_models as _tests_unit_test_models

    test_models = _tests_unit_test_models
    import tests.unit.test_protocols as _tests_unit_test_protocols

    test_protocols = _tests_unit_test_protocols
    import tests.unit.test_services as _tests_unit_test_services

    test_services = _tests_unit_test_services
    import tests.unit.test_typings as _tests_unit_test_typings

    test_typings = _tests_unit_test_typings
    import tests.unit.test_utilities as _tests_unit_test_utilities

    test_utilities = _tests_unit_test_utilities
    import tests.unit.test_version as _tests_unit_test_version

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
_LAZY_IMPORTS = {
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
