# AUTO-GENERATED FILE — Regenerate with: make gen
"""Models package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_web._models._auth import FlextWebModelsAuth
    from flext_web._models._base import FlextWebModelsBase
    from flext_web._models._config import FlextWebModelsConfig
    from flext_web._models._entity import FlextWebModelsEntity
    from flext_web._models._factory import FlextWebModelsFactory
    from flext_web._models._http import FlextWebModelsHttp
    from flext_web._models._responses import FlextWebModelsResponses
    from flext_web._models._system import FlextWebModelsSystem
    from flext_web._models._web_message import FlextWebModelsWebMessage
    from flext_web._models._web_request import FlextWebModelsWebRequest
_LAZY_IMPORTS = build_lazy_import_map(
    {
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
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
