# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""FLEXT Web Tests - Test infrastructure and utilities.

Provides TestsFlextWeb classes extending FlextTests and FlextWeb for comprehensive testing.
Centralized runtime aliases: c, p, m, r, t, u, s from tests and flext_web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

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
    from tests.constants import TestsFlextWebConstants, c
    from tests.helpers.models import TestsModels
    from tests.helpers.protocols import TestsProtocols
    from tests.helpers.typings import TestsTypings
    from tests.helpers.utilities import TestsUtilities
    from tests.integration.test_examples import ExamplesFullFunctionalityTest, logger
    from tests.models import TestsFlextWebModels, m
    from tests.port_manager import TestPortManager
    from tests.protocols import TestsFlextWebProtocols, p
    from tests.typings import TestsFlextWebTypes, t
    from tests.unit.test___init__ import TestFlextWebInit
    from tests.unit.test___main__ import (
        TestFlextWebCliService,
        TestFlextWebCliService as s,
        TestMainFunction,
    )
    from tests.unit.test_api import TestFlextWebApi
    from tests.unit.test_app import TestFlextWebApp
    from tests.unit.test_config import TestFlextWebSettings
    from tests.unit.test_constants import TestFlextWebConstants
    from tests.unit.test_fields import TestFlextWebFields
    from tests.unit.test_handlers import TestFlextWebHandlers, TestFlextWebHandlers as h
    from tests.unit.test_protocols import TestFlextWebProtocols
    from tests.unit.test_services import TestFlextWebService
    from tests.unit.test_typings import TestFlextWebModels
    from tests.unit.test_utilities import TestFlextWebUtilities
    from tests.unit.test_version import TestFlextWebVersion, assert_version_info
    from tests.utilities import TestsFlextWebUtilities, u

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
    "docker_manager": ("tests.conftest", "docker_manager"),
    "h": ("tests.unit.test_handlers", "TestFlextWebHandlers"),
    "invalid_app_data": ("tests.conftest", "invalid_app_data"),
    "logger": ("tests.integration.test_examples", "logger"),
    "m": ("tests.models", "m"),
    "p": ("tests.protocols", "p"),
    "production_config": ("tests.conftest", "production_config"),
    "pytest_configure": ("tests.conftest", "pytest_configure"),
    "real_app": ("tests.conftest", "real_app"),
    "real_config": ("tests.conftest", "real_config"),
    "real_service": ("tests.conftest", "real_service"),
    "run_parameterized_test": ("tests.conftest", "run_parameterized_test"),
    "running_service": ("tests.conftest", "running_service"),
    "s": ("tests.unit.test___main__", "TestFlextWebCliService"),
    "setup_test_environment": ("tests.conftest", "setup_test_environment"),
    "t": ("tests.typings", "t"),
    "test_app_data": ("tests.conftest", "test_app_data"),
    "u": ("tests.utilities", "u"),
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
    "docker_manager",
    "h",
    "invalid_app_data",
    "logger",
    "m",
    "p",
    "production_config",
    "pytest_configure",
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
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
