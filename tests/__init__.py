# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _t.TYPE_CHECKING:
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants
    from tests.conftest import (
        docker_manager,
        invalid_app_data,
        production_config,
        pytest_configure,
        pytest_plugins,
        real_app,
        real_config,
        real_service,
        running_service,
        setup_test_environment,
        test_app_data,
        web_settings,
    )

    constants = _tests_constants
    import tests.helpers as _tests_helpers
    from tests.constants import FlextWebTestConstants, FlextWebTestConstants as c

    helpers = _tests_helpers
    import tests.integration as _tests_integration
    from tests.helpers import TestsModels, TestsProtocols, TestsTypings, TestsUtilities

    integration = _tests_integration
    import tests.models as _tests_models
    from tests.integration import (
        ExamplesFullFunctionalityTest,
        TestExamples,
        logger,
        main,
        test_examples,
    )

    models = _tests_models
    import tests.protocols as _tests_protocols
    from tests.models import FlextWebTestModels, FlextWebTestModels as m

    protocols = _tests_protocols
    import tests.typings as _tests_typings
    from tests.protocols import FlextWebTestProtocols, FlextWebTestProtocols as p

    typings = _tests_typings
    import tests.unit as _tests_unit
    from tests.typings import FlextWebTestTypes, FlextWebTestTypes as t

    unit = _tests_unit
    import tests.utilities as _tests_utilities
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

    utilities = _tests_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests.utilities import FlextWebTestUtilities, FlextWebTestUtilities as u
_LAZY_IMPORTS = merge_lazy_imports(
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
        "c": ("tests.constants", "FlextWebTestConstants"),
        "conftest": "tests.conftest",
        "constants": "tests.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "docker_manager": "tests.conftest",
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "helpers": "tests.helpers",
        "integration": "tests.integration",
        "invalid_app_data": "tests.conftest",
        "m": ("tests.models", "FlextWebTestModels"),
        "models": "tests.models",
        "p": ("tests.protocols", "FlextWebTestProtocols"),
        "production_config": "tests.conftest",
        "protocols": "tests.protocols",
        "pytest_configure": "tests.conftest",
        "pytest_plugins": "tests.conftest",
        "r": ("flext_core.result", "FlextResult"),
        "real_app": "tests.conftest",
        "real_config": "tests.conftest",
        "real_service": "tests.conftest",
        "running_service": "tests.conftest",
        "s": ("flext_core.service", "FlextService"),
        "setup_test_environment": "tests.conftest",
        "t": ("tests.typings", "FlextWebTestTypes"),
        "test_app_data": "tests.conftest",
        "typings": "tests.typings",
        "u": ("tests.utilities", "FlextWebTestUtilities"),
        "unit": "tests.unit",
        "utilities": "tests.utilities",
        "web_settings": "tests.conftest",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)
_ = _LAZY_IMPORTS.pop("cleanup_submodule_namespace", None)
_ = _LAZY_IMPORTS.pop("install_lazy_exports", None)
_ = _LAZY_IMPORTS.pop("lazy_getattr", None)
_ = _LAZY_IMPORTS.pop("merge_lazy_imports", None)
_ = _LAZY_IMPORTS.pop("output", None)
_ = _LAZY_IMPORTS.pop("output_reporting", None)

__all__ = [
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
    "TestsModels",
    "TestsProtocols",
    "TestsTypings",
    "TestsUtilities",
    "assert_version_info",
    "c",
    "conftest",
    "constants",
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
    "production_config",
    "protocols",
    "pytest_configure",
    "pytest_plugins",
    "r",
    "real_app",
    "real_config",
    "real_service",
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
    "web_settings",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
