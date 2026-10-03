"""FLEXT Web model facade.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_cli import FlextCliModels

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

if TYPE_CHECKING:
    from flext_web import t


class FlextWebModels(FlextCliModels):
    """HTTP domain models for flext-web."""

    class Web(
        FlextWebModelsBase,
        FlextWebModelsConfig,
        FlextWebModelsEntity,
        FlextWebModelsFactory,
        FlextWebModelsHttp,
        FlextWebModelsResponses,
        FlextWebModelsSystem,
        FlextWebModelsWebMessage,
        FlextWebModelsWebRequest,
        FlextWebModelsAuth,
    ):
        """Web domain models namespace."""


m = FlextWebModels

__all__: t.MutableSequenceOf[str] = ["FlextWebModels", "m"]
