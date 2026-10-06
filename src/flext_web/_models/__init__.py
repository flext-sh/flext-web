# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web. Models package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from ._auth import FlextWebModelsAuth
    from ._base import FlextWebModelsBase
    from ._config import FlextWebModelsConfig
    from ._entity import FlextWebModelsEntity
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
    "FlextWebModelsHttp",
    "FlextWebModelsResponses",
    "FlextWebModelsSystem",
    "FlextWebModelsWebMessage",
    "FlextWebModelsWebRequest",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextWebModelsAuth": "._auth",
        "FlextWebModelsBase": "._base",
        "FlextWebModelsConfig": "._config",
        "FlextWebModelsEntity": "._entity",
        "FlextWebModelsHttp": "._http",
        "FlextWebModelsResponses": "._responses",
        "FlextWebModelsSystem": "._system",
        "FlextWebModelsWebMessage": "._web_message",
        "FlextWebModelsWebRequest": "._web_request",
    }),
    public_exports=__all__,
)
