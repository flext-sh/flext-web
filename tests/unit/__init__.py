# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map({
    ".test___init__": ("TestsFlextWebInit",),
    ".test___main__": ("TestsFlextWebMain",),
    ".test_api": ("TestsFlextWebApi",),
    ".test_app": ("TestsFlextWebApp",),
    ".test_auth_service": ("TestsFlextWebAuth",),
    ".test_config": ("TestsFlextWebConfig",),
    ".test_constants": ("TestsFlextWebConstantsUnit",),
    ".test_entities_service": ("TestsFlextWebEntities",),
    ".test_factory": ("TestsFlextWebFactory",),
    ".test_fields": ("TestsFlextWebFields",),
    ".test_handlers": ("TestsFlextWebHandlers",),
    ".test_handlers_direct": ("TestsFlextWebHandlersDirect",),
    ".test_health": ("TestsFlextWebHealth",),
    ".test_models": ("TestsFlextWebModelsUnit",),
    ".test_protocols": ("TestsFlextWebProtocolsUnit",),
    ".test_services": ("TestsFlextWebService",),
    ".test_settings": ("TestsFlextWebSettings",),
    ".test_typings": ("TestsFlextWebTypesUnit",),
    ".test_utilities": ("TestsFlextWebUtilitiesUnit",),
    ".test_version": ("TestsFlextWebVersion",),
    ".test_web_services_direct": ("TestsFlextWebServicesDirect",),
    "flext_tests": (
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
    ),
})


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
