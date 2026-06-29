"""Internal flext-web models package.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from ._auth import FlextWebModelsAuth
from ._base import _coerce_method
from ._config import FlextWebModelsConfig
from ._entity import FlextWebModelsEntity
from ._factory import FlextWebModelsFactory
from ._http import FlextWebModelsHttp
from ._responses import FlextWebModelsResponses
from ._system import FlextWebModelsSystem
from ._web_message import FlextWebModelsWebMessage
from ._web_request import FlextWebModelsWebRequest

__all__: list[str] = [
    "FlextWebModelsAuth",
    "FlextWebModelsConfig",
    "FlextWebModelsEntity",
    "FlextWebModelsFactory",
    "FlextWebModelsHttp",
    "FlextWebModelsResponses",
    "FlextWebModelsSystem",
    "FlextWebModelsWebMessage",
    "FlextWebModelsWebRequest",
    "_coerce_method",
]
