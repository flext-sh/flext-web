"""Web protocol namespace assembled from focused shards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from flext_web._protocols import (
    FlextWebProtocolsConfig,
    FlextWebProtocolsData,
    FlextWebProtocolsFramework,
    FlextWebProtocolsLifecycle,
    FlextWebProtocolsMonitoring,
    FlextWebProtocolsTemplate,
)


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
