"""FLEXT Web model facade.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_web/models
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliModels

from flext_web import t
from flext_web._models import (
    FlextWebModelsAuth,
    FlextWebModelsBase,
    FlextWebModelsConfig,
    FlextWebModelsEntity,
    FlextWebModelsHttp,
    FlextWebModelsResponses,
    FlextWebModelsSystem,
    FlextWebModelsWebMessage,
    FlextWebModelsWebNamespace,
    FlextWebModelsWebRequest,
)


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

__all__: t.MutableSequenceOf[str] = [
    "FlextWebModels",
    "FlextWebModelsWebNamespace",
    "m",
]
