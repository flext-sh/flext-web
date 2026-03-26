# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_tests import d, e, h, r, s, x

    from tests import helpers, integration, unit
    from tests.conftest import (
        assert_failure,
        assert_result,
        assert_success,
        create_comprehensive_test_suite,
        create_entry,
        create_test_app,
        create_test_data,
        create_test_result,
        docker_manager,
        invalid_app_data,
        production_config,
        pytest_configure,
        real_app,
        real_config,
        real_service,
        run_parameterized_test,
        running_service,
        setup_test_environment,
        test_app_data,
    )
    from tests.constants import FlextWebTestConstants, FlextWebTestConstants as c
    from tests.helpers.models import TestsModels
    from tests.helpers.protocols import TestsProtocols
    from tests.helpers.typings import TestsTypings
    from tests.helpers.utilities import TestsUtilities
    from tests.integration.test_examples import (
        ExamplesFullFunctionalityTest,
        logger,
        main,
    )
    from tests.models import FlextWebTestModels, FlextWebTestModels as m
    from tests.port_manager import TestPortManager
    from tests.protocols import FlextWebTestProtocols, FlextWebTestProtocols as p
    from tests.typings import FlextWebTestTypes, FlextWebTestTypes as t
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
    from tests.utilities import FlextWebTestUtilities, FlextWebTestUtilities as u

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "ExamplesFullFunctionalityTest": ["tests.integration.test_examples", "ExamplesFullFunctionalityTest"],
    "FlextWebTestConstants": ["tests.constants", "FlextWebTestConstants"],
    "FlextWebTestModels": ["tests.models", "FlextWebTestModels"],
    "FlextWebTestProtocols": ["tests.protocols", "FlextWebTestProtocols"],
    "FlextWebTestTypes": ["tests.typings", "FlextWebTestTypes"],
    "FlextWebTestUtilities": ["tests.utilities", "FlextWebTestUtilities"],
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
    "TestPortManager": ["tests.port_manager", "TestPortManager"],
    "TestsModels": ["tests.helpers.models", "TestsModels"],
    "TestsProtocols": ["tests.helpers.protocols", "TestsProtocols"],
    "TestsTypings": ["tests.helpers.typings", "TestsTypings"],
    "TestsUtilities": ["tests.helpers.utilities", "TestsUtilities"],
    "assert_failure": ["tests.conftest", "assert_failure"],
    "assert_result": ["tests.conftest", "assert_result"],
    "assert_success": ["tests.conftest", "assert_success"],
    "assert_version_info": ["tests.unit.test_version", "assert_version_info"],
    "c": ["tests.constants", "FlextWebTestConstants"],
    "create_comprehensive_test_suite": ["tests.conftest", "create_comprehensive_test_suite"],
    "create_entry": ["tests.conftest", "create_entry"],
    "create_test_app": ["tests.conftest", "create_test_app"],
    "create_test_data": ["tests.conftest", "create_test_data"],
    "create_test_result": ["tests.conftest", "create_test_result"],
    "d": ["flext_tests", "d"],
    "docker_manager": ["tests.conftest", "docker_manager"],
    "e": ["flext_tests", "e"],
    "h": ["flext_tests", "h"],
    "helpers": ["tests.helpers", ""],
    "integration": ["tests.integration", ""],
    "invalid_app_data": ["tests.conftest", "invalid_app_data"],
    "logger": ["tests.integration.test_examples", "logger"],
    "m": ["tests.models", "FlextWebTestModels"],
    "main": ["tests.integration.test_examples", "main"],
    "p": ["tests.protocols", "FlextWebTestProtocols"],
    "production_config": ["tests.conftest", "production_config"],
    "pytest_configure": ["tests.conftest", "pytest_configure"],
    "r": ["flext_tests", "r"],
    "real_app": ["tests.conftest", "real_app"],
    "real_config": ["tests.conftest", "real_config"],
    "real_service": ["tests.conftest", "real_service"],
    "run_parameterized_test": ["tests.conftest", "run_parameterized_test"],
    "running_service": ["tests.conftest", "running_service"],
    "s": ["flext_tests", "s"],
    "setup_test_environment": ["tests.conftest", "setup_test_environment"],
    "t": ["tests.typings", "FlextWebTestTypes"],
    "test_app_data": ["tests.conftest", "test_app_data"],
    "u": ["tests.utilities", "FlextWebTestUtilities"],
    "unit": ["tests.unit", ""],
    "x": ["flext_tests", "x"],
}

__all__ = [
    "ExamplesFullFunctionalityTest",
    "FlextWebTestConstants",
    "FlextWebTestModels",
    "FlextWebTestProtocols",
    "FlextWebTestTypes",
    "FlextWebTestUtilities",
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
    "TestPortManager",
    "TestsModels",
    "TestsProtocols",
    "TestsTypings",
    "TestsUtilities",
    "assert_failure",
    "assert_result",
    "assert_success",
    "assert_version_info",
    "c",
    "create_comprehensive_test_suite",
    "create_entry",
    "create_test_app",
    "create_test_data",
    "create_test_result",
    "d",
    "docker_manager",
    "e",
    "h",
    "helpers",
    "integration",
    "invalid_app_data",
    "logger",
    "m",
    "main",
    "p",
    "production_config",
    "pytest_configure",
    "r",
    "real_app",
    "real_config",
    "real_service",
    "run_parameterized_test",
    "running_service",
    "s",
    "setup_test_environment",
    "t",
    "test_app_data",
    "u",
    "unit",
    "x",
]


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


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


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
