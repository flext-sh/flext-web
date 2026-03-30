# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import *

    from tests import (
        conftest,
        constants,
        models,
        port_manager,
        protocols,
        typings,
        utilities,
    )
    from tests.conftest import *
    from tests.constants import *
    from tests.helpers import *
    from tests.integration import *
    from tests.models import *
    from tests.port_manager import *
    from tests.protocols import *
    from tests.typings import *
    from tests.unit import *
    from tests.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "ExamplesFullFunctionalityTest": "tests.integration.test_examples",
    "FlextWebTestConstants": "tests.constants",
    "FlextWebTestModels": "tests.models",
    "FlextWebTestProtocols": "tests.protocols",
    "FlextWebTestTypes": "tests.typings",
    "FlextWebTestUtilities": "tests.utilities",
    "TestExamples": "tests.integration.test_examples",
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
    "TestPortManager": "tests.port_manager",
    "TestsModels": "tests.helpers.models",
    "TestsProtocols": "tests.helpers.protocols",
    "TestsTypings": "tests.helpers.typings",
    "TestsUtilities": "tests.helpers.utilities",
    "assert_failure": "tests.conftest",
    "assert_result": "tests.conftest",
    "assert_success": "tests.conftest",
    "assert_version_info": "tests.unit.test_version",
    "c": ["tests.constants", "FlextWebTestConstants"],
    "conftest": "tests.conftest",
    "constants": "tests.constants",
    "create_comprehensive_test_suite": "tests.conftest",
    "create_entry": "tests.conftest",
    "create_test_app": "tests.conftest",
    "create_test_data": "tests.conftest",
    "create_test_result": "tests.conftest",
    "d": "flext_tests",
    "docker_manager": "tests.conftest",
    "e": "flext_tests",
    "h": "flext_tests",
    "helpers": "tests.helpers",
    "integration": "tests.integration",
    "invalid_app_data": "tests.conftest",
    "logger": "tests.integration.test_examples",
    "m": ["tests.models", "FlextWebTestModels"],
    "main": "tests.integration.test_examples",
    "models": "tests.models",
    "p": ["tests.protocols", "FlextWebTestProtocols"],
    "port_manager": "tests.port_manager",
    "production_config": "tests.conftest",
    "protocols": "tests.protocols",
    "pytest_configure": "tests.conftest",
    "r": "flext_tests",
    "real_app": "tests.conftest",
    "real_config": "tests.conftest",
    "real_service": "tests.conftest",
    "run_parameterized_test": "tests.conftest",
    "running_service": "tests.conftest",
    "s": "flext_tests",
    "setup_test_environment": "tests.conftest",
    "t": ["tests.typings", "FlextWebTestTypes"],
    "test___init__": "tests.unit.test___init__",
    "test___main__": "tests.unit.test___main__",
    "test_api": "tests.unit.test_api",
    "test_app": "tests.unit.test_app",
    "test_app_data": "tests.conftest",
    "test_config": "tests.unit.test_config",
    "test_constants": "tests.unit.test_constants",
    "test_examples": "tests.integration.test_examples",
    "test_fields": "tests.unit.test_fields",
    "test_handlers": "tests.unit.test_handlers",
    "test_models": "tests.unit.test_models",
    "test_protocols": "tests.unit.test_protocols",
    "test_services": "tests.unit.test_services",
    "test_typings": "tests.unit.test_typings",
    "test_utilities": "tests.unit.test_utilities",
    "test_version": "tests.unit.test_version",
    "typings": "tests.typings",
    "u": ["tests.utilities", "FlextWebTestUtilities"],
    "unit": "tests.unit",
    "utilities": "tests.utilities",
    "x": "flext_tests",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
