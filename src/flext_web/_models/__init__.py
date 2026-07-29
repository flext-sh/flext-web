# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web. Models package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from ._auth import FlextWebModelsAuth as FlextWebModelsAuth
    from ._base import FlextWebModelsBase as FlextWebModelsBase
    from ._config import FlextWebModelsConfig as FlextWebModelsConfig
    from ._entity import FlextWebModelsEntity as FlextWebModelsEntity
    from ._factory import FlextWebModelsFactory as FlextWebModelsFactory
    from ._http import FlextWebModelsHttp as FlextWebModelsHttp
    from ._responses import FlextWebModelsResponses as FlextWebModelsResponses
    from ._system import FlextWebModelsSystem as FlextWebModelsSystem
    from ._web_message import FlextWebModelsWebMessage as FlextWebModelsWebMessage
    from ._web_request import FlextWebModelsWebRequest as FlextWebModelsWebRequest

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._auth": ("FlextWebModelsAuth",),
    "._base": ("FlextWebModelsBase",),
    "._config": ("FlextWebModelsConfig",),
    "._entity": ("FlextWebModelsEntity",),
    "._factory": ("FlextWebModelsFactory",),
    "._http": ("FlextWebModelsHttp",),
    "._responses": ("FlextWebModelsResponses",),
    "._system": ("FlextWebModelsSystem",),
    "._web_message": ("FlextWebModelsWebMessage",),
    "._web_request": ("FlextWebModelsWebRequest",),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
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
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
