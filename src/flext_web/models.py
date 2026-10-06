"""FLEXT Web model facade.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_web/models
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliModels

from flext_web import t
from flext_web._models import WebNamespace
from flext_web._models._auth import FlextWebModelsAuth
from flext_web._models.base import FlextWebModelsBase
from flext_web._models._config import FlextWebModelsConfig
from flext_web._models._entity import FlextWebModelsEntity
from flext_web._models._http import FlextWebModelsHttp
from flext_web._models._responses import FlextWebModelsResponses
from flext_web._models._system import FlextWebModelsSystem
from flext_web._models._web_message import FlextWebModelsWebMessage
from flext_web._models._web_request import FlextWebModelsWebRequest


class FlextWebModels(FlextCliModels):
    """HTTP domain models for flext-web."""

    class Web(
        FlextWebModelsBase,
        FlextWebModelsConfig,
        FlextWebModelsEntity,
        FlextWebModelsHttp,
        FlextWebModelsResponses,
        FlextWebModelsSystem,
        FlextWebModelsWebMessage,
        FlextWebModelsWebRequest,
        FlextWebModelsAuth,
    ):
        """Web domain models namespace."""


m = FlextWebModels

__all__: t.MutableSequenceOf[str] = ["FlextWebModels", "WebNamespace", "m"]
