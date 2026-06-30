# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export registry."""

from __future__ import annotations

from flext_core.lazy import merge_lazy_imports
from flext_web._exports_lazy_part_01 import FLEXT_WEB_LAZY_IMPORTS_PART_01

_LOCAL_LAZY_IMPORTS = {
    **FLEXT_WEB_LAZY_IMPORTS_PART_01,
}

FLEXT_WEB_LAZY_IMPORTS = merge_lazy_imports(
    (
        "._models",
        "._protocols",
        ".services",
    ),
    _LOCAL_LAZY_IMPORTS,
    exclude_names=(
        "FlextWebModelsAuth",
        "FlextWebModelsConfig",
        "FlextWebModelsEntity",
        "FlextWebModelsFactory",
        "FlextWebModelsHttp",
        "FlextWebModelsResponses",
        "FlextWebModelsSystem",
        "FlextWebModelsWebMessage",
        "FlextWebModelsWebRequest",
        "FlextWebProtocolsConfig",
        "FlextWebProtocolsData",
        "FlextWebProtocolsFramework",
        "FlextWebProtocolsLifecycle",
        "FlextWebProtocolsMonitoring",
        "FlextWebProtocolsTemplate",
        "_coerce_method",
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
        "services",
    ),
    module_name="flext_web",
)

__all__: list[str] = ["FLEXT_WEB_LAZY_IMPORTS"]
