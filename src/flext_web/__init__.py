# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports
from flext_web.__version__ import (
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
    from flext_cli import d, e, h, r, x

    from ._config import FlextWebConfig, config
    from ._models._auth import FlextWebModelsAuth
    from ._models._base import FlextWebModelsBase
    from ._models._config import FlextWebModelsConfig
    from ._models._entity import FlextWebModelsEntity
    from ._models._factory import FlextWebModelsFactory
    from ._models._http import FlextWebModelsHttp
    from ._models._responses import FlextWebModelsResponses
    from ._models._system import FlextWebModelsSystem
    from ._models._web_message import FlextWebModelsWebMessage
    from ._models._web_request import FlextWebModelsWebRequest
    from ._protocols.config import FlextWebProtocolsConfig
    from ._protocols.data import FlextWebProtocolsData
    from ._protocols.framework import FlextWebProtocolsFramework
    from ._protocols.lifecycle import FlextWebProtocolsLifecycle
    from ._protocols.monitoring import FlextWebProtocolsMonitoring
    from ._protocols.template import FlextWebProtocolsTemplate
    from ._settings import FlextWebSettings, settings
    from .api import FlextWeb, web
    from .base import FlextWebServiceBase, s
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

    _ = (
        c,
        FlextWebConstants,
        t,
        FlextWebTypes,
        p,
        FlextWebProtocols,
        m,
        FlextWebModels,
        u,
        FlextWebUtilities,
        d,
        e,
        h,
        r,
        x,
        s,
        FlextWebServiceBase,
        FlextWebConfig,
        config,
        FlextWebModelsAuth,
        FlextWebModelsBase,
        FlextWebModelsConfig,
        FlextWebModelsEntity,
        FlextWebModelsFactory,
        FlextWebModelsHttp,
        FlextWebModelsResponses,
        FlextWebModelsSystem,
        FlextWebModelsWebMessage,
        FlextWebModelsWebRequest,
        FlextWebProtocolsConfig,
        FlextWebProtocolsData,
        FlextWebProtocolsFramework,
        FlextWebProtocolsLifecycle,
        FlextWebProtocolsMonitoring,
        FlextWebProtocolsTemplate,
        FlextWebSettings,
        settings,
        FlextWeb,
        web,
        FlextWebApp,
        FlextWebAuth,
        FlextWebEntities,
        FlextWebHandlers,
        FlextWebHealth,
        FlextWebServices,
    )


_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._config": ("FlextWebConfig", "config"),
    "._models._auth": ("FlextWebModelsAuth",),
    "._models._base": ("FlextWebModelsBase",),
    "._models._config": ("FlextWebModelsConfig",),
    "._models._entity": ("FlextWebModelsEntity",),
    "._models._factory": ("FlextWebModelsFactory",),
    "._models._http": ("FlextWebModelsHttp",),
    "._models._responses": ("FlextWebModelsResponses",),
    "._models._system": ("FlextWebModelsSystem",),
    "._models._web_message": ("FlextWebModelsWebMessage",),
    "._models._web_request": ("FlextWebModelsWebRequest",),
    "._protocols.config": ("FlextWebProtocolsConfig",),
    "._protocols.data": ("FlextWebProtocolsData",),
    "._protocols.framework": ("FlextWebProtocolsFramework",),
    "._protocols.lifecycle": ("FlextWebProtocolsLifecycle",),
    "._protocols.monitoring": ("FlextWebProtocolsMonitoring",),
    "._protocols.template": ("FlextWebProtocolsTemplate",),
    "._settings": ("FlextWebSettings", "settings"),
    ".api": ("FlextWeb", "web"),
    ".base": ("FlextWebServiceBase", "s"),
    ".constants": ("FlextWebConstants", "c"),
    ".models": ("FlextWebModels", "m"),
    ".protocols": ("FlextWebProtocols", "p"),
    ".services.app": ("FlextWebApp",),
    ".services.auth": ("FlextWebAuth",),
    ".services.entities": ("FlextWebEntities",),
    ".services.handlers": ("FlextWebHandlers",),
    ".services.health": ("FlextWebHealth",),
    ".services.web": ("FlextWebServices",),
    ".typings": ("FlextWebTypes", "t"),
    ".utilities": ("FlextWebUtilities", "u"),
    "flext_cli": ("d", "e", "h", "r", "x"),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_DIRECT_IMPORTS: tuple[str, ...] = (
    "FlextWeb",
    "FlextWebApp",
    "FlextWebAuth",
    "FlextWebConfig",
    "FlextWebConstants",
    "FlextWebEntities",
    "FlextWebHandlers",
    "FlextWebHealth",
    "FlextWebModels",
    "FlextWebModelsAuth",
    "FlextWebModelsBase",
    "FlextWebModelsConfig",
    "FlextWebModelsEntity",
    "FlextWebModelsFactory",
    "FlextWebModelsHttp",
    "FlextWebModelsResponses",
    "FlextWebModelsSystem",
    "FlextWebModelsWebMessage",
    "FlextWebModelsWebRequest",
    "FlextWebProtocols",
    "FlextWebProtocolsConfig",
    "FlextWebProtocolsData",
    "FlextWebProtocolsFramework",
    "FlextWebProtocolsLifecycle",
    "FlextWebProtocolsMonitoring",
    "FlextWebProtocolsTemplate",
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
    "build_lazy_import_map",
    "c",
    "config",
    "d",
    "e",
    "h",
    "install_lazy_exports",
    "m",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "u",
    "web",
    "x",
)

__all__: tuple[str, ...] = (
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
    "settings",
    "t",
    "u",
    "web",
    "x",
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
