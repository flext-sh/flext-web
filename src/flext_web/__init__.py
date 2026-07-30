# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import __author__ as __author__
from .__version__ import __author_email__ as __author_email__
from .__version__ import __description__ as __description__
from .__version__ import __license__ as __license__
from .__version__ import __title__ as __title__
from .__version__ import __url__ as __url__
from .__version__ import __version__ as __version__
from .__version__ import __version_info__ as __version_info__

if TYPE_CHECKING:
    from flext_cli import d as d
    from flext_cli import e as e
    from flext_cli import h as h
    from flext_cli import r as r
    from flext_cli import x as x

    from ._config import FlextWebConfig as FlextWebConfig
    from ._config import config as config
    from ._settings import FlextWebSettings as FlextWebSettings
    from ._settings import settings as settings
    from .api import FlextWeb as FlextWeb
    from .api import web as web
    from .base import FlextWebServiceBase as FlextWebServiceBase

    s: type[FlextWebServiceBase]
    from .constants import FlextWebConstants as FlextWebConstants

    c: type[FlextWebConstants]
    from .models import FlextWebModels as FlextWebModels

    m: type[FlextWebModels]
    from .protocols import FlextWebProtocols as FlextWebProtocols

    p: type[FlextWebProtocols]
    from .typings import FlextWebTypes as FlextWebTypes

    t: type[FlextWebTypes]
    from .utilities import FlextWebUtilities as FlextWebUtilities

    u: type[FlextWebUtilities]

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._config": ("FlextWebConfig", "config"),
    "._settings": ("FlextWebSettings", "settings"),
    ".api": ("FlextWeb", "web"),
    ".base": ("FlextWebServiceBase", "s"),
    ".constants": ("FlextWebConstants", "c"),
    ".models": ("FlextWebModels", "m"),
    ".protocols": ("FlextWebProtocols", "p"),
    ".typings": ("FlextWebTypes", "t"),
    ".utilities": ("FlextWebUtilities", "u"),
    "flext_cli": ("d", "e", "h", "r", "x"),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextWeb",
    "FlextWebConfig",
    "FlextWebConstants",
    "FlextWebModels",
    "FlextWebProtocols",
    "FlextWebServiceBase",
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
    "p",
    "r",
    "s",
    "settings",
    "t",
    "u",
    "web",
    "x",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
