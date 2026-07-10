"""FlextWebConfig — frozen config singleton for flext-web (ADR-005 §7).

Model-less: business rules live in ``config/*.yaml`` under the ``Web:`` key and
are exposed through the open ``config.Web`` namespace (``extra="allow"``), with
no per-domain model. Access is ``config.Web.<domain>[<key>...]``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from flext_cli import FlextCliConfig


class _WebNamespace(BaseModel):
    """Open, frozen namespace exposing every ``config/*.yaml`` domain model-less."""

    model_config = ConfigDict(extra="allow", frozen=True)


class FlextWebConfig(FlextCliConfig):
    """Web config auto-loaded model-less from ``config/*.yaml``."""

    Web: _WebNamespace = _WebNamespace()


config: FlextWebConfig = FlextWebConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_web import config``."""

__all__: list[str] = ["FlextWebConfig", "config"]
