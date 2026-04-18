# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test___init__": ("TestFlextWebInit",),
        ".test___main__": (
            "TestFlextWebCliService",
            "TestMainFunction",
        ),
        ".test_api": ("TestFlextWebApi",),
        ".test_app": ("TestFlextWebApp",),
        ".test_config": ("TestFlextWebSettings",),
        ".test_constants": ("TestFlextWebConstants",),
        ".test_fields": ("TestFlextWebFields",),
        ".test_handlers": ("TestFlextWebHandlers",),
        ".test_models": ("TestFlextWebModels",),
        ".test_protocols": ("TestFlextWebProtocols",),
        ".test_services": ("TestFlextWebService",),
        ".test_utilities": ("TestFlextWebUtilities",),
        ".test_version": ("TestFlextWebVersion",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
