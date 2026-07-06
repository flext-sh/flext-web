# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if TYPE_CHECKING:
    from flext_tests import d, e, h, r, td, tf, tk, tm, tv, x

    from tests.base import TestsFlextWebServiceBase, s
    from tests.constants import TestsFlextWebConstants, c
    from tests.integration.test_examples import (
        ExamplesFullFunctionalityTest,
        TestsFlextWebExamples,
    )
    from tests.models import TestsFlextWebModels, m
    from tests.protocols import TestsFlextWebProtocols, p
    from tests.settings import TestsFlextWebSettings
    from tests.typings import TestsFlextWebTypes, t
    from tests.unit.test___init__ import TestsFlextWebInit
    from tests.unit.test___main__ import TestsFlextWebMain
    from tests.unit.test_api import TestsFlextWebApi
    from tests.unit.test_app import TestsFlextWebApp
    from tests.unit.test_auth_service import TestsFlextWebAuth
    from tests.unit.test_config import TestsFlextWebConfig
    from tests.unit.test_constants import TestsFlextWebConstantsUnit
    from tests.unit.test_entities_service import TestsFlextWebEntities
    from tests.unit.test_factory import TestsFlextWebFactory
    from tests.unit.test_fields import TestsFlextWebFields
    from tests.unit.test_handlers import TestsFlextWebHandlers
    from tests.unit.test_handlers_direct import TestsFlextWebHandlersDirect
    from tests.unit.test_health import TestsFlextWebHealth
    from tests.unit.test_models import TestsFlextWebModelsUnit
    from tests.unit.test_protocols import TestsFlextWebProtocolsUnit
    from tests.unit.test_services import TestsFlextWebService
    from tests.unit.test_typings import TestsFlextWebTypesUnit
    from tests.unit.test_utilities import TestsFlextWebUtilitiesUnit
    from tests.unit.test_version import TestsFlextWebVersion
    from tests.unit.test_web_services_direct import TestsFlextWebServicesDirect
    from tests.utilities import TestsFlextWebUtilities, u
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
            ".conftest": ("conftest",),
            ".constants": (
                "TestsFlextWebConstants",
                "c",
            ),
            ".integration": ("integration",),
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
            ".unit": ("unit",),
            ".unit.test___init__": ("TestsFlextWebInit",),
            ".unit.test___main__": ("TestsFlextWebMain",),
            ".unit.test_api": ("TestsFlextWebApi",),
            ".unit.test_app": ("TestsFlextWebApp",),
            ".unit.test_auth_service": ("TestsFlextWebAuth",),
            ".unit.test_config": ("TestsFlextWebConfig",),
            ".unit.test_constants": ("TestsFlextWebConstantsUnit",),
            ".unit.test_entities_service": ("TestsFlextWebEntities",),
            ".unit.test_factory": ("TestsFlextWebFactory",),
            ".unit.test_fields": ("TestsFlextWebFields",),
            ".unit.test_handlers": ("TestsFlextWebHandlers",),
            ".unit.test_handlers_direct": ("TestsFlextWebHandlersDirect",),
            ".unit.test_health": ("TestsFlextWebHealth",),
            ".unit.test_models": ("TestsFlextWebModelsUnit",),
            ".unit.test_protocols": ("TestsFlextWebProtocolsUnit",),
            ".unit.test_services": ("TestsFlextWebService",),
            ".unit.test_typings": ("TestsFlextWebTypesUnit",),
            ".unit.test_utilities": ("TestsFlextWebUtilitiesUnit",),
            ".unit.test_version": ("TestsFlextWebVersion",),
            ".unit.test_web_services_direct": ("TestsFlextWebServicesDirect",),
            ".utilities": (
                "TestsFlextWebUtilities",
                "u",
            ),
            "flext_tests": (
                "d",
                "e",
                "h",
                "r",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
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


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
