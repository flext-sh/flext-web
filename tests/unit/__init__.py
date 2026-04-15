# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test___init__": ("test___init__",),
        ".test___main__": ("test___main__",),
        ".test_api": ("test_api",),
        ".test_app": ("test_app",),
        ".test_config": ("test_config",),
        ".test_constants": ("test_constants",),
        ".test_fields": ("test_fields",),
        ".test_handlers": ("test_handlers",),
        ".test_models": ("test_models",),
        ".test_protocols": ("test_protocols",),
        ".test_services": ("test_services",),
        ".test_typings": ("test_typings",),
        ".test_utilities": ("test_utilities",),
        ".test_version": ("test_version",),
        "flext_web": (
            "c",
            "d",
            "e",
            "h",
            "m",
            "p",
            "r",
            "s",
            "t",
            "u",
            "x",
        ),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
