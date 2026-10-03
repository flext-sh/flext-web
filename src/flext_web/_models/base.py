"""Base model facade for flext-web.

Absorbs every model shard through MRO so the public ``models.py`` facade
composes a single ``Api`` namespace.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web._models._auth import FlextWebModelsAuth
from flext_web._models._config import FlextWebModelsConfig
from flext_web._models._entity import FlextWebModelsEntity
from flext_web._models._factory import FlextWebModelsFactory
from flext_web._models._http import FlextWebModelsHttp
from flext_web._models._responses import FlextWebModelsResponses
from flext_web._models._system import FlextWebModelsSystem
from flext_web._models._web_message import FlextWebModelsWebMessage
from flext_web._models._web_request import FlextWebModelsWebRequest


class FlextWebModelsBase(
    FlextWebModelsAuth,
    FlextWebModelsConfig,
    FlextWebModelsEntity,
    FlextWebModelsFactory,
    FlextWebModelsHttp,
    FlextWebModelsResponses,
    FlextWebModelsSystem,
    FlextWebModelsWebMessage,
    FlextWebModelsWebRequest,
):
    """FLEXT Web model namespace."""


__all__: list[str] = ["FlextWebModelsBase"]
