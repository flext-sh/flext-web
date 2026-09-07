# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import (
    __author__ as __author__,
    __author_email__ as __author_email__,
    __description__ as __description__,
    __license__ as __license__,
    __title__ as __title__,
    __url__ as __url__,
    __version__ as __version__,
    __version_info__ as __version_info__,
)

if TYPE_CHECKING:
    from enum import IntEnum, StrEnum, unique
    from ipaddress import IPv4Address
    from typing import ClassVar, Final

    from flext_cli import d, e, h, r, x

    from . import services as services
    from ._config import FlextWebConfig, config
    from ._settings import FlextWebSettings, settings
    from .api import FlextWeb, web
    from .base import FlextWebServiceBase, FlextWebServiceBase as s
    from .constants import FlextWebConstants, FlextWebConstants as c
    from .models import FlextWebModels, FlextWebModels as m
    from .protocols import FlextWebProtocols, FlextWebProtocols as p
    from .services.app import FlextWebApp
    from .services.auth import FlextWebAuth
    from .services.entities import FlextWebEntities
    from .services.handlers import FlextWebHandlers
    from .services.health import FlextWebHealth
    from .services.web import FlextWebServices
    from .typings import FlextWebTypes, FlextWebTypes as t
    from .utilities import FlextWebUtilities, FlextWebUtilities as u
__all__: tuple[str, ...] = (
    "ClassVar",
    "Final",
    "FlextWeb",
    "FlextWebApp",
    "FlextWebAuth",
    "FlextWebConfig",
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
    "IPv4Address",
    "IntEnum",
    "MappingProxyType",
    "StrEnum",
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
    "p",
    "r",
    "s",
    "services",
    "settings",
    "t",
    "u",
    "unique",
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
            ".constants": ("FlextWebConstants", "c"),
            ".models": ("FlextWebModels", "m"),
            ".protocols": ("FlextWebProtocols", "p"),
            ".services": ("services",),
            ".services.app": ("FlextWebApp",),
            ".services.auth": ("FlextWebAuth",),
            ".services.entities": ("FlextWebEntities",),
            ".services.handlers": ("FlextWebHandlers",),
            ".services.health": ("FlextWebHealth",),
            ".services.web": ("FlextWebServices",),
            ".typings": ("FlextWebTypes", "t"),
            ".utilities": ("FlextWebUtilities", "u"),
            "enum": ("IntEnum", "StrEnum", "unique"),
            "flext_cli": ("d", "e", "h", "r", "x"),
            "ipaddress": ("IPv4Address",),
            "types": ("MappingProxyType",),
            "typing": ("ClassVar", "Final"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
