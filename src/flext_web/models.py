"""FLEXT Web models for web applications.

Provides Pydantic models for web-based applications with validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import m
from flext_web._models import (
    FlextWebModelsAuth,
    FlextWebModelsConfig,
    FlextWebModelsEntity,
    FlextWebModelsFactory,
    FlextWebModelsHttp,
    FlextWebModelsResponses,
    FlextWebModelsSystem,
    FlextWebModelsWebMessage,
    FlextWebModelsWebRequest,
)


class FlextWebModels(
    m,
):
    """Web application models collection.

    Provides Pydantic models for web applications with validation.
    """

    class Web(
        FlextWebModelsHttp.Web,
        FlextWebModelsWebMessage.Web,
        FlextWebModelsEntity.Web,
        FlextWebModelsAuth.Web,
        FlextWebModelsResponses.Web,
        FlextWebModelsWebRequest.Web,
        FlextWebModelsConfig.Web,
        FlextWebModelsSystem.Web,
        FlextWebModelsFactory.Web,
    ):
        """Web application models namespace.

        Contains HTTP message models, application entities, and web-specific
        domain objects used throughout the FLEXT web ecosystem.

        Models are immutable value objects (frozen=True) following domain-driven
        design principles with Pydantic v2 validation.
        """


m = FlextWebModels

__all__: list[str] = ["FlextWebModels", "m"]
