# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web. Models package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from ._auth import FlextWebModelsAuth
    from ._base import FlextWebModelsBase
    from ._config import FlextWebModelsConfig
    from ._entity import FlextWebModelsEntity
    from ._factory import FlextWebModelsFactory
    from ._http import FlextWebModelsHttp
    from ._responses import FlextWebModelsResponses
    from ._system import FlextWebModelsSystem
    from ._web_message import FlextWebModelsWebMessage
    from ._web_request import FlextWebModelsWebRequest
__all__: tuple[str, ...] = (
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

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
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
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
