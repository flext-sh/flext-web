# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Web model facade.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_web/models
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliModels

from flext_web._models import (
    FlextWebModelsAuth,
    FlextWebModelsBase,
    FlextWebModelsConfig,
    FlextWebModelsEntity,
    FlextWebModelsHttp,
    FlextWebModelsNamespace,
    FlextWebModelsResponses,
    FlextWebModelsSystem,
    FlextWebModelsWebMessage,
    FlextWebModelsWebRequest,
)


class FlextWebModels(FlextCliModels):
    """HTTP domain models for flext-web."""

    class Web(
        FlextWebModelsAuth,
        FlextWebModelsConfig,
        FlextWebModelsEntity,
        FlextWebModelsHttp,
        FlextWebModelsResponses,
        FlextWebModelsSystem,
        FlextWebModelsWebMessage,
        FlextWebModelsWebRequest,
        FlextWebModelsBase,
        FlextWebModelsNamespace,
    ):
        """Web domain models namespace."""


m = FlextWebModels
__all__: list[str] = ["FlextWebModels", "FlextWebModelsNamespace", "m"]
