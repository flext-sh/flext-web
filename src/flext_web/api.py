"""Public MRO facade for flext-web.

This module exposes the canonical public interface: one facade class and one
shared alias instance.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from .services.app import FlextWebApp
from .services.auth import FlextWebAuth
from .services.entities import FlextWebEntities
from .services.handlers import FlextWebHandlers
from .services.health import FlextWebHealth
from .services.web import FlextWebServices


class FlextWeb(
    FlextWebApp,
    FlextWebServices,
    FlextWebAuth,
    FlextWebEntities,
    FlextWebHealth,
    FlextWebHandlers,
):
    """Canonical public facade composed via MRO."""


web: FlextWeb = FlextWeb.fetch_global()
"""Shared FlextWeb facade instance."""


__all__: list[str] = ["FlextWeb", "web"]
