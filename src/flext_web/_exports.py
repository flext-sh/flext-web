# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export registry."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, merge_lazy_imports

_LOCAL_LAZY_IMPORTS = build_lazy_import_map(
    {
        "._models": ("_models",),
        "._protocols": ("_protocols",),
        ".api": (
            "FlextWeb",
            "web",
        ),
        ".base": (
            "FlextWebServiceBase",
            "s",
        ),
        ".constants": (
            "FlextWebConstants",
            "c",
        ),
        ".models": (
            "FlextWebModels",
            "m",
        ),
        ".protocols": (
            "FlextWebProtocols",
            "p",
        ),
        ".services": ("services",),
        ".services.app": ("FlextWebApp",),
        ".services.auth": ("FlextWebAuth",),
        ".services.entities": ("FlextWebEntities",),
        ".services.handlers": ("FlextWebHandlers",),
        ".services.health": ("FlextWebHealth",),
        ".services.web": ("FlextWebServices",),
        ".settings": ("FlextWebSettings",),
        ".typings": (
            "FlextWebTypes",
            "t",
        ),
        ".utilities": (
            "FlextWebUtilities",
            "u",
        ),
        "flext_cli": (
            "d",
            "e",
            "h",
            "r",
            "x",
        ),
    },
)

FLEXT_WEB_LAZY_IMPORTS = merge_lazy_imports(
    (".services",),
    _LOCAL_LAZY_IMPORTS,
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
    module_name="flext_web",
)

__all__: list[str] = ["FLEXT_WEB_LAZY_IMPORTS"]
