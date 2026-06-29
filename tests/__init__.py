# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

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
