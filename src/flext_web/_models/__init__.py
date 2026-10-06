# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_web._models._auth import FlextWebModelsAuth
    from flext_web._models._config import FlextWebModelsConfig
    from flext_web._models._entity import FlextWebModelsEntity
    from flext_web._models._http import FlextWebModelsHttp
    from flext_web._models._responses import FlextWebModelsResponses
    from flext_web._models._system import FlextWebModelsSystem
    from flext_web._models._web_message import FlextWebModelsWebMessage
    from flext_web._models._web_namespace import FlextWebModelsWebNamespace
    from flext_web._models._web_request import FlextWebModelsWebRequest
    from flext_web._models.base import FlextWebModelsBase


__all__: tuple[str, ...] = (
    "FlextWebModelsAuth",
    "FlextWebModelsBase",
    "FlextWebModelsConfig",
    "FlextWebModelsEntity",
    "FlextWebModelsHttp",
    "FlextWebModelsResponses",
    "FlextWebModelsSystem",
    "FlextWebModelsWebMessage",
    "FlextWebModelsWebNamespace",
    "FlextWebModelsWebRequest",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextWebModelsAuth": "._auth",
        "FlextWebModelsBase": ".base",
        "FlextWebModelsConfig": "._config",
        "FlextWebModelsEntity": "._entity",
        "FlextWebModelsHttp": "._http",
        "FlextWebModelsResponses": "._responses",
        "FlextWebModelsSystem": "._system",
        "FlextWebModelsWebMessage": "._web_message",
        "FlextWebModelsWebNamespace": "._web_namespace",
        "FlextWebModelsWebRequest": "._web_request",
    }),
    public_exports=__all__,
)
