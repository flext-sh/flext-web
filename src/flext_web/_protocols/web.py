"""Web protocol namespace assembled from focused shards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from .config import FlextWebProtocolsConfig
from .data import FlextWebProtocolsData
from .framework import FlextWebProtocolsFramework
from .lifecycle import FlextWebProtocolsLifecycle
from .monitoring import FlextWebProtocolsMonitoring
from .template import FlextWebProtocolsTemplate


class FlextWebProtocolsWeb(
    FlextWebProtocolsConfig,
    FlextWebProtocolsData,
    FlextWebProtocolsFramework,
    FlextWebProtocolsLifecycle,
    FlextWebProtocolsMonitoring,
    FlextWebProtocolsTemplate,
):
    """Web protocol namespace assembled from focused contracts."""


__all__: list[str] = ["FlextWebProtocolsWeb"]
