"""Public MRO facade for flext-web.

This module exposes the canonical public interface: one facade class and one
shared alias instance.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web import (
    FlextWebApp,
    FlextWebAuth,
    FlextWebEntities,
    FlextWebHandlers,
    FlextWebHealth,
    FlextWebServices,
)
from flext_web.services.api_runtime import FlextWebApiRuntime


class FlextWeb(
    FlextWebApiRuntime,
    FlextWebApp,
    FlextWebServices,
    FlextWebAuth,
    FlextWebEntities,
    FlextWebHealth,
    FlextWebHandlers,
):
    """Canonical public facade composed via MRO."""

    pass


web = FlextWeb.instance()


__all__: list[str] = ["FlextWeb", "web"]
