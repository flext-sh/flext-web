# AUTO-GENERATED FILE — Regenerate with: make gen
"""Models package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_web._models._auth import FlextWebModelsAuth as FlextWebModelsAuth
    from flext_web._models._config import FlextWebModelsConfig as FlextWebModelsConfig
    from flext_web._models._entity import FlextWebModelsEntity as FlextWebModelsEntity
    from flext_web._models._factory import (
        FlextWebModelsFactory as FlextWebModelsFactory,
    )
    from flext_web._models._http import FlextWebModelsHttp as FlextWebModelsHttp
    from flext_web._models._responses import (
        FlextWebModelsResponses as FlextWebModelsResponses,
    )
    from flext_web._models._system import FlextWebModelsSystem as FlextWebModelsSystem
    from flext_web._models._web_message import (
        FlextWebModelsWebMessage as FlextWebModelsWebMessage,
    )
    from flext_web._models._web_request import (
        FlextWebModelsWebRequest as FlextWebModelsWebRequest,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        "._auth": ("FlextWebModelsAuth",),
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
