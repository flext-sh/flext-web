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
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_web import (
        conftest,
        constants,
        helpers,
        integration,
        models,
        protocols,
        test___init__,
        test___main__,
        test_api,
        test_app,
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
        unit,
        utilities,
    )
    from flext_web.conftest import (
        docker_manager,
        invalid_app_data,
        production_config,
        real_app,
        real_config,
        real_service,
        running_service,
        setup_test_environment,
        test_app_data,
    )
    from flext_web.constants import FlextWebTestConstants, FlextWebTestConstants as c
    from flext_web.helpers import (
        TestsModels,
        TestsProtocols,
        TestsTypings,
        TestsUtilities,
    )
    from flext_web.integration import ExamplesFullFunctionalityTest, logger
    from flext_web.models import FlextWebTestModels, FlextWebTestModels as m
    from flext_web.protocols import FlextWebTestProtocols, FlextWebTestProtocols as p
    from flext_web.typings import FlextWebTestTypes, FlextWebTestTypes as t
    from flext_web.unit import (
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
        assert_version_info,
    )
    from flext_web.utilities import FlextWebTestUtilities, FlextWebTestUtilities as u

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
    (
        "flext_web.helpers",
        "flext_web.integration",
        "flext_web.unit",
    ),
    {
        "FlextWebTestConstants": "flext_web.constants",
        "FlextWebTestModels": "flext_web.models",
        "FlextWebTestProtocols": "flext_web.protocols",
        "FlextWebTestTypes": "flext_web.typings",
        "FlextWebTestUtilities": "flext_web.utilities",
        "c": ("flext_web.constants", "FlextWebTestConstants"),
        "conftest": "flext_web.conftest",
        "constants": "flext_web.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "docker_manager": "flext_web.conftest",
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "helpers": "flext_web.helpers",
        "integration": "flext_web.integration",
        "invalid_app_data": "flext_web.conftest",
        "m": ("flext_web.models", "FlextWebTestModels"),
        "models": "flext_web.models",
        "p": ("flext_web.protocols", "FlextWebTestProtocols"),
        "production_config": "flext_web.conftest",
        "protocols": "flext_web.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "real_app": "flext_web.conftest",
        "real_config": "flext_web.conftest",
        "real_service": "flext_web.conftest",
        "running_service": "flext_web.conftest",
        "s": ("flext_core.service", "FlextService"),
        "setup_test_environment": "flext_web.conftest",
        "t": ("flext_web.typings", "FlextWebTestTypes"),
        "test___init__": "flext_web.test___init__",
        "test___main__": "flext_web.test___main__",
        "test_api": "flext_web.test_api",
        "test_app": "flext_web.test_app",
        "test_app_data": "flext_web.conftest",
        "test_config": "flext_web.test_config",
        "test_constants": "flext_web.test_constants",
        "test_examples": "flext_web.test_examples",
        "test_fields": "flext_web.test_fields",
        "test_handlers": "flext_web.test_handlers",
        "test_models": "flext_web.test_models",
        "test_protocols": "flext_web.test_protocols",
        "test_services": "flext_web.test_services",
        "test_typings": "flext_web.test_typings",
        "test_utilities": "flext_web.test_utilities",
        "test_version": "flext_web.test_version",
        "typings": "flext_web.typings",
        "u": ("flext_web.utilities", "FlextWebTestUtilities"),
        "unit": "flext_web.unit",
        "utilities": "flext_web.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
