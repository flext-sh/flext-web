# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)
from flext_web.__version__ import *

if _t.TYPE_CHECKING:
    from flext_core import d, e, h, r, s, x
    from flext_web.api import FlextWeb
    from flext_web.base import FlextWebServiceBase
    from flext_web.constants import FlextWebConstants, c
    from flext_web.models import FlextWebModels, m
    from flext_web.protocols import FlextWebProtocols, p
    from flext_web.services.app import FlextWebApp
    from flext_web.services.auth import FlextWebAuth
    from flext_web.services.entities import FlextWebEntities
    from flext_web.services.handlers import FlextWebHandlers
    from flext_web.services.health import FlextWebHealth
    from flext_web.services.web import FlextWebServices
    from flext_web.settings import FlextWebSettings
    from flext_web.typings import FlextWebTypes, t
    from flext_web.utilities import FlextWebUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    (".services",),
    build_lazy_import_map(
        {
            ".__version__": (
                "__author__",
                "__author_email__",
                "__description__",
                "__license__",
                "__title__",
                "__url__",
                "__version__",
                "__version_info__",
            ),
            ".api": ("FlextWeb",),
            ".base": ("FlextWebServiceBase",),
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
            ".settings": ("FlextWebSettings",),
            ".typings": (
                "FlextWebTypes",
                "t",
            ),
            ".utilities": (
                "FlextWebUtilities",
                "u",
            ),
            "flext_core": (
                "d",
                "e",
                "h",
                "r",
                "s",
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
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__ = [
    "FlextWeb",
    "FlextWebApp",
    "FlextWebAuth",
    "FlextWebConstants",
    "FlextWebEntities",
    "FlextWebHandlers",
    "FlextWebHealth",
    "FlextWebModels",
    "FlextWebProtocols",
    "FlextWebServiceBase",
    "FlextWebServices",
    "FlextWebSettings",
    "FlextWebTypes",
    "FlextWebUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
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
]
