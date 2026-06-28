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
    from flext_tests import td as td, tf as tf, tk as tk, tv as tv

    from flext_web import d as d, e as e, h as h, r as r, x as x
    from tests.base import TestsFlextWebServiceBase as TestsFlextWebServiceBase, s as s
    from tests.constants import TestsFlextWebConstants as TestsFlextWebConstants, c as c
    from tests.integration.test_examples import (
        ExamplesFullFunctionalityTest as ExamplesFullFunctionalityTest,
        TestsFlextWebExamples as TestsFlextWebExamples,
    )
    from tests.models import TestsFlextWebModels as TestsFlextWebModels, m as m
    from tests.protocols import TestsFlextWebProtocols as TestsFlextWebProtocols, p as p
    from tests.settings import TestsFlextWebSettings as TestsFlextWebSettings
    from tests.typings import TestsFlextWebTypes as TestsFlextWebTypes, t as t
    from tests.unit.test___init__ import TestsFlextWebInit as TestsFlextWebInit
    from tests.unit.test___main__ import TestsFlextWebMain as TestsFlextWebMain
    from tests.unit.test_api import TestsFlextWebApi as TestsFlextWebApi
    from tests.unit.test_app import TestsFlextWebApp as TestsFlextWebApp
    from tests.unit.test_config import TestsFlextWebConfig as TestsFlextWebConfig
    from tests.unit.test_constants import (
        TestsFlextWebConstantsUnit as TestsFlextWebConstantsUnit,
    )
    from tests.unit.test_fields import TestsFlextWebFields as TestsFlextWebFields
    from tests.unit.test_handlers import TestsFlextWebHandlers as TestsFlextWebHandlers
    from tests.unit.test_models import (
        TestsFlextWebModelsUnit as TestsFlextWebModelsUnit,
    )
    from tests.unit.test_protocols import (
        TestsFlextWebProtocolsUnit as TestsFlextWebProtocolsUnit,
    )
    from tests.unit.test_services import TestsFlextWebService as TestsFlextWebService
    from tests.unit.test_typings import TestsFlextWebTypesUnit as TestsFlextWebTypesUnit
    from tests.unit.test_utilities import (
        TestsFlextWebUtilitiesUnit as TestsFlextWebUtilitiesUnit,
    )
    from tests.unit.test_version import TestsFlextWebVersion as TestsFlextWebVersion
    from tests.utilities import TestsFlextWebUtilities as TestsFlextWebUtilities, u as u
_LAZY_IMPORTS = merge_lazy_imports(
    (
        ".integration",
        ".unit",
    ),
    build_lazy_import_map(
        {
            ".base": (
                "TestsFlextWebServiceBase",
                "s",
            ),
            ".constants": (
                "TestsFlextWebConstants",
                "c",
            ),
            ".integration.test_examples": (
                "ExamplesFullFunctionalityTest",
                "TestsFlextWebExamples",
            ),
            ".models": (
                "TestsFlextWebModels",
                "m",
            ),
            ".protocols": (
                "TestsFlextWebProtocols",
                "p",
            ),
            ".settings": ("TestsFlextWebSettings",),
            ".typings": (
                "TestsFlextWebTypes",
                "t",
            ),
            ".unit.test___init__": ("TestsFlextWebInit",),
            ".unit.test___main__": ("TestsFlextWebMain",),
            ".unit.test_api": ("TestsFlextWebApi",),
            ".unit.test_app": ("TestsFlextWebApp",),
            ".unit.test_config": ("TestsFlextWebConfig",),
            ".unit.test_constants": ("TestsFlextWebConstantsUnit",),
            ".unit.test_fields": ("TestsFlextWebFields",),
            ".unit.test_handlers": ("TestsFlextWebHandlers",),
            ".unit.test_models": ("TestsFlextWebModelsUnit",),
            ".unit.test_protocols": ("TestsFlextWebProtocolsUnit",),
            ".unit.test_services": ("TestsFlextWebService",),
            ".unit.test_typings": ("TestsFlextWebTypesUnit",),
            ".unit.test_utilities": ("TestsFlextWebUtilitiesUnit",),
            ".unit.test_version": ("TestsFlextWebVersion",),
            ".utilities": (
                "TestsFlextWebUtilities",
                "u",
            ),
            "flext_tests": (
                "td",
                "tf",
                "tk",
                "tv",
            ),
            "flext_web": (
                "d",
                "e",
                "h",
                "r",
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
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "ExamplesFullFunctionalityTest",
    "TestsFlextWebApi",
    "TestsFlextWebApp",
    "TestsFlextWebConfig",
    "TestsFlextWebConstants",
    "TestsFlextWebConstantsUnit",
    "TestsFlextWebExamples",
    "TestsFlextWebFields",
    "TestsFlextWebHandlers",
    "TestsFlextWebInit",
    "TestsFlextWebMain",
    "TestsFlextWebModels",
    "TestsFlextWebModelsUnit",
    "TestsFlextWebProtocols",
    "TestsFlextWebProtocolsUnit",
    "TestsFlextWebService",
    "TestsFlextWebServiceBase",
    "TestsFlextWebSettings",
    "TestsFlextWebTypes",
    "TestsFlextWebTypesUnit",
    "TestsFlextWebUtilities",
    "TestsFlextWebUtilitiesUnit",
    "TestsFlextWebVersion",
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
    "tv",
    "u",
    "x",
]
