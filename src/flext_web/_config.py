"""FlextWebConfig — frozen config singleton for flext-web (ADR-005 §7).

Model-less: business rules live in ``config/*.yaml`` under the ``Web:`` key and
are exposed through the open ``config.Web`` namespace (``extra="allow"``), with
no per-domain model. Access is ``config.Web.<domain>[<key>...]``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated, Self

from flext_cli import FlextCliConfig, m

from flext_core import FlextSettings
from flext_web._models import WebNamespace


class FlextWebConfig(FlextSettings, FlextCliConfig):
    """Web config auto-loaded model-less from ``config/*.yaml``.

    MRO carries ``FlextSettings`` FIRST (ENFORCE-042); the class stays a frozen,
    YAML-validated config singleton.
    """

    # ENFORCE-042 namespace-holder contract: ``FlextSettings`` contributes
    # namespacing only — instance machinery stays plain object semantics so the
    # settings singleton ``__new__`` cannot leak into the config singleton.
    # The inherited pydantic ``__init__`` still runs the frozen, YAML-validated
    # construction, and the inherited pydantic ``__setattr__`` keeps the frozen
    # guard.
    def __new__(cls, **kwargs: object) -> Self:
        _ = kwargs
        return object.__new__(cls)

    def __eq__(self, other: object) -> bool:
        """Identity equality for the frozen config singleton."""
        return object.__eq__(self, other)

    def __hash__(self) -> int:
        """Identity hash for the frozen config singleton."""
        return object.__hash__(self)

    Web: Annotated[
        WebNamespace,
        m.Field(description="Open namespace exposing ``config/*.yaml`` under ``Web``."),
    ] = WebNamespace()


config: FlextWebConfig = FlextWebConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_web import config``."""

__all__: list[str] = ["FlextWebConfig", "config"]
