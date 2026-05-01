"""Shared service foundation for flext-web components.

Centralizes typed access to the registered `web` settings namespace while
preserving the flext-core service lifecycle and logger/runtime inheritance.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from abc import ABC
from typing import Annotated, override

from flext_core import FlextSettings, s
from flext_web import FlextWebSettings, t, u


class FlextWebServiceBase[
    TDomainResult: t.JsonPayload | t.SequenceOf[t.JsonPayload],
](
    s[TDomainResult],
    ABC,
):
    """Base class for flext-web services with typed `web` settings access."""

    settings_type: Annotated[
        type | None,
        u.Field(description="Settings class for web services"),
    ] = FlextWebSettings

    @property
    @override
    def settings(self) -> FlextWebSettings:
        """Return the typed web settings bound to this service runtime."""
        return FlextSettings.fetch_global().fetch_namespace("web", FlextWebSettings)


s = FlextWebServiceBase

__all__: list[str] = ["FlextWebServiceBase", "s"]
