"""FLEXT Web protocols — pure ``@runtime_checkable`` Protocol surface.

Per AGENTS.md §2.7 (Library Abstraction) + python.md §5a: this module
contains ONLY Protocol class definitions. All runtime/implementation code
lives in ``flext_web.utilities`` (``FlextWebUtilities.Web``).

The composed ``Web`` namespace is owned once by ``_protocols.base`` and
delegated to here, following FLEXT namespace rules (``c/m/t/p/u`` facades).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import p

from ._protocols.base import FlextWebProtocolsBase
from ._protocols.web import FlextWebProtocolsWeb


class FlextWebProtocols(p):
    """Web-specific ``@runtime_checkable`` Protocol surface extending ``p``."""

    class Web(FlextWebProtocolsBase, FlextWebProtocolsWeb):
        """Web domain-specific Protocols."""


p = FlextWebProtocols

__all__: list[str] = ["FlextWebProtocols", "p"]
