# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_web._models._auth import FlextWebModelsAuth
    from flext_web._models._base import FlextWebModelsBase
    from flext_web._models._config import FlextWebModelsConfig
    from flext_web._models._entity import FlextWebModelsEntity
    from flext_web._models._http import FlextWebModelsHttp
    from flext_web._models._responses import FlextWebModelsResponses
    from flext_web._models._system import FlextWebModelsSystem
    from flext_web._models._web_message import FlextWebModelsWebMessage
    from flext_web._models._web_request import FlextWebModelsWebRequest


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

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._auth": ("FlextWebModelsAuth",),
            "._base": ("FlextWebModelsBase",),
            "._config": ("FlextWebModelsConfig",),
            "._entity": ("FlextWebModelsEntity",),
            "._http": ("FlextWebModelsHttp",),
            "._responses": ("FlextWebModelsResponses",),
            "._system": ("FlextWebModelsSystem",),
            "._web_message": ("FlextWebModelsWebMessage",),
            "._web_request": ("FlextWebModelsWebRequest",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
