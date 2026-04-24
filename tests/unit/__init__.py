# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
