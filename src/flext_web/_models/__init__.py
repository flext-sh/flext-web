# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import defer_lazy_bases, install_lazy_exports

if TYPE_CHECKING:
    from flext_web._models.auth import FlextWebModelsAuth
    from flext_web._models.base import FlextWebModelsBase
    from flext_web._models.config import FlextWebModelsConfig
    from flext_web._models.entity import FlextWebModelsEntity
    from flext_web._models.http import FlextWebModelsHttp
    from flext_web._models.namespace import FlextWebModelsNamespace
    from flext_web._models.responses import FlextWebModelsResponses
    from flext_web._models.system import FlextWebModelsSystem
    from flext_web._models.web import FlextWebModelsWeb


__all__: tuple[str, ...] = (
    "FlextWebModelsAuth",
    "FlextWebModelsBase",
    "FlextWebModelsConfig",
    "FlextWebModelsEntity",
    "FlextWebModelsHttp",
    "FlextWebModelsNamespace",
    "FlextWebModelsResponses",
    "FlextWebModelsSystem",
    "FlextWebModelsWeb",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextWebModelsAuth": ".auth",
        "FlextWebModelsBase": ".base",
        "FlextWebModelsConfig": ".config",
        "FlextWebModelsEntity": ".entity",
        "FlextWebModelsHttp": ".http",
        "FlextWebModelsNamespace": ".namespace",
        "FlextWebModelsResponses": ".responses",
        "FlextWebModelsSystem": ".system",
        "FlextWebModelsWeb": ".web",
    },
    public_exports=__all__,
    deferred_members={
        "FlextWebModelsAuth": (
            "Credentials",
            "UserData",
            "AppData",
            "EntityData",
        ),
        "FlextWebModelsConfig": ("FastAPIAppConfig",),
        "FlextWebModelsEntity": (
            "Entity",
            "EntityConfig",
        ),
        "FlextWebModelsHttp": (
            "Message",
            "Request",
            "Response",
        ),
        "FlextWebModelsNamespace": ("ConfigNamespace",),
        "FlextWebModelsResponses": (
            "AuthResponse",
            "UserResponse",
            "ApplicationResponse",
            "HealthResponse",
            "MetricsResponse",
            "DashboardResponse",
            "ServiceResponse",
        ),
        "FlextWebModelsSystem": (
            "SystemInfo",
            "HealthStatus",
        ),
        "FlextWebModelsWeb": (),
    },
)

defer_lazy_bases(
    __name__,
    {
        "FlextWebModelsWeb": (
            ("flext_web._models._web", "FlextWebModelsWebMessage"),
            ("flext_web._models._web", "FlextWebModelsWebRequest"),
        ),
    },
)
