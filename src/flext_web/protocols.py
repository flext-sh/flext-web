"""FLEXT Web protocols — pure ``@runtime_checkable`` Protocol surface.

Per AGENTS.md §2.7 (Library Abstraction) + python.md §5a: this module
contains ONLY Protocol class definitions. All runtime/implementation code
lives in ``flext_web.utilities`` (``FlextWebUtilities.Web``).

The protocols are composed from shards under ``_protocols/`` via MRO mixin
parts, following FLEXT namespace rules (``c/m/t/p/u`` facades).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import p
from flext_web._protocols.config import FlextWebProtocolsConfig
from flext_web._protocols.data import FlextWebProtocolsData
from flext_web._protocols.framework import FlextWebProtocolsFramework
from flext_web._protocols.lifecycle import FlextWebProtocolsLifecycle
from flext_web._protocols.monitoring import FlextWebProtocolsMonitoring
from flext_web._protocols.template import FlextWebProtocolsTemplate


class FlextWebProtocols(p):
    """Web-specific ``@runtime_checkable`` Protocol surface extending ``p``."""

    class Web(
        FlextWebProtocolsLifecycle.Web,
        FlextWebProtocolsData.Web,
        FlextWebProtocolsTemplate.Web,
        FlextWebProtocolsMonitoring.Web,
        FlextWebProtocolsConfig.Web,
        FlextWebProtocolsFramework.Web,
    ):
        """Web domain-specific Protocols."""


p = FlextWebProtocols

__all__: list[str] = ["FlextWebProtocols", "p"]
