# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_web.tests.unit.test___init__ import (
        TestsFlextWebInit as TestsFlextWebInit,
    )
    from flext_web.tests.unit.test___main__ import (
        TestsFlextWebMain as TestsFlextWebMain,
    )
    from flext_web.tests.unit.test_api import TestsFlextWebApi as TestsFlextWebApi
    from flext_web.tests.unit.test_app import TestsFlextWebApp as TestsFlextWebApp
    from flext_web.tests.unit.test_config import (
        TestsFlextWebConfig as TestsFlextWebConfig,
    )
    from flext_web.tests.unit.test_constants import (
        TestsFlextWebConstantsUnit as TestsFlextWebConstantsUnit,
    )
    from flext_web.tests.unit.test_fields import (
        TestsFlextWebFields as TestsFlextWebFields,
    )
    from flext_web.tests.unit.test_handlers import (
        TestsFlextWebHandlers as TestsFlextWebHandlers,
    )
    from flext_web.tests.unit.test_models import (
        TestsFlextWebModelsUnit as TestsFlextWebModelsUnit,
    )
    from flext_web.tests.unit.test_protocols import (
        TestsFlextWebProtocolsUnit as TestsFlextWebProtocolsUnit,
    )
    from flext_web.tests.unit.test_services import (
        TestsFlextWebService as TestsFlextWebService,
    )
    from flext_web.tests.unit.test_typings import (
        TestsFlextWebTypesUnit as TestsFlextWebTypesUnit,
    )
    from flext_web.tests.unit.test_utilities import (
        TestsFlextWebUtilitiesUnit as TestsFlextWebUtilitiesUnit,
    )
    from flext_web.tests.unit.test_version import (
        TestsFlextWebVersion as TestsFlextWebVersion,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test___init__": ("TestsFlextWebInit",),
        ".test___main__": ("TestsFlextWebMain",),
        ".test_api": ("TestsFlextWebApi",),
        ".test_app": ("TestsFlextWebApp",),
        ".test_config": ("TestsFlextWebConfig",),
        ".test_constants": ("TestsFlextWebConstantsUnit",),
        ".test_fields": ("TestsFlextWebFields",),
        ".test_handlers": ("TestsFlextWebHandlers",),
        ".test_models": ("TestsFlextWebModelsUnit",),
        ".test_protocols": ("TestsFlextWebProtocolsUnit",),
        ".test_services": ("TestsFlextWebService",),
        ".test_typings": ("TestsFlextWebTypesUnit",),
        ".test_utilities": ("TestsFlextWebUtilitiesUnit",),
        ".test_version": ("TestsFlextWebVersion",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
