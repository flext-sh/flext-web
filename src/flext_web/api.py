"""Public MRO facade for flext-web.

This module exposes the canonical public interface: one facade class and one
shared alias instance.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web.services.app import FlextWebApp
from flext_web.services.auth import FlextWebAuth
from flext_web.services.entities import FlextWebEntities
from flext_web.services.handlers import FlextWebHandlers
from flext_web.services.health import FlextWebHealth
from flext_web.services.web import FlextWebServices


class FlextWeb(
    FlextWebApp,
    FlextWebServices,
    FlextWebAuth,
    FlextWebEntities,
    FlextWebHealth,
    FlextWebHandlers,
):
    """Canonical public facade composed via MRO."""


web = FlextWeb.fetch_global()
"""Shared FlextWeb facade instance."""


__all__: list[str] = ["FlextWeb", "web"]
