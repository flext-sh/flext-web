# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports
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
from flext_web._exports import FLEXT_WEB_LAZY_IMPORTS

if TYPE_CHECKING:
    from flext_cli import d as d, e as e, h as h, r as r, x as x
    from flext_web.api import FlextWeb as FlextWeb, web as web
    from flext_web.base import FlextWebServiceBase as FlextWebServiceBase, s as s
    from flext_web.constants import FlextWebConstants as FlextWebConstants, c as c
    from flext_web.models import FlextWebModels as FlextWebModels, m as m
    from flext_web.protocols import FlextWebProtocols as FlextWebProtocols, p as p
    from flext_web.services.app import FlextWebApp as FlextWebApp
    from flext_web.services.auth import FlextWebAuth as FlextWebAuth
    from flext_web.services.entities import FlextWebEntities as FlextWebEntities
    from flext_web.services.handlers import FlextWebHandlers as FlextWebHandlers
    from flext_web.services.health import FlextWebHealth as FlextWebHealth
    from flext_web.services.web import FlextWebServices as FlextWebServices
    from flext_web.settings import FlextWebSettings as FlextWebSettings
    from flext_web.typings import FlextWebTypes as FlextWebTypes, t as t
    from flext_web.utilities import FlextWebUtilities as FlextWebUtilities, u as u


_LAZY_IMPORTS = FLEXT_WEB_LAZY_IMPORTS


_EAGER_EXPORTS = (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)


_PUBLIC_EXPORTS: tuple[str, ...] = (
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
    "web",
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
    "t",
    "u",
    "web",
    "x",
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    public_exports=_PUBLIC_EXPORTS,
)
