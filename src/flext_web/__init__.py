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
    from flext_cli import cli
    from pydantic_core import from_json, to_json, to_jsonable_python

    from flext_core import core, d, e, h, lazy_attribute, r, x

    from . import services
    from ._config import FlextWebConfig, config
    from ._settings import FlextWebSettings, settings
    from .api import FlextWeb, web
    from .base import FlextWebServiceBase, FlextWebServiceBase as s
    from .cli import FlextWebCli, main
    from .constants import FlextWebConstants, c
    from .models import FlextWebModels, m
    from .protocols import FlextWebProtocols, p
    from .services.app import FlextWebApp
    from .services.auth import FlextWebAuth
    from .services.entities import FlextWebEntities
    from .services.handlers import FlextWebHandlers
    from .services.health import FlextWebHealth
    from .services.web import FlextWebServices
    from .typings import FlextWebTypes, t
    from .utilities import FlextWebUtilities, u
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
    "cli",
    "config",
    "core",
    "d",
    "e",
    "from_json",
    "h",
    "lazy_attribute",
    "m",
    "main",
    "p",
    "r",
    "s",
    "services",
    "settings",
    "t",
    "to_json",
    "to_jsonable_python",
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
            ".services.web": ("FlextWebServices",),
            ".typings": ("FlextWebTypes", "t"),
            ".utilities": ("FlextWebUtilities", "u"),
            "flext_cli": ("cli",),
            "flext_core": ("core", "d", "e", "h", "lazy_attribute", "r", "x"),
            "pydantic_core": ("from_json", "to_json", "to_jsonable_python"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
