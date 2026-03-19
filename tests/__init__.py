# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from flext_web.decorators import d
    from flext_web.exceptions import e
    from flext_web.handlers import h
    from flext_web.mixins import x
    from flext_web.result import r
    from flext_web.service import s

    from . import helpers as helpers, integration as integration, unit as unit
    from .conftest import (
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
    from .constants import TestsFlextWebConstants, c
    from .helpers.models import TestsModels
    from .helpers.protocols import TestsProtocols
    from .helpers.typings import TestsTypings
    from .helpers.utilities import TestsUtilities
    from .integration.test_examples import ExamplesFullFunctionalityTest, logger
    from .models import TestsFlextWebModels, m
    from .port_manager import TestPortManager
    from .protocols import TestsFlextWebProtocols, p
    from .typings import TestsFlextWebTypes, t
    from .unit.test___init__ import TestFlextWebInit
    from .unit.test___main__ import TestFlextWebCliService, TestMainFunction
    from .unit.test_api import TestFlextWebApi
    from .unit.test_app import TestFlextWebApp
    from .unit.test_config import TestFlextWebSettings
    from .unit.test_constants import TestFlextWebConstants
    from .unit.test_fields import TestFlextWebFields
    from .unit.test_handlers import TestFlextWebHandlers
    from .unit.test_protocols import TestFlextWebProtocols
    from .unit.test_services import TestFlextWebService
    from .unit.test_typings import TestFlextWebModels
    from .unit.test_utilities import TestFlextWebUtilities
    from .unit.test_version import TestFlextWebVersion, assert_version_info
    from .utilities import TestsFlextWebUtilities, u

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "ExamplesFullFunctionalityTest": (
        "tests.integration.test_examples",
        "ExamplesFullFunctionalityTest",
    ),
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
    "TestPortManager": ("tests.port_manager", "TestPortManager"),
    "TestsFlextWebConstants": ("tests.constants", "TestsFlextWebConstants"),
    "TestsFlextWebModels": ("tests.models", "TestsFlextWebModels"),
    "TestsFlextWebProtocols": ("tests.protocols", "TestsFlextWebProtocols"),
    "TestsFlextWebTypes": ("tests.typings", "TestsFlextWebTypes"),
    "TestsFlextWebUtilities": ("tests.utilities", "TestsFlextWebUtilities"),
    "TestsModels": ("tests.helpers.models", "TestsModels"),
    "TestsProtocols": ("tests.helpers.protocols", "TestsProtocols"),
    "TestsTypings": ("tests.helpers.typings", "TestsTypings"),
    "TestsUtilities": ("tests.helpers.utilities", "TestsUtilities"),
    "assert_failure": ("tests.conftest", "assert_failure"),
    "assert_result": ("tests.conftest", "assert_result"),
    "assert_success": ("tests.conftest", "assert_success"),
    "assert_version_info": ("tests.unit.test_version", "assert_version_info"),
    "c": ("tests.constants", "c"),
    "create_comprehensive_test_suite": (
        "tests.conftest",
        "create_comprehensive_test_suite",
    ),
    "create_entry": ("tests.conftest", "create_entry"),
    "create_test_app": ("tests.conftest", "create_test_app"),
    "create_test_data": ("tests.conftest", "create_test_data"),
    "create_test_result": ("tests.conftest", "create_test_result"),
    "d": ("flext_web.decorators", "d"),
    "docker_manager": ("tests.conftest", "docker_manager"),
    "e": ("flext_web.exceptions", "e"),
    "h": ("flext_web.handlers", "h"),
    "helpers": ("tests.helpers", ""),
    "integration": ("tests.integration", ""),
    "invalid_app_data": ("tests.conftest", "invalid_app_data"),
    "logger": ("tests.integration.test_examples", "logger"),
    "m": ("tests.models", "m"),
    "p": ("tests.protocols", "p"),
    "production_config": ("tests.conftest", "production_config"),
    "pytest_configure": ("tests.conftest", "pytest_configure"),
    "r": ("flext_web.result", "r"),
    "real_app": ("tests.conftest", "real_app"),
    "real_config": ("tests.conftest", "real_config"),
    "real_service": ("tests.conftest", "real_service"),
    "run_parameterized_test": ("tests.conftest", "run_parameterized_test"),
    "running_service": ("tests.conftest", "running_service"),
    "s": ("flext_web.service", "s"),
    "setup_test_environment": ("tests.conftest", "setup_test_environment"),
    "t": ("tests.typings", "t"),
    "test_app_data": ("tests.conftest", "test_app_data"),
    "u": ("tests.utilities", "u"),
    "unit": ("tests.unit", ""),
    "x": ("flext_web.mixins", "x"),
}

__all__ = [
    "ExamplesFullFunctionalityTest",
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
    "TestsFlextWebConstants",
    "TestsFlextWebModels",
    "TestsFlextWebProtocols",
    "TestsFlextWebTypes",
    "TestsFlextWebUtilities",
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


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
