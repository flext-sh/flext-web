# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports
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
    from flext_web.models import FlextWebModels, FlextWebModelsWebNamespace, m
    from flext_web.protocols import FlextWebProtocols, p
    from flext_web.services.app import FlextWebApp
    from flext_web.services.auth import FlextWebAuth
    from flext_web.services.entities import FlextWebEntities
    from flext_web.services.handlers import FlextWebHandlers
    from flext_web.services.health import FlextWebHealth
    from flext_web.services.monitoring import FlextWebMonitoring
    from flext_web.services.web import FlextWebServices
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
    "FlextWebModelsWebNamespace",
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

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextWeb": ".api",
        "FlextWebApp": ".services.app",
        "FlextWebAuth": ".services.auth",
        "FlextWebCli": ".cli",
        "FlextWebConfig": "._config",
        "FlextWebConstants": ".constants",
        "FlextWebEntities": ".services.entities",
        "FlextWebHandlers": ".services.handlers",
        "FlextWebHealth": ".services.health",
        "FlextWebModels": ".models",
        "FlextWebModelsWebNamespace": ".models",
        "FlextWebMonitoring": ".services.monitoring",
        "FlextWebProtocols": ".protocols",
        "FlextWebServiceBase": ".base",
        "FlextWebServices": ".services.web",
        "FlextWebSettings": "._settings",
        "FlextWebTypes": ".typings",
        "FlextWebUtilities": ".utilities",
        "c": ".constants",
        "config": "._config",
        "d": "flext_cli",
        "e": "flext_cli",
        "h": "flext_cli",
        "m": ".models",
        "main": ".cli",
        "p": ".protocols",
        "r": "flext_cli",
        "s": ".base",
        "services": ".services",
        "settings": "._settings",
        "t": ".typings",
        "u": ".utilities",
        "web": ".api",
        "x": "flext_cli",
    }),
    public_exports=__all__,
)
