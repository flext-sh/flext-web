# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import d, e, h, r, s, x

    from tests import (
        conftest as conftest,
        constants as constants,
        helpers as helpers,
        integration as integration,
        models as models,
        port_manager as port_manager,
        protocols as protocols,
        typings as typings,
        unit as unit,
        utilities as utilities,
    )
    from tests.conftest import (
        assert_failure as assert_failure,
        assert_result as assert_result,
        assert_success as assert_success,
        create_comprehensive_test_suite as create_comprehensive_test_suite,
        create_entry as create_entry,
        create_test_app as create_test_app,
        create_test_data as create_test_data,
        create_test_result as create_test_result,
        docker_manager as docker_manager,
        invalid_app_data as invalid_app_data,
        production_config as production_config,
        pytest_configure as pytest_configure,
        real_app as real_app,
        real_config as real_config,
        real_service as real_service,
        run_parameterized_test as run_parameterized_test,
        running_service as running_service,
        setup_test_environment as setup_test_environment,
        test_app_data as test_app_data,
    )
    from tests.constants import (
        FlextWebTestConstants as FlextWebTestConstants,
        FlextWebTestConstants as c,
    )
    from tests.helpers.models import TestsModels as TestsModels
    from tests.helpers.protocols import TestsProtocols as TestsProtocols
    from tests.helpers.typings import TestsTypings as TestsTypings
    from tests.helpers.utilities import TestsUtilities as TestsUtilities
    from tests.integration import test_examples as test_examples
    from tests.integration.test_examples import (
        ExamplesFullFunctionalityTest as ExamplesFullFunctionalityTest,
        TestExamples as TestExamples,
        logger as logger,
        main as main,
    )
    from tests.models import (
        FlextWebTestModels as FlextWebTestModels,
        FlextWebTestModels as m,
    )
    from tests.port_manager import TestPortManager as TestPortManager
    from tests.protocols import (
        FlextWebTestProtocols as FlextWebTestProtocols,
        FlextWebTestProtocols as p,
    )
    from tests.typings import (
        FlextWebTestTypes as FlextWebTestTypes,
        FlextWebTestTypes as t,
    )
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
    from tests.utilities import (
        FlextWebTestUtilities as FlextWebTestUtilities,
        FlextWebTestUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "ExamplesFullFunctionalityTest": ["tests.integration.test_examples", "ExamplesFullFunctionalityTest"],
    "FlextWebTestConstants": ["tests.constants", "FlextWebTestConstants"],
    "FlextWebTestModels": ["tests.models", "FlextWebTestModels"],
    "FlextWebTestProtocols": ["tests.protocols", "FlextWebTestProtocols"],
    "FlextWebTestTypes": ["tests.typings", "FlextWebTestTypes"],
    "FlextWebTestUtilities": ["tests.utilities", "FlextWebTestUtilities"],
    "TestExamples": ["tests.integration.test_examples", "TestExamples"],
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
    "conftest": ["tests.conftest", ""],
    "constants": ["tests.constants", ""],
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
    "models": ["tests.models", ""],
    "p": ["tests.protocols", "FlextWebTestProtocols"],
    "port_manager": ["tests.port_manager", ""],
    "production_config": ["tests.conftest", "production_config"],
    "protocols": ["tests.protocols", ""],
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
    "test___init__": ["tests.unit.test___init__", ""],
    "test___main__": ["tests.unit.test___main__", ""],
    "test_api": ["tests.unit.test_api", ""],
    "test_app": ["tests.unit.test_app", ""],
    "test_app_data": ["tests.conftest", "test_app_data"],
    "test_config": ["tests.unit.test_config", ""],
    "test_constants": ["tests.unit.test_constants", ""],
    "test_examples": ["tests.integration.test_examples", ""],
    "test_fields": ["tests.unit.test_fields", ""],
    "test_handlers": ["tests.unit.test_handlers", ""],
    "test_models": ["tests.unit.test_models", ""],
    "test_protocols": ["tests.unit.test_protocols", ""],
    "test_services": ["tests.unit.test_services", ""],
    "test_typings": ["tests.unit.test_typings", ""],
    "test_utilities": ["tests.unit.test_utilities", ""],
    "test_version": ["tests.unit.test_version", ""],
    "typings": ["tests.typings", ""],
    "u": ["tests.utilities", "FlextWebTestUtilities"],
    "unit": ["tests.unit", ""],
    "utilities": ["tests.utilities", ""],
    "x": ["flext_tests", "x"],
}

_EXPORTS: Sequence[str] = [
    "ExamplesFullFunctionalityTest",
    "FlextWebTestConstants",
    "FlextWebTestModels",
    "FlextWebTestProtocols",
    "FlextWebTestTypes",
    "FlextWebTestUtilities",
    "TestExamples",
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
    "conftest",
    "constants",
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
    "models",
    "p",
    "port_manager",
    "production_config",
    "protocols",
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
    "test___init__",
    "test___main__",
    "test_api",
    "test_app",
    "test_app_data",
    "test_config",
    "test_constants",
    "test_examples",
    "test_fields",
    "test_handlers",
    "test_models",
    "test_protocols",
    "test_services",
    "test_typings",
    "test_utilities",
    "test_version",
    "typings",
    "u",
    "unit",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
