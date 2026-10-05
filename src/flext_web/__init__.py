# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports
from flext_web.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if TYPE_CHECKING:
    from flext_cli import d, e, h, r, x

    from flext_web import services
    from flext_web._config import FlextWebConfig, config
    from flext_web._settings import FlextWebSettings, settings
    from flext_web.api import FlextWeb, web
    from flext_web.base import FlextWebServiceBase, s
    from flext_web.cli import FlextWebCli, main
    from flext_web.constants import FlextWebConstants, c
    from flext_web.models import FlextWebModels, m
    from flext_web.protocols import FlextWebProtocols, p
    from flext_web.services.app import FlextWebApp
    from flext_web.services.auth import FlextWebAuth
    from flext_web.services.entities import FlextWebEntities
    from flext_web.services.handlers import FlextWebHandlers
    from flext_web.services.health import FlextWebHealth
    from flext_web.services.web import FlextWebMonitoring, FlextWebServices
    from flext_web.typings import FlextWebTypes, t
    from flext_web.utilities import FlextWebUtilities, u


__all__: tuple[str, ...] = (
    "FlextWeb",
    "FlextWebApp",
    "FlextWebAuth",
    "FlextWebCli",
    "FlextWebConfig",
    "FlextWebConstants",
    "FlextWebEntities",
    "FlextWebHandlers",
    "FlextWebHealth",
    "FlextWebModels",
    "FlextWebMonitoring",
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
    "config",
    "d",
    "e",
    "h",
    "m",
    "main",
    "p",
    "r",
    "s",
    "services",
    "settings",
    "t",
    "u",
    "web",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._config": ("FlextWebConfig", "config"),
            "._settings": ("FlextWebSettings", "settings"),
            ".api": ("FlextWeb", "web"),
            ".base": ("FlextWebServiceBase", "s"),
            ".cli": ("FlextWebCli", "main"),
            ".constants": ("FlextWebConstants", "c"),
            ".models": ("FlextWebModels", "m"),
            ".protocols": ("FlextWebProtocols", "p"),
            ".services": ("services",),
            ".services.app": ("FlextWebApp",),
            ".services.auth": ("FlextWebAuth",),
            ".services.entities": ("FlextWebEntities",),
            ".services.handlers": ("FlextWebHandlers",),
            ".services.health": ("FlextWebHealth",),
            ".services.web": ("FlextWebMonitoring", "FlextWebServices"),
            ".typings": ("FlextWebTypes", "t"),
            ".utilities": ("FlextWebUtilities", "u"),
            "flext_cli": ("d", "e", "h", "r", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
