# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_tests import d, e, h, r, s, x

    from tests import (
        conftest,
        constants,
        helpers,
        integration,
        models,
        port_manager,
        protocols,
        typings,
        unit,
        utilities,
    )
    from tests.conftest import (
        docker_manager,
        invalid_app_data,
        production_config,
        pytest_configure,
        real_app,
        real_config,
        real_service,
        running_service,
        setup_test_environment,
        test_app_data,
    )
    from tests.constants import FlextWebTestConstants, FlextWebTestConstants as c
    from tests.helpers import TestsModels, TestsProtocols, TestsTypings, TestsUtilities
    from tests.integration import (
        ExamplesFullFunctionalityTest,
        TestExamples,
        logger,
        main,
        test_examples,
    )
    from tests.models import FlextWebTestModels, FlextWebTestModels as m
    from tests.port_manager import TestPortManager
    from tests.protocols import FlextWebTestProtocols, FlextWebTestProtocols as p
    from tests.typings import FlextWebTestTypes, FlextWebTestTypes as t
    from tests.unit import (
        TestFlextWebApi,
        TestFlextWebApp,
        TestFlextWebCliService,
        TestFlextWebConstants,
        TestFlextWebFields,
        TestFlextWebHandlers,
        TestFlextWebInit,
        TestFlextWebModels,
        TestFlextWebProtocols,
        TestFlextWebService,
        TestFlextWebSettings,
        TestFlextWebUtilities,
        TestFlextWebVersion,
        TestMainFunction,
        assert_version_info,
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
    from tests.utilities import FlextWebTestUtilities, FlextWebTestUtilities as u

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = merge_lazy_imports(
    (
        "tests.helpers",
        "tests.integration",
        "tests.unit",
    ),
    {
        "FlextWebTestConstants": "tests.constants",
        "FlextWebTestModels": "tests.models",
        "FlextWebTestProtocols": "tests.protocols",
        "FlextWebTestTypes": "tests.typings",
        "FlextWebTestUtilities": "tests.utilities",
        "TestPortManager": "tests.port_manager",
        "c": ("tests.constants", "FlextWebTestConstants"),
        "conftest": "tests.conftest",
        "constants": "tests.constants",
        "d": "flext_tests",
        "docker_manager": "tests.conftest",
        "e": "flext_tests",
        "h": "flext_tests",
        "helpers": "tests.helpers",
        "integration": "tests.integration",
        "invalid_app_data": "tests.conftest",
        "m": ("tests.models", "FlextWebTestModels"),
        "models": "tests.models",
        "p": ("tests.protocols", "FlextWebTestProtocols"),
        "port_manager": "tests.port_manager",
        "production_config": "tests.conftest",
        "protocols": "tests.protocols",
        "pytest_configure": "tests.conftest",
        "r": "flext_tests",
        "real_app": "tests.conftest",
        "real_config": "tests.conftest",
        "real_service": "tests.conftest",
        "running_service": "tests.conftest",
        "s": "flext_tests",
        "setup_test_environment": "tests.conftest",
        "t": ("tests.typings", "FlextWebTestTypes"),
        "test_app_data": "tests.conftest",
        "typings": "tests.typings",
        "u": ("tests.utilities", "FlextWebTestUtilities"),
        "unit": "tests.unit",
        "utilities": "tests.utilities",
        "x": "flext_tests",
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
