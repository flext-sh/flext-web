# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if _t.TYPE_CHECKING:
    from flext_tests import td, tf, tk, tm, tv
    from flext_web import d, e, h, r, s, x
    from tests.constants import TestsFlextWebConstants, c
    from tests.helpers.models import TestsModels
    from tests.helpers.protocols import TestsProtocols
    from tests.helpers.typings import TestsTypings
    from tests.helpers.utilities import TestsUtilities
    from tests.integration.test_examples import (
        ExamplesFullFunctionalityTest,
        TestExamples,
    )
    from tests.models import TestsFlextWebModels, m
    from tests.protocols import TestsFlextWebProtocols, p
    from tests.typings import TestsFlextWebTypes, t
    from tests.unit.test___init__ import TestFlextWebInit
    from tests.unit.test___main__ import TestFlextWebCliService, TestMainFunction
    from tests.unit.test_api import TestFlextWebApi
    from tests.unit.test_app import TestFlextWebApp
    from tests.unit.test_config import TestFlextWebSettings
    from tests.unit.test_constants import TestFlextWebConstants
    from tests.unit.test_fields import TestFlextWebFields
    from tests.unit.test_handlers import TestFlextWebHandlers
    from tests.unit.test_models import TestFlextWebModels
    from tests.unit.test_protocols import TestFlextWebProtocols
    from tests.unit.test_services import TestFlextWebService
    from tests.unit.test_typings import TestFlextWebModelsTypings
    from tests.unit.test_utilities import TestFlextWebUtilities
    from tests.unit.test_version import TestFlextWebVersion
    from tests.utilities import TestsFlextWebUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    (
        ".helpers",
        ".integration",
        ".unit",
    ),
    build_lazy_import_map(
        {
            ".constants": (
                "TestsFlextWebConstants",
                "c",
            ),
            ".helpers.models": ("TestsModels",),
            ".helpers.protocols": ("TestsProtocols",),
            ".helpers.typings": ("TestsTypings",),
            ".helpers.utilities": ("TestsUtilities",),
            ".integration.test_examples": (
                "ExamplesFullFunctionalityTest",
                "TestExamples",
            ),
            ".models": (
                "TestsFlextWebModels",
                "m",
            ),
            ".protocols": (
                "TestsFlextWebProtocols",
                "p",
            ),
            ".typings": (
                "TestsFlextWebTypes",
                "t",
            ),
            ".unit.test___init__": ("TestFlextWebInit",),
            ".unit.test___main__": (
                "TestFlextWebCliService",
                "TestMainFunction",
            ),
            ".unit.test_api": ("TestFlextWebApi",),
            ".unit.test_app": ("TestFlextWebApp",),
            ".unit.test_config": ("TestFlextWebSettings",),
            ".unit.test_constants": ("TestFlextWebConstants",),
            ".unit.test_fields": ("TestFlextWebFields",),
            ".unit.test_handlers": ("TestFlextWebHandlers",),
            ".unit.test_models": ("TestFlextWebModels",),
            ".unit.test_protocols": ("TestFlextWebProtocols",),
            ".unit.test_services": ("TestFlextWebService",),
            ".unit.test_typings": ("TestFlextWebModelsTypings",),
            ".unit.test_utilities": ("TestFlextWebUtilities",),
            ".unit.test_version": ("TestFlextWebVersion",),
            ".utilities": (
                "TestsFlextWebUtilities",
                "u",
            ),
            "flext_tests": (
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
            ),
            "flext_web": (
                "d",
                "e",
                "h",
                "r",
                "s",
                "x",
            ),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "ExamplesFullFunctionalityTest",
    "TestExamples",
    "TestFlextWebApi",
    "TestFlextWebApp",
    "TestFlextWebCliService",
    "TestFlextWebConstants",
    "TestFlextWebFields",
    "TestFlextWebHandlers",
    "TestFlextWebInit",
    "TestFlextWebModels",
    "TestFlextWebModelsTypings",
    "TestFlextWebProtocols",
    "TestFlextWebService",
    "TestFlextWebSettings",
    "TestFlextWebUtilities",
    "TestFlextWebVersion",
    "TestMainFunction",
    "TestsFlextWebConstants",
    "TestsFlextWebModels",
    "TestsFlextWebProtocols",
    "TestsFlextWebTypes",
    "TestsFlextWebUtilities",
    "TestsModels",
    "TestsProtocols",
    "TestsTypings",
    "TestsUtilities",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
]
