"""FlextWebConfig — frozen config singleton for flext-web (ADR-005 §7).

Model-less: business rules live in ``config/*.yaml`` under the ``Web:`` key and
are exposed through the open ``config.Web`` namespace (``extra="allow"``), with
no per-domain model. Access is ``config.Web.<domain>[<key>...]``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_cli import FlextCliConfig

from flext_core import FlextSettings
from flext_web import m
from flext_web._models import FlextWebModelsWebNamespace


class FlextWebConfig(FlextSettings, FlextCliConfig):
    """Web config auto-loaded model-less from ``config/*.yaml``.

    MRO carries ``FlextSettings`` FIRST (ENFORCE-042); the class stays a frozen,
    YAML-validated config singleton.
    """

    Web: Annotated[
        FlextWebModelsWebNamespace,
        m.Field(description="Open namespace exposing ``config/*.yaml`` under ``Web``."),
    ] = FlextWebModelsWebNamespace()


config: FlextWebConfig = FlextWebConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_web import config``."""

__all__: list[str] = ["FlextWebConfig", "config"]
