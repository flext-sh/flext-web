# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests.unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import c, d, e, h, m, p, r, s, t, td, tf, tk, tm, tv, u, x

    from .test___init__ import TestsFlextWebInit
    from .test___main__ import TestsFlextWebMain
    from .test_api import TestsFlextWebApi
    from .test_app import TestsFlextWebApp
    from .test_auth_service import TestsFlextWebAuth
    from .test_config import TestsFlextWebConfig
    from .test_constants import TestsFlextWebConstantsUnit
    from .test_entities_service import TestsFlextWebEntities
    from .test_factory import TestsFlextWebFactory
    from .test_fields import TestsFlextWebFields
    from .test_handlers import TestsFlextWebHandlers
    from .test_handlers_direct import TestsFlextWebHandlersDirect
    from .test_health import TestsFlextWebHealth
    from .test_models import TestsFlextWebModelsUnit
    from .test_protocols import TestsFlextWebProtocolsUnit
    from .test_services import TestsFlextWebService
    from .test_settings import TestsFlextWebSettings
    from .test_typings import TestsFlextWebTypesUnit
    from .test_utilities import TestsFlextWebUtilitiesUnit
    from .test_version import TestsFlextWebVersion
    from .test_web_services_direct import TestsFlextWebServicesDirect
__all__: tuple[str, ...] = (
    "TestsFlextWebApi",
    "TestsFlextWebApp",
    "TestsFlextWebAuth",
    "TestsFlextWebConfig",
    "TestsFlextWebConstantsUnit",
    "TestsFlextWebEntities",
    "TestsFlextWebFactory",
    "TestsFlextWebFields",
    "TestsFlextWebHandlers",
    "TestsFlextWebHandlersDirect",
    "TestsFlextWebHealth",
    "TestsFlextWebInit",
    "TestsFlextWebMain",
    "TestsFlextWebModelsUnit",
    "TestsFlextWebProtocolsUnit",
    "TestsFlextWebService",
    "TestsFlextWebServicesDirect",
    "TestsFlextWebSettings",
    "TestsFlextWebTypesUnit",
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
    "tm",
    "tv",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
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
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
