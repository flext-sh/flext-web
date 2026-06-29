"""Web monitoring protocol shard.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_cli import p
from flext_web import t


class FlextWebProtocolsMonitoring:
    """Monitoring protocol shard."""

    class Web:
        """Web monitoring protocols."""

        @runtime_checkable
        class WebMonitoring(p.Service[t.Web.ResponseDict], Protocol):
            """Protocol for web monitoring helpers."""

            @staticmethod
            def web_health_status() -> t.Web.ResponseDict:
                """Return web health status."""
                ...

            @staticmethod
            def web_metrics() -> t.Web.ResponseDict:
                """Return web metrics payload."""
                ...

            def record_web_request(
                self,
                request: t.Web.RequestDict,
                response_time: float,
            ) -> None:
                """Record a request observation."""
                ...


__all__: list[str] = ["FlextWebProtocolsMonitoring"]
