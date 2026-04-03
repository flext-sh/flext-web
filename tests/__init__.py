# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.decorators import FlextDecorators as d
from flext_core.exceptions import FlextExceptions as e
from flext_core.handlers import FlextHandlers as h
from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_core.mixins import FlextMixins as x
from flext_core.result import FlextResult as r
from flext_core.service import FlextService as s
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
from tests.helpers.models import TestsModels
from tests.helpers.protocols import TestsProtocols
from tests.helpers.typings import TestsTypings
from tests.helpers.utilities import TestsUtilities
from tests.integration.test_examples import (
    ExamplesFullFunctionalityTest,
    TestExamples,
    logger,
    main,
)
from tests.models import FlextWebTestModels, FlextWebTestModels as m
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

if _t.TYPE_CHECKING:
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants

    constants = _tests_constants
    import tests.helpers as _tests_helpers

    helpers = _tests_helpers
    import tests.integration as _tests_integration

    integration = _tests_integration
    import tests.integration.test_examples as _tests_integration_test_examples

    test_examples = _tests_integration_test_examples
    import tests.models as _tests_models

    models = _tests_models
    import tests.protocols as _tests_protocols

    protocols = _tests_protocols
    import tests.typings as _tests_typings

    typings = _tests_typings
    import tests.unit as _tests_unit

    unit = _tests_unit
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
    import tests.utilities as _tests_utilities

    utilities = _tests_utilities

    _ = (
        ExamplesFullFunctionalityTest,
        FlextWebTestConstants,
        FlextWebTestModels,
        FlextWebTestProtocols,
        FlextWebTestTypes,
        FlextWebTestUtilities,
        TestExamples,
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
        TestsModels,
        TestsProtocols,
        TestsTypings,
        TestsUtilities,
        assert_version_info,
        c,
        conftest,
        constants,
        d,
        docker_manager,
        e,
        h,
        helpers,
        integration,
        invalid_app_data,
        logger,
        m,
        main,
        models,
        p,
        production_config,
        protocols,
        pytest_configure,
        r,
        real_app,
        real_config,
        real_service,
        running_service,
        s,
        setup_test_environment,
        t,
        test___init__,
        test___main__,
        test_api,
        test_app,
        test_app_data,
        test_config,
        test_constants,
        test_examples,
        test_fields,
        test_handlers,
        test_models,
        test_protocols,
        test_services,
        test_typings,
        test_utilities,
        test_version,
        typings,
        u,
        unit,
        utilities,
        x,
    )
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
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)

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
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
