"""Web protocol namespace assembled from focused shards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web._protocols.config import FlextWebProtocolsConfig
from flext_web._protocols.data import FlextWebProtocolsData
from flext_web._protocols.framework import FlextWebProtocolsFramework
from flext_web._protocols.lifecycle import FlextWebProtocolsLifecycle
from flext_web._protocols.monitoring import FlextWebProtocolsMonitoring
from flext_web._protocols.template import FlextWebProtocolsTemplate


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
