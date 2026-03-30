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
        helpers,
        integration,
        models,
        port_manager,
        protocols,
        typings,
        unit,
        utilities,
    )
    from tests.conftest import *
    from tests.constants import *
    from tests.helpers.models import *
    from tests.helpers.protocols import *
    from tests.helpers.typings import *
    from tests.helpers.utilities import *
    from tests.integration import test_examples
    from tests.integration.test_examples import *
    from tests.models import *
    from tests.port_manager import *
    from tests.protocols import *
    from tests.typings import *
    from tests.unit import (
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
    from tests.unit.test___init__ import *
    from tests.unit.test___main__ import *
    from tests.unit.test_api import *
    from tests.unit.test_app import *
    from tests.unit.test_config import *
    from tests.unit.test_constants import *
    from tests.unit.test_fields import *
    from tests.unit.test_handlers import *
    from tests.unit.test_protocols import *
    from tests.unit.test_services import *
    from tests.unit.test_typings import *
    from tests.unit.test_utilities import *
    from tests.unit.test_version import *
    from tests.utilities import *

from tests.helpers import _LAZY_IMPORTS as _HELPERS_LAZY
from tests.integration import _LAZY_IMPORTS as _INTEGRATION_LAZY
from tests.unit import _LAZY_IMPORTS as _UNIT_LAZY

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    **_HELPERS_LAZY,
    **_INTEGRATION_LAZY,
    **_UNIT_LAZY,
    "FlextWebTestConstants": "tests.constants",
    "FlextWebTestModels": "tests.models",
    "FlextWebTestProtocols": "tests.protocols",
    "FlextWebTestTypes": "tests.typings",
    "FlextWebTestUtilities": "tests.utilities",
    "TestPortManager": "tests.port_manager",
    "assert_failure": "tests.conftest",
    "assert_result": "tests.conftest",
    "assert_success": "tests.conftest",
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
    "m": ["tests.models", "FlextWebTestModels"],
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
    "test_app_data": "tests.conftest",
    "typings": "tests.typings",
    "u": ["tests.utilities", "FlextWebTestUtilities"],
    "unit": "tests.unit",
    "utilities": "tests.utilities",
    "x": "flext_tests",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
